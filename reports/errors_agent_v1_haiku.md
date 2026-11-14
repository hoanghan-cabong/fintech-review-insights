# Lỗi của agent_v1_haiku

Chỉ liệt kê review sai category hoặc sai S1/không S1.

- **[CAT] gp_momo_00350** (random): đáp án `NON_ISSUE/S4` · dự đoán `FRAUD_SECURITY/S3`  
  > tôi nghi là app giả tạo lắm 3* thôi 🤔  
  evidence: _tôi nghi là app giả tạo lắm_

- **[CAT] gp_momo_00629** (random): đáp án `TXN_FAILURE/S2` · dự đoán `AUTH_ACCESS/S2`  
  > đổi sổ điện thoại rồi vẫn gửi mã otp về số cũ không liên kết ngân hàng được  
  evidence: _vẫn gửi mã otp về số cũ không liên kết ngân hàng được_

- **[S1-FALSE] gp_momo_01143** (random): đáp án `TXN_FAILURE/S2` · dự đoán `TXN_FAILURE/S1`  
  > app gì suốt ngày lỗi không đăng nhập hoài vậy tiền thì gửi momo tới lúc cần vô rút thì app lỗi  
  evidence: _lúc cần vô rút thì app lỗi_

- **[CAT] gp_momo_01231** (random): đáp án `AUTH_ACCESS/S1` · dự đoán `TXN_FAILURE/S1`  
  > tự nhiên tôi bị đánh dấu lừa đảo ko rút đc tiền  
  evidence: _ko rút đc tiền_

- **[CAT] gp_zalopay_00119** (random): đáp án `NON_ISSUE/S4` · dự đoán `APP_EXPERIENCE/S4`  
  > Mình chủ yếu dùng tính năng Số dư sinh lời. Mình để làm nguồn tiền chính luôn ai chuyển tiền cho là tự vào trong đó luôn. lúc đi ăn, mua đồ hay chuyển tiền cho bạn bè thì dùng luôn. Khá tiện vì tiền trong Số dư sinh lời có thể dùng trực tiếp. Mình thích nhất điểm này, kiểu tiền vừa có thể sinh lời m  
  evidence: _hiện tại muốn nạp thêm tiền thì phải chuyển khoản_

- **[CAT] gp_zalopay_00539** (random): đáp án `ONBOARD_EKYC/S2` · dự đoán `AUTH_ACCESS/S2`  
  > không nhận dc otp để đăng ký tk  
  evidence: _không nhận dc otp để đăng ký tk_

- **[CAT] gp_zalopay_03633** (random): đáp án `NON_ISSUE/S4` · dự đoán `APP_EXPERIENCE/S3`  
  > 10 điểm chuyển nhanh chóng rút tiền nhanh, lâu lâu bị lỗi  
  evidence: _lâu lâu bị lỗi_

- **[CAT] gp_shopeepay_01382** (random): đáp án `APP_EXPERIENCE/S2` · dự đoán `NON_ISSUE/S4`  
  > mong có phương thức xác thực thay thế nfc vì không phải tất cả đt đề có nfc để quét chip cccd MONG TIẾP THU Ý KHIẾN !!!  
  evidence: __

- **[CAT] gp_shopeepay_00284** (random): đáp án `NON_ISSUE/S4` · dự đoán `APP_EXPERIENCE/S3`  
  > úng dụng mua sắm bày đặt ép tải .ứng dụng ngân hàng đầy đủ việc j phải tải cái này cho nặng máy  
  evidence: _ứng dụng mua sắm bày đặt ép tải_

- **[CAT] gp_viettelmoney_01309** (random): đáp án `APP_EXPERIENCE/S3` · dự đoán `PROMO_REWARDS/S3`  
  > Hồi truớc đổi điểm trong này luôn mà cứ bắt tải cái ứng dụng khác lằng nhằng ghê vậy  
  evidence: _cứ bắt tải cái ứng dụng khác lằng nhằng_

- **[S1-FALSE] gp_viettelmoney_00459** (random): đáp án `PROMO_REWARDS/S3` · dự đoán `FEES_LIMITS/S1`  
  > trc đây còn khuyến mãi. giờ hễ xíu là ko để ý là tích vào bảo hiểm vỡ gì đó. Tệ  
  evidence: _ko để ý là tích vào bảo hiểm vỡ gì đó_

