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

### Chung

- **Asset:** concept 4 nhân vật, 4 bảo bối, ảnh thế giới, ảnh xếp hàng bốn nhân vật đúng chiều cao (`01_BRAND/Character_Bible/cast_lineup.png`). Ảnh tham chiếu dựng model đủ bộ của Lumo, Tavi, Nori, Piko (thân A-pose, T-pose, bản đủ đồ, nhìn trước và sau; đuôi, cánh), sinh vật nhỏ và bốn bảo bối (nhìn trước và sau). Ảnh xoay (trước và sau trong một ảnh) của bốn nhân vật chính là ảnh tham chiếu nhân vật cho Seedance; ảnh cận đầu Lumo (`lumo_head_ref.png`) giữ chỏm lông. Bảng cỡ mọi món và ảnh đã soát cỡ: `02_ASSET_LIBRARY/MODELING.md`, mục "Bảng cỡ" (ảnh còn lệch nhẹ ghi ở "Ảnh lệch cỡ so với bảng"). Chưa dựng model 3D nào trong Blender.
- **Quy trình làm một tập:** kịch bản → ảnh của tập (chỉ ảnh Seedance cần) → previz 2D từng cảnh có CC → previz khối có CC → Seedance (`03_CONTENT/README.md`, mục "Làm một tập"). Công cụ cho từng bước (bộ cutout 2D, bộ khối 3D, in CC, ghép video): `pipeline/README.md`.
- **Review bằng agent:** `/review` cho beat sheet, kịch bản, previz 2D, previz khối, prompt Seedance và take (`.claude/skills/review/SKILL.md`); `/revise-script` sửa kịch bản theo kết quả review. Chưa review được cả tập đã ghép.
- **Seedance:** sinh qua API bằng `pipeline/seedance_gen.py`: chỉ bản nháp Seedance 2.5 480p, đoạn tối đa 30 giây, ghi chi phí vào `04_PRODUCTION/seedance_log.csv`; bản final đang bị chặn (`04_PRODUCTION/SEEDANCE.md`, mục "Sinh qua API"). Đã chạy thật từ ngày 07/11/2026.

### Season 0 (khung 5 tập, Wonder Hub và Chronicle Engine: `03_CONTENT/README.md`)

