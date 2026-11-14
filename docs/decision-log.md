# Decision Log

Mỗi quyết định ghi theo mẫu: **bối cảnh → các lựa chọn → quyết định → lý do → cách kiểm chứng sau**.
Quyết định bị thay đổi sẽ không bị xoá, mà được đánh dấu *Đã điều chỉnh bởi Dxxx*. Lịch sử thay đổi tư duy cũng là chất liệu cho case study.

---

### D001 · Chọn phân khúc ví điện tử · 2026-11-12
- **Lựa chọn:** ví điện tử (MoMo, ZaloPay, ShopeePay, VNPay) hoặc ngân hàng số.
- **Quyết định:** ví điện tử.
- **Lý do:** cùng mô hình kinh doanh nên so sánh công bằng; lượng review lớn; nhiều vấn đề liên quan đến tiền nên làm nổi bật cách chấm theo rủi ro.
- *Đã điều chỉnh bởi D015: VNPAY được thay bằng Viettel Money.*

### D002 · Google Play là nguồn dữ liệu chính · 2026-11-12
- **Lựa chọn:** Google Play, App Store, hoặc cả hai.
- **Quyết định:** chỉ Google Play cho v1. App Store là phần làm thêm.
- **Lý do:** App Store giới hạn số review lấy được. Android chiếm phần lớn người dùng ở Việt Nam. Google Play còn cho lấy phiên bản app và phản hồi của nhà phát triển (xem D008).
- **Giới hạn ghi nhận:** kết quả không đại diện cho người dùng iOS.

### D003 · Xử lý hàng loạt trong Claude Code, trình bày bằng artifact · 2026-11-12
- **Lựa chọn:** web app gọi API; artifact xử lý toàn bộ; hoặc kết hợp.
- **Quyết định:** phân loại hàng loạt và eval chạy trong Claude Code; dashboard tĩnh trên artifact; ô "Thử ngay" gọi Claude bằng tài khoản của người xem.
- **Lý do:** chi phí phát sinh bằng 0 (nằm trong gói Max); ai cũng xem được dashboard; demo tương tác vẫn có cho người dùng Claude.
- **Đánh đổi:** người không có tài khoản Claude không thử trực tiếp được.

### D004 · Chấm mức nghiêm trọng theo rủi ro, phân vân thì chọn mức cao hơn · 2026-11-12
- **Lựa chọn:** chấm theo số sao, theo cảm xúc, hoặc theo rủi ro tài chính và lòng tin.
- **Quyết định:** theo rủi ro (S1–S4). Phân vân trong các ca liên quan đến tiền hoặc bảo mật thì chọn mức cao hơn.
- **Lý do:** chi phí của hai loại sai không cân xứng. Bỏ sót một ca mất tiền tệ hơn nhiều so với báo nhầm.
- **Kiểm chứng:** recall S1 ≥ 95% là chỉ số số 1, **có chỉ số chặn precision S1 ≥ 70%** để không gắn S1 tràn lan *(bổ sung ở v0.2)*.

### D005 · Tự gắn nhãn tập đáp án, không dùng AI · 2026-11-12
- **Quyết định:** tự gắn nhãn tay.
- **Lý do:** tập đáp án là thước đo. Nếu AI tự gắn nhãn rồi tự chấm thì eval mất ý nghĩa.
- **Giới hạn ghi nhận:** chỉ một người gắn nhãn. Giảm thiểu bằng cách gắn nhãn lại 30 review sau một tuần để đo độ nhất quán.
- *Cỡ và cấu trúc tập đáp án đã điều chỉnh bởi D009.*

---

## Rà soát v0.2 (góc nhìn senior) · 2026-11-12

### D006 · Đổi trọng tâm: từ xử lý review sang thông tin đối thủ
- **Bối cảnh:** PM của một ví đã có ticket CS, dữ liệu trong app và công cụ VoC nội bộ, giàu hơn review công khai nhiều. Nếu chỉ "giúp PM đọc review" thì giá trị yếu.
- **Quyết định:** giá trị cốt lõi là **so sánh với đối thủ**, thứ dữ liệu nội bộ không có. Persona chính: PM / Strategy của một ví. Persona phụ: PM của fintech nhỏ, chưa có công cụ VoC. Bỏ persona CX Lead.
- **Lý do:** một persona sắc nét với một câu hỏi rõ ràng thuyết phục hơn ba persona mờ nhạt.

