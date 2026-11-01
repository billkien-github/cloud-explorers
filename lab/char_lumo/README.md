# Lumo: thử nghiệm rig bằng code

Mục tiêu: kiểm chứng xem rig hoàn toàn bằng code tự chủ được tới đâu, với một nhân vật không phải người (cáo mây có tai to, đuôi bông, tay chân ngắn).

## Chạy

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup -P lab\char_lumo\build_lumo.py   # dựng + rig -> lumo.blend (~15s)
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b lab\char_lumo\lumo.blend -P lab\char_lumo\pose_test.py   # 16 tư thế -> renders\
```

Mở `lumo.blend` trong Blender: chọn `RIG-Lumo`, vào Pose Mode rồi kéo các controller để thử. Blender sẽ hỏi có cho chạy script `rig_ui.py` không. Đây là bảng điều khiển IK/FK do chính Rigify sinh ra, bấm **Allow** thì bảng mới hiện.

## Quy trình (toàn bộ bằng code, `build_lumo.py`)

1. **Nặn hình:** ghép các khối metaball (đầu, mõm, má, thân, bụng, tay, chân, tai). Đuôi mây là một khối riêng, tránh dính vào đầu.
2. **Làm lại lưới:** voxel remesh cho ra lưới đều, toàn tứ giác (thân 19,8k đỉnh, đuôi 9,5k đỉnh).
3. **Tô màu theo vùng:** màu cam đào, bụng và mõm màu kem, chóp tai và gan chân màu cam đậm, đuôi màu trắng mây (bảng màu trong BRIEF).
4. **Khung xương:** lấy mẫu người của Rigify, đặt lại từng xương theo dáng Lumo, bỏ xương ngực và chậu, **thêm 2 chuỗi xương tai và 1 chuỗi xương đuôi**.
5. **Sinh rig:** Rigify tạo 259 xương, có controller, IK/FK cho tay chân, controller cho từng đốt tai và đuôi.
6. **Gắn da tự động** (bone heat) rồi **sửa da:** bật giữ thể tích (dual quaternion), tự làm mượt trọng số bằng numpy, thêm modifier Corrective Smooth.
7. **Mặt:** mắt (lòng trắng, tròng màu mint, con ngươi, đốm sáng), mũi, miệng, má hồng, ngôi sao trên trán. Tất cả là object rời, gắn vào xương đầu (cách làm giống Piko).

## Kết quả kiểm tra

`pose_test.py` đặt Lumo vào 16 tư thế khó, render 2 góc mỗi tư thế (`renders/pose_sheet.png`) và đo độ méo lưới so với tư thế nghỉ (`renders/pose_qa.txt`).

| Tư thế | Mặt hỏng: gắn da tự động → sau khi sửa | Thể tích: trước → sau |
|---|---|---|
| Bật nhảy | 2,1% → **1,6%** | 0.96 → **0.98** |
| Quay đầu | 0,3% → **0,2%** | 0.95 → **1.00** |
| Giơ hai tay | 2,5% → **1,6%** | 0.96 → **0.98** |
| Chạy | 1,2% → **0,9%** | 0.96 → **0.99** |
| Ngoái đầu (cổ xoắn) | 1,4% → **0,7%** | 0.91 → **0.99** |
| Đuôi cuộn | 9,1% → 7,5% | 0.75 → 1.14 |

(Bản trước khi sửa lưu ở `renders/pose_qa_raw.txt` và `renders/pose_sheet_raw.png`.)

**Các vòng sửa đã chạy tự động:**
1. Số liệu chỉ ra lỗi tập trung ở vai, cổ, chân → bật giữ thể tích, làm mượt trọng số da, thêm Corrective Smooth.
2. Ảnh cận cảnh cho thấy chóp nhọn ở chỗ tay nối vai. Làm mượt mạnh hơn vẫn không hết.
3. Render tư thế nghỉ thì thấy chóp nhọn **có sẵn trong hình khối**, không phải lỗi rig. Sửa phần nặn hình (thêm khối khuỷu tay) → hết.

## Vòng đi bộ (`walk_cycle.py`)

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b lab\char_lumo\lumo.blend -P lab\char_lumo\walk_cycle.py      # -> lumo_walk.blend + renders\walk_qa.txt
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b lab\char_lumo\lumo_walk.blend -P pipeline\render.py -- preview   # -> renders\lumo_walk_preview.mp4
```

