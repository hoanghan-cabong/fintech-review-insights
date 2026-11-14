"""Phân tích so sánh 4 ví từ kết quả của agent trên mẫu lớn (tuần 4).

- Mọi tỷ lệ đều có trọng số theo tầng lấy mẫu (xem classify_corpus.py) và tính trong nhóm
  REVIEW PHÀN NÀN (category khác NON_ISSUE), theo D016.
- Khoảng tin cậy 95% dùng Wilson với cỡ mẫu hiệu dụng (Kish) để tính đến trọng số.
- Điểm ưu tiên = tỷ trọng × trọng số mức nghiêm trọng (PRD §6); kiểm tra độ nhạy bằng 3 bộ trọng số.
Chạy: .venv/bin/python src/analyze.py
"""
import csv
import json
import re
from collections import Counter
import math
from collections import defaultdict

from config import DATA, ROOT, STUDY_APPS

CORPUS = DATA / "corpus"
OUT = DATA / "analysis"
REPORT = ROOT / "reports" / "insights.md"
APP_NAME = {"momo": "MoMo", "zalopay": "ZaloPay", "shopeepay": "ShopeePay", "viettelmoney": "Viettel Money"}
CATS = ["TXN_FAILURE", "AUTH_ACCESS", "ONBOARD_EKYC", "FRAUD_SECURITY", "FEES_LIMITS", "SUPPORT",
        "PROMO_REWARDS", "APP_EXPERIENCE"]
CAT_VI = {"TXN_FAILURE": "Giao dịch lỗi", "AUTH_ACCESS": "Đăng nhập / truy cập", "ONBOARD_EKYC": "Đăng ký / eKYC",
          "FRAUD_SECURITY": "Lừa đảo / bảo mật", "FEES_LIMITS": "Phí / hạn mức", "SUPPORT": "CSKH",
          "PROMO_REWARDS": "Khuyến mãi", "APP_EXPERIENCE": "Trải nghiệm app"}
FLOWS = ["transfer", "payment", "topup_withdraw", "credit_bnpl", "unknown"]
FLOW_VI = {"transfer": "Chuyển tiền", "payment": "Thanh toán", "topup_withdraw": "Nạp / rút / liên kết",
           "credit_bnpl": "Trả sau / vay", "unknown": "Không rõ"}
WEIGHT_SETS = {"A (mặc định)": {"S1": 10, "S2": 5, "S3": 2, "S4": 1},
               "B (giãn ít)": {"S1": 5, "S2": 3, "S3": 2, "S4": 1},
               "C (S1 rất nặng)": {"S1": 20, "S2": 5, "S3": 2, "S4": 1}}


def wci(mask_w: list[tuple[bool, float]]):
    """Tỷ lệ có trọng số + khoảng tin cậy Wilson với cỡ mẫu hiệu dụng."""
    sw = sum(w for _, w in mask_w)
    if sw == 0:
        return float("nan"), float("nan"), float("nan"), 0
    p = sum(w for m, w in mask_w if m) / sw
    n_eff = sw ** 2 / sum(w * w for _, w in mask_w)
    z = 1.96
    d = 1 + z * z / n_eff
    c = (p + z * z / (2 * n_eff)) / d
    h = z * math.sqrt(p * (1 - p) / n_eff + z * z / (4 * n_eff ** 2)) / d
    return p, max(0, c - h), min(1, c + h), len(mask_w)


def pct(t):
    p, lo, hi, n = t
    return "–" if n == 0 else f"{p:.0%} ({lo:.0%}–{hi:.0%})"


def wmedian(vals: list[tuple[float, float]]):
    vals = sorted(vals)
    if not vals:
        return float("nan")
    half, acc = sum(w for _, w in vals) / 2, 0
    for v, w in vals:
        acc += w
        if acc >= half:
            return v
    return vals[-1][0]


