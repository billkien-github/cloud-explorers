# Dựng shot bằng previz Blender + Seedance

Blender lo phần **đạo diễn**: bối cảnh khối, nhân vật dạng khối, chuyển động, cú máy, nhịp thời gian, tất cả dựng bằng `build_shot.py`. Seedance lo phần **hình**: lấy video previz làm khung (video-to-video), cùng ảnh nhân vật, bối cảnh và prompt viết theo từng giây, rồi vẽ lại thành clip hoàn chỉnh. Camera và timing chốt trong Blender trước khi tốn credit.

Đây là quy trình **đề xuất**, đang thử, chưa có take nào dùng được.

## Seedance ở đâu, giới hạn gì (tra tài liệu chính thức của BytePlus ModelArk ngày 06/11/2026)

- **Nơi chạy:** BytePlus ModelArk, sinh qua API bằng `pipeline/seedance_gen.py` (mục "Sinh qua API"). Clip 16:9, 720p, watermark tắt; `duration` là số nguyên giây; `generate_audio` bật tắt tiếng động.
- **Hai dòng model**, chọn theo số ảnh tham chiếu; dòng 2.0 có ba bậc, dùng từ rẻ tới đắt (mục "Sinh qua API"):

| | Seedance 2.5 | Seedance 2.0 mini | Seedance 2.0 fast | Seedance 2.0 |
|---|---|---|---|---|
| Mã model | `dreamina-seedance-2-5-260628` | `dreamina-seedance-2-0-mini-260615` | `dreamina-seedance-2-0-fast-260128` | `dreamina-seedance-2-0-260128` |
| Giây sinh | 4–30 | 4–15 | 4–15 | 4–15 |
| Ảnh tham chiếu | tối đa 30 | tối đa 9 | tối đa 9 | tối đa 9 |
| Video tham chiếu | tối đa 10, tổng tối đa 30 giây | tối đa 3, tổng tối đa 15 giây | như mini | như mini |
| Độ phân giải | 480p, 720p, 1080p | 480p, 720p | 480p, 720p | 480p, 720p, 1080p, 4k |
| Giá 480p, 720p khi có video vào (USD / 1 triệu token) | 6.40 | 2.10 | 3.30 | 4.30 |
| Ví dụ: previz 15 giây vào, 15 giây ra, 720p | khoảng $4.15 | khoảng $1.36 | khoảng $2.14 | khoảng $2.79 |

- **Tính tiền:** theo token, chỉ task thành công mới tính. Token ≈ (giây video vào + giây ra) × rộng × cao × 24 / 1024 (720p 16:9 là 1280×720). API chỉ trả số token (`usage.completion_tokens`), không trả tiền. Không có video vào thì đơn giá cao hơn (2.5: 10.70, 2.0: 7.00) nhưng không tính giây video vào; có video vào thì có mức token tối thiểu. Có hay không có tiếng giá như nhau.
- **Tham chiếu:** ảnh (role `reference_image`), video (`reference_video`), tiếng (`reference_audio`). Prompt gọi `@Image1`, `@Video1`, viết liền không cách, số theo thứ tự đưa vào. Ảnh gửi được dạng base64: mỗi ảnh dưới 30 MB, cạnh 300–6000 px, tỉ lệ rộng/cao 0.4–2.5, cả request tối đa 64 MB. Video chỉ nhận URL công khai: mp4 hoặc mov, 24–60 fps, mỗi file tối đa 200 MB, mỗi video từ 2 giây.
- Link video kết quả sống 24 giờ. Thông số và giá đổi nhanh: kiểm tra lại trước mỗi đợt sinh, đổi thì sửa `MODELS` trong `pipeline/seedance_gen.py`.

## Các bước

