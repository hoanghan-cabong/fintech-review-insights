# Video promo 35 giây — Review Risk Agent

> Dựng bằng **Remotion**. Tài liệu này đủ chi tiết để đưa thẳng cho người dựng hoặc cho Claude Code.
> Phong cách: motion graphics, kinetic typography, mỗi cảnh một ý, chuyển cảnh liền mạch.

---

## 1 · Brief

| | |
|---|---|
| **Nhiệm vụ** | Mồi câu. Giữ người xem 35 giây rồi đẩy họ sang trang công cụ. |
| **Không phải nhiệm vụ** | Chứng minh phương pháp. Phần đó do video demo 100 giây ([docs/video-script.md](video-script.md)) và chính trang web gánh. |
| **Người xem** | Nhà tuyển dụng lướt LinkedIn, tắt tiếng, quyết định dừng hay lướt trong 2 giây đầu. |
| **Độ dài** | 35 giây · 1.050 khung @ 30fps |
| **Khung hình** | 1080×1080 (vuông). Mọi chữ nằm trong vùng an toàn giữa 1080×1350 để cắt 9:16 không mất chữ. |
| **Đăng ở** | LinkedIn, đầu trang portfolio, phần mô tả của video demo dài |

**Một câu phải đọng lại:** *gần một nửa số ca mất tiền trong ví điện tử không phải bị hack — mà là bị trừ tiền.*

**Ràng buộc trung thực.** Video này ngắn nên dễ nói quá. Ba luật:
- Được nói **49%**, nhưng luôn kèm dòng nhỏ `95% CI 44–54%`. Dự án này lấy khoảng tin cậy làm chữ ký, bỏ đi là tự phản bội.
- **Không** nói "7 out of 7", "AI-powered", "cutting-edge", hay bất kỳ tuyên bố độ chính xác nào. Tập kiểm tra chỉ có 7 ca S1.
- Mọi con số trên màn hình phải truy được về `reports/key_findings.json`.

---

## 2 · Hệ thiết kế

### Màu — lấy thẳng từ `assets/site.css`, không chế thêm

| Vai trò | Hex | Dùng ở đâu |
|---|---|---|
| Nền tối | `#171631` | nền chính của cảnh tối |
| Nền tối sâu | `#0F0E24` | nền cảnh 7 (con số lớn) |
| Nền sáng | `#FFFFFF` | cảnh sáng, xen kẽ tạo nhịp |
| Nền hồng nhạt | `#FFF3FA` | nền cảnh sản phẩm |
| **Hồng thương hiệu** | `#FF8AD3` | màu nhấn chính trên nền tối |
| Hồng đậm | `#D92A87` | nhấn trên nền sáng (hồng nhạt không đọc được trên trắng) |
| **Vàng** | `#F9E75D` | điểm nhấn, đúng một lần ở cảnh 7 |
| Cobalt | `#1609B7` | chi tiết giao diện, nút |
| Chữ trên nền tối | `#FFFFFF` | |
| Chữ phụ | `#A9A5C4` | dòng nhỏ, CI |

> **Luật màu:** một cảnh dùng tối đa **2 màu nhấn**. Vàng xuất hiện **đúng một lần** trong cả video — ở cảnh 7. Dùng nhiều hơn là mất tác dụng.

### Chữ

- Font: **Be Vietnam Pro** — `assets/fonts/be-vietnam-pro-latin-600-normal.woff2` (và 500/400). Đây là font đang dùng trên portfolio, dáng sans tròn hiện đại, đúng phong cách yêu cầu.
- Cỡ chữ chính: **96–140px** trên khung 1080. Chữ phải to tới mức xem trên điện thoại không cần nhíu mắt.
- Dòng nhỏ / CI: **26px**, màu `#A9A5C4`, letter-spacing `.04em`.
- **Tối đa 5 từ một màn hình.** Quá 5 từ là tách cảnh.
- Chữ hiện **theo từng từ**, không hiện cả câu. Mỗi từ lệch nhau 3 khung (100ms).

