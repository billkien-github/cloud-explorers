# CLAUDE.md

Dặn dò cho agent làm việc trong repo **Cloud Explorers** (phim hoạt hình 3D cho trẻ em: ChatGPT sinh ảnh tham chiếu, Blender + code Python dựng model và previz, Seedance sinh hình cuối của shot). Trao đổi và viết tài liệu bằng **tiếng Việt**.

## Trước khi làm

Đọc `README.md` (trạng thái, cấu trúc, quy ước), rồi đọc file sở hữu chủ đề sắp đụng tới (bảng dưới).

## Mỗi chủ đề chỉ có một file sở hữu

| Chủ đề | File sở hữu |
|---|---|
| Tổng quan dự án, trạng thái, cấu trúc thư mục, quy ước chung, công cụ, git | `README.md` |
| Nhân vật: tính cách, ngoại hình, màu, chiều cao, bảo bối, giới hạn khi diễn | `01_BRAND/Character_Bible/README.md` |
| Hướng nội dung, Wonder Hub và Chronicle Engine, Season 0, series, khung tập, các bước làm một tập, cách viết kịch bản (Fountain) | `03_CONTENT/README.md` |
| Beat sheet, kịch bản từng tập | `03_CONTENT/Scripts/EPxxx_<tên>.md` (beat sheet), `.fountain` (kịch bản) |
| Previz 2D cutout, file mốc thời gian của cảnh (`timing.py`), CC | `03_CONTENT/PREVIZ_2D.md` |
| Quy ước thư mục asset | `02_ASSET_LIBRARY/README.md` |
| Ảnh tham chiếu và model 3D: ảnh của từng tập cho Seedance, bộ ảnh dựng model, prompt ChatGPT và cách sinh ảnh, dựng và rig trong Blender | `02_ASSET_LIBRARY/MODELING.md` |
| Previz Blender + Seedance, quy ước khối previz, chọn ảnh tham chiếu, thư mục tải lên, prompt theo giây | `04_PRODUCTION/SEEDANCE.md` |
| Code dùng chung, render, Blender MCP, lưu ý kỹ thuật Blender | `pipeline/README.md` |
| Review bằng agent (beat sheet, kịch bản, previz, prompt Seedance, take, shot): nhóm reviewer theo đầu vào, cách chạy, mức độ lỗi, định dạng kết quả | `.claude/skills/review/SKILL.md`; việc riêng của từng reviewer trong `.claude/agents/<tên>-reviewer.md` |
| Cách giữ tài liệu, việc của agent sau mỗi lần làm | `CLAUDE.md` (file này) |

- Thông tin chỉ ghi ở file sở hữu. File khác cần nhắc tới thì trỏ đường dẫn, **không chép lại** (chép lại là nguồn gốc của mâu thuẫn).
- Chủ đề mới chưa có chủ: tạo file trong đúng thư mục theo `README.md`, rồi thêm vào bảng này và bảng "Tài liệu" trong `README.md`.
- Không tạo file ghi chú, báo cáo, tóm tắt phiên làm việc trong repo.

## Sau mỗi lần làm việc: tự review và dọn dẹp

Làm trước khi báo xong việc, không cần người dùng nhắc:

1. **Xem lại thay đổi:** `git status` và `git diff`. Với mỗi thay đổi, hỏi: file sở hữu chủ đề này đã phản ánh đúng chưa?
2. **Cập nhật tài liệu tại chỗ:**
   - Quyết định mới, đổi thiết kế, đổi quy trình: sửa thẳng vào file sở hữu, xoá câu cũ.
   - Không thêm "cập nhật ngày…", không giữ đoạn đã lỗi thời kèm ghi chú, không giữ phương án đã bị bỏ. Lịch sử nằm trong git.
   - Ngày tra cứu thông tin bên ngoài (giá, tính năng Seedance…) thì được ghi, vì đó là độ mới của dữ liệu.
   - Cập nhật mục **Trạng thái** trong `README.md` (đã có gì, bước tiếp theo).
   - Việc còn chờ người dùng quyết: ghi một lần ở file sở hữu. Khi đã chốt thì xoá mục chờ và ghi kết quả như thông tin bình thường.
3. **Dò mâu thuẫn và tham chiếu chết:**
   - Grep tên file, thư mục, tên cũ vừa đổi hoặc xoá trong mọi `.md`, `.py`, `.ps1`, `.sh`.
   - Mọi đường dẫn nhắc trong tài liệu phải tồn tại (trừ mẫu như `<tên>` hay file sẽ do script tạo).
   - Sửa `pipeline/run.ps1` hay `pipeline/run.sh` thì sửa cả hai cho khớp (`pipeline/README.md`, đoạn "Giữ hai file đồng bộ").
   - Cùng một con số, tên gọi, quyết định không được khác nhau giữa các file.
4. **Dọn file:**
   - Xoá file tạm, shot thử, script thử, `__pycache__`, output test.
   - Code không còn ai dùng thì xoá (lấy lại từ git khi cần). `pipeline/` chỉ chứa code có từ hai nơi trở lên dùng; code riêng nằm cạnh asset hay shot của nó.
   - File nằm sai chỗ so với cấu trúc trong `README.md` thì chuyển hoặc xoá. Không dùng `.gitkeep`: thư mục trống không cần có trên git.
   - Tài liệu nào rỗng ý, trùng ý hoặc quá dài so với giá trị thì gộp, rút gọn hoặc xoá.
5. **Kiểm tra code đã sửa** còn chạy (ít nhất kiểm tra cú pháp; script render thì chạy thử trên dữ liệu nhỏ rồi xoá dữ liệu thử).
6. **Báo lại** cho người dùng những gì đã cập nhật, đã xoá, và chỗ nào còn chưa chắc.

## Riêng cho agent

Quy ước chung (dựng bằng script, file gốc, đặt tên, shot, git LFS) và công cụ nằm ở `README.md`, lưu ý API Blender 5.2 ở `pipeline/README.md`. Thêm:
- Chỉ commit, push khi người dùng yêu cầu. Commit message tiếng Việt.
- Không ghi API key (BytePlus…) vào repo hay vào chat; người dùng tự đặt biến môi trường.
- Sinh Seedance tốn tiền thật: đoạn cần hơn 9 ảnh tham chiếu thì không tự gửi bằng 2.5, phải phân tích ảnh nào bỏ hay gộp được rồi hỏi người dùng trước (`04_PRODUCTION/SEEDANCE.md`, mục "Gộp ảnh tham chiếu").
