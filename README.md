# Cloud Explorers

Phim hoạt hình 3D cho trẻ em, phát hành YouTube-first. Bốn người bạn Lumo, Tavi, Nori, Piko phiêu lưu qua những vùng đất kỳ diệu. Phim dựng bằng **Blender**, phần lớn bằng **code Python** (dựng cảnh, rig, animation, âm thanh). Hình nhân vật sinh bằng **Meshy**.

> Tên dự án theo concept sheet và repo là **Cloud Explorers**. `docs/BRIEF.md` viết trước đó gọi nhóm nhân vật là *The Wonderlings*.

## Đọc trước

1. [`docs/BRIEF.md`](docs/BRIEF.md): định hướng nội dung, 4 nhân vật, kịch bản tập 01, quy tắc tạo hình cho Meshy (mục 3.1)
2. [`01_BRAND/Character_Bible/`](01_BRAND/Character_Bible/README.md): nhân vật theo concept sheet đã chốt, kèm những chỗ còn lệch với quy tắc Meshy
3. [`docs/MESHY_PROMPTS.md`](docs/MESHY_PROMPTS.md): prompt và các bước sinh hình, rig trên Meshy

## Cấu trúc thư mục

```
studio/
├── docs/                    Tài liệu dự án: BRIEF, prompt Meshy, nguồn asset
├── 01_BRAND/
│   ├── Logo/
│   ├── Brand_Guideline/     Ảnh chủ đạo của thế giới (world_key_art.png), sau này: màu, font
│   └── Character_Bible/     Concept sheet 4 nhân vật + mô tả chuẩn
├── 02_ASSET_LIBRARY/        Mọi asset 3D (quy ước trong 02_ASSET_LIBRARY/README.md)
│   ├── Characters/          Lumo, Tavi, Nori, Piko: concept/, source/ (file Meshy), file rig
│   ├── Environments/
│   ├── Props/               4 bảo bối: Wonder_Compass, Inventor_Pack, Story_Lens, Pocket_of_Wonders
│   ├── Materials/           Material, shader dùng chung
│   ├── Animation_Library/   Animation dùng lại được (thư viện Meshy, tự làm)
│   └── Third_Party/         Asset của bên thứ ba, kèm giấy phép (Quaternius CC0)
├── 03_CONTENT/              Scripts/ (kịch bản), Storyboards/, Animatics/
├── 04_PRODUCTION/           Mỗi tập một thư mục: EP001_Great_Rain_Experiment/
├── 05_POST_PRODUCTION/      Editing/, Sound/, Dubbing/ (lồng tiếng Việt, Anh)
├── 06_PUBLISHING/           Thumbnails/, Metadata/ (tiêu đề, mô tả, ghi công), Final_Videos/
├── 07_ANALYTICS/            Monthly_Report/, Annual_Report/
├── pipeline/                Code dùng chung: lablib.py, render.py, run.ps1, âm thanh, tool
└── lab/                     Thử nghiệm đã làm: shot01, shot02 (demo MAX POWER), rig Lumo bằng code
```

Các thư mục đánh số 01–07 theo cấu trúc studio đề xuất ban đầu. `docs/`, `pipeline/`, `lab/` là phần kỹ thuật, không đánh số.

## Quy ước

- **Dựng bằng script:** mỗi asset hay shot có một script build nằm cạnh nó. Muốn sửa thì sửa script rồi build lại. File `.blend` do script tạo ra có thể bị ghi đè, đừng sửa tay trong đó (thử nghiệm bằng tay qua Blender MCP xong thì chép thay đổi vào script).
- **File gốc tải về không sửa:** file từ Meshy để trong `source/`, đồ bên thứ ba để trong `Third_Party/`. Bản đã chỉnh luôn là file mới do code tạo ra.
- **Đặt tên:** thư mục sản xuất viết hoa chữ đầu, nối bằng gạch dưới (`EP001_Great_Rain_Experiment`, `Wonder_Compass`). Tên file viết thường, không dấu, nối bằng gạch dưới (`lumo_hero.png`). Không dùng dấu tiếng Việt trong tên file vì Blender và ffmpeg hay lỗi đường dẫn.
- **Shot:** `04_PRODUCTION/EP001_.../sh010/` gồm `build_shot.py`, `sh010.blend`, `renders/`. Đánh số cách 10 để còn chèn shot vào giữa.
- **Render:** dùng `pipeline/run.ps1` cho mọi shot, ví dụ `.\pipeline\run.ps1 preview -Shot 04_PRODUCTION\EP001_Great_Rain_Experiment\sh010`.

## Công cụ

| Công cụ | Ghi chú |
|---|---|
| Blender 5.2.3 LTS | `C:\Program Files\Blender Foundation\Blender 5.2`, render bằng EEVEE (máy dùng card tích hợp Vega 11) |
| Python của Blender | `...\Blender 5.2\5.2\python\bin\python.exe`, có sẵn numpy, dùng cho script âm thanh |
| Meshy (gói Pro) | Sinh hình nhân vật, Remesh, rig Humanoid, thư viện animation |
| Blender MCP | Cho Claude điều khiển Blender đang mở, xem `pipeline/README.md` |

## Git

- Repo: https://github.com/billkien-github/cloud-explorers
- File nhị phân (`.blend`, ảnh, video, âm thanh, FBX/GLB, zip) đi qua **Git LFS**, danh sách trong `.gitattributes`.
- **Không đưa lên git** (`.gitignore`):
  - File backup `*.blend1`, log, cache Python.
  - `renders/` trong `04_PRODUCTION/` và `06_PUBLISHING/Final_Videos/`: tạo lại được, lại rất nặng. Video thành phẩm lưu ở ổ riêng hoặc cloud.
  - Pack Quaternius trong `Third_Party/quaternius/`: tải lại theo `02_ASSET_LIBRARY/Third_Party/README.md`. Chỉ giữ ảnh xem trước. Muốn build lại shot02 phải tải pack về trước.

## Chuyển thư mục ngày 01/11/2026

| Trước | Sau |
|---|---|
| `wonderlings/*.md` | `docs/` |
| `docs/` (ảnh ChatGPT) | Ảnh nhân vật vào `02_ASSET_LIBRARY/Characters/<Tên>/concept/`, bảo bối vào `02_ASSET_LIBRARY/Props/<Tên>/concept/`, concept sheet vào `01_BRAND/Character_Bible/`, ảnh thế giới vào `01_BRAND/Brand_Guideline/` |
| `assets/quaternius/`, `assets/README.md` | `02_ASSET_LIBRARY/Third_Party/` |
| `assets/make_previews.py` | `pipeline/tools/` |
| `lab/lablib.py`, `render.py`, `mux_audio.py`, `run.ps1`, `sound/` | `pipeline/` |
| `lab/shot01_dawn`, `shot02_max_power`, `char_lumo` | Giữ nguyên trong `lab/` |
