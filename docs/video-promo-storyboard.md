# Video promo 35 giây — Review Risk Agent · v2

> Dựng bằng **Remotion**. Đủ chi tiết để đưa thẳng cho người dựng hoặc cho Claude Code.
> Phong cách: motion graphics, kinetic typography, mỗi cảnh một ý, chuyển cảnh liền mạch.
> Video đi kèm, khác nhiệm vụ: [docs/video-script.md](video-script.md) (demo 100 giây, gánh phần chứng minh).

**v2 sửa gì so với v1** (rà soát ngày 16/11/2026):
con số 49% có mẫu số trên cùng màn hình · thêm nhịp quyết định sản phẩm (PRD) · hook không còn nói với "You" · cảnh sản phẩm cắt cận để đọc được trên điện thoại · cảnh kết có tên người làm, bỏ nút giả · gộp hai cảnh dựng bối cảnh · bỏ câu "every number opens a review" vì nói quá · mọi chữ chính ≤ 5 từ (kiểm bằng script) · bản ngắn tính lại đúng 20 giây.

---

## 1 · Brief

| | |
|---|---|
| **Nhiệm vụ** | Mồi câu. Giữ người xem 35 giây rồi đẩy họ sang trang công cụ. |
| **Không phải nhiệm vụ** | Chứng minh phương pháp — việc của video demo 100 giây và của chính trang web. |
| **Người xem** | Nhà tuyển dụng / hiring manager lướt LinkedIn, **tắt tiếng**, quyết định dừng hay lướt trong 2 giây đầu. Họ **không phải** người bị trừ tiền — nên video không xưng "You". |
| **Độ dài** | 35 giây · 1.050 khung @ 30fps · bản ngắn 20 giây · 600 khung |
| **Khung hình** | 1080×1080. Mọi chữ nằm trong vùng giữa 1080×960 để cắt 9:16 không mất chữ. |
| **Đăng ở** | LinkedIn, cạnh trang công cụ trên portfolio |

**Hai câu phải đọng lại:**
1. *Gần một nửa số khiếu nại mất tiền trong ví điện tử không phải bị hack hay giao dịch lỗi — mà là bị trừ tiền khi người dùng không đồng ý.*
2. *Người làm ra nó không dừng ở phát hiện — họ viết PRD từ đó.*

Câu thứ hai là thứ biến video từ "tôi làm được con bot" thành "tôi ra quyết định sản phẩm từ dữ liệu".

### Ràng buộc trung thực

Video ngắn nên rất dễ nói quá. Năm luật, không ngoại lệ:

1. **49% luôn đi cùng mẫu số** *of money-loss complaints* trên **cùng một màn hình**, kèm dòng `95% CI 44–54%`. Thiếu mẫu số, người xem đọc thành "49% người dùng bị trừ tiền" — sai.
2. **Không nói "every number cites a review".** Đúng là: agent không được nêu con số nào mà chưa gọi tool, và trích dẫn review khi đưa ví dụ. Video dùng *"Shows its working."* — đúng và vẫn gọn.
3. **Cảnh 7–9 là bản ghi màn hình thật**, không vẽ lại giao diện. Nếu tua nhanh đoạn chờ thì ghi rõ `sped up 3×` ở góc.
4. **Không** "7 out of 7", "AI-powered", "cutting-edge", hay bất kỳ tuyên bố độ chính xác nào. Tập kiểm tra chỉ có 7 ca S1.
5. Mọi con số truy được về `reports/key_findings.json` hoặc `data/corpus/run_meta.json`.

---

## 2 · Hệ thiết kế

### Màu — lấy thẳng từ `assets/site.css`

