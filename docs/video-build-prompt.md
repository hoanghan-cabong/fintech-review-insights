Dựng video promo "Review Risk Agent" bằng Remotion, đúng theo storyboard có sẵn.

## Nguồn sự thật

Đọc HẾT file này trước khi viết dòng code nào:
/Users/hoanghan05/Documents/fintech-review-insights/docs/video-promo-storyboard.md

(Nếu không đọc được đường dẫn trên, dừng lại và báo tôi — tôi sẽ đính kèm file.)

Storyboard là nguồn sự thật cho mọi thứ: chữ trên màn hình, màu, cỡ chữ, thời lượng từng cảnh tính bằng khung, spring config, chuyển cảnh, SFX. Khi tôi và storyboard nói khác nhau, theo storyboard — trừ một ngoại lệ về font ghi ở dưới.

## Làm ở đâu

- Tạo dự án MỚI tại `~/Documents/review-risk-agent-promo`. Thư mục này hiện chưa có.
- KHÔNG sửa gì trong `~/Documents/fintech-review-insights` — chỉ đọc storyboard ở đó.
- Máy có sẵn Node v24 / npm 11. Khởi tạo bằng template Remotion trống (TypeScript). Sau khi cài xong, ghim phiên bản chính xác trong `package.json` (bỏ `^` và `~`) để render lại sau này ra đúng kết quả.

## Cần dựng

1. **Hai composition**, 30fps, 1080×1080:
   - `ReviewRiskAgentPromo` — 1.050 khung, 11 cảnh (mục 3 của storyboard).
   - `ReviewRiskAgentPromo20` — 600 khung, bản ngắn (mục 8): cảnh 1, 3, 4, 9, 10 và cảnh 11 rút còn 90 khung.
2. **`src/theme.ts`** chứa toàn bộ mã màu và ba spring config (`bouncy`, `punchy`, `smooth`) ở mục 2. Không được hardcode hex hay số spring rải rác trong các cảnh.
3. **Component dùng chung** theo cấu trúc ở mục 7: `KineticLine`, `CountUp`, `CircleMask`, `BlobBg`, `DrawStroke`, `ScreenCard`, `Pill`. Mỗi cảnh là một file trong `src/scenes/`.
4. **Thời lượng cảnh định nghĩa ở một chỗ duy nhất** (một mảng trong `src/timeline.ts`), cả hai composition đều đọc từ đó.

## Font — ngoại lệ duy nhất so với storyboard

Storyboard bảo chép `.woff2` từ portfolio vào `public/fonts/`. Bạn không có các file đó. Thay vào đó dùng `@remotion/google-fonts` để nạp **Be Vietnam Pro** (400/500/600) và **Fraunces**. Nếu gói đó không có một trong hai font, tải `.woff2` từ Google Fonts vào `public/fonts/` rồi nạp bằng `staticFile()`. Không bao giờ để Remotion lấy font hệ thống.

## Bản ghi màn hình cho cảnh 7–9 — chưa có

Cảnh 7, 8, 9 dùng một file `public/take.mp4` mà tôi CHƯA quay. Làm như sau:

- Tạo `src/take-config.ts` chứa một cờ `HAS_TAKE` và, cho từng cảnh 7/8/9, các số `startFrom` (tính theo khung của file nguồn) và `playbackRate`. Đây là chỗ DUY NHẤT tôi phải sửa sau khi quay.
- Khi `HAS_TAKE = false`: `ScreenCard` hiện một khung xám bo góc đúng kích thước 1040px, có chữ "take.mp4 — cảnh 7/8/9", để toàn bộ video vẫn render và xem nhịp được.
- Khi `HAS_TAKE = true`: dùng `<OffthreadVideo>` (không dùng `<Video>`).
- Nếu `playbackRate > 1` thì TỰ ĐỘNG hiện nhãn nhỏ `sped up N×` ở góc dưới-phải đúng như storyboard. Đây là ràng buộc trung thực, không phải trang trí.
- Viết vào README cách tôi tìm `startFrom` cho từng cảnh sau khi quay (ví dụ mở take trong Remotion Studio, đọc số khung tại các mốc thao tác ở mục 6 của storyboard).

## Ràng buộc không được vi phạm

- Chữ trên màn hình chép **nguyên văn** từ storyboard. Không sửa câu, không thêm câu, không thêm cảnh, không thêm hiệu ứng ngoài những gì đã ghi.
- Con số `49%` luôn xuất hiện cùng `of money-loss complaints` và `95% CI 44–54%` trên cùng màn hình.
- Màu vàng `#F9E75D` chỉ dùng ở cảnh 4.
- Không dùng easing `linear` cho chuyển động vào/ra. Mọi `spring()` lấy `fps` từ `useVideoConfig()`.
- Nếu thấy storyboard thiếu hoặc mâu thuẫn ở chỗ nào, ghi lại và hỏi tôi. Đừng tự chế cho xong.

## Kiểm tra trước khi báo là xong

1. Một script kiểm (`npm run check`) xác nhận: tổng khung 1.050 và 600; các cảnh nối liền không hở không chồng; mọi mốc chuyển cảnh là bội của 15 (đúng phách 120 BPM); mỗi dòng chữ chính ≤ 5 từ, chữ phụ ≤ 6 từ.
2. Render một ảnh tĩnh giữa mỗi cảnh vào `out/stills/` (`npx remotion still`), và tự xem lại từng ảnh: chữ không tràn khung, không chồng lên nhau, đúng màu.
3. Thu nhỏ vài ảnh tĩnh về rộng 390px để thử độ đọc được trên điện thoại — chữ chính phải còn đọc rõ.
4. Render cả hai bản ra `out/promo-35s.mp4` và `out/promo-20s.mp4` (h264, crf 18) với `HAS_TAKE = false`.

## Báo cáo cuối

- Danh sách file đã tạo.
- Lệnh mở Remotion Studio để tôi xem.
- Kết quả từng bước kiểm ở trên, kể cả chỗ nào không đạt.
- Những gì còn lại: quay `take.mp4` theo mục 6 storyboard, điền `take-config.ts`, render lại.
- Chỗ nào bạn đã phải tự quyết vì storyboard không nói rõ.
