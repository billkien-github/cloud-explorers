# Cloud Explorers

Phim hoạt hình 3D cho trẻ em, phát hành YouTube-first. Bốn người bạn Lumo, Tavi, Nori, Piko phiêu lưu qua những vùng đất kỳ diệu. Dựng bằng **Blender**, phần lớn bằng **code Python**. Ảnh concept và ảnh tham chiếu sinh bằng **ChatGPT**, model nhân vật, đạo cụ dựng trong Blender, hình cuối của shot sinh bằng **Seedance**.

## Dự án

| | |
|---|---|
| Mô hình | Studio nhỏ (2–5 người), **YouTube-first** |
| Khán giả | Trẻ em, Việt Nam + quốc tế (một bộ hình, nhiều bản lồng tiếng) |
| Mục tiêu năm 1 | Views. Sau 12 tháng cần **1 IP có tiềm năng + 1 pipeline 3D hiệu quả + 1 format đã được kiểm chứng** |
| Nguyên tắc số 1 | **Content đi trước production**: chốt câu chuyện rồi mới modeling |
| Lộ trình 12 tháng | Foundation (T1–2) → Prototype (T3–4) → Validation (T5–6) → Growth (T7–8) → Brand (T9–10) → Scale (T11–12) |

Chính sách YouTube: nội dung cho trẻ phải khai báo **Made for Kids** (mất bình luận, thông báo, quảng cáo cá nhân hoá). Chính sách **inauthentic content** nhắm vào nội dung hàng loạt, lặp lại: tái sử dụng asset được, nhưng mỗi tập phải có câu chuyện riêng thật sự.

## Trạng thái

- Có: concept 4 nhân vật, 4 bảo bối, ảnh thế giới; ảnh tham chiếu dựng model đã đủ bộ của bốn nhân vật chính Lumo, Tavi, Nori, Piko (thân A-pose, T-pose, bản đủ đồ, nhìn trước và sau; đuôi, cánh) và sinh vật nhỏ, bốn bảo bối (nhìn trước và sau), cùng mọi đạo cụ và nhân vật phụ tập 01 (máy Rain-O-Matic, thuyền, cầu ván, đôi voi con, Noah, thú trên boong…). Chưa dựng model nào trong Blender. Ảnh xoay (trước và sau trong một ảnh) của bốn nhân vật chính để làm tham chiếu Seedance, chưa thử trong take nào. Danh sách và prompt ChatGPT trong `02_ASSET_LIBRARY/MODELING.md`; beat sheet tập 01 đã chốt (khoảng 7 phút); code dùng chung trong `pipeline/`.
- Previz thử `04_PRODUCTION/TEST_First_Rain/sh010`: Cảnh 3 tập 01 (mây bé, Piko hoá cái bát, đè nút MAX POWER) rút gọn 27 giây, 7 shot cắt trong một previz, đủ 4 nhân vật dạng khối. Đã có prompt theo giây, danh sách file tải lên (`seedance/prompt.md`) và take 1 (`seedance/sh010_take01.mp4`), chưa soát.
- Quy trình: kịch bản → previz 2D từng cảnh có CC (`03_CONTENT/PREVIZ_2D.md`) → previz khối có CC → Seedance (`04_PRODUCTION/SEEDANCE.md`). Đã có công cụ in CC (`pipeline/cc.py`), công cụ ghép video kèm CC và `.srt` (`pipeline/edit.py`) và bộ nhân vật cutout 2D (`pipeline/cutout.py`), cảnh thử ở `03_CONTENT/Previz_2D/TEST_Cutout/canh01` (11 giây, Lumo vội với tay, khựng lại, bị Piko đè xuống nút).
- Previz 2D tập 01 (`03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/`, có CC): Cảnh 1 (`canh01`, khoảng 55 giây, 14 cú máy) đã sửa theo năm lượt review (từ lượt ba không còn lỗi Chặn); các diễn biến previz thêm vào đã ghi vào kịch bản. Cảnh 2 (`canh02`, khoảng 87 giây, 27 cú máy: montage lắp máy, bánh răng vàng, ròng rọc và Story Lens, Wonder Hub, nút đỏ) đã sửa theo lượt review đầu (có một lỗi Chặn: cần gạt TẮT bị che), chờ review lại. Cảnh 3–7 chưa dựng.
- Previz khối tập 01 (`04_PRODUCTION/EP001_Great_Rain_Experiment/`, có CC): Cảnh 1 chia hai đoạn dưới 30 giây, `sh010` (0–28.8 s, S1–S6) và `sh020` (28.8–55 s, S7–S14), dựng chung từ `canh01_blocks.py` theo mốc của previz 2D. Cả hai đoạn có prompt Seedance và file tải lên gom sẵn (8 ảnh tham chiếu). `sh020` đã sinh take 1 (`sh020/seedance/sh020_take01.mp4`, 480p), review thấy chưa dùng được (thìa đè lên mắt Piko, Nori bị lá che ở cuối); đã sửa prompt và previz (render lại `ref` cả hai đoạn), chờ sinh take 2. `sh010` chưa sinh; prompt đã áp các bài học từ take 1. Danh sách dựng cả cảnh: `canh01_edit.py` (đang trỏ `sh010_take01`, `sh020_take01`; take chưa có thì `edit.py` thay bằng khung tối). Previz hai đoạn chưa `/review`. Ảnh tham chiếu sinh bằng ChatGPT (prompt trong `04_PRODUCTION/SEEDANCE.md`): bối cảnh Thung lũng Mây khô hạn, Piko đeo Pocket of Wonders, sinh vật nhỏ của thung lũng.
- Review bằng agent (`.claude/skills/review/SKILL.md`): `/review EP001` cho beat sheet, kịch bản; `/review <thư mục cảnh>` cho previz 2D; `/review <thư mục shot>` cho previz khối; `/review <shot>/seedance/prompt.md` trước khi sinh; `/review <file take>` cho take. Kết quả gộp trong chat. Chưa review được cả tập đã ghép.
- Kịch bản tập 01 đã chốt (`03_CONTENT/Scripts/EP001_great_rain_experiment.fountain`), 7 cảnh, qua ba lượt `/review`.
- Season 0 (khung 5 tập, Wonder Hub và Chronicle Engine: `03_CONTENT/README.md`): EP000A (tập Lumo) có beat sheet (`03_CONTENT/Scripts/EP000A_mysterious_compass.md`) và kịch bản bản nháp 5 (`.fountain`), lượt `/review` thứ năm còn một lỗi Chặn (tiếng TÍT ở Cảnh 2 chưa theo luật "càng gần càng kêu") và một lỗi Nên sửa (hòn đảo chìm vào mây trái beat sheet), chưa sửa. EP000B–E mới là bản nháp ChatGPT, chưa đưa vào repo; khi viết EP000E phải theo đoạn kết bánh răng vàng đã chốt.
- Chưa có: model 3D của cả bốn nhân vật và đạo cụ.
- **Bước tiếp theo:** sinh take 2 của `sh020` và take 1 của `sh010` trên BytePlus ModelArk (prompt đã theo cú pháp `@Image1`, video dài 29 s và 27 s, lúc dựng cắt về 28.8 s và 26.2 s), soát bằng `/review`; `/review` previz khối hai đoạn Cảnh 1; review lại Cảnh 2 và Cảnh 1, chốt hai cảnh; dựng previz 2D Cảnh 3–7, mỗi cảnh xong thì `/review`. Cái máy Rain-O-Matic đang dựng trong `build_shot.py` của Cảnh 2: dựng Cảnh 3 thì chuyển nó sang `pipeline/` để dùng chung. Song song: soát take 1 của `TEST_First_Rain` bằng `/review` và ghi kết quả vào `seedance/prompt.md`; sinh các ảnh tham chiếu còn thiếu theo `02_ASSET_LIBRARY/MODELING.md` (gồm concept máy Rain-O-Matic).

