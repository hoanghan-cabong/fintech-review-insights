# Kịch bản video demo — Review Risk Agent

> Mục tiêu: **100 giây**. Người xem là nhà tuyển dụng, không phải đồng nghiệp kỹ thuật — họ bỏ đi ở giây thứ 90.
> Lời thoại tiếng Anh vì portfolio tiếng Anh. Chỉ dẫn quay tiếng Việt.
> Trang quay: `https://claude.ai/artifact/2JbYahDzxaLHCe26DkJZbX` → mục *Fintech & agentic AI* → **Open the tool**.

---

## Trước khi bấm ghi — 6 việc bắt buộc

Bốn việc đầu mà bỏ qua là hỏng take.

1. **Cấp quyền trước.** Mở trang, gõ một câu bất kỳ, bấm đồng ý khi Claude hỏi. Nếu không, hộp thoại xin quyền sẽ nhảy ra giữa lúc đang quay.
2. **Làm nóng dữ liệu.** Sau khi cấp quyền, bấm vào ô nhập một lần rồi đợi 2–3 giây. File dữ liệu 397 KB chỉ tải khi bạn chạm vào ô nhập — nếu không làm nóng, câu trả lời đầu tiên trong video sẽ đứng im chờ tải.
3. **Quay thử ít nhất một lần.** Câu trả lời của agent **không cố định** — mỗi lần hỏi ra một chữ khác. Nếu take nào agent trả lời dở, **quay lại** chứ đừng cắt ghép, vì cắt giữa đoạn streaming nhìn ra ngay.
4. **Chỉnh cửa sổ đủ rộng để 4 chip nằm một hàng.** Khoảng 1100px trở lên. Hẹp hơn thì chip rớt xuống hai hàng, nhìn rối.
5. Ẩn thanh bookmark, dùng cửa sổ trình duyệt sạch, không có tab lạ.
6. Chọn một chế độ sáng **hoặc** tối rồi giữ nguyên cả video.

---

## Bản A — có giọng đọc

### Nhịp 1 · Nói thẳng phát hiện (0:00 – 0:12)

**Hình:** mở sẵn ở phần số liệu, thấy dòng *"Half of all money-loss complaints are charges nobody agreed to."* và 4 ô số liệu.

> "Across two thousand three hundred Google Play reviews of four Vietnamese e-wallets, I found that nearly half the cases where someone loses money are not failed transactions. They are charges the user never agreed to. It happens at all four wallets."

**Chỉ dẫn:** đừng mở đầu bằng "Hi, I'm Han" hay giới thiệu dự án. Vào thẳng con số. Phần giới thiệu bản thân đã nằm trên portfolio rồi.

### Nhịp 2 · Agent chạy thật (0:12 – 0:45)

**Hình:** cuộn lên đầu trang. Bấm chip **"How do MoMo users most often lose money?"**

> "This is not a write-up. The agent is live on the page. It has three tools over the labelled data, and it has to call them before it states any number."

**Hình:** câu trả lời hiện dần. Khi xong, **bấm mở dòng "N tool calls"** để lộ tham số từng lần gọi.

> "Here is what it actually ran."

**Hình:** bấm vào một **mã review** trong câu trả lời, ví dụ `gp_momo_00123`. Review gốc mở ra.

> "And every number traces back to reviews you can open."

**Chỉ dẫn:** đoạn mở "tool calls" và bấm mã review là **phần quan trọng nhất của cả video**. Đừng vội. Để mỗi thứ nằm trên màn hình 2 giây rồi mới thao tác tiếp.

### Nhịp 3 · Hỏi câu nó không trả lời được (0:45 – 1:05)

**Hình:** bấm chip **"Which wallet has the most users?"**

> "I also put in a question the data cannot answer. Review text says nothing about user counts."

**Hình:** agent từ chối, nói thẳng là dữ liệu không cho biết điều đó.

> "It says so instead of inventing a number. That behaviour is specified in the prompt, and it is the part I care about most."

**Chỉ dẫn:** đây là 20 giây thuyết phục nhất trong video đối với vai trò AI product. Nếu agent lỡ bịa ra con số, **đừng quay tiếp** — đó là lỗi cần sửa prompt, không phải lỗi quay.

### Nhịp 4 · Quyết định sản phẩm (1:05 – 1:35)

**Hình:** cuộn xuống khối **"The product decision"**.

> "A finding is not a decision. If half the money-loss cases are charges nobody agreed to, the fix is not better error handling — it is consent and visibility around automatic payments. So I wrote the PRD."

**Hình:** dừng ở ô viền đỏ **"What would stop it"**.

> "With the part that would stop it: the extra confirmation adds friction to paying, so payment success is a guardrail, agreed before the test. And step zero is checking this against internal tickets. Public reviews are a signal, not proof."

### Kết (1:35 – 1:40)

**Hình:** về đầu trang công cụ, con trỏ ở ô nhập.

> "Everything here runs in the browser. Link in the description."

---

## Bản B — không giọng đọc, chỉ phụ đề

Cùng 4 nhịp, cùng thao tác, thay lời thoại bằng chữ chèn trên màn hình. An toàn hơn và quay nhanh hơn.

| Nhịp | Chữ trên màn hình | Giây |
|---|---|---|
| 1 | **49% of money-loss complaints are charges nobody agreed to** · 2,339 reviews · 4 wallets · 90 days | 0:00–0:10 |
| 2 | The agent is live. It must call a tool before stating any number. | 0:10–0:22 |
| 2 | ↓ what it actually ran | 0:22–0:32 |
| 2 | Every number opens the reviews behind it | 0:32–0:45 |
| 3 | Now a question the data **cannot** answer | 0:45–0:55 |
| 3 | It refuses instead of inventing one | 0:55–1:05 |
| 4 | A finding is not a decision → the PRD | 1:05–1:18 |
| 4 | …including what would stop it | 1:18–1:35 |

**Chỉ dẫn:** mỗi dòng chữ ở trên màn hình ít nhất 2,5 giây. Chữ ngắn, một ý một dòng.

---

## Hai điều không được nói

**1. Đừng nói "the agent caught 7 out of 7".** Đúng về số nhưng nghe như một tuyên bố chắc chắn, trong khi tập kiểm tra chỉ có **7 ca S1**, khoảng tin cậy 65–100%. Nói thế là tự đưa cổ vào chỗ người phỏng vấn sẽ chém.

Nếu muốn nhắc tới chuyện đánh giá, nói đúng mức — một câu, chèn vào cuối nhịp 2:

> "I checked it against a keyword filter on a test set I labelled before the model ran. The agent found money-loss cases the filter missed. The page says how small that test set is."

**2. Đừng nói "AI-powered" hay "cutting-edge".** Cả video không cần một tính từ marketing nào. Thứ thuyết phục là nó chạy được trước mắt người xem.

---

## Sau khi quay

- Cắt đầu đuôi, **không** chèn nhạc nền, **không** hiệu ứng chuyển cảnh.
- Xuất 1080p. Nếu đăng LinkedIn thì thêm phụ đề cứng — phần lớn người xem tắt tiếng.
- Đổi tên file thành `review-risk-agent-demo.mp4`.
- Nhớ: người xem phải **đăng nhập Claude** mới dùng được agent. Trong phần mô tả nên ghi một dòng, không thì họ bấm link rồi tưởng trang hỏng.
