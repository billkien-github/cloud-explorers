# Nội dung

**Công thức lõi:** Phiêu lưu + Hài hước + Khoa học đơn giản + Nhân vật và bảo bối dễ nhớ. Trẻ em nhớ nhân vật qua **công năng và đạo cụ**, không chỉ qua ngoại hình.

**Cơ chế hài "Chain Reaction"** (lấy cảm hứng từ cơ chế, không sao chép, chú sóc Scrat trong *Ice Age*):
> Mong muốn nhỏ → hành động theo tính cách → hậu quả không ngờ → leo thang → twist bất ngờ nhưng hợp lý.

Chính nhân vật **can thiệp và làm lệch** câu chuyện cổ tích hay phát minh, chứ không chỉ đứng xem.

## Series

5 series nối với nhau qua **Story Portal** (cổng du hành) đặt tại căn cứ **Wonder Hub**:

| Series | Nội dung | Tỷ trọng |
|---|---|---|
| Fairy Tale Adventures | Cổ tích quen thuộc (Jack & cây đậu, Ba chú heo…) | 30% |
| The Invention Lab | Phát minh: bánh xe, kính thiên văn, máy bay… | 25% |
| 1001 Magical Nights | Thảm bay, đèn thần, kho báu phương Đông | 15% |
| Journey Through Time | Khủng long, kỷ băng hà, nền văn minh cổ | 15% |
| What If? | Giả tưởng: không có trọng lực, đồ vật biết nói… | 15% |

3 tháng đầu chỉ làm 3 series đầu.

## Khung một tập (6–8 phút, độ dài theo nội dung)

Nội dung hấp dẫn và nhịp nhanh quan trọng hơn con số. Tỉ lệ dưới đây là mốc kết thúc gợi ý của từng nhịp.

| Nhịp | Kết thúc ở khoảng | Việc của nhịp |
|---|---|---|
| Hook | 0:15 | Một gag hoặc hình ảnh giữ người xem lại, có gag trong 10 giây đầu, tên phim trước giây 30 |
| Discovery | 12% | Vấn đề xuất hiện, nhân vật muốn gì. Mục tiêu phải rõ trong phút đầu |
| Gadget Action | 40% | Bảo bối vào cuộc, giới hạn của nó lộ ra |
| **Comedy Twist** | 75% | Chain Reaction: hậu quả không ngờ, leo thang. Sự cố lớn đến trước nửa tập |
| Science Moment | 90% | Một ý khoa học đơn giản, gắn vào việc giải quyết chứ không đứng riêng |
| Resolution | hết | Giải quyết, twist cuối, kết. Ngắn, một đoạn kết duy nhất |

## Nhịp cho trẻ em

1. Khoảng **15–20 giây** lại có một gag hoặc một chuyển động lớn. Mỗi cảnh chỉ một mục tiêu.
2. Tối đa **một bí ẩn** cùng lúc.
3. Gag lặp theo **luật bộ ba** (lần 1 gài, lần 2 lặp, lần 3 lật ngược). Có một câu cả nhóm hô được để trẻ nhớ và hô theo.
4. Mọi thứ dùng để giải quyết phải được **gài trước**.
5. Lời giải là **một kế hoạch rõ** mà trẻ đoán theo được (đếm, làm theo bước), mỗi bảo bối góp phần theo đúng giới hạn của nó.
6. **Bài học thể hiện bằng hành động**, chỉ nói thành lời một câu ngắn.
7. Nguy hiểm thì kỳ ảo, có cứu giúp kịp thời, không làm trẻ sợ.

**Luật đạo cụ:** nhìn là nhận ra, công dụng rõ, **có giới hạn** (quan trọng nhất), hiệu ứng dễ nhớ, sinh ra được nhiều tình huống. Đạo cụ không được giải quyết mọi việc ngay lập tức.

## Viết một tập

| Bước | File trong `Scripts/` | Nội dung |
|---|---|---|
| 1. Beat sheet | `EPxxx_<tên>.md` | Logline (1–2 câu) + bảng nhịp theo khung tập, có thời gian |
| 2. Kịch bản | `EPxxx_<tên>.fountain` | Kịch bản đầy đủ, bắt đầu từ [`Scripts/template.fountain`](Scripts/template.fountain) |
| 3. Storyboard | `Storyboards/EPxxx/` | Khung hình từng cảnh |
| 4. Animatic | `Animatics/EPxxx/` | Storyboard có thời gian và tiếng tạm. Độ dài thật của tập đo ở bước này |

Chỉ dựng hàng loạt shot ở `04_PRODUCTION/` khi animatic đã chốt. Trước đó chỉ dựng thử vài shot để kiểm tra pipeline; số shot sẽ đánh lại theo storyboard.

**Kịch bản viết bằng [Fountain](https://fountain.io):** format kịch bản chuẩn (screenplay) dạng chữ thường. Xem thay đổi được trong git, xuất PDF đúng format bằng Highland, Fade In hoặc extension "Better Fountain" của VS Code.

| Thành phần | Cách viết |
|---|---|
| Nhịp của khung tập | `# HOOK`, `# DISCOVERY`… Dòng `= …` ngay dưới là tóm tắt nhịp, không in ra PDF |
| Tiêu đề cảnh | `EXT. THUNG LŨNG MÂY - NGÀY` (`EXT.` ngoài trời, `INT.` trong nhà) |
| Hành động | Tả những gì nhìn thấy, nghe thấy, thì hiện tại. Không viết suy nghĩ. Gag tả cụ thể từng bước |
| Tiếng động | Viết HOA trong hành động: `BOING!`, `SLURP!` |
| Thoại | Tên nhân vật viết HOA một dòng, thoại ngay dưới. Chỉ dẫn diễn xuất trong ngoặc: `(thì thầm)` |
| Nói ngoài khung / lời dẫn | `TAVI (O.S.)` / `NARRATOR (V.O.)` |
| Chuyển cảnh | `CUT TO:` |
| Ghi chú không in ra | `/* … */` |

**Thoại:** ngắn, ít chơi chữ, để lồng tiếng Việt và Anh không mất ý. Mỗi nhân vật nói đúng chất trong Character Bible.

## Thư mục

| Thư mục | Nội dung |
|---|---|
| `Scripts/` | Beat sheet (`.md`) và kịch bản (`.fountain`) từng tập, template |
| `Storyboards/` | Storyboard từng tập |
| `Animatics/` | Animatic từng tập |
