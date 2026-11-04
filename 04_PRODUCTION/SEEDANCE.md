# Dựng shot bằng previz Blender + Seedance

Blender lo phần **đạo diễn**: bối cảnh khối, nhân vật dạng khối, chuyển động, cú máy, nhịp thời gian, tất cả dựng bằng `build_shot.py`. Seedance lo phần **hình**: lấy video previz làm khung (video-to-video), cùng ảnh nhân vật, bối cảnh và prompt viết theo từng giây, rồi vẽ lại thành clip hoàn chỉnh. Camera và timing chốt trong Blender trước khi tốn credit.

Đây là quy trình **đề xuất**, mới sinh thử một take, chưa soát: `04_PRODUCTION/TEST_First_Rain/sh010` (previz 27 giây, 7 shot cắt, đủ 4 nhân vật).

## Seedance ở đâu, giới hạn gì (tra ngày 03/11/2026)

- **Nơi chạy:** Higgsfield (đã có tài khoản và add-on trong Blender, xem `README.md`). Model **Seedance 2.5**, chế độ video-to-video: bài mẫu của Higgsfield sinh một lần trọn 30 giây từ previz 30 giây (1920x1080, 24 fps, MP4).
- **Seedance 2.0** (theo tài liệu của Venice): mỗi lần ra 4–15 giây. Tối đa 9 ảnh, 3 video tham chiếu (mỗi video 2–15 giây, tổng ≤ 15 giây, MP4/MOV H.264, ≤ 50 MB). Ảnh có cạnh ngắn ≥ 300 px.
- **Cách gọi tham chiếu trong prompt** tuỳ nền tảng: Higgsfield `@Video 1`, `@Image 1`; nơi khác `<Video 1>` hoặc `[Video 1]`. Viết đúng cú pháp của nơi đang dùng.
- Thông số trên thay đổi nhanh: kiểm tra lại trong app trước mỗi đợt sinh.

## Các bước

| # | Bước | Ra cái gì |
|---|---|---|
| 1 | Chọn đoạn từ previz 2D đã chốt của cảnh (`03_CONTENT/PREVIZ_2D.md`): ai, ở đâu, làm gì, mấy giây, cú máy | Mô tả ngắn ở docstring `build_shot.py` |
| 2 | Dựng previz bằng `build_shot.py` (xem "Previz") | `sh010.blend`, `backups/` |
| 3 | Duyệt previz: `run.ps1 stills`, `run.ps1 preview`, in CC bằng `pipeline/cc.py` (`03_CONTENT/PREVIZ_2D.md`, mục CC), rồi `/review <thư mục shot>` (hình có kể đúng kịch bản, nhịp, bố cục). **Chốt timing**: từ đây prompt bám theo từng con số | Bản previz đã chốt |
| 4 | Render video tham chiếu: `run.ps1 ref` (1920x1080, 24 fps, MP4, ít sample cho nhanh, không in CC) | `renders/sh010_ref.mp4` |
| 5 | Chọn ảnh tham chiếu (xem "Ảnh tham chiếu") | Danh sách `@Image` |
| 6 | Soạn prompt theo giây (xem "Prompt theo giây"); gom file tải lên vào một thư mục, đặt tên theo số tham chiếu. Trước khi sinh: `/review <thư mục shot>/seedance/prompt.md` | `seedance/prompt.md`, `renders/seedance_upload/` |
| 7 | Sinh trên Higgsfield: 16:9, 1080p, thời lượng bằng previz | `seedance/sh010_take01.mp4` |
| 8 | Soát take theo bảng "Soát take": `/review <thư mục shot>/seedance/<take>.mp4`. Lỗi do prompt thì sửa prompt; lỗi do previz thì sửa `build_shot.py`, render lại, sửa mốc trong prompt | Take được chọn |
| 9 | Hậu kỳ: lồng tiếng, nhạc, tiếng động ở `05_POST_PRODUCTION/` | |

