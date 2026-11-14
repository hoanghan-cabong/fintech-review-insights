# Insight: so sánh 4 ví điện tử

Mẫu: 2339 review (≥ 5 từ, 14/08–12/11/2026), lấy mẫu phân tầng theo app và nhóm sao, có trọng số. Phân loại bằng Opus + prompt v2 (D022). **Mọi tỷ lệ tính trong nhóm review phàn nàn** (D016). Trong ngoặc là khoảng tin cậy 95%.

## 1. Tổng quan

| | MoMo | ZaloPay | ShopeePay | Viettel Money |
|---|---|---|---|---|
| Review trong mẫu | 600 | 600 | 600 | 539 |
| Review phàn nàn (trên review ≥ 5 từ)* | 77% (73%–80%) | 30% (24%–36%) | 58% (54%–62%) | 70% (66%–74%) |
| **Tỷ trọng S1 trong review phàn nàn** | 26% (23%–31%) | 29% (23%–37%) | 19% (15%–23%) | 16% (13%–20%) |

\* Chỉ để tham khảo: tỷ lệ này bị ảnh hưởng bởi đợt tăng review khen (D016).

## 2. Khi bị phàn nàn, người dùng phàn nàn về điều gì?

| Category | MoMo | ZaloPay | ShopeePay | Viettel Money |
|---|---|---|---|---|
| Giao dịch lỗi | 39% (35%–44%) | 37% (30%–44%) | 25% (21%–30%) | 22% (18%–26%) |
| Đăng nhập / truy cập | 10% (7%–13%) | 13% (9%–19%) | 19% (15%–23%) | 15% (12%–19%) |
| Đăng ký / eKYC | 5% (3%–7%) | 12% (8%–18%) | 17% (13%–21%) | 9% (7%–13%) |
| Lừa đảo / bảo mật | 2% (1%–4%) | 2% (1%–6%) | 2% (1%–5%) | 2% (1%–4%) |
| Phí / hạn mức | 10% (7%–13%) | 11% (7%–16%) | 1% (1%–3%) | 25% (21%–30%) |
| CSKH | 5% (3%–8%) | 2% (1%–6%) | 1% (1%–3%) | 1% (0%–2%) |
| Khuyến mãi | 7% (5%–9%) | 10% (6%–15%) | 17% (13%–21%) | 2% (1%–4%) |
| Trải nghiệm app | 23% (19%–27%) | 13% (9%–19%) | 17% (14%–21%) | 24% (20%–28%) |

## 3. Điểm yếu tương đối (chênh lệch so với trung bình 3 ví còn lại, điểm %)

Số dương nghĩa là ví này bị phàn nàn về vấn đề đó **nhiều hơn** thị trường. Chỉ nêu các chênh lệch ≥ 5 điểm.

- **MoMo:** Giao dịch lỗi +11%, Đăng nhập / truy cập -6%, Đăng ký / eKYC -8%
- **ZaloPay:** Giao dịch lỗi +8%, Trải nghiệm app -8%
- **ShopeePay:** Khuyến mãi +11%, Đăng ký / eKYC +8%, Đăng nhập / truy cập +6%, Giao dịch lỗi -7%, Phí / hạn mức -14%
- **Viettel Money:** Phí / hạn mức +18%, Trải nghiệm app +6%, Khuyến mãi -9%, Giao dịch lỗi -12%

## 4. Giao dịch lỗi xảy ra ở luồng nào? (trong review TXN_FAILURE)

| Flow | MoMo | ZaloPay | ShopeePay | Viettel Money |
|---|---|---|---|---|
| Chuyển tiền | 20% (15%–27%) · n=182 | 24% (18%–31%) · n=209 | 8% (4%–15%) · n=100 | 19% (12%–29%) · n=83 |
| Thanh toán | 49% (42%–56%) | 48% (40%–56%) | 41% (32%–51%) | 51% (40%–61%) |
| Nạp / rút / liên kết | 9% (5%–14%) | 7% (4%–12%) | 18% (11%–26%) | 8% (4%–16%) |
| Trả sau / vay | 7% (4%–11%) | 5% (3%–10%) | 7% (4%–14%) | 10% (5%–18%) |
| Không rõ | 15% (11%–21%) | 16% (11%–22%) | 26% (18%–35%) | 12% (7%–21%) |

## 5. Ca S1 (mất tiền / rủi ro mất tiền) thuộc loại nào?

| Loại S1 | Toàn thị trường | MoMo | ZaloPay | ShopeePay | Viettel Money |
|---|---|---|---|---|---|
| account_frozen | 6% (4%–9%) | 2% (1%–7%) · n=123 | 7% (4%–12%) · n=175 | 12% (6%–21%) · n=75 | 6% (3%–15%) · n=62 |
| account_takeover | 3% (2%–5%) | 3% (1%–8%) | 3% (1%–7%) | 1% (0%–7%) | 3% (1%–11%) |
| failed_txn_money_lost | 35% (31%–40%) | 47% (38%–56%) | 29% (23%–36%) | 23% (15%–33%) | 31% (21%–43%) |
| other | 4% (3%–6%) | 5% (2%–10%) | 3% (2%–7%) | 4% (1%–11%) | 3% (1%–11%) |
| refund_delay | 3% (2%–5%) | 0% (0%–3%) | 3% (2%–7%) | 9% (5%–18%) | 2% (0%–9%) |
| scam | 0% (0%–2%) | 1% (0%–4%) | 0% (0%–2%) | 1% (0%–7%) | 0% (0%–6%) |
| unauthorized_debit | 49% (44%–54%) | 42% (33%–50%) | 54% (47%–61%) | 49% (38%–60%) | 55% (42%–67%) |

