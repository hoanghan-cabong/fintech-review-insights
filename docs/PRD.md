# PRD — Fintech Review Insights Agent

> Phiên bản: v1.0 · Cập nhật: 2026-11-13 · Trạng thái: Hoàn thành tuần 1–4 (còn tuần 5: case study)
> Phạm vi: MoMo · ZaloPay · ShopeePay · Viettel Money (ví điện tử, review công khai trên Google Play, 14/08–12/11/2026)
> v1.0: chốt kết quả eval trên tập kiểm tra (D022), chạy trên mẫu 2.339 review, thêm thanh chat hỏi đáp dữ liệu (D023–D025)
> v0.4: điều chỉnh theo dữ liệu thực tế: thay VNPAY bằng Viettel Money, so sánh trong nhóm review phàn nàn (D014–D016)
> v0.2: đổi trọng tâm sang thông tin đối thủ, thêm baseline và tiêu chí thất bại, chuẩn hoá khi so sánh, thiết kế lại eval (D006–D012)
> v0.3: rút gọn bộ phân loại và công gắn nhãn cho vừa sức một người làm (D013)

## 1. Vấn đề

PM của một ví điện tử hiểu rất rõ người dùng **của mình**: họ có ticket CS, dữ liệu trong app, công cụ VoC nội bộ. Nhưng họ gần như **không có dữ liệu có hệ thống về trải nghiệm người dùng của đối thủ**. Các câu hỏi chiến lược hiện được trả lời bằng cảm tính, ví dụ:

- Đối thủ đang yếu ở luồng nào (eKYC, chuyển tiền, QR, nạp/rút…) mà mình có thể tận dụng?
- Ở luồng nào mình đang tụt lại so với thị trường?
- Đối thủ phản hồi người dùng nhanh đến đâu khi có sự cố liên quan đến tiền?

Review công khai trên Google Play là nguồn dữ liệu đối thủ hiếm hoi mà ai cũng truy cập được. Tuy vậy, đọc thủ công thì không mở rộng được, còn đếm theo số sao hoặc theo số lượng thì đánh giá sai mức độ quan trọng: 100 review chê giao diện trông "to" hơn 5 review "bị trừ tiền mà không nhận được".

**Giả thuyết:** một agent phân loại review theo bộ phân loại riêng cho fintech, chấm mức nghiêm trọng theo rủi ro tài chính, chuẩn hoá để so sánh công bằng giữa các app và luôn kèm trích dẫn gốc sẽ cho ra bức tranh so sánh đối thủ **đáng tin hơn rõ rệt** so với cách đơn giản (lọc theo số sao hoặc từ khoá).

## 2. Người dùng mục tiêu

| | Persona | Nhu cầu chính (Job to be done) |
|---|---|---|
| **Chính** | PM / Strategy của một ví điện tử | "Khi chuẩn bị planning hoặc đánh giá chiến lược, tôi muốn biết đối thủ đang để lộ điểm yếu gì và mình đang tụt lại ở đâu, có số liệu và trích dẫn, để đề xuất ưu tiên có căn cứ." |
| Phụ | PM của fintech nhỏ hoặc mới gia nhập thị trường | "Tôi chưa có công cụ VoC. Tôi muốn hiểu nỗi đau của người dùng ví điện tử trên thị trường để chọn chỗ tạo khác biệt." |

## 3. Chỉ số thành công

### 3.1 Chất lượng agent (kết quả cuối đo trên tập kiểm tra 80 review gắn nhãn trước, D021–D022; xem [taxonomy.md §6](taxonomy.md))

| Chỉ số | Mục tiêu | Vai trò |
|---|---|---|
| **Recall của S1** | ≥ 95% | Chỉ số số 1: không được bỏ sót review mất tiền hoặc lừa đảo |
| **Precision của S1** | ≥ 70% | Chặn việc gắn S1 tràn lan để ép recall lên cao |
| Độ chính xác category | ≥ 85% | |
| Độ chính xác mức nghiêm trọng (đúng hoặc lệch ±1 bậc) | ≥ 90% | |
| Trích dẫn sai so với review gốc | 0 | Kiểm tra tự động: `evidence` phải khớp nguyên văn |

