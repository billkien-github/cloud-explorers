# Dựng shot bằng previz Blender + Seedance

Blender lo phần **đạo diễn**: bối cảnh khối, nhân vật dạng khối, chuyển động, cú máy, nhịp thời gian, tất cả dựng bằng `build_shot.py`. Seedance lo phần **hình**: lấy video previz làm khung (video-to-video), cùng ảnh nhân vật, bối cảnh và prompt viết theo từng giây, rồi vẽ lại thành clip hoàn chỉnh. Camera và timing chốt trong Blender trước khi tốn credit.

Đây là quy trình **đề xuất**, đang thử: mới có take 1 của `EP001_Great_Rain_Experiment/sh020` (đã soát, chưa dùng được).

## Seedance ở đâu, giới hạn gì (tra ngày 06/11/2026)

- **Nơi chạy:** BytePlus ModelArk (console hoặc API), model **Seedance 2.5** (mã `dreamina-seedance-2-5-260628` theo tài liệu bên thứ ba, đối chiếu lại trong console). Mỗi lần sinh 4–30 giây, `duration` là số nguyên giây. Tham số: `ratio` 16:9; `resolution` 480p, 720p, 1080p (nguồn bên thứ ba ghi 1080p có giá từ tháng 10/2026; chưa có thì 720p); `watermark` tắt; `generate_audio` bật tắt tiếng động.
- **Tham chiếu:** ảnh (role `reference_image`), video (`reference_video`), tiếng (`reference_audio`). Prompt gọi `@Image1`, `@Video1`, viết liền không cách, số theo thứ tự đưa vào. Qua API, video phải là URL (đặt file lên chỗ lưu trữ trước). Số tham chiếu tối đa và tổng thời lượng video tham chiếu (khoảng 30 giây) lấy từ nguồn bên thứ ba, chưa đối chiếu được trang chính thức.
- Thông số trên thay đổi nhanh: kiểm tra lại trong console trước mỗi đợt sinh.

## Các bước

| # | Bước | Ra cái gì |
|---|---|---|
| 1 | Chọn đoạn từ previz 2D đã chốt của cảnh (`03_CONTENT/PREVIZ_2D.md`): ai, ở đâu, làm gì, mấy giây, cú máy | Mô tả ngắn ở docstring `build_shot.py` |
| 2 | Dựng previz bằng `build_shot.py` (xem "Previz") | `sh010.blend`, `backups/` |
| 3 | Duyệt previz: `run.ps1 stills`, `run.ps1 preview`, in CC bằng `pipeline/cc.py` (`03_CONTENT/PREVIZ_2D.md`, mục CC), rồi `/review <thư mục shot>` (hình có kể đúng kịch bản, nhịp, bố cục). **Chốt timing**: từ đây prompt bám theo từng con số | Bản previz đã chốt |
| 4 | Render video tham chiếu: `run.ps1 ref` (1920x1080, 24 fps, MP4, ít sample cho nhanh, không in CC) | `renders/sh010_ref.mp4` |
| 5 | Chọn ảnh tham chiếu (xem "Ảnh tham chiếu") | Danh sách `@Image` |
| 6 | Soạn prompt theo giây (xem "Prompt theo giây"), kèm bảng số tham chiếu → file tải lên → nguồn. Tạo ngay thư mục tải lên riêng của shot: `python pipeline/seedance_upload.py <thư mục shot>` chép video previz, từng ảnh (tên theo số) và `prompt.txt`; sửa prompt hay đổi ảnh thì chạy lại. Trước khi sinh: `/review <thư mục shot>/seedance/prompt.md` | `seedance/prompt.md`, `renders/seedance_upload/` |
| 7 | Sinh trên BytePlus ModelArk: 16:9, 1080p, `duration` bằng `SECONDS` của `build_shot.py`, watermark tắt | `seedance/sh010_take01.mp4` |
| 8 | Soát take theo bảng "Soát take": `/review <thư mục shot>/seedance/<take>.mp4`. Lỗi do prompt thì sửa prompt; lỗi do previz thì sửa `build_shot.py`, render lại, sửa mốc trong prompt | Take được chọn |
| 9 | Dựng cảnh: ghi take được chọn của từng đoạn vào danh sách dựng `<tập>/canhNN_edit.py`, nối bằng `pipeline/edit.py` (cắt theo `SEGMENT`, CC theo `TIMING`) | `<tập>/renders/canhNN_edit_cc.mp4` + `.srt` |
| 10 | Hậu kỳ: lồng tiếng, nhạc, tiếng động ở `05_POST_PRODUCTION/` | |