### Chuyển động — thông số Remotion cụ thể

```ts
// Nảy: dùng cho chữ, con số, icon vào khung
const bouncy  = { damping: 12,  stiffness: 180, mass: 0.8 };
// Mượt không nảy: dùng cho nền, mặt nạ, camera
const smooth  = { damping: 200, stiffness: 100, mass: 1   };

const t = spring({ frame: frame - delay, fps, config: bouncy });
```

| Quy tắc | Giá trị |
|---|---|
| Stagger giữa các phần tử anh em | **3 khung** (100ms) |
| Chữ vào | `translateY: interpolate(t,[0,1],[40,0])` + `opacity` + `scale` từ `0.92` |
| Overshoot | để `damping: 12` tự tạo, **không** tự viết keyframe vượt đích |
| Không bao giờ | chuyển động tuyến tính (`linear`). Mọi thứ đều spring hoặc ease-in-out. |

### Chuyển cảnh

Gần như không cắt cứng. Ba kiểu, dùng xen kẽ:

1. **Mặt nạ tròn** — vòng tròn nở từ tâm phần tử vừa nhấn, phủ khung, lộ cảnh sau. 12 khung, `smooth`.
2. **Match cut** — phần tử cảnh trước biến thành phần tử cảnh sau (chữ → logo, khối tròn → nền).
3. **Đẩy khối tròn** — khối tròn lớn tràn mép trượt qua khung mang theo cảnh mới.

### Hình khối nền

- Khối tròn lớn (600–900px) tràn ra ngoài mép, `blur(40px)`, `opacity .35`, màu hồng thương hiệu.
- Nét cong vẽ dần (`strokeDasharray` chạy) màu `#FF8AD3`, nét 8px, bo đầu tròn. Dùng ở cảnh 2 và 9.
- Icon phẳng, không dùng ảnh chụp.

---

## 3 · Storyboard — 11 cảnh

> Ký hiệu: `f` = khung hình @30fps. Chữ in đậm trong cột *Trên màn hình* là từ được tô màu nhấn.

### Cảnh 1 · Mồi (f0–90 · 0:00–0:03)

| | |
|---|---|
| **Nền** | `#171631`, khối tròn hồng mờ tràn góc dưới-phải |
| **Trên màn hình** | `You didn't get hacked.` — chữ trắng `#FFFFFF` |
| **Chuyển động** | Từng từ một, stagger 3f, `bouncy`. Từ `hacked.` vào trễ thêm 6f để tạo khoảng nghỉ. |
| **Chuyển ra** | Match cut: chữ `hacked.` co về tâm, biến thành chữ cảnh 2 |
| **SFX** | pop nhẹ mỗi từ |

**Chỉ dẫn:** đây là 2 giây quyết định người ta dừng hay lướt. Không logo, không giới thiệu. Chỉ một câu phủ định gây tò mò.

### Cảnh 2 · Lật (f90–180 · 0:03–0:06)

| | |
|---|---|
| **Nền** | `#171631` → nét cong hồng vẽ dần từ trái sang, gạch dưới chữ |
| **Trên màn hình** | `You just got` **`charged.`** — `charged.` màu `#FF8AD3`, cỡ lớn hơn 1,3× |
| **Chuyển động** | `You just got` vào nhanh (stagger 2f). `charged.` vào sau 10f, `bouncy`, kèm scale `0.8 → 1`. Nét cong vẽ trong 14f. |
| **Chuyển ra** | Mặt nạ tròn nở từ dấu chấm của `charged.` |
| **SFX** | whoosh khi nét cong chạy |

### Cảnh 3 · Thương hiệu (f180–240 · 0:06–0:08)

