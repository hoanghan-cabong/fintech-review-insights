# Báo cáo eval: TẬP KIỂM TRA CUỐI (D021)

80 review ngẫu nhiên, gắn nhãn trước khi chạy model, không dùng để sửa prompt. Khoảng trong ngoặc là khoảng tin cậy 95%.


## Tập kiểm tra

| Chỉ số | agent_v1_opus | agent_v2_opus | baseline |
|---|---|---|---|
| Độ chính xác category | 89% (71/80; 80%–94%) | 85% (68/80; 76%–91%) | 56% (45/80; 45%–67%) |
| Mức nghiêm trọng (đúng hẳn) | 82% (66/80; 73%–89%) | 85% (68/80; 76%–91%) | 69% (55/80; 58%–78%) |
| Mức nghiêm trọng (lệch ≤ 1 bậc) | 99% (79/80; 93%–100%) | 99% (79/80; 93%–100%) | 91% (73/80; 83%–96%) |
| **Recall S1** | 100% (7/7; 65%–100%) | 100% (7/7; 65%–100%) | 29% (2/7; 8%–64%) |
| **Precision S1** | 70% (7/10; 40%–89%) | 88% (7/8; 53%–98%) | 50% (2/4; 15%–85%) |
| Flow (khi cùng là TXN_FAILURE) | 75% (6/8; 41%–93%) | 71% (5/7; 36%–92%) | 20% (1/5; 4%–62%) |
| Trích dẫn khớp nguyên văn | 100% (41/41; 91%–100%) | 97% (38/39; 87%–100%) | – |

## Theo category (tập chính, category có ≥ 5 mẫu)

| Category | agent_v1_opus | agent_v2_opus | baseline |
|---|---|---|---|
| NON_ISSUE | 38/41 | 38/41 | 25/41 |
| TXN_FAILURE | 8/9 | 7/9 | 5/9 |
| AUTH_ACCESS | 8/8 | 7/8 | 2/8 |
| APP_EXPERIENCE | 5/7 | 5/7 | 6/7 |
| ONBOARD_EKYC | 4/5 | 3/5 | 4/5 |
| FEES_LIMITS | 4/5 | 4/5 | 2/5 |

## Quy tắc chuyển sang người duyệt (cả hai tập)

| Lần chạy | Review bị chuyển duyệt | Lỗi S1 của agent được bắt |
|---|---|---|
| agent_v1_opus | 11/80 (14%) | 3/3 |
| agent_v2_opus | 9/80 (11%) | 1/1 |

## Tiêu chí thất bại (PRD §3.3), trên tập chính

- **agent_v1_opus**: hơn baseline +32% ở category, +71% ở recall S1 (mục tiêu ≥ +10 điểm). Baseline đạt 63% chất lượng category của agent (ngưỡng thất bại ≥ 90%).
- **agent_v2_opus**: hơn baseline +29% ở category, +71% ở recall S1 (mục tiêu ≥ +10 điểm). Baseline đạt 66% chất lượng category của agent (ngưỡng thất bại ≥ 90%).

- Chi phí và thời gian `agent_v1_opus`: 80 review, 219.3 giây, $1.3799 quy đổi API (≈ $17.25 / 1.000 review).

- Chi phí và thời gian `agent_v2_opus`: 80 review, 217.9 giây, $0.594 quy đổi API (≈ $7.42 / 1.000 review).
