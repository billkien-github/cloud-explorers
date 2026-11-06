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
| 1 | Chia cảnh (previz 2D đã chốt, `03_CONTENT/PREVIZ_2D.md`) thành các đoạn theo mục "Chia cảnh thành đoạn": chạy `pipeline/chia_doan.py`, chọn cách nối theo nhịp truyện. Mỗi đoạn: ai, ở đâu, làm gì, mấy giây, cú máy; liệt kê các thứ cần ảnh tham chiếu, quá 9 ảnh thì phân tích và hỏi người dùng trước (mục "Gộp ảnh tham chiếu") | Mô tả ngắn ở docstring `build_shot.py` |
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

## Chia cảnh thành đoạn

Mỗi lần gọi API sinh một **đoạn**: nhiều cú máy liền nhau của một cảnh, như bài mẫu của Higgsfield (trong một lần sinh, nhân vật giữ đồng nhất qua các cú cắt). Chỗ nối hai đoạn là chỗ dễ lộ nhất, vì hai lần sinh khác nhau đôi chút về ánh sáng, màu, chi tiết nhân vật. Chia theo thứ tự:

1. **Chỉ nối ở điểm cắt máy** giữa hai cú liền nhau trong `SHOTS` của `timing.py`: người xem đã chờ một cú cắt ở đó nên khác biệt nhỏ không lộ. Không bao giờ nối giữa một cú (giữa một chuyển động máy, một hành động liền). Cú nào một mình dài quá giới hạn thì thêm điểm cắt máy trong previz 2D (sửa `timing.py`, review lại), hay dùng 2.5 cho cảnh (đắt hơn, hỏi người dùng).
2. **Độ dài theo model, tính cả đuôi:** dòng 2.0 tối đa 15 giây, 2.5 tối đa 30 giây. **Đuôi** ít nhất 0.5 giây: cú máy cuối giữ thêm sau `SEGMENT`, lúc dựng `pipeline/edit.py` cắt bỏ, để chỗ nối không rơi vào mấy khung cuối của take (hay chững, trôi). `SECONDS` = `SEGMENT` + đuôi, làm tròn lên số nguyên, ít nhất 4.
3. **Ít đoạn nhất** (mỗi chỗ nối là một rủi ro, mỗi đoạn tốn thêm đuôi), không có đoạn vụn, các đoạn đều nhau. `python pipeline/chia_doan.py <timing.py> [--max 15|30]` tính mọi cách thoả luật 1–3, in vài cách tốt nhất với `OFFSET`, `SEGMENT`, `SECONDS` của từng đoạn và hai cú máy hai bên mỗi chỗ nối.
4. **Chọn theo nhịp truyện** trong các cách script đưa ra, không lấy máy móc cách đầu: chỗ nối nên rơi vào chỗ chuyển ý, đổi địa điểm, đổi nhóm nhân vật, đổi cỡ cảnh mạnh (toàn sang cận), hoặc sau khi một câu thoại, một khoảnh khắc đã khép lại. Tránh nối giữa một cặp hành động – phản ứng (vấp và được kéo lại, hỏi và đáp, rút la bàn và kim quay), và giữa hai cú cùng góc máy, cùng cỡ cảnh (cắt nhảy, lệch lộ nhất). Chỗ nối làm mỗi đoạn ít nhân vật, ít đạo cụ hơn thì tốt hơn (đoạn dễ vào 9 ảnh). Ví dụ Cảnh 1 tập 01, giới hạn 30 giây: script xếp nối ở 26.4 s (đều hơn) trước 28.8 s, nhưng 28.8 s (hết cận la bàn, trước "Có gì lạ kìa!") mới là chỗ chuyển ý.
5. **Giữ liền giữa các đoạn của một cảnh:**
   - Cùng model, cùng bậc, cùng độ phân giải. Nâng bậc một đoạn (mini → fast → 2.0) thì xem chỗ nối với đoạn kề; lệch thì hỏi người dùng có sinh lại đoạn kề bằng bậc đó không.
   - Cùng ảnh tham chiếu cho cùng một thứ; khối STYLE, CHARACTERS và câu tả địa điểm, giờ, ánh sáng chép nguyên giữa các prompt, chỉ bớt nhân vật không có mặt.
   - Khối TIMELINE đầu của đoạn sau mở bằng đúng trạng thái `END` của đoạn trước: ai ở đâu, cầm gì, biểu cảm, đồ vật đã đổi (Piko đã ướt sau cú húp, cái thìa đã cong). Mốc trong prompt tính lại từ 0 của đoạn (mốc trong cảnh trừ `OFFSET`).
   - Tiếng động của mỗi take dừng ở chỗ nối; tiếng nền của cả cảnh (gió, côn trùng) trải liền ở hậu kỳ.
