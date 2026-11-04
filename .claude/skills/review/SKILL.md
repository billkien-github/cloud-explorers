---
name: review
description: Review một tập hoặc một shot của Cloud Explorers bằng các reviewer độc lập rồi gộp kết quả. Beat sheet, kịch bản Fountain dùng 4 reviewer (story, character, audience, safety); shot đã render dùng 5 reviewer (character, visual, animation, pacing, audio). Dùng khi người dùng gõ /review, hoặc nhờ review, đánh giá, soi lỗi beat sheet, kịch bản, shot, video.
argument-hint: <EPxxx | file kịch bản | thư mục shot | file video> [ghi chú, ví dụ "chỉ cảnh 3"]
---

# Review

Tám reviewer trong `.claude/agents/<tên>-reviewer.md`. Mỗi loại đầu vào gọi một nhóm:

| Đầu vào | Reviewer |
|---|---|
| Beat sheet `.md`, kịch bản `.fountain` trong `03_CONTENT/Scripts/` | `story`, `character`, `audience`, `safety` |
| Shot trong `04_PRODUCTION/`: thư mục shot hoặc file video | `character`, `visual`, `animation`, `pacing`, `audio` (chỉ khi video có tiếng) |

Storyboard, animatic và bản phim hoàn chỉnh chưa có quy trình review.

## Chạy

1. **Chọn đầu vào:**
   - Mã tập (`EP001`): `03_CONTENT/Scripts/EPxxx_*.fountain` nếu đã có, chưa có thì beat sheet `EPxxx_*.md`.
   - Đường dẫn file kịch bản: file đó.
   - File video: file đó. Thư mục shot: video mới nhất trong `renders/` của shot theo thứ tự `_final`, `_preview_sound`, `_preview`.
   - Không có đối số: hỏi người dùng.
2. **Với shot, chuẩn bị trước** (Blender ở đường dẫn trong mục Công cụ của `README.md`):
   ```
   blender -b --factory-startup -P .claude/skills/review/extract_shot.py -- <video> <thư mục shot>/renders/review
   ```
   Lệnh tạo `frames/` (1 khung mỗi giây) và `review.json` (thông số video, điểm cắt, độ chuyển động từng giây, mức tiếng). Mỗi lần chạy xoá làm lại. `renders/` không lên git.
3. **Gọi các reviewer của nhóm trong cùng một lượt** để chạy song song. Prompt cho mỗi agent chỉ gồm:
   - Kịch bản: đường dẫn file, ghi chú của người dùng nếu có.
   - Shot: thư mục shot, đường dẫn video, thư mục `renders/review`, beat sheet của tập nếu shot nằm trong một thư mục `EPxxx_*`, shot có phải previz không (có thư mục `seedance/` là previz khối), ghi chú của người dùng nếu có.

   Không kèm nhận xét hay kết luận nào của phiên hiện tại, để reviewer đánh giá độc lập.
4. **Kiểm bằng chứng:**
   - Câu trích: grep trong file được review. Không tìm thấy thì hạ xuống "Nghi ngờ" và ghi "trích không khớp", hoặc bỏ nếu lỗi chỉ dựa vào câu trích đó.
   - Khung hình: file có trong `renders/review/frames/`. Với lỗi Chặn, tự mở khung được dẫn để xem lại.
   - Số đo (điểm cắt, chuyển động, mức tiếng): khớp `review.json`.
5. **Gộp:** các lỗi cùng một nguyên nhân thì gộp làm một, giữ mức cao nhất, ghi reviewer nào nêu. Hai reviewer nói ngược nhau về chuyện sáng tạo thì ghi cả hai ý, để người dùng quyết.
6. **Trả kết quả trong chat**, không ghi thành file trong repo (`CLAUDE.md` cấm file báo cáo):
   - **Kết luận:** Khoá được / Sửa rồi khoá / Chưa khoá được (còn lỗi Chặn).
   - **Lỗi** xếp theo mức Chặn → Nên sửa → Gợi ý, theo định dạng dưới đây.
   - Với kịch bản: **Checklist "Kiểm tra trước khi khóa kịch bản"** của beat sheet, từng mục Đạt / Chưa đạt / Không kiểm được.
   - **Điểm mạnh:** tối đa ba ý.
7. Không sửa file được review khi người dùng chưa đồng ý. Sửa xong thì chạy lại `/review`.

## Kết quả của reviewer

Các reviewer đọc mục này trước khi review.

**Quy tắc:**
- Chỉ đánh giá những gì có trong file hay khung hình được giao. Không bịa cảnh, dòng, câu thoại, khung hình. Không tự cho là đã kiểm phần không được giao.
- Mỗi lỗi có bằng chứng kèm vị trí:
  - Kịch bản: câu trích nguyên văn, ngắn, kèm cảnh và số dòng.
  - Shot: khung `frames/t<giây>.jpg` kèm điều nhìn thấy trong khung, hoặc số đo trong `review.json`, kèm thời điểm.
- Mỗi lỗi có căn cứ là file chuẩn của dự án và mục bị trái. File agent, skill không phải căn cứ. Không có căn cứ thì lỗi đó tối đa là Gợi ý.
- Lựa chọn sáng tạo nằm trong canon thì không phải lỗi.
- Đề xuất sửa phải cụ thể, làm được, và không trái Character Bible. Với shot, chỉ ra chỗ sửa trong `build_shot.py` nếu biết.
- Không chấm điểm số.

**Mức độ:**

| Mức | Khi nào |
|---|---|
| Chặn | Trái Character Bible, trái luật nhân quả hay checklist của tập; lời giải dùng thứ chưa gài trước; nội dung có thể làm trẻ sợ, gây nguy hiểm, sai khoa học khi trình bày như sự thật, thiếu tôn trọng truyện hay văn hoá. Với shot: nhân vật sai thiết kế, màu, dáng; động tác vượt giới hạn khi diễn; xuyên vật thể, giật hình, khung đen, thiếu material thấy rõ; tiếng méo. Phải sửa trước khi khoá |
| Nên sửa | Nhịp chậm, gag yếu, thoại lệch chất, lệch nhẹ so với `03_CONTENT/README.md`. Với shot: bố cục hay ánh sáng làm hành động khó đọc, trượt chân nhẹ, cú máy quá dài hay quá ngắn, lệch timeline, tiếng lệch hình |
| Gợi ý | Làm hay hơn, tuỳ chọn |

Kèm độ chắc: **Chắc** (bằng chứng rõ) hoặc **Nghi ngờ** (cần người xem lại).

**Định dạng trả về:**

```
## <tên reviewer>

### Lỗi
- [Chặn | Nên sửa | Gợi ý · Chắc | Nghi ngờ] <Cảnh n, dòng n | t=<giây>>: <vấn đề>
  - Bằng chứng: "<trích nguyên văn>" | frames/t<giây>.jpg: <điều thấy> | review.json: <số đo>
  - Căn cứ: <file>, mục <tên mục>
  - Sửa: <đề xuất cụ thể>

### Checklist của tập (chỉ khi review kịch bản, chỉ các mục thuộc phần mình)
- [Đạt | Chưa đạt | Không kiểm được] <mục>: <lý do ngắn>

### Điểm mạnh (tối đa 3)
- ...
```
