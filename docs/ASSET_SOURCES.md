# Nguồn asset 3D bên ngoài

Dùng cho những thứ không cần thiết kế riêng: cây cỏ, đá, đồ đạc, thú vật phụ, texture, bầu trời. 4 nhân vật chính và 4 bảo bối là thiết kế riêng (concept trong `01_BRAND/` và `02_ASSET_LIBRARY/`), không lấy từ thư viện.

> Tra cứu ngày 01/11/2026. Mới kiểm tra **giấy phép và số polygon** qua API/trang của từng nguồn, **chưa mở từng model để duyệt hình**. Trước khi tải, nên bấm link xem trước để chắc là hợp phong cách. Chưa tải asset nào về dự án.

---

## 1. Giấy phép: cái nào dùng được cho kênh YouTube

Kênh có bật kiếm tiền tức là **dùng thương mại**.

| Nhãn giấy phép | Dùng được? | Điều kiện |
|---|---|---|
| **CC0** (Public Domain) | ✅ | Không cần ghi tên. Tốt nhất |
| **CC-BY** (CC Attribution) | ✅ | **Bắt buộc ghi tên tác giả + link + tên giấy phép** trong mô tả video |
| **Free Standard** (Sketchfab / Fab) | ✅ | Dùng thương mại trên mọi loại media. Không được bán lại hay phát tán file gốc |
| CC-BY-**NC** (NonCommercial) | ❌ | Cấm thương mại |
| CC-BY-**ND** (NoDerivs) | ❌ | Không được chỉnh sửa. Đưa vào phim là rủi ro |
| CC-BY-**SA** | ⚠️ Tránh | Sản phẩm phái sinh phải dùng cùng giấy phép |

Asset CC0/CC-BY thì ai cũng dùng được, không thể đăng ký hay độc quyền. Vì vậy những gì làm nên nhận diện của phim (nhân vật, bảo bối) phải là thiết kế riêng.

---

## 2. Thư viện nền