| Vai trò | Hex | Dùng ở đâu |
|---|---|---|
| Nền tối | `#171631` | cảnh 1–3, 10 |
| Nền tối sâu | `#0F0E24` | chỉ cảnh 4 (con số) |
| Nền sáng | `#FFFFFF` | cảnh 5, 7–9, 11 |
| Nền hồng nhạt | `#FFF3FA` | cảnh 6 |
| **Hồng thương hiệu** | `#FF8AD3` | nhấn trên nền tối, nhãn, thẻ |
| Hồng đậm | `#D92A87` | nhấn trên nền sáng |
| **Vàng** | `#F9E75D` | **chỉ cảnh 4** — đúng một lần trong cả video |
| Cobalt | `#1609B7` | ô logo, tên ở cảnh kết |
| Chữ trên nền tối | `#FFFFFF` | |
| Chữ phụ trên nền tối | `#A9A5C4` | CI, dòng chặn |
| Chữ phụ trên nền sáng | `#5D5A73` | |

> **Luật màu:** mỗi cảnh tối đa **2 màu nhấn**. Vàng xuất hiện **một lần** — dùng nhiều là mất tác dụng.

### Chữ

- **Be Vietnam Pro** 600/500/400 — `assets/fonts/be-vietnam-pro-latin-*.woff2`. Font đang dùng trên portfolio, dáng sans tròn hiện đại.
- **Fraunces** — `assets/fonts/fraunces-latin-opsz-normal.woff2` — **chỉ** cho tên "Hoang Han" ở cảnh kết, giống cách site dùng serif cho tiêu đề lớn.
- **Chữ chính ≤ 5 từ một màn hình. Chữ phụ ≤ 6 từ.** Quá là tách cảnh. Nhãn ví (MoMo, ZaloPay…) và chip không tính.
- Cỡ chữ chính **96–150px** trên khung 1080 → khoảng 35–55px trên điện thoại. Chữ phụ không nhỏ hơn **24px**.
- Chữ hiện **theo từng từ**, lệch nhau 3 khung (100ms). Tên ở cảnh kết hiện **theo từng chữ cái**, lệch 1 khung.

### Chuyển động — thông số Remotion

```ts
const bouncy = { damping: 12,  stiffness: 180, mass: 0.8 }; // chữ, số, thẻ vào khung
const punchy = { damping: 10,  stiffness: 200, mass: 0.8 }; // từ được nhấn mạnh nhất cảnh
const smooth = { damping: 200, stiffness: 100, mass: 1   }; // nền, mặt nạ, zoom

const t = spring({ frame: frame - delay, fps, config: bouncy });
```

| Quy tắc | Giá trị |
|---|---|
| Stagger giữa phần tử anh em | **3 khung** (thẻ lớn: 6 khung) |
| Chữ vào | `translateY 40→0` + `opacity 0→1` + `scale .92→1` |
| Overshoot | để spring tự tạo, **không** viết keyframe vượt đích |
| Không bao giờ | `linear` cho chuyển động vào/ra |

### Hình khối nền

- Khối tròn 600–900px tràn mép, `blur(40px)`, `opacity .35`, màu `#FF8AD3`.
- Nét cong vẽ dần (`strokeDasharray`), nét 8px, đầu tròn, màu `#FF8AD3`. Dùng ở cảnh 3 và cảnh 9.
- Icon phẳng. Không ảnh chụp.

---

## 3 · Storyboard — 11 cảnh

> `f` = khung @30fps. Mỗi mốc là bội của 15 → rơi đúng phách ở 120 BPM.
> Cảnh 7, 8, 9 dùng **một** bản ghi màn hình liền mạch (xem mục 6).

### Cảnh 1 · Mồi (f0–45 · 0:00–0:01.5)

| | |
|---|---|
| **Nền** | `#171631`, khối tròn hồng mờ tràn góc dưới-phải |
| **Chữ chính** | `Not hacked.` |
| **Chữ phụ** | — |
| **Màu / cỡ** | trắng 140px, giữa khung |
| **Chuyển động** | hai từ, stagger 4f, `bouncy` |
| **Chuyển ra** | đẩy dọc — chữ trượt lên khỏi khung, cảnh 2 vào từ dưới (8f) |
| **SFX** | pop nhẹ mỗi từ |

**Chỉ dẫn:** không logo, không giới thiệu. Một phủ định ngắn, để người xem tự hỏi "vậy là gì?".

### Cảnh 2 · Phủ định thứ hai (f45–105 · 0:01.5–0:03.5)

