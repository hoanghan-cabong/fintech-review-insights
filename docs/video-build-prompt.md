Dựng video promo "Review Risk Agent" trong project này, đúng theo một storyboard đã viết sẵn.

**Storyboard đã có rồi — đừng viết storyboard mới, cũng đừng dựng video demo phong cách.** Việc của bạn là dựng đúng cái đã thiết kế.

## Nguồn sự thật

Đọc HẾT file này trước khi viết dòng code nào:
/Users/hoanghan05/Documents/fintech-review-insights/docs/video-promo-storyboard.md

File nằm ngoài thư mục project; nếu bị hỏi quyền đọc thì tôi sẽ cho phép. Chỉ ĐỌC, không sửa gì trong `~/Documents/fintech-review-insights`.

Storyboard quyết định mọi thứ: chữ trên màn hình, màu, cỡ chữ, thời lượng từng cảnh tính bằng khung, spring config, chuyển cảnh, SFX. Khi tôi và storyboard nói khác nhau thì theo storyboard, trừ các ngoại lệ ghi rõ dưới đây.

## Project hiện tại

- `~/Documents/my-motion-video` — Remotion **4.0.544** (đã ghim đúng bản), React 19, Tailwind v4, TypeScript. Có git, mới một commit khởi tạo.
- Đang có composition mẫu `MyComp` (1280×720, 2 giây) trong `src/Composition.tsx`. **Xoá nó** và đăng ký hai composition mới trong `src/Root.tsx`.
- `public/` đang trống: chưa có logo, nhạc, sfx hay bản ghi màn hình.
- Remotion Studio dùng cấu hình `remotion-studio` trong `.claude/launch.json` (cổng 3000). Xem trước bằng cấu hình đó, **đừng mở thêm server nào khác**.
- Skill Remotion đã cài trong `.claude/skills`. Đọc `remotion-best-practices` trước khi bắt đầu, đọc `remotion-multimedia` trước khi làm phần video/âm thanh, và đọc `remotion-render` trước khi render.

## Cài thêm đúng một gói

```bash
npm i @remotion/google-fonts@4.0.544 --save-exact
```

Mọi gói `@remotion/*` phải **cùng phiên bản** với `remotion`. Lệch bản là Remotion báo lỗi hoặc render ra sai. Không cài thêm gói nào khác nếu chưa hỏi tôi.

## Cần dựng

1. **Hai composition**, 30fps, **1080×1080** (vuông, không phải 9:16):
   - `ReviewRiskAgentPromo` — 1.050 khung, 11 cảnh (mục 3 của storyboard).
   - `ReviewRiskAgentPromo20` — 600 khung, bản ngắn (mục 8): cảnh 1, 3, 4, 9, 10, và cảnh 11 rút còn 90 khung.
2. **`src/theme.ts`**: toàn bộ mã màu và ba spring config (`bouncy`, `punchy`, `smooth`) ở mục 2. Tailwind dùng cho bố cục thì được, nhưng **màu và thông số spring chỉ lấy từ `theme.ts`**. Không viết hex hay class màu Tailwind trong các cảnh.
3. **`src/timeline.ts`**: thời lượng các cảnh định nghĩa ở **đúng một chỗ**, cả hai composition đều đọc từ đây.
4. **Component dùng chung** theo mục 7: `KineticLine`, `CountUp`, `CircleMask`, `BlobBg`, `DrawStroke`, `ScreenCard`, `Pill`. Mỗi cảnh là một file trong `src/scenes/`.

## Ngoại lệ so với storyboard

**Font.** Storyboard bảo chép `.woff2` từ portfolio vào `public/fonts/`, nhưng bạn không có các file đó. Hãy nạp **Be Vietnam Pro** (400/500/600) và **Fraunces** qua `@remotion/google-fonts`. Nếu gói không có một trong hai font thì báo tôi. Không được để Remotion tự lấy font hệ thống.

**Logo `HH`.** Vẽ bằng code theo mô tả ở cảnh 5: ô bo tròn màu cobalt, chữ `HH` trắng. Không cần file ảnh.

**Âm thanh.** Chưa có nhạc và sfx. **Không tự tải nhạc trên mạng** vì dính bản quyền. Hãy làm như sau:
- Tạo `src/audio-config.ts` liệt kê tên file mong đợi trong `public/` (ví dụ `music.mp3`, `sfx-pop.mp3`, `sfx-whoosh.mp3`, `sfx-thump.mp3`…) và mốc khung của từng sfx theo bảng SFX của từng cảnh.
- File nào chưa có thì video vẫn render, chỉ là im lặng, không báo lỗi.
- Trong README, liệt kê đúng các file tôi cần bỏ vào `public/`.