Thư mục shot thêm `seedance/`:
```
sh010/
├── build_shot.py, sh010.blend, backups/, renders/   (như cũ)
├── renders/seedance_upload/  video1_previz.mp4, image1_<tên>.png…, prompt.txt: đúng thứ tự tải lên, do pipeline/seedance_upload.py tạo (không lên git)
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
  - Từ hai nhân vật: mỗi nhân vật một màu cố định (Lumo cam, Tavi xanh lá, Nori tím nhạt, Piko xanh ngọc), mặt trước đầu có ô trắng báo hướng nhìn. Bối cảnh, đạo cụ để xám để không lẫn màu nhân vật. Đang dùng ở Cảnh 1 tập 01.
- **Khối 4 nhân vật**, máy quay, tự kiểm khung và cài đặt render ở `pipeline/blocks.py`.
- **Một cảnh dài chia nhiều đoạn:** bối cảnh và diễn của cả cảnh viết một lần trong `<tập>/canhNN_blocks.py` (hàm `build(timing, offset, seconds, out_blend)`); mỗi đoạn là một thư mục shot, `build_shot.py` chỉ khai `TIMING`, `OFFSET`, `FPS, SECONDS` rồi gọi `build`. Danh sách cú máy của đoạn lấy từ `SHOTS` của `timing.py`. CC in bằng `pipeline/cc.py` với giây bắt đầu của đoạn. ModelArk nhận số nguyên giây, nên `SECONDS` làm tròn lên số nguyên và `SEGMENT` ghi độ dài đoạn trong cảnh: máy quay chỉ dựng các cú trong `SEGMENT`, phần dư giữ cú máy cuối, lúc dựng `pipeline/edit.py` cắt bỏ; `check_prompt.py` đọc cả hai. Đang dùng cho Cảnh 1 tập 01: `EP001_Great_Rain_Experiment/sh010` (0–28.8 s, S1–S6) và `sh020` (28.8–55 s, S7–S14).
- **Vật hiện ra, biến mất** bằng key scale 0 và 1 cách nhau ít nhất một khung; hai key gần hơn một khung rơi vào cùng khung và vật lộ dần từ key trước đó.
- **Vật cầm tay:** khối tay bọc lấy đầu cán như nắm tay, vật hơi chếch khỏi trục tay; đặt vật ở bên hông hay cạnh đầu, không chĩa vào mặt. Que nối thẳng từ một quả cầu tay sát mặt thì Seedance vẽ tay thành bong bóng có que xuyên qua và đưa vật vào miệng (take 1 của `EP001_Great_Rain_Experiment/sh020`). Vật nhỏ làm to hơn cỡ thật một chút cho đọc được.
- **Bối cảnh:** chỉ cần đúng khối, kích thước, vật cản và đạo cụ chính. Hình thật do ảnh tham chiếu và prompt quyết định.
- **Bố trí để thấy mặt:** nhân vật nhìn thẳng vào vật chính (máy, cửa) thì máy quay phía trước chỉ thấy lưng. Đặt chỗ tương tác ở hông vật để nhân vật đứng nghiêng về phía máy quay; tránh để hai, ba nhân vật thẳng hàng với máy quay (che nhau).
- **Nhiều shot trong một previz:** mỗi shot một camera, cắt bằng timeline marker gắn camera; danh sách `SHOTS` ở đầu script ghi giây bắt đầu, kết thúc.
- **Tự kiểm tra trong script:** máy không ra ngoài bối cảnh, đầu nhân vật luôn trong khung. Kiểm tra này không bắt được nhân vật bị che, vẫn phải xem ảnh tĩnh từng shot.
- Previz không có mặt: biểu cảm, mắt, miệng, tai, đuôi chỉ có trong prompt.

## Ảnh tham chiếu

- **Chọn ảnh đầy đủ nhất về hình**, mỗi asset một ảnh để tiết kiệm suất `@Image`: ảnh xoay (trước và sau trong một ảnh) hơn ảnh một mặt, ảnh 3/4 hơn ảnh nhìn thẳng, nền trơn hơn ảnh có bối cảnh. Ảnh sinh cho từng tập: `02_ASSET_LIBRARY/MODELING.md`, mục "Ảnh cho một tập".
- Mỗi nhân vật **một ảnh cố định cho mọi shot** để giữ nhân vật đồng nhất: ảnh xoay `02_ASSET_LIBRARY/Characters/<Tên>/concept/<tên>_turnaround.png` (nhìn trước bên trái, nhìn sau bên phải, nền trơn; ghép bằng `pipeline/turnaround.py`). Ảnh xoay của Piko ghép từ ảnh Piko đeo Pocket of Wonders. Nhân vật chưa có ảnh xoay thì dùng `<tên>_ref.png`.
  - Ghi trong ACTIVE REFERENCES: `@Image1 = Lumo turnaround sheet: left front view, right back view of ONE character. Layout, background and pose not inherited.`
  - Chưa thử trong take nào: take đầu dùng ảnh xoay thì soát xem Seedance có vẽ hai bản của cùng một nhân vật không, và mặt sau có đúng khi nhân vật quay lưng.
- Bối cảnh: ảnh riêng của từng địa điểm, chưa có thì `01_BRAND/Brand_Guideline/world_key_art.png`. Đã có: Thung lũng Mây khô hạn (Cảnh 1 tập 01) `02_ASSET_LIBRARY/Environments/Cloud_Valley/concept/cloud_valley_dry_hero.png`.
- Đạo cụ: `02_ASSET_LIBRARY/Props/<Tên>/concept/<tên>_ref.png` (nhìn 3/4, nền trơn). Đạo cụ tập 01 chưa có `_ref` thì dùng `_front.png` (vật dài: `_side.png`), hoặc ảnh trạng thái khi trạng thái đó lên hình (`_frost.png`). Nhân vật nền (sinh vật nhỏ của thung lũng): `02_ASSET_LIBRARY/Characters/Valley_Critters/concept/valley_critters_ref.png`; ghi trong prompt tư thế nào dùng cho clip.
- Chỉ đưa ảnh của thứ có trong shot. Số `@Image` theo thứ tự tải lên: mỗi số một ảnh, ghi bảng số → file trong `prompt.md` và soát lại trước khi sinh (bài mẫu của Higgsfield có chỗ hai ảnh cùng ghi `@Image 2`).
- Bối cảnh, Piko đeo túi và sinh vật nhỏ sinh bằng ChatGPT theo các prompt dưới. Sinh lại thì đính kèm đúng ảnh ghi ở mỗi prompt, lưu đúng đường dẫn ghi kèm, soát theo Character Bible trước khi dùng.

### Prompt sinh ảnh tham chiếu bằng ChatGPT

**Thung lũng Mây khô hạn** (bối cảnh Cảnh 1 tập 01). Đính kèm `01_BRAND/Brand_Guideline/world_key_art.png`. Lưu `02_ASSET_LIBRARY/Environments/Cloud_Valley/concept/cloud_valley_dry_hero.png`.
```
The attached image is a style and palette reference only: soft stylized 3D animated film for young children, warm sunlight, pastel blue sky, floating islands with pagodas and a cloud sea far away. Do not copy its layout, its lush green ground or its waterfalls.

