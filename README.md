# Cloud Explorers

Phim hoạt hình 3D cho trẻ em, phát hành YouTube-first. Bốn người bạn Lumo, Tavi, Nori, Piko phiêu lưu qua những vùng đất kỳ diệu. Dựng bằng **Blender**, phần lớn bằng **code Python**. Hình nhân vật và đạo cụ sinh bằng **Meshy**.

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

- Có: concept 4 nhân vật, 4 bảo bối, ảnh thế giới; ảnh đầu vào Meshy cho cả 8 asset (Lumo đã đạt cả A-pose và T-pose; Tavi, Nori, Piko cần sửa ảnh bằng GPT trước, prompt trong `02_ASSET_LIBRARY/MESHY.md`); beat sheet tập 01 đã chốt (khoảng 7 phút); code dùng chung trong `pipeline/`.
- Previz thử `04_PRODUCTION/TEST_First_Rain/sh010`: Cảnh 3 tập 01 (mây bé, Piko hoá cái bát, đè nút MAX POWER) rút gọn 27 giây, 7 shot cắt trong một previz, đủ 4 nhân vật dạng khối. Đã có prompt theo giây, danh sách file tải lên (`seedance/prompt.md`) và take 1 (`seedance/sh010_take01.mp4`), chưa soát.
- Quy trình: kịch bản → previz 2D từng cảnh có CC (`03_CONTENT/PREVIZ_2D.md`) → previz khối có CC → Seedance (`04_PRODUCTION/SEEDANCE.md`). Đã có công cụ in CC (`pipeline/cc.py`) và bộ nhân vật cutout 2D, thử ở `03_CONTENT/Previz_2D/TEST_Cutout/canh01` (11 giây, Lumo vội với tay, khựng lại, bị Piko đè xuống nút); chưa dựng previz 2D cảnh thật nào.
- Review bằng agent (`.claude/skills/review/SKILL.md`): `/review EP001` cho beat sheet, kịch bản; `/review <thư mục cảnh>` cho previz 2D; `/review <thư mục shot>` cho previz khối; `/review <shot>/seedance/prompt.md` trước khi sinh; `/review <file take>` cho take. Kết quả gộp trong chat. Chưa review được cả tập đã ghép.
- Kịch bản tập 01 đã chốt (`03_CONTENT/Scripts/EP001_great_rain_experiment.fountain`), 7 cảnh, qua ba lượt `/review`.
- Chưa có: model 3D của cả bốn nhân vật và đạo cụ.
- **Bước tiếp theo:** dựng previz 2D từng cảnh của tập 01, bắt đầu từ Cảnh 1 (bộ cutout lấy từ `TEST_Cutout`, chuyển sang `pipeline/`), mỗi cảnh xong thì `/review`. Song song: soát take 1 của `TEST_First_Rain` bằng `/review` và ghi kết quả vào `seedance/prompt.md`; làm ảnh concept máy Rain-O-Matic.

## Tài liệu

