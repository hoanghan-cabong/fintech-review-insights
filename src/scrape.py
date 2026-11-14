"""Lấy review công khai trên Google Play của 4 ví điện tử.

Bỏ tên và ảnh người dùng ngay khi lấy về, không bao giờ ghi xuống đĩa.
Chạy: .venv/bin/python src/scrape.py
"""
import json
import time
from datetime import datetime, timedelta

from google_play_scraper import Sort, reviews

from config import APPS, COUNTRY, DAYS, LANG, MAX_PER_APP, RAW_DIR

KEEP = ["reviewId", "content", "score", "thumbsUpCount", "reviewCreatedVersion",
        "appVersion", "at", "replyContent", "repliedAt"]


def fetch(app_id: str, cutoff: datetime) -> list[dict]:
    out, token = [], None
    while len(out) < MAX_PER_APP:
        batch, token = reviews(app_id, lang=LANG, country=COUNTRY, sort=Sort.NEWEST,
                               count=200, continuation_token=token)
        if not batch:
            break
        for r in batch:
            if r["at"] < cutoff:
                return out
            out.append({k: r.get(k) for k in KEEP})
        if token is None or token.token is None:
            break
        time.sleep(1)  # lịch sự với máy chủ
    return out[:MAX_PER_APP]


def to_json(v):
    return v.isoformat() if isinstance(v, datetime) else v


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cutoff = datetime.now() - timedelta(days=DAYS)
    for code, app_id in APPS.items():
        rows = fetch(app_id, cutoff)
        path = RAW_DIR / f"{code}.jsonl"
        with path.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps({k: to_json(v) for k, v in r.items()}, ensure_ascii=False) + "\n")
        oldest = rows[-1]["at"].date() if rows else "-"
        warn = "  ⚠️ chạm giới hạn, cửa sổ bị cắt" if len(rows) >= MAX_PER_APP else ""
        print(f"{code:12s} {len(rows):6d} review  (cũ nhất: {oldest}){warn}", flush=True)


if __name__ == "__main__":
    main()