- **EP000A** (tập Lumo, `03_CONTENT/Scripts/EP000A_mysterious_compass.md`, `.fountain`): beat sheet và kịch bản đã chốt sau sáu lượt `/review`, các diễn biến previz 2D thêm vào và thời lượng đo được đã ghi vào kịch bản, beat sheet. Ảnh của tập đã sinh và soát đủ (`02_ASSET_LIBRARY/MODELING.md`, mục "Tập 000A").
  - Previz 2D (`03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/`, có CC), cả tập khoảng 5:17: Cảnh 1 (`scene01`, 48.6 giây, 14 cú máy) đã khoá sau một lượt `/review`, sau đó đổi gag bụi gai thành vấp hòn đá ngã vào (theo người dùng), chưa review lại. Cảnh 2 (`scene02`, 44.8 giây, 10 cú máy), Cảnh 3 (`scene03`, 74.9 giây, 14 cú máy), Cảnh 4 (`scene04`, 84.8 giây, 25 cú máy), Cảnh 5 (`scene05`, 59.3 giây, 18 cú máy) và post-credit (`scene06`, 5 giây) đã qua một lượt `/review` (story, character, audience, pacing), đã sửa hết Chặn và Nên sửa; Cảnh 3 qua thêm lượt xác nhận; Gợi ý chờ người dùng chọn.
  - Previz khối (`04_PRODUCTION/EP000A_Mysterious_Compass/`): mỗi cảnh một `sceneNN_blocks.py`; bối cảnh rừng mây và phế tích dùng chung ở `ruins_blocks.py`, hòn đảo có Wonder Hub ở `island_blocks.py`.
    - Cảnh 1: hai đoạn Seedance 2.5 nối ở 21.9 giây: `sh010` (S1–S8, sinh 23 giây, 6 ảnh tham chiếu), `sh020` (S9–S14, sinh 28 giây, 7 ảnh tham chiếu). Bản nháp đang dùng tạm: `sh010` take08, `sh020` take02. Review lại take ngày 07/11/2026 (đủ sáu reviewer, soát cỡ theo Bảng cỡ): `sh010` còn lỗi Chặn hai rương trên bản đồ; chỏm lông thành nơ hồng ở cả hai đoạn; chim, bướm, ánh vàng to hơn Bảng cỡ; `sh020` lùi máy làm tường phế tích che sườn dốc. Đã sửa previz (chim, bướm dẫn mắt, ánh vàng nhỏ lại), prompt (một ảnh bản đồ, ảnh cận đầu Lumo, cỡ so với bộ phận trong khung, bố cục phế tích, mốc giữa cho hai cú máy dồn) và render lại `ref`; chưa sinh lại. `sh010/seedance/takes/` còn sáu take thử của cách chia cũ để so model.
    - Cảnh 2 (`scene02_blocks.py`): đã khoá sau `/review` lượt 2; hai đoạn nối ở 23.0 giây: `sh030` (S1–S5, 24 giây), `sh040` (S6–S10, 23 giây). Đã dựng lại `.blend` sau khi ánh vàng dùng chung nhỏ lại; `preview` có CC và `ref` cần render lại. Chưa có `seedance/prompt.md`.
    - Cảnh 3 (`scene03_blocks.py`): đã khoá sau `/review` lượt 2; ba đoạn nối ở 29.4 và 46.4 giây: `sh050` (S1–S7, sinh 30 giây), `sh060` (S8–S9, sinh 18 giây), `sh070` (S10–S14, sinh 29 giây). Dây leo rủ dài hơn Cảnh 2 để che kín phù điêu (prompt `sh050` phải tả). Đã render `preview` có CC và `ref`; chưa có prompt.
    - Cảnh 4 (`scene04_blocks.py`): đã khoá sau `/review` lượt 2. Giữ bốn đoạn dù `split_segments.py` tính ra ít nhất ba (lý do trong docstring): nối ở 14.8, 38.6, 61.6 giây: `sh080` (S1–S4, 16 giây), `sh090` (S5–S11, 25 giây), `sh100` (S12–S19, 24 giây), `sh110` (S20–S25, 24 giây). La bàn ở Cảnh 4 không lóe xanh ngọc (luật "Tín hiệu nối bốn tập" trong `03_CONTENT/README.md`). Đã render `preview` có CC và `ref`; chưa có prompt.
    - Cảnh 5 (`scene05_blocks.py`): đã khoá sau `/review` lượt 2; ba đoạn: `sh120` (S1–S7, 27 giây), `sh130` (S8–S11, 16 giây), `sh140` (S12–S18, sinh 19 giây). Đã render `preview` có CC và `ref`; chưa có prompt.
    - Post-credit (`scene06_blocks.py`): qua `/review` lượt 1, chỉ còn Gợi ý; một đoạn `sh150` (sinh 6 giây, 3 ảnh tham chiếu: bãi phế liệu, hòn đảo có Wonder Hub, Inventor Pack; hòn đảo và Inventor Pack lóe xanh ngọc cùng nhịp). Đã render `ref`; chưa có prompt.