| | |
|---|---|
| **Nền** | `#171631` |
| **Chữ chính** | `Not a failed payment.` |
| **Chữ phụ** | — |
| **Màu / cỡ** | trắng 110px |
| **Chuyển động** | stagger 3f, `bouncy` |
| **Chuyển ra** | đẩy dọc (8f) |
| **SFX** | pop nhẹ |

**Chỉ dẫn:** hai phủ định liên tiếp loại đi hai cách giải thích mà ai cũng nghĩ tới đầu tiên. Nhịp phải nhanh — 2 giây, không hơn.

### Cảnh 3 · Lật (f105–165 · 0:03.5–0:05.5)

| | |
|---|---|
| **Nền** | `#171631`, nét cong hồng vẽ dần gạch dưới chữ |
| **Chữ chính** | `Charged` · `without agreeing.` |
| **Chữ phụ** | — |
| **Màu / cỡ** | `Charged` hồng `#FF8AD3` 150px dòng 1 · `without agreeing.` trắng 90px dòng 2 |
| **Chuyển động** | `Charged` vào `punchy`, scale `.7→1`. Dòng 2 vào sau 8f. Nét cong vẽ trong 14f. |
| **Chuyển ra** | **match cut** — cả cụm co lại, bay lên đỉnh khung, thành nhãn của cảnh 4 |
| **SFX** | pop mạnh ở `Charged` + whoosh khi nét cong chạy |

### Cảnh 4 · Con số đinh ★ (f165–315 · 0:05.5–0:10.5)

| | |
|---|---|
| **Nền** | `#171631` → `#0F0E24` (`smooth`, 15f) |
| **Chữ chính** | `49%` · `of money-loss complaints` |
| **Chữ phụ** | `Charged without agreeing` · `95% CI 44–54%` |
| **Bố cục** | trên cùng: nhãn `Charged without agreeing` (mang từ cảnh 3), hồng 40px · giữa: **`49%`** vàng `#F9E75D` 260px · dưới: `of money-loss complaints` trắng 52px · đáy: `95% CI 44–54%` `#A9A5C4` 34px, cách thanh ngang ~70px (26px chỉ còn ~9px khi thu về 390px, không đọc được) · một thanh ngang chạy đầy tới 49%, vàng |
| **Chuyển động** | số đếm 0→49 trong 20f (ease-out) rồi nảy một nhịp `punchy`. `of money-loss complaints` và CI vào **cùng lúc số bắt đầu đếm** (f+0, `smooth`, xong trong ~8f), để **không khung nào có `49%` đứng một mình** (ràng buộc 1). Sự chú ý vẫn dồn vào số vì chỉ số chuyển động. Giữ yên **ít nhất 45f** sau khi mọi thứ đã vào. |
| **Chuyển ra** | mặt nạ tròn đóng về tâm số `49%`, mở ra nền trắng cảnh 5 (12f) |
| **SFX** | một tiếng "thump" trầm đúng lúc số dừng |

**Chỉ dẫn:** đỉnh của video, đặt ở **giây thứ 5,5** — ngay sau hook, trước cả logo. Đọc liền ba dòng sẽ ra: *Charged without agreeing — 49% of money-loss complaints.* Mẫu số và CI **không được bỏ** (ràng buộc 1).

### Cảnh 5 · Ai làm, làm gì (f315–375 · 0:10.5–0:12.5)

| | |
|---|---|
| **Nền** | `#FFFFFF` (đảo sáng — tạo nhịp) |
| **Chữ chính** | `Review Risk Agent` |
| **Chữ phụ** | `by Hoang Han` |
| **Bố cục** | ô bo tròn cobalt `#1609B7` chữ `HH` trắng · bên phải: `Review Risk Agent` `#171631` 72px · dưới: `by Hoang Han` `#5D5A73` 36px |
| **Chuyển động** | ô bật vào `bouncy` scale `0→1`; tên công cụ trượt ra từ sau ô, stagger 3f; `by Hoang Han` vào sau 8f |
| **Chuyển ra** | khối tròn hồng tràn mép trượt từ phải, mang cảnh 6 (10f) |
| **SFX** | click |