### D007 · Bắt buộc so sánh với baseline và đặt tiêu chí thất bại
- **Bối cảnh:** độ chính xác của agent đứng riêng một mình không chứng minh được LLM có giá trị.
- **Quyết định:** chạy baseline từ khoá và số sao song song; so sánh model nhỏ với model lớn theo chất lượng, chi phí và tốc độ; tự bấm giờ khi phân loại tay 100 review. Agent phải vượt baseline ≥ 10 điểm %. Nếu baseline đạt ≥ 90% chất lượng của agent thì kết luận LLM không đáng dùng.
- **Lý do:** AI PM phải trả lời được câu hỏi "có cần AI không" trước câu hỏi "AI làm tốt đến đâu".

### D008 · So sánh bằng tỷ lệ chuẩn hoá; thêm dữ liệu phản hồi của nhà phát triển
- **Bối cảnh:** lượng review chênh lệch lớn giữa các app. Nếu đếm số lượng thô, app lớn nhất sẽ luôn "nhiều vấn đề nhất".
- **Quyết định:** mọi so sánh đều dùng tỷ lệ trên 1.000 review của từng app. Lấy thêm ngày, phiên bản app và phản hồi của nhà phát triển. Thêm hai chỉ số: tỷ lệ phản hồi và thời gian phản hồi, tách theo mức nghiêm trọng.
- **Lý do:** so sánh công bằng là điều kiện để kết luận đứng vững. Dữ liệu phản hồi lấy được gần như miễn phí mà cho ra insight cạnh tranh rất mạnh.

### D009 · Tách tập đáp án: ngẫu nhiên và ca khó
- **Bối cảnh:** tập 150 review chọn có chủ đích (nhiều ca khó) không phản ánh phân phối thật. Chỉ 20 ca S1 thì một ca sai đã làm recall đổi 5 điểm %.
- **Quyết định:** tập ngẫu nhiên 100 review để đo chỉ số chính, tập ca khó 60 review để thử độ bền. Tổng cộng ≥ 35 ca S1. Mọi tỷ lệ báo cáo kèm khoảng tin cậy 95%.
- **Lý do:** kết quả đo phải trung thực về độ không chắc chắn.

### D010 · Bỏ `confidence` tự chấm, dùng quy tắc chuyển duyệt kiểm tra được
- **Bối cảnh:** mức tự tin do LLM tự báo thường không phản ánh đúng khả năng nó đúng hay sai, nên ngưỡng 0.6 là cảm tính.
- **Quyết định:** chuyển sang người duyệt khi (1) agent dự đoán S1, (2) hai lần chạy cho kết quả khác nhau, hoặc (3) baseline và agent bất đồng ở cờ liên quan đến tiền.
- **Kiểm chứng:** đo tỷ lệ review bị chuyển duyệt và tỷ lệ lỗi mà quy tắc này bắt được.
- *Đã điều chỉnh bởi D013: bỏ quy tắc (2) "chạy 2 lần", còn 2 quy tắc.*

### D011 · Thu hẹp phạm vi tuần 5; skill thành phần làm thêm
- **Quyết định:** bắt buộc có case study, dashboard và báo cáo eval. Skill Claude Code và App Store là phần làm thêm.
- **Lý do:** người tuyển dụng đánh giá dựa trên case study và kết quả, không dựa trên việc có bao nhiêu thứ được làm. Làm ít mà kỹ tốt hơn làm nhiều mà dở dang.

### D012 · Đơn giản hoá điểm ưu tiên; thêm luồng nghiệp vụ và ma sát do quy định
- **Quyết định:**
  - Điểm ưu tiên = tỷ lệ chuẩn hoá × trọng số mức nghiêm trọng. Hệ số xu hướng và cộng điểm cho ý định rời bỏ để sang v2.
  - Thêm trường `flow` (chuyển tiền, QR, nạp/rút, liên kết ngân hàng, trả sau…) để chi tiết hơn mà không tăng số category.
  - Thêm category `POLICY_FRICTION` để tách yêu cầu bắt buộc theo quy định khỏi lỗi sản phẩm.
  - Thêm cờ `social_engineering`: bị lừa mà người dùng tự chuyển tiền vẫn là S1, nhưng được phân tích riêng.
  - Bỏ cờ `after_update`, thay bằng metadata phiên bản app.
- **Lý do:** công thức càng nhiều hệ số chưa kiểm chứng càng khó bảo vệ. Chi tiết nên đặt ở chỗ phục vụ trực tiếp quyết định sản phẩm (luồng nào yếu), không đặt ở công thức.
- *Đã điều chỉnh bởi D013: flow rút còn 5; `POLICY_FRICTION` chuyển sang v2.*

---

## Rà soát v0.3 (tính khả thi) · 2026-11-12