Thư mục shot thêm `seedance/`:
```
sh010/
├── build_shot.py, sh010.blend, backups/, renders/   (như cũ)
├── renders/seedance_upload/  video1_previz.mp4, image1_<tên>.png…, prompt.txt: đúng thứ tự tải lên (không lên git)
└── seedance/
    ├── prompt.md            prompt đã gửi (tiếng Anh) + file tham chiếu theo số @Image + ghi nhận từng take
    └── sh010_take01.mp4     clip Seedance trả về, giữ nguyên, không sửa
```

## Previz

- **Mốc thời gian khai báo thành hằng số ở đầu `build_shot.py`**, mỗi khoá máy có chú thích cỡ cảnh và ý đồ. Prompt lấy số từ đây, không đo lại bằng mắt. Shot thuộc một cảnh đã có previz 2D thì đầu `build_shot.py` khai `TIMING = "<đường dẫn timing.py của cảnh, tính từ gốc repo>"` và `OFFSET = <giây bắt đầu của đoạn trong cảnh>`, lấy mốc từ `timing.py` trừ `OFFSET`, không gõ lại số. `check_prompt.py` của `/review` đọc theo cặp này.
- **Chuyển động đọc được ở cỡ cảnh của shot:** đủ biên độ, có giữ tư thế. Seedance bám chuyển động của previz ("video wins"), nên một động tác previz làm quá nhỏ (tay rụt vài độ) thì take coi như không có.
- **Nhân vật dạng khối đúng chiều cao và tỉ lệ trong `01_BRAND/Character_Bible/README.md`.** Khối sai tỉ lệ thì Seedance kéo nhân vật theo.
- **Màu khối** để Seedance biết ai là ai, quay hướng nào (bảng màu ghi vào prompt):
  - Một nhân vật: đỏ = mặt trước, đen = lưng, xanh lá = hai bên và đỉnh.
  - Từ hai nhân vật: mỗi nhân vật một màu cố định (Lumo cam, Tavi xanh lá, Nori tím nhạt, Piko xanh ngọc), mặt trước đầu có ô trắng báo hướng nhìn. Bối cảnh, đạo cụ để xám để không lẫn màu nhân vật. Đã dùng ở `TEST_First_Rain`.
- **Khối 4 nhân vật** dựng trong `TEST_First_Rain/sh010/build_shot.py`. Previz thứ hai cần thì chuyển sang `pipeline/`.
- **Bối cảnh:** chỉ cần đúng khối, kích thước, vật cản và đạo cụ chính. Hình thật do ảnh tham chiếu và prompt quyết định.
- **Bố trí để thấy mặt:** nhân vật nhìn thẳng vào vật chính (máy, cửa) thì máy quay phía trước chỉ thấy lưng. Đặt chỗ tương tác ở hông vật để nhân vật đứng nghiêng về phía máy quay; tránh để hai, ba nhân vật thẳng hàng với máy quay (che nhau).
- **Nhiều shot trong một previz:** mỗi shot một camera, cắt bằng timeline marker gắn camera; danh sách `SHOTS` ở đầu script ghi giây bắt đầu, kết thúc.
- **Tự kiểm tra trong script:** máy không ra ngoài bối cảnh, đầu nhân vật luôn trong khung. Kiểm tra này không bắt được nhân vật bị che, vẫn phải xem ảnh tĩnh từng shot.
- Previz không có mặt: biểu cảm, mắt, miệng, tai, đuôi chỉ có trong prompt.

## Ảnh tham chiếu

- Mỗi nhân vật **một ảnh cố định cho mọi shot** để giữ nhân vật đồng nhất: `02_ASSET_LIBRARY/Characters/<Tên>/concept/<tên>_hero.png` (Lumo: chưa chốt, xem cuối file).
- Bối cảnh: `01_BRAND/Brand_Guideline/world_key_art.png` hoặc ảnh riêng của từng địa điểm (thêm vào khi có).
- Đạo cụ: `02_ASSET_LIBRARY/Props/<Tên>/concept/<tên>_hero.png`.
- Chỉ đưa ảnh của thứ có trong shot. Số `@Image` theo thứ tự tải lên: mỗi số một ảnh, ghi bảng số → file trong `prompt.md` và soát lại trước khi sinh (bài mẫu của Higgsfield có chỗ hai ảnh cùng ghi `@Image 2`).

