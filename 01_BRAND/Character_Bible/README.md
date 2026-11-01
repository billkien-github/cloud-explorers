# Character Bible

Nguồn chuẩn cho mọi thông tin về nhân vật. Concept: [`cloud_explorers_character_sheet.png`](cloud_explorers_character_sheet.png) và ảnh trong `02_ASSET_LIBRARY/Characters/<Tên>/concept/` (`_hero` có bối cảnh, `_apose` / `_ref` chính diện nền trơn).

**Nhóm Cloud Explorers:** khám phá những vùng đất kỳ diệu · giải mã bí ẩn của thế giới · học hỏi, sáng chế và trải nghiệm · tạo ra vô vàn tình huống dở khóc dở cười.

**Thế giới:** Fantasy + Science. Đảo đá bay giữa mây, thác nước, chùa tháp mái cong, cây hoa hồng (`01_BRAND/Brand_Guideline/world_key_art.png`). Cầu nối giữa phép thuật và máy móc là **tinh thể phát sáng**. Tạo hình **soft stylized**: tròn, mềm, pastel, đầu to (gần bằng nửa chiều cao).

## Nhân vật

| | **LUMO** | **TAVI** | **NORI** | **PIKO** |
|---|---|---|---|---|
| Danh hiệu | Cáo Mây | Nhà Phát Minh | Tinh Linh Ánh Sáng | Bóng Nước Kỳ Quặc |
| Vai | Explorer, mở đầu phiêu lưu | Inventor, ra giải pháp | Story Keeper, kiến thức | Wild Card, **động cơ gây hài** |
| Tính cách | Tò mò, năng động, luôn khởi xướng phiêu lưu | Thiên tài sáng chế, thích lắp ráp, thử nghiệm, nhiều ý tưởng "điên rồ" | Điềm đạm, tinh tế, giàu kiến thức, đưa ra manh mối và góc nhìn mới | Tinh nghịch, háu ăn, đáng yêu, cực kỳ khó đoán |
| Chất hài | Hấp tấp, làm trước nghe sau | Giải pháp phức tạp cho việc đơn giản | Giải thích dài, bị ngắt lời | Chạm lung tung, dễ phân tâm vì đồ lấp lánh, hay gây bất ngờ "ngoài kịch bản" |
| Ngoại hình | Cáo, tai rất to (trong hồng), chỏm lông trắng trên đầu, mắt nâu to, bụng và mõm màu kem, đuôi bông | Bò sát nhỏ, bụng kem, **gai tinh thể** dọc lưng và đuôi, mắt xanh lá | Khối tròn phát sáng, đầu liền thân, **4 cánh trong suốt**, 2 râu đầu ngôi sao vàng, tay nhỏ, vệt sáng thay chân | Khối thạch trong suốt, 2 sừng xanh đậm, tay nhỏ, giọt nước bắn quanh người |
| Đồ đeo | Áo choàng đỏ viền hoa văn mây vàng, khuy tròn vàng, túi da đeo chéo có hình mây | Mũ phi công da + kính bảo hộ, áo gile kem nhiều túi, thắt lưng | — | — |
| Dáng | Đứng, đi 2 chân | Đứng, đi 2 chân, chân ngắn, có đuôi | **Bay, không chân** | **Không chân**, nảy và trườn trên đất |
| Chiều cao | 1.00 (chuẩn) | 0.85 | 0.70 | 0.80 |
| Màu tham chiếu | Lông cam `#FD8A2B`, kem `#FEECCF`, áo choàng `#FC6640` | Da `#7EA258`, bụng `#ECBA7B`, tinh thể `#14F5F4` | Thân `#A787F6`, cánh `#D3ABFC`, sao `#FEF7A0` | Thân `#3BDCFD` → `#0988D1`, lưỡi `#D23C55` |

Mã màu lấy mẫu trực tiếp từ ảnh concept (vùng được chiếu sáng), dùng làm điểm xuất phát khi làm material.

**Cặp quan hệ tạo chuyện:** Lumo ↔ Tavi (vội vàng vs cẩn thận) · Tavi ↔ Nori (máy móc vs nguồn gốc) · Nori ↔ Piko (trật tự vs hỗn loạn) · **Lumo ↔ Piko** (cặp gây hài nhiều nhất).

## Bảo bối

| Bảo bối | Của | Công dụng | Giới hạn |
|---|---|---|---|
| Wonder Compass | Lumo | Cảm nhận được điều kỳ lạ | Không biết đó là gì |
| Inventor Pack | Tavi | Mỗi lần lắp được 1 máy (thiết bị, công cụ…) | Cần thời gian, hay xảy ra lỗi |
| Story Lens | Nori | Cho manh mối, gợi ý | Vẫn phải tự suy luận, giải mã |
| Pocket of Wonders | Piko | Lấy ra những vật phẩm bất ngờ | Không kiểm soát được thứ mình lấy ra |

Concept: `02_ASSET_LIBRARY/Props/<Tên>/concept/`.

## Làm 3D

| Nhân vật | Cách làm |
|---|---|
| Lumo, Tavi | Meshy sinh thân và rig Humanoid (dùng được thư viện animation). Đồ rời (áo choàng, túi), đuôi, xương tai, gai, mặt làm trong Blender |
| Nori, Piko | Giữ đúng concept: **không chân**. Meshy chỉ sinh hình thân. Rig bằng code trong Blender: thân co giãn bằng shape keys, tay nhỏ, cánh, râu, sừng, mặt |

Chi tiết: `02_ASSET_LIBRARY/MESHY.md`.

**Mỗi nhân vật cần:** turnaround (front/side/back/3/4), 12 biểu cảm, pose sheet, prop sheet, 8–12 animation loop dùng lại được (idle, walk, run, jump, surprised, laugh, think…).