### D013 · Rút gọn bộ phân loại và công gắn nhãn
- **Bối cảnh:** v0.2 thêm độ chặt chẽ đúng chỗ, nhưng cũng thiết kế quá tay. Mỗi review phải gắn khoảng 9 trường, tổng 160 review cộng 30 gắn lại, ước tính 8–10 giờ chỉ riêng gắn nhãn. 13 category trên tập ngẫu nhiên 100 review khiến nhiều category chỉ có 2–3 mẫu, gần như không đo được gì.
- **Nguyên tắc cắt:** giữ những gì tạo độ tin cậy với chi phí thấp (baseline, chuẩn hoá, precision S1, tách tập, kiểm tra trích dẫn, khoảng tin cậy). Bỏ những gì làm tăng công gắn nhãn mà v1 chưa dùng đến.
- **Quyết định:**
  - Category: từ 13 xuống 9. Gộp lỗi kỹ thuật, giao diện và đề xuất tính năng thành `APP_EXPERIENCE`; gộp khen và khác thành `NON_ISSUE`; chuyển `POLICY_FRICTION` sang v2.
  - Flow: từ 8 xuống 5, và chỉ gắn khi category là `TXN_FAILURE`.
  - Bỏ category phụ, bỏ cờ `money_at_risk`, `churn_intent`, `trust_damage`. Chỉ giữ `social_engineering`, và chỉ cho `FRAUD_SECURITY`.
  - Quy tắc chuyển sang người duyệt: từ 3 xuống 2 (bỏ "chạy 2 lần" vì nhân đôi số lần chạy).
  - Tập đáp án: 100 ngẫu nhiên và 40 ca khó (≥ 30 ca S1); gắn lại 20 thay vì 30.
  - Đo thời gian phân loại tay bằng cách bấm giờ ngay khi gắn nhãn tập ngẫu nhiên, không làm bước riêng.
- **Kết quả:** công gắn nhãn còn khoảng 4–5 giờ, tức giảm khoảng một nửa. Bốn điểm mạnh của câu chuyện vẫn giữ nguyên: chấm theo rủi ro, so với baseline, so sánh chuẩn hoá, và tốc độ phản hồi của nhà phát triển.
- **Bài học:** độ chặt chẽ chỉ có giá trị khi phục vụ một quyết định cụ thể. Chi tiết chưa dùng ở v1 thì để sang v2.

---

## Điều chỉnh theo dữ liệu thực tế (tuần 2) · 2026-11-12

Số liệu 90 ngày (14/08–12/11/2026):

| App | Tổng review | Review ≥ 5 từ | 5 sao | Tỷ lệ phản hồi (review ≥ 5 từ) | Trung vị giờ phản hồi |
|---|---|---|---|---|---|
| MoMo | 2.945 | 1.634 (55%) | 48% | 85% | 0,4 |
| ZaloPay | 22.324 | 4.210 (19%) | 94% | 72% | 15,0 |
| ShopeePay | 2.420 | 994 (41%) | 63% | 98% | 39,8 |
| Viettel Money | 1.389 | 543 (39%) | 60% | 36% | 3,1 |
| *VNPAY (đã loại)* | *71* | *57* | *31%* | *72%* | *209,7* |

*Tỷ lệ phản hồi ở đây tính trên mọi review ≥ 5 từ, chưa tách nhóm phàn nàn. Bảng này chỉ để mô tả dữ liệu, chưa phải kết quả phân tích.*

### D014 · Review dưới 5 từ được gán NON_ISSUE bằng quy tắc
- **Bối cảnh:** 45–81% review mỗi app là câu rất ngắn ("ok", "tốt", "good"). Đưa những review này qua agent vừa tốn công vừa không có thông tin.
- **Quyết định:** review dưới 5 từ được gán `NON_ISSUE` tự động. Tập đáp án và agent chỉ xử lý review từ 5 từ trở lên.
- **Rủi ro:** có thể bỏ sót review phàn nàn rất ngắn ("mất tiền rồi"). **Kiểm chứng:** đọc ngẫu nhiên khoảng 50 review dưới 5 từ, đếm số ca bị loại nhầm.

### D015 · Thay VNPAY bằng Viettel Money
- **Bối cảnh:** app VNPAY chỉ có 71 review trong 90 ngày, quá ít để tính tỷ trọng theo từng category với khoảng tin cậy chấp nhận được.
- **Lựa chọn:** giữ VNPAY; chỉ so sánh 3 ví; thay bằng một ví khác.
- **Quyết định:** thay bằng Viettel Money (`com.bplus.vtpay`, 1.389 review cùng kỳ).
- **Ghi nhận:** việc VNPAY có rất ít review trên app riêng là một quan sát đáng nêu. Có thể phần lớn người dùng tiếp cận VNPAY qua QR trong app ngân hàng, nhưng đây chỉ là giả thuyết, chưa kiểm chứng.