6. **Soát chỗ nối:** đủ take các đoạn thì dựng cả cảnh bằng `pipeline/edit.py`, xem từng chỗ nối (ánh sáng, màu, chi tiết nhân vật, vị trí, hướng nhìn); lệch thì sửa prompt đoạn lệch rồi sinh lại đoạn đó.

## Sinh qua API

Claude chạy `pipeline/seedance_gen.py`, không cần mở console: script đọc `seedance/prompt.md` (bảng số tham chiếu và khối prompt), chọn model, gửi ảnh và video, chờ, tải take về `seedance/<shot>_takeNN.mp4` (số take tự tăng) và ghi chi phí.

```bash
python pipeline/seedance_gen.py <thư mục shot> --dry-run   # in model, tham chiếu, chi phí ước tính, lỗi; không gửi
python pipeline/seedance_gen.py <thư mục shot>             # gửi thật, chờ tới khi xong (vài phút tới vài chục phút)
python pipeline/seedance_gen.py <thư mục shot> --resume    # chờ tiếp task đã gửi (hết giờ chờ, mất mạng lúc tải take)
```

Tuỳ chọn khác (`--model`, `--resolution`, `--no-audio`, `--duration`, `--wait`) ở docstring của script.

- **Chọn model và độ dài đoạn:** đoạn có tối đa 9 ảnh tham chiếu (`ANH_IT` trong script) dùng dòng Seedance 2.0, dài tối đa 15 giây, bắt đầu ở bản mini; take chưa đạt vì chất lượng hình (không phải lỗi prompt hay previz) thì sinh lại bằng `--model 2.0-fast`, vẫn chưa đạt thì `--model 2.0` (dry-run in giá từng bậc; bậc đã dùng xem ở cột `model` của log); nhiều ảnh hơn thì **không tự gửi**: script dừng, phải hỏi người dùng gộp ảnh xuống 9 hay giữ nguyên (mục "Gộp ảnh tham chiếu"). Người dùng chọn giữ nguyên thì dùng Seedance 2.5 (`--model 2.5`), cắt đoạn dài 30 giây và sinh trọn một lần (đoạn cuối của cảnh có thể ngắn hơn). Chia đoạn theo luật này ngay từ bước 1 (mục "Chia cảnh thành đoạn"). Đoạn tối đa 9 ảnh mà dài hơn 15 giây thì script dừng, không gửi; muốn sinh nguyên đoạn bằng 2.5 (đắt hơn) cũng phải hỏi người dùng trước. Đoạn 2.5 ngắn hơn 30 giây thì dry-run in gợi ý.
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
- **Một cảnh dài chia nhiều đoạn:** bối cảnh và diễn của cả cảnh viết một lần trong `<tập>/canhNN_blocks.py` (hàm `build(timing, offset, seconds, out_blend)`); mỗi đoạn là một thư mục shot, `build_shot.py` chỉ khai `TIMING`, `OFFSET`, `FPS, SECONDS` rồi gọi `build`. Danh sách cú máy của đoạn lấy từ `SHOTS` của `timing.py`. CC in bằng `pipeline/cc.py` với giây bắt đầu của đoạn. Điểm nối và độ dài theo mục "Chia cảnh thành đoạn": `SEGMENT` ghi độ dài đoạn trong cảnh, `SECONDS` = `SEGMENT` + đuôi làm tròn lên: máy quay chỉ dựng các cú trong `SEGMENT`, phần dư giữ cú máy cuối, lúc dựng `pipeline/edit.py` cắt bỏ; `check_prompt.py` đọc cả hai.
- **Vật hiện ra, biến mất** bằng key scale 0 và 1 cách nhau ít nhất một khung; hai key gần hơn một khung rơi vào cùng khung và vật lộ dần từ key trước đó.
- **Vật cầm tay:** khối tay bọc lấy đầu cán như nắm tay, vật hơi chếch khỏi trục tay; đặt vật ở bên hông hay cạnh đầu, không chĩa vào mặt. Que nối thẳng từ một quả cầu tay sát mặt thì Seedance vẽ tay thành bong bóng có que xuyên qua và đưa vật vào miệng (take thử Cảnh 1 tập 01). Vật nhỏ làm to hơn cỡ thật một chút cho đọc được.
- **Bối cảnh:** chỉ cần đúng khối, kích thước, vật cản và đạo cụ chính. Hình thật do ảnh tham chiếu và prompt quyết định.
- **Bố trí để thấy mặt:** nhân vật nhìn thẳng vào vật chính (máy, cửa) thì máy quay phía trước chỉ thấy lưng. Đặt chỗ tương tác ở hông vật để nhân vật đứng nghiêng về phía máy quay; tránh để hai, ba nhân vật thẳng hàng với máy quay (che nhau).
- **Nhiều shot trong một previz:** mỗi shot một camera, cắt bằng timeline marker gắn camera; danh sách `SHOTS` ở đầu script ghi giây bắt đầu, kết thúc.
- **Cú nhìn của nhân vật** (nhìn xuống vật trong tay): máy đặt ở chỗ mắt, nhìn vào vật; đầu nhân vật ẩn bằng scale 0 suốt cú đó để không che máy; tay hiện ở đáy khung (Cảnh 1 tập 000A, S2 và S6). Mọi thay đổi chỉ dành cho một cú (ẩn đầu, ẩn vật che máy) chỉ áp khi cú đó thuộc đoạn đang dựng: đuôi của đoạn trước giữ máy cú cuối nên sẽ thấy thay đổi đó (Lumo mất đầu ở đuôi `sh010`).
- **Chữ** (tên phim, biển hiệu) không dựng trong previz khối, thêm ở hậu kỳ: chữ trong video dẫn sẽ lọt vào take.
- **Tự kiểm tra trong script:** máy không ra ngoài bối cảnh, không chui xuống đất (cảnh có dốc, hố thì truyền `ground` cho `check_in_frame`), đầu nhân vật luôn trong khung. Kiểm tra này không bắt được nhân vật bị che, vẫn phải xem ảnh tĩnh từng shot.
- Previz không có mặt: biểu cảm, mắt, miệng, tai, đuôi chỉ có trong prompt.