def load():
    meta = {r["review_id"]: r for r in csv.DictReader((CORPUS / "sample.csv").open(encoding="utf-8"))}
    preds = {p["review_id"]: p for p in map(json.loads, (CORPUS / "preds_v2_opus.jsonl").open(encoding="utf-8"))}
    sub_f = CORPUS / "s1_subtypes.jsonl"
    subs = {p["review_id"]: p for p in map(json.loads, sub_f.open(encoding="utf-8"))} if sub_f.exists() else {}
    rows = []
    for rid, m in meta.items():
        if rid in preds:
            rows.append({**m, **preds[rid], "weight": float(m["weight"]), "s1_type": subs.get(rid, {}).get("s1_type")})
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load()
    comp = [r for r in rows if r["category"] != "NON_ISSUE"]
    by_app = {a: [r for r in comp if r["app"] == a] for a in STUDY_APPS}
    out = ["# Insight: so sánh 4 ví điện tử\n",
           f"Mẫu: {len(rows)} review (≥ 5 từ, 14/08–12/11/2026), lấy mẫu phân tầng theo app và nhóm sao, "
           "có trọng số. Phân loại bằng Opus + prompt v2 (D022). **Mọi tỷ lệ tính trong nhóm review phàn nàn** "
           "(D016). Trong ngoặc là khoảng tin cậy 95%.\n"]
    data = {"apps": {}, "categories": CATS, "flows": FLOWS}

    # 1. Tổng quan
    out.append("## 1. Tổng quan\n")
    out.append("| | " + " | ".join(APP_NAME[a] for a in STUDY_APPS) + " |")
    out.append("|---|" + "---|" * len(STUDY_APPS))
    row_n, row_comp, row_s1 = [], [], []
    for a in STUDY_APPS:
        all_a = [r for r in rows if r["app"] == a]
        row_n.append(str(len(all_a)))
        row_comp.append(pct(wci([(r["category"] != "NON_ISSUE", r["weight"]) for r in all_a])))
        row_s1.append(pct(wci([(r["severity"] == "S1", r["weight"]) for r in by_app[a]])))
        data["apps"][a] = {"n_sample": len(all_a), "n_complaints": len(by_app[a])}
    out.append("| Review trong mẫu | " + " | ".join(row_n) + " |")
    out.append("| Review phàn nàn (trên review ≥ 5 từ)* | " + " | ".join(row_comp) + " |")
    out.append("| **Tỷ trọng S1 trong review phàn nàn** | " + " | ".join(row_s1) + " |")
    out.append("\n\\* Chỉ để tham khảo: tỷ lệ này bị ảnh hưởng bởi đợt tăng review khen (D016).\n")

    # 2. Tỷ trọng category
    out.append("## 2. Khi bị phàn nàn, người dùng phàn nàn về điều gì?\n")
    out.append("| Category | " + " | ".join(APP_NAME[a] for a in STUDY_APPS) + " |")
    out.append("|---|" + "---|" * len(STUDY_APPS))
    for c in CATS:
        cells = []
        for a in STUDY_APPS:
            t = wci([(r["category"] == c, r["weight"]) for r in by_app[a]])
            data["apps"][a].setdefault("category_share", {})[c] = t[:3]
            cells.append(pct(t))
        out.append(f"| {CAT_VI[c]} | " + " | ".join(cells) + " |")

    # 3. Điểm yếu tương đối: chênh lệch so với trung bình 3 ví còn lại
    out.append("\n## 3. Điểm yếu tương đối (chênh lệch so với trung bình 3 ví còn lại, điểm %)\n")
    out.append("Số dương nghĩa là ví này bị phàn nàn về vấn đề đó **nhiều hơn** thị trường. Chỉ nêu các chênh lệch ≥ 5 điểm.\n")
    for a in STUDY_APPS:
        gaps = []
        for c in CATS:
            mine = data["apps"][a]["category_share"][c][0]
            others = [data["apps"][b]["category_share"][c][0] for b in STUDY_APPS if b != a]
            gaps.append((mine - sum(others) / len(others), c))
        data["apps"][a]["gaps"] = {c: g for g, c in gaps}
        big = [f"{CAT_VI[c]} {g:+.0%}" for g, c in sorted(gaps, reverse=True) if abs(g) >= 0.05]
        out.append(f"- **{APP_NAME[a]}:** " + (", ".join(big) if big else "không có chênh lệch lớn"))

    # 4. Giao dịch lỗi theo flow
    out.append("\n## 4. Giao dịch lỗi xảy ra ở luồng nào? (trong review TXN_FAILURE)\n")
    out.append("| Flow | " + " | ".join(APP_NAME[a] for a in STUDY_APPS) + " |")
    out.append("|---|" + "---|" * len(STUDY_APPS))
    for fl in FLOWS:
        cells = []
        for a in STUDY_APPS:
            tx = [r for r in by_app[a] if r["category"] == "TXN_FAILURE"]
            t = wci([(r["flow"] == fl, r["weight"]) for r in tx])
            data["apps"][a].setdefault("flow_share", {})[fl] = t[:3]
            cells.append(pct(t) + f" · n={len(tx)}" if fl == FLOWS[0] else pct(t))
        out.append(f"| {FLOW_VI[fl]} | " + " | ".join(cells) + " |")

    # 5. S1: loại nào?
    s1 = [r for r in comp if r["severity"] == "S1"]
    if any(r["s1_type"] for r in s1):
        types = sorted({r["s1_type"] for r in s1 if r["s1_type"]})
        out.append("\n## 5. Ca S1 (mất tiền / rủi ro mất tiền) thuộc loại nào?\n")
        out.append("| Loại S1 | Toàn thị trường | " + " | ".join(APP_NAME[a] for a in STUDY_APPS) + " |")
        out.append("|---|---|" + "---|" * len(STUDY_APPS))
        for t_ in types:
            cells = [pct(wci([(r["s1_type"] == t_, r["weight"]) for r in s1]))]
            for a in STUDY_APPS:
                sa = [r for r in s1 if r["app"] == a]
                tt = wci([(r["s1_type"] == t_, r["weight"]) for r in sa])
                data["apps"][a].setdefault("s1_type_share", {})[t_] = tt[:3]
                cells.append(pct(tt) + (f" · n={len(sa)}" if t_ == types[0] else ""))
            out.append(f"| {t_} | " + " | ".join(cells) + " |")

    # 6. Phản hồi của nhà phát triển
    out.append("\n## 6. Đội phát triển phản hồi review phàn nàn thế nào?\n")
    out.append("| | " + " | ".join(APP_NAME[a] for a in STUDY_APPS) + " |")
    out.append("|---|" + "---|" * len(STUDY_APPS))
    for label, sev in [("Tỷ lệ phản hồi, mọi mức", None), ("Tỷ lệ phản hồi, chỉ S1", "S1")]:
        cells = []
        for a in STUDY_APPS:
            rs = [r for r in by_app[a] if sev is None or r["severity"] == sev]
            t = wci([(r["has_reply"] == "1", r["weight"]) for r in rs])
            data["apps"][a][f"reply_rate_{sev or 'all'}"] = t[:3]
            cells.append(pct(t))
        out.append(f"| {label} | " + " | ".join(cells) + " |")
    for label, sev in [("Trung vị giờ phản hồi, mọi mức", None), ("Trung vị giờ phản hồi, chỉ S1", "S1")]:
        cells = []
        for a in STUDY_APPS:
            vals = [(float(r["reply_hours"]), r["weight"]) for r in by_app[a]
                    if r["reply_hours"] and (sev is None or r["severity"] == sev)]
            m = wmedian(vals)
            data["apps"][a][f"reply_hours_{sev or 'all'}"] = m
            cells.append("–" if math.isnan(m) else f"{m:.1f} giờ")
        out.append(f"| {label} | " + " | ".join(cells) + " |")

    # 6b. Phản hồi có phải văn mẫu không? Một phản hồi được coi là "văn mẫu" khi 70 ký tự đầu
    # (đã thay số bằng #) trùng với ít nhất 5 phản hồi khác của cùng ví.
    clean_rows = {r["review_id"]: r for r in csv.DictReader((DATA / "clean" / "reviews.csv").open(encoding="utf-8"))}

    def head(t):
        t = re.sub(r"\d+", "#", t.lower())
        return re.sub(r"\s+", " ", t)[:70]
    cells_tpl, cells_var = [], []
    for a in STUDY_APPS:
        reps = [clean_rows[r["review_id"]]["reply_content"] for r in by_app[a]
                if clean_rows[r["review_id"]]["reply_content"]]
        cnt = Counter(head(x) for x in reps)
        tpl = sum(1 for x in reps if cnt[head(x)] >= 5) / len(reps) if reps else float("nan")
        data["apps"][a]["reply_template_share"] = tpl
        data["apps"][a]["reply_distinct_openings"] = len(cnt) / len(reps) if reps else float("nan")
        cells_tpl.append(f"{tpl:.0%}")
        cells_var.append(f"{len(cnt)} / {len(reps)}")
    out.append("| Phản hồi là văn mẫu (≥ 5 phản hồi cùng mở đầu) | " + " | ".join(cells_tpl) + " |")
    out.append("| Số kiểu mở đầu khác nhau / số phản hồi | " + " | ".join(cells_var) + " |")
    out.append("\nTỷ lệ và tốc độ phản hồi chủ yếu đo **mức tự động hoá**: phần lớn phản hồi là văn mẫu, "
               "nên không nên đọc là chất lượng chăm sóc khách hàng.\n")

    # 7. Ưu tiên và độ nhạy
    out.append("\n## 7. Vấn đề nên ưu tiên (điểm = tỷ trọng × trọng số mức nghiêm trọng) và độ nhạy\n")
    out.append("| Ví | " + " | ".join(f"Top 3 theo bộ trọng số {k}" for k in WEIGHT_SETS) + " | Ổn định? |")
    out.append("|---|" + "---|" * len(WEIGHT_SETS) + "---|")
    for a in STUDY_APPS:
        tw = sum(r["weight"] for r in by_app[a])
        tops = {}
        for name, ws in WEIGHT_SETS.items():
            score = defaultdict(float)
            for r in by_app[a]:
                score[r["category"]] += r["weight"] * ws[r["severity"]] / tw
            tops[name] = [c for c, _ in sorted(score.items(), key=lambda x: -x[1])[:3]]
            if name.startswith("A"):
                data["apps"][a]["priority"] = dict(sorted(score.items(), key=lambda x: -x[1]))
        stable = len({tuple(v) for v in tops.values()}) == 1
        same_set = len({frozenset(v) for v in tops.values()}) == 1
        verdict = "✅ giữ nguyên thứ tự" if stable else ("≈ cùng 3 vấn đề, đổi thứ tự" if same_set else "⚠️ thay đổi")
        out.append(f"| {APP_NAME[a]} | " + " | ".join(", ".join(CAT_VI[c] for c in v) for v in tops.values())
                   + f" | {verdict} |")

    # 8. Trích dẫn ví dụ cho S1
    out.append("\n## 8. Ví dụ trích dẫn S1 (nguyên văn, đã ẩn danh)\n")
    for a in STUDY_APPS:
        ex = [r for r in by_app[a] if r["severity"] == "S1" and r.get("evidence")][:3]
        for r in ex:
            out.append(f"- **{APP_NAME[a]}** `{r['category']}` {('· ' + r['s1_type']) if r['s1_type'] else ''}: "
                       f"\"{r['evidence']}\"")

    (OUT / "summary.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