| | |
|---|---|
| **Nền** | `#FFFFFF` (đảo sáng — tạo nhịp) |
| **Trên màn hình** | Logo `HH` (ô bo tròn cobalt `#1609B7`, chữ trắng) + `Review Risk Agent` màu `#171631` |
| **Chuyển động** | Ô logo bật vào `bouncy` scale `0 → 1`; chữ trượt ra từ sau logo, stagger 3f |
| **Chuyển ra** | Khối tròn hồng tràn mép trượt từ phải sang, mang cảnh 4 |
| **SFX** | click |

**Chỉ dẫn:** logo xuất hiện **sớm, giây thứ 6**, đúng khung thể loại. Nhưng chỉ 2 giây — không phải phim giới thiệu công ty.

### Cảnh 4 · Cỡ dữ liệu (f240–330 · 0:08–0:11)

| | |
|---|---|
| **Nền** | `#FFF3FA` |
| **Trên màn hình** | Số **`2,339`** chạy từ 0 lên, màu `#D92A87`, cỡ 160px · dưới là `Google Play reviews` màu `#171631` cỡ 44px |
| **Chuyển động** | Số đếm trong 24f theo `ease-out` (nhanh đầu, chậm cuối). Chữ dưới vào ở f+18. |
| **Chuyển ra** | Số co nhỏ về góc trên-trái, giữ nguyên trên màn hình sang cảnh 5 |
| **SFX** | tiếng đếm lạch tạch nhỏ, dừng cùng lúc số dừng |

### Cảnh 5 · Bốn ví (f330–390 · 0:11–0:13)

| | |
|---|---|
| **Nền** | `#FFF3FA`, số `2,339` thu nhỏ còn ở góc |
| **Trên màn hình** | 4 thẻ bo tròn xếp 2×2: `MoMo` · `ZaloPay` · `ShopeePay` · `Viettel Money` |
| **Chuyển động** | Stagger 4f theo thứ tự trên-trái → dưới-phải, `bouncy`, scale `0.85 → 1` |
| **Chuyển ra** | 4 thẻ cùng trượt xuống dưới khung, lộ nền tối cảnh 6 |
| **SFX** | 4 tiếng pop lệch nhau |

### Cảnh 6 · Câu hỏi (f390–480 · 0:13–0:16)

| | |
|---|---|
| **Nền** | `#171631` |
| **Trên màn hình** | `Where does the money` **`actually go?`** — `actually go?` màu `#FF8AD3` |
| **Chuyển động** | Từng từ, stagger 3f. Sau khi đủ chữ, cả cụm nhích lên 20px rồi dừng (`bouncy`, tạo cảm giác hít thở). |
| **Chuyển ra** | Mặt nạ tròn đóng lại vào giữa, mở ra ở cảnh 7 |
| **SFX** | drone trầm nhỏ dâng lên |

### Cảnh 7 · Con số đinh (f480–630 · 0:16–0:21) ★

| | |
|---|---|
| **Nền** | `#0F0E24` — tối nhất cả video |
| **Trên màn hình** | **`49%`** cỡ 260px, màu `#F9E75D` ← **lần duy nhất dùng vàng** · dưới: `charged without agreeing to it` trắng 48px · dòng nhỏ `95% CI 44–54%` màu `#A9A5C4` 26px |
| **Chuyển động** | `49%` đếm 0→49 trong 20f rồi **nảy một nhịp** (`bouncy`). Thanh ngang dưới chạy đầy 49% trong 24f, màu `#F9E75D`. Dòng CI mờ hiện ở f+40, chậm, `smooth`. |
| **Chuyển ra** | Chữ `49%` co lại thành một chấm tròn vàng, chấm đó nở thành nút gửi của cảnh 8 (match cut) |
| **SFX** | một tiếng "thump" trầm đúng lúc số dừng |

**Chỉ dẫn:** đây là đỉnh của video, cảnh dài nhất (5 giây). Để con số đứng yên ít nhất 1,5 giây sau khi nảy xong. Dòng CI **không được bỏ** — nó nhỏ, không ai bắt buộc phải đọc, nhưng nó có mặt.