Create a NEW location in the same world: the Valley of Clouds during a long drought. One wide 16:9 image, eye level, sunny afternoon, no characters, no animals.
- Valley floor: pale beige earth with a network of dry cracks, patches of dry yellowed grass, a few smooth pale rocks.
- Center left: a small rectangular garden bed of darker brown soil edged with flat stones, a few thin pale seedlings drooping; next to it a dry curled twig holding one curled dry leaf, and a small wilted flower with its head bent down.
- Right: a big rounded hill of dry yellow grass rising above the garden; a thin band of soft white cloud clings to its summit like a scarf.
- Far background, small and hazy: floating islands with tiny pagodas and the cloud sea from the reference.
- No water anywhere in the valley: no river, no pond, no waterfall. No buildings in the valley or on the hill.
- Thirsty but gentle and cute, never bleak or scary. Soft rounded shapes, pastel colors, soft shadows.
- No text, no logos, no watermark.
```

**Piko đeo Pocket of Wonders.** Đính kèm theo thứ tự `02_ASSET_LIBRARY/Characters/Piko/concept/piko_apose_body.png`, `02_ASSET_LIBRARY/Props/Pocket_of_Wonders/concept/pocket_of_wonders_ref.png`. Lưu `02_ASSET_LIBRARY/Characters/Piko/concept/piko_pouch_ref.png`; ảnh nhìn sau `piko_pouch_ref_back.png`.
```
Image 1 is Piko, a character of a soft stylized 3D animated film for young children. Image 2 is Piko's pouch. Draw Piko wearing the pouch. Keep Piko exactly as in Image 1: same translucent aqua jelly body, two dark-blue horns, eyes, mouth, tiny paws, proportions; no legs.