| File | Nội dung |
|---|---|
| [`01_BRAND/Character_Bible/README.md`](01_BRAND/Character_Bible/README.md) | Nhân vật: tính cách, ngoại hình, màu, chiều cao, bảo bối, cách làm 3D |
| [`03_CONTENT/README.md`](03_CONTENT/README.md) | Hướng nội dung: công thức, 5 series, khung tập 6–8 phút, nhịp cho trẻ em, luật đạo cụ, cách viết kịch bản |
| [`03_CONTENT/PREVIZ_2D.md`](03_CONTENT/PREVIZ_2D.md) | Previz 2D cutout từng cảnh, file mốc thời gian `timing.py` của cảnh, CC |
| [`03_CONTENT/Scripts/EP001_great_rain_experiment.md`](03_CONTENT/Scripts/EP001_great_rain_experiment.md) | Beat sheet tập 01 |
| [`03_CONTENT/Scripts/EP001_great_rain_experiment.fountain`](03_CONTENT/Scripts/EP001_great_rain_experiment.fountain) | Kịch bản tập 01 |
| [`02_ASSET_LIBRARY/README.md`](02_ASSET_LIBRARY/README.md) | Quy ước thư mục asset |
| [`02_ASSET_LIBRARY/MESHY.md`](02_ASSET_LIBRARY/MESHY.md) | Làm nhân vật, đạo cụ bằng Meshy + Blender, prompt |
| [`02_ASSET_LIBRARY/Third_Party/README.md`](02_ASSET_LIBRARY/Third_Party/README.md) | Nguồn asset bên ngoài, giấy phép |
| [`04_PRODUCTION/SEEDANCE.md`](04_PRODUCTION/SEEDANCE.md) | Dựng shot bằng previz Blender + Seedance, prompt theo giây |
| [`pipeline/README.md`](pipeline/README.md) | Code dùng chung, cách render, Blender MCP |
| [`.claude/skills/review/SKILL.md`](.claude/skills/review/SKILL.md) | Skill `/review`: 8 reviewer trong `.claude/agents/` cho kịch bản, previz, prompt Seedance, take và shot; mức độ lỗi, định dạng kết quả |
| [`CLAUDE.md`](CLAUDE.md) | Dặn dò cho agent: file nào sở hữu chủ đề nào, việc review và dọn tài liệu sau mỗi lần làm |

## Cấu trúc thư mục

```
studio/
├── 01_BRAND/                Logo/, Brand_Guideline/ (world_key_art.png), Character_Bible/
├── 02_ASSET_LIBRARY/        Characters/, Props/, Environments/, Materials/, Animation_Library/, Third_Party/
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
- **File gốc tải về không sửa:** file Meshy để trong `source/`, đồ bên thứ ba trong `Third_Party/`.
- **Đặt tên:** thư mục viết hoa chữ đầu, nối bằng gạch dưới (`EP001_Great_Rain_Experiment`, `Wonder_Compass`). File viết thường, không dấu, nối bằng gạch dưới (`lumo_hero.png`); riêng mã tập giữ viết hoa (`EP001_great_rain_experiment.md`). Không dùng dấu tiếng Việt trong tên file vì Blender và ffmpeg hay lỗi đường dẫn.
- **Shot:** `sh010/` gồm `build_shot.py`, `sh010.blend`, `renders/`; shot làm qua Seedance có thêm `seedance/` (`04_PRODUCTION/SEEDANCE.md`). Đánh số cách 10 để còn chèn shot vào giữa.
- **Tài liệu chỉ ghi thông tin hiện hành**, mỗi thông tin chỉ nằm ở một file (bảng file sở hữu và cách giữ tài liệu: `CLAUDE.md`). Lịch sử đã có git.

## Công cụ

| Công cụ | Ghi chú |
|---|---|
| Blender 5.2.3 LTS | `C:\Program Files\Blender Foundation\Blender 5.2`. Render bằng EEVEE vì máy chỉ có card tích hợp Vega 11 |
| Python của Blender | `...\Blender 5.2\5.2\python\bin\python.exe`, có sẵn numpy |
| Meshy (gói Pro) | Sinh hình, Remesh, rig Humanoid, thư viện animation |
| Blender MCP | Cho Claude điều khiển Blender đang mở, xem `pipeline/README.md` |
| Add-on Higgsfield 1.5.60 | Sinh 3D, ảnh, video, animation bằng AI ngay trong viewport (thanh prompt ở đáy 3D view, đăng nhập tài khoản Higgsfield, trừ credit). Cài vào repo `user_default` của Blender 5.2. Tài khoản này cũng dùng để chạy Seedance (`04_PRODUCTION/SEEDANCE.md`) |

## Git

- Repo: https://github.com/billkien-github/cloud-explorers
- File nhị phân (`.blend`, ảnh, video, âm thanh, FBX/GLB, zip) đi qua **Git LFS** (`.gitattributes`).
- Không đưa lên git (`.gitignore`): `*.blend1`, log, cache Python, mọi thư mục `renders/` và `backups/` (bản lưu từng giai đoạn của build script), `06_PUBLISHING/Final_Videos/`.