## Prompt theo giây

Viết tiếng Anh. Dựa theo bài mẫu của Higgsfield (nguồn cuối file), gồm các khối theo thứ tự:

1. **Tiêu đề và tóm tắt:** shot, thời lượng, video-to-video; 1–2 câu: ai, ở đâu, làm gì, kết thúc ra sao.
2. **ACTIVE REFERENCES:** mỗi `@Video`, `@Image` một dòng, nói nó **quyết định gì** và **không lấy gì** (nền, tư thế, ánh sáng của ảnh nhân vật; vật liệu, màu, ánh sáng của previz). Có bảng màu khối → nhân vật.
3. **STYLE:** khối chuẩn bên dưới, giống nhau ở mọi shot. Địa điểm, giờ trong ngày, ánh sáng riêng của cảnh viết ở tóm tắt và TIMELINE, không sửa khối chuẩn.
4. **CHARACTERS:** đặc điểm phải giữ của từng nhân vật lấy từ Character Bible (tỉ lệ, giới hạn khi diễn, đồ mang theo); đúng bao nhiêu nhân vật trong khung.
5. **CAMERA:** bám `@Video 1` 1:1, khớp từng khung; một cú liền hay cắt ở giây nào.
6. **RULES:** luật đánh số. Đếm được thì ghi số (bao nhiêu nhân vật, đạo cụ nào ở đâu); không chữ, không logo; không có gì đáng sợ, bạo lực.
7. **TIMELINE:** chia khối 2–5 giây theo cú máy hoặc hành động (cảnh cắt nhanh thì mỗi shot một khối). Mỗi khối:
   - `0–3.5s —` cú máy theo `@Video 1` (cỡ cảnh, hướng chuyển động, ví dụ "low frontal, retreating");
   - hành động, mốc nhấn ghi tới 0.1 giây ("at 9.7s Lumo turns the head toward camera");
   - biểu cảm (mắt, miệng, tai, đuôi);
   - `END 3.5s:` trạng thái cuối khối (ai ở đâu, đang làm gì).
8. **AUDIO:** không nhạc, không lời thoại (nhạc và lồng tiếng nhiều thứ tiếng làm ở hậu kỳ). Có sinh tiếng động hay không: chưa chốt.
9. **HOLD:** nhắc lại các khoá quan trọng nhất ở cuối.

Quy tắc viết:
- Mốc trong prompt phải trùng hằng số trong `build_shot.py`. Đối chiếu bằng ảnh tĩnh đúng khung của từng mốc: khung = giây × 24 + 1 (`run.ps1 stills 217,469 -Shot <shot>` cho 9.0 s và 19.5 s).
- Mỗi nhân vật luôn gọi đúng một tên, không thay bằng "the fox", "the hero".
- Mỗi mốc chỉ một hành động chính. Không nhồi nhiều việc hơn số giây cho phép.
- Chữ và video mâu thuẫn về chuyển động thì video thắng (ghi rõ trong prompt).
- **Lời thoại:** ghi khoảng giây nhân vật nói theo kịch bản ("3.0–4.5s Lumo talks, mouth moving, no voice"), giọng lồng ở hậu kỳ. Câu nói không được tạo thêm cảnh: máy vẫn theo previz.
- Nền tảng chỉ cho sinh tối đa 15 giây: cắt previz ở chỗ cắt cảnh hoặc chỗ nhân vật dừng, mỗi đoạn một prompt, mốc thời gian tính lại từ 0.

**STYLE chuẩn:**
```
Soft stylized 3D animated film for young children: rounded soft shapes, pastel colors, warm gentle light, soft shadows. Every character keeps the materials of its reference image. Friendly and safe: nothing scary, no injuries, no realism, no live-action, no text, no logos, no watermarks. Original, no IP.
```