### D016 · So sánh trong nhóm review phàn nàn, không chia trên tổng số review
- **Bối cảnh:** từ tuần đầu tháng 10/2026, ZaloPay tăng từ khoảng 120 lên khoảng 3.000 review mỗi tuần, tỷ lệ 5 sao từ 35% lên 96%, trong khi số review 1–2 sao gần như không đổi (479 trong 8 tuần trước, 581 trong 7 tuần sau). Nếu chia trên tổng số review như PRD v0.3, ZaloPay sẽ trông tốt một cách giả tạo.
- **Lựa chọn:** chia trên tổng số review; chia trên review ≥ 5 từ; bỏ giai đoạn có đợt tăng; chia trong nhóm review phàn nàn.
- **Quyết định:** mọi chỉ số so sánh đều tính **trong nhóm review phàn nàn** (≥ 5 từ và khác `NON_ISSUE`).
- **Lý do:** nhóm review phàn nàn không bị ảnh hưởng bởi đợt tăng review khen, và vẫn giữ trọn 90 ngày dữ liệu.
- **Đánh đổi:** không còn trả lời được câu hỏi "app nào bị phàn nàn nhiều hơn" theo số tuyệt đối, chỉ trả lời được "khi bị phàn nàn thì vì chuyện gì, và nặng đến đâu". Với mục tiêu tìm điểm yếu theo từng luồng, câu hỏi thứ hai mới là câu cần trả lời.
- **Bài học cho case study:** thiết kế trong PRD (chia trên 1.000 review) đã sai khi gặp dữ liệu thật. Phát hiện ra sớm nhờ kiểm tra phân phối dữ liệu trước khi phân tích.

---

## Chất lượng nhãn (tuần 2) · 2026-11-12

### D017 · Giữ lõi định nghĩa mức nghiêm trọng, làm rõ quy tắc và gắn lại
- **Bối cảnh:** lần gắn nhãn đầu cho tập ngẫu nhiên mất 11 phút (khoảng 5 giây mỗi review). Kết quả: S1 chiếm 36%, không có review S3 nào, và 33/52 review 1 sao bị gắn S1. Mức nghiêm trọng đang đi theo số sao và mức độ bực bội của người viết, không theo tiêu chí "đã mất tiền hoặc có rủi ro mất tiền". Ví dụ: không nhận OTP khi đăng ký, phí dịch vụ 10k, khuyến mãi không về đều bị gắn S1.
- **Lựa chọn:** (a) nới định nghĩa cho khớp nhãn đã gắn; (b) giữ định nghĩa, gắn lại.
- **Quyết định:** (b), kèm hai quy tắc làm rõ lấy từ chính lần gắn nhãn đầu:
  - Bị trừ tiền mà người dùng không đồng ý (phí tự ý, gói hoặc bảo hiểm tự tích sẵn) → S1. Phí đã công bố nhưng người dùng thấy cao → S3.
  - Lỗi app khi đang giao dịch: chưa bị trừ tiền → S2; đã bị trừ → S1; chỉ lag → S3.
  - Thêm cây quyết định 4 câu hỏi, hiển thị ngay trong công cụ gắn nhãn.
- **Cách gắn lại:** chỉ gắn lại cột mức nghiêm trọng (56 review); giữ category của lần 1; `NON_ISSUE` tự là S4. Mức cũ bị xoá khỏi file gắn lại để lần 2 không bị neo theo nhãn cũ.
- **Lý do:** chấm theo rủi ro là điểm khác biệt cốt lõi của dự án. Nếu nới định nghĩa thì S1 chiếm 36% và mất khả năng phân biệt.
- **Bài học cho case study:** người gắn nhãn (chính tôi) cũng mắc đúng lỗi mà dự án muốn khắc phục: chấm theo cảm xúc thay vì theo hậu quả. Định nghĩa trên giấy là chưa đủ, cần một công cụ đặt định nghĩa ngay tại chỗ ra quyết định. Lần 1 được giữ lại (`random_set_pass1.csv`) để so sánh với lần 2.

