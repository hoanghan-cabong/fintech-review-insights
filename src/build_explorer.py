"""Đóng gói dữ liệu cho trang insight + chat (explorer/data.json).

Gồm: số liệu tổng hợp từ analyze.py và danh sách review trong mẫu đã phân loại
(nội dung đã ẩn danh, cắt tối đa 400 ký tự) để agent trong chat tra cứu.
Chạy sau analyze.py: .venv/bin/python src/build_explorer.py
"""
import csv
import json

from config import DATA, ROOT

CORPUS = DATA / "corpus"
OUT = ROOT / "explorer"


def main():
    OUT.mkdir(exist_ok=True)
    summary = json.loads((DATA / "analysis" / "summary.json").read_text(encoding="utf-8"))
    meta = {r["review_id"]: r for r in csv.DictReader((CORPUS / "sample.csv").open(encoding="utf-8"))}
    preds = {p["review_id"]: p for p in map(json.loads, (CORPUS / "preds_v2_opus.jsonl").open(encoding="utf-8"))}
    sub_f = CORPUS / "s1_subtypes.jsonl"
    subs = {p["review_id"]: p["s1_type"] for p in map(json.loads, sub_f.open(encoding="utf-8"))} if sub_f.exists() else {}
    reviews = []
    for rid, m in meta.items():
        p = preds.get(rid)
        if not p:
            continue
        reviews.append({
            "id": rid, "app": m["app"], "date": m["date"], "stars": int(m["score"]),
            "w": float(m["weight"]), "cat": p["category"], "sev": p["severity"], "flow": p["flow"],
            "s1": subs.get(rid), "replied": m["has_reply"] == "1",
            "reply_h": float(m["reply_hours"]) if m["reply_hours"] else None,
            "text": m["content"][:400], "ev": p.get("evidence") or "",
        })
    run = json.loads((CORPUS / "run_meta.json").read_text(encoding="utf-8"))
    test = json.loads((ROOT / "reports" / "eval_summary_test.json").read_text(encoding="utf-8"))["test"]
    ev = {k: test["agent_v2_opus"][k] for k in ("category", "s1_recall", "s1_precision")}
    evb = {k: test["baseline"][k] for k in ("category", "s1_recall", "s1_precision")}
    # Phát hiện chính do người phân tích viết sau khi đọc reports/insights.md (không sinh tự động)
    findings = json.loads((ROOT / "reports" / "key_findings.json").read_text(encoding="utf-8"))
    data = {"summary": summary, "reviews": reviews, "run": run, "eval": {"agent": ev, "baseline": evb},
            "period": "14/08–12/11/2026", "findings": findings}
    (OUT / "data.json").write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"explorer/data.json: {len(reviews)} review, {(OUT / 'data.json').stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