**Chỉ dẫn:** cố ý **không** để logo ở giây thứ 5 như quy ước của thể loại. Trên LinkedIn, 3 giây đầu quyết định dừng hay lướt, và logo của một case chưa ai biết thì không giữ chân ai — con số thì có. Dòng `by Hoang Han` bắt buộc: đây là portfolio, người xem cần biết công cụ của ai.

### Cảnh 6 · Cỡ dữ liệu (f375–450 · 0:12.5–0:15)

| | |
|---|---|
| **Nền** | `#FFF3FA` |
| **Chữ chính** | `2,339 reviews` |
| **Chữ phụ** | `Google Play · 90 days` |
| **Bố cục** | `2,339` hồng đậm `#D92A87` 140px + `reviews` `#171631` 56px · dưới: một hàng 4 chip bo tròn `MoMo` `ZaloPay` `ShopeePay` `Viettel Money` · đáy: chữ phụ `#5D5A73` 28px |
| **Chuyển động** | số đếm trong 18f (ease-out). Chip bắt đầu vào khi số đếm được nửa (f+9), stagger 3f, `bouncy`, scale `.85→1` |
| **Chuyển ra** | chip trượt xuống; khung ghi hình của cảnh 7 trồi lên từ dưới (12f) |
| **SFX** | tiếng đếm lạch tạch nhỏ, dừng cùng lúc số dừng · 4 tiếng pop theo chip |

**Chỉ dẫn:** v1 tốn 5 giây cho hai cảnh này; giờ gộp còn 2,5 giây. Nó chỉ trả lời "dữ liệu ở đâu ra" — không đáng hơn thế.

### Cảnh 7 · Chạy thật (f450–600 · 0:15–0:20)

| | |
|---|---|
| **Nền** | `#FFFFFF`, khối tròn hồng mờ phía sau khung ghi hình |
| **Chữ chính** | `Live. Not a mockup.` |
| **Chữ phụ** | `sped up 3×` *(chỉ khi có tua)* |
| **Bố cục** | khung ghi hình bo 22px, **rộng 1040px**, bóng nhẹ, gần tràn khung. Bên trong: bản ghi thật — bấm chip *"How do MoMo users most often lose money?"* → câu trả lời hiện dần. Nhãn `Live. Not a mockup.` là một viên thuốc hồng `#FF8AD3`, chữ `#171631` 34px, góc trên-trái khung ghi hình |
| **Chuyển động** | khung trồi lên `bouncy`. **Không cho camera trôi** — chữ trong bản ghi phải đứng yên để đọc được. Nhãn vào ở f+12. |
| **Tua** | đoạn chờ agent trả lời thường dài 8–15 giây; nén vào cảnh bằng `playbackRate` tối đa 3×. Khi đang tua thì hiện `sped up 3×` 24px `#5D5A73` ở góc dưới-phải |
| **Chuyển ra** | zoom liền vào vùng dòng "N tool calls" (`scale 1→1.35`, `smooth`, 15f) — chảy thẳng sang cảnh 8, không cắt |
| **SFX** | gõ phím nhẹ · "ping" khi câu trả lời xong · nhạc nền hạ xuống −8dB từ cảnh này đến hết cảnh 9 |

**Chỉ dẫn:** v1 đặt bản ghi trong laptop nghiêng isometric — đẹp trên màn hình lớn nhưng **trên điện thoại chữ chỉ còn khoảng 3–4px**. Giờ khung ghi hình gần tràn khung và không nghiêng. Cách tính độ đọc được ở mục 6.

### Cảnh 8 · Cho xem cách nó làm (f600–675 · 0:20–0:22.5)

| | |
|---|---|
| **Nền** | tiếp bản ghi, đang zoom 1.35× |
| **Chữ chính** | `Shows its working.` |
| **Chữ phụ** | — |
| **Bố cục** | dải hồng `#FF8AD3` cao 120px trượt xuống từ đỉnh khung, chữ `#171631` 64px · bên dưới, trong bản ghi: dòng "3 tool calls" bung ra, rồi bấm một mã review → review gốc mở |
| **Chuyển động** | dải trượt xuống `smooth` 10f; chữ stagger 3f |
| **Chuyển ra** | zoom ra về 1× (`smooth`, 12f); dải trượt lên — chảy sang cảnh 9 |
| **SFX** | click khi bấm mã review |

