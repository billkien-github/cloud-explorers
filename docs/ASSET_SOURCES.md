# The Wonderlings — Nguồn 3D cho film thử

> Đối chiếu với `BRIEF.md` và kịch bản tập 01 *The Great Rain Experiment*. Tra cứu ngày 01/11/2026.
> Tôi mới kiểm tra **giấy phép và số polygon** qua API/trang của từng nguồn, **chưa mở từng model để duyệt hình**. Trước khi tải, bạn nên bấm link xem trước để chắc là hợp phong cách.

---

## 0. Kết luận nhanh

| Nhóm | Tìm được thư viện? | Hướng đi |
|---|---|---|
| **4 nhân vật chính** (Lumo, Tavi, Nori, Piko) | ❌ Không nên dùng thư viện | Phải **tự làm** để sở hữu IP: dựng bằng code (như Piko), dùng AI tạo 3D bản trả phí, hoặc thuê artist |
| Thú vật & sinh vật phụ (thỏ, chim, thú lên thuyền) | ✅ Nhiều | Quaternius (CC0) cùng một số model Sketchfab (CC-BY) |
| Đạo cụ (la bàn, ba lô, kính lúp, bình tưới, cà rốt) | ✅ Đủ | Sketchfab CC-BY, Quaternius CC0 |
| Thung lũng Mây (nấm, cây, hoa, đá) | ✅ Tốt | Quaternius Stylized Nature (CC0) + nhà nấm Sketchfab |
| Wonder Hub (xưởng phát minh, nội thất) | ⚠️ Ít | Ghép đồ lẻ (Quaternius props/furniture) hoặc tự dựng |
| **Thuyền Noah** | ⚠️ Không có bản dễ thương miễn phí | Có 1 bản CC-BY rất đơn giản làm nền. Thuyền là khối hình học dễ, **nên tự dựng bằng code** |
| Trời, HDRI, texture | ✅ Rất tốt | Poly Haven, ambientCG (CC0) |

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

**Lưu ý quan trọng về IP:** asset CC0/CC-BY thì ai cũng dùng được. Bạn **không thể đăng ký hay độc quyền** một nhân vật lấy từ thư viện. Vì vậy 4 nhân vật chính bắt buộc phải là thiết kế riêng.

---

## 2. Thư viện nền (nên tải trọn bộ)

> ✅ **Đã tải 01/11/2026:** 7 pack Quaternius dưới đây (cùng Ultimate Food) nằm trong `02_ASSET_LIBRARY/Third_Party/quaternius/`, có ảnh xem trước. Xem `02_ASSET_LIBRARY/Third_Party/README.md`.