## Ảnh tham chiếu

- **Chọn ảnh đầy đủ nhất về hình**, mỗi asset một ảnh để tiết kiệm suất `@Image`: ảnh xoay (trước và sau trong một ảnh) hơn ảnh một mặt, ảnh 3/4 hơn ảnh nhìn thẳng, nền trơn hơn ảnh có bối cảnh. Ảnh sinh cho từng tập: `02_ASSET_LIBRARY/MODELING.md`, mục "Ảnh cho một tập".
- Mỗi nhân vật **một ảnh cố định cho mọi shot** để giữ nhân vật đồng nhất: ảnh xoay `02_ASSET_LIBRARY/Characters/<Tên>/concept/<tên>_turnaround.png` (nhìn trước bên trái, nhìn sau bên phải, nền trơn; ghép bằng `pipeline/turnaround.py`). Ảnh xoay của Piko ghép từ ảnh Piko đeo Pocket of Wonders. Nhân vật chưa có ảnh xoay thì dùng `<tên>_ref.png`.
  - Ghi trong ACTIVE REFERENCES: `@Image1 = Lumo turnaround sheet: left front view, right back view of ONE character. Layout, background and pose not inherited.`
  - Chưa thử trong take nào: take đầu dùng ảnh xoay thì soát xem Seedance có vẽ hai bản của cùng một nhân vật không, và mặt sau có đúng khi nhân vật quay lưng.
