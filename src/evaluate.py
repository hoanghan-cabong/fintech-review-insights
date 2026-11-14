"""Chấm baseline và các lần chạy agent trên tập đáp án, xuất báo cáo.

Chỉ số chính tính trên tập ngẫu nhiên (PRD §3.1). Tập ca khó báo cáo riêng.
Mọi tỷ lệ kèm khoảng tin cậy 95% (Wilson).
Chạy: .venv/bin/python src/evaluate.py
"""
import json
import math
import re
import sys
from collections import Counter

from config import DATA, ROOT
from golden import load_golden, load_test

PRED_DIR = DATA / "preds"
REPORT_DIR = ROOT / "reports"
SEV_RANK = {"S1": 1, "S2": 2, "S3": 3, "S4": 4}


def wilson(k: int, n: int) -> tuple[float, float, float]:
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p, z = k / n, 1.96
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0, c - h), min(1, c + h)


def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return "–" if n == 0 else f"{p:.0%} ({k}/{n}; {lo:.0%}–{hi:.0%})"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip().lower()


def load_preds(pred_dir) -> dict[str, dict]:
    runs = {}
    for f in sorted(pred_dir.glob("*.jsonl")):
        runs[f.stem] = {p["review_id"]: p for p in map(json.loads, f.open(encoding="utf-8"))}
    return runs


def metrics(gold: list[dict], preds: dict) -> dict:
    rows = [(g, preds.get(g["review_id"])) for g in gold]
    rows = [(g, p) for g, p in rows if p]
    n = len(rows)
    cat_ok = sum(g["category"] == p["category"] for g, p in rows)
    sev_ok = sum(g["severity"] == p["severity"] for g, p in rows)
    sev_pm1 = sum(abs(SEV_RANK[g["severity"]] - SEV_RANK[p["severity"]]) <= 1 for g, p in rows)
    s1_gold = [(g, p) for g, p in rows if g["severity"] == "S1"]
    s1_pred = [(g, p) for g, p in rows if p["severity"] == "S1"]
    txn = [(g, p) for g, p in rows if g["category"] == "TXN_FAILURE" and p["category"] == "TXN_FAILURE"]
    ev = [(g, p) for g, p in rows if p.get("evidence") is not None and p["category"] != "NON_ISSUE"]
    ev_ok = sum(bool(norm(p["evidence"])) and norm(p["evidence"]) in norm(g["content"]) for g, p in ev)
    return {
        "n": n,
        "category": (cat_ok, n),
        "severity": (sev_ok, n),
        "severity_pm1": (sev_pm1, n),
        "s1_recall": (sum(p["severity"] == "S1" for _, p in s1_gold), len(s1_gold)),
        "s1_precision": (sum(g["severity"] == "S1" for g, _ in s1_pred), len(s1_pred)),
        "flow": (sum(g["flow"] == p["flow"] for g, p in txn), len(txn)),
        "evidence": (ev_ok, len(ev)),
    }


def routing(gold, agent, base):
    """Quy tắc chuyển duyệt (PRD §5): agent đoán S1, hoặc agent và baseline bất đồng về S1."""
    routed = {g["review_id"] for g in gold
              if agent[g["review_id"]]["severity"] == "S1"
              or (agent[g["review_id"]]["severity"] == "S1") != (base[g["review_id"]]["severity"] == "S1")}
    s1_err = [g for g in gold if (g["severity"] == "S1") != (agent[g["review_id"]]["severity"] == "S1")]
    caught = [g for g in s1_err if g["review_id"] in routed]
    return len(routed), len(gold), len(caught), len(s1_err)


def per_category(gold, preds, min_n=5):
    by = Counter(g["category"] for g in gold)
    out = []
    for cat, n in by.most_common():
        if n < min_n:
            continue
        rows = [g for g in gold if g["category"] == cat]
        out.append((cat, sum(preds[g["review_id"]]["category"] == cat for g in rows), n))
    return out