| # | Bước | Ra cái gì |
|---|---|---|
| 1 | Chọn đoạn từ previz 2D đã chốt của cảnh (`03_CONTENT/PREVIZ_2D.md`): ai, ở đâu, làm gì, mấy giây, cú máy. Liệt kê các thứ cần ảnh tham chiếu của đoạn; quá 9 ảnh thì phân tích và hỏi người dùng trước (mục "Gộp ảnh tham chiếu"). Độ dài đoạn theo model: tối đa 9 ảnh tham chiếu thì đoạn tối đa 15 giây (dòng Seedance 2.0), người dùng chọn giữ hơn 9 ảnh thì đoạn 30 giây (Seedance 2.5) | Mô tả ngắn ở docstring `build_shot.py` |
| 2 | Dựng previz bằng `build_shot.py` (xem "Previz") | `sh010.blend`, `backups/` |
| 3 | Duyệt previz: `run.ps1 stills`, `run.ps1 preview`, in CC bằng `pipeline/cc.py` (`03_CONTENT/PREVIZ_2D.md`, mục CC), rồi `/review <thư mục shot>` (hình có kể đúng kịch bản, nhịp, bố cục). **Chốt timing**: từ đây prompt bám theo từng con số | Bản previz đã chốt |
| 4 | Render video tham chiếu: `run.ps1 ref` (1920x1080, 24 fps, MP4, ít sample cho nhanh, không in CC) | `renders/sh010_ref.mp4` |
| 5 | Chọn ảnh tham chiếu (xem "Ảnh tham chiếu"; quá 9 ảnh: "Gộp ảnh tham chiếu") | Danh sách `@Image`, tấm gộp nếu có |
| 6 | Soạn prompt theo giây (xem "Prompt theo giây"), kèm bảng số tham chiếu → file tải lên → nguồn. Trước khi sinh: `python pipeline/seedance_gen.py <thư mục shot> --dry-run` (model, giới hạn, chi phí ước tính) và `/review <thư mục shot>/seedance/prompt.md` | `seedance/prompt.md` |
| 7 | Sinh qua API: `python pipeline/seedance_gen.py <thư mục shot>` (mục "Sinh qua API"): model theo số ảnh, 16:9, 720p, `duration` bằng `SECONDS` của `build_shot.py`, watermark tắt; tải take về và ghi chi phí | `seedance/sh010_take01.mp4`, một dòng trong `04_PRODUCTION/seedance_log.csv` |
| 8 | Soát take theo bảng "Soát take": `/review <thư mục shot>/seedance/<take>.mp4`. Lỗi do prompt thì sửa prompt; lỗi do previz thì sửa `build_shot.py`, render lại, sửa mốc trong prompt | Take được chọn |
| 9 | Dựng cảnh: ghi take được chọn của từng đoạn vào danh sách dựng `<tập>/canhNN_edit.py`, nối bằng `pipeline/edit.py` (cắt theo `SEGMENT`, CC theo `TIMING`) | `<tập>/renders/canhNN_edit_cc.mp4` + `.srt` |
| 10 | Hậu kỳ ở `05_POST_PRODUCTION/`: lồng tiếng, nhạc; tiếng động lấy từ take, thiếu hay lệch mốc thì bù | |

Thư mục shot thêm `seedance/`:
```
sh010/
├── build_shot.py, sh010.blend, backups/, renders/   (như cũ)
├── renders/seedance_pending.json  task đã gửi mà chưa tải take về, do pipeline/seedance_gen.py ghi (không lên git)
├── renders/seedance_upload/  chỉ khi sinh tay trên console: video1_previz.mp4, image1_<tên>.png…, prompt.txt đúng thứ tự tải lên, do pipeline/seedance_upload.py tạo (không lên git)
└── seedance/
    ├── prompt.md            prompt đã gửi (tiếng Anh) + file tham chiếu theo số @Image + ghi nhận từng take
    └── sh010_take01.mp4     clip Seedance trả về, giữ nguyên, không sửa
```

## Sinh qua API

Claude chạy `pipeline/seedance_gen.py`, không cần mở console: script đọc `seedance/prompt.md` (bảng số tham chiếu và khối prompt), chọn model, gửi ảnh và video, chờ, tải take về `seedance/<shot>_takeNN.mp4` (số take tự tăng) và ghi chi phí.

