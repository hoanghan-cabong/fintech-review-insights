# Bộ phân loại và thang mức nghiêm trọng (v0.3)

Tài liệu này là chuẩn chung cho **ba bên**: bạn khi gắn nhãn tập đáp án, agent khi phân loại, và baseline từ khoá. Mọi thay đổi đều phải ghi vào [decision-log.md](decision-log.md), vì đổi định nghĩa thì phải gắn nhãn lại.

Các ví dụ dưới đây là câu **tự viết để minh hoạ**, không phải review thật.

> Thay đổi so với v0.2 (D013): từ 13 xuống 9 category, từ 8 xuống 5 flow, bỏ category phụ, chỉ còn 1 cờ, tập đáp án còn 140 review. Mục tiêu: giảm khoảng một nửa công gắn nhãn mà không làm yếu kết luận.

---

## 1. Bạn cần gắn nhãn gì cho mỗi review

| Trường | Bắt buộc? | Giá trị |
|---|---|---|
| `category` | Luôn có | 1 trong 9 category (§2) |
| `severity` | Luôn có | S1 / S2 / S3 / S4 (§4) |
| `flow` | Chỉ khi category là `TXN_FAILURE` | 1 trong 5 flow (§3) |
| `social_engineering` | Chỉ khi category là `FRAUD_SECURITY` | true / false (§4, quy tắc 5) |

Chỉ có vậy. Trích dẫn `evidence` do agent tự lấy, bạn không cần gắn.

---

## 2. Category (chọn đúng 1)

| Mã | Tên | Bao gồm | Ví dụ minh hoạ |
|---|---|---|---|
| `ONBOARD_EKYC` | Đăng ký và xác thực danh tính | eKYC, chụp CCCD, nhận diện khuôn mặt khi mở tài khoản | "Chụp CCCD 10 lần vẫn báo không hợp lệ" |
| `AUTH_ACCESS` | Đăng nhập và truy cập | OTP không về, quên mật khẩu, sinh trắc học, tài khoản bị khoá | "OTP không gửi về, không vào được app" |
| `TXN_FAILURE` | Giao dịch lỗi | Giao dịch thất bại, bị treo, trừ tiền nhưng không nhận được, hoàn tiền chậm | "Nạp 500k bị trừ tiền ngân hàng mà ví không cộng" |
| `FRAUD_SECURITY` | Lừa đảo và bảo mật | Bị chiếm tài khoản, giao dịch lạ, bị lừa, lo ngại bảo mật | "Tự nhiên mất 2 triệu, tôi không hề giao dịch" |
| `FEES_LIMITS` | Phí và hạn mức | Phí rút hoặc chuyển tiền, phí ẩn, hạn mức giao dịch | "Rút tiền về ngân hàng mất phí mà không báo trước" |
| `SUPPORT` | Chăm sóc khách hàng | Không liên hệ được, phản hồi chậm, trả lời theo mẫu, không giải quyết | "Gọi tổng đài 3 ngày không ai bắt máy" |
| `PROMO_REWARDS` | Khuyến mãi và điểm thưởng | Voucher không áp dụng được, hoàn tiền khuyến mãi, điều kiện mập mờ | "Voucher 50k báo hết lượt ngay khi vừa mở" |
| `APP_EXPERIENCE` | Trải nghiệm app | Lag, crash, lỗi sau cập nhật, giao diện rối, nhiều quảng cáo, đề xuất tính năng | "Cập nhật xong mở app là bị văng" |
| `NON_ISSUE` | Không phải vấn đề | Khen, spam, nội dung không rõ hoặc không liên quan. **Review dưới 5 từ được gán `NON_ISSUE` tự động bằng quy tắc, không qua agent và không cần gắn nhãn** (D014) | "App tiện", "ok" |

**Quy tắc chọn category:** review nhắc nhiều vấn đề thì chọn vấn đề **gây hậu quả nặng nhất**, không phải vấn đề được nhắc đầu tiên.
Ví dụ: "Giao diện xấu, mà chuyển tiền bị treo 2 ngày chưa hoàn" → `TXN_FAILURE`.

---

## 3. Flow (chỉ khi category là `TXN_FAILURE`)

| Mã | Luồng |
|---|---|
| `transfer` | Chuyển tiền cho người khác hoặc sang ngân hàng |
| `payment` | Thanh toán: quét QR, mua hàng online, hoá đơn, nạp điện thoại |
| `topup_withdraw` | Nạp tiền vào ví, rút tiền về ngân hàng, liên kết ngân hàng |
| `credit_bnpl` | Ví trả sau, vay, trả góp |
| `unknown` | Không xác định được |

---