| Nguồn | Giấy phép | Dùng cho gì | Ghi chú |
|---|---|---|---|
| [Quaternius — Stylized Nature MegaKit](https://quaternius.com/packs/stylizednaturemegakit.html) | CC0 | 40 cây, 35 cây cỏ hoa, 27 đá. Phong cách "Ghibli" | Khoảng 60–70% miễn phí, phần còn lại thuộc bản Pro/Source trả phí |
| [Quaternius — Ultimate Animated Animal Pack](https://quaternius.com/packs/ultimateanimatedanimals.html) | CC0 | 12 con vật, mỗi con hơn 12 animation (đi, nhảy, phi…) | Trang không liệt kê tên từng con. Theo các pack cũ thì chủ yếu là thú trang trại và rừng, **có thể không có voi, hươu cao cổ** |
| [Quaternius — Farm Animal Pack](https://quaternius.com/packs/farmanimal.html) | CC0 | Bò, heo, ngựa, cừu, lạc đà không bướu… có animation | Hợp cảnh muôn thú lên thuyền |
| [Quaternius — Cute Animated Monsters](https://quaternius.com/packs/cutemonsters.html) | CC0 | 21 sinh vật dễ thương có animation | Làm "sinh vật nhỏ ở Thung lũng Mây" |
| [Quaternius — Fantasy Props MegaKit](https://quaternius.com/packs/fantasypropsmegakit.html) | CC0 | 211 đạo cụ: sách, bình thuốc, rương, đồ nội thất, dụng cụ | Đồ trang trí Wonder Hub |
| [Quaternius — Ultimate Crops / Food](https://quaternius.com/packs/ultimatecrops.html) | CC0 | Rau củ (cà rốt cho gag của Piko) | |
| [Poly Haven](https://polyhaven.com) | CC0 | HDRI trời nắng hoặc u ám, texture, một số model | Ánh sáng trời thật cho cảnh mưa bão |
| [ambientCG](https://ambientcg.com) | CC0 | Texture đất, gỗ, kim loại | |

> ⚠️ **Phong cách:** Quaternius là **low-poly mặt phẳng**, còn demo Piko là **soft stylized bo tròn**. Khi ghép vào, nên thay material bằng bộ màu pastel của mình, có thể thêm modifier Subdivision cho mềm. Nếu không sẽ lệch tông.

---

## 3. Theo từng nhu cầu trong kịch bản

### 3.1 Thung lũng Mây

| Model | Giấy phép | Polygon | Link |
|---|---|---|---|
| ⭐ Stylized mushrooms — QumoDone | CC-BY | 12k | https://sketchfab.com/models/9d22e02ce2a548959b1c4c4c1d546842 |
| ⭐ Mushroom House — Brynnnnn | CC-BY | 6k | https://sketchfab.com/models/13774337157f4ac0a7e7fb3570de4bdc |
| Stylized mushroom house — nessa70 | CC-BY | 12k | https://sketchfab.com/models/72233d2bbc9a4573a707c75e82aae1d3 |
| mushroom house — LittleEarthRabbit | CC-BY | 25k | https://sketchfab.com/models/38abb056659e45858f7db09ddc7ca6c4 |
| Fairy Island (low poly) — YanaBelaya | CC-BY | 1.3k | https://sketchfab.com/models/86948296a080488f932326fce83f8ad0 |

Nhà nấm trong demo hiện tại là tự dựng bằng code. Các model trên chi tiết hơn (cửa sổ, ống khói, rêu).

### 3.2 Wonder Hub (xưởng phát minh)

| Model | Giấy phép | Polygon | Link |
|---|---|---|---|
| stylised sky player home diorama — Sander.Vander.Meiren | CC-BY | 23k | https://sketchfab.com/models/6597e6c9a5184f07a638ac33c08c2ad5 |
| Stylised Gramophone — MaddyKolberg | CC-BY | 6k | https://sketchfab.com/models/5021ecc8b3704303af8c4a95aba6dc6b |
| Stylized Alchemist's Barrel Bookshelf — rgurjjar321 | CC-BY | 16k | https://sketchfab.com/models/7d1198d993ba4aa3ac059a725ddeb369 |
| Bubbling Witch Cauldron (animated) — artel_3D | CC-BY | **153k (nặng)** | https://sketchfab.com/models/286513082150416aaaca76d9b85bd1d5 |

Không tìm thấy một "xưởng phát minh" hoàn chỉnh miễn phí. Đề xuất: tự dựng phòng tròn có Story Portal ở giữa (khối hình học đơn giản), rồi rải đồ của Quaternius Fantasy Props và các món trên.

### 3.3 Bảo bối của 4 nhân vật

| Bảo bối | Model gợi ý | Giấy phép | Polygon | Link |
|---|---|---|---|---|
| Wonder Compass (Lumo) | ⭐ Stylized Magic Compass — mar.cos. (825 lượt thích) | CC-BY | 22k | https://sketchfab.com/models/4f935b708d194be5b8a51369756c5caa |
| | Low Poly Stylized Compass — pau.raurellgomis | CC-BY | 0.5k | https://sketchfab.com/models/8de466ea26ab43cdadcf67d86344052a |
| Inventor Pack (Tavi) | Adventure Bag — Tim0 | CC-BY | 2.3k | https://sketchfab.com/models/36f80cc7e5884d5db1f818d3a89183f5 |
| | Backpack low-poly — dimaponomar2019 | CC-BY | 3.8k | https://sketchfab.com/models/d7225bdd1d6c42d992485d72438cab28 |
| Story Lens (Nori) | Styled Magnifying Glass — incg5764 | CC-BY | 1.9k | https://sketchfab.com/models/2d456cf49dd248739f3fb9616036c239 |
| Pocket of Wonders (Piko) | Không có bản phù hợp | | | Túi mềm dễ dựng bằng code |

Bảo bối là nhận diện thương hiệu của nhân vật, giống như bản thân nhân vật. Model thư viện **chỉ nên dùng để làm demo hoặc tham khảo**. Bản chính thức nên được thiết kế riêng.

### 3.4 Đạo cụ phụ trong tập 01

| Đạo cụ | Model | Giấy phép | Link |
|---|---|---|---|
| Bình tưới (cảnh mở đầu) | Free Low Poly Watering Can — warcool (468 polygon) | CC-BY | https://sketchfab.com/models/152e3ba5527b4a3aa29ffe4e0ce84bc6 |
| | Gardening Tools — Teen-Wolf (17k) | CC-BY | https://sketchfab.com/models/eacf394c1cbf496ca2c77373504ffaac |
| Cà rốt khổng lồ | Quaternius Ultimate Crops / Food | CC0 | https://quaternius.com/packs/ultimatecrops.html |
| Máy Rain-O-Matic 3000 | Đã dựng bằng code trong demo | — | `lab/shot02_max_power/build_shot.py` |

### 3.5 Thuyền Noah

| Model | Giấy phép | Polygon | Nhận xét | Link |
|---|---|---|---|---|
| Noah's Ark — Kneisler | CC-BY | 2.2k | Dựng theo bản vẽ của Kircher (1675), nhẹ, có 3 tầng. Phong cách tả thực đơn giản | https://sketchfab.com/models/cd5678d48bf24773b79aeaced79f0895 |
| Diorama Noahs Ark — Quakti | Free Standard | 28k | Là **căn phòng** trong thuyền, không phải con thuyền | https://sketchfab.com/models/123d7bd5918d469bb4d86cba20e88398 |

Không có bản dễ thương miễn phí. **Đề xuất tự dựng bằng code**: thân thuyền cong, nhà gỗ trên boong, mái dốc, cửa sổ tròn. Cách này giữ được phong cách soft stylized và không vướng giấy phép.

### 3.6 Thú vật lên thuyền & sinh vật phụ

| Con vật | Model | Giấy phép | Link |
|---|---|---|---|
| Thỏ (gag cà rốt) | Mushroom Bunny — hanna_siau (21k) | CC-BY | https://sketchfab.com/models/a52fb9309ba64858ba2747838bbf8a5c |
| | Cute bunny — art.lizzy (7.6k, có 1 animation) | CC-BY | https://sketchfab.com/models/a44cfe6e2b0142a7b6425878b6b811bf |
| Voi | Low poly elephant — MrEliptik | CC-BY | https://sketchfab.com/3d-models/low-poly-elephant-84fd98c561464b1ba5d3dd48ab161b9c |
| | Elephant Toy — marzipanne (12k) | CC-BY | https://sketchfab.com/models/d445d4067c664386b414a05cc118cbc1 |
| Hươu cao cổ | Low poly giraffe — Garu Games (~1k tris) | CC-BY | https://sketchfab.com/3d-models/low-poly-giraffe-e9715aee26bd4e03b2740547b5b259d0 |
| Thú trang trại, rừng | Quaternius Ultimate Animated Animals / Farm Animal Pack | CC0 | xem mục 2 |
| Chim nhỏ | Bird — klidas8 (37k) | CC-BY | https://sketchfab.com/models/e63479b07d8c4ae6a69b34247d572299 |

Thú lấy từ nhiều nguồn sẽ lệch phong cách. Nên chọn **một nguồn chính** (Quaternius) để đồng bộ, rồi chỉ lấy lẻ những con còn thiếu.

### 3.7 Tham khảo cho Piko (không dùng trực tiếp)

| Model | Giấy phép | Ghi chú | Link |
|---|---|---|---|
| Cute Slime — hugannh3 | CC-BY | 7.6k, có 3 animation | https://sketchfab.com/models/cf04b5e4d11f4fcba581dbda21134896 |
| Glowing Blue Slime — smomotempest | CC-BY | 824 polygon, có 4 animation | https://sketchfab.com/models/e1f25982bf634415a088a6cfc87fdc98 |

Piko trong demo đã là thiết kế riêng, dựng bằng code. Hai model này chỉ để tham khảo cách người khác làm nhịp nảy và co giãn của slime.

---

## 4. Làm 4 nhân vật chính thế nào

| Cách | Ưu | Nhược | Hợp với |
|---|---|---|---|
| **Dựng bằng code** (như Piko) | Sở hữu 100%, sửa nhanh, hợp hình khối tròn | Khó với lông, cánh mỏng, chi tiết hữu cơ | Piko ✅, Tavi (khối chắc, tinh thể) ✅ |
| **AI tạo 3D từ ảnh concept** (Meshy, Tripo, Rodin) | Nhanh, ra được hình hữu cơ | Lưới rối, phải dọn lại và rig. **Bản miễn phí của Meshy ra file CC BY 4.0 và public**, muốn sở hữu riêng phải trả phí. Thông tin về bản miễn phí của Tripo đang mâu thuẫn, chưa xác minh được | Lumo (tai, đuôi bông), Nori (cánh) |
| **Thuê artist** | Chất lượng và phong cách đồng nhất nhất | Tốn chi phí | Khi đã chốt kênh, làm bản chính thức |

**Đề xuất cho giai đoạn thử:**
1. Tavi dựng bằng code, vì hình khối của Tavi gần giống máy Rain-O-Matic.
2. Lumo và Nori: dùng AI tạo từ ảnh concept, bản trả phí 1 tháng để giữ quyền riêng. Sau đó dọn lưới và tô lại material trong Blender.

> *Cập nhật 01/11/2026:* cả 4 nhân vật đã chuyển sang dáng người (`BRIEF.md` mục 3.1) để dùng rig Humanoid và hơn 600 animation có sẵn của Meshy. Hướng mới: **cả 4 sinh bằng Meshy** (prompt ở `MESHY_PROMPTS.md`). Code chỉ lo phần Meshy không làm được: đuôi mây, cánh, râu, mặt, shader trong suốt và phát sáng.

---

## 5. Lưu ý kỹ thuật khi tải về

- **Máy Vega 11:** ưu tiên model **dưới 50k polygon**. Các model 150k–1M polygon (cauldron, tượng scan) sẽ làm EEVEE rất chậm.
- **Định dạng:** chọn **glTF/GLB** hoặc **.blend** nếu có, giữ material tốt hơn FBX/OBJ.
- **Sketchfab** cần **đăng nhập** mới tải được. Bạn tự đăng nhập và tải, tôi không tạo tài khoản thay được. Quaternius tải qua itch.io, có thể bỏ qua bước trả tiền "pay what you want".
- **Ghi công:** lập một file `CREDITS.md` cho mọi asset CC-BY (tên model, tác giả, link, giấy phép) để dán vào mô tả video.
- Asset tải về để trong `02_ASSET_LIBRARY/`: đồ của bên thứ ba vào `Third_Party/<nguồn>/`, đồ của dự án vào `Characters/`, `Environments/`, `Props/` (quy ước ở `02_ASSET_LIBRARY/README.md`).

---

## Nguồn tra cứu

- [Quaternius — danh mục pack](https://quaternius.com/) · [Stylized Nature MegaKit](https://quaternius.com/packs/stylizednaturemegakit.html) · [Ultimate Animated Animals](https://quaternius.com/packs/ultimateanimatedanimals.html) · [Cute Animated Monsters](https://quaternius.com/packs/cutemonsters.html) · [Fantasy Props MegaKit](https://quaternius.com/packs/fantasypropsmegakit.html)
- [Quaternius LowPoly Animated Animals (itch.io)](https://quaternius.itch.io/lowpoly-animated-animals) · [LowPoly Animated Monsters (itch.io)](https://quaternius.itch.io/lowpoly-animated-monsters) · [Textured Cute Monster Pack (OpenGameArt)](https://opengameart.org/content/textured-cute-monster-pack)
- Sketchfab Data API v3: `api.sketchfab.com/v3/search` (lọc downloadable + giấy phép), chi tiết model qua `api.sketchfab.com/v3/models/<uid>`
- [Sketchfab — Noahs Ark (benjtm)](https://sketchfab.com/3d-models/noahs-ark-209ecb2cfc4344159ca613bc2e80f997) · [MushroomHouse (Sloyd, CC BY 4.0)](https://www.sloyd.ai/free-3d-models/model/mushroomhouse-us681)
- [Sketchfab — Low poly elephant](https://sketchfab.com/3d-models/low-poly-elephant-84fd98c561464b1ba5d3dd48ab161b9c) · [Low poly giraffe](https://sketchfab.com/3d-models/low-poly-giraffe-e9715aee26bd4e03b2740547b5b259d0)
- Fab Standard License: [CG Channel](https://www.cgchannel.com/2024/11/epic-games-to-share-new-free-assets-on-fab-every-two-weeks) · [Animation Magazine](https://animationmagazine.net/2024/10/epic-launches-fab-unified-content-market) · [Fab CLA](https://www.fab.com/cla) · [Fab docs](https://dev.epicgames.com/documentation/fab)
- Giấy phép AI 3D: [Meshy — Pricing & Credits](https://docs.meshy.ai/en/webapp/pricing) · [Meshy — Can I use assets commercially](https://intercom.help/meshy/en/articles/16102098-can-i-use-meshy-assets-commercially) · [Tripo blog — Meshy alternative](https://www.tripo3d.ai/blog/cheaper-meshy-alternative-private-commercial-use-3d-models) · [Costbench — Tripo pricing](https://costbench.com/software/ai-3d-generation/tripo-ai/)