```bash
python pipeline/seedance_gen.py <thư mục shot> --dry-run   # in model, tham chiếu, chi phí ước tính, lỗi; không gửi
python pipeline/seedance_gen.py <thư mục shot>             # gửi thật, chờ tới khi xong (vài phút tới vài chục phút)
python pipeline/seedance_gen.py <thư mục shot> --resume    # chờ tiếp task đã gửi (hết giờ chờ, mất mạng lúc tải take)
```

Tuỳ chọn khác (`--model`, `--resolution`, `--no-audio`, `--duration`, `--wait`) ở docstring của script.

- **Chọn model và độ dài đoạn:** đoạn có tối đa 9 ảnh tham chiếu (`ANH_IT` trong script) dùng dòng Seedance 2.0, dài tối đa 15 giây, bắt đầu ở bản mini; take chưa đạt vì chất lượng hình (không phải lỗi prompt hay previz) thì sinh lại bằng `--model 2.0-fast`, vẫn chưa đạt thì `--model 2.0` (dry-run in giá từng bậc; bậc đã dùng xem ở cột `model` của log); nhiều ảnh hơn thì **không tự gửi**: script dừng, phải hỏi người dùng gộp ảnh xuống 9 hay giữ nguyên (mục "Gộp ảnh tham chiếu"). Người dùng chọn giữ nguyên thì dùng Seedance 2.5 (`--model 2.5`), cắt đoạn dài 30 giây và sinh trọn một lần (đoạn cuối của cảnh có thể ngắn hơn). Chia đoạn theo luật này ngay từ bước 1 (mục "Previz", ý "Một cảnh dài chia nhiều đoạn"; mỗi đoạn một prompt, mốc tính lại từ 0). Đoạn tối đa 9 ảnh mà dài hơn 15 giây thì script dừng, không gửi; muốn sinh nguyên đoạn bằng 2.5 (đắt hơn) cũng phải hỏi người dùng trước. Đoạn 2.5 ngắn hơn 30 giây thì dry-run in gợi ý.
- **Chạy từ Claude:** chạy `--dry-run` trước và sửa hết lỗi, rồi chạy thật ở chế độ nền (một lần sinh lâu hơn giới hạn 2 phút của một lệnh). Mỗi lần chạy thật là một lần trả tiền.
- **Biến môi trường**, người dùng tự đặt (`~/.zshrc` trên macOS, `setx` trên Windows), không ghi vào repo hay vào chat:
  - `ARK_API_KEY`: API key của ModelArk.
  - API chỉ nhận video tham chiếu qua URL, nên script tải video previz lên một bucket riêng tư trên **Cloudflare R2** (BytePlus TOS chỉ bán cho tài khoản doanh nghiệp), đưa ModelArk link ký sẵn có hạn, task xong thì xoá file. R2 miễn phí 10 GB lưu trữ và không tính tiền tải xuống; mỗi lần chỉ một file vài chục MB nằm trên bucket trong lúc sinh. Cần `S3_ENDPOINT`, `S3_BUCKET`, `S3_ACCESS_KEY`, `S3_SECRET_KEY`. Script ký link theo chuẩn S3 nên đổi sang dịch vụ chuẩn S3 khác chỉ cần đổi bốn biến này, có khi thêm `S3_REGION`.
  - Thiết lập R2 một lần: bật R2 trong trang Cloudflare (có thể phải thêm thẻ dù dùng gói miễn phí); tạo bucket (để mặc định, không bật truy cập công khai) → tên bucket là `S3_BUCKET`; trong Settings của bucket, Object Lifecycle Rules → Add rule cho tiền tố `seedance/`, xoá file sau 2 ngày, để file sót (máy tắt giữa chừng) tự dọn; ở trang R2, Manage API tokens → tạo token quyền Object Read & Write, chỉ cho bucket đó: Access Key ID → `S3_ACCESS_KEY`, Secret Access Key → `S3_SECRET_KEY` (chỉ hiện một lần), endpoint S3 dạng `https://<ACCOUNT_ID>.r2.cloudflarestorage.com` → `S3_ENDPOINT`.