- Bối cảnh: ảnh riêng của từng địa điểm, chưa có thì `01_BRAND/Brand_Guideline/world_key_art.png`. Đã có: Thung lũng Mây khô hạn (Cảnh 1 tập 01) `02_ASSET_LIBRARY/Environments/Cloud_Valley/concept/cloud_valley_dry_hero.png`; các địa điểm của EP000A (bảng "Tập 000A" trong `02_ASSET_LIBRARY/MODELING.md`).
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

**Bối cảnh EP000A.** Bảng và thứ tự sinh: `02_ASSET_LIBRARY/MODELING.md`, mục "Tập 000A". Mỗi ảnh một chat. Phế tích, vòm đá, bệ đá không mang dáng nơi thờ tự (ghi chú Cảnh 2 của kịch bản); cầu ván không có khung nhìn xuống khe sâu (ghi chú Cảnh 4).

**Rừng Mây** (Cảnh 1). Đính kèm `01_BRAND/Brand_Guideline/world_key_art.png`. Lưu `02_ASSET_LIBRARY/Environments/Cloud_Forest/concept/cloud_forest_hero.png`.
```
The attached image is a style and palette reference only: soft stylized 3D animated film for young children, warm sunlight, pastel colors, floating islands and a cloud sea. Do not copy its layout or its pagodas.

Create a NEW location in the same world: the Cloud Forest, a lush forest on a floating island. One wide 16:9 image, eye level, bright morning, no characters, no animals.
- A wide forest path of soft earth runs from the foreground into the distance on the right, open and inviting.
- Left: the path is blocked by a tall smooth rock wall; right in front of it grows a round bush covered with small fuzzy round burrs (soft-looking, like burdock burrs, no sharp thorns).
- Right side: the path edge drops into a gentle slope covered with a thick layer of dry orange-brown leaves that clearly goes DOWN, away from the viewer, to a lower mossy clearing with a soft pile of leaves at its foot. We look down the slope from the path and see its grassy, mossy bottom clearly; it is gentle, never a cliff. No raised mound of leaves.
- Background: big round tree canopies, and beyond the island's edge other floating islands with waterfalls pouring into the cloud sea.
- Soft rounded shapes, gentle and cheerful. No buildings, no ruins. No text, no logos, no watermark.
```

**Phế tích cổ** (Cảnh 2–3, ngoài trời). Đính kèm `world_key_art.png`. Lưu `02_ASSET_LIBRARY/Environments/Ancient_Ruins/concept/ancient_ruins_hero.png`.
```
The attached image is a style and palette reference only: soft stylized 3D animated film for young children, warm sunlight, pastel colors. Do not copy its layout or its pagodas.

Create a NEW location in the same world: the forgotten ruins of an unknown ancient people who watched the sky, almost swallowed by the Cloud Forest. One wide 16:9 image, eye level, soft daylight, no characters, no animals.
- A mossy clearing with a thick soft carpet of moss and a few flat stone slabs lying on the ground.
- Behind it, a long old stone wall of big rounded weathered blocks with moss and small ferns.
- Along the wall to the right, a thick curtain of hanging vines; through a small gap in the vines, part of a large stone relief carved in the shape of a cloud is visible.
- The only carved symbols are clouds, compass faces and compass-rose stars (four long points alternating with four short points). No eight equal points, no five- or six-pointed stars.
- NOT a temple or shrine: no pagoda roofs, no statues, no altars, no incense, no candles, no lanterns, no religious symbols.
- Big round tree canopies all around. Warm and mysterious, never scary. No text, no logos, no watermark.
```