### Cảnh 8 · Sản phẩm chạy (f630–780 · 0:21–0:26)

| | |
|---|---|
| **Nền** | `#FFFFFF`, khối tròn hồng mờ sau thiết bị |
| **Trên màn hình** | Mockup laptop nghiêng isometric, trên màn là trang công cụ: ô nhập → câu trả lời hiện dần → dòng `3 tool calls` bung ra |
| **Chuyển động** | Camera trôi chậm sang phải 40px suốt cảnh (`smooth`, tuyến tính nhẹ). Bên trong màn: chữ trả lời hiện từng dòng stagger 4f; dòng `tool calls` trượt xuống ở f+70. |
| **Chuyển ra** | Khối tròn sau thiết bị phóng to thành nền cảnh 9 |
| **SFX** | tiếng gõ phím nhẹ, rồi một tiếng "ping" khi tool calls bung |

**Chỉ dẫn:** **quay màn hình thật**, đừng vẽ lại giao diện. Cả điểm mạnh của dự án là nó chạy được — dựng giả là tự bắn vào chân.

### Cảnh 9 · Truy được (f780–870 · 0:26–0:29)

| | |
|---|---|
| **Nền** | `#FF8AD3` (hồng đặc — cảnh duy nhất nền hồng) |
| **Trên màn hình** | `Every number opens the` **`review behind it.`** — chữ `#171631`, cụm nhấn gạch chân bằng nét cong trắng vẽ dần |
| **Chuyển động** | Chữ vào từng từ stagger 3f. Nét cong vẽ 12f sau khi chữ xong. |
| **Chuyển ra** | Mặt nạ tròn đóng về giữa |
| **SFX** | whoosh |

### Cảnh 10 · Điểm nhấn — nó biết nói không (f870–960 · 0:29–0:32) ★

| | |
|---|---|
| **Nền** | `#171631` |
| **Trên màn hình** | Dòng 1: `Ask what it can't answer.` trắng 72px · Dòng 2 (vào sau 14f): **`It says so.`** màu `#FF8AD3` 110px |
| **Chuyển động** | Dòng 1 vào bình thường. Dòng 2 vào `bouncy` mạnh hơn (damping 10), scale `0.7 → 1`. |
| **Chuyển ra** | Cả hai dòng trượt lên khỏi khung |
| **SFX** | một tiếng pop rõ ở `It says so.` |

**Chỉ dẫn:** đây là cảnh phân biệt dự án này với mọi demo chatbot khác. Nếu phải cắt video xuống 20 giây, cắt cảnh 4, 5, 9 — **giữ cảnh này**.

### Cảnh 11 · Kết (f960–1050 · 0:32–0:35)

| | |
|---|---|
| **Nền** | `#FFFFFF` |
| **Trên màn hình** | Logo `HH` + `Review Risk Agent` · dưới: nút bo tròn cobalt `#1609B7` chữ trắng `Open the tool` · dòng nhỏ `Runs on your own Claude account` màu `#5D5A73` 24px |
| **Chuyển động** | Logo bật vào `bouncy`; nút vào sau 6f; dòng nhỏ mờ hiện sau 12f. Giữ yên 40f cuối. |
| **SFX** | tiếng kết nhẹ |

**Chỉ dẫn:** dòng `Runs on your own Claude account` **bắt buộc có**. Thiếu nó, người xem bấm link, gặp màn đăng nhập và tưởng trang hỏng.

---

## 4 · Bản đồ chuyển cảnh