**Chỉ dẫn:** v1 viết *"Every number opens the review behind it"* — vừa quá 5 từ, vừa nói quá (xem ràng buộc 2). *"Shows its working"* đúng với cả hai thứ đang hiện trên màn hình: danh sách tool đã gọi và review được trích.

### Cảnh 9 · Nó biết nói không ★ (f675–780 · 0:22.5–0:26)

| | |
|---|---|
| **Nền** | tiếp bản ghi |
| **Chữ chính** | `Ask what it can't answer.` · `It says so.` |
| **Chữ phụ** | — |
| **Bố cục** | **f0–45:** bản ghi rõ nét — bấm chip *"Which wallet has the most users?"*, agent trả lời rằng review không cho biết số người dùng; một nét cong hồng vẽ gạch dưới câu từ chối trong bản ghi. Dòng `Ask what it can't answer.` trắng 56px trên dải tối `#171631` ở đáy khung. **f45–105:** bản ghi tối đi còn 40%, `It says so.` hồng `#FF8AD3` 130px giữa khung |
| **Chuyển động** | dòng 1 vào stagger 3f. `It says so.` vào `punchy`, scale `.7→1` |
| **Chuyển ra** | mặt nạ tròn nở từ dấu chấm của `so.` → nền tối cảnh 10 (12f) |
| **SFX** | pop rõ ở `It says so.` |

**Chỉ dẫn:** 1,5 giây đầu phải để người xem **thấy câu từ chối thật** trong bản ghi trước khi chữ lớn che lên. Nếu chữ lớn vào ngay, cảnh này chỉ còn là lời tự khen.

### Cảnh 10 · Quyết định sản phẩm ★ (f780–930 · 0:26–0:31)

| | |
|---|---|
| **Nền** | `#171631` |
| **Chữ chính** | `So I wrote the PRD.` |
| **Chữ phụ** | `Guardrail: payment success can't drop` |
| **Bố cục** | câu chính trắng 96px, chữ `PRD` hồng `#FF8AD3` · sau 30f câu lùi lên nửa trên (`smooth`), 3 thẻ bo tròn xếp dọc vào lần lượt: `Warn before charging` · `One autopay screen` · `Confirm first charges` — thẻ viền hồng 2px, nền trong suốt, chữ trắng 44px · dòng chặn `#A9A5C4` 28px ở đáy, vào ở f+90 |
| **Chuyển động** | câu chính stagger 3f `bouncy` · thẻ stagger **6f**, `bouncy`, trượt từ phải `60→0` · dòng chặn `smooth` |
| **Chuyển ra** | quét dọc nền tối → trắng (10f) |
| **SFX** | 3 tiếng pop theo thẻ |

**Chỉ dẫn:** nhịp mà v1 thiếu hẳn. Chọn **3 trong 4** tính năng của PRD theo cỡ vấn đề mà nó xử lý: gói tự gia hạn (~79/217 ca) → *warn before charging*; trừ từ ngân hàng liên kết không OTP (~49) → *confirm first charges*; không thấy toàn cảnh → *one autopay screen*. Bỏ *nothing pre-ticked* vì chỉ ~9 ca. Dòng chặn ngắn nhưng nói được điều PM nào cũng bị hỏi: tính năng này có thể làm hại cái gì.

### Cảnh 11 · Kết (f930–1050 · 0:31–0:35)

| | |
|---|---|
| **Nền** | `#FFFFFF` |
| **Chữ chính** | `Hoang Han` · `Link in the post` |
| **Chữ phụ** | `Runs on your own Claude account` |
| **Bố cục** | `Hoang Han` **Fraunces** 120px cobalt `#1609B7` · dưới: `Link in the post` `#171631` 44px · đáy: chữ phụ `#5D5A73` 24px |
| **Chuyển động** | tên hiện **từng chữ cái**, stagger 1f, `bouncy` · dòng 2 vào sau 10f · chữ phụ mờ hiện sau 20f · giữ yên **45f** cuối |
| **SFX** | tiếng kết nhẹ |

