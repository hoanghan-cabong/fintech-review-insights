"""Tạo file ứng viên bổ sung cho tập ca khó: ca bị lừa và review không dấu.

Nguồn 200 ứng viên đầu không có ca "bị lừa mà tự chuyển tiền" nào và chỉ có 10 review
không dấu. File này lấy từ những review chưa xuất hiện trong hai tập đã gắn nhãn.
Chạy: .venv/bin/python src/make_hard_extra.py
"""
import csv
import random
import re

from config import CLEAN_DIR, LABEL_DIR, SEED, STUDY_APPS
from make_label_sets import LABEL_COLS, MONEY_WORDS, NEGATIVE_WORDS, has_diacritics

SCAM = re.compile(
    r"mạo danh|giả danh|bị lừa|lừa đảo|bị dụ|dụ dỗ|kẻ gian|lua dao|bi lua|scam|"
    r"cung cấp (mã )?otp|link lạ|bị hack|chiếm (đoạt|tài khoản)|lấy cắp|đánh cắp", re.I)
SCAM_PER_APP = 12
NO_DIACRITICS_TOTAL = 15

used = set()
for name in ["random_set_v2.csv", "hard_pool.csv"]:
    used |= {r["review_id"] for r in csv.DictReader((LABEL_DIR / name).open(encoding="utf-8-sig"))}

rows = [r for r in csv.DictReader((CLEAN_DIR / "reviews.csv").open(encoding="utf-8"))
        if r["app"] in STUDY_APPS and r["review_id"] not in used]

out = []
# Ca lừa đảo: ưu tiên review dài, vì review kể lại sự việc thường dài hơn review chỉ chửi "lừa đảo"
for app in STUDY_APPS:
    cand = [r for r in rows if r["app"] == app and int(r["n_words"]) >= 8 and SCAM.search(r["content"])]
    cand.sort(key=lambda r: -int(r["n_words"]))
    out += [dict(r, hint_scam=1) for r in cand[:SCAM_PER_APP]]

taken = {r["review_id"] for r in out}
nodiac = [r for r in rows if r["review_id"] not in taken and int(r["n_words"]) >= 6
          and not has_diacritics(r["content"])]
rng = random.Random(SEED)
out += [dict(r, hint_scam=0) for r in rng.sample(nodiac, min(NO_DIACRITICS_TOTAL, len(nodiac)))]
rng.shuffle(out)

base = ["review_id", "app", "score", "content"]
hints = ["hint_scam", "hint_money", "hint_no_diacritics", "hint_star_mismatch"]
dst = LABEL_DIR / "hard_extra.csv"
with dst.open("w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["pick"] + base + hints + LABEL_COLS)
    for r in out:
        text, score = r["content"], int(r["score"])
        h = [r["hint_scam"], int(bool(MONEY_WORDS.search(text))), int(not has_diacritics(text)),
             int(score >= 4 and bool(NEGATIVE_WORDS.search(text)))]
        w.writerow([""] + [r[c] for c in base] + h + [""] * len(LABEL_COLS))

n_scam = sum(r["hint_scam"] for r in out)
print(f"Đã tạo {dst.name}: {len(out)} ứng viên ({n_scam} nghi lừa đảo, {len(out) - n_scam} không dấu); "
      f"tổng review không dấu có thể chọn: {len(nodiac)}")
