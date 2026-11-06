# Previz 2D và CC

Previz 2D là bước dựng câu chuyện thành hình chuyển động, làm khi kịch bản đã chốt và đã có ảnh của tập (`03_CONTENT/README.md`, mục "Làm một tập"). Nó thay cho storyboard và animatic. Mục đích là soi **diễn xuất**: ai làm gì, mắt, miệng, tai, đuôi, nhịp gag, thoại có đúng lúc không. Previz khối không có mặt nên không soi được những thứ này. Previz khối (`04_PRODUCTION/SEEDANCE.md`) làm sau, khi previz 2D của cảnh đã chốt, để soi không gian và cú máy cho Seedance.

Cả previz 2D lẫn previz khối đều có CC, và chuyển động phải kỹ: đủ biên độ, giữ tư thế đủ lâu để đọc được ở cỡ cảnh của từng cú máy.

## Thư mục

Mỗi cảnh trong beat sheet có một previz 2D:

```
03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/canh03/
├── timing.py       Nguồn mốc thời gian của cảnh: cú máy, mốc hành động, CC
├── build_shot.py   Script dựng previz 2D, đọc timing.py (cùng tên với script của shot để chạy bằng run.ps1)
├── canh03.blend    Do script tạo ra
└── renders/        canh03_preview.mp4, canh03_preview_cc.mp4 + .srt (không lên git)
```

Cảnh thử đặt ở `Previz_2D/TEST_<tên>/canhNN/`.

## timing.py

```python
FPS, SECONDS = 24, 50
SHOTS = [("S1", 0.0, 5.0), ("S2", 5.0, 9.0)]   # cú máy: (tên, giây bắt đầu, kết thúc)
KNOB_TURN = 1.0                               # mốc hành động: số hoặc (bắt đầu, kết thúc); chú thích là việc xảy ra
SHOUT_WATER = (7.5, 8.3)
CC = [
    (7.0, 7.5, "[giọt nước trúng mũi Lumo: TÁCH]"),
    (7.5, 8.3, "LUMO: NƯỚC!"),
]
```

- Mọi mốc tính bằng giây trong cảnh, tên viết hoa. Previz 2D, previz khối, CC và prompt Seedance đều lấy số từ file này. Không gõ lại số ở nơi khác: keyframe trong `build_shot.py` viết theo mốc (`LUMO_TRIP + 0.15`), việc nào chưa có mốc thì thêm mốc.
- Previz khối của một đoạn trong cảnh: xem mục "Previz" trong `04_PRODUCTION/SEEDANCE.md`.

## CC

- **Nội dung:** thoại cộng hành động và tiếng động, như phụ đề cho người khiếm thính.
  - Thoại: `TÊN: lời`, đúng chữ trong kịch bản `.fountain`. Chỉ dẫn diễn xuất trong ngoặc như kịch bản: `LUMO (thì thầm): Thêm chút nữa thôi…`. Chỉ dẫn đổi theo từng vế thoại (cử chỉ minh hoạ từng ý) thì để thoại một dòng, mỗi cử chỉ thành một dòng hành động chạy song song.
  - Hành động, tiếng động: trong `[ ]`, ngắn, thì hiện tại; tiếng động viết HOA như kịch bản: `[Piko húp nước: SỤP]`.
  - Thoại hiện đúng khoảng nhân vật nói. Dòng hành động hiện từ lúc việc xảy ra (không sớm hơn hình), đủ lâu để đọc: khoảng 20 ký tự mỗi giây trở xuống. Tránh để hai dòng chồng nhau lúc hình có chi tiết quan trọng ở đáy khung.
- **In lên video:**
  ```
  blender -b --factory-startup -P pipeline/cc.py -- <video> <timing.py> <video>_cc.mp4 [giây bắt đầu của đoạn]
  ```
  Ra video có CC (chữ trắng trên nền tối, giữa đáy khung) và file `.srt` cạnh nó. Các dòng chồng thời gian được gộp thành nhiều dòng. Previz khối của một đoạn thì truyền giây bắt đầu của đoạn để dời CC về 0.
- **Nhiều video nối lại** (các đoạn take của một cảnh, các cảnh của một tập): `pipeline/edit.py` lấy CC của từng đoạn theo `timing.py` và giây trong cảnh, dòng vắt qua chỗ nối thành một dòng liền. `--clean` không in lên hình, chỉ xuất `.srt` để tải lên làm phụ đề riêng.
- Bản có CC chỉ để duyệt và review. Video dẫn cho Seedance (`run.ps1 ref`) không in CC, nếu không chữ sẽ lọt vào take.

## Dựng previz 2D (cutout bằng code)