**Chỉ dẫn:** v1 có nút `Open the tool` — trong video không bấm được, và không có tên người làm. Giờ tên là thứ to nhất. Dòng `Runs on your own Claude account` bắt buộc — thiếu nó người xem bấm link, gặp màn đăng nhập và tưởng trang hỏng.

---

## 4 · Bản đồ chuyển cảnh

| Giữa | Kiểu | Khung |
|---|---|---|
| 1 → 2 | Đẩy dọc | 8 |
| 2 → 3 | Đẩy dọc | 8 |
| 3 → 4 | **Match cut** — cụm chữ bay lên thành nhãn | 12 |
| 4 → 5 | Mặt nạ tròn đóng về `49%` rồi mở | 12 |
| 5 → 6 | Khối tròn trượt từ phải | 10 |
| 6 → 7 | Chip trượt xuống, khung ghi hình trồi lên | 12 |
| 7 → 8 | **Zoom liền** vào tool calls | 15 |
| 8 → 9 | **Zoom liền** ra | 12 |
| 9 → 10 | Mặt nạ tròn nở từ `so.` | 12 |
| 10 → 11 | Quét dọc tối → trắng | 10 |

Ba cảnh 7–8–9 là **một bản ghi liền**, nối bằng zoom — người xem cảm thấy đang nhìn một phiên dùng thật chứ không phải ba clip ghép.

---

## 5 · Âm thanh

- Nhạc nền electronic / lo-fi vui, **120 BPM** (một phách = 15 khung), không lời. Vào từ f0, hạ −8dB ở cảnh 7–9 để nghe tiếng thao tác, dâng lại ở cảnh 10.
- SFX theo bảng từng cảnh.
- **Xuất thêm một bản không nhạc nền**, chỉ sfx. LinkedIn phát tắt tiếng mặc định — video này toàn chữ trên màn hình nên tắt tiếng vẫn hiểu đủ; đó là chủ đích.

---

## 6 · Quay bản ghi cho cảnh 7–9

Một take liền, chừng 40–60 giây thật, sau đó nén vào 11 giây.

### Trước khi bấm ghi

1. **Cấp quyền Claude trước.** Gõ thử một câu, bấm đồng ý. Không thì hộp thoại xin quyền nhảy ra giữa take.
2. **Làm nóng dữ liệu:** bấm vào ô nhập, đợi 2–3 giây. File 397 KB chỉ tải ở lần chạm đầu.
3. **Cửa sổ trình duyệt rộng đúng 600px CSS**, màn hình Retina (DPR 2), zoom 100%, chế độ sáng, ẩn thanh bookmark.

### Vì sao là 600px — phép tính độ đọc được

| Bước | Hệ số |
|---|---|
| Trang rộng 600px CSS lấp khung ghi hình rộng 1040px | ×1,73 |
| Chữ thân trang 17px → trong khung video | ≈ 29px |
| LinkedIn trên điện thoại hiện video vuông rộng ~390px | ×0,36 |
| **Chữ thân trang trên điện thoại** | **≈ 10–11px — đọc được** |

So với v1 (laptop nghiêng): ≈ 3–4px. Ghi ở DPR 2 để khi phóng 1,73× vẫn nét. **Nếu quay ở cửa sổ rộng hơn 630px thì chữ rơi xuống dưới 10px** — đừng.

### Thao tác trong take, theo thứ tự

1. Bấm chip *"How do MoMo users most often lose money?"*
2. Đợi câu trả lời chạy **hết**.
3. Bấm dòng **"N tool calls"** cho bung ra. Dừng 2 giây.
4. Bấm **một mã review** trong câu trả lời. Review gốc mở ra. Dừng 2 giây.
5. Bấm chip *"Which wallet has the most users?"*
6. Đợi câu trả lời chạy hết. Dừng 3 giây.