## Tài liệu

| File | Nội dung |
|---|---|
| [`01_BRAND/Character_Bible/README.md`](01_BRAND/Character_Bible/README.md) | Nhân vật: tính cách, ngoại hình, màu, chiều cao, bảo bối, cách làm 3D |
| [`03_CONTENT/README.md`](03_CONTENT/README.md) | Hướng nội dung: công thức, Wonder Hub và Chronicle Engine, Season 0, 5 series, khung tập 6–8 phút, nhịp cho trẻ em, luật đạo cụ, cách viết kịch bản |
| [`03_CONTENT/PREVIZ_2D.md`](03_CONTENT/PREVIZ_2D.md) | Previz 2D cutout từng cảnh, file mốc thời gian `timing.py` của cảnh, CC |
| [`03_CONTENT/Scripts/EP001_great_rain_experiment.md`](03_CONTENT/Scripts/EP001_great_rain_experiment.md) | Beat sheet tập 01 |
| [`03_CONTENT/Scripts/EP001_great_rain_experiment.fountain`](03_CONTENT/Scripts/EP001_great_rain_experiment.fountain) | Kịch bản tập 01 |
| [`03_CONTENT/Scripts/EP000A_mysterious_compass.md`](03_CONTENT/Scripts/EP000A_mysterious_compass.md) | Beat sheet Season 0, tập Lumo |
| [`03_CONTENT/Scripts/EP000A_mysterious_compass.fountain`](03_CONTENT/Scripts/EP000A_mysterious_compass.fountain) | Kịch bản nháp Season 0, tập Lumo |
| [`02_ASSET_LIBRARY/README.md`](02_ASSET_LIBRARY/README.md) | Quy ước thư mục asset |
| [`02_ASSET_LIBRARY/MODELING.md`](02_ASSET_LIBRARY/MODELING.md) | Làm nhân vật, đạo cụ 3D: bộ ảnh tham chiếu và hiện trạng, prompt ChatGPT, dựng và rig trong Blender |
| [`04_PRODUCTION/SEEDANCE.md`](04_PRODUCTION/SEEDANCE.md) | Dựng shot bằng previz Blender + Seedance, prompt theo giây |
| [`pipeline/README.md`](pipeline/README.md) | Code dùng chung, cách render, Blender MCP |
| [`.claude/skills/review/SKILL.md`](.claude/skills/review/SKILL.md) | Skill `/review`: 8 reviewer trong `.claude/agents/` cho kịch bản, previz, prompt Seedance, take và shot; mức độ lỗi, định dạng kết quả |
| [`CLAUDE.md`](CLAUDE.md) | Dặn dò cho agent: file nào sở hữu chủ đề nào, việc review và dọn tài liệu sau mỗi lần làm |