- **Log chi phí:** mỗi task kết thúc thêm một dòng vào `04_PRODUCTION/seedance_log.csv` (lên git, đọc lại để làm báo cáo): thời gian, shot, take, model, mã task, trạng thái, độ phân giải, giây sinh, số ảnh và video, giây video vào, có tiếng không, token, đơn giá, `cost_usd`, ước tính, lỗi. `cost_usd` = token × đơn giá niêm yết lúc chạy, chưa trừ gói tiết kiệm hay resource pack; số tiền thật xem ở Billing của BytePlus. Task lỗi, bị chặn hay bị từ chối ghi `cost_usd` 0.
- Sinh tay trên console vẫn được: `python pipeline/seedance_upload.py <thư mục shot>` chép video previz, từng ảnh (tên theo số) và `prompt.txt` vào `renders/seedance_upload/` đúng thứ tự tải lên.

## Previz

- **Mốc thời gian khai báo thành hằng số ở đầu `build_shot.py`**, mỗi khoá máy có chú thích cỡ cảnh và ý đồ. Prompt lấy số từ đây, không đo lại bằng mắt. Shot thuộc một cảnh đã có previz 2D thì đầu `build_shot.py` khai `TIMING = "<đường dẫn timing.py của cảnh, tính từ gốc repo>"` và `OFFSET = <giây bắt đầu của đoạn trong cảnh>`, lấy mốc từ `timing.py` trừ `OFFSET`, không gõ lại số. `check_prompt.py` của `/review` đọc theo cặp này.
- **Chuyển động đọc được ở cỡ cảnh của shot:** đủ biên độ, có giữ tư thế. Seedance bám chuyển động của previz ("video wins"), nên một động tác previz làm quá nhỏ (tay rụt vài độ) thì take coi như không có.
- **Nhân vật dạng khối đúng chiều cao và tỉ lệ trong `01_BRAND/Character_Bible/README.md`.** Khối sai tỉ lệ thì Seedance kéo nhân vật theo.
- **Màu khối** để Seedance biết ai là ai, quay hướng nào (bảng màu ghi vào prompt):
  - Một nhân vật: đỏ = mặt trước, đen = lưng, xanh lá = hai bên và đỉnh.
  - Từ hai nhân vật: mỗi nhân vật một màu cố định (Lumo cam, Tavi xanh lá, Nori tím nhạt, Piko xanh ngọc), mặt trước đầu có ô trắng báo hướng nhìn. Bối cảnh, đạo cụ để xám để không lẫn màu nhân vật.
- **Khối 4 nhân vật**, máy quay, tự kiểm khung và cài đặt render ở `pipeline/blocks.py`.
- **Một cảnh dài chia nhiều đoạn:** bối cảnh và diễn của cả cảnh viết một lần trong `<tập>/canhNN_blocks.py` (hàm `build(timing, offset, seconds, out_blend)`); mỗi đoạn là một thư mục shot, `build_shot.py` chỉ khai `TIMING`, `OFFSET`, `FPS, SECONDS` rồi gọi `build`. Danh sách cú máy của đoạn lấy từ `SHOTS` của `timing.py`. CC in bằng `pipeline/cc.py` với giây bắt đầu của đoạn. ModelArk nhận số nguyên giây, nên `SECONDS` làm tròn lên số nguyên và `SEGMENT` ghi độ dài đoạn trong cảnh: máy quay chỉ dựng các cú trong `SEGMENT`, phần dư giữ cú máy cuối, lúc dựng `pipeline/edit.py` cắt bỏ; `check_prompt.py` đọc cả hai.
- **Vật hiện ra, biến mất** bằng key scale 0 và 1 cách nhau ít nhất một khung; hai key gần hơn một khung rơi vào cùng khung và vật lộ dần từ key trước đó.
- **Vật cầm tay:** khối tay bọc lấy đầu cán như nắm tay, vật hơi chếch khỏi trục tay; đặt vật ở bên hông hay cạnh đầu, không chĩa vào mặt. Que nối thẳng từ một quả cầu tay sát mặt thì Seedance vẽ tay thành bong bóng có que xuyên qua và đưa vật vào miệng (take thử Cảnh 1 tập 01). Vật nhỏ làm to hơn cỡ thật một chút cho đọc được.
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

