# Asset bên thứ ba

Dùng cho những thứ không cần thiết kế riêng: cây cỏ, đá, đồ đạc, thú vật phụ, texture, bầu trời. Nhân vật chính và bảo bối là thiết kế riêng, không lấy từ thư viện. Hiện chưa tải asset nào.

## Giấy phép (kênh có kiếm tiền = dùng thương mại)

| Giấy phép | Dùng được? | Điều kiện |
|---|---|---|
| **CC0** | ✅ | Không cần ghi tên |
| **CC-BY** | ✅ | **Bắt buộc ghi tên tác giả + link + tên giấy phép** trong mô tả video |
| **Free Standard** (Sketchfab / Fab) | ✅ | Không được bán lại hay phát tán file gốc |
| CC-BY-**NC** | ❌ | Cấm thương mại |
| CC-BY-**ND** | ❌ | Không được chỉnh sửa |
| CC-BY-**SA** | ⚠️ Tránh | Sản phẩm phái sinh phải dùng cùng giấy phép |

## Nguồn

| Nguồn | Giấy phép | Có gì |
|---|---|---|
| [Quaternius](https://quaternius.com/) | CC0 | Stylized Nature MegaKit (cây, cỏ hoa, đá, nấm), Fantasy Props MegaKit (đồ cho Wonder Hub), Ultimate Crops (cà rốt), Farm Animal và Ultimate Animated Animals (thú có animation), Cute Animated Monsters. Tải qua itch.io, bỏ qua được bước trả tiền |
| [Poly Haven](https://polyhaven.com) | CC0 | HDRI bầu trời, texture |
| [ambientCG](https://ambientcg.com) | CC0 | Texture đất, gỗ, kim loại |
| [Sketchfab](https://sketchfab.com) | Tuỳ model | Lọc "Downloadable" và giấy phép. Cần đăng nhập mới tải được |

⚠️ Quaternius là **low-poly mặt phẳng**, còn phim là **soft stylized bo tròn**. Khi dùng phải đổi material sang màu pastel, thêm Subdivision, hoặc chỉ đặt ở hậu cảnh xa.

## Gợi ý cho tập 01

Mới kiểm tra giấy phép và số polygon, chưa duyệt hình từng model.

| Nhu cầu | Model | Giấy phép |
|---|---|---|
| Nhà nấm Thung lũng Mây | [Mushroom House — Brynnnnn](https://sketchfab.com/models/13774337157f4ac0a7e7fb3570de4bdc) (6k) · [Stylized mushrooms — QumoDone](https://sketchfab.com/models/9d22e02ce2a548959b1c4c4c1d546842) (12k) | CC-BY |
| Đồ trong Wonder Hub | Quaternius Fantasy Props · [Stylised Gramophone](https://sketchfab.com/models/5021ecc8b3704303af8c4a95aba6dc6b) (6k) · [Alchemist's Barrel Bookshelf](https://sketchfab.com/models/7d1198d993ba4aa3ac059a725ddeb369) (16k) | CC0 / CC-BY |
| Bình tưới | [Low Poly Watering Can — warcool](https://sketchfab.com/models/152e3ba5527b4a3aa29ffe4e0ce84bc6) (468) | CC-BY |
| Thú lên thuyền | Quaternius Farm Animal + Animated Animals; voi [Elephant Toy — marzipanne](https://sketchfab.com/models/d445d4067c664386b414a05cc118cbc1); hươu cao cổ [Low poly giraffe — Garu Games](https://sketchfab.com/3d-models/low-poly-giraffe-e9715aee26bd4e03b2740547b5b259d0) | CC0 / CC-BY |
| Thỏ (gag cà rốt) | [Cute bunny — art.lizzy](https://sketchfab.com/models/a44cfe6e2b0142a7b6425878b6b811bf) (7.6k, có animation) | CC-BY |

**Tự làm** (không có bản dễ thương miễn phí): phòng Wonder Hub có Story Portal, con thuyền Noah. Thú từ nhiều nguồn sẽ lệch phong cách, nên chọn một nguồn chính.

## Khi tải về

- Để trong `Third_Party/<nguồn>/`, giữ nguyên cấu trúc gốc và file giấy phép.
- Ưu tiên **glTF/GLB** hoặc `.blend`, model **dưới 50k polygon** (máy Vega 11).
- Mọi asset CC-BY ghi vào `06_PUBLISHING/Metadata/CREDITS.md` (tên model, tác giả, link, giấy phép).
