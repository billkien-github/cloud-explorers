---
name: review
description: Review beat sheet hoặc kịch bản Fountain của một tập Cloud Explorers bằng ba reviewer độc lập (story, character, kids) rồi gộp kết quả. Dùng khi người dùng gõ /review, hoặc nhờ review, đánh giá, soi lỗi beat sheet hay kịch bản.
argument-hint: <EPxxx | đường dẫn file> [ghi chú, ví dụ "chỉ cảnh 3"]
---

# Review kịch bản

Hiện chỉ review beat sheet (`.md`) và kịch bản (`.fountain`) trong `03_CONTENT/Scripts/`. Storyboard, shot, video chưa có reviewer.

## Chạy

1. **Chọn file:** đối số là mã tập (`EP001`) thì lấy `03_CONTENT/Scripts/EPxxx_*.fountain` nếu đã có, chưa có thì lấy beat sheet `EPxxx_*.md`. Đối số là đường dẫn thì lấy file đó. Không có đối số thì hỏi người dùng.
2. **Gọi ba subagent trong cùng một lượt** để chạy song song: `story-reviewer`, `character-reviewer`, `kids-reviewer`. Prompt cho mỗi agent chỉ gồm đường dẫn file cần review và ghi chú của người dùng nếu có. Không kèm nhận xét hay kết luận nào của phiên hiện tại, để reviewer đánh giá độc lập.
3. **Kiểm bằng chứng:** với mỗi lỗi, grep câu trích trong file được review. Không tìm thấy thì hạ xuống "Nghi ngờ" và ghi "trích không khớp", hoặc bỏ nếu lỗi chỉ dựa vào câu trích đó.
4. **Gộp:** các lỗi cùng một nguyên nhân thì gộp làm một, giữ mức cao nhất, ghi reviewer nào nêu. Hai reviewer nói ngược nhau về chuyện sáng tạo thì ghi cả hai ý, để người dùng quyết.
5. **Trả kết quả trong chat**, không ghi thành file trong repo (`CLAUDE.md` cấm file báo cáo):
   - **Kết luận:** Khoá được / Sửa rồi khoá / Chưa khoá được (còn lỗi Chặn).
   - **Lỗi** xếp theo mức Chặn → Nên sửa → Gợi ý, theo định dạng dưới đây.
   - **Checklist "Kiểm tra trước khi khóa kịch bản"** của beat sheet: từng mục Đạt / Chưa đạt / Không kiểm được.
   - **Điểm mạnh:** tối đa ba ý.
6. Không sửa file được review khi người dùng chưa đồng ý. Sửa xong thì chạy lại `/review`.

## Kết quả của reviewer

Các reviewer đọc mục này trước khi review.

**Quy tắc:**
- Chỉ đánh giá những gì có trong file. Không bịa cảnh, dòng, câu thoại. Không tự cho là đã kiểm phần không được giao.
- Mỗi lỗi có bằng chứng là câu trích nguyên văn, ngắn, kèm vị trí (cảnh, số dòng).
- Mỗi lỗi có căn cứ là file chuẩn của dự án và mục bị trái. File agent, skill không phải căn cứ. Không có căn cứ thì lỗi đó tối đa là Gợi ý.
- Lựa chọn sáng tạo nằm trong canon thì không phải lỗi.
- Đề xuất sửa phải cụ thể, làm được, và không trái Character Bible.
- Không chấm điểm số.

**Mức độ:**

| Mức | Khi nào |
|---|---|
| Chặn | Trái Character Bible, trái luật nhân quả hay checklist của tập; lời giải dùng thứ chưa gài trước; nội dung có thể làm trẻ sợ, gây nguy hiểm, sai khoa học khi trình bày như sự thật, thiếu tôn trọng truyện hay văn hoá. Phải sửa trước khi khoá |
| Nên sửa | Nhịp chậm, gag yếu, thoại lệch chất, lệch nhẹ so với `03_CONTENT/README.md` |
| Gợi ý | Làm hay hơn, tuỳ chọn |

Kèm độ chắc: **Chắc** (bằng chứng rõ trong file) hoặc **Nghi ngờ** (cần người xem lại).

**Định dạng trả về:**

```
## <tên reviewer>

### Lỗi
- [Chặn | Nên sửa | Gợi ý · Chắc | Nghi ngờ] <Cảnh n, dòng n>: <vấn đề>
  - Bằng chứng: "<trích nguyên văn>"
  - Căn cứ: <file>, mục <tên mục>
  - Sửa: <đề xuất cụ thể>

### Checklist của tập (chỉ các mục thuộc phần mình)
- [Đạt | Chưa đạt | Không kiểm được] <mục>: <lý do ngắn>

### Điểm mạnh (tối đa 3)
- ...
```