## 4. Mức nghiêm trọng (chấm theo rủi ro, không theo số sao)

| Mức | Tên | Định nghĩa | Ví dụ minh hoạ |
|---|---|---|---|
| **S1** | Critical | **Đã mất tiền hoặc có rủi ro mất tiền**: tiền bị trừ hoặc treo chưa hoàn, giao dịch lạ, bị chiếm tài khoản, bị lừa, **bị trừ tiền mà người dùng không đồng ý** (phí tự ý, gói hoặc bảo hiểm tự đăng ký) | "Bị trừ 1 triệu mà người nhận không nhận được, 5 ngày chưa hoàn" |
| **S2** | High | **Không dùng được chức năng cốt lõi** nhưng chưa mất tiền: không đăng nhập được, không eKYC được, không chuyển hoặc thanh toán được | "Không nhận OTP nên không đăng nhập được 2 ngày nay" |
| **S3** | Medium | **Gây phiền nhưng vẫn dùng tiếp được**: phí khó hiểu, khuyến mãi không áp dụng được, hỗ trợ chậm nhưng chưa ảnh hưởng tiền, lag | "Voucher không dùng được, bực mình" |
| **S4** | Low | Thẩm mỹ, đề xuất tính năng, chê chung chung, hoặc khen | "Giao diện nên đổi màu", "App tốt" |

### Cây quyết định (hỏi lần lượt, dừng ở câu "có" đầu tiên)

1. Người dùng **đã mất tiền, tiền bị treo, hoặc có rủi ro mất tiền**? → **S1**
2. Người dùng **không làm được việc chính**: đăng ký/eKYC, đăng nhập, chuyển tiền, thanh toán, nạp/rút? → **S2**
3. Người dùng **vẫn dùng được nhưng bị phiền**: phí cao, khuyến mãi không như hứa, lag, hỗ trợ chậm? → **S3**
4. Còn lại: góp ý, chê chung chung, khen → **S4**

**Chỉ dựa vào hậu quả mà review mô tả.** Số sao, chửi thề, dấu "???", hay từ "lừa" dùng theo nghĩa bực bội ("m lừa bọn t à?" khi khuyến mãi không về) đều **không** làm tăng mức.

### Quy tắc khi phân vân

1. **Phân vân giữa 2 mức thì chọn mức cao hơn** khi review liên quan đến tiền hoặc bảo mật. Precision S1 ≥ 70% là chỉ số chặn để không gắn S1 tràn lan.
2. **Không suy diễn quá nội dung review.** "App lỗi" chung chung → S3.
3. **Số sao không quyết định mức nghiêm trọng.** Review 5 sao kể bị trừ tiền chưa hoàn vẫn là S1.
4. Category `SUPPORT` có mức bằng **vấn đề gốc**. Ví dụ không liên hệ được để đòi tiền bị treo → S1.
5. **Bị lừa mà người dùng tự chuyển tiền** (bị dụ, mạo danh): `FRAUD_SECURITY`, mức S1, `social_engineering = true`. Lúc phân tích, nhóm này được tách riêng khỏi lỗi hệ thống.
6. **Phí:** phí đã công bố nhưng người dùng thấy cao hoặc vô lý → S3. Tiền bị trừ mà người dùng không đồng ý (phí tự ý, gói tự gia hạn, bảo hiểm tự tích sẵn) → S1. *(Thêm sau lần gắn nhãn đầu, D017.)*
7. **Lỗi app khi đang giao dịch:** app văng hoặc báo lỗi, không làm được giao dịch, chưa thấy trừ tiền → S2. Đã bị trừ tiền → S1. Chỉ lag nhưng vẫn làm được → S3.
8. **Không rút được tiền đang có trong ví** *(D021)*: do tài khoản bị khoá, đóng băng, hoặc bị đánh dấu nghi ngờ → `AUTH_ACCESS`, **S1** (không biết khi nào lấy lại được tiền). Do app lỗi tạm thời → S2 theo quy tắc 7.
9. **Chửi "lừa đảo" mà không kể sự việc** *(D021)*: "app lừa đảo", "tiếp tay lừa đảo" mà không mô tả chuyện gì đã xảy ra → `NON_ISSUE`, S4. Có kể sự việc thì phân loại theo sự việc đó.
10. **Dịch vụ bên thứ ba** *(D021)*: tiền bị trừ cho dịch vụ bên thứ ba (gói trên Google Play, ứng dụng khác…) **qua ví hoặc qua ngân hàng liên kết với ví**, mà người dùng không đồng ý → `TXN_FAILURE`, flow `payment`, S1. Review không cho thấy ví liên quan đến việc trừ tiền → `NON_ISSUE`.