### Gộp ảnh tham chiếu

Dòng Seedance 2.0 nhận tối đa 9 ảnh và rẻ hơn 2.5 nhiều, nên đoạn cần hơn 9 ảnh thì **không tự gửi bằng 2.5**, kể cả khi `seedance_gen.py` được gọi thẳng (script dừng ở `--model auto`). Làm theo thứ tự:

1. **Phân tích:** liệt kê từng ảnh của đoạn, mỗi ảnh để làm gì, lên hình bao lâu, to hay nhỏ trong khung. Đề xuất cụ thể bỏ ảnh nào, gộp những ảnh nào thành tấm nào, để còn tối đa 9 ảnh.
2. **Hỏi người dùng** trước khi làm gì tiếp, kèm: số ảnh hiện có, đề xuất ở bước 1, chi phí hai cách (dry-run in sẵn: gộp xuống 9 ảnh dùng dòng 2.0, giữ nguyên dùng 2.5), chỗ có thể kém đi nếu gộp (chi tiết nhỏ của món bị thu nhỏ). Người dùng quyết; không tự chọn thay.
3. **Gộp:** người dùng đồng ý thì ghép theo đề xuất đã duyệt, sửa bảng số và ACTIVE REFERENCES, chạy lại dry-run. Người dùng chọn giữ nguyên thì chạy với `--model 2.5` và cắt đoạn 30 giây.

Cái gì nên bỏ, nên gộp (đề xuất theo thứ tự này):
- **Bỏ** ảnh của thứ chỉ thoáng qua, nhỏ, ở xa, hoặc prompt tả đủ (que khô, hòn đá, cỏ): chỉ giữ ảnh cho thứ người xem phải nhận ra.
- **Gộp đạo cụ** cùng lên hình trong đoạn vào một tấm, mỗi món một ô; ưu tiên các món nhỏ, đơn giản.
- **Gộp nhân vật nền**, sinh vật cùng loại, hoặc các trạng thái của cùng một vật (trước, sau khi biến đổi) vào một tấm.
- **Dùng ảnh đã gộp sẵn** nếu có, ví dụ ảnh nhân vật đang đeo đồ thay cho hai ảnh nhân vật và đồ.
- **Không gộp:** bốn nhân vật chính (mỗi người giữ ảnh xoay cố định cho mọi shot), ảnh bối cảnh, và món chính của đoạn nếu có cận cảnh (cần đủ chi tiết).

Ghép tấm bằng `pipeline/turnaround.py` với `--hop` (cách chạy ở docstring): nền xám trơn, mỗi món một ô, tự xếp hàng cho tỉ lệ nằm trong giới hạn của API. Lưu tấm ở `seedance/` của shot, tên `sheet_<nội dung>.png` (ví dụ `sheet_compass_lens_rope.png`), ghi lệnh ghép dưới bảng số trong `prompt.md` để ghép lại được khi ảnh gốc đổi. Ghi trong ACTIVE REFERENCES: `@Image6 = prop sheet of separate objects, left to right: the Wonder Compass, the Story Lens, the coiled rope. Each object appears alone; layout, background and relative size not inherited.` Cỡ thật của từng món tả trong CHARACTERS hoặc TIMELINE.

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
8. **AUDIO:** tiếng động do Seedance sinh (`generate_audio` bật, mặc định của `seedance_gen.py`): tả tiếng động của đoạn và các mốc nhấn theo giây (Timed accents), trùng mốc hành động. Không nhạc, không lời thoại: nhạc và lồng tiếng nhiều thứ tiếng làm ở hậu kỳ.
9. **HOLD:** nhắc lại các khoá quan trọng nhất ở cuối.