## Bản ghi màn hình cho cảnh 7–9: chưa quay

Cảnh 7, 8, 9 dùng chung một file `public/take.mp4` mà tôi chưa quay.

- Tạo `src/take-config.ts` gồm cờ `HAS_TAKE`, và cho từng cảnh 7/8/9 hai số `startFrom` (tính theo khung của file nguồn) và `playbackRate`. Sau khi quay, đây là **file duy nhất** tôi phải sửa.
- Khi `HAS_TAKE = false`: `ScreenCard` hiện một khung xám bo góc rộng đúng 1040px, ghi "take.mp4 — cảnh 7/8/9". Cả video vẫn render được để xem nhịp.
- Khi `HAS_TAKE = true`: dùng `<OffthreadVideo>`, không dùng `<Video>`.
- Khi `playbackRate > 1`, **tự động** hiện nhãn `sped up N×` ở góc dưới-phải đúng như storyboard. Đây là ràng buộc trung thực, không phải chi tiết trang trí.
- Trong README, ghi cách tìm `startFrom` cho từng cảnh sau khi quay: mở take trong Studio, đọc số khung tại các mốc thao tác ở mục 6 storyboard.

## Ràng buộc không được vi phạm

- Chữ trên màn hình chép **nguyên văn** storyboard. Không sửa câu, không thêm câu, không thêm cảnh, không thêm hiệu ứng ngoài những gì storyboard ghi.
- `49%` luôn xuất hiện cùng `of money-loss complaints` và `95% CI 44–54%` trên cùng một màn hình.
- Màu vàng `#F9E75D` chỉ dùng ở cảnh 4.
- Không dùng easing `linear` cho chuyển động vào/ra. Mọi `spring()` lấy `fps` từ `useVideoConfig()`.
- Chỗ nào storyboard thiếu hoặc mâu thuẫn thì ghi lại và hỏi tôi, đừng tự chế cho xong.

## Thứ tự làm, có một điểm dừng

**Bước 1 — Khung.** Làm `theme.ts`, `timeline.ts`, `Root.tsx` với hai composition. Tạm cho mỗi cảnh hiện một ô ghi số cảnh và số khung, để tôi kiểm nhịp trong Studio ngay. Chạy `npm run lint` cho sạch rồi commit.

**Bước 2 — Phần mở đầu.** Làm các component dùng chung và **cảnh 1–4** (hook ba nhịp và con số 49%). Render ảnh tĩnh giữa mỗi cảnh vào `out/stills/`. Commit, rồi **DỪNG lại cho tôi duyệt**. Bốn cảnh này quyết định phong cách của cả video; sai ở đây thì sửa sớm sẽ rẻ hơn nhiều.

**Bước 3 — Sau khi tôi duyệt.** Làm cảnh 5–11, bản ngắn, phần âm thanh và phần bản ghi. Chạy toàn bộ phần kiểm tra bên dưới, render, rồi commit.

## Kiểm tra trước khi báo là xong

1. Thêm script `npm run check` kiểm: tổng khung đúng 1.050 và 600; các cảnh nối liền, không hở, không chồng; mọi mốc chuyển cảnh là bội của 15 (đúng phách 120 BPM); mỗi dòng chữ chính ≤ 5 từ, chữ phụ ≤ 6 từ.
2. `npm run lint` không còn lỗi.
3. Render ảnh tĩnh giữa mỗi cảnh vào `out/stills/` và tự xem lại từng ảnh: chữ không tràn khung, không chồng lên nhau, đúng màu.
4. Thu nhỏ vài ảnh tĩnh về rộng 390px để thử trên điện thoại. Chữ chính phải còn đọc rõ.
5. Render cả hai bản ra `out/promo-35s.mp4` và `out/promo-20s.mp4` (h264, crf 18), với `HAS_TAKE = false`.

## Báo cáo cuối

- Danh sách file đã tạo hoặc sửa.
- Kết quả từng bước kiểm tra, kể cả bước nào không đạt.
- Việc còn lại phía tôi: các file âm thanh cần bỏ vào `public/`, quay `take.mp4` theo mục 6 storyboard, điền `take-config.ts`, rồi render lại.
- Những chỗ bạn phải tự quyết vì storyboard không nói rõ.
