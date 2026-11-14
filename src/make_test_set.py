"""Tạo tập kiểm tra cuối cùng (D021): 80 review ngẫu nhiên chưa từng xuất hiện ở bất kỳ file nào.

Gắn nhãn tập này TRƯỚC khi chạy model trên nó. Chỉ dùng để báo cáo kết quả cuối, không dùng để sửa prompt.
Chạy: .venv/bin/python src/make_test_set.py
"""
import csv
import random
import sys

from config import CLEAN_DIR, LABEL_DIR, MIN_WORDS, STUDY_APPS

PER_APP = 20
SEED = 2026  # khác seed của tập ngẫu nhiên ban đầu

dst = LABEL_DIR / "test_set.csv"
if dst.exists() and "--force" not in sys.argv:
    sys.exit(f"{dst.name} đã tồn tại (có thể đã gắn nhãn). Thêm --force để ghi đè.")

seen = set()
for f in LABEL_DIR.glob("*.csv"):
    if f.name != dst.name:
        seen |= {r["review_id"] for r in csv.DictReader(f.open(encoding="utf-8-sig"))}

rows = [r for r in csv.DictReader((CLEAN_DIR / "reviews.csv").open(encoding="utf-8"))
        if r["app"] in STUDY_APPS and int(r["n_words"]) >= MIN_WORDS and r["review_id"] not in seen]
rng = random.Random(SEED)
sample = []
for app in STUDY_APPS:
    pool = [r for r in rows if r["app"] == app]
    sample += rng.sample(pool, PER_APP)
rng.shuffle(sample)

cols = ["review_id", "app", "score", "content", "category", "severity", "flow", "social_engineering", "note"]
with dst.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in sample:
        w.writerow({**r, "category": "", "severity": "", "flow": "", "social_engineering": "", "note": ""})
print(f"Đã tạo {dst.name}: {len(sample)} review ({PER_APP} mỗi app), loại trừ {len(seen)} review đã dùng")
