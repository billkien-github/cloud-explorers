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

- Có: concept 4 nhân vật, 4 bảo bối, ảnh thế giới; ảnh tham chiếu dựng model đã đủ bộ của bốn nhân vật chính Lumo, Tavi, Nori, Piko (thân A-pose, T-pose, bản đủ đồ, nhìn trước và sau; đuôi, cánh) và sinh vật nhỏ, bốn bảo bối (nhìn trước và sau), cùng mọi đạo cụ và nhân vật phụ tập 01 (máy Rain-O-Matic, thuyền, cầu ván, đôi voi con, Noah, thú trên boong…). Chưa dựng model nào trong Blender. Ảnh xoay (trước và sau trong một ảnh) của bốn nhân vật chính là ảnh tham chiếu nhân vật cho Seedance, chưa thử trong take nào. Danh sách và prompt ChatGPT trong `02_ASSET_LIBRARY/MODELING.md`; beat sheet tập 01 đã chốt (khoảng 7 phút); code dùng chung trong `pipeline/`.
- Quy trình làm một tập: kịch bản → ảnh của tập (chỉ ảnh Seedance cần) → previz 2D từng cảnh có CC → previz khối có CC → Seedance (`03_CONTENT/README.md`, mục "Làm một tập"). Công cụ cho từng bước (bộ cutout 2D, bộ khối 3D, in CC, ghép video): `pipeline/README.md`.
- Previz 2D tập 01 (`03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/`, có CC): Cảnh 1 (`canh01`, khoảng 55 giây, 14 cú máy) đã sửa theo năm lượt review (từ lượt ba không còn lỗi Chặn); các diễn biến previz thêm vào đã ghi vào kịch bản. Cảnh 2 (`canh02`, khoảng 87 giây, 27 cú máy: montage lắp máy, bánh răng vàng, ròng rọc và Story Lens, Wonder Hub, nút đỏ) đã sửa theo lượt review đầu (có một lỗi Chặn: cần gạt TẮT bị che), chờ review lại; trước khi review lại, đổi cú S10 Tavi giơ tay kéo kính thành gật đầu cho kính trượt xuống, hất đầu cho kính bật lên (tay Tavi không với tới kính: Character Bible, "Giới hạn khi diễn"; sửa `build_shot.py`, CC trong `timing.py`, render lại). Cảnh 3–7 chưa dựng.
- Previz khối và Seedance tập 01: chưa có; làm lại theo quy trình, mỗi cảnh sau khi previz 2D của cảnh đã chốt. Bài học từ take thử Cảnh 1 đã ghi trong `04_PRODUCTION/SEEDANCE.md`. Sinh qua API bằng `pipeline/seedance_gen.py` (đoạn tối đa 9 ảnh tham chiếu dùng dòng Seedance 2.0, dài tối đa 15 giây, chạy bản mini trước, chưa đạt thì fast rồi 2.0; nhiều hơn dùng 2.5, đoạn 30 giây; 16:9, 720p, ghi chi phí vào `04_PRODUCTION/seedance_log.csv`): đã chạy thật lần đầu ngày 07/11/2026 trên shot thử 4 giây (Seedance 2.0 mini, 480p, $0.17): tải video lên Cloudflare R2, sinh, tải take về, ghi log, xoá file trên R2 đều chạy, mất khoảng 2 phút. Ảnh tham chiếu sinh bằng ChatGPT (prompt trong `04_PRODUCTION/SEEDANCE.md`): bối cảnh Thung lũng Mây khô hạn, Piko đeo Pocket of Wonders, sinh vật nhỏ của thung lũng.
- Review bằng agent: `/review` cho beat sheet, kịch bản, previz 2D, previz khối, prompt Seedance và take (cách chạy: `.claude/skills/review/SKILL.md`). Chưa review được cả tập đã ghép.
- Kịch bản tập 01 đã chốt (`03_CONTENT/Scripts/EP001_great_rain_experiment.fountain`), 7 cảnh, qua ba lượt `/review`.
- Season 0 (khung 5 tập, Wonder Hub và Chronicle Engine: `03_CONTENT/README.md`): beat sheet và kịch bản EP000A (tập Lumo, `03_CONTENT/Scripts/EP000A_mysterious_compass.md`, `.fountain`) đã chốt sau sáu lượt `/review`, các diễn biến previz 2D thêm vào và thời lượng đo được đã ghi vào kịch bản, beat sheet; ảnh của tập đã sinh và soát đủ (`02_ASSET_LIBRARY/MODELING.md`, mục "Tập 000A"). EP000B (tập Tavi, `03_CONTENT/Scripts/EP000B_impossible_invention.md`, `.fountain`): bản nháp 3 của beat sheet và kịch bản, chuyển từ bản nháp ChatGPT, đã sửa Chặn và Nên sửa của hai lượt `/review`, chờ lượt xác nhận; cách Inventor Pack hoạt động đã ghi vào Character Bible. Beat sheet và kịch bản EP000C (tập Nori, `03_CONTENT/Scripts/EP000C_forgotten_story.md`, `.fountain`) chuyển từ bản nháp ChatGPT, đã qua ba lượt `/review`; luật Story Lens, quyển sách nhỏ, sách bay đã ghi vào Character Bible, tín hiệu nối bốn tập và bốn biểu tượng vào `03_CONTENT/README.md`. EP000D, E chưa đưa vào repo: mỗi tập viết beat sheet trước rồi mới viết Fountain; post-credit EP000B nên khớp mục "Nối với EP000B" trong beat sheet EP000C; khi viết EP000E phải theo đoạn kết bánh răng vàng và cánh cửa bốn hốc đã chốt, và soát lại bản vẽ phác Chronicle Engine ở Cảnh 5 EP000B.
- Previz 2D EP000A (`03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/`, có CC): Cảnh 1 (`canh01`, 48.6 giây, 14 cú máy: bản đồ cầm ngược, vấp hòn đá ngã vào bụi gai, tên phim, chú chim cười, dốc lá khô, bướm và ánh vàng ở phế tích) đã khoá sau một lượt `/review`; sau đó đổi gag bụi gai thành vấp hòn đá ngã vào (theo người dùng), chưa review lại. Cảnh 2 (`canh02`, 44.8 giây, 10 cú máy), Cảnh 3 (`canh03`, 74.9 giây, 14 cú máy), Cảnh 4 (`canh04`, 84.8 giây, 25 cú máy), Cảnh 5 (`canh05`, 58.5 giây, 18 cú máy) và post-credit (`canh06`, 5 giây) đã dựng và qua một lượt `/review` (story, character, audience, pacing): đã sửa hết Chặn và Nên sửa, Cảnh 3 qua thêm lượt xác nhận; Gợi ý còn chờ người dùng chọn. Cả tập khoảng 5:17.
- Previz khối EP000A Cảnh 1 (`04_PRODUCTION/EP000A_Mysterious_Compass/`): bối cảnh và diễn cả cảnh trong `canh01_blocks.py`, chia hai đoạn sinh Seedance 2.5, nối ở 21.9 giây (sau cú toàn đường rừng, trước cú cận chú chim): `sh010` (S1–S8, 23 giây), `sh020` (S9–S14, 28 giây), mỗi đoạn 6 ảnh tham chiếu. Đã render `ref`, có `seedance/prompt.md` (qua `check_prompt.py`, chưa `/review` prompt). `sh010/seedance/takes/` còn sáu take thử của cách chia cũ (đoạn 14 giây) để so model. Bối cảnh rừng mây và phế tích dùng chung giữa các cảnh nằm ở `ruins_blocks.py`.
- Previz khối EP000A Cảnh 2 (`canh02_blocks.py`): đã dựng, chưa `/review`; hai đoạn Seedance 2.5 nối ở 23.0 giây (hết cú nhìn la bàn chỉ về bức tường, trước cú đi vòng qua phiến đá): `sh030` (S1–S5, 24 giây), `sh040` (S6–S10, 23 giây). Đã render `preview` có CC và `ref`; chưa có `seedance/prompt.md`.
- Previz khối EP000A Cảnh 3 (`canh03_blocks.py`): đã dựng, chưa `/review`; ba đoạn Seedance 2.5 nối ở 26.0 và 49.2 giây: `sh050` (S1–S6, 26 giây, sinh 27 giây), `sh060` (S7–S10, 23.2 giây, sinh 24 giây), `sh070` (S11–S14, 25.7 giây, sinh 27 giây). Đã render `preview` có CC và `ref`; chưa có prompt.
- Previz khối EP000A Cảnh 4 (`canh04_blocks.py`): đã dựng, chưa `/review`; bốn đoạn Seedance 2.5 nối ở 14.8, 38.6, 61.6 giây (sau cận la bàn chỉ ngôi sao đá; sau cận la bàn "vẫn chỉ"; sau cú lộ bản đồ khắc; tránh hai chỗ giữa cầu kêu, cầu sập và cú túm dây leo): `sh080` (S1–S4, 16 giây), `sh090` (S5–S11, 25 giây), `sh100` (S12–S19, 24 giây), `sh110` (S20–S25, 24 giây). Đã render `preview` có CC và `ref`; chưa có prompt.
- Previz khối EP000A Cảnh 5 (`canh05_blocks.py`): đã dựng, chưa `/review`; ba đoạn: `sh120` (S1–S7, 27 giây), `sh130` (S8–S11, 16 giây, nối sau "Được rồi, bạn la bàn."), `sh140` (S12–S18, 18 giây, nối sau khi cất bản đồ). Đã render `preview` có CC và `ref`; chưa có prompt.
- Previz khối EP000A post-credit (`canh06_blocks.py`): đã dựng, chưa `/review`; một đoạn `sh150` (5 giây, sinh 6 giây, 3 ảnh tham chiếu: bãi phế liệu, hòn đảo có Wonder Hub, Inventor Pack); hòn đảo và Inventor Pack lóe xanh ngọc cùng nhịp. Đã render `ref`; chưa có prompt.
- Chưa có: model 3D của cả bốn nhân vật và đạo cụ.
- **Bước tiếp theo:** review lại Cảnh 2 và Cảnh 1, chốt hai cảnh, rồi dựng previz khối và sinh Seedance cho từng cảnh đã chốt (`04_PRODUCTION/SEEDANCE.md`); dựng previz 2D Cảnh 3–7, mỗi cảnh xong thì `/review`. Cái máy Rain-O-Matic đang dựng trong `build_shot.py` của Cảnh 2: dựng Cảnh 3 thì chuyển nó sang `pipeline/` để dùng chung. EP000A: Cảnh 1 dùng tạm bản nháp `sh010` take08 và `sh020` take02 (người dùng chấp nhận; lỗi còn lại ở mục Take của từng `prompt.md`, sửa sau nếu cần: cú xoay bản đồ, chỏm lông Lumo, ánh vàng và nhạc làm ở hậu kỳ); còn: cú xoay bản đồ (ghép ở hậu kỳ hoặc sinh riêng), ảnh cận đầu Lumo cho chỏm lông, ánh vàng và nhạc làm ở hậu kỳ, sửa nốt prompt và previz rồi sinh lại bản nháp (Seedance 2.5, 480p; bản final đang bị chặn), dựng Cảnh 1 bằng bản nháp; chọn các Gợi ý còn lại của previz 2D Cảnh 2–5, khoá các cảnh đó, rồi dựng previz khối. EP000C: người dùng duyệt kịch bản, rồi làm ảnh của tập (thêm mục "Tập 000C" vào `02_ASSET_LIBRARY/MODELING.md` theo mục "Ảnh cho một tập") và previz 2D. EP000B: `/review` beat sheet và kịch bản, sửa rồi khoá, sau đó lập bảng ảnh của tập.
## Tài liệu