| Giữa | Kiểu | Khung |
|---|---|---|
| 1 → 2 | Match cut (chữ → chữ) | 8f |
| 2 → 3 | Mặt nạ tròn nở từ dấu chấm | 12f |
| 3 → 4 | Khối tròn trượt từ phải | 10f |
| 4 → 5 | Giữ phần tử (số thu nhỏ về góc) | 10f |
| 5 → 6 | Thẻ trượt xuống lộ nền | 10f |
| 6 → 7 | Mặt nạ tròn đóng rồi mở | 14f |
| 7 → 8 | Match cut (số → nút gửi) | 12f |
| 8 → 9 | Khối tròn phóng thành nền | 12f |
| 9 → 10 | Mặt nạ tròn đóng | 10f |
| 10 → 11 | Trượt lên | 8f |

**Nhịp nền nhạc:** cắt cảnh rơi vào phách. Ở 120 BPM, một phách = 15 khung. Mọi mốc chuyển cảnh ở trên đều là bội của 15 tính từ f0 — giữ nguyên để khớp nhạc.

---

## 5 · Âm thanh

- Nhạc nền: electronic / lo-fi vui, 120 BPM, không lời. Vào từ f0, hạ nhỏ ở cảnh 8 để nghe tiếng gõ phím, dâng lại ở cảnh 10.
- SFX theo bảng từng cảnh ở trên.
- **Xuất thêm một bản không nhạc nền**, chỉ sfx — LinkedIn phát tắt tiếng mặc định, và nhiều người thích bản không nhạc.
- **Phụ đề cứng cho mọi chữ thoại.** Thực ra video này đã toàn chữ trên màn hình nên không cần thoại — đó là lợi thế, giữ nguyên.

---

## 6 · Dựng bằng Remotion

```ts
// remotion.config.ts → Composition
<Composition
  id="ReviewRiskAgentPromo"
  component={Promo}
  durationInFrames={1050}
  fps={30}
  width={1080}
  height={1080}
/>
```

**Cấu trúc đề xuất**

```
src/
  Promo.tsx              // <Series> gồm 11 <Series.Sequence>
  scenes/S01Hook.tsx … S11End.tsx
  components/
    KineticLine.tsx      // nhận words[], màu nhấn, stagger -> hiện từng từ
    CountUp.tsx          // số chạy + nảy một nhịp khi dừng
    CircleMask.tsx       // chuyển cảnh mặt nạ tròn
    BlobBg.tsx           // khối tròn mờ tràn mép
    DrawStroke.tsx       // nét cong vẽ dần bằng strokeDasharray
  theme.ts               // toàn bộ hex ở mục 2, không hardcode rải rác
```

**Bốn chỗ dễ sai**

1. **Font phải nhúng bằng `staticFile()`**, dùng chính các `.woff2` trong `assets/fonts/`. Để Remotion tự lấy font hệ thống là mỗi máy render ra một kiểu chữ khác.
2. **Cảnh 8 là video thật**, nhúng bằng `<OffthreadVideo>`, không phải `<Video>` — `<Video>` hay rớt khung khi render.
3. **Mọi `spring()` phải nhận `fps` từ `useVideoConfig()`**, không hardcode 30. Đổi fps mà quên là toàn bộ nhịp lệch.
4. **Đừng dùng `interpolate` với `linear` cho chuyển động vào/ra.** Cả phong cách này sống nhờ nảy; một cảnh tuyến tính lộ ra ngay.

**Render**

```bash
npx remotion render ReviewRiskAgentPromo out/promo.mp4 --codec=h264 --crf=18
```

Xuất thêm bản 9:16 bằng cách đổi `height={1920}` và kiểm lại vùng an toàn — mọi chữ đã được đặt trong vùng giữa nên về lý thuyết không mất, nhưng **phải xem lại từng cảnh**, nhất là cảnh 5 (lưới 2×2) và cảnh 8 (mockup nghiêng).

---

## 7 · Nếu phải cắt ngắn

Bản 20 giây: bỏ cảnh **4, 5, 9**. Giữ 1, 2, 3, 6, 7, 8, 10, 11.

Lý do giữ cảnh 10 bằng mọi giá: ai cũng quay được một con bot trả lời đúng. Rất ít người quay cảnh nó **từ chối**.
