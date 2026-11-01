# Asset Library

## Quy ước cho mỗi asset

Mỗi nhân vật, đạo cụ hay bối cảnh có một thư mục riêng:

```
Characters/Lumo/
├── concept/          Ảnh 2D: ảnh chính diện, turnaround, ảnh A-pose đưa vào Meshy Image to 3D
├── source/           File gốc tải từ Meshy (FBX/GLB + animation). Không sửa, chỉ thêm bản mới
├── build_lumo.py     Script: import source, thêm xương, face rig, material -> lumo_rig.blend
├── lumo_rig.blend    File đã rig, do script tạo ra (dùng trong shot)
└── qa/               Ảnh kiểm tra tư thế, biểu cảm, số liệu độ méo
```

- File Meshy mới tải về thì tăng số phiên bản (`lumo_meshy_v02.fbx`), không ghi đè bản cũ.
- Shot dùng asset bằng cách import hoặc link file `<tên>_rig.blend`, không sửa asset ngay trong shot.
- Script build dùng các module trong `pipeline/rigging/` (face rig, sửa da, kiểm tra rig).

## Hiện có

| Thư mục | Nội dung |
|---|---|
| `Characters/Lumo, Tavi, Nori, Piko/concept/` | Ảnh chính diện từ bộ concept (`<tên>_hero.png`). `source/` trống, chờ file Meshy |
| `Props/Wonder_Compass, Inventor_Pack, Story_Lens, Pocket_of_Wonders/concept/` | Ảnh concept 4 bảo bối, dùng thẳng cho Meshy Image to 3D được |
| `Environments/`, `Materials/`, `Animation_Library/`, `Third_Party/` | Trống |

Ảnh chủ đạo của thế giới nằm ở `01_BRAND/Brand_Guideline/world_key_art.png`.

## Bên thứ ba

- Để trong `Third_Party/<nguồn>/`, giữ nguyên cấu trúc gốc của pack, kèm file giấy phép.
- Asset CC-BY phải ghi công trong `06_PUBLISHING/Metadata/CREDITS.md` (tên model, tác giả, link, giấy phép) để dán vào mô tả video.
- Danh sách nguồn và giấy phép đã tra: `docs/ASSET_SOURCES.md`.