### D018 · Ghi nhận giới hạn: không có ca bị lừa mà tự chuyển tiền
- **Bối cảnh:** tập ca khó cần ≥ 4 ca `social_engineering`. Nguồn 200 ứng viên ban đầu không có ca nào. Đã tạo thêm file bổ sung gồm 42 review có từ khoá lừa đảo, mạo danh, bị hack, lấy cắp; đọc hết vẫn không có ca nào đúng định nghĩa.
- **Quan sát:** trong review, chữ "lừa đảo" gần như luôn là cách nói bức xúc ("app lừa đảo"), hoặc chỉ việc **bị trừ tiền tự động mà không đồng ý**, chứ không phải người dùng bị dụ tự chuyển tiền. Có thể người bị lừa kiểu này không coi đó là lỗi của app, nên không viết review.
- **Quyết định:** không tìm thêm. Giữ cờ `social_engineering` trong định dạng đầu ra, nhưng **không báo cáo độ chính xác cho cờ này** và không đưa ra kết luận về nhóm lừa đảo kiểu này. Review không dấu chỉ có 5 mẫu (mục tiêu 8), nên kết quả nhóm này chỉ báo cáo dạng định tính.
- **Lý do:** cố tìm thêm sẽ tốn công mà vẫn không chắc có. Ép một review vào nhóm này chỉ để đủ chỉ tiêu sẽ làm sai tập đáp án.
- **Bài học cho case study:** review công khai không phải nguồn tốt để nghiên cứu lừa đảo qua thao túng tâm lý. Chọn đúng nguồn dữ liệu cho từng câu hỏi cũng là một quyết định sản phẩm. Ngược lại, "bị trừ tiền tự động mà không đồng ý" nổi lên như nhóm S1 chính, và cần được kiểm chứng ở tuần 4.

---

## Agent v1 (tuần 3) · 2026-11-13

### D019 · Cách chạy agent v1 và chọn model so sánh
- **Quyết định:**
  - Agent chạy qua `claude -p` (Claude Code CLI) để nằm trong gói Max, kết quả ép theo JSON schema, mỗi lô 20 review. Review bị model bỏ sót được gọi lại riêng.
  - Agent **chỉ nhận nội dung review, không nhận số sao**, để kiểm chứng đúng tinh thần "chấm theo nội dung". Baseline vẫn dùng số sao.
  - So sánh **Haiku với Opus** (thay cho Sonnet như dự định ban đầu): hai đầu rẻ nhất và mạnh nhất cho thấy rõ nhất đánh đổi giữa chất lượng và chi phí.
- **Kết quả v1 trên tập ngẫu nhiên** (chi tiết: `reports/eval_report.md`):

  | | Baseline | Haiku | Opus |
  |---|---|---|---|
  | Category | 59% | 75% | 74% |
  | Mức nghiêm trọng đúng hẳn | 63% | 78% | 84% |
  | Recall S1 | 50% | 80% | 80% |
  | Precision S1 | 62% | 67% | 80% |
  | Trích dẫn nguyên văn | – | 98% | 100% |
  | Chi phí quy đổi / 1.000 review | 0 | ≈ $5,2 | ≈ $8,1 |

- **Đánh giá:** vượt baseline rõ rệt (category +15–16 điểm, recall S1 +30 điểm), nên tiêu chí thất bại không bị kích hoạt. Nhưng chưa đạt mục tiêu recall S1 ≥ 95% và category ≥ 85%.
- **Quan sát quan trọng:** trong 157 review, có 31 ca **cả Haiku và Opus cùng ra một đáp án nhưng khác nhãn tay**. Đọc thử thì nhiều ca là nhãn tay chưa đúng theo taxonomy (ví dụ "thu phí dịch vụ 10k????" gắn S1, "tự động trừ tiền" gắn S2), chứ không phải model sai. Cần một vòng rà soát nhãn trước khi sửa prompt (D020).

### D020 · Rà soát nhãn bằng bất đồng giữa người và model; cảnh báo thiên lệch
- **Cách làm:** lấy 31 ca mà Haiku và Opus cùng một đáp án nhưng khác nhãn tay. Người gắn nhãn xem nhãn tay, đáp án model và trích dẫn, rồi quyết định giữ hoặc sửa, có ghi lý do (`data/labels/adjudication.csv`). Nhãn gốc giữ nguyên; `golden.py` áp thay đổi lên trên.
- **Kết quả:** sửa 26/31 ca (25 ca theo đúng đáp án model), giữ 5 ca. Phần lớn là sửa category (ví dụ lỗi đăng nhập bị gắn nhầm vào eKYC hoặc trải nghiệm app) và hạ mức các ca bị chấm theo cảm xúc.
- **Chỉ số v1 sau rà soát (tập ngẫu nhiên):**

  | | Baseline | Haiku | Opus |
  |---|---|---|---|
  | Category | 61% | 88% | 87% |
  | Mức nghiêm trọng đúng hẳn | 63% | 86% | 92% |
  | Recall S1 | 62% (5/8) | 100% (8/8) | 100% (8/8) |
  | Precision S1 | 62% | 67% | 80% |