def error_dump(gold, preds, run):
    lines = [f"# Lỗi của {run}\n", "Chỉ liệt kê review sai category hoặc sai S1/không S1.\n"]
    for g in gold:
        p = preds[g["review_id"]]
        s1_wrong = (g["severity"] == "S1") != (p["severity"] == "S1")
        if g["category"] != p["category"] or s1_wrong:
            tag = "S1-MISS" if g["severity"] == "S1" and p["severity"] != "S1" else \
                  "S1-FALSE" if s1_wrong else "CAT"
            lines.append(f"- **[{tag}] {g['review_id']}** ({g['split']}): "
                         f"đáp án `{g['category']}/{g['severity']}` · dự đoán `{p['category']}/{p['severity']}`  \n"
                         f"  > {g['content'][:300]}  \n"
                         f"  evidence: _{p.get('evidence') or ''}_\n")
    (REPORT_DIR / f"errors_{run}.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    REPORT_DIR.mkdir(exist_ok=True)
    test = "test" in sys.argv[1:]
    pred_dir = PRED_DIR / "test" if test else PRED_DIR
    suffix = "_test" if test else ""
    runs = load_preds(pred_dir)
    if test:
        gold = load_test()
        splits = {"test": gold}
        out = ["# Báo cáo eval: TẬP KIỂM TRA CUỐI (D021)\n",
               f"{len(gold)} review ngẫu nhiên, gắn nhãn trước khi chạy model, không dùng để sửa prompt. "
               "Khoảng trong ngoặc là khoảng tin cậy 95%.\n"]
    else:
        gold = load_golden()
        splits = {"random": [g for g in gold if g["split"] == "random"],
                  "hard": [g for g in gold if g["split"] == "hard"]}
        raw = {r["review_id"]: r for r in load_golden(apply_adjudication=False)}
        changed = [g for g in gold if any(g[k] != raw[g["review_id"]][k] for k in ("category", "severity", "flow"))]
        out = ["# Báo cáo eval: tập phát triển\n",
               f"Tập đáp án: {len(splits['random'])} review ngẫu nhiên, {len(splits['hard'])} ca khó. "
               "Khoảng trong ngoặc là khoảng tin cậy 95%.\n",
               f"Nhãn đã sửa sau vòng rà soát (D020, D021): {len(changed)} review.\n"]
    main_split = next(iter(splits))
    summary = {}
    labels = [("category", "Độ chính xác category"), ("severity", "Mức nghiêm trọng (đúng hẳn)"),
              ("severity_pm1", "Mức nghiêm trọng (lệch ≤ 1 bậc)"), ("s1_recall", "**Recall S1**"),
              ("s1_precision", "**Precision S1**"), ("flow", "Flow (khi cùng là TXN_FAILURE)"),
              ("evidence", "Trích dẫn khớp nguyên văn")]
    for split, g in splits.items():
        out.append(f"\n## Tập {({'random': 'ngẫu nhiên (chỉ số chính)', 'hard': 'ca khó', 'test': 'kiểm tra'})[split]}\n")
        out.append("| Chỉ số | " + " | ".join(runs) + " |")
        out.append("|---|" + "---|" * len(runs))
        ms = {r: metrics(g, p) for r, p in runs.items()}
        summary[split] = {r: {k: v for k, v in m.items()} for r, m in ms.items()}
        for key, label in labels:
            out.append(f"| {label} | " + " | ".join(fmt(*ms[r][key]) for r in runs) + " |")

    base = runs.get("baseline")
    out.append("\n## Theo category (tập chính, category có ≥ 5 mẫu)\n")
    out.append("| Category | " + " | ".join(runs) + " |")
    out.append("|---|" + "---|" * len(runs))
    cats = per_category(splits[main_split], next(iter(runs.values())))
    for cat, _, n in cats:
        cells = []
        for r, p in runs.items():
            k = sum(p[g["review_id"]]["category"] == cat for g in splits[main_split] if g["category"] == cat)
            cells.append(f"{k}/{n}")
        out.append(f"| {cat} | " + " | ".join(cells) + " |")

    if base:
        out.append("\n## Quy tắc chuyển sang người duyệt (cả hai tập)\n")
        out.append("| Lần chạy | Review bị chuyển duyệt | Lỗi S1 của agent được bắt |")
        out.append("|---|---|---|")
        for r, p in runs.items():
            if r == "baseline":
                continue
            routed, n, caught, errs = routing(gold, p, base)
            out.append(f"| {r} | {routed}/{n} ({routed / n:.0%}) | {caught}/{errs} |")

        out.append("\n## Tiêu chí thất bại (PRD §3.3), trên tập chính\n")
        bm = summary[main_split]["baseline"]
        for r in runs:
            if r == "baseline":
                continue
            am = summary[main_split][r]
            pa = lambda m, k: m[k][0] / m[k][1] if m[k][1] else 0
            d_cat = pa(am, "category") - pa(bm, "category")
            d_rec = pa(am, "s1_recall") - pa(bm, "s1_recall")
            ratio = pa(bm, "category") / pa(am, "category") if pa(am, "category") else 0
            out.append(f"- **{r}**: hơn baseline {d_cat:+.0%} ở category, {d_rec:+.0%} ở recall S1 "
                       f"(mục tiêu ≥ +10 điểm). Baseline đạt {ratio:.0%} chất lượng category của agent "
                       f"(ngưỡng thất bại ≥ 90%).")

    for f in sorted(pred_dir.glob("*.meta.json")):
        m = json.loads(f.read_text(encoding="utf-8"))
        out.append(f"\n- Chi phí và thời gian `{m['run']}`: {m['n']} review, {m['seconds']} giây, "
                   f"${m['cost_usd']} quy đổi API (≈ ${m['cost_usd'] / m['n'] * 1000:.2f} / 1.000 review).")

    for r, p in runs.items():
        error_dump(gold, p, r + suffix)
    (REPORT_DIR / f"eval_report{suffix}.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    (REPORT_DIR / f"eval_summary{suffix}.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