---

## 5. Định dạng đầu ra của agent

```json
{
  "review_id": "gp_momo_000123",
  "category": "TXN_FAILURE",
  "flow": "topup_withdraw",
  "severity": "S1",
  "social_engineering": null,
  "evidence": "đoạn trích NGUYÊN VĂN từ review"
}
```

- `flow` và `social_engineering` để `null` khi không áp dụng.
- `evidence` phải là một đoạn **nguyên văn** của review. Một script sẽ tự kiểm tra điều này.
- Không có trường `confidence`. Việc chuyển sang người duyệt dùng quy tắc kiểm tra được ([PRD §5](PRD.md)).

---

## 6. Tập đáp án (gắn nhãn tay)

| Tập | Cỡ | Cách chọn | Dùng để |
|---|---|---|---|
| **Ngẫu nhiên** | 100 | Lấy ngẫu nhiên 25 review mỗi app, trong số review từ 5 từ trở lên | Đo chất lượng trên phân phối thật. Các chỉ số trong PRD §3.1 được tính trên tập này. **Bấm giờ khi gắn nhãn tập này**: đó chính là số liệu thời gian phân loại tay |
| **Ca khó** | 40 | Chọn có chủ đích theo checklist bên dưới | Thử độ bền. Báo cáo riêng, không gộp vào chỉ số chính |

**Đủ mẫu S1:** tổng hai tập cần **≥ 30 review S1**. Recall S1 được báo cáo kèm khoảng tin cậy 95%.

**Checklist cho tập ca khó (40 review):**
- [ ] ≥ 20 review S1, trong đó ≥ 4 ca `social_engineering`
- [ ] ≥ 8 review không dấu hoặc teencode ("bi tru tien ma k nhan dc")
- [ ] ≥ 6 review lệch giữa số sao và nội dung
- [ ] ≥ 6 review nhắc nhiều vấn đề cùng lúc
- [ ] ≥ 4 review mỉa mai ("Tuyệt vời, mất tiền nhanh nhất VN")

*(Một review có thể đáp ứng nhiều mục cùng lúc.)*

**Đo độ nhất quán của chính mình:** *(đã thay đổi)* thay cho việc gắn lại 20 review sau 1 tuần, dự án dùng: so sánh lần gắn 1 và lần gắn 2 (chỉ 15/53 review có vấn đề trùng mức, D017), rà soát bất đồng người–model có ghi lý do (D020), và tập kiểm tra 80 review gắn nhãn trước khi chạy model (D021).

**Kết quả thực tế (13/11/2026):**

| Tiêu chí | Đạt | Mục tiêu |
|---|---|---|
| Tập ngẫu nhiên | 100 (`random_set_v2.csv`) | 100 ✅ |
| Tập ca khó, đủ nhãn | 57 (`hard_pool.csv`) | 40 ✅ |
| Tổng S1 hai tập | 31 | 30 ✅ |
| Lệch sao | 9 | 6 ✅ |
| Không dấu | 5 | 8 ⚠️ thiếu 3 |
| Bị lừa mà tự chuyển tiền | **0** | 4 ❌ không tìm thấy trong dữ liệu (D018) |

Hệ quả: cờ `social_engineering` vẫn giữ trong định dạng đầu ra, nhưng không có số liệu eval; kết quả trên review không dấu chỉ báo cáo dạng định tính (5 mẫu).

**Category ít mẫu:** category nào có dưới 5 mẫu trong tập ngẫu nhiên thì không báo cáo độ chính xác riêng, chỉ tính vào độ chính xác tổng.

---

## 7. Baseline từ khoá và số sao

Một bộ quy tắc cố ý đơn giản để làm mốc so sánh:
- **Category:** danh sách từ khoá cho từng category, có cả biến thể không dấu.
- **Mức nghiêm trọng:** chứa từ khoá về tiền hoặc lừa đảo ("trừ tiền", "mất tiền", "lừa", "chưa hoàn"…) → S1; 1–2 sao → S2; 3 sao → S3; 4–5 sao → S4.

Baseline trả lời câu hỏi: *"Có cần LLM không, hay vài dòng quy tắc là đủ?"*

---

## Để sang v2

Những phần cố ý chưa làm ở v1, ghi lại để không mất ý tưởng:
- Category `POLICY_FRICTION` (ma sát do yêu cầu theo quy định). Ở v1, nếu gặp thì ghi chú lại như một quan sát.
- Cờ `churn_intent` và `trust_damage`, dùng cho điểm ưu tiên có xét ý định rời bỏ.
- Category phụ cho review nhắc nhiều vấn đề.
