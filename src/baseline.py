"""Baseline từ khoá và số sao (taxonomy §7).

Cố ý đơn giản: trả lời câu hỏi "có cần LLM không, hay vài dòng quy tắc là đủ?".
Chạy: .venv/bin/python src/baseline.py
"""
import json
import re
import sys

from config import DATA
from golden import load_set

PRED_DIR = DATA / "preds"

# Thứ tự quan trọng: category nặng hơn được kiểm tra trước (giống quy tắc "chọn vấn đề nặng nhất")
CATEGORY_KEYWORDS = [
    ("FRAUD_SECURITY", r"lừa đảo|lua dao|mạo danh|hack|chiếm|lấy cắp|bảo mật|bao mat|lộ thông tin"),
    ("TXN_FAILURE", r"trừ tiền|tru tien|chưa hoàn|chua hoan|hoàn tiền|hoan tien|giao dịch|giao dich|"
                    r"chuyển tiền|chuyen tien|thanh toán|thanh toan|nạp|nap tien|rút|rut tien|treo|tự động trừ|gia hạn"),
    ("ONBOARD_EKYC", r"ekyc|cccd|căn cước|can cuoc|xác minh|xac minh|xác thực|xac thuc|khuôn mặt|khuon mat|"
                     r"nfc|đăng ký|dang ky|liên kết|lien ket"),
    ("AUTH_ACCESS", r"otp|đăng nhập|dang nhap|mật khẩu|mat khau|bị khoá|bị khóa|khoá tài khoản|khóa tài khoản|không vào được"),
    ("FEES_LIMITS", r"phí|phi dich vu|hạn mức|han muc"),
    ("SUPPORT", r"cskh|tổng đài|tong dai|hỗ trợ|ho tro|chăm sóc|nhân viên"),
    ("PROMO_REWARDS", r"khuyến mãi|khuyen mai|voucher|ưu đãi|uu dai|hoàn xu|điểm thưởng|tặng"),
    ("APP_EXPERIENCE", r"lag|lỗi|loi|văng|crash|đơ|chậm|quảng cáo|giao diện|cập nhật|load"),
]
MONEY_S1 = re.compile(r"trừ tiền|tru tien|mất tiền|mat tien|chưa hoàn|chua hoan|không hoàn|lừa|lua dao|"
                      r"treo|bị trừ|tự động trừ|tự trừ|chiếm|hack", re.I)
FLOW_KEYWORDS = [
    ("credit_bnpl", r"trả sau|tra sau|vay|trả góp"),
    ("topup_withdraw", r"nạp|nap|rút|rut|liên kết|lien ket"),
    ("transfer", r"chuyển tiền|chuyen tien|chuyển khoản|chuyen khoan"),
    ("payment", r"thanh toán|thanh toan|qr|hoá đơn|hóa đơn|gia hạn|mua"),
]


def predict(text: str, score: int) -> dict:
    t = text.lower()
    category = "NON_ISSUE" if score >= 4 else "APP_EXPERIENCE"
    for cat, pat in CATEGORY_KEYWORDS:
        if re.search(pat, t):
            category = cat
            break
    if MONEY_S1.search(t):
        severity = "S1"
    else:
        severity = {1: "S2", 2: "S2", 3: "S3"}.get(score, "S4")
    flow = None
    if category == "TXN_FAILURE":
        flow = next((f for f, pat in FLOW_KEYWORDS if re.search(pat, t)), "unknown")
    se = False if category == "FRAUD_SECURITY" else None
    return {"category": category, "severity": severity, "flow": flow, "social_engineering": se, "evidence": None}


def main():
    name = "test" if "--set=test" in sys.argv or "test" in sys.argv[1:] else "dev"
    out_dir = PRED_DIR / "test" if name == "test" else PRED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    golden = load_set(name)
    dst = out_dir / "baseline.jsonl"
    with dst.open("w", encoding="utf-8") as f:
        for r in golden:
            f.write(json.dumps({"review_id": r["review_id"], **predict(r["content"], int(r["score"]))},
                               ensure_ascii=False) + "\n")
    print(f"Đã ghi {len(golden)} dự đoán vào {dst.relative_to(DATA.parent)}")


if __name__ == "__main__":
    main()