- **EP000B** (tập Tavi, `03_CONTENT/Scripts/EP000B_impossible_invention.md`, `.fountain`): beat sheet và kịch bản chuyển từ bản nháp ChatGPT, đã khoá sau bốn lượt `/review`; cách Inventor Pack hoạt động đã ghi vào Character Bible. Sáu ảnh của tập đã sinh và soát, máy phân loại và bản vẽ đã sinh lại cho đúng tầm với (`02_ASSET_LIBRARY/MODELING.md`, mục "Tập 000B").
- **EP000C** (tập Nori, `03_CONTENT/Scripts/EP000C_forgotten_story.md`, `.fountain`): beat sheet và kịch bản chuyển từ bản nháp ChatGPT, đã chốt sau bốn lượt `/review`. Tám ảnh của tập đã sinh và soát (mục "Tập 000C"; quyển sách nhỏ có ảnh xoay). Luật Story Lens, quyển sách nhỏ, sách bay và tầm với của Nori đã ghi vào Character Bible; tín hiệu nối bốn tập và bốn biểu tượng vào `03_CONTENT/README.md`. Post-credit EP000B nên khớp mục "Nối với EP000B" trong beat sheet EP000C.
- **EP000D** (tập Piko, `03_CONTENT/Scripts/EP000D_magic_pocket.md`, `.fountain`): beat sheet và kịch bản đã khoá sau ba lượt `/review`; cách Pocket of Wonders hoạt động, giới hạn khi diễn của Piko, bà Gấu và cá mây đã ghi vào Character Bible. Ảnh của tập đã lập bảng (11 ảnh) và viết prompt, chưa sinh (mục "Tập 000D").
- **EP000E** (tập kết Season 0, khoảng 5:30, `03_CONTENT/Scripts/EP000E_chronicle_engine.md`, `.fountain`): beat sheet chuyển từ bản nháp ChatGPT, rút từ 9 phút còn 5–6 phút theo người dùng; beat sheet và kịch bản đã khoá sau bốn lượt `/review` và hai lượt xác nhận (sửa bằng `/revise-script`); độ dài đo lại ở previz 2D, quá 6 phút thì cắt tiếp. Dáng Chronicle Engine, cánh cửa bốn múi và cổng truyện đã chốt ở `03_CONTENT/README.md` (bản phác ở Cảnh 5 EP000B khớp).

### Tập 01

- Beat sheet (khoảng 7 phút) và kịch bản (`03_CONTENT/Scripts/EP001_great_rain_experiment.md`, `.fountain`, 7 cảnh) đã chốt qua ba lượt `/review`. Còn hai dòng "Piko ôm chặt con vịt" trái giới hạn khi diễn của Piko (tay không gặp nhau trước bụng), chờ người dùng quyết sửa.
- Ảnh: mọi đạo cụ và nhân vật phụ (máy Rain-O-Matic, thuyền, cầu ván, đôi voi con, Noah, thú trên boong…); máy Rain-O-Matic đã sinh lại cho nút đỏ ngang ngực Lumo. Ảnh bối cảnh sinh bằng ChatGPT (prompt trong `04_PRODUCTION/SEEDANCE.md`): Thung lũng Mây khô hạn, Piko đeo Pocket of Wonders, sinh vật nhỏ của thung lũng.
- Previz 2D (`03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/`, có CC): Cảnh 1 (`scene01`, khoảng 55 giây, 14 cú máy) đã sửa theo năm lượt review (từ lượt ba không còn Chặn); các diễn biến previz thêm vào đã ghi vào kịch bản. Cảnh 2 (`scene02`, khoảng 87 giây, 27 cú máy) đã sửa theo lượt review đầu (có một Chặn: cần gạt TẮT bị che), chờ review lại; trước đó đổi cú S10 Tavi giơ tay kéo kính thành gật đầu cho kính trượt xuống, hất đầu cho kính bật lên (sửa `build_shot.py`, CC trong `timing.py`, render lại). Cảnh 3–7 chưa dựng.
- Previz khối và Seedance: chưa có; làm theo quy trình, mỗi cảnh sau khi previz 2D của cảnh đã chốt. Bài học từ take thử Cảnh 1 đã ghi trong `04_PRODUCTION/SEEDANCE.md`.

### Bước tiếp theo