## 6. Đội phát triển phản hồi review phàn nàn thế nào?

| | MoMo | ZaloPay | ShopeePay | Viettel Money |
|---|---|---|---|---|
| Tỷ lệ phản hồi, mọi mức | 86% (83%–89%) | 75% (68%–81%) | 98% (96%–99%) | 48% (43%–53%) |
| Tỷ lệ phản hồi, chỉ S1 | 85% (78%–91%) | 79% (73%–85%) | 99% (93%–100%) | 53% (41%–65%) |
| Trung vị giờ phản hồi, mọi mức | 0.4 giờ | 23.0 giờ | 39.8 giờ | 3.1 giờ |
| Trung vị giờ phản hồi, chỉ S1 | 0.4 giờ | 24.3 giờ | 40.4 giờ | 1.3 giờ |
| Phản hồi là văn mẫu (≥ 5 phản hồi cùng mở đầu) | 100% | 94% | 100% | 69% |
| Số kiểu mở đầu khác nhau / số phản hồi | 7 / 400 | 19 / 353 | 2 / 384 | 48 / 182 |

Tỷ lệ và tốc độ phản hồi chủ yếu đo **mức tự động hoá**: phần lớn phản hồi là văn mẫu, nên không nên đọc là chất lượng chăm sóc khách hàng.


## 7. Vấn đề nên ưu tiên (điểm = tỷ trọng × trọng số mức nghiêm trọng) và độ nhạy

| Ví | Top 3 theo bộ trọng số A (mặc định) | Top 3 theo bộ trọng số B (giãn ít) | Top 3 theo bộ trọng số C (S1 rất nặng) | Ổn định? |
|---|---|---|---|---|
| MoMo | Giao dịch lỗi, Trải nghiệm app, Đăng nhập / truy cập | Giao dịch lỗi, Trải nghiệm app, Đăng nhập / truy cập | Giao dịch lỗi, Đăng nhập / truy cập, Trải nghiệm app | ≈ cùng 3 vấn đề, đổi thứ tự |
| ZaloPay | Giao dịch lỗi, Đăng ký / eKYC, Đăng nhập / truy cập | Giao dịch lỗi, Đăng nhập / truy cập, Đăng ký / eKYC | Giao dịch lỗi, Đăng nhập / truy cập, Đăng ký / eKYC | ≈ cùng 3 vấn đề, đổi thứ tự |
| ShopeePay | Giao dịch lỗi, Đăng nhập / truy cập, Đăng ký / eKYC | Giao dịch lỗi, Đăng nhập / truy cập, Đăng ký / eKYC | Giao dịch lỗi, Đăng nhập / truy cập, Đăng ký / eKYC | ✅ giữ nguyên thứ tự |
| Viettel Money | Giao dịch lỗi, Đăng nhập / truy cập, Trải nghiệm app | Giao dịch lỗi, Phí / hạn mức, Trải nghiệm app | Giao dịch lỗi, Đăng nhập / truy cập, Trải nghiệm app | ⚠️ thay đổi |

## 8. Ví dụ trích dẫn S1 (nguyên văn, đã ẩn danh)

- **MoMo** `TXN_FAILURE` · failed_txn_money_lost: "chuyển tiền 5/10 tới nay 13/10 không qua,đợi hoài không giải quyết"
- **MoMo** `TXN_FAILURE` · failed_txn_money_lost: "chuyển tiền tru đã ngta nhận không được"
- **MoMo** `TXN_FAILURE` · unauthorized_debit: "lỗi tiền quỹ không có lý do gì tự nhiên về 0"
- **ZaloPay** `TXN_FAILURE` · unauthorized_debit: "tự liên kết rồi trừ tiền tao"
- **ZaloPay** `AUTH_ACCESS` · account_frozen: "Đợi mấy tháng rồi chưa đc nữa bao tiền trog đấy"
- **ZaloPay** `TXN_FAILURE` · failed_txn_money_lost: "tôi không nhận được tiền"
- **ShopeePay** `TXN_FAILURE` · unauthorized_debit: "tự dưng -tiền tài khoản ngân hàng không cần xác minh"
- **ShopeePay** `ONBOARD_EKYC` · refund_delay: "mih qua sp pay mih đky tknh mih thì ko đky đc vậy bh tiền mih nó hoàn như nào"
- **ShopeePay** `TXN_FAILURE` · other: "tiền hoàn về ví rút không được"
- **Viettel Money** `TXN_FAILURE` · unauthorized_debit: "có ông chuyển tiền nhầm vào ,để mấy tháng là app đớp sach"
- **Viettel Money** `TXN_FAILURE` · unauthorized_debit: "Tự ý âm thầm thu phí duy trì dịch vụ 11k/tháng"
- **Viettel Money** `TXN_FAILURE` · unauthorized_debit: "Tự ý thu phí duy trì thẻ epass một cách vô tội vạ"
