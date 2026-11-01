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

## ⚠️ Cần chốt: concept lệch với quy tắc tạo hình cho Meshy

`docs/BRIEF.md` mục 3.1 đặt quy tắc cả 4 nhân vật có dáng người (2 tay, 2 chân, không đồ rộng) để dùng rig Humanoid và thư viện animation của Meshy. Concept sheet lệch ở mấy chỗ sau:

| Nhân vật | Concept sheet | Quy tắc mục 3.1 | Hệ quả nếu giữ concept |
|---|---|---|---|
| **Nori** | Bay, không chân | 2 tay, 2 chân | Không dùng được rig Humanoid. Phải dùng Smart Rig (không có thư viện animation) hoặc rig bằng code |
| **Piko** | Khối thạch không chân | Người thạch có tay chân | Như Nori. Cách dựng bằng code như demo shot02 (co giãn bằng shape keys) hợp với Piko hơn |
| **Lumo** | Áo choàng, túi đeo chéo | Không mặc đồ rộng | Sinh Lumo không áo choàng, không túi. Hai món này làm thành mesh riêng, áo choàng cần xương hoặc mô phỏng vải |
| **Tavi** | Áo gile, đồ đeo, gai tinh thể to, có đuôi | Gai ôm sát, không đồ rộng | Gile ôm sát có thể để liền. Đuôi và gai to cần thêm xương trong Blender |
| Cả nhóm | Đầu gần bằng một nửa chiều cao | Đầu không quá 40% | Meshy có thể đặt sai khớp. Cần sinh thử một nhân vật để kiểm tra |

Hai hướng:
1. **Giữ concept:** Lumo và Tavi đi đường Meshy Humanoid. Nori và Piko là khối tròn, ít đi đứng, nên rig bằng code (thân co giãn, cánh, râu, tay nhỏ). Hướng này giữ đúng thiết kế, chỉ mất thư viện animation cho hai nhân vật vốn không cần đi bộ.
2. **Sửa concept theo mục 3.1:** vẽ lại Nori và Piko có tay chân. Cả 4 dùng chung thư viện animation, nhưng đổi thiết kế đã chốt.