**Vòm đá** (Cảnh 3, trong vòm). Đính kèm theo thứ tự `ancient_ruins_hero.png`, `01_BRAND/Character_Bible/cloud_explorers_character_sheet.png`. Lưu `02_ASSET_LIBRARY/Environments/Ancient_Ruins/concept/stone_vault_hero.png`.
```
Image 1 shows the outside of these ruins (soft stylized 3D animated film for young children). Image 2 shows the characters, for scale only. Create the inside: a small old stone vault behind the ruin wall. One wide 16:9 image, eye level, no characters, no animals.
- The same weathered stone and moss as Image 1. A rounded vault ceiling with a few small round openings; daylight spreads softly and evenly through the whole room, with no light beam falling on anything.
- Center: a slim round stone pillar only about as wide as Lumo's shoulders in Image 2, its flat top at Lumo's chest height, so the small compass recess in the middle of the top is within reach of his very short arms. The top is carved like a big compass face, with a shallow round recess the size of a pocket compass in the middle, plain stone, not glowing; clouds and compass-rose stars (four long points alternating with four short points) are carved around its sides.
- Far end: a closed stone door carved all over with cloud shapes.
- Quiet, dusty, a little magical. NOT a temple or shrine: no altar, no statue, no lotus base, no candles, no incense, no offerings, no religious symbols. No text, no logos, no watermark.
```

**Cầu ván cổ qua khe núi** (Cảnh 4; lối nhỏ, lưới dây leo, bệ đá bên kia khe). Đính kèm theo thứ tự `ancient_ruins_hero.png`, `cloud_explorers_character_sheet.png`. Lưu `02_ASSET_LIBRARY/Environments/Ancient_Ruins/concept/vine_bridge_hero.png`.
```
Image 1 shows the ruins (soft stylized 3D animated film for young children). Image 2 shows the characters, for scale only. Create a NEW location behind the ruins: an old wooden bridge across a narrow mountain gorge, seen from a stone doorway on this side. One wide 16:9 image, eye level, soft daylight, no characters, no animals.
- The same weathered stone and moss as Image 1.
- An old plank bridge crosses the gorge straight ahead. Its low side rails, wrapped in green vines, reach the chest of Lumo the fox in Image 2. The planks are weathered and a few look loose.
- Just under the bridge, about one fox-height below it, a thick net of woven green vines stretches like a hammock across the whole gorge from cliff to cliff, hiding everything below. The bottom of the gorge is never visible, no dark drop.
- On the far side: a square stone plinth with a raised eight-pointed compass-rose star on its top like a button (four long points alternating with four short points).
- To the left of the doorway, half hidden behind leafy bushes: a narrow path of wide stone steps set back into the cliff, with a low stone lip on the outer edge and a thick vine handrail at the fox's chest height. It runs along the cliff to the head of the gorge, where the gorge narrows, and around to the plinth. The vine net reaches right up to the foot of this path.
- Calm and adventurous, never scary. No text, no logos, no watermark.
```

**Đỉnh đồi lúc hoàng hôn** (Cảnh 5, lúc hòn đảo chưa hiện). Đính kèm `world_key_art.png`. Lưu `02_ASSET_LIBRARY/Environments/Sunset_Hill/concept/sunset_hill_hero.png`.
```
The attached image is a style and palette reference only: soft stylized 3D animated film for young children, pastel colors, floating islands and a cloud sea. Do not copy its layout or its pagodas.

Create a NEW location in the same world: a gentle grassy hilltop on a floating island at sunset, looking out over a vast cloud sea. One wide 16:9 image, eye level, no characters, no animals.
- Foreground: the soft rounded top of the hill, short grass, a flat smooth rock in the middle, wide enough to lay a map on.
- The hilltop ends a few steps beyond the rock in a soft rounded edge, and from there a wide gentle slope covered with a thick layer of dry orange-brown leaves goes DOWN away from us, so we look down along it and clearly see its grassy bottom with a few bushes. On the right, a stone footpath winds gently down beside the leaf slope. No cliff, no drop.
- Beyond: a vast golden-pink cloud sea under a warm sunset sky. On the horizon a thick bank of clouds hides whatever is behind it; no island visible.
- Peaceful and full of promise. No buildings. No text, no logos, no watermark.
```