- **Nhịp:** một vòng 18 frame (2 bước). Bước ngắn, nhanh kiểu "lạch bạch" hợp với chân ngắn.
- **Chân** (IK): gót chạm đất → bàn chân phẳng → nhón gót đẩy → nhấc lên đưa ra trước. Khi bàn chân đặt trên đất, nó lùi đều về sau đúng bằng tốc độ đi, nên chân không trượt.
- **Thân:** nhún thấp nhất ngay sau khi chạm đất, lắc sang bên chân đang trụ, hông xoay theo bước, ngực xoay ngược lại. Tay vung ngược với chân cùng bên.
- **Chuyển động thứ cấp:** tai nảy theo nhịp nhún, trễ dần từ gốc ra chóp. Đuôi vẫy ngang như sóng, mỗi đốt trễ 2 frame.
- Mọi kênh được lặp vô hạn bằng modifier Cycles. Đoạn đi thật cho cả rig tiến về trước với tốc độ khớp sải chân.

**Đo trượt chân** khi đi thật trên sàn ô vuông (`renders/walk_qa.txt`): lúc đặt trên đất, bàn chân xê dịch tối đa **0,26 mm/frame**, trung bình 0,15 mm/frame, trong khi Lumo đi được 6,7 mm/frame. Tức trượt khoảng 2%, mắt thường không thấy.

Video: `renders/lumo_walk_preview.mp4` (hình), `renders/lumo_walk_sound.mp4` (có tiếng bước chân từ `walk_audio.py`).

## Biểu cảm (`face_rig.py`, `expressions.py`)

Face rig gồm các bộ phận rời gắn vào xương đầu, điều khiển bằng **21 thanh trượt số** đặt trên object `RIG-Lumo` (panel *Custom Properties*). Có thể keyframe bằng code hoặc kéo tay trong Blender. Driver chỉ dùng biểu thức đơn giản nên chạy được mà không cần cho phép script.

| Nhóm | Thanh trượt | Cách hoạt động |
|---|---|---|
| Mí mắt | `eye_open_L/R`, `lower_lid_L/R`, `lid_tilt_L/R` | Mỗi mí là một nửa quả cầu màu lông, xoay quanh mắt: nhắm, mở, trợn, mắt cười (mí dưới đẩy lên), xếch giận, rủ buồn |
| Mắt | `pupil`, `look_x`, `look_z` | Đồng tử to hoặc nhỏ, liếc ngang hoặc dọc. Mí không xoay theo mắt khi liếc |
| Lông mày | `brow_raise_L/R`, `brow_tilt_L/R` | Lông mày nổi: nhướng, cau, nghiêng buồn hoặc giận |
| Miệng | `mouth_smile/grin/open/frown/flat/wavy` | 7 hình miệng là shape key của cùng một vòng đỉnh. Mỗi điểm được **chiếu lên bề mặt mõm** nên luôn ôm sát da |
| Khác | `blush`, `sweat` | Má hồng to dần, giọt mồ hôi hiện ra |

`expressions.py` định nghĩa **9 biểu cảm** (Bình thường, Tò mò, Bất ngờ, Phấn khích, Bối rối, Ngượng ngùng, Buồn, Quyết tâm, Vui). Mỗi biểu cảm kết hợp các thanh trượt trên với tư thế đầu và tai. Script render `renders/expression_sheet.png` và tạo `lumo_faces.blend`, một đoạn 9 giây chuyển qua lần lượt từng biểu cảm, có chớp mắt. Tiếng hiệu ứng được tạo bằng `faces_audio.py`.

**Lỗi đã phát hiện và sửa trong lúc làm:**
1. Lông mày ngược dấu ("giận" ra "buồn"): phát hiện khi rà chiều xoay.
2. Miệng quá nhỏ, bị mí và mõm che: phóng to và chiếu lên bề mặt mõm.
3. Miệng há/cười toe bị khuất dưới mõm: thêm **khối cằm** cho phần dưới mặt đứng thẳng hơn.
4. Miệng biến mất khi đầu ngửa: render so sánh có và không có tư thế đầu thì thấy da cằm bị xương cổ kéo theo. Sửa trọng số để **khối đầu, mõm, cằm đi theo xương đầu 100%**.

## Còn lại

| Vấn đề | Mức độ | Ghi chú |
|---|---|---|
| Mặt trong của đuôi khi cuộn bị ép (7,5% mặt) | Không thấy được | Nằm khuất trong chỗ cong. Nếu cần có thể thêm đốt đuôi |
| Gan bàn chân bị ép khi bẹp mạnh | Không thấy được | Nằm dưới gan bàn chân |
| Tai mất khoảng 10% thể tích khi cụp | Nhẹ | Tai mỏng đi một chút khi gập |
| **Tai trông giống tai thỏ** | Thiết kế | Cần chốt lại hình tai cáo trên concept art |
| **Chưa kiểm tra chuyển động** (đi, chạy, nhảy theo thời gian) | Cần người duyệt | Rig đạt về kỹ thuật, còn cảm giác chuyển động phải xem video |
