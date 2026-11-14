"""Tạo file rà soát nhãn: những review mà Haiku và Opus cùng ra một đáp án nhưng khác nhãn tay (D020).

Cột category/severity/flow/social_engineering được điền sẵn bằng NHÃN TAY hiện tại.
Bạn chỉ sửa khi taxonomy ủng hộ cách hiểu khác, và ghi lý do vào cột note.
Nhãn gốc không bị ghi đè: golden.py áp các thay đổi từ file này lên trên.
Chạy: .venv/bin/python src/make_adjudication.py
"""
import csv
import json
import sys

from config import DATA, LABEL_DIR
from golden import load_golden

RUNS = ["agent_v1_haiku", "agent_v1_opus"]
KEY = ("category", "severity")


def main():
    gold = load_golden(apply_adjudication=False)
    preds = {r: {p["review_id"]: p for p in map(json.loads, (DATA / "preds" / f"{r}.jsonl").open(encoding="utf-8"))}
             for r in RUNS}
    rows = []
    for g in gold:
        ps = [preds[r][g["review_id"]] for r in RUNS]
        same = all(tuple(p[k] for k in KEY) == tuple(ps[0][k] for k in KEY) for p in ps)
        if same and tuple(ps[0][k] for k in KEY) != tuple(g[k] for k in KEY):
            m = ps[-1]  # Opus
            rows.append({
                "review_id": g["review_id"], "app": g["app"], "score": g["score"], "content": g["content"],
                "split": g["split"],
                "gold_label": f"{g['category']} / {g['severity']}" + (f" / {g['flow']}" if g["flow"] else ""),
                "model_label": f"{m['category']} / {m['severity']}" + (f" / {m['flow']}" if m["flow"] else ""),
                "model_evidence": m["evidence"],
                "category": g["category"], "severity": g["severity"], "flow": g["flow"],
                "social_engineering": g["social_engineering"], "note": "",
            })
    # Ưu tiên các ca liên quan đến S1 lên đầu
    rows.sort(key=lambda r: ("S1" not in r["gold_label"] and "S1" not in r["model_label"], r["review_id"]))
    dst = LABEL_DIR / "adjudication.csv"
    if dst.exists() and "--force" not in sys.argv:
        sys.exit(f"{dst.name} đã tồn tại (có thể chứa kết quả rà soát). Thêm --force để ghi đè.")
    with dst.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Đã tạo {dst.name}: {len(rows)} ca cần rà soát")


if __name__ == "__main__":
    main()