How Piko wears the pouch:
- Only the pouch itself from Image 2: purple velvet, gold drawstring with tassels, cream cloud emblem. Its mouth is gathered shut; none of the items in Image 2 (bottle, crystal, mushroom, map, compass, feather, stars) are visible.
- The pouch is small, about the size of one of Piko's paws.
- A thin gold cord carries it crossbody: looped over the root of Piko's RIGHT horn (the horn on the viewer's left when Piko faces us), down Piko's back, then diagonally across the front just under the mouth to Piko's LEFT hip.
- The pouch hangs at Piko's left hip (the viewer's right when Piko faces us), at paw height, resting against the jelly body.

Full body, three-quarter view, Piko turned toward the viewer's left so that Piko's left side and the pouch face us. Happy expression. Plain flat light-grey background, soft even studio light. No text, no logos, no watermark.
```
Ảnh nhìn sau, nhắn tiếp: `Now the same Piko with the same pouch seen from behind, as a separate image, same rules: show the gold cord looped over the right horn and running down the back.`

**Sinh vật nhỏ của thung lũng** (nhân vật nền, có mặt từ Cảnh 1 tới Cảnh 7). Đính kèm `01_BRAND/Character_Bible/cloud_explorers_character_sheet.png`. Lưu `02_ASSET_LIBRARY/Characters/Valley_Critters/concept/valley_critters_ref.png`. Thiết kế chọn xong thì ghi vào Character Bible.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style only. Design ONE new background creature species: the tiny creatures of the Valley of Clouds.
- Tiny: about one sixth of the fox's height in the sheet. Round, soft and simple, so they never compete with the four main characters.
- A small rounded bean-shaped body in a soft pastel color that is not orange, green, lavender or aqua (for example pale peach-beige), a slightly lighter belly, two small dot eyes, tiny stubby arms and feet. No horns, no wings, no tail. Not a fox, not a reptile, not a jelly blob.
- Each one wears a single dry leaf on its head like a hat.

A design sheet on a plain light-grey background with the same creature in four poses: 1) sitting droopy and sad under its dry leaf; 2) sighing, the leaf sliding down over its eyes; 3) running, holding a big green leaf over its head like an umbrella; 4) splashing happily in a small puddle. No text, no labels, no logos, no watermark.
```

## Prompt theo giây

Viết tiếng Anh. Dựa theo bài mẫu của Higgsfield (nguồn cuối file), gồm các khối theo thứ tự:

1. **Tiêu đề và tóm tắt:** shot, thời lượng, video-to-video; 1–2 câu: ai, ở đâu, làm gì, kết thúc ra sao.
2. **ACTIVE REFERENCES:** mỗi `@Video`, `@Image` một dòng, nói nó **quyết định gì** và **không lấy gì** (nền, tư thế, ánh sáng của ảnh nhân vật; vật liệu, màu, ánh sáng của previz). Có bảng màu khối → nhân vật.
3. **STYLE:** khối chuẩn bên dưới, giống nhau ở mọi shot. Địa điểm, giờ trong ngày, ánh sáng riêng của cảnh viết ở tóm tắt và TIMELINE, không sửa khối chuẩn.
4. **CHARACTERS:** đặc điểm phải giữ của từng nhân vật lấy từ Character Bible (tỉ lệ, giới hạn khi diễn, đồ mang theo); đúng bao nhiêu nhân vật trong khung.
5. **CAMERA:** bám `@Video1` 1:1, khớp từng khung; một cú liền hay cắt ở giây nào.
6. **RULES:** luật đánh số. Đếm được thì ghi số (bao nhiêu nhân vật, đạo cụ nào ở đâu); không chữ, không logo; không có gì đáng sợ, bạo lực.
7. **TIMELINE:** chia khối 2–5 giây theo cú máy hoặc hành động (cảnh cắt nhanh thì mỗi shot một khối). Mỗi khối:
   - `0–3.5s —` cú máy theo `@Video1` (cỡ cảnh, hướng chuyển động, ví dụ "low frontal, retreating");
   - hành động, mốc nhấn ghi tới 0.1 giây ("at 9.7s Lumo turns the head toward camera");
   - biểu cảm (mắt, miệng, tai, đuôi);
   - `END 3.5s:` trạng thái cuối khối (ai ở đâu, đang làm gì).
