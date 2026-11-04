# Previz 2D và CC

Previz 2D là bước dựng câu chuyện thành hình chuyển động ngay sau khi kịch bản xong (`03_CONTENT/README.md`, mục "Viết một tập"). Nó thay cho storyboard và animatic. Mục đích là soi **diễn xuất**: ai làm gì, mắt, miệng, tai, đuôi, nhịp gag, thoại có đúng lúc không. Previz khối không có mặt nên không soi được những thứ này. Previz khối (`04_PRODUCTION/SEEDANCE.md`) làm sau, khi previz 2D của cảnh đã chốt, để soi không gian và cú máy cho Seedance.

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

Cảnh thử đặt ở `Previz_2D/TEST_<tên>/canhNN/`. Hiện có `TEST_Cutout/canh01`: 11 giây, khoảnh khắc Lumo vội với tay, khựng lại rồi bị Piko đè xuống nút ở Cảnh 3 tập 01.

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

- Mọi mốc tính bằng giây trong cảnh, tên viết hoa. Previz 2D, previz khối, CC và prompt Seedance đều lấy số từ file này. Không gõ lại số ở nơi khác.
- Previz khối của một đoạn trong cảnh: xem mục "Previz" trong `04_PRODUCTION/SEEDANCE.md`.

## CC

- **Nội dung:** thoại cộng hành động và tiếng động, như phụ đề cho người khiếm thính.
  - Thoại: `TÊN: lời`, đúng chữ trong kịch bản `.fountain`. Chỉ dẫn diễn xuất trong ngoặc như kịch bản: `LUMO (thì thầm): Thêm chút nữa thôi…`.
  - Hành động, tiếng động: trong `[ ]`, ngắn, thì hiện tại; tiếng động viết HOA như kịch bản: `[Piko húp nước: SỤP]`.
  - Thoại hiện đúng khoảng nhân vật nói. Dòng hành động hiện từ lúc việc xảy ra, đủ lâu để đọc.
- **In lên video:**
  ```
  blender -b --factory-startup -P pipeline/cc.py -- <video> <timing.py> <video>_cc.mp4 [giây bắt đầu của đoạn]
  ```
  Ra video có CC (chữ trắng trên nền tối, giữa đáy khung) và file `.srt` cạnh nó. Các dòng chồng thời gian được gộp thành nhiều dòng. Previz khối của một đoạn thì truyền giây bắt đầu của đoạn để dời CC về 0.
- Bản có CC chỉ để duyệt và review. Video dẫn cho Seedance (`run.ps1 ref`) không in CC, nếu không chữ sẽ lọt vào take.

## Dựng previz 2D (cutout bằng code)

- Dựng trong Blender bằng `build_shot.py`, như previz khối: máy quay orthographic, nhìn ngang hoặc chếch nhẹ. Cú máy cắt theo `SHOTS` bằng timeline marker gắn camera; cỡ cảnh chỉnh bằng độ zoom ortho. Render bằng Workbench, màu phẳng, có viền tối quanh từng mảnh để tay nổi trên thân cùng màu. Cả cảnh render trong vài chục giây.
- **Nhân vật** là cutout phẳng ghép từ hình cơ bản (tròn, elip, bo góc), đúng màu tham chiếu và chiều cao trong `01_BRAND/Character_Bible/README.md`. Lớp trước, lớp sau theo độ sâu. Mỗi nhân vật có mảnh chuyển động riêng:
  - Chung: đầu, thân, tay, mắt (mở, nhắm, hướng nhìn), miệng (ngậm, mở, cười, chữ O).
  - Lumo: tai (dựng, cụp ra sau), đuôi. Tavi: đuôi, gai. Nori: 4 cánh, 2 râu, vệt sáng thay chân. Piko: thân co giãn, 2 sừng.
- **Diễn** đúng dáng và giới hạn khi diễn trong Character Bible: Nori luôn bay, Piko chỉ nảy, tay Lumo giơ cao nhất tới ngang tai. Mỗi hành động có lấy đà, có giữ tư thế; cảm xúc đọc được từ mặt và tai.
- **Bối cảnh:** mặt phẳng màu đơn giản cộng đạo cụ chính đúng chỗ. Không cần đẹp.
- **Bộ nhân vật cutout** (bốn nhân vật, bộ mặt, các biểu cảm dựng sẵn, hàm diễn) đang nằm trong `TEST_Cutout/canh01/build_shot.py`. Cảnh thật đầu tiên cần thì chuyển sang `pipeline/`.
- **Duyệt:** `run.ps1 preview -Shot <thư mục cảnh>`, in CC, rồi `/review <thư mục cảnh>` (`.claude/skills/review/SKILL.md`). Chốt previz 2D của cảnh rồi mới dựng previz khối.