- **⚠️ Thiên lệch cần nói rõ:** nhãn được sửa theo hướng đáp án của chính model v1, và ghi chú lý do đa phần chỉ là "sửa". Vì vậy các con số sau rà soát **lạc quan hơn thực tế** cho v1. Báo cáo sẽ luôn đưa cả hai con số (trước và sau rà soát), và kết quả cuối cùng phải đo trên một **tập kiểm tra mới, gắn nhãn trước khi xem đáp án của model** (D021).
- **Lỗi còn lại chủ yếu do taxonomy chưa rõ, không phải do model:**
  - "Tiền bị treo" nghĩa là giao dịch bị treo, hay cả việc **không rút được tiền đang có trong ví** (app lỗi, tài khoản bị khoá)? Model coi là S1, nhãn tay coi là S2.
  - Review chửi "app tiếp tay lừa đảo" không kể sự việc: nhãn tay S1, Opus S3. Theo quy tắc "từ lừa đảo để bày tỏ bực bội không làm tăng mức" thì model đúng hơn.
  - Review về dịch vụ bên thứ ba (Alarmy trên Google Play bị trừ 1 triệu) đăng ở trang của ví: có tính là vấn đề của ví không?

### D021 · Chốt 3 quy tắc, tách tập phát triển và tập kiểm tra, dừng tối ưu sau v2
- **Ba quy tắc mới** (taxonomy §4, quy tắc 8–10), áp vào prompt v2 và vào 3 nhãn bị ảnh hưởng trong tập phát triển:
  - Không rút được tiền trong ví do tài khoản bị khoá hoặc bị đánh dấu nghi ngờ → `AUTH_ACCESS`, S1. Do app lỗi tạm thời → S2.
  - Chửi "lừa đảo" mà không kể sự việc → `NON_ISSUE`, S4.
  - Bị trừ tiền cho dịch vụ bên thứ ba qua ví hoặc ngân hàng liên kết với ví, không đồng ý → `TXN_FAILURE` / `payment` / S1. Không thấy ví liên quan → `NON_ISSUE`.
- **Tách tập:** 157 review cũ trở thành **tập phát triển**, chỉ dùng để sửa prompt. **Tập kiểm tra** mới gồm 80 review ngẫu nhiên (20 mỗi app, chưa từng xuất hiện ở đâu), **gắn nhãn trước khi chạy model**, và chỉ chạy model đúng một lần. Script từ chối chạy model trên tập kiểm tra khi nhãn chưa đủ.
- **Dừng tối ưu sau v2:** không lặp v3, v4 trên tập phát triển, vì càng lặp càng khớp với chính tập đó.
- **Chọn Opus làm model chính:** precision S1 tốt hơn Haiku (80% so với 67%), chỉ đắt hơn khoảng 1,5 lần. Haiku là phương án dự phòng.
- **Kế hoạch cho tuần 4:** chạy Opus trên mẫu tối đa 600 review mỗi app (≥ 5 từ), thay vì toàn bộ 7.381 review. Chi phí quy đổi khoảng $19 thay vì khoảng $60, đỡ chạm giới hạn gói Max. Báo cáo so sánh tỷ trọng nên 600 review mỗi app là đủ (khoảng tin cậy khoảng ±4 điểm).

### D022 · Kết quả cuối trên tập kiểm tra; chốt Opus + prompt v2
- **Tập kiểm tra:** 80 review ngẫu nhiên, gắn nhãn trước khi chạy model (7,5 phút, trung vị 4 giây mỗi review), không rà soát lại sau khi xem kết quả. Chạy đúng một lần. Chi tiết: `reports/eval_report_test.md`.

  | Chỉ số | Baseline | Opus v1 | **Opus v2** | Mục tiêu |
  |---|---|---|---|---|
  | Category | 56% | 89% | **85%** | ≥ 85% ✅ |
  | Mức nghiêm trọng đúng hẳn | 69% | 82% | **85%** | |
  | Mức nghiêm trọng lệch ≤ 1 bậc | 91% | 99% | **99%** | ≥ 90% ✅ |
  | Recall S1 | **29%** (2/7) | 100% (7/7) | **100%** (7/7; KTC 65–100%) | ≥ 95% ✅* |
  | Precision S1 | 50% | 70% | **88%** (7/8) | ≥ 70% ✅ |
  | Trích dẫn nguyên văn | – | 100% | **97%** (38/39) | 100% ⚠️ |
  | Review bị chuyển duyệt | – | 14% | **11%** | |

  \* Chỉ có 7 ca S1, nên khoảng tin cậy rất rộng (65–100%). Kết quả này nhất quán với tập phát triển (recall S1 95–100%), nhưng chưa đủ để khẳng định chắc chắn ≥ 95%.