8. **AUDIO:** không nhạc, không lời thoại (nhạc và lồng tiếng nhiều thứ tiếng làm ở hậu kỳ).
9. **HOLD:** nhắc lại các khoá quan trọng nhất ở cuối.

Quy tắc viết:
- Mốc trong prompt phải trùng hằng số trong `build_shot.py`. Đối chiếu bằng ảnh tĩnh đúng khung của từng mốc: khung = giây × 24 + 1 (`run.ps1 stills 217,469 -Shot <shot>` cho 9.0 s và 19.5 s).
- Mỗi nhân vật luôn gọi đúng một tên, không thay bằng "the fox", "the hero".
- Mỗi mốc chỉ một hành động chính. Không nhồi nhiều việc hơn số giây cho phép.
- Chữ và video mâu thuẫn về chuyển động thì video thắng (ghi rõ trong prompt).
- **Lời thoại:** ghi khoảng giây nhân vật nói theo kịch bản ("3.0–4.5s Lumo talks, mouth moving, no voice"), giọng lồng ở hậu kỳ. Câu nói không được tạo thêm cảnh: máy vẫn theo previz.
- **Thời lượng mỗi lần sinh:** Seedance 2.5 sinh trọn một đoạn tới 30 giây. Đoạn dài hơn, hoặc nơi chỉ cho 15 giây (Seedance 2.0), thì cắt previz ở chỗ cắt cảnh hoặc chỗ nhân vật dừng, mỗi đoạn một prompt, mốc thời gian tính lại từ 0.
- Ảnh đạo cụ vẽ thêm đồ (ảnh Pocket of Wonders có túi mở, tràn đồ): ghi trong ACTIVE REFERENCES chỉ lấy gì, không lấy gì.
- Những chỗ Seedance hay làm sai (rút từ take 1 của `EP001_Great_Rain_Experiment/sh020`), nên ghi sẵn trong prompt:
  - Nhân vật chỉ lấp ló ở mép khung trong previz dễ bị bỏ, có khi biến mất giữa cú máy: ghi rõ ai ở mép nào, thêm luật "stay visible at that edge, partly cut".
  - Chữ gọi cỡ cảnh ("medium two-shot") làm Seedance kéo chặt khung: ghi thêm "exactly as framed in @Video1, never tighter, never wider".
  - Bố cục của ảnh bối cảnh có thể đè lên previz (cành khô dời chỗ, che mặt nhân vật): ghi vật nào đứng đúng chỗ `@Video1` đặt, không vật gì đi ngang trước mặt nhân vật.
  - Khối nhỏ bị chép nguyên hình (tay cầu của Piko thành bong bóng nước), vật nhỏ bị đổi loại (bông hoa thành mầm cây): ghi khối đó là gì, trông ra sao.
  - Đồ đeo xoay theo hướng mặt (túi Piko thành dây chuyền khi Piko nhìn thẳng): tả cách đeo bằng con số và chữ "never" (một dây chéo, không hai dây).
  - Hướng chỉ của một vật đối xứng (mũi sao tám cánh) không đọc ra: cho một dấu hiệu nhìn thấy, ví dụ tia sáng từ mũi tới vật được chỉ.
  - Vật cầm tay có thể đè lên mặt nhân vật: ghi vật ở đâu so với mặt.
  - Thêm "no voice" vào từng khoảng nói; không viết lời trong ngoặc kép (ví dụ "aha") ở chỗ nhân vật mở miệng.

**STYLE chuẩn:**
```
Soft stylized 3D animated film for young children: rounded soft shapes, pastel colors, warm gentle light, soft shadows. Every character keeps the materials of its reference image. Friendly and safe: nothing scary, no injuries, no realism, no live-action, no text, no logos, no watermarks. Original, no IP.
```