- Dựng trong Blender bằng `build_shot.py`, như previz khối: máy quay orthographic, nhìn ngang hoặc chếch nhẹ. Cú máy cắt theo `SHOTS` bằng timeline marker gắn camera; cỡ cảnh chỉnh bằng độ zoom ortho. Một cú có thể lia máy (keyframe vị trí và độ zoom của camera) để nối hai ý trong cùng một cú, như lia theo ánh mắt nhân vật. `review.json` nhận điểm cắt theo độ khác màu giữa hai khung: cú lia nhanh có thể bị đếm nhầm thành điểm cắt, còn hai cú cùng nền, cùng nhân vật (cận rồi trung cùng một chỗ) có thể không được đếm. Render bằng Workbench, màu phẳng, có viền tối quanh từng mảnh để tay nổi trên thân cùng màu. Cả cảnh render trong vài chục giây.
- **Nhân vật** là cutout phẳng ghép từ hình cơ bản (tròn, elip, bo góc), đúng màu tham chiếu và chiều cao trong `01_BRAND/Character_Bible/README.md`. Lớp trước, lớp sau theo độ sâu. Mỗi nhân vật có mảnh chuyển động riêng:
  - Chung: đầu, thân, tay, mắt (mở, nhắm, hướng nhìn), miệng (ngậm, mở, cười, chữ O).
  - Lumo: tai (dựng, cụp ra sau), đuôi. Tavi: đuôi, gai. Nori: 4 cánh, 2 râu, vệt sáng thay chân. Piko: thân co giãn, 2 sừng.
- **Diễn** đúng dáng và giới hạn khi diễn trong Character Bible: Nori luôn bay, Piko chỉ nảy, tay Lumo giơ cao nhất tới ngang tai. Mỗi hành động có lấy đà, có giữ tư thế; cảm xúc đọc được từ mặt và tai. Câu kịch bản có "nhìn" thì cho mắt nhìn đúng chỗ (`look()`).
- **Quay mặt** bằng lật gương (scale X = -1), nên đồ đeo một bên đổi bên khi nhân vật quay (túi đeo chéo của Piko luôn ở hông phía mặt nhìn). Previz 2D chấp nhận điều này; previz khối và dựng 3D theo đúng Character Bible.
- **Bối cảnh:** mặt phẳng màu đơn giản cộng đạo cụ chính đúng chỗ. Không cần đẹp. Nhân vật phụ, đạo cụ theo hình khối, màu chính và cỡ trong ảnh của tập (bảng của tập trong `02_ASSET_LIBRARY/MODELING.md`).
- **Key qua điểm cắt:** đổi chỗ hay tư thế tức thì thì đặt key giữ sớm hơn đúng một khung hình (`1 / FPS`); hai key cách nhau dưới một khung rơi vào cùng khung, key sau ghi đè key trước và nhân vật trượt dần qua nhiều cú. Nhân vật không có mặt trong cú thì đưa ra ngoài khung, nếu không sẽ lọt vào cú của người khác (Cảnh 2 tập 01 có sẵn `enter()`, `park()`). Mảnh nào bật tắt (`show`) thì đặt trạng thái ở giây 0 trước: trước key đầu tiên, Blender giữ đúng giá trị của key đó.
- **Bộ nhân vật cutout** nằm ở `pipeline/cutout.py`: bốn nhân vật (Piko có túi đeo chéo; kính bảo hộ và Inventor Pack của Tavi là mảnh riêng để kéo kính, hạ ba lô), bộ mặt và biểu cảm dựng sẵn (lông mày bù góc cúi người, giữ nét tới sát lúc đổi), hàm keyframe và diễn, máy quay theo `SHOTS`, cài đặt render. `build_shot.py` của cảnh chỉ dựng bối cảnh, đạo cụ riêng và phần diễn.
- **Khung hình:** chừa đáy khung (khoảng 15%) cho dải CC, đừng đặt chỗ chạm đất hay đạo cụ chính ở đó. Đạo cụ nhỏ mà gag dựa vào (cái thìa, la bàn) thì cắt sang cú máy cận. Cú cận cần thấy quan hệ giữa các đạo cụ (la bàn chỉ vào túi chứ không vào thìa, la bàn chỉ về vòm kính) hay một thao tác nhỏ (dời cái móc) có thể dựng riêng, phóng to, ở một góc xa của scene (Cảnh 1 tập 01 dựng ở X = 20 và X = 30, Cảnh 2 ở X = 40 tới 70).
- **Duyệt:** `run.ps1 preview -Shot <thư mục cảnh>`, in CC, rồi `/review <thư mục cảnh>` (`.claude/skills/review/SKILL.md`). Chốt previz 2D của cảnh rồi mới dựng previz khối.