Quay **ít nhất 3 take**. Câu trả lời mỗi lần một khác. Chọn take mà ở bước 6 agent **từ chối rõ ràng**. Nếu take nào agent bịa ra số người dùng — đừng dùng, và báo lại: đó là lỗi prompt cần sửa, không phải lỗi quay.

---

## 7 · Dựng bằng Remotion

```tsx
<Composition id="ReviewRiskAgentPromo" component={Promo}
  durationInFrames={1050} fps={30} width={1080} height={1080} />
<Composition id="ReviewRiskAgentPromo20" component={PromoShort}
  durationInFrames={600}  fps={30} width={1080} height={1080} />
```

```
src/
  Promo.tsx · PromoShort.tsx   // <Series> các cảnh
  scenes/S01NotHacked.tsx … S11End.tsx
  components/
    KineticLine.tsx   // words[], màu nhấn theo từ, stagger
    CountUp.tsx       // số chạy + nảy một nhịp khi dừng
    CircleMask.tsx    // chuyển cảnh mặt nạ tròn
    BlobBg.tsx        // khối tròn mờ tràn mép
    DrawStroke.tsx    // nét cong vẽ dần
    ScreenCard.tsx    // khung ghi hình bo góc + OffthreadVideo + zoom
    Pill.tsx          // nhãn viên thuốc
  theme.ts            // toàn bộ hex và spring config ở mục 2
public/
  take.mp4            // MỘT bản ghi cho cảnh 7–9
  fonts/              // chép từ assets/fonts/ của portfolio
```

**Năm chỗ dễ sai**

1. **Font nhúng bằng `staticFile()`** từ `public/fonts/`. Để Remotion lấy font hệ thống là mỗi máy render ra một kiểu chữ.
2. **Bản ghi dùng `<OffthreadVideo>`**, không phải `<Video>` — `<Video>` hay rớt khung khi render.
3. **Cảnh 7–9 cắt từ cùng một `take.mp4`** bằng `startFrom` (tính theo khung của file nguồn) và `playbackRate`. Đừng xuất ba clip riêng — mất tính liền mạch của zoom.
4. **Mọi `spring()` lấy `fps` từ `useVideoConfig()`**, không hardcode 30.
5. **Không dùng `linear`** cho chuyển động vào/ra. Phong cách này sống nhờ độ nảy.

**Render**

```bash
npx remotion render ReviewRiskAgentPromo out/promo-35s.mp4 --codec=h264 --crf=18
```

```bash
npx remotion render ReviewRiskAgentPromo20 out/promo-20s.mp4 --codec=h264 --crf=18
```

Bản 9:16: đổi `height={1920}` rồi **xem lại từng cảnh** — nhất là cảnh 6 (hàng chip) và cảnh 7–9 (khung ghi hình).

---

## 8 · Bản ngắn — đúng 20 giây

Giữ cảnh **1, 3, 4, 9, 10, 11** (cảnh 11 rút còn 3 giây):

| Cảnh | Giây | Khung |
|---|---|---|
| 1 · Not hacked. | 1,5 | 45 |
| 3 · Charged without agreeing. | 2 | 60 |
| 4 · 49% | 5 | 150 |
| 9 · It says so. | 3,5 | 105 |
| 10 · So I wrote the PRD. | 5 | 150 |
| 11 · Hoang Han (rút gọn) | 3 | 90 |
| **Tổng** | **20** | **600** |

Bỏ gì và vì sao:
- **Cảnh 2** — hook vẫn chạy với hai nhịp *Not hacked → Charged*.
- **Cảnh 5, 6** — tên đã có ở cảnh kết; cỡ dữ liệu là chi tiết, không phải câu chuyện.
- **Cảnh 7, 8** — cảnh 9 vẫn là bản ghi thật nên video ngắn vẫn chứng minh được nó chạy.

**Không bao giờ cắt cảnh 9 và 10.** Ai cũng quay được con bot trả lời đúng; rất ít người quay cảnh nó **từ chối**, và càng ít người đi tiếp tới **quyết định sản phẩm**.