- **Đánh giá:**
  - **AI có giá trị rõ ràng:** baseline từ khoá chỉ bắt được 2/7 ca S1; agent bắt được 7/7. Category hơn baseline 29 điểm.
  - **Prompt v2 đáng dùng hơn v1:** precision S1 tăng từ 70% lên 88% (ít báo nhầm hơn), category giảm 4 điểm nhưng nằm trong biên sai số (3 review).
  - **Lỗi còn lại** chủ yếu là ranh giới giữa các category gần nhau (eKYC và đăng nhập; NON_ISSUE và góp ý nhẹ). 1 ca S1 "báo nhầm" có thể là nhãn tay chưa đúng ("lỗi trừ tiền nhưng giao dịch không thành công" được gắn S2, trong khi quy tắc 7 nói đã bị trừ tiền là S1). Ca này **không sửa** để giữ tập kiểm tra sạch.
  - **Chi phí:** chi phí quy đổi CLI báo dao động theo cache (từ $7 đến $17 cho 1.000 review trong các lần chạy). Dùng mức trung bình khoảng **$8 / 1.000 review** để lập kế hoạch.
- **Quyết định:** chốt **Opus + prompt v2** cho tuần 4. Dừng tối ưu prompt.

---

## Phân tích đối thủ (tuần 4) · 2026-11-13

### D023 · Chạy agent trên mẫu phân tầng 2.339 review
- **Lấy mẫu:** trong review ≥ 5 từ, mỗi ví lấy tối đa 450 review 1–3 sao và 150 review 4–5 sao, có trọng số khi tính tỷ lệ. Lý do: ZaloPay có 77% review ≥ 5 từ là 4–5 sao (đợt tăng review khen); lấy ngẫu nhiên đơn thuần sẽ có quá ít review phàn nàn của ZaloPay.
- **Chạy:** Opus + prompt v2, 3 lô song song, 2.339/2.339 review, 33 phút, chi phí quy đổi $22,5 (≈ $9,6 / 1.000 review), nằm trong gói Max.
- **Thời gian so với làm tay:** người gắn nhãn mất khoảng 5,7 giây mỗi review (tập kiểm tra); agent khoảng 0,8 giây mỗi review, tức nhanh hơn khoảng 7 lần theo thời gian chạy, **chưa đạt mục tiêu 10 lần** của PRD. Có thể tăng số lô song song, nhưng không cần: lợi ích chính là agent chạy nền, không tốn thời gian của người.
- **Ngưỡng 5 từ:** đọc kiểm tra review ngắn: chỉ 670/21.697 review dưới 5 từ là 1–3 sao, phần lớn chửi chung chung ("tệ", "rác"); khoảng một phần ba nêu vấn đề cụ thể, rất ít ca giống S1. Giữ ngưỡng, ghi như một giới hạn nhỏ.

### D024 · Phản hồi của đội phát triển phần lớn là văn mẫu: đổi cách diễn giải
- **Phát hiện:** 69–100% phản hồi là văn mẫu (70 ký tự đầu trùng với ≥ 5 phản hồi khác). ShopeePay có 2 kiểu mở đầu cho 384 phản hồi; MoMo 7 kiểu cho 400 phản hồi. ZaloPay có văn mẫu riêng theo loại vấn đề (giao dịch, phí). Viettel Money đa dạng nhất (48 kiểu cho 182 phản hồi) nhưng chỉ phản hồi khoảng một nửa.
- **Quyết định:** báo cáo tỷ lệ và tốc độ phản hồi là **mức tự động hoá**, kèm chỉ số văn mẫu; không dùng chúng để nói về chất lượng chăm sóc khách hàng. Trả lời luôn câu hỏi mở trong PRD về phản hồi theo mẫu.