| Nguồn | Giấy phép | Dùng cho gì | Ghi chú |
|---|---|---|---|
| [Quaternius — Stylized Nature MegaKit](https://quaternius.com/packs/stylizednaturemegakit.html) | CC0 | Cây, cỏ hoa, đá, nấm | Bản free có khoảng 68/116 model |
| [Quaternius — Ultimate Animated Animal Pack](https://quaternius.com/packs/ultimateanimatedanimals.html) | CC0 | 12 thú có animation (cáo, hươu, ngựa, bò, sói…) | Low-poly kiểu tả thực, không có voi, hươu cao cổ |
| [Quaternius — Farm Animal Pack](https://quaternius.com/packs/farmanimal.html) | CC0 | Bò, heo, ngựa, cừu, lạc đà không bướu, ngựa vằn… có animation | Hợp cảnh muôn thú lên thuyền |
| [Quaternius — Cute Animated Monsters](https://quaternius.com/packs/cutemonsters.html) | CC0 | 21 sinh vật dễ thương có animation | Sinh vật nhỏ ở Thung lũng Mây |
| [Quaternius — Fantasy Props MegaKit](https://quaternius.com/packs/fantasypropsmegakit.html) | CC0 | Sách, bình thuốc, rương, bàn thợ, vạc, nến… | Đồ trang trí Wonder Hub |
| [Quaternius — Ultimate Crops / Food](https://quaternius.com/packs/ultimatecrops.html) | CC0 | Rau củ, đồ ăn (cà rốt cho gag của Piko) | |
| [Poly Haven](https://polyhaven.com) | CC0 | HDRI trời nắng hoặc u ám, texture, một số model | Ánh sáng trời cho cảnh mưa bão |
| [ambientCG](https://ambientcg.com) | CC0 | Texture đất, gỗ, kim loại | |

Quaternius tải qua itch.io, có thể bỏ qua bước trả tiền "pay what you want".

⚠️ **Lệch phong cách:** Quaternius là **low-poly mặt phẳng**, còn phim là **soft stylized bo tròn** (xem `01_BRAND/Brand_Guideline/world_key_art.png`). Khi dùng phải thay material bằng màu pastel, thêm Subdivision cho mềm, hoặc chỉ đặt ở hậu cảnh xa.

---

## 3. Theo nhu cầu của tập 01

### 3.1 Thung lũng Mây

| Model | Giấy phép | Polygon | Link |
|---|---|---|---|
| ⭐ Stylized mushrooms — QumoDone | CC-BY | 12k | https://sketchfab.com/models/9d22e02ce2a548959b1c4c4c1d546842 |
| ⭐ Mushroom House — Brynnnnn | CC-BY | 6k | https://sketchfab.com/models/13774337157f4ac0a7e7fb3570de4bdc |
| Stylized mushroom house — nessa70 | CC-BY | 12k | https://sketchfab.com/models/72233d2bbc9a4573a707c75e82aae1d3 |
| mushroom house — LittleEarthRabbit | CC-BY | 25k | https://sketchfab.com/models/38abb056659e45858f7db09ddc7ca6c4 |
| Fairy Island (low poly) — YanaBelaya | CC-BY | 1.3k | https://sketchfab.com/models/86948296a080488f932326fce83f8ad0 |

### 3.2 Wonder Hub (xưởng phát minh)

| Model | Giấy phép | Polygon | Link |
|---|---|---|---|
| stylised sky player home diorama — Sander.Vander.Meiren | CC-BY | 23k | https://sketchfab.com/models/6597e6c9a5184f07a638ac33c08c2ad5 |
| Stylised Gramophone — MaddyKolberg | CC-BY | 6k | https://sketchfab.com/models/5021ecc8b3704303af8c4a95aba6dc6b |
| Stylized Alchemist's Barrel Bookshelf — rgurjjar321 | CC-BY | 16k | https://sketchfab.com/models/7d1198d993ba4aa3ac059a725ddeb369 |
| Bubbling Witch Cauldron (animated) — artel_3D | CC-BY | **153k (nặng)** | https://sketchfab.com/models/286513082150416aaaca76d9b85bd1d5 |

Không có "xưởng phát minh" hoàn chỉnh miễn phí. Đề xuất: tự dựng phòng tròn có Story Portal ở giữa, rồi rải đồ Quaternius Fantasy Props và các món trên.

### 3.3 Đạo cụ phụ

| Đạo cụ | Model | Giấy phép | Link |
|---|---|---|---|
| Bình tưới (cảnh mở đầu) | Free Low Poly Watering Can — warcool (468 polygon) | CC-BY | https://sketchfab.com/models/152e3ba5527b4a3aa29ffe4e0ce84bc6 |
| | Gardening Tools — Teen-Wolf (17k) | CC-BY | https://sketchfab.com/models/eacf394c1cbf496ca2c77373504ffaac |
| Cà rốt khổng lồ | Quaternius Ultimate Crops / Food | CC0 | https://quaternius.com/packs/ultimatecrops.html |
| Máy Rain-O-Matic 3000 | Không lấy thư viện, sinh bằng Meshy (prompt trong `docs/MESHY.md`) | — | — |

### 3.4 Thuyền Noah

| Model | Giấy phép | Polygon | Nhận xét | Link |
|---|---|---|---|---|
| Noah's Ark — Kneisler | CC-BY | 2.2k | Dựng theo bản vẽ của Kircher (1675), nhẹ, 3 tầng, kiểu tả thực đơn giản | https://sketchfab.com/models/cd5678d48bf24773b79aeaced79f0895 |
| Diorama Noahs Ark — Quakti | Free Standard | 28k | Là **căn phòng** trong thuyền, không phải con thuyền | https://sketchfab.com/models/123d7bd5918d469bb4d86cba20e88398 |

Không có bản dễ thương miễn phí. Đề xuất **tự dựng bằng code** (thân thuyền cong, nhà gỗ trên boong, mái dốc, cửa sổ tròn) hoặc sinh bằng Meshy, để giữ phong cách soft stylized.

### 3.5 Thú vật lên thuyền & sinh vật phụ

| Con vật | Model | Giấy phép | Link |
|---|---|---|---|
| Thỏ (gag cà rốt) | Mushroom Bunny — hanna_siau (21k) | CC-BY | https://sketchfab.com/models/a52fb9309ba64858ba2747838bbf8a5c |
| | Cute bunny — art.lizzy (7.6k, có 1 animation) | CC-BY | https://sketchfab.com/models/a44cfe6e2b0142a7b6425878b6b811bf |
| Voi | Low poly elephant — MrEliptik | CC-BY | https://sketchfab.com/3d-models/low-poly-elephant-84fd98c561464b1ba5d3dd48ab161b9c |
| | Elephant Toy — marzipanne (12k) | CC-BY | https://sketchfab.com/models/d445d4067c664386b414a05cc118cbc1 |
| Hươu cao cổ | Low poly giraffe — Garu Games (~1k tris) | CC-BY | https://sketchfab.com/3d-models/low-poly-giraffe-e9715aee26bd4e03b2740547b5b259d0 |
| Thú trang trại, rừng | Quaternius Ultimate Animated Animals / Farm Animal Pack | CC0 | xem mục 2 |
| Chim nhỏ | Bird — klidas8 (37k) | CC-BY | https://sketchfab.com/models/e63479b07d8c4ae6a69b34247d572299 |

Thú lấy từ nhiều nguồn sẽ lệch phong cách. Nên chọn **một nguồn chính** để đồng bộ, chỉ lấy lẻ những con còn thiếu.

---

## 4. Lưu ý khi tải về

- **Máy Vega 11:** ưu tiên model **dưới 50k polygon**. Model 150k–1M polygon làm EEVEE rất chậm.
- **Định dạng:** chọn **glTF/GLB** hoặc **.blend** nếu có, giữ material tốt hơn FBX/OBJ.
- **Sketchfab** cần **đăng nhập** mới tải được. Bạn tự đăng nhập và tải, Claude không tạo tài khoản thay được.
- **Chỗ để:** `02_ASSET_LIBRARY/Third_Party/<nguồn>/`, giữ nguyên cấu trúc gốc và file giấy phép.
- **Ghi công:** mọi asset CC-BY ghi vào `06_PUBLISHING/Metadata/CREDITS.md` (tên model, tác giả, link, giấy phép) để dán vào mô tả video.

---

## Nguồn tra cứu

- [Quaternius — danh mục pack](https://quaternius.com/) · [LowPoly Animated Animals (itch.io)](https://quaternius.itch.io/lowpoly-animated-animals) · [LowPoly Animated Monsters (itch.io)](https://quaternius.itch.io/lowpoly-animated-monsters)
- Sketchfab Data API v3: `api.sketchfab.com/v3/search` (lọc downloadable + giấy phép), chi tiết model qua `api.sketchfab.com/v3/models/<uid>`
- Fab Standard License: [Fab CLA](https://www.fab.com/cla) · [Fab docs](https://dev.epicgames.com/documentation/fab)