Quy tắc viết:
- Mốc trong prompt phải trùng hằng số trong `build_shot.py`. Đối chiếu bằng ảnh tĩnh đúng khung của từng mốc: khung = giây × 24 + 1 (`run.ps1 stills 217,469 -Shot <shot>` cho 9.0 s và 19.5 s).
- Mỗi nhân vật luôn gọi đúng một tên, không thay bằng "the fox", "the hero".
- Mỗi mốc chỉ một hành động chính. Không nhồi nhiều việc hơn số giây cho phép.
- Chữ và video mâu thuẫn về chuyển động thì video thắng (ghi rõ trong prompt).
- **Lời thoại:** ghi khoảng giây nhân vật nói theo kịch bản ("3.0–4.5s Lumo talks, mouth moving, no voice"), giọng lồng ở hậu kỳ. Câu nói không được tạo thêm cảnh: máy vẫn theo previz.
- **Thời lượng mỗi lần sinh:** Seedance 2.0 sinh tối đa 15 giây, Seedance 2.5 tới 30 giây; đoạn cắt theo model (mục "Sinh qua API"). Đoạn dài hơn thì cắt previz ở chỗ cắt cảnh hoặc chỗ nhân vật dừng, mỗi đoạn một prompt, mốc thời gian tính lại từ 0.
- **Độ dài prompt:** BytePlus khuyên tối đa 1.000 từ tiếng Anh, dài hơn thì model dễ bỏ chi tiết (`seedance_gen.py` cảnh báo). Prompt hai đoạn thử Cảnh 1 tập 01 dài 2.700–3.250 từ.
- Ảnh đạo cụ vẽ thêm đồ (ảnh Pocket of Wonders có túi mở, tràn đồ): ghi trong ACTIVE REFERENCES chỉ lấy gì, không lấy gì.
- Những chỗ Seedance hay làm sai (rút từ take thử Cảnh 1 tập 01), nên ghi sẵn trong prompt:
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
No music, no dialogue, no voice. Sound effects: ... Timed accents: <t>s ..., <t>s ...

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
| Tiếng động đúng mốc nhấn; không nhạc, không giọng nói | Sửa Timed accents trong AUDIO cho trùng mốc hành động; nhấn "no music, no voice" ở AUDIO và HOLD. Lỗi nhỏ để hậu kỳ bù |

Ghi kết quả từng take (đạt, lỗi gì) vào cuối `seedance/prompt.md`.

## Chưa chốt

- **Mỗi lần sinh là một shot hay một đoạn nhiều shot.** Bài mẫu của Higgsfield dựng 19 shot trong một previz 30 giây rồi sinh một lần, nhân vật giữ đồng nhất qua các lần cắt. Nếu theo cách này thì thư mục sinh nằm ở cấp đoạn, không ở cấp `sh010/`.
- Take lưu vào git (qua LFS) hết, hay chỉ take được chọn.

## Nguồn

Tra ngày 06/11/2026 (tài liệu chính thức của BytePlus): [ModelArk: Create a video generation task](https://docs.byteplus.com/en/docs/modelark/create-video-generation-task-api) · [ModelArk: Retrieve a video generation task](https://docs.byteplus.com/en/docs/modelark/get-video-generation-task-api) · [ModelArk: Pricing](https://docs.byteplus.com/en/docs/modelark/model-pricing) · [Cloudflare R2: Presigned URLs](https://developers.cloudflare.com/r2/api/s3/presigned-urls/) · [Cloudflare R2: Object lifecycles](https://developers.cloudflare.com/r2/buckets/object-lifecycles/) · [Fuser: Seedance 2.5 prompt guide](https://fuser.studio/articles/seedance-2-5-prompt-guide)

Tra ngày 03/11/2026:

[Higgsfield: Blender + Higgsfield workflow (5 ví dụ prompt đầy đủ)](https://higgsfield.ai/@adilinthewild/blogs/this-blender-higgsfield-ai-workflow-changes-how-you-make-ai-video) · [Venice: Seedance 2.0 reference-to-video](https://docs.venice.ai/it/guides/media/seedance-2-0) · [MindStudio: timeline prompting](https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video)
