"""Che thông tin cá nhân trong nội dung review và gộp 4 app thành một file CSV.

- Số điện thoại, email, dãy số dài (số tài khoản, số thẻ) được thay bằng nhãn.
- reviewId gốc của Google được thay bằng mã nội bộ (gp_<app>_<số thứ tự>).
- Số tiền như "500k", "1.000.000đ" được giữ nguyên vì cần cho việc chấm mức nghiêm trọng.
Chạy: .venv/bin/python src/anonymize.py
"""
import csv
import json
import re
from datetime import datetime

from config import APPS, CLEAN_DIR, RAW_DIR

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"(?<!\d)(?:\+?84|0)(?:[\s.\-]?\d){9,10}(?!\d)")
LONG_DIGITS = re.compile(r"(?<!\d)\d{9,19}(?!\d)")  # số tài khoản, số thẻ (không có dấu phân cách)


def mask(text: str) -> str:
    text = EMAIL.sub("[EMAIL]", text)
    text = PHONE.sub("[SĐT]", text)
    text = LONG_DIGITS.sub("[SỐ_TK]", text)
    return text


def main():
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    # n_words: dùng để lọc review "có nội dung" (xem decision log D014)
    fields = ["review_id", "app", "date", "score", "app_version", "thumbs_up",
              "n_words", "content", "has_reply", "reply_hours", "reply_content"]
    path = CLEAN_DIR / "reviews.csv"
    n_masked = 0
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for code in APPS:
            src = RAW_DIR / f"{code}.jsonl"
            # Đánh số từ review cũ nhất để mã ổn định khi lấy thêm dữ liệu mới
            rows = [json.loads(line) for line in src.open(encoding="utf-8")][::-1]
            for i, r in enumerate(rows, 1):
                content = (r["content"] or "").strip()
                masked = mask(content)
                n_masked += masked != content
                reply_hours = ""
                if r["repliedAt"]:
                    delta = datetime.fromisoformat(r["repliedAt"]) - datetime.fromisoformat(r["at"])
                    reply_hours = round(max(delta.total_seconds(), 0) / 3600, 1)
                w.writerow({
                    "review_id": f"gp_{code}_{i:05d}",
                    "app": code,
                    "date": r["at"][:10],
                    "score": r["score"],
                    "app_version": r["appVersion"] or r["reviewCreatedVersion"] or "",
                    "thumbs_up": r["thumbsUpCount"],
                    "n_words": len(masked.split()),
                    "content": masked,
                    "has_reply": int(bool(r["replyContent"])),
                    "reply_hours": reply_hours,
                    "reply_content": mask(r["replyContent"] or ""),
                })
    print(f"Đã ghi {path.relative_to(CLEAN_DIR.parent.parent)}; {n_masked} review có thông tin bị che")


if __name__ == "__main__":
    main()
