---
name: review
description: Review một tập, một cảnh hoặc một shot của Cloud Explorers bằng các reviewer độc lập rồi gộp kết quả, theo đường kịch bản → previz 2D → previz khối → Seedance. Beat sheet, kịch bản Fountain; previz 2D từng cảnh; previz khối; prompt Seedance trước khi sinh; take Seedance; shot dựng 3D. Dùng khi người dùng gõ /review, hoặc nhờ review, đánh giá, soi lỗi beat sheet, kịch bản, previz, prompt, take, shot, video.
argument-hint: <EPxxx | file kịch bản | thư mục cảnh previz 2D | thư mục shot | seedance/prompt.md | file take> [ghi chú, ví dụ "chỉ cảnh 3"]
---

# Review

Tám reviewer trong `.claude/agents/<tên>-reviewer.md`. Mỗi cổng gọi một nhóm. Previz 2D theo `03_CONTENT/PREVIZ_2D.md`; previz khối, prompt, take là bước 3, 6, 8 trong `04_PRODUCTION/SEEDANCE.md`.

| Cổng | Đầu vào | Reviewer |
|---|---|---|
| Kịch bản | `EPxxx`, hoặc file `.md`, `.fountain` trong `03_CONTENT/Scripts/` | `story`, `character`, `audience`, `safety` |
| Previz 2D | Thư mục cảnh trong `03_CONTENT/Previz_2D/` | `story`, `character`, `audience`, `pacing` |
| Previz khối | Thư mục shot có `seedance/` | `story`, `audience`, `pacing`, `visual`, `character` |
| Prompt | `<shot>/seedance/prompt.md` | `check_prompt.py`, rồi `pacing`, `character` |
| Take | File video trong `<shot>/seedance/` | `character`, `visual`, `animation`, `pacing`, `safety`; thêm `audio` nếu take có tiếng |
| Shot dựng 3D | Thư mục shot không có `seedance/`, hoặc một video trong `renders/` của nó | `character`, `visual`, `animation`, `pacing`; thêm `audio` nếu có tiếng |

Cả tập đã ghép chưa có quy trình review.

## Chạy

1. **Chọn đầu vào** theo bảng trên. Không có đối số thì hỏi người dùng. Mã tập: beat sheet cùng `.fountain` nếu đã có, chưa có `.fountain` thì chỉ beat sheet. Có `.fountain` mà chưa có beat sheet (có Luật nhân quả, Gài trước trả sau, checklist) thì dừng, đề nghị viết beat sheet trước: không có thước đo thì mỗi lượt reviewer tự đặt chuẩn, lỗi không bao giờ hết.
2. **Chuẩn bị video** (Blender ở đường dẫn trong mục Công cụ của `README.md`):
   ```
   blender -b --factory-startup -P .claude/skills/review/extract_shot.py -- <video> <thư mục shot>/renders/review/<previz|take|shot>
   ```
   Mỗi lần chạy, thư mục đích bị xoá làm lại. Kết quả gồm `frames/t<giây>.jpg` (1 khung mỗi giây, take và previz cùng tên theo giây để so) và `review.json` (thông số, điểm cắt, độ chuyển động từng giây, mức tiếng). `renders/` không lên git.
   - **Previz 2D:** `renders/<tên>_preview_cc.mp4` (có CC), chưa có thì `_preview.mp4`, vào `review/previz2d`.
   - **Previz khối:** `renders/<tên>_preview_cc.mp4` (có CC), chưa có thì `_ref.mp4`, rồi `_preview.mp4`, vào `review/previz`.
   - **Prompt:** trích previz như trên, rồi chạy `python .claude/skills/review/check_prompt.py <thư mục shot> <thư mục shot>/renders/review/previz/review.json`. Previz dùng ở đây là bản đã tải lên Seedance: `renders/seedance_upload/video1_previz.mp4`, chưa có thì `_ref.mp4`.
   - **Take:** take vào `review/take`, previz đã tải lên Seedance vào `review/previz`.
   - **Shot dựng 3D:** video mới nhất trong `renders/` theo thứ tự `_final`, `_preview_sound`, `_preview`, vào `review/shot`.