### D025 · Thêm thanh chat hỏi đáp dữ liệu vào trang insight
- **Yêu cầu:** cho phép hỏi đáp câu đơn giản dựa trên dữ liệu, không tốn thêm tiền ngoài gói Max.
- **Đánh giá khả thi:** khả thi. Trang artifact có thể gọi Claude bằng tài khoản của người xem, nên với chủ sở hữu dùng gói Max thì không phát sinh chi phí. Người xem không có quyền dùng Claude vẫn xem đủ phần số liệu; thanh chat tự ẩn.
- **Thiết kế:** agent có 3 công cụ chạy ngay trong trang trên dữ liệu đã phân loại (`get_overview`, `compare_apps`, `search_reviews`). Agent buộc phải lấy số liệu qua công cụ, trích dẫn mã review (bấm để xem nguyên văn), báo khi mẫu nhỏ, không xếp hạng tổng thể. Mọi tính toán (tỷ trọng có trọng số, khoảng tin cậy) làm bằng code trong trang, model chỉ chọn câu hỏi cần tra và diễn đạt kết quả.
- **Lý do chọn cách này:** dữ liệu khoảng 800 KB, quá lớn để nhét vào mỗi câu hỏi; công cụ giúp câu trả lời bám dữ liệu và giảm bịa số. Đây cũng là một ví dụ nhỏ về agent dùng công cụ, thể hiện đúng chủ đề "AI trong sản phẩm".
- **Giới hạn:** chưa tự kiểm tra được thanh chat end-to-end, vì lần gọi đầu cần chủ tài khoản bấm cho phép.

### D026 · Phát hiện chính, phân loại phụ cho S1 và PRD đề xuất
- **Phân loại phụ cho S1:** thêm một bước gán cơ chế mất tiền cho 435 review S1 (bị trừ không đồng ý, giao dịch lỗi đã bị trừ, chậm hoàn, tài khoản bị khoá, bị chiếm tài khoản, bị lừa, khác). Bước này không có tập đáp án; đọc kiểm tra ngẫu nhiên 23 ca, 22 ca đúng. Ghi rõ là phân tích phụ.
- **Phát hiện chính** (chi tiết: `reports/insights.md`, `reports/key_findings.json`):
  1. Bị trừ tiền không đồng ý là cơ chế mất tiền số 1: 49% số review S1 (KTC 44–54%), có ở cả 4 ví.
  2. MoMo và ZaloPay: giao dịch lỗi chiếm gần 40% phàn nàn; MoMo là ví duy nhất có giao dịch lỗi nhiều hơn trừ không đồng ý trong nhóm S1.
  3. Mỗi ví có điểm nghẽn riêng: Viettel Money về phí (25%, chủ yếu phí ePass), ShopeePay về khuyến mãi mời bạn và eKYC.
  4. Phản hồi nhanh không có nghĩa là được hỗ trợ (D024).
- **Điểm ưu tiên trong từng ví ít giá trị phân biệt:** "Giao dịch lỗi" đứng đầu ở cả 4 ví với mọi bộ trọng số. Kiểm tra độ nhạy: 3/4 ví giữ nguyên top 3 (MoMo, ZaloPay đổi thứ tự trong top 3); Viettel Money đổi khi giãn trọng số. Vì vậy câu chuyện cạnh tranh dựa vào **chênh lệch so với 3 ví còn lại** và **cơ chế mất tiền**, còn điểm ưu tiên chỉ dùng trong PRD của từng ví.
- **Quy tắc chuyển duyệt (PRD §5)** không được chạy trên 435 ca S1 của tuần 4, vì đây là phân tích một lần, không phải hệ thống vận hành. Thay vào đó: precision S1 88% trên tập kiểm tra và đọc kiểm tra ngẫu nhiên. Quy tắc chuyển duyệt giữ nguyên như thiết kế cho khi dùng thật (11% review cần người duyệt trên tập kiểm tra).
- **PRD đề xuất:** "Trung tâm thanh toán tự động" (`docs/PRD_proposal_autopay.md`), với north star đo bằng chính agent này hằng tháng. Ghi rõ cần kiểm chứng bằng dữ liệu nội bộ trước khi cam kết.

### D027 · Rà soát cuối tuần 1–4: những gì giữ nguyên và việc tồn đọng
- **Đã đồng bộ:** PRD lên v1.0 (kết quả, hạ tầng chat, các câu hỏi mở đã trả lời), taxonomy (cách đo độ nhất quán đã thay đổi), README.
- **Lỗi trích dẫn duy nhất trên tập kiểm tra** (`gp_momo_02159`): model nối hai đoạn nguyên văn bằng "…". Không phải bịa nội dung, nhưng vi phạm yêu cầu "liền mạch". Sửa ở prompt v3 nếu tối ưu tiếp (thêm câu "không dùng dấu … để nối"); hiện chưa sửa vì đã chốt dừng tối ưu (D021).
- **Tồn đọng có chủ đích:** tập kiểm tra chỉ có 7 ca S1; phân loại cơ chế S1 chỉ được kiểm tra bằng 23 ca; chỉ một người gắn nhãn; chưa có git. Các điểm này được nêu trong phần giới hạn, không che đi.

---

<!-- Quyết định tiếp theo: D028 ... -->