- **EP000A:** sinh lại bản nháp Cảnh 1 (`sh010`, `sh020`, Seedance 2.5 480p, khoảng $6.3, chờ người dùng đồng ý), review take, dựng Cảnh 1; mặt bản đồ sau cú xoay, ánh vàng và nhạc làm ở hậu kỳ. Render lại `preview` có CC và `ref` của `sh030`, `sh040`. Chọn Gợi ý còn lại của previz 2D Cảnh 2–5 và previz khối Cảnh 2–5, post-credit; viết `seedance/prompt.md` từng đoạn (`sh030`–`sh150`).
- **EP000B:** previz 2D (ảnh của tập đã đủ); đo nhịp Cảnh 3 và độ dài Cảnh 4 ở previz 2D.
- **EP000C:** previz 2D (ảnh của tập đã đủ; ban công: bóng lan can trong ảnh đổ về phía máy, ánh sáng hoàng hôn sau lưng máy làm theo kịch bản ở previz và prompt Seedance).
- **EP000D:** sinh 11 ảnh của tập theo thứ tự bảng "Tập 000D" trong `02_ASSET_LIBRARY/MODELING.md` (khu chợ giữ dáng `floating_market_hero.png`), soát từng ảnh, rồi previz 2D. Cỡ từng món: "Bảng cỡ", mục "Cỡ tập 000D".
- **EP000E:** lập bảng cỡ và bảng ảnh "Tập 000E" trong `02_ASSET_LIBRARY/MODELING.md`, viết prompt, sinh và soát ảnh, rồi previz 2D.
- **Tập 01:** review lại previz 2D Cảnh 2 và Cảnh 1, chốt hai cảnh, rồi previz khối và Seedance từng cảnh đã chốt; dựng previz 2D Cảnh 3–7, mỗi cảnh xong thì `/review`. Cái máy Rain-O-Matic đang dựng trong `build_shot.py` của Cảnh 2: dựng Cảnh 3 thì chuyển nó sang `pipeline/` để dùng chung.

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
| [`03_CONTENT/Scripts/EP000D_magic_pocket.md`](03_CONTENT/Scripts/EP000D_magic_pocket.md) | Beat sheet Season 0, tập Piko |
| [`03_CONTENT/Scripts/EP000D_magic_pocket.fountain`](03_CONTENT/Scripts/EP000D_magic_pocket.fountain) | Kịch bản Season 0, tập Piko |
| [`03_CONTENT/Scripts/EP000E_chronicle_engine.md`](03_CONTENT/Scripts/EP000E_chronicle_engine.md) | Beat sheet Season 0, tập kết (Cỗ Máy Biên Niên) |
| [`03_CONTENT/Scripts/EP000E_chronicle_engine.fountain`](03_CONTENT/Scripts/EP000E_chronicle_engine.fountain) | Kịch bản Season 0, tập kết |
| [`02_ASSET_LIBRARY/README.md`](02_ASSET_LIBRARY/README.md) | Quy ước thư mục asset |
| [`02_ASSET_LIBRARY/MODELING.md`](02_ASSET_LIBRARY/MODELING.md) | Bảng cỡ mọi nhân vật phụ, đạo cụ, bối cảnh; ảnh tham chiếu và model 3D: ảnh của từng tập cho Seedance, bộ ảnh dựng model, prompt ChatGPT và cách sinh, dựng và rig trong Blender |
| [`04_PRODUCTION/SEEDANCE.md`](04_PRODUCTION/SEEDANCE.md) | Dựng shot bằng previz Blender + Seedance, prompt theo giây |
| [`pipeline/README.md`](pipeline/README.md) | Code dùng chung, cách render, Blender MCP |
| [`.claude/skills/review/SKILL.md`](.claude/skills/review/SKILL.md) | Skill `/review`: 8 reviewer trong `.claude/agents/` cho kịch bản, previz, prompt Seedance, take và shot; mức độ lỗi, định dạng kết quả |
| [`.claude/skills/revise-script/SKILL.md`](.claude/skills/revise-script/SKILL.md) | Skill `/revise-script`: sửa beat sheet và Fountain theo kết quả review, tự soát, chuẩn bị lượt review lại |
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
└── .claude/                 agents/ (các reviewer), skills/review/ (skill /review), skills/revise-script/ (skill /revise-script)
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