**Khung prompt:**
```
# <SHOT> — <SCENE NAME> (<N>s, video-to-video)

<One or two sentences: who, where, what happens, how it ends.> Video-to-video pass driven by @Video1.

ACTIVE REFERENCES
@Video1 = the Blender previz (<N>s, <N*24> frames, 24fps), frame-aligned. SOLE authority for the camera (path, framing, lens, timing) and for every character's position and motion. Block figures: <RED face = the direction Lumo faces, BLACK = back, GREEN = sides and top>. Every block becomes the real character or object its position implies. Do NOT take any material, color, texture or lighting from it. If the text and the video disagree about motion, the video wins.
@Image1 = Lumo — defines design, proportions, colors, cape and bag. Background, pose and lighting not inherited.
@Image2 = <location> — defines look, palette and light. Layout follows @Video1. Camera angle not inherited.

STYLE
<STYLE chuẩn>

CHARACTERS
Lumo: <proportions and limits from the Character Bible>. Exactly <K> characters in frame, never extras.

CAMERA
Strictly follow the camera work of @Video1, 1:1 and frame-aligned for all <N> seconds. <One continuous take, no cuts. | Cuts exactly at ...>

RULES
1. ...

TIMELINE
0–3.5s — (camera per @Video1: ...) Lumo ... At 2.0s ... Face: ... END 3.5s: ...
3.5–7.0s — ...

AUDIO
No music, no dialogue, no voice. <Sound effects: ... Timed accents: <t>s ..., <t>s ... | No sound at all.>

HOLD
@Video1 camera 1:1 for all <N> seconds. Exactly <K> characters. @Image1 identity constant. No text, no logos, no watermarks.
```

## Soát take

| Kiểm tra | Sai thì |
|---|---|
| Cú máy, cỡ cảnh, chỗ cắt khớp previz từng giây | Nhấn mạnh CAMERA, HOLD; nếu vẫn lệch thì làm previz rõ hơn (khối to hơn, ít vật thừa) |
| Đúng số nhân vật, không người thừa | Thêm số vào RULES, HOLD |
| Nhân vật giống ảnh tham chiếu, đúng tỉ lệ | Sửa tỉ lệ khối trong previz; thêm ý vào CHARACTERS |
| Màu khối không lọt vào hình | Nhấn "do not take color from @Video1" |
| Hành động, biểu cảm, khoảng nói đúng mốc giây | Tách khối TIMELINE nhỏ hơn, mỗi mốc một việc |
| Không chữ, logo, cảnh đáng sợ | Thêm vào RULES |

Ghi kết quả từng take (đạt, lỗi gì) vào cuối `seedance/prompt.md`.

## Chưa chốt

- **Mỗi lần sinh là một shot hay một đoạn nhiều shot.** Bài mẫu của Higgsfield dựng 19 shot trong một previz 30 giây rồi sinh một lần, nhân vật giữ đồng nhất qua các lần cắt. Nếu theo cách này thì thư mục sinh nằm ở cấp đoạn, không ở cấp `sh010/`. Đang thử bằng hai đoạn dưới 30 giây của Cảnh 1 tập 01 (`EP001_Great_Rain_Experiment/sh010`, `sh020`; cả hai đã có prompt, `sh020` có take 1).
- Có cho Seedance sinh tiếng động không, hay làm hết tiếng ở hậu kỳ.
- Take lưu vào git (qua LFS) hết, hay chỉ take được chọn.

## Nguồn

Tra ngày 06/11/2026 (BytePlus ModelArk): [BytePlus ModelArk: Dreamina Seedance](https://docs.byteplus.com/en/docs/ModelArk/2608626) · [DataCamp: Seedance 2.0 API guide](https://www.datacamp.com/tutorial/seedance-2-0-api-guide) · [BytePlus Seedance 2.5 API setup](https://seedance2-5.com/blog/byteplus-seedance-2-5-api) · [Fuser: Seedance 2.5 prompt guide](https://fuser.studio/articles/seedance-2-5-prompt-guide)

Tra ngày 03/11/2026:

[Higgsfield: Blender + Higgsfield workflow (5 ví dụ prompt đầy đủ)](https://higgsfield.ai/@adilinthewild/blogs/this-blender-higgsfield-ai-workflow-changes-how-you-make-ai-video) · [Venice: Seedance 2.0 reference-to-video](https://docs.venice.ai/it/guides/media/seedance-2-0) · [MindStudio: timeline prompting](https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video)
