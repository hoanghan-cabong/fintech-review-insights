# PRD đề xuất: Trung tâm thanh toán tự động

> Phiên bản: v0.1 · 2026-11-13 · Trạng thái: Đề xuất từ dữ liệu review công khai, **cần kiểm chứng bằng dữ liệu nội bộ** trước khi đưa vào roadmap.
> Nguồn: [reports/insights.md](../reports/insights.md) · Quyết định liên quan: D023–D026

## 1. Vấn đề

**Gần một nửa số ca người dùng ví điện tử mất tiền không đến từ giao dịch lỗi, mà từ việc bị trừ tiền khi họ không đồng ý.**

Trong 435 review S1 (đã mất tiền hoặc có rủi ro mất tiền) của MoMo, ZaloPay, ShopeePay và Viettel Money (14/08–12/11/2026), "bị trừ tiền không đồng ý" chiếm **49%** (khoảng tin cậy 44–54%), nhiều hơn giao dịch lỗi đã bị trừ tiền (35%). Hiện tượng này **không riêng một ví nào**: Viettel Money 55%, ZaloPay 54%, ShopeePay 49%, MoMo 42%.

Người dùng mô tả (nguyên văn, đã ẩn danh):
- "áp này tự động liên kết ngân hàng rồi trừ tiền của kh" `gp_shopeepay_00636`
- "nó tự nạo tiền đt mà t kh cài nạo tự động" `gp_zalopay_00729`
- "thu phí hàng tháng là 11k mà ko thông báo cho kh biết" `gp_viettelmoney_00261`
- "bị trừ tiền vô lý mà ko tra cứu đc" `gp_shopeepay_02381`

Bốn kiểu thường gặp (đếm theo từ khoá, có trùng lặp, nên chỉ để định hướng):

| Kiểu | Số review / 217 |
|---|---|
| Gói hoặc dịch vụ bên thứ ba tự gia hạn (ứng dụng trên Google Play, gói data…) | ~79 |
| Trừ từ ngân hàng liên kết mà không hỏi OTP hay sinh trắc học | ~49 |
| Phí tự ý, phí duy trì không được báo | ~16 |
| Bảo hiểm hoặc dịch vụ được chèn sẵn khi thanh toán | ~9 |

**Vì sao đáng ưu tiên:** đây là mức S1, nhóm nghiêm trọng nhất. Người dùng không chỉ mất tiền mà còn mất niềm tin vào chính việc liên kết ngân hàng, thứ mà ví cần để giữ chân họ. Và vì ví nào cũng gặp, **ví giải quyết trước có thể biến điều này thành khác biệt cạnh tranh** ("ví không bao giờ trừ tiền khi bạn chưa biết").

## 2. Giả thuyết

Người dùng không hề "bị trộm tiền". Phần lớn họ **không nhớ, không thấy, hoặc không tìm được chỗ huỷ** các khoản thanh toán tự động mà họ (hoặc một ứng dụng khác) đã thiết lập. Ba lỗ hổng:
1. **Không biết trước:** khoản trừ xảy ra mà không có thông báo trước.
2. **Không thấy toàn cảnh:** không có một nơi liệt kê mọi khoản trừ tự động và ngân hàng liên kết đang được dùng.
3. **Không đồng ý rõ ràng:** khoản trừ đầu tiên từ một bên mới, hoặc dịch vụ chèn thêm, không cần thao tác xác nhận.

## 3. Người dùng và nhu cầu

| Persona | Nhu cầu |
|---|---|
| Người dùng có liên kết ngân hàng hoặc dùng ví thanh toán gói dịch vụ | "Tôi muốn biết trước khi tiền bị trừ, và huỷ được trong một chạm." |
| Đội CSKH | "Tôi muốn giảm khiếu nại 'trừ tiền không rõ lý do', vốn tốn công tra soát." |

## 4. Giải pháp đề xuất (MVP)