Mọi tỷ lệ đều báo cáo **kèm khoảng tin cậy 95%**, vì cỡ mẫu nhỏ.

### 3.2 Chứng minh AI có giá trị (so với baseline)

| So sánh | Mục tiêu |
|---|---|
| Agent so với **baseline từ khoá và số sao** | Vượt ≥ 10 điểm % ở cả recall S1 và độ chính xác category |
| Model nhỏ so với model lớn | Báo cáo bảng chất lượng / chi phí / tốc độ và chọn model theo mức "đủ tốt" |
| Thời gian phân tích | So với **thời gian tự phân loại tay 100 review**, đo bằng cách bấm giờ khi gắn nhãn tập ngẫu nhiên; mục tiêu nhanh hơn ≥ 10 lần |
| Chi phí | 0 đ phát sinh (chạy trong gói Max); vẫn ghi lại **chi phí API quy đổi trên 1.000 review** để người đọc có thể so sánh |

### 3.3 Tiêu chí thất bại (giả thuyết bị bác bỏ khi…)

- Baseline từ khoá đạt **≥ 90%** chất lượng của agent: LLM không đáng dùng cho bài toán này. Khi đó kết luận được viết thẳng trong case study.
- Sau 3 vòng cải tiến, recall S1 vẫn **< 85%**: agent chưa đủ tin cậy cho việc phát hiện rủi ro.
- Kết quả so sánh đảo thứ hạng hoàn toàn khi chỉnh trọng số trong khoảng hợp lý: kết luận so sánh không bền vững và không nên công bố.

### 3.4 Kết quả (tập kiểm tra 80 review, D022; chi phí và thời gian từ lần chạy 2.339 review, D023)

| Chỉ số | Mục tiêu | Kết quả | |
|---|---|---|---|
| Recall S1 | ≥ 95% | 100% (7/7; KTC 65–100%) | ✅ nhưng mẫu nhỏ |
| Precision S1 | ≥ 70% | 88% (7/8) | ✅ |
| Category | ≥ 85% | 85% | ✅ sát ngưỡng |
| Mức nghiêm trọng lệch ≤ 1 bậc | ≥ 90% | 99% | ✅ |
| Trích dẫn sai | 0 | 1/39 | ⚠️ |
| Hơn baseline | ≥ +10 điểm | category +29, recall S1 +71 | ✅ |
| Nhanh hơn làm tay | ≥ 10 lần | ≈ 7 lần theo thời gian chạy (0,8 so với 5,7 giây/review); gần như 100% thời gian của người được giải phóng vì agent chạy nền | ⚠️ một nửa |
| Chi phí phát sinh | 0 đ | 0 đ (gói Max); quy đổi API ≈ $9,6 / 1.000 review | ✅ |

## 4. Phạm vi

**Làm (v1):**
- Lấy review công khai trên Google Play trong 90 ngày gần nhất, kèm **ngày, phiên bản app, số sao và phản hồi của nhà phát triển (nếu có)**.
- Ẩn danh, rồi phân loại theo 9 category, mức nghiêm trọng S1–S4, `flow` (cho giao dịch lỗi) và cờ `social_engineering` (cho lừa đảo). Xem [taxonomy.md](taxonomy.md).
- Chạy baseline từ khoá và số sao song song với agent để so sánh.
- So sánh 4 app bằng **chỉ số chuẩn hoá** (§6).
- Người duyệt: PM xác nhận danh sách ưu tiên và các ca được chuyển sang hàng chờ duyệt (§5).
- Báo cáo so sánh đối thủ, kèm 1 PRD đề xuất cho một cơ hội được chọn.

**Làm nếu còn thời gian (stretch):**
- Đóng gói thành skill Claude Code.
- Bổ sung review từ App Store.

**Không làm (cố ý):**
- Theo dõi theo thời gian thực hoặc gửi cảnh báo tự động.
- Xếp hạng tổng thể "app nào tốt nhất". Báo cáo chỉ nói về từng luồng cụ thể, trong một khoảng thời gian cụ thể.

