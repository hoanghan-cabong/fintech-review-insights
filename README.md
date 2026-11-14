# Fintech Review Insights Agent

Agent AI phân tích review công khai trên Google Play của 4 ví điện tử Việt Nam (MoMo, ZaloPay, ShopeePay, Viettel Money) để trả lời một câu hỏi chiến lược: **đối thủ đang yếu ở đâu, và người dùng đang mất tiền theo cách nào?**

**Phát hiện chính:** gần một nửa số ca người dùng mất tiền (49%, KTC 44–54%) không đến từ giao dịch lỗi, mà từ việc **bị trừ tiền khi họ không đồng ý**: gói tự gia hạn, trừ từ ngân hàng liên kết không hỏi OTP, phí hay dịch vụ được chèn sẵn. Hiện tượng có ở cả 4 ví. → [PRD đề xuất: Trung tâm thanh toán tự động](docs/PRD_proposal_autopay.md)

**Trang insight có chat hỏi đáp dữ liệu:** https://claude.ai/artifact/DGZwuTtJ9oaWwiB2x7A8iP (hiện ở chế độ riêng tư)

Điểm khác biệt:
- **Chấm theo rủi ro tài chính**, không theo số sao: S1 = đã mất tiền hoặc có rủi ro mất tiền.
- **Chứng minh có cần AI:** trên tập kiểm tra gắn nhãn trước, bộ lọc từ khoá bắt 2/7 ca mất tiền, agent bắt 7/7 (precision 88%), chi phí quy đổi khoảng $9,6 / 1.000 review.
- **So sánh công bằng:** tính trong nhóm review phàn nàn, có trọng số, kèm khoảng tin cậy; không bị lệch bởi đợt tăng review khen của ZaloPay.
- **Eval trung thực:** tách tập phát triển và tập kiểm tra; ghi lại cả những lần chính người gắn nhãn sai (D017, D020).
- **Truy vết được:** mọi nhận định kèm trích dẫn nguyên văn; 27 quyết định thiết kế được ghi lại kèm lý do.

> Dự án portfolio cá nhân, hướng AI Product Management. Chỉ dùng dữ liệu công khai đã ẩn danh. Không đại diện cho quan điểm của doanh nghiệp nào.

## Tài liệu

| Tài liệu | Nội dung |
|---|---|
| [docs/PRD.md](docs/PRD.md) | Vấn đề, persona, chỉ số thành công và kết quả, tiêu chí thất bại, giới hạn dữ liệu |
| [docs/taxonomy.md](docs/taxonomy.md) | 9 category, 5 flow, thang S1–S4 với 10 quy tắc, thiết kế tập đáp án, baseline |
| [docs/decision-log.md](docs/decision-log.md) | 27 quyết định thiết kế và lý do |
| [docs/PRD_proposal_autopay.md](docs/PRD_proposal_autopay.md) | PRD đề xuất từ phát hiện số 1 |
| [reports/insights.md](reports/insights.md) | Bảng so sánh 4 ví đầy đủ |
| [reports/eval_report_test.md](reports/eval_report_test.md) | Kết quả eval cuối trên tập kiểm tra |
| [reports/eval_report.md](reports/eval_report.md) | Eval trên tập phát triển (Haiku, Opus v1, Opus v2, baseline) |

## Cấu trúc

```
src/
  scrape.py, anonymize.py        lấy và ẩn danh dữ liệu
  make_label_sets.py, make_*.py  tạo các tập gắn nhãn (ngẫu nhiên, ca khó, rà soát, kiểm tra)
  golden.py                      đọc tập đáp án (áp kết quả rà soát lên trên nhãn gốc)
  baseline.py                    baseline từ khoá và số sao
  agent.py                       agent phân loại qua `claude -p` (gói Max)
  evaluate.py                    chấm điểm, khoảng tin cậy, danh sách lỗi
  classify_corpus.py             chạy agent trên mẫu phân tầng 2.339 review
  s1_subtype.py                  phân loại cơ chế mất tiền cho review S1
  analyze.py                     so sánh 4 ví → reports/insights.md
  build_explorer.py              đóng gói dữ liệu cho trang insight
prompts/                         prompt phân loại v1, v2 và prompt phân loại cơ chế S1
tools/labeler.html               công cụ gắn nhãn tay (bấm giờ, phím tắt, chế độ rà soát)
explorer/index.html              trang insight + chat
```

## Chạy lại

```bash
python3 -m venv .venv && .venv/bin/pip install google-play-scraper
```
```bash
.venv/bin/python src/scrape.py && .venv/bin/python src/anonymize.py
```
```bash
.venv/bin/python src/baseline.py test && .venv/bin/python src/agent.py --model opus --prompt v2 --set test && .venv/bin/python src/evaluate.py test
```
```bash
.venv/bin/python src/classify_corpus.py && .venv/bin/python src/s1_subtype.py && .venv/bin/python src/analyze.py && .venv/bin/python src/build_explorer.py
```

Agent gọi Claude qua Claude Code CLI (`claude -p`), nên cần đăng nhập `claude` bằng tài khoản có gói phù hợp. `data/raw/` và `data/clean/` không đưa lên GitHub.

## Gắn nhãn tay

Mở [tools/labeler.html](tools/labeler.html) bằng Chrome rồi kéo thả file CSV trong `data/labels/` vào trang. Phím tắt: `1`–`9` category, `A S D F` mức S1–S4, `Z X C V B` flow, `Y`/`U` cờ bị lừa, `Enter` sang review tiếp. Đồng hồ chỉ đếm thời gian làm thật. File có cột `model_label` mở ở chế độ rà soát (bắt buộc ghi lý do).

## Trạng thái

- [x] Tuần 1: PRD, bộ phân loại, decision log
- [x] Tuần 2: Dữ liệu (29.078 review), công cụ gắn nhãn, tập đáp án 157 review
- [x] Tuần 3: Baseline, agent v1 → v2, so sánh Haiku/Opus, rà soát nhãn, tập kiểm tra 80 review (D022)
- [x] Tuần 4: Mẫu 2.339 review, so sánh 4 ví, cơ chế mất tiền, trang insight có chat, PRD đề xuất (D023–D026)
- [ ] Tuần 5: Case study, video demo, chia sẻ trang *(skill Claude Code là phần làm thêm)*
