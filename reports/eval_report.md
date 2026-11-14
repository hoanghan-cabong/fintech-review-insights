# Báo cáo eval: tập phát triển

Tập đáp án: 100 review ngẫu nhiên, 57 ca khó. Khoảng trong ngoặc là khoảng tin cậy 95%.

Nhãn đã sửa sau vòng rà soát (D020, D021): 29 review.


## Tập ngẫu nhiên (chỉ số chính)

| Chỉ số | agent_v1_haiku | agent_v1_opus | agent_v2_opus | baseline |
|---|---|---|---|---|
| Độ chính xác category | 88% (88/100; 80%–93%) | 88% (88/100; 80%–93%) | 87% (87/100; 79%–92%) | 61% (61/100; 51%–70%) |
| Mức nghiêm trọng (đúng hẳn) | 87% (87/100; 79%–92%) | 93% (93/100; 86%–97%) | 92% (92/100; 85%–96%) | 64% (64/100; 54%–73%) |
| Mức nghiêm trọng (lệch ≤ 1 bậc) | 96% (96/100; 90%–98%) | 99% (99/100; 95%–100%) | 99% (99/100; 95%–100%) | 91% (91/100; 84%–95%) |
| **Recall S1** | 100% (9/9; 70%–100%) | 100% (9/9; 70%–100%) | 100% (9/9; 70%–100%) | 67% (6/9; 35%–88%) |
| **Precision S1** | 75% (9/12; 47%–91%) | 90% (9/10; 60%–98%) | 90% (9/10; 60%–98%) | 75% (6/8; 41%–93%) |
| Flow (khi cùng là TXN_FAILURE) | 87% (13/15; 62%–96%) | 100% (13/13; 77%–100%) | 100% (13/13; 77%–100%) | 91% (10/11; 62%–98%) |
| Trích dẫn khớp nguyên văn | 98% (56/57; 91%–100%) | 100% (57/57; 94%–100%) | 100% (56/56; 94%–100%) | – |

## Tập ca khó

| Chỉ số | agent_v1_haiku | agent_v1_opus | agent_v2_opus | baseline |
|---|---|---|---|---|
| Độ chính xác category | 89% (51/57; 79%–95%) | 86% (49/57; 75%–93%) | 88% (50/57; 77%–94%) | 68% (39/57; 56%–79%) |
| Mức nghiêm trọng (đúng hẳn) | 95% (54/57; 86%–98%) | 95% (54/57; 86%–98%) | 95% (54/57; 86%–98%) | 56% (32/57; 43%–68%) |
| Mức nghiêm trọng (lệch ≤ 1 bậc) | 98% (56/57; 91%–100%) | 100% (57/57; 94%–100%) | 100% (57/57; 94%–100%) | 81% (46/57; 69%–89%) |
| **Recall S1** | 95% (19/20; 76%–99%) | 100% (20/20; 84%–100%) | 95% (19/20; 76%–99%) | 70% (14/20; 48%–85%) |
| **Precision S1** | 95% (19/20; 76%–99%) | 100% (20/20; 84%–100%) | 100% (19/19; 83%–100%) | 67% (14/21; 45%–83%) |
| Flow (khi cùng là TXN_FAILURE) | 61% (11/18; 39%–80%) | 68% (13/19; 46%–85%) | 67% (12/18; 44%–84%) | 53% (9/17; 31%–74%) |
| Trích dẫn khớp nguyên văn | 98% (39/40; 87%–100%) | 100% (41/41; 91%–100%) | 98% (39/40; 87%–100%) | – |

## Theo category (tập chính, category có ≥ 5 mẫu)

| Category | agent_v1_haiku | agent_v1_opus | agent_v2_opus | baseline |
|---|---|---|---|---|
| NON_ISSUE | 42/46 | 43/46 | 44/46 | 28/46 |
| APP_EXPERIENCE | 15/18 | 14/18 | 13/18 | 11/18 |
| TXN_FAILURE | 15/17 | 13/17 | 13/17 | 11/17 |
| ONBOARD_EKYC | 5/6 | 6/6 | 6/6 | 4/6 |
| PROMO_REWARDS | 4/5 | 5/5 | 5/5 | 2/5 |
| AUTH_ACCESS | 4/5 | 5/5 | 4/5 | 2/5 |

## Quy tắc chuyển sang người duyệt (cả hai tập)

| Lần chạy | Review bị chuyển duyệt | Lỗi S1 của agent được bắt |
|---|---|---|
| agent_v1_haiku | 40/157 (25%) | 4/5 |
| agent_v1_opus | 39/157 (25%) | 1/1 |
| agent_v2_opus | 38/157 (24%) | 1/2 |

## Tiêu chí thất bại (PRD §3.3), trên tập chính

- **agent_v1_haiku**: hơn baseline +27% ở category, +33% ở recall S1 (mục tiêu ≥ +10 điểm). Baseline đạt 69% chất lượng category của agent (ngưỡng thất bại ≥ 90%).
- **agent_v1_opus**: hơn baseline +27% ở category, +33% ở recall S1 (mục tiêu ≥ +10 điểm). Baseline đạt 69% chất lượng category của agent (ngưỡng thất bại ≥ 90%).
- **agent_v2_opus**: hơn baseline +26% ở category, +33% ở recall S1 (mục tiêu ≥ +10 điểm). Baseline đạt 70% chất lượng category của agent (ngưỡng thất bại ≥ 90%).

- Chi phí và thời gian `agent_v1_haiku`: 157 review, 1009.9 giây, $0.8152 quy đổi API (≈ $5.19 / 1.000 review).

- Chi phí và thời gian `agent_v1_opus`: 157 review, 430.6 giây, $1.2663 quy đổi API (≈ $8.07 / 1.000 review).

- Chi phí và thời gian `agent_v2_opus`: 157 review, 439.3 giây, $1.2754 quy đổi API (≈ $8.12 / 1.000 review).
