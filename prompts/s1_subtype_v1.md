Bạn phân tích các review ví điện tử đã được xác định là S1 (người dùng đã mất tiền, tiền bị kẹt, hoặc có rủi ro mất tiền). Với mỗi review, chọn đúng MỘT loại mô tả rõ nhất cơ chế khiến người dùng mất tiền. Chỉ dựa vào nội dung review.

- unauthorized_debit: bị trừ tiền mà người dùng KHÔNG đồng ý hoặc không biết: gói/dịch vụ tự gia hạn, thanh toán tự động, ví trả sau tự trừ, liên kết ngân hàng tự nạp/tự trừ, phí bị trừ không báo trước, tự tích sẵn bảo hiểm.
- failed_txn_money_lost: người dùng CHỦ ĐỘNG giao dịch (chuyển, thanh toán, nạp, rút) và bị trừ tiền nhưng giao dịch không thành công, bên kia không nhận được, hoặc tiền bị treo.
- refund_delay: đã được xác nhận sẽ hoàn tiền (hoặc giao dịch đã huỷ) nhưng chậm hoàn hoặc không hoàn.
- account_frozen: tài khoản bị khoá, đóng băng, bị đánh dấu nghi ngờ khiến không rút được tiền trong ví.
- account_takeover: giao dịch lạ không do người dùng thực hiện, bị chiếm tài khoản, bị hack, lộ thông tin dẫn tới mất tiền.
- scam: người dùng bị lừa và TỰ chuyển tiền hoặc tự cung cấp OTP.
- other: không thuộc các loại trên hoặc không đủ thông tin.

Đầu vào là danh sách JSON {"review_id", "text"}. Trả về kết quả cho TẤT CẢ review theo schema.
