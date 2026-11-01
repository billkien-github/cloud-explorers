# Character Bible: Cloud Explorers

Nguồn: concept sheet [`cloud_explorers_character_sheet.png`](cloud_explorers_character_sheet.png) và ảnh chính diện từng nhân vật trong `02_ASSET_LIBRARY/Characters/<Tên>/concept/`. Vai trò, chất hài, cặp quan hệ và chiều cao xem `docs/BRIEF.md` mục 3.

**Nhóm Cloud Explorers:** khám phá những vùng đất kỳ diệu · giải mã bí ẩn của thế giới · học hỏi, sáng chế và trải nghiệm · và tạo ra vô vàn tình huống dở khóc dở cười. Thế giới là những đảo đá bay giữa mây, có thác nước, chùa tháp mái cong và cây hoa hồng (`01_BRAND/Brand_Guideline/world_key_art.png`).

## Nhân vật

| | **LUMO** | **TAVI** | **NORI** | **PIKO** |
|---|---|---|---|---|
| Danh hiệu | Cáo Mây | Nhà Phát Minh | Tinh Linh Ánh Sáng | Bóng Nước Kỳ Quặc |
| Tính cách | Tò mò, năng động, luôn khởi xướng phiêu lưu | Thiên tài sáng chế, thích lắp ráp, thử nghiệm, nhiều ý tưởng "điên rồ" | Điềm đạm, tinh tế, giàu kiến thức, đưa ra manh mối và góc nhìn mới | Tinh nghịch, háu ăn, đáng yêu, cực kỳ khó đoán, hay tạo bất ngờ "ngoài kịch bản" |
| Ngoại hình | Cáo cam đào, tai rất to (trong hồng), chỏm lông trắng trên đầu, mắt nâu to, bụng và mõm màu kem, đuôi bông | Bò sát nhỏ màu xanh lá, bụng kem, **gai tinh thể xanh ngọc** dọc lưng và đuôi, mắt xanh lá | Khối tròn tím lavender phát sáng, đầu liền thân, **4 cánh trong suốt**, 2 râu đầu ngôi sao vàng, tay nhỏ, vệt sáng thay chân | Khối thạch xanh aqua trong suốt, 2 sừng xanh đậm, tay nhỏ, giọt nước bắn quanh người |
| Trang phục, đồ đeo | **Áo choàng đỏ** viền hoa văn mây vàng, khuy tròn vàng, **túi da đeo chéo** có hình mây | **Mũ phi công da + kính bảo hộ**, **áo gile** kem nhiều túi, thắt lưng, cờ lê, cuộn giấy | Không | Không |
| Dáng đứng | 2 chân | 2 chân, chân ngắn, có đuôi | **Bay, không chân** | **Không chân**, nằm bẹt trên đất |
| Pose trong sheet | Đọc bản đồ, chạy, nhìn ống nhòm | Lắp máy, cầm cờ lê, cầm dụng cụ | Đọc sách, bay trong vòng sáng | Ngồi cạnh túi, bắn tung nước |

## Bảo bối

| Bảo bối | Của | Công dụng | Giới hạn | Concept |
|---|---|---|---|---|
| Wonder Compass | Lumo | Chỉ cảm nhận được điều kỳ lạ | Không biết đó là gì | `Props/Wonder_Compass/concept/` |
| Inventor Pack | Tavi | Mỗi lần lắp 1 máy (thiết bị, công cụ…) | Cần thời gian, hay xảy ra lỗi | `Props/Inventor_Pack/concept/` |
| Story Lens | Nori | Chỉ cho manh mối, gợi ý | Vẫn phải tự suy luận, giải mã | `Props/Story_Lens/concept/` |
| Pocket of Wonders | Piko | Lấy ra những vật phẩm bất ngờ | Không kiểm soát được thứ mình lấy ra | `Props/Pocket_of_Wonders/concept/` |

(Các đường dẫn `Props/...` nằm trong `02_ASSET_LIBRARY/`.)

## ⚠️ Cần chốt: Nori và Piko có chân không?

Rig có sẵn của Meshy (kèm thư viện hơn 600 động tác) chỉ dành cho nhân vật **2 tay, 2 chân** (xem `docs/MESHY.md`). Lumo và Tavi hợp. Nori (bay) và Piko (khối thạch) trong concept **không có chân**.

| Hướng | Cách làm | Được | Mất |
|---|---|---|---|
| **1. Giữ concept** (đang theo) | Meshy chỉ sinh hình thân. Rig Nori và Piko bằng code: thân co giãn bằng shape keys, tay nhỏ, cánh, râu, sừng | Đúng thiết kế đã chốt | Nori và Piko không dùng được thư viện animation (hai nhân vật này vốn ít đi bộ) |
| 2. Thêm chân | Vẽ lại Nori, Piko có tay chân ngắn, cả 4 dùng rig Humanoid của Meshy | Cả nhóm dùng chung thư viện animation | Đổi thiết kế, Piko mất chất "khối thạch" |

Ngoài ra concept có **đầu gần bằng nửa chiều cao**, to hơn mức Meshy làm tốt. Cần sinh thử Lumo trước để biết Meshy có đặt khớp đúng không.