## Cấu trúc thư mục

```
studio/
├── 01_BRAND/                Logo/, Brand_Guideline/ (world_key_art.png), Character_Bible/
├── 02_ASSET_LIBRARY/        Characters/, Props/, Environments/, Materials/, Animation_Library/
├── 03_CONTENT/              Scripts/, Previz_2D/
├── 04_PRODUCTION/           Mỗi tập một thư mục, mỗi shot một thư mục con: EP001_Great_Rain_Experiment/sh010/; clip thử: TEST_<tên>/
├── 05_POST_PRODUCTION/      Editing/, Sound/, Dubbing/
├── 06_PUBLISHING/           Thumbnails/, Metadata/ (tiêu đề, mô tả, CREDITS.md), Final_Videos/
├── 07_ANALYTICS/            Monthly_Report/, Annual_Report/
├── pipeline/                Code dùng chung
└── .claude/                 agents/ (các reviewer), skills/review/ (skill /review)
```

## Quy ước

- **Dựng bằng script:** mỗi asset hay shot có script build nằm cạnh nó. Sửa script rồi build lại, không sửa tay file `.blend` do script tạo ra (thử bằng tay qua Blender MCP xong thì chép thay đổi vào script).
- **Asset tự làm hết:** không dùng model, texture hay asset bên thứ ba.
- **Đặt tên:** thư mục viết hoa chữ đầu, nối bằng gạch dưới (`EP001_Great_Rain_Experiment`, `Wonder_Compass`). File viết thường, không dấu, nối bằng gạch dưới (`lumo_hero.png`); riêng mã tập giữ viết hoa (`EP001_great_rain_experiment.md`). Không dùng dấu tiếng Việt trong tên file vì Blender và ffmpeg hay lỗi đường dẫn.
- **Shot:** `sh010/` gồm `build_shot.py`, `sh010.blend`, `renders/`; shot làm qua Seedance có thêm `seedance/` (`04_PRODUCTION/SEEDANCE.md`). Đánh số cách 10 để còn chèn shot vào giữa.
- **Tài liệu chỉ ghi thông tin hiện hành**, mỗi thông tin chỉ nằm ở một file (bảng file sở hữu và cách giữ tài liệu: `CLAUDE.md`). Lịch sử đã có git.

## Công cụ

| Công cụ | Ghi chú |
|---|---|
| Blender 5.2.3 LTS | Windows: `C:\Program Files\Blender Foundation\Blender 5.2`. macOS: `/Applications/Blender.app`, chạy dòng lệnh bằng `/Applications/Blender.app/Contents/MacOS/Blender`. Render bằng EEVEE vì máy Windows chỉ có card tích hợp Vega 11 |
| Python của Blender | Windows: `...\Blender 5.2\5.2\python\bin\python.exe`. macOS: `/Applications/Blender.app/Contents/Resources/5.2/python/bin/python3.13`. Có sẵn numpy |
| ChatGPT | Sinh ảnh: concept, ảnh tham chiếu dựng model (`02_ASSET_LIBRARY/MODELING.md`), ảnh tham chiếu cho Seedance (`04_PRODUCTION/SEEDANCE.md`) |
| Seedance (BytePlus ModelArk) | Sinh hình cuối của shot từ previz Blender (`04_PRODUCTION/SEEDANCE.md`) |
| Blender MCP | Cho Claude điều khiển Blender đang mở, xem `pipeline/README.md` |
| Add-on Higgsfield 1.5.60 | Sinh 3D, ảnh, video, animation bằng AI ngay trong viewport (thanh prompt ở đáy 3D view, đăng nhập tài khoản Higgsfield, trừ credit). Cài vào repo `user_default` của Blender 5.2 trên máy Windows. Tài khoản này đã dùng cho các take Seedance thử đầu; nay Seedance chạy trên BytePlus ModelArk (`04_PRODUCTION/SEEDANCE.md`) |

## Git

- Repo: https://github.com/billkien-github/cloud-explorers
- File nhị phân (`.blend`, ảnh, video, âm thanh, FBX/GLB, zip) đi qua **Git LFS** (`.gitattributes`).
- Không đưa lên git (`.gitignore`): `*.blend1`, log, cache Python, mọi thư mục `renders/` và `backups/` (bản lưu từng giai đoạn của build script), `06_PUBLISHING/Final_Videos/`.