## 5. Giải pháp tổng quan

```
Google Play ──► Lấy dữ liệu ──► Ẩn danh ──┬──► Baseline từ khoá/số sao ──┐
  (review, ngày, phiên bản,               │                              ├──► Eval (tập đáp án)
   phản hồi của nhà phát triển)           └──► Agent phân loại ───────────┘
                                                     │
                                       Quy tắc chuyển sang người duyệt
                                                     │
                                                     ▼
                                     Chuẩn hoá ──► So sánh 4 app ──► [PM duyệt]
                                                                         │
                                       Báo cáo · Dashboard (artifact) · PRD đề xuất
```

**Quy tắc chuyển sang người duyệt** (không dùng mức tự tin do model tự báo):
1. Agent dự đoán S1.
2. Agent và baseline bất đồng về việc review có phải S1 hay không.

**Hạ tầng:** xử lý hàng loạt trong Claude Code (gói Max). Trang insight trên artifact cho mọi người xem, kèm **thanh chat hỏi đáp dữ liệu**: agent dùng công cụ ngay trong trang để tra cứu số liệu và review, trả lời có trích dẫn, chạy bằng tài khoản Claude của người xem và tự ẩn nếu không dùng được (D025).

## 6. Chỉ số so sánh và điểm ưu tiên (v1)

**So sánh giữa các app: mẫu số là nhóm review phàn nàn, không phải tổng số review (D016).**

"Review phàn nàn" là review có từ 5 từ trở lên và được phân loại khác `NON_ISSUE`. Lý do: dữ liệu thực tế cho thấy tổng số review có thể bị đẩy lên bởi các đợt tăng review khen (xem §7). Số review phàn nàn thì ổn định hơn nhiều, nên so sánh trong nhóm này công bằng hơn.

| Chỉ số | Cách tính |
|---|---|
| Tỷ trọng vấn đề | Số review thuộc (category, flow) / số review phàn nàn của app đó |
| Tỷ trọng S1 | Số review S1 / số review phàn nàn |
| Tỷ lệ phản hồi của nhà phát triển | Số review phàn nàn được phản hồi / số review phàn nàn, tách theo mức nghiêm trọng |
| Thời gian phản hồi | Trung vị số giờ từ lúc có review đến khi nhà phát triển phản hồi, tách theo mức nghiêm trọng |

**Điểm ưu tiên của một vấn đề trong một app:**

```
Priority = Tỷ trọng vấn đề (trong review phàn nàn) × Trọng số mức nghiêm trọng
Trọng số: S1 = 10 · S2 = 5 · S3 = 2 · S4 = 1
```

Kiểm tra độ nhạy: thử các bộ trọng số khác (ví dụ S1 = 5 hoặc 20), xem top 3 có đổi không, và ghi kết quả vào decision log.
Hệ số xu hướng theo thời gian và cộng điểm cho ý định rời bỏ được **để sang v2**, khi có đủ dữ liệu theo thời gian.

## 7. Giới hạn của dữ liệu

Các giới hạn này sẽ được nêu rõ trong mọi báo cáo:

- **Lệch do tự chọn:** người gặp sự cố có xu hướng viết review nhiều hơn, nên review lệch về phía tiêu cực. Chỉ dùng để **so sánh tương đối** giữa các app, không dùng để đo mức hài lòng tuyệt đối.
- **Chỉ có Android.** Không đại diện cho người dùng iOS.
- **Có đợt tăng đột biến review khen (đã quan sát thấy).** Từ đầu tháng 10/2026, ZaloPay tăng từ khoảng 120 lên khoảng 3.000 review mỗi tuần, tỷ lệ 5 sao từ 35% lên 96%, phần lớn là review rất ngắn ("ok", "tốt"). Trong cùng giai đoạn, số review 1–2 sao gần như không đổi. Báo cáo chỉ mô tả hiện tượng, không suy đoán nguyên nhân. Cách xử lý: so sánh trong nhóm review phàn nàn (§6).
- **Lượng review khác nhau giữa các app:** từ khoảng 1.400 (Viettel Money) đến khoảng 22.000 (ZaloPay) trong 90 ngày. App ít review có khoảng tin cậy rộng hơn.
- **Ngày của review** là ngày cập nhật gần nhất trên Google Play, có thể muộn hơn ngày viết lần đầu.
- **Không có ca "bị lừa mà tự chuyển tiền" trong tập đáp án** (D018). Đã đọc 200 ứng viên ban đầu và thêm 42 review có từ khoá lừa đảo, mạo danh, bị hack, nhưng không tìm thấy ca nào. Chữ "lừa đảo" trong review gần như luôn là cách nói bức xúc, hoặc dùng để chỉ việc bị trừ tiền tự động. Vì vậy **không đo được độ chính xác của agent với cờ `social_engineering`**, và báo cáo sẽ không đưa ra kết luận về nhóm này. Kênh phù hợp để nghiên cứu nhóm này là ticket CS hoặc báo cáo lừa đảo, không phải review công khai.
- **Gắn nhãn chỉ do một người làm**, nên có thể thiên lệch (xem cách giảm thiểu bên dưới).

## 8. Rủi ro và cách giảm thiểu

| Rủi ro | Cách giảm thiểu |
|---|---|
| Điều khoản sử dụng khi lấy dữ liệu | Chỉ dữ liệu công khai, khối lượng nhỏ, cho nghiên cứu cá nhân; không đăng lại dữ liệu thô |
| Lộ thông tin cá nhân | Ẩn danh trước khi phân loại; che số điện thoại, số tài khoản, email, tên |
| Phát biểu gây hiểu lầm về thương hiệu | Giọng trung lập; mọi nhận định đều kèm tỷ lệ, khoảng tin cậy và trích dẫn; không xếp hạng tổng thể; ghi rõ đây là phân tích cá nhân |
| Agent bịa trích dẫn | Kiểm tra tự động `evidence` khớp nguyên văn với review gốc |
| Review không dấu, teencode, mỉa mai | Đưa vào tập ca khó, báo cáo kết quả riêng |
| Thiên lệch của người gắn nhãn duy nhất | Đã thay bằng: so sánh lần gắn 1 và lần gắn 2 (D017), rà soát bất đồng người–model có ghi lý do (D020), và tập kiểm tra gắn nhãn trước khi chạy model (D021) |

## 9. Các mốc

| Tuần | Kết quả bắt buộc |
|---|---|
| 1 | PRD, bộ phân loại, decision log ✅ |
| 2 | Bộ lấy dữ liệu và ẩn danh (29.078 review); gắn nhãn tập ngẫu nhiên 100 review và tập ca khó 57 review ✅ |
| 3 | Baseline; agent v1 → v2; so sánh model; báo cáo eval kèm khoảng tin cậy ✅ (D022) |
| 4 | Chạy trên mẫu phân tầng 2.339 review; so sánh đối thủ; kiểm tra độ nhạy; trang insight có chat; PRD đề xuất ✅ (D023–D026) |
| 5 | **Case study, dashboard và báo cáo eval** (bắt buộc); video demo; skill là phần làm thêm |

## 10. Câu hỏi còn mở

- Mỗi review chỉ có 1 category (vấn đề nặng nhất). Cần kiểm tra trong lúc gắn nhãn xem có mất nhiều thông tin không. Nếu có, xét thêm category phụ ở v2.
- ~~90 ngày có đủ review không?~~ Đã kiểm tra: đủ cho cả 4 app sau khi thay VNPAY (D015).
- ~~Ngưỡng 5 từ có loại nhầm review phàn nàn ngắn không?~~ Đã kiểm tra (D023): chỉ 670/21.697 review ngắn là 1–3 sao, phần lớn chửi chung chung; ảnh hưởng nhỏ, ghi như một giới hạn.
- ~~Phản hồi theo mẫu có tính là đã phản hồi không?~~ Đã đo (D024): 69–100% phản hồi là văn mẫu, nên tỷ lệ và tốc độ phản hồi được báo cáo là **mức tự động hoá**, kèm chỉ số văn mẫu.
