# Asset Library

## Quy ước cho mỗi asset

Mỗi nhân vật, đạo cụ hay bối cảnh có một thư mục riêng:

```
Characters/Lumo/
├── concept/          Ảnh 2D: ảnh chính diện, turnaround, ảnh đưa vào Meshy Image to 3D
├── source/           File gốc tải từ Meshy (FBX/GLB + animation). Không sửa, chỉ thêm bản mới
├── build_lumo.py     Script: import source, thêm xương, face rig, material -> lumo_rig.blend
├── lumo_rig.blend    File đã rig, do script tạo ra (dùng trong shot)
└── qa/               Ảnh kiểm tra tư thế, biểu cảm, số liệu độ méo
```

- Bản Meshy mới tải về thì thêm hậu tố ngày hoặc số phiên bản (`lumo_meshy_v02.fbx`), không ghi đè bản cũ.
- Shot dùng asset bằng cách import hoặc link file `<tên>_rig.blend`, không sửa asset ngay trong shot.

## Hiện có

| Thư mục | Nội dung |
|---|---|
| `Characters/Lumo, Tavi, Nori, Piko/concept/` | Ảnh chính diện từ bộ concept (`<tên>_hero.png`). `source/` đang trống, chờ file Meshy |
| `Props/Wonder_Compass, Inventor_Pack, Story_Lens, Pocket_of_Wonders/concept/` | Ảnh concept 4 bảo bối |
| `Environments/` | Trống. Ảnh chủ đạo của thế giới ở `01_BRAND/Brand_Guideline/world_key_art.png` |
| `Materials/`, `Animation_Library/` | Trống |
| `Third_Party/quaternius/` | 7 pack Quaternius CC0 (cây cỏ, đạo cụ, thú, quái vật dễ thương). Xem `Third_Party/README.md` |

Bản Lumo dựng hoàn toàn bằng code (rig Rigify, face rig, 9 biểu cảm) vẫn nằm ở `lab/char_lumo/`. Đó là bản thử, các module dùng lại được (`face_rig.py`, cách sửa da, bài kiểm tra 16 tư thế) sẽ chuyển sang `pipeline/` khi làm bản Lumo từ Meshy.

## Bên thứ ba

- Giữ nguyên cấu trúc gốc của pack trong `Third_Party/<nguồn>/`, kèm file giấy phép.
- Asset CC-BY phải ghi công: ghi vào `06_PUBLISHING/Metadata/CREDITS.md` (tên model, tác giả, link, giấy phép) để dán vào mô tả video.
- Danh sách nguồn và giấy phép đã tra: `docs/ASSET_SOURCES.md`.
