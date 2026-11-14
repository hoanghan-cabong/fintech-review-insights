"""Phân loại phụ cho các review S1: cơ chế mất tiền là gì? (tuần 4, D023)

Đây là bước phân tích, không phải bộ phân loại chính, nên không có tập đáp án riêng.
Chất lượng được kiểm tra bằng cách đọc ngẫu nhiên một số ca (ghi trong decision log).
Chạy: .venv/bin/python src/s1_subtype.py
"""
import json
import subprocess
import time

from config import DATA, ROOT

CORPUS = DATA / "corpus"
TYPES = ["unauthorized_debit", "failed_txn_money_lost", "refund_delay", "account_frozen",
         "account_takeover", "scam", "other"]
SCHEMA = {"type": "object", "properties": {"results": {"type": "array", "items": {
    "type": "object",
    "properties": {"review_id": {"type": "string"}, "s1_type": {"type": "string", "enum": TYPES}},
    "required": ["review_id", "s1_type"]}}}, "required": ["results"]}


def main():
    import csv
    meta = {r["review_id"]: r for r in csv.DictReader((CORPUS / "sample.csv").open(encoding="utf-8"))}
    preds = [p for p in map(json.loads, (CORPUS / "preds_v2_opus.jsonl").open(encoding="utf-8"))
             if p["severity"] == "S1"]
    system = (ROOT / "prompts" / "s1_subtype_v1.md").read_text(encoding="utf-8")
    out = {}
    for i in range(0, len(preds), 30):
        batch = preds[i:i + 30]
        payload = json.dumps([{"review_id": p["review_id"], "text": meta[p["review_id"]]["content"]} for p in batch],
                             ensure_ascii=False)
        cmd = ["claude", "-p", "--model", "opus", "--tools", "", "--no-session-persistence", "--system-prompt", system,
               "--output-format", "json", "--json-schema", json.dumps(SCHEMA)]
        t0 = time.time()
        res = json.loads(subprocess.run(cmd, input=payload, capture_output=True, text=True, timeout=600, cwd=ROOT).stdout)
        data = res.get("structured_output") or json.loads(res["result"][res["result"].find("{"):res["result"].rfind("}") + 1])
        ids = {p["review_id"] for p in batch}
        for r in data["results"]:
            if r["review_id"] in ids:
                out[r["review_id"]] = r
        print(f"  lô {i // 30 + 1}: {len(batch)} review, {time.time() - t0:.0f}s", flush=True)
    with (CORPUS / "s1_subtypes.jsonl").open("w", encoding="utf-8") as f:
        for r in out.values():
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Đã phân loại {len(out)}/{len(preds)} review S1")


if __name__ == "__main__":
    main()