3. **Gọi các reviewer của cổng trong cùng một lượt** để chạy song song. Prompt cho mỗi agent chỉ gồm:
   - tên cổng;
   - đường dẫn file kịch bản, hoặc thư mục shot, video, các thư mục `renders/review/...` đã chuẩn bị;
   - kịch bản của tập nếu có (`.fountain` nếu đã có, không thì beat sheet), lấy theo thư mục `EPxxx_*` của cảnh, shot hoặc đường dẫn ghi trong docstring `build_shot.py`;
   - `timing.py` của cảnh và file `.srt` của CC nếu có;
   - `seedance/prompt.md` nếu có, và kết quả `check_prompt.py` ở cổng prompt;
   - ghi chú của người dùng nếu có;
   - lượt review lại: danh sách lỗi Chặn, Nên sửa của lượt trước (nguyên văn reviewer đã nêu), để kiểm đã sửa đúng chưa.

   Không kèm nhận xét hay kết luận nào khác của phiên hiện tại, để reviewer đánh giá độc lập.
4. **Kiểm bằng chứng:**
   - Câu trích: grep trong file được review. Không tìm thấy thì hạ xuống "Nghi ngờ" và ghi "trích không khớp", hoặc bỏ nếu lỗi chỉ dựa vào câu trích đó.
   - Khung hình: file có trong `renders/review/.../frames/`. Với lỗi Chặn, tự mở khung được dẫn để xem lại.
   - Số đo (điểm cắt, chuyển động, mức tiếng): khớp `review.json`.
   - Kết quả của `check_prompt.py` là số đo, không cần kiểm lại.
5. **Gộp:** các lỗi cùng một nguyên nhân thì gộp làm một, giữ mức cao nhất, ghi reviewer nào nêu (script là `check_prompt`). Hai reviewer nói ngược nhau về chuyện sáng tạo thì ghi cả hai ý, để người dùng quyết.
6. **Trả kết quả trong chat**, không ghi thành file trong repo (`CLAUDE.md` cấm file báo cáo):
   - **Kết luận:** Khoá được / Sửa rồi khoá / Chưa khoá được (còn lỗi Chặn). Với take: Dùng được / Sửa prompt hay previz rồi sinh lại.
   - **Lỗi** xếp theo mức Chặn → Nên sửa → Gợi ý, theo định dạng dưới đây.
   - Với kịch bản: **Checklist "Kiểm tra trước khi khóa kịch bản"** của beat sheet, từng mục Đạt / Chưa đạt / Không kiểm được.
   - Với take: một dòng tóm tắt cho mục Take ở cuối `seedance/prompt.md` (theo `SEEDANCE.md`). Chỉ ghi vào file khi người dùng đồng ý.
   - **Điểm mạnh:** tối đa ba ý.
7. Không sửa file được review khi người dùng chưa đồng ý.

## Sửa và review lại

Phần lớn lỗi của các lượt sau sinh ra từ chính lần sửa trước. Sửa theo thứ tự:

1. **Sửa hết Chặn và Nên sửa. Gợi ý chỉ áp cái người dùng chọn.** Mỗi Gợi ý thêm một chi tiết mới, tức là thêm một chỗ có thể vênh với luật. Áp cả loạt Gợi ý cùng lúc sửa lỗi Chặn thì lượt sau gần như chắc chắn có lỗi mới.
2. **Lỗi đòi thêm hay đổi một luật** (cách bảo bối báo hiệu, luật nhân quả, một mục checklist): ghi luật vào file sở hữu trước, rồi soát toàn bộ kịch bản theo luật đó, không chỉ dòng bị nêu.
3. **Tự soát trước khi chạy lại:** đi qua từng gạch Luật nhân quả và từng mục checklist của beat sheet, đối chiếu mọi dòng đã đổi; sửa beat sheet cùng lúc với kịch bản để hai file khớp nhau.
4. **Chạy lại khi nào:**
   - Lượt vừa rồi còn Chặn, hoặc lần sửa thêm hay đổi luật: chạy lại `/review`, gửi kèm danh sách lỗi Chặn, Nên sửa của lượt trước (bước 3 ở mục Chạy).
   - Chỉ còn Nên sửa và lần sửa không đổi luật: sửa, tự soát, rồi khoá; không cần chạy lại cả nhóm reviewer.
   - Gợi ý mới ở lượt review lại không chặn khoá. Khoá khi không còn Chặn và Nên sửa.
