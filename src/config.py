"""Cấu hình chung cho toàn bộ pipeline."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RAW_DIR = DATA / "raw"          # review đã bỏ tên/ảnh người dùng, chưa che PII trong nội dung
CLEAN_DIR = DATA / "clean"      # review đã ẩn danh hoàn toàn
LABEL_DIR = DATA / "labels"     # file gắn nhãn tay

# Mã ngắn -> app ID trên Google Play (đã kiểm tra ngày 2026-11-12)
APPS = {
    "momo": "com.mservice.momotransfer",
    "zalopay": "vn.com.vng.zalopay",
    "shopeepay": "com.beeasy.toppay",
    "viettelmoney": "com.bplus.vtpay",
    # VNPAY (vnpay.smartacccount) bị thay ra: chỉ 71 review / 90 ngày (D015)
}

LANG, COUNTRY = "vi", "vn"
DAYS = 90               # MỌI app dùng cùng cửa sổ 90 ngày để so sánh công bằng
MAX_PER_APP = 30000     # chỉ là chốt an toàn; không được để giới hạn này cắt cửa sổ thời gian
MIN_WORDS = 5           # review ngắn hơn được coi là NON_ISSUE bằng quy tắc (D014)

STUDY_APPS = list(APPS)

SEED = 42               # cố định để lấy mẫu ngẫu nhiên lặp lại được