- **[S1-FALSE] gp_viettelmoney_00092** (random): đáp án `APP_EXPERIENCE/S3` · dự đoán `FEES_LIMITS/S1`  
  > top 1 ứng dụng tài chính hút máu người dùng bằng đký gói, ko có ưu đãi, tệ hơn chữ tệ. rate xong gỡ app  
  evidence: _hút máu người dùng bằng đký gói, ko có ưu đãi_

- **[CAT] gp_viettelmoney_00317** (random): đáp án `TXN_FAILURE/S2` · dự đoán `APP_EXPERIENCE/S4`  
  > vay khó ứng dụng tệ  
  evidence: _vay khó ứng dụng tệ_

- **[CAT] gp_momo_01174** (hard): đáp án `TXN_FAILURE/S1` · dự đoán `AUTH_ACCESS/S1`  
  > CỰC KỲ TỆ, KHÔNG THỂ ĐĂNG NHẬP MẤT TIỀN !  
  evidence: _KHÔNG THỂ ĐĂNG NHẬP MẤT TIỀN_

- **[CAT] gp_viettelmoney_00744** (hard): đáp án `TXN_FAILURE/S2` · dự đoán `APP_EXPERIENCE/S3`  
  > Hay bị lỗi chuyển tiền dạo gần đây. Tiện nhưng bất cập quá  
  evidence: _Hay bị lỗi chuyển tiền dạo gần đây_

- **[CAT] gp_momo_00307** (hard): đáp án `PROMO_REWARDS/S3` · dự đoán `FEES_LIMITS/S3`  
  > làm theo các bước thanh toán spotify khi ở ngoài thì ghi là sau khi liên kết sẽ thanh toán 32500đ/ 3 tháng nhưng khi thanh toán thì lại phải trả 65000đ/1 tháng. nếu như spotify đang không trong giai đoạn giảm giá thì momo hãy làm ơn ghi là 65000đ/1 tháng chứ ko thì ko khác gì lừa dối khách hàng  
  evidence: _ghi là sau khi liên kết sẽ thanh toán 32500đ/ 3 tháng nhưng khi thanh toán thì lại phải trả 65000đ/1 tháng_

- **[CAT] gp_shopeepay_01555** (hard): đáp án `FRAUD_SECURITY/S1` · dự đoán `TXN_FAILURE/S1`  
  > ứng dụng lộ thông tin người dùng. mọi người đừng dùng. tôi đã bị trừ hơn 522k trong tài khoản ngân hàng sacombank do liên kết với ứng dụng Shopee pay này. ứng dụng lừa đảo  
  evidence: _bị trừ hơn 522k trong tài khoản ngân hàng sacombank do liên kết_

- **[S1-FALSE] gp_zalopay_16233** (hard): đáp án `NON_ISSUE/S4` · dự đoán `TXN_FAILURE/S1`  
  > Mình đăng ký dùng thử miễn phí Alarmy, nhưng sau khi hết hạn, thẻ ngân hàng bị trừ 1.086.667 đồng. Mình đã cố gắng hủy nhưng không tìm thấy gói thuê bao trên Google Play. Mình gửi yêu cầu hoàn tiền nhưng bị Google từ chối. Đây là số tiền rất lớn đối với mình. Mình mong Alarmy xem xét lại và hỗ trợ h  
  evidence: _sau khi hết hạn, thẻ ngân hàng bị trừ 1.086.667 đồng_

- **[S1-MISS] gp_shopeepay_00600** (hard): đáp án `TXN_FAILURE/S1` · dự đoán `ONBOARD_EKYC/S2`  
  > bực mih thật sự tự dưng bên shop giao sai đơn mà bây h mih ko xài shoppe pay mà shop nó ko chịu nó cứ ép mih hoàn = sp pay bh mih qua sp pay mih đky tknh mih thì ko đky đc vậy bh tiền mih nó hoàn như nào rồi sao mih sử dụng đây?  
  evidence: _mih đky tknh mih thì ko đky đc_