| File | Nội dung |
|---|---|
| [`01_BRAND/Character_Bible/README.md`](01_BRAND/Character_Bible/README.md) | Nhân vật: tính cách, ngoại hình, màu, chiều cao, bảo bối, giới hạn khi diễn |
| [`03_CONTENT/README.md`](03_CONTENT/README.md) | Hướng nội dung: công thức, Wonder Hub và Chronicle Engine, Season 0, 5 series, khung tập 6–8 phút, nhịp cho trẻ em, luật đạo cụ, các bước làm một tập, cách viết kịch bản |
| [`03_CONTENT/PREVIZ_2D.md`](03_CONTENT/PREVIZ_2D.md) | Previz 2D cutout từng cảnh, file mốc thời gian `timing.py` của cảnh, CC |
| [`03_CONTENT/Scripts/EP001_great_rain_experiment.md`](03_CONTENT/Scripts/EP001_great_rain_experiment.md) | Beat sheet tập 01 |
| [`03_CONTENT/Scripts/EP001_great_rain_experiment.fountain`](03_CONTENT/Scripts/EP001_great_rain_experiment.fountain) | Kịch bản tập 01 |
| [`03_CONTENT/Scripts/EP000A_mysterious_compass.md`](03_CONTENT/Scripts/EP000A_mysterious_compass.md) | Beat sheet Season 0, tập Lumo |
| [`03_CONTENT/Scripts/EP000A_mysterious_compass.fountain`](03_CONTENT/Scripts/EP000A_mysterious_compass.fountain) | Kịch bản Season 0, tập Lumo |
| [`03_CONTENT/Scripts/EP000B_impossible_invention.md`](03_CONTENT/Scripts/EP000B_impossible_invention.md) | Beat sheet Season 0, tập Tavi |
| [`03_CONTENT/Scripts/EP000B_impossible_invention.fountain`](03_CONTENT/Scripts/EP000B_impossible_invention.fountain) | Kịch bản Season 0, tập Tavi |
| [`03_CONTENT/Scripts/EP000C_forgotten_story.md`](03_CONTENT/Scripts/EP000C_forgotten_story.md) | Beat sheet Season 0, tập Nori |
| [`03_CONTENT/Scripts/EP000C_forgotten_story.fountain`](03_CONTENT/Scripts/EP000C_forgotten_story.fountain) | Kịch bản Season 0, tập Nori |
| [`02_ASSET_LIBRARY/README.md`](02_ASSET_LIBRARY/README.md) | Quy ước thư mục asset |
| [`02_ASSET_LIBRARY/MODELING.md`](02_ASSET_LIBRARY/MODELING.md) | Ảnh tham chiếu và model 3D: ảnh của từng tập cho Seedance, bộ ảnh dựng model, prompt ChatGPT và cách sinh, dựng và rig trong Blender |
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
├── 04_PRODUCTION/           Mỗi tập một thư mục, mỗi shot một thư mục con: EP001_Great_Rain_Experiment/sh010/; clip thử: TEST_<tên>/; seedance_log.csv: chi phí từng lần sinh Seedance
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
| ChatGPT | Sinh ảnh: ảnh của từng tập, ảnh dựng model (`02_ASSET_LIBRARY/MODELING.md`), ảnh bối cảnh cho Seedance (`04_PRODUCTION/SEEDANCE.md`) |
| Seedance (BytePlus ModelArk) | Sinh hình cuối của shot từ previz Blender, gọi API bằng `pipeline/seedance_gen.py` (`04_PRODUCTION/SEEDANCE.md`). Cần biến môi trường `ARK_API_KEY` và một bucket Cloudflare R2 để đưa video tham chiếu cho ModelArk |
| Blender MCP | Cho Claude điều khiển Blender đang mở, xem `pipeline/README.md` |

## Git

- Repo: https://github.com/billkien-github/cloud-explorers
- File nhị phân (`.blend`, ảnh, video, âm thanh, FBX/GLB, zip) đi qua **Git LFS** (`.gitattributes`).
- Không đưa lên git (`.gitignore`): `*.blend1`, log, cache Python, mọi thư mục `renders/` và `backups/` (bản lưu từng giai đoạn của build script), take Seedance trong `seedance/takes/` của mỗi shot (sinh lại được từ `prompt.md`, chi phí ghi ở `04_PRODUCTION/seedance_log.csv`), `06_PUBLISHING/Final_Videos/`.
