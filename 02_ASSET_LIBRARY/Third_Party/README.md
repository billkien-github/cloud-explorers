# Thư viện asset

Asset tải về để dùng cho film thử *The Wonderlings*. Danh sách nguồn đầy đủ, kể cả những thứ chưa tải, nằm trong `docs/ASSET_SOURCES.md`.

## Quaternius (CC0, tải ngày 01/11/2026)

Giấy phép **CC0 1.0** (đã kiểm tra file `License_Standard.txt` trong pack): dùng thương mại thoải mái, không bắt buộc ghi tên. Nếu muốn ủng hộ tác giả: https://www.patreon.com/quaternius

| Thư mục | Định dạng | Số model | Xem trước | Nội dung |
|---|---|---|---|---|
| `quaternius/ultimate_animated_animals/glTF` | glTF (có animation) | 12 | [ảnh](quaternius/_previews/ultimate_animated_animals.png) | Alpaca, Bull, Cow, Deer, Donkey, Fox, Horse, Horse_White, Husky, ShibaInu, Stag, Wolf |
| `quaternius/farm_animals/FBX` | FBX (có animation) | 7 | [ảnh](quaternius/_previews/farm_animals.png) | Cow, Horse, Llama, Pig, Pug, Sheep, Zebra |
| `quaternius/cute_animated_monsters/glTF` | glTF (có animation) | 21 | [ảnh](quaternius/_previews/cute_animated_monsters.png) | Chicken, Penguin, Pig, Panda, Mushroom, Cactus, Bee, Ghost, Yeti… |
| `quaternius/stylized_nature_megakit/` | glTF / FBX / OBJ + texture | 68 (bản free, đủ bộ là 116) | [ảnh](quaternius/_previews/stylized_nature_megakit.png) | Cây thường, **cây khô**, thông, cây xoắn đỏ, hoa, **nấm**, cỏ, đá, lối đá |
| `quaternius/fantasy_props_megakit/Exports/` | glTF / FBX / OBJ + texture | 94 (bản free) | [ảnh](quaternius/_previews/fantasy_props_megakit.png) | Bàn thợ, vạc, giá sách, bình thuốc, nến, rương, thùng, **túi**, cà rốt… |
| `quaternius/ultimate_crops/FBX` | FBX | 102 | — | Cà rốt, bí ngô, dưa hấu, cà chua, ngô… (4 giai đoạn lớn) |
| `quaternius/ultimate_food/FBX` | FBX | 103 | — | Đồ ăn, nồi, đĩa, chai lọ |
| `quaternius/_zips/` | | | | File zip gốc. Có thể xoá sau khi đã dùng ổn |

## Gợi ý chọn cho tập 01 *The Great Rain Experiment*

| Nhu cầu | Lấy từ | Model |
|---|---|---|
| Thung lũng **khô** (đầu tập) | Nature MegaKit | `DeadTree_1..5`, `Grass_Wispy_Short/Tall` (cỏ vàng khô), `Rock_Medium_*`, `Pebble_*` |
| Thung lũng **tươi lại** (cuối tập) | Nature MegaKit | `CommonTree_*`, `Flower_3/4_*`, `Bush_Common_Flowers`, `Mushroom_Common`, `Clover_*` |
| Sinh vật nhỏ trong thung lũng | Cute Monsters | `Chicken`, `Penguin`, `Pig`, `Panda`, `Mushroom`, `Cactus`, `Bee` (mắt to tròn, gần phong cách Piko) |
| Túi của Piko (Pocket of Wonders) | Fantasy Props | `Pouch_Large` hoặc `Bag`. Tạm thời, bản chính thức nên thiết kế riêng |
| Gag cà rốt khổng lồ | Fantasy Props / Crops | `Carrot`, `FarmCrate_Carrot`, `Carrot_*` |
| Đồ trong Wonder Hub | Fantasy Props | `Workbench`, `Workbench_Drawers`, `Cauldron`, `Bookcase_2`, `Potion_*`, `Shelf_*`, `Candle*`, `Lantern_Wall`, `Scroll_*` |
| Thú lên thuyền Noah | Animals + Farm | `Cow`, `Horse`, `Sheep`, `Pig`, `Llama`, `Zebra`, `Deer`, `Fox`… |

## Lưu ý khi dùng

- **Lệch phong cách:** hai bộ thú (`ultimate_animated_animals`, `farm_animals`) là **low-poly kiểu tả thực**, không dễ thương như Piko. Nếu đưa vào cùng khung hình, cần làm mềm lại: thêm Subdivision, đổi sang màu pastel, phóng to đầu và mắt. Hoặc chỉ dùng ở hậu cảnh xa. Bộ thiên nhiên và quái vật hợp hơn.
- **Còn thiếu:** voi, hươu cao cổ, sư tử (cho cảnh thuyền Noah). Xem các lựa chọn CC-BY trong `docs/ASSET_SOURCES.md`, mục 3.6.
- **Nhập vào Blender bằng code:** `bpy.ops.import_scene.gltf(filepath=...)` cho `.gltf`, `bpy.ops.import_scene.fbx(filepath=...)` cho `.fbx`. Animation đi kèm nằm trong các Action của armature.
- **Tạo lại ảnh xem trước:** `make_previews.py` render một bảng tổng hợp cho bất kỳ thư mục model nào:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup -P pipeline\tools\make_previews.py -- <thư mục model> <ảnh.png> <số cột>
```