5. **Rút kinh nghiệm:** một đầu vào phải review từ lượt thứ ba trở lên thì tìm vì sao lỗi cứ xuất hiện (thiếu thước đo, lần sửa gây lỗi mới, reviewer thiếu căn cứ…) và cập nhật vào skill này, file vai reviewer hoặc file chuẩn. Không ghi file báo cáo.

## Kết quả của reviewer

Các reviewer đọc mục này trước khi review.

**Quy tắc:**
- Chỉ đánh giá những gì có trong file hay khung hình được giao. Không bịa cảnh, dòng, câu thoại, khung hình. Không tự cho là đã kiểm phần không được giao.
- Mỗi lỗi có bằng chứng kèm vị trí:
  - Kịch bản, prompt: câu trích nguyên văn, ngắn, kèm cảnh hoặc khối và số dòng.
  - Video: khung `frames/t<giây>.jpg` kèm điều nhìn thấy trong khung, hoặc số đo trong `review.json`, kèm thời điểm. Take thì ghi kèm khung previz cùng giây nếu so sánh.
- Mỗi lỗi có căn cứ là file chuẩn của dự án và mục bị trái. File agent, skill không phải căn cứ. Không có căn cứ thì lỗi đó tối đa là Gợi ý.
- Lựa chọn sáng tạo nằm trong canon thì không phải lỗi.
- Đề xuất sửa phải cụ thể, làm được, và không trái Character Bible. Chỉ ra chỗ sửa: dòng kịch bản, hằng số trong `build_shot.py`, hay khối nào trong prompt.
- Không chấm điểm số.

**Mức độ:**

| Mức | Khi nào |
|---|---|
| Chặn | Trái Character Bible, trái luật nhân quả hay checklist của tập; lời giải dùng thứ chưa gài trước; nội dung có thể làm trẻ sợ, gây nguy hiểm, sai khoa học khi trình bày như sự thật, thiếu tôn trọng truyện hay văn hoá. Previz: hành động không đọc ra đúng ý kịch bản (vô ý thành cố ý, không thấy nguyên nhân). Prompt: thời lượng, điểm cắt, tham chiếu `@Image`, `@Video` hay file tải lên sai. Take, shot: nhân vật sai thiết kế, màu, dáng; người thừa; chữ, logo, màu khối lọt vào hình; xuyên vật thể, biến dạng, giật hình thấy rõ; cú máy lệch previz; tiếng méo. Phải sửa trước khi khoá hay trước khi sinh |
| Nên sửa | Nhịp chậm, gag yếu, thoại lệch chất, lệch nhẹ so với `03_CONTENT/README.md`. Previz, take, shot: bố cục hay ánh sáng làm hành động khó đọc, trượt chân nhẹ, cú máy quá dài hay quá ngắn, lệch timeline. Previz: CC lệch kịch bản hay lệch hình. Prompt: mốc không lấy từ hằng số, một mốc nhồi nhiều việc |
| Gợi ý | Làm hay hơn, tuỳ chọn |

Kèm độ chắc: **Chắc** (bằng chứng rõ) hoặc **Nghi ngờ** (cần người xem lại).

**Định dạng trả về:**

```
## <tên reviewer>

### Lỗi
- [Chặn | Nên sửa | Gợi ý · Chắc | Nghi ngờ] <Cảnh n, dòng n | t=<giây> | khối prompt>: <vấn đề>
  - Bằng chứng: "<trích nguyên văn>" | frames/t<giây>.jpg: <điều thấy> | review.json: <số đo>
  - Căn cứ: <file>, mục <tên mục>
  - Sửa: <đề xuất cụ thể>

### Checklist của tập (chỉ khi review kịch bản, chỉ các mục thuộc phần mình)
- [Đạt | Chưa đạt | Không kiểm được] <mục>: <lý do ngắn>

### Điểm mạnh (tối đa 3)
- ...
```