**Hòn đảo có Wonder Hub, nhìn từ xa** (Cảnh 5: mây tách, đảo dần hiện ra, đài thiên văn lóe xanh ngọc; post-credit: đảo ở chân trời). Đính kèm theo thứ tự `sunset_hill_hero.png`, `world_key_art.png`. Lưu `02_ASSET_LIBRARY/Environments/Wonder_Hub/concept/wonder_hub_island_hero.png`. Dáng Wonder Hub theo previz 2D Cảnh 2 tập 01 (`03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/canh02/build_shot.py`, đoạn "cú cận: Wonder Hub"): nền tròn thấp màu kem, mái vòm tím nhạt viền vàng, ô cửa tròn khung vàng giữa vòm, khối phụ thấp bên phải.
```
Image 1 is the view from a hilltop at sunset; Image 2 is a style reference only (soft stylized 3D animated film for young children). Create a long telephoto view far across the same cloud sea, in the same sunset light as Image 1. One wide 16:9 image, no characters, no animals. Nothing from Image 1's foreground: no hilltop, no tree, no rock, no grass, no leaves; only the sky, the cloud sea and the island.
- Center, far away and slightly hazy: a floating island emerging as the clouds part around it. On the island, a big rounded hill and, at its foot, a huge ancient observatory.
- The observatory: a wide low round base of cream stone, topped by a big round dome in soft pale lavender with a gold band along its lower rim; one large round window in the front of the dome with a gold frame; a small low cream wing on its right side. Its silhouette reads clearly against the sky.
- The observatory is not glowing in this image; only warm sunset light on the dome.
- Wisps of cloud still drift around the island. Magical, calm and inviting. No text, no logos, no watermark.
```

**Bãi phế liệu** (post-credit EP000A: hộp kim loại, Inventor Pack lóe qua khe nắp cùng nhịp hòn đảo ở chân trời). Đính kèm theo thứ tự `world_key_art.png`, `wonder_hub_island_hero.png`, `02_ASSET_LIBRARY/Props/Inventor_Pack/concept/inventor_pack_ref.png`. Lưu `02_ASSET_LIBRARY/Environments/Junkyard/concept/junkyard_hero.png`.
```
Image 1 is a style and palette reference only (soft stylized 3D animated film for young children); do not copy its layout or its pagodas. Image 2 is a far island with a domed observatory. Image 3 is a backpack, only for the look of its strap. Create a NEW location in the same world: a cozy junkyard of old machine parts at sunset. One wide 16:9 image, eye level, no characters, no animals.
- Soft rounded piles of old gears, springs, pipes, wheels and copper scraps, a little rusty but cute and never dangerous: no sharp edges, no broken glass.
- Center foreground: a dusty old metal box with its lid slightly open; through the gap only one brown leather strap with a gold buckle from Image 3 is visible, nothing else of the backpack.
- Far away on the horizon, behind the piles: the island from Image 2, small and hazy, not glowing.
- Warm sunset light, quiet and a little mysterious. No text, no logos, no watermark.
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
- **Thời lượng mỗi lần sinh, chỗ nối với đoạn trước và sau:** mục "Chia cảnh thành đoạn" (luật 2, 5).
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

- Take lưu vào git (qua LFS) hết, hay chỉ take được chọn.

## Nguồn

Tra ngày 06/11/2026 (tài liệu chính thức của BytePlus): [ModelArk: Create a video generation task](https://docs.byteplus.com/en/docs/modelark/create-video-generation-task-api) · [ModelArk: Retrieve a video generation task](https://docs.byteplus.com/en/docs/modelark/get-video-generation-task-api) · [ModelArk: Pricing](https://docs.byteplus.com/en/docs/modelark/model-pricing) · [Cloudflare R2: Presigned URLs](https://developers.cloudflare.com/r2/api/s3/presigned-urls/) · [Cloudflare R2: Object lifecycles](https://developers.cloudflare.com/r2/buckets/object-lifecycles/) · [Fuser: Seedance 2.5 prompt guide](https://fuser.studio/articles/seedance-2-5-prompt-guide)

Tra ngày 03/11/2026:

[Higgsfield: Blender + Higgsfield workflow (5 ví dụ prompt đầy đủ)](https://higgsfield.ai/@adilinthewild/blogs/this-blender-higgsfield-ai-workflow-changes-how-you-make-ai-video) · [Venice: Seedance 2.0 reference-to-video](https://docs.venice.ai/it/guides/media/seedance-2-0) · [MindStudio: timeline prompting](https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video)