**Khung prompt:**
```
# <SHOT> — <SCENE NAME> (<N>s, video-to-video)

<One or two sentences: who, where, what happens, how it ends.> Video-to-video pass driven by @Video 1.

ACTIVE REFERENCES
@Video 1 = the Blender previz (<N>s, <N*24> frames, 24fps), frame-aligned. SOLE authority for the camera (path, framing, lens, timing) and for every character's position and motion. Block figures: <RED face = the direction Lumo faces, BLACK = back, GREEN = sides and top>. Every block becomes the real character or object its position implies. Do NOT take any material, color, texture or lighting from it. If the text and the video disagree about motion, the video wins.
@Image 1 = Lumo — defines design, proportions, colors, cape and bag. Background, pose and lighting not inherited.
@Image 2 = <location> — defines look, palette and light. Layout follows @Video 1. Camera angle not inherited.

STYLE
<STYLE chuẩn>

CHARACTERS
Lumo: <proportions and limits from the Character Bible>. Exactly <K> characters in frame, never extras.

CAMERA
Strictly follow the camera work of @Video 1, 1:1 and frame-aligned for all <N> seconds. <One continuous take, no cuts. | Cuts exactly at ...>

RULES
1. ...

TIMELINE
0–3.5s — (camera per @Video 1: ...) Lumo ... At 2.0s ... Face: ... END 3.5s: ...
3.5–7.0s — ...

AUDIO
No music, no dialogue, no voice. <Sound effects: ... Timed accents: <t>s ..., <t>s ... | No sound at all.>

HOLD
@Video 1 camera 1:1 for all <N> seconds. Exactly <K> characters. @Image 1 identity constant. No text, no logos, no watermarks.
```

## Soát take

| Kiểm tra | Sai thì |
|---|---|
| Cú máy, cỡ cảnh, chỗ cắt khớp previz từng giây | Nhấn mạnh CAMERA, HOLD; nếu vẫn lệch thì làm previz rõ hơn (khối to hơn, ít vật thừa) |
| Đúng số nhân vật, không người thừa | Thêm số vào RULES, HOLD |
| Nhân vật giống ảnh tham chiếu, đúng tỉ lệ | Sửa tỉ lệ khối trong previz; thêm ý vào CHARACTERS |
| Màu khối không lọt vào hình | Nhấn "do not take color from @Video 1" |
| Hành động, biểu cảm, khoảng nói đúng mốc giây | Tách khối TIMELINE nhỏ hơn, mỗi mốc một việc |
| Không chữ, logo, cảnh đáng sợ | Thêm vào RULES |

Ghi kết quả từng take (đạt, lỗi gì) vào cuối `seedance/prompt.md`.

## Chưa chốt

- **Ảnh tham chiếu Lumo**, mỗi bản lệch một kiểu: `lumo_hero.png` (đủ áo choàng dài và túi, nhưng nền cảnh phức tạp), hay `lumo_apose_meshy.png` (nền trơn, nhưng không áo choàng, không túi).
- **Mỗi lần sinh là một shot hay một đoạn nhiều shot.** Bài mẫu của Higgsfield dựng 19 shot trong một previz 30 giây rồi sinh một lần, nhân vật giữ đồng nhất qua các lần cắt. Nếu theo cách này thì thư mục sinh nằm ở cấp đoạn, không ở cấp `sh010/`. Đang thử bằng `TEST_First_Rain/sh010`.
- Có cho Seedance sinh tiếng động không, hay làm hết tiếng ở hậu kỳ.
- Take lưu vào git (qua LFS) hết, hay chỉ take được chọn.

## Nguồn (tra ngày 03/11/2026)

[Higgsfield: Blender + Higgsfield workflow (5 ví dụ prompt đầy đủ)](https://higgsfield.ai/@adilinthewild/blogs/this-blender-higgsfield-ai-workflow-changes-how-you-make-ai-video) · [Venice: Seedance 2.0 reference-to-video](https://docs.venice.ai/it/guides/media/seedance-2-0) · [MindStudio: timeline prompting](https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video)
