"""Tạo file gắn lại mức nghiêm trọng từ lần gắn nhãn đầu (D017).

Giữ category / flow / social_engineering của lần 1, XOÁ mức nghiêm trọng và thời gian
để lần 2 không bị neo theo nhãn cũ. Thời gian lần 1 vẫn còn trong file pass1.
Chạy: .venv/bin/python src/make_relabel.py
"""
import csv

from config import LABEL_DIR

src = LABEL_DIR / "random_set_pass1.csv"
dst = LABEL_DIR / "random_set_v2.csv"

rows = list(csv.DictReader(src.open(encoding="utf-8-sig")))
cols = ["review_id", "app", "score", "content", "category", "severity", "flow", "social_engineering", "note"]
with dst.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    todo = 0
    for r in rows:
        # NON_ISSUE luôn là S4 theo định nghĩa, không cần gắn lại
        sev = "S4" if r["category"] == "NON_ISSUE" else ""
        todo += not sev
        w.writerow({**r, "severity": sev})
print(f"Đã tạo {dst.name}: {len(rows)} review, {todo} review cần gắn lại mức nghiêm trọng")
