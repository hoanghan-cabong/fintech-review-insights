"""Đóng gói dữ liệu rút gọn để nhúng công cụ vào trang portfolio.

Khác với build_explorer.py: chỉ giữ một tập review đủ để agent trong trang tra cứu và
trích dẫn (toàn bộ S1 + mẫu của các mức khác), nội dung cắt ngắn, nhằm giữ kích thước nhỏ
và không đăng lại toàn bộ dữ liệu thô.
Chạy: .venv/bin/python src/build_portfolio_data.py
"""
import csv
import json
import random

from config import DATA, ROOT, STUDY_APPS

CORPUS = DATA / "corpus"
OUT = ROOT / "portfolio_tool"
KEEP_PER_APP_NON_S1 = 55
SEED = 9


def main():
    OUT.mkdir(exist_ok=True)
    meta = {r["review_id"]: r for r in csv.DictReader((CORPUS / "sample.csv").open(encoding="utf-8"))}
    preds = {p["review_id"]: p for p in map(json.loads, (CORPUS / "preds_v2_opus.jsonl").open(encoding="utf-8"))}
    subs = {p["review_id"]: p["s1_type"] for p in map(json.loads, (CORPUS / "s1_subtypes.jsonl").open(encoding="utf-8"))}

    rows = []
    for rid, m in meta.items():
        p = preds.get(rid)
        if not p:
            continue
        rows.append({
            "id": rid, "app": m["app"], "date": m["date"], "stars": int(m["score"]),
            "w": round(float(m["weight"]), 3), "cat": p["category"], "sev": p["severity"],
            "flow": p["flow"], "s1": subs.get(rid), "replied": m["has_reply"] == "1",
            "text": m["content"][:260], "ev": (p.get("evidence") or "")[:160],
        })

    rng = random.Random(SEED)
    keep = [r for r in rows if r["sev"] == "S1"]
    for app in STUDY_APPS:
        for sev in ("S2", "S3", "S4"):
            pool = [r for r in rows if r["app"] == app and r["sev"] == sev]
            keep += rng.sample(pool, min(KEEP_PER_APP_NON_S1, len(pool)))
    rng.shuffle(keep)

    summary = json.loads((DATA / "analysis" / "summary.json").read_text(encoding="utf-8"))
    findings = json.loads((ROOT / "reports" / "key_findings.json").read_text(encoding="utf-8"))["en"]
    test = json.loads((ROOT / "reports" / "eval_summary_test.json").read_text(encoding="utf-8"))["test"]
    run = json.loads((CORPUS / "run_meta.json").read_text(encoding="utf-8"))

    data = {
        "period": "14 Aug – 12 Nov 2026",
        "corpus": {"classified": run["n_pred"], "minutes": round(run["wall_seconds"] / 60),
                   "cost_per_1k": round(run["cost_usd_equiv"] / run["n_pred"] * 1000, 2),
                   "scraped": 29078, "sampled_from": len(rows)},
        "summary": summary,
        "findings": findings,
        "eval": {k: {m: test[k][m] for m in ("category", "severity_pm1", "s1_recall", "s1_precision", "evidence")}
                 for k in ("agent_v2_opus", "baseline")},
        "reviews": keep,
    }
    path = OUT / "data.json"
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{path.name}: {len(keep)} review ({sum(r['sev'] == 'S1' for r in keep)} S1), "
          f"{path.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
