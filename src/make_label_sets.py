"""Tạo file gắn nhãn tay cho tập ngẫu nhiên và nguồn ứng viên cho tập ca khó.

Chỉ lấy từ review "có nội dung" (>= MIN_WORDS từ). Review ngắn hơn ("ok", "tốt")
được gán NON_ISSUE bằng quy tắc, không cần agent và không cần gắn nhãn (D014).

Đầu ra (mở bằng Google Sheets hoặc Excel):
- data/labels/random_set.csv : 25 review mỗi app, gắn nhãn toàn bộ, nhớ bấm giờ
- data/labels/hard_pool.csv  : ~200 ứng viên kèm gợi ý; đánh dấu pick=1 cho 40 review
                               rồi gắn nhãn những review đã chọn
Chạy: .venv/bin/python src/make_label_sets.py
"""
import csv
import random
import re
import unicodedata

from config import CLEAN_DIR, LABEL_DIR, MIN_WORDS, SEED, STUDY_APPS

PER_APP_RANDOM = 25
POOL_PER_APP = 50

LABEL_COLS = ["category", "severity", "flow", "social_engineering", "note"]
MONEY_WORDS = re.compile(
    r"trừ tiền|mất tiền|chưa hoàn|không hoàn|hoàn tiền|lừa|treo|tru tien|mat tien|"
    r"chua hoan|lua dao|bị trừ|bi tru|không nhận được tiền|chiếm|hack", re.I)
NEGATIVE_WORDS = re.compile(r"lỗi|tệ|kém|không được|chán|lừa|mất|loi|te|kem", re.I)


def has_diacritics(text: str) -> bool:
    return any(unicodedata.decomposition(c) for c in text if c.isalpha())


def main():
    rows = list(csv.DictReader((CLEAN_DIR / "reviews.csv").open(encoding="utf-8")))
    rows = [r for r in rows if r["app"] in STUDY_APPS and int(r["n_words"]) >= MIN_WORDS]
    rng = random.Random(SEED)
    LABEL_DIR.mkdir(parents=True, exist_ok=True)

    random_set, pool = [], []
    for app in STUDY_APPS:
        app_rows = [r for r in rows if r["app"] == app]
        rng.shuffle(app_rows)
        random_set += app_rows[:PER_APP_RANDOM]
        pool += app_rows[PER_APP_RANDOM:PER_APP_RANDOM + POOL_PER_APP * 4]  # lấy rộng rồi lọc

    # Nguồn ca khó: ưu tiên review có gợi ý, nhưng vẫn giữ một phần không có gợi ý
    # để tập ca khó không chỉ chứa những ca mà baseline từ khoá bắt được.
    def hints(r):
        text, score = r["content"], int(r["score"])
        return {
            "hint_money": int(bool(MONEY_WORDS.search(text))),
            "hint_no_diacritics": int(not has_diacritics(text)),
            "hint_star_mismatch": int(score >= 4 and bool(NEGATIVE_WORDS.search(text))),
        }

    hard = []
    for app in STUDY_APPS:
        cand = [dict(r, **hints(r)) for r in pool if r["app"] == app]
        flagged = [r for r in cand if any(r[k] for k in r if k.startswith("hint_"))]
        plain = [r for r in cand if r not in flagged]
        hard += (flagged[: int(POOL_PER_APP * 0.7)] + plain)[:POOL_PER_APP]
    rng.shuffle(hard)

    base = ["review_id", "app", "score", "content"]
    with (LABEL_DIR / "random_set.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(base + LABEL_COLS)
        for r in random_set:
            w.writerow([r[c] for c in base] + [""] * len(LABEL_COLS))

    hint_cols = ["hint_money", "hint_no_diacritics", "hint_star_mismatch"]
    with (LABEL_DIR / "hard_pool.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pick"] + base + hint_cols + LABEL_COLS)
        for r in hard:
            w.writerow([""] + [r[c] for c in base] + [r[c] for c in hint_cols] + [""] * len(LABEL_COLS))

    print(f"random_set.csv: {len(random_set)} review · hard_pool.csv: {len(hard)} ứng viên")


if __name__ == "__main__":
    main()
