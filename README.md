# Cloud Explorers

Phim hoạt hình 3D cho trẻ em, phát hành YouTube-first. Bốn người bạn Lumo, Tavi, Nori, Piko phiêu lưu qua những vùng đất kỳ diệu. Phim dựng bằng **Blender**, phần lớn bằng **code Python** (dựng cảnh, rig, animation, âm thanh). Hình nhân vật sinh bằng **Meshy**.

## Đọc trước

1. [`docs/BRIEF.md`](docs/BRIEF.md): định hướng nội dung, 4 nhân vật, kịch bản tập 01
2. [`01_BRAND/Character_Bible/`](01_BRAND/Character_Bible/README.md): hình dáng nhân vật theo concept sheet, bảo bối, **việc cần chốt**
3. [`docs/MESHY.md`](docs/MESHY.md): cách làm nhân vật 3D bằng Meshy + Blender, prompt
4. [`docs/ASSET_SOURCES.md`](docs/ASSET_SOURCES.md): nguồn asset bên ngoài và giấy phép

## Trạng thái (01/11/2026)

- Đã có: concept 4 nhân vật, 4 bảo bối, ảnh thế giới. Code dùng chung trong `pipeline/` (render, âm thanh, face rig, sửa da, kiểm tra rig).
- Chưa có: model 3D nào. Bước tiếp theo là sinh Lumo trên Meshy (gói Pro) để thử rig.
- Cần chốt: Nori và Piko có chân hay không (xem Character Bible).

## Cấu trúc thư mục

```
studio/
├── docs/                    Tài liệu dự án: BRIEF, Meshy, nguồn asset
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
│   └── Third_Party/         Asset của bên thứ ba, kèm giấy phép
├── 03_CONTENT/              Scripts/ (kịch bản), Storyboards/, Animatics/
├── 04_PRODUCTION/           Mỗi tập một thư mục: EP001_Great_Rain_Experiment/
├── 05_POST_PRODUCTION/      Editing/, Sound/, Dubbing/ (lồng tiếng Việt, Anh)
├── 06_PUBLISHING/           Thumbnails/, Metadata/ (tiêu đề, mô tả, ghi công), Final_Videos/
├── 07_ANALYTICS/            Monthly_Report/, Annual_Report/
└── pipeline/                Code dùng chung (xem pipeline/README.md)
```

## Quy ước

- **Dựng bằng script:** mỗi asset hay shot có một script build nằm cạnh nó. Muốn sửa thì sửa script rồi build lại. File `.blend` do script tạo ra có thể bị ghi đè, đừng sửa tay trong đó (thử bằng tay qua Blender MCP xong thì chép thay đổi vào script).
- **File gốc tải về không sửa:** file từ Meshy để trong `source/`, đồ bên thứ ba để trong `Third_Party/`. Bản đã chỉnh luôn là file mới do code tạo ra.
- **Đặt tên:** thư mục sản xuất viết hoa chữ đầu, nối bằng gạch dưới (`EP001_Great_Rain_Experiment`, `Wonder_Compass`). Tên file viết thường, không dấu, nối bằng gạch dưới (`lumo_hero.png`). Không dùng dấu tiếng Việt trong tên file vì Blender và ffmpeg hay lỗi đường dẫn.
- **Shot:** `04_PRODUCTION/EP001_.../sh010/` gồm `build_shot.py`, `sh010.blend`, `renders/`. Đánh số cách 10 để còn chèn shot vào giữa.
- **Tài liệu chỉ ghi thông tin hiện hành.** Khi một quyết định thay đổi thì sửa thẳng vào tài liệu, không giữ bản cũ hay ghi chú lịch sử. Lịch sử đã có git.

## Công cụ

| Công cụ | Ghi chú |
|---|---|
| Blender 5.2.3 LTS | `C:\Program Files\Blender Foundation\Blender 5.2`. Render bằng EEVEE, vì máy chỉ có card tích hợp Vega 11 (Cycles quá chậm) |
| Python của Blender | `...\Blender 5.2\5.2\python\bin\python.exe`, có sẵn numpy, dùng cho script âm thanh |
| Meshy (gói Pro) | Sinh hình nhân vật, Remesh, rig Humanoid, thư viện animation |
| Blender MCP | Cho Claude điều khiển Blender đang mở, xem `pipeline/README.md` |

## Git

- Repo: https://github.com/billkien-github/cloud-explorers
- File nhị phân (`.blend`, ảnh, video, âm thanh, FBX/GLB, zip) đi qua **Git LFS**, danh sách trong `.gitattributes`.
- Không đưa lên git (`.gitignore`): file backup `*.blend1`, log, cache Python, `renders/` của các shot, `06_PUBLISHING/Final_Videos/`. Render tạo lại được, video thành phẩm lưu ở ổ riêng hoặc cloud.