| # | Tính năng | Lỗ hổng xử lý |
|---|---|---|
| 1 | **Thông báo trước khi trừ:** mọi khoản trừ định kỳ hoặc tự động có thông báo trước 24 giờ, kèm nút "Huỷ lần này" và "Tắt tự động" | Không biết trước |
| 2 | **Màn hình "Thanh toán tự động":** một nơi duy nhất liệt kê mọi gói, mọi bên được trừ tự động, ngân hàng liên kết dùng cho mỗi bên, khoản trừ gần nhất và kế tiếp; huỷ trong một chạm | Không thấy toàn cảnh |
| 3 | **Xác nhận lần đầu:** khoản trừ đầu tiên từ một bên mới, hoặc vượt ngưỡng do người dùng đặt, cần OTP hoặc sinh trắc học | Không đồng ý rõ ràng |
| 4 | **Bỏ tích sẵn:** dịch vụ hoặc bảo hiểm đi kèm khi thanh toán mặc định ở trạng thái **không chọn** | Không đồng ý rõ ràng |

**Không làm trong MVP:** hoàn tiền tự động; thay đổi luồng thanh toán của bên thứ ba (Google Play); tính năng quản lý chi tiêu tổng quát.

## 5. Chỉ số thành công

| Loại | Chỉ số | Hướng |
|---|---|---|
| **North star** | Tỷ trọng review S1 kiểu "bị trừ không đồng ý" (đo hằng tháng bằng chính agent của dự án này) | Giảm |
| Vận hành | Số ticket CSKH "trừ tiền không rõ lý do" trên 10.000 người dùng hoạt động | Giảm |
| Sử dụng | Tỷ lệ người dùng có thanh toán tự động đã mở màn hình mới; số khoản bị huỷ từ thông báo trước | Tăng |
| **Chỉ số chặn** | Tỷ lệ thanh toán thành công và doanh thu từ gói định kỳ hợp lệ | Không giảm quá ngưỡng thống nhất trước khi thử nghiệm |

## 6. Đánh đổi và rủi ro

| Rủi ro | Cách xử lý |
|---|---|
| Thêm bước xác nhận làm giảm tỷ lệ thanh toán thành công | Chỉ áp cho lần đầu với bên mới hoặc vượt ngưỡng; A/B test với chỉ số chặn |
| Đối tác và bên thứ ba (nhà bán, kho ứng dụng) phản đối thông báo trước vì làm tăng huỷ | Bắt đầu với các khoản do chính ví quản lý; trình bày dữ liệu về mất niềm tin |
| Phát hiện từ review công khai không đại diện cho toàn bộ người dùng | Bước 0 là kiểm chứng bằng dữ liệu nội bộ (ticket, tranh chấp giao dịch) trước khi cam kết |
| Yêu cầu tuân thủ về xác thực giao dịch | Làm việc với bộ phận pháp chế; thiết kế để đáp ứng hoặc vượt yêu cầu hiện hành |

## 7. Lộ trình

1. **Kiểm chứng (2 tuần):** đối chiếu với ticket CSKH và tranh chấp giao dịch nội bộ. Nếu nhóm này chiếm dưới khoảng 10% ticket về tiền, xếp lại ưu tiên.
2. **MVP (6–8 tuần):** tính năng 1 và 2, thử nghiệm A/B trên nhóm có thanh toán tự động.
3. **Mở rộng:** tính năng 3 và 4, sau khi có kết quả chỉ số chặn.
4. **Theo dõi:** chạy agent phân tích review mỗi tháng, so với 3 ví còn lại.

## 8. Câu hỏi mở

- Bao nhiêu phần trăm khoản trừ bị khiếu nại là thanh toán qua kho ứng dụng (ví chỉ là phương thức thanh toán) so với khoản do ví tự khởi tạo?
- Người dùng muốn nhận thông báo trước qua kênh nào để không bị coi là làm phiền?
- MoMo là ví duy nhất có giao dịch lỗi nhiều hơn trừ không đồng ý trong nhóm S1: có phải MoMo đã có cơ chế tương tự? Nên nghiên cứu như một hình mẫu (không kết luận chỉ từ review).
