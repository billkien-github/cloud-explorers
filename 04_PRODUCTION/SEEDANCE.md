# Dựng shot bằng previz Blender + Seedance

Blender lo phần **đạo diễn**: bối cảnh khối, nhân vật dạng khối, chuyển động, cú máy, nhịp thời gian, tất cả dựng bằng `build_shot.py`. Seedance lo phần **hình**: lấy video previz làm khung (video-to-video), cùng ảnh nhân vật, bối cảnh và prompt viết theo từng giây, rồi vẽ lại thành clip hoàn chỉnh. Camera và timing chốt trong Blender trước khi tốn credit.

Quy trình đang dùng cho bản nháp: Cảnh 1 tập 000A dựng tạm bằng bản nháp 480p.

## Seedance ở đâu, giới hạn gì (tra tài liệu chính thức của BytePlus ModelArk ngày 06/11/2026)

- **Nơi chạy:** BytePlus ModelArk, sinh qua API bằng `pipeline/seedance_gen.py` (mục "Sinh qua API"). Clip 16:9, bản nháp 480p (hiện chỉ sinh bản nháp), watermark tắt; `duration` là số nguyên giây; `generate_audio` bật tắt tiếng động.
- **Hai dòng model**; dự án dùng 2.5 (mục "Sinh qua API"), dòng 2.0 chỉ để so:

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
| 1 | Chia cảnh (previz 2D đã chốt, `03_CONTENT/PREVIZ_2D.md`) thành các đoạn theo mục "Chia cảnh thành đoạn": chạy `pipeline/split_segments.py`, chọn cách nối theo nhịp truyện. Mỗi đoạn: ai, ở đâu, làm gì, mấy giây, cú máy; liệt kê các thứ cần ảnh tham chiếu | Mô tả ngắn ở docstring `build_shot.py` |
| 2 | Dựng previz bằng `build_shot.py` (xem "Previz") | `sh010.blend`, `backups/` |
| 3 | Duyệt previz: `run.ps1 stills`, `run.ps1 preview`, in CC bằng `pipeline/cc.py` (`03_CONTENT/PREVIZ_2D.md`, mục CC), rồi `/review <thư mục shot>` (hình có kể đúng kịch bản, nhịp, bố cục). **Chốt timing**: từ đây prompt bám theo từng con số | Bản previz đã chốt |
| 4 | Render video tham chiếu: `run.ps1 ref` (1920x1080, 24 fps, MP4 không tiếng để dài đúng `SECONDS`, ít sample cho nhanh, không in CC) | `renders/sh010_ref.mp4` |
| 5 | Chọn ảnh tham chiếu (xem "Ảnh tham chiếu") | Danh sách `@Image` |
| 6 | Soạn prompt theo giây (xem "Prompt theo giây"), kèm bảng số tham chiếu → file tải lên → nguồn. Trước khi sinh: `python pipeline/seedance_gen.py <thư mục shot> --dry-run` (model, giới hạn, chi phí ước tính) và `/review <thư mục shot>/seedance/prompt.md` | `seedance/prompt.md` |
| 7 | Sinh bản nháp qua API: `python pipeline/seedance_gen.py <thư mục shot>` (mục "Sinh qua API"): Seedance 2.5, draft 480p, 16:9, `duration` bằng `SECONDS` của `build_shot.py`, watermark tắt; tải take về và ghi chi phí | `seedance/takes/sh010_take01.mp4`, một dòng trong `04_PRODUCTION/seedance_log.csv` |
| 8 | Soát take theo bảng "Soát take": `/review <thư mục shot>/seedance/takes/<take>.mp4`. Lỗi do prompt thì sửa prompt; lỗi do previz thì sửa `build_shot.py`, render lại, sửa mốc trong prompt, sinh bản nháp mới | Bản nháp được chọn |
| 9 | Dựng cảnh: ghi take được chọn của từng đoạn vào danh sách dựng `<tập>/sceneNN_edit.py`, nối bằng `pipeline/edit.py` (cắt theo `SEGMENT`, CC theo `TIMING`) | `<tập>/renders/sceneNN_edit_cc.mp4` + `.srt` |
| 10 | Hậu kỳ ở `05_POST_PRODUCTION/`: lồng tiếng, nhạc; tiếng động lấy từ take, thiếu hay lệch mốc thì bù | |

Thư mục shot thêm `seedance/`:
```
sh010/
├── build_shot.py, sh010.blend, backups/, renders/   (như cũ)
├── renders/seedance_pending.json  task đã gửi mà chưa tải take về, do pipeline/seedance_gen.py ghi (không lên git)
├── renders/seedance_upload/  chỉ khi sinh tay trên console: video1_previz.mp4, image1_<tên>.png…, prompt.txt đúng thứ tự tải lên, do pipeline/seedance_upload.py tạo (không lên git)
└── seedance/
    ├── prompt.md            prompt đã gửi (tiếng Anh) + file tham chiếu theo số @Image + ghi nhận từng take
    └── takes/               clip Seedance trả về (sh010_take01.mp4…), giữ nguyên, không sửa; không lên git
                             (sinh lại được từ prompt.md, mã task và chi phí ở 04_PRODUCTION/seedance_log.csv)
```

## Chia cảnh thành đoạn

Mỗi lần gọi API sinh một **đoạn**: nhiều cú máy liền nhau của một cảnh, như bài mẫu của Higgsfield (trong một lần sinh, nhân vật giữ đồng nhất qua các cú cắt). Chỗ nối hai đoạn là chỗ dễ lộ nhất, vì hai lần sinh khác nhau đôi chút về ánh sáng, màu, chi tiết nhân vật. Chia theo thứ tự:

1. **Chỉ nối ở điểm cắt máy** giữa hai cú liền nhau trong `SHOTS` của `timing.py`: người xem đã chờ một cú cắt ở đó nên khác biệt nhỏ không lộ. Không bao giờ nối giữa một cú (giữa một chuyển động máy, một hành động liền). Cú nào một mình dài quá giới hạn thì thêm điểm cắt máy trong previz 2D (sửa `timing.py`, review lại).
2. **Độ dài tối đa 30 giây một đoạn (Seedance 2.5), tính cả đuôi.** **Đuôi** ít nhất 0.5 giây: cú máy cuối giữ thêm sau `SEGMENT`, lúc dựng `pipeline/edit.py` cắt bỏ, để chỗ nối không rơi vào mấy khung cuối của take (hay chững, trôi). `SECONDS` = `SEGMENT` + đuôi, làm tròn lên số nguyên, ít nhất 4.
3. **Ít đoạn nhất** (mỗi chỗ nối là một rủi ro, mỗi đoạn tốn thêm đuôi), không có đoạn vụn, các đoạn đều nhau. `python pipeline/split_segments.py <timing.py>` tính mọi cách thoả luật 1–3, in vài cách tốt nhất với `OFFSET`, `SEGMENT`, `SECONDS` của từng đoạn và hai cú máy hai bên mỗi chỗ nối.
4. **Chọn theo nhịp truyện** trong các cách script đưa ra, không lấy máy móc cách đầu: chỗ nối nên rơi vào chỗ chuyển ý, đổi địa điểm, đổi nhóm nhân vật, đổi cỡ cảnh mạnh (toàn sang cận), hoặc sau khi một câu thoại, một khoảnh khắc đã khép lại. Tránh nối giữa một cặp hành động – phản ứng (vấp và được kéo lại, hỏi và đáp, rút la bàn và kim quay), và giữa hai cú cùng góc máy, cùng cỡ cảnh (cắt nhảy, lệch lộ nhất). Ví dụ Cảnh 1 tập 01, giới hạn 30 giây: script xếp nối ở 26.4 s (đều hơn) trước 28.8 s, nhưng 28.8 s (hết cận la bàn, trước "Có gì lạ kìa!") mới là chỗ chuyển ý.
5. **Giữ liền giữa các đoạn của một cảnh:**
   - Cùng model, cùng độ phân giải (hiện mọi đoạn đều là bản nháp 2.5, 480p).
   - Cùng ảnh tham chiếu cho cùng một thứ; khối STYLE, CHARACTERS và câu tả địa điểm, giờ, ánh sáng chép nguyên giữa các prompt, chỉ bớt nhân vật không có mặt. Mọi vật lên hình ở cả hai đoạn (bụi cây, tảng đá, đạo cụ) phải được tả bằng cùng câu ở cả hai prompt: đoạn sau bỏ câu tả thì Seedance vẽ một vật khác (bụi gai có quả ké tròn ở `sh010` thành bụi gai sẫm gai nhọn ở `sh020`, Cảnh 1 tập 000A).
   - Khối TIMELINE đầu của đoạn sau mở bằng đúng trạng thái `END` của đoạn trước: ai ở đâu, cầm gì, biểu cảm, đồ vật đã đổi (Piko đã ướt sau cú húp, cái thìa đã cong). Mốc trong prompt tính lại từ 0 của đoạn (mốc trong cảnh trừ `OFFSET`).
   - Tiếng động của mỗi take dừng ở chỗ nối; tiếng nền của cả cảnh (gió, côn trùng) trải liền ở hậu kỳ.
6. **Sửa `timing.py` của cảnh đã chia đoạn** (sửa previz khối theo review, kéo dài một cú): chạy `python pipeline/split_segments.py <timing.py> --check <thư mục tập>` và sửa `OFFSET`, `SEGMENT`, `SECONDS` theo kết quả, vì chỉ dời mốc vài phần mười giây cũng có thể đổi số đoạn ít nhất hay đẩy một đoạn qua 30 giây (Cảnh 5 tập 000A dài thêm 0.8 giây thì từ 2 đoạn thành ít nhất 3). Cùng lần đó: dựng và render lại previz 2D của cảnh (`03_CONTENT/PREVIZ_2D.md`) rồi xem lại hình ở các mốc đã dời; tổng thời lượng cảnh đổi thì sửa mốc phút trong beat sheet, tiêu đề cảnh trong `.fountain` và mục Trạng thái của `README.md`. Đoạn `--check` báo sát trần thì biết trước là kéo dài cú nào trong đó cũng phải chia lại.
7. **Soát chỗ nối:** đủ take các đoạn thì dựng cả cảnh bằng `pipeline/edit.py`, xem từng chỗ nối (ánh sáng, màu, chi tiết nhân vật, vị trí, hướng nhìn); lệch thì sửa prompt đoạn lệch rồi sinh lại đoạn đó.

## Sinh qua API

Claude chạy `pipeline/seedance_gen.py`, không cần mở console: script đọc `seedance/prompt.md` (bảng số tham chiếu và khối prompt), gửi ảnh và video, chờ, tải take về `seedance/takes/<shot>_takeNN.mp4` (số take tự tăng) và ghi chi phí.

```bash
python pipeline/seedance_gen.py <thư mục shot> --dry-run   # in model, tham chiếu, chi phí ước tính, lỗi; không gửi
python pipeline/seedance_gen.py <thư mục shot>             # bản nháp 2.5 draft 480p, chờ tới khi xong (vài phút)
python pipeline/seedance_gen.py <thư mục shot> --resume    # chờ tiếp task đã gửi (hết giờ chờ, mất mạng lúc tải take)
```

Tuỳ chọn khác (`--no-audio`, `--duration`, `--wait`) ở docstring của script.

- **Chỉ sinh bản nháp Seedance 2.5** (quyết định của người dùng, 07/11/2026): `draft: true` của API, chỉ ra 480p, tính tiền như video 480p thường (ví dụ đoạn 23 giây khoảng $2.83); đoạn dài tối đa 30 giây. Sửa prompt, previz rồi sinh bản nháp mới tới khi người dùng chốt; dùng bản nháp 480p để dựng trước. **Bản final đang bị chặn**, `seedance_gen.py` không còn đường sinh final (lấy lại từ git khi người dùng mở): API cho sinh bản final 1080p từ ID task của bản nháp trong 14 ngày, dùng lại prompt, tham chiếu, seed, tiếng, tỉ lệ, độ dài, tính tiền riêng theo 1080p kèm giây video tham chiếu (đoạn 23 giây khoảng $15.65; tra ngày 07/11/2026). Không còn sinh bằng dòng 2.0.
- **So model** (`sh010` Cảnh 1 tập 000A, 07/11/2026, cùng prompt, cùng previz): dòng 2.0 chép chiều và bố cục của ảnh tham chiếu; 2.5 bám previz hơn nhưng hay kéo chặt cú trung và cú cận, nên dự án dùng 2.5.
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
- **Cú va chạm hài** (cắm mặt vào bụi, đâm vào vật, ngã) dựng đủ ba nhịp: lấy đà (ưỡn người, hếch cằm), quán tính (sải bước, người còn trôi tới sau lúc chạm, nén lại rồi nảy), và chỗ chạm đủ sâu (đầu lút hẳn vào lá, giữ nguyên ở cú sau). Ngả cứng cả người quanh bàn chân, mặt chỉ chạm mép vật thì take ra gượng, như đang tựa (take thử `sh010` Cảnh 1 tập 000A).
- **Vật lấy ra từ túi, hộp:** cho vật (đang gấp nhỏ) ló ra ở mép miệng túi rồi kéo lên, túi giữ nguyên chỗ và hình; cho vật phóng từ scale 0 ngay trong khối túi thì Seedance biến chính cái túi thành vật đó (túi da tan thành bản đồ, bản nháp `sh020` Cảnh 1 tập 000A).
- **Tay cầm vật phải đi theo vật:** vật xoay, lật, đổi chỗ trong tay thì khối bàn tay làm con của vật hay key cùng nhịp; chỉ xoay vật còn tay đứng yên thì take cho tay buông, vật lơ lửng (xoay bản đồ, bản nháp `sh010`). Vật xoay quá khoảng 45° (bản đồ xoay nửa vòng, cả vòng) thì tay không quay trọn theo vật, vì bàn tay sẽ ra mép xa, quá tầm với: xoay từng nấc ≤ 90° giữa hai bàn tay, giữa các nấc tay nhích về chỗ cũ như đổi tay cầm, và mỗi key vẫn theo luật "Tay với tới đúng chỗ chạm" (Cảnh 5 tập 000A, S10: bàn tay quay theo bản đồ ra cách vai 0.47 m).
- **Tay với tới đúng chỗ chạm:** khối tay dài cố định, nên chỗ bàn tay chạm (mép phiến đá đang nhấc, vật trong hốc, mặt tường lúc gõ) phải cách vai đúng một chiều dài tay ở mọi key; ngắn hơn thì tay xuyên qua vật, dài hơn thì với hụt.
  - Đổi độ chồm, chỗ đứng theo vật (chồm thấp khi mép còn thấp, ngả lên theo mép đang nhấc). Tính chỗ chạm và hướng tay từ toạ độ thật trong script (vị trí vai, `matrix_world` sau khi key tư thế), cả chỗ tai áp tường; không ước bằng mắt.
  - Đo đúng điểm: khối tay Lumo 0.29 m gồm cả bàn tay (cổ tay ở 0.22 m). Chạm bằng đầu tay (gõ, đẩy, ấn) cách vai 0.29 m; chỗ nắm (vành la bàn, cạnh bản đồ) là tâm bàn tay, cách vai khoảng 0.25 m. Khối bàn tay dựng rời (con của vật cầm) thì kiểm tâm của nó ≤ 0.25 m.
- **Phản ứng nhỏ ở cú toàn bị bỏ:** nhổm lên 6 cm trong đống lá không thành hình; phản ứng ở cú toàn cần biên độ cỡ một phần tư chiều cao nhân vật.
- **Máy di chuyển đều** (hạ máy, lia) thì key máy nội suy LINEAR trong previz; để ease thì Seedance dồn chuyển động vào giữa thành một cú vụt (cú hạ máy mở đầu Cảnh 1 tập 000A).
- **Cú trung có toàn thân:** dựng previz rộng hơn ý muốn một chút (ống kính ngắn hơn, chừa khoảng trống dưới chân), vì Seedance hay cắt cú trung chặt lại tới ngang hông.
- **Nhân vật dạng khối đúng chiều cao và tỉ lệ trong `01_BRAND/Character_Bible/README.md`.** Khối sai tỉ lệ thì Seedance kéo nhân vật theo.
- **Màu khối** để Seedance biết ai là ai, quay hướng nào (bảng màu ghi vào prompt):
  - Một nhân vật: đỏ = mặt trước, đen = lưng, xanh lá = hai bên và đỉnh.
  - Từ hai nhân vật: mỗi nhân vật một màu cố định (Lumo cam, Tavi xanh lá, Nori tím nhạt, Piko xanh ngọc), mặt trước đầu có ô trắng báo hướng nhìn. Bối cảnh, đạo cụ để xám để không lẫn màu nhân vật.
- **Khối 4 nhân vật**, máy quay, tự kiểm khung và cài đặt render ở `pipeline/blocks.py`.
- **Một cảnh dài chia nhiều đoạn:**
  - Bối cảnh và diễn của cả cảnh viết một lần trong `<tập>/sceneNN_blocks.py` (hàm `build(timing, offset, seconds, out_blend)`); mỗi đoạn là một thư mục shot, `build_shot.py` chỉ khai `TIMING`, `OFFSET`, `FPS, SECONDS` rồi gọi `build`. Danh sách cú máy của đoạn lấy từ `SHOTS` của `timing.py`; CC in bằng `pipeline/cc.py` với giây bắt đầu của đoạn.
  - Bối cảnh dùng chung nhiều cảnh của tập (cảnh sau nối ngay cuối cảnh trước) dựng một lần trong module cấp tập (`EP000A_Mysterious_Compass/ruins_blocks.py`) để vị trí khớp ở chỗ nối.
  - Điểm nối và độ dài theo mục "Chia cảnh thành đoạn": `SEGMENT` là độ dài đoạn trong cảnh, `SECONDS` = `SEGMENT` + đuôi làm tròn lên. Máy chỉ dựng các cú trong `SEGMENT`; phần đuôi giữ cú máy cuối (máy đang di chuyển đều thì đi tiếp cùng tốc độ), lúc dựng `pipeline/edit.py` cắt bỏ; `check_prompt.py` đọc cả hai.
  - Key diễn "tới hết" trong `build()` tính theo hết cảnh, không theo hết video của đoạn; đặt ở hết video thì đoạn giữa kéo diễn cuối cảnh lên sớm.
- **Vật hiện ra, biến mất:**
  - Bằng key scale 0 và 1 cách nhau ít nhất một khung; hai key gần hơn một khung rơi vào cùng khung và vật lộ dần từ key trước đó.
  - Vật chỉ được lên hình từ một mốc (ánh sáng lộ ra, nhân vật nền chỉ có ở vài cú) thì ẩn bằng scale 0 ở mọi cú trước mốc của cả tập, không chỉ đặt ngoài khung: vật phát sáng hay nhân vật nhỏ lộ một đốm ở mép khung là Seedance vẽ thành thật. Cảnh sau gọi lại hàm bối cảnh chung thì tự ẩn lại những thứ cảnh trước đã tắt, lấy đi.
  - Bối cảnh dựng riêng ở xa cho một cú (hộp đen của khung đen, góc cận dựng riêng) cũng ẩn ngoài cú đó (hộp đen lộ thành ô vuông đen ở chân trời).
  - Thứ kịch bản cho "lộ ra" (lối đi sau bụi, khe sáng sau cánh cửa, phù điêu sau dây leo, bản đồ dưới phiến đá) phải bị che kín từ mọi máy của các cú trước mốc: khe hở vài mm, đỉnh vật nhô quá mặt nắp, dây leo ngắn hơn hốc đều thành lộ sớm. Soát bằng ảnh tĩnh mọi cú trước mốc.
- **Vật phát sáng giữ màu:** với view Standard, cường độ phát sáng cao làm khối cháy thành trắng (ánh xanh ngọc thành đĩa, quả cầu trắng). Giữ cường độ vừa phải (khoảng 1–3 tuỳ màu, xem trên ảnh render), cần nổi hơn thì làm khối to hơn chứ không sáng hơn (Cảnh 4–6 tập 000A). Lóe tín hiệu nối bốn tập (bảo bối lóe cùng nhịp hòn đảo) dùng màu xanh ngọc của luật trong `03_CONTENT/README.md`, không dùng màu phát sáng thường của bảo bối (la bàn lóe vàng, Cảnh 5 tập 000A).
- **Mặt trước khối tròn không có chấm tròn sẫm** (ô cửa trên mái vòm, lỗ trên quả cầu): trước nền sáng, chấm đó đọc thành con mắt và Seedance có thể vẽ thành mặt.
- **Dựng lại từ previz 2D:** previz 2D vẽ theo mặt cắt, xếp vật thành lớp; dựng 3D thì đặt lại theo không gian thật, đừng đùn nguyên mặt cắt (mặt lưới dâng lên chân lối nhỏ thành một bức tường lưới chắn giữa khung, Cảnh 4 tập 000A). Cú ngang và cú nhìn từ trên cùng một nhóm đạo cụ: chọn chỗ đặt sao cho trái–phải của mọi vật và hướng chỉ cuối khớp ở cả hai cú. Máy đẩy của 2D (ortho) thành dolly có phối cảnh, vật ở chân trời không to lên theo: tính cỡ vật xa theo khung cuối (post-credit tập 000A).
- **Nhân vật nhìn vật ở chân trời trong cùng khung:** máy nhìn theo hướng vật thì chỉ thấy lưng; dáng nghiêng của 2D không dựng lại được. Đặt nhân vật sát một mép khung, vật ở mép kia, ống kính 24–26 mm, xoay người chéo 10–15° về phía máy, chỉ quay đầu về vật (thấy nhân vật khoảng 45–55° tính từ sau lưng); ghi góc đó trong prompt (Cảnh 5 tập 000A, S6, S8, S16).
- **Nhân vật lao ra khỏi khung:** cho chạy ngang theo bên phải hay trái của máy, không chạy về hậu cảnh (chạy xa máy thì hết cú vẫn còn trong khung); kiểm lúc ra, vào khung bằng `world_to_camera_view`.
- **Vật vạch ra trước lối đi** (bụi cây, rèm dây leo): nửa ngả về phía máy chắn mọi máy đặt phía trước lối sau đó; cú trên lối dựng máy đi theo sau nhân vật trên chính lối (Cảnh 4 tập 000A, S16). Vạch thì hai nửa ngả sang trái, phải trên màn hình (vuông góc trục nhìn); ngả theo trục sâu thì hai nửa chồng lên nhau, nhìn từ máy không thấy gì lộ ra (Cảnh 4 tập 000A, S12).
- **Hai cú liền nhau khác hẳn góc hoặc cỡ cảnh**, kể cả trong một đoạn (đổi hướng máy từ khoảng 30°, hoặc toàn sang cận): gần cùng góc, cùng cỡ thì thành cắt nhảy, và Seedance dễ bỏ luôn điểm cắt. Dấu hiệu: `review.json` không bắt được điểm cắt có trong `SHOTS`. Bối cảnh cùng một tông nhạt (vòm đá, Cảnh 3 S8→S9 tập 000A) thì máy dò có thể sót cả cú cắt khác hẳn góc; khi đó mở khung hai bên điểm cắt để chốt bằng mắt. Sửa máy một cú thì soát cả cú trước và cú sau nó (Cảnh 3 S3→S4, Cảnh 5 S16→S17 tập 000A; Cảnh 4 S24→S25 do chính lần sửa máy S24 gây ra).
- **Chuyển động nhanh bị đọc thành điểm cắt:** cú quay người khoảng 0.2 giây, cú lùi máy hay đổi ống kính gấp đôi trong dưới 0.5 giây thì `review.json` bắt thành điểm cắt, và take dễ thành cú cắt thật. Quay người từ khoảng 0.6 giây, lùi máy hay đổi ống từ khoảng 1 giây (Cảnh 2 S7, Cảnh 4 S21, Cảnh 5 S9 tập 000A).
- **Ngồi xổm bằng khối:** khối chân thẳng không gập được, ngả cả người quanh bàn chân thì đọc thành sắp cắm đầu. Chĩa khối chân ra trước khoảng 55–65° (dạng sang hai bên nếu phía trước có vật), hạ gốc cho bàn chân chạm đất, độ ngả thân chọn theo tầm với tới chỗ bàn tay chạm (Cảnh 2 tập 000A, S1).
- **Nhân vật chọn một lối giữa hai lối** (lối mòn thay vì dốc lá): máy nhìn dọc lối được chọn, lối chạy từ chân nhân vật vào sâu trong khung, lối bị bỏ ở một mép khung; máy đặt ngang dốc để thấy dốc đổ chéo, nhìn thẳng từ chân dốc thì dốc thành một gò nhô lên (Cảnh 5 tập 000A, S12, S17).
- **Đầu khối cúi tối đa khoảng 25°:** khớp cổ ở đáy khối đầu, cúi sâu hơn trông như cả người chúi tới; vật ở thấp thì cúi thêm bằng thân.
- **Vật cầm tay:** khối tay bọc lấy đầu cán như nắm tay, vật hơi chếch khỏi trục tay; đặt vật ở bên hông hay cạnh đầu, không chĩa vào mặt. Que nối thẳng từ một quả cầu tay sát mặt thì Seedance vẽ tay thành bong bóng có que xuyên qua và đưa vật vào miệng (take thử Cảnh 1 tập 01). Vật nhỏ làm to hơn cỡ thật một chút cho đọc được. Đạo cụ phẳng (bản đồ, tấm bảng) có chi tiết vẽ ở mặt trước thì chi tiết đó không được ló ra mặt sau: ở cú nhìn lưng vật, vệt sẫm trên tấm trắng thành tấm thẻ trong take (bản đồ giấy, `sh010` Cảnh 1 tập 000A).
- **Bối cảnh:** chỉ cần đúng khối, kích thước, vật cản và đạo cụ chính. Hình thật do ảnh tham chiếu và prompt quyết định. Vật lên hình ở nhiều cảnh (hòn đảo Wonder Hub) dựng bằng một hàm dùng chung theo ảnh tham chiếu; mỗi cảnh tự dựng thì dáng lệch nhau và Seedance vẽ thành hai vật khác (Cảnh 5 và post-credit tập 000A).
- **Vật nhỏ mang gag** (hòn sỏi rơi, chiếc lá trượt): khác tông với nền sau nó, đủ to để thấy trên điện thoại (cỡ vài chục pixel ở khung 768), và cả đường rơi, trượt nằm trọn trong khung đủ lâu để mắt bắt kịp; nhân vật nền có cỡ trong Character Bible (chim) thì đưa máy lại gần chứ không phóng to. Vật nhỏ rơi thì làm sẫm, to hơn cỡ thật và rơi đều chậm, để phần rơi trong khung lên hình từ khoảng 0.3 giây. Vật gây ra gag (sỏi rơi khi gõ) có mặt trong khung từ trước và nhúc nhích theo từng nhịp gây ra nó, không chỉ hiện ra lúc rơi. Lượt review đầu Cảnh 2–5 tập 000A: sỏi khoảng 20 px rơi sát mép trên khung, lá khoảng 15 px trượt mất khỏi khung.
- **Bố trí để thấy mặt:** nhân vật nhìn thẳng vào vật chính (máy, cửa) thì máy quay phía trước chỉ thấy lưng. Đặt chỗ tương tác ở hông vật để nhân vật đứng nghiêng về phía máy quay; tránh để hai, ba nhân vật thẳng hàng với máy quay (che nhau).
- **Nhiều shot trong một previz:** mỗi shot một camera, cắt bằng timeline marker gắn camera; danh sách `SHOTS` ở đầu script ghi giây bắt đầu, kết thúc.
- **Cú nhìn của nhân vật** (nhìn xuống vật trong tay): máy đặt ở chỗ mắt, nhìn vào vật; đầu nhân vật ẩn bằng scale 0 suốt cú đó để không che máy; tay hiện ở đáy khung (Cảnh 1 tập 000A, S2 và S6). Mọi thay đổi chỉ dành cho một cú (ẩn đầu, ẩn vật che máy) chỉ áp khi cú đó thuộc đoạn đang dựng: đuôi của đoạn trước giữ máy cú cuối nên sẽ thấy thay đổi đó (Lumo mất đầu ở đuôi `sh010`).
- **Cú cận vật cầm trước ngực mà phải thấy cả thứ vật chỉ tới ở hậu cảnh** (la bàn chỉ về bức tường; lỗi hay gặp nhất ở lượt review đầu Cảnh 2–5 tập 000A):
  - Máy đặt sát bên người thì khối tay, đầu che kín vật: dựng thành cú nhìn của nhân vật (vật giơ trước mắt, mặt vật quay về mắt, đích ở nửa trên khung), hoặc đặt máy trước mặt nhân vật sau khi quay. Cú nhìn là cú cuối của đoạn thì đầu ẩn luôn qua phần đuôi, vì máy ở chỗ mắt.
  - Soát bằng ảnh tĩnh ở mọi điểm dừng của vật (trước và sau mỗi lần nhân vật quay, xoay): mặt vật thấy rõ, không bị tay, thân hay dải CC che; đầu chỉ trên màn hình hướng về đích trên màn hình; đích là một mặt nhìn chéo đủ to, không phải mặt tường nhìn gần song song.
  - Cách đã làm được:
    - Vật chìa ra ngoài thân ở phía máy, mặt quay về máy; tâm vật đặt trước bàn tay khoảng một bán kính vật để tay chỉ nắm mép vỏ, không đè lên mặt vật. Mỗi điểm dừng giữ ít nhất 0.5 giây.
    - Máy sau gáy cách khoảng 0.6 m, ống khoảng 40 mm, ngắm điểm giữa vật và đích (đích xa, tay ngắn); hoặc máy thấp sau vật để đích ở nửa trên khung. Ống rộng đặt trên vai thì đích nhỏ mất.
    - Nhân vật đứng sát mặt phẳng đích (tường): máy ở chỗ mắt chỉ thấy mặt phẳng gần song song. Dựng riêng vật và khối tay trước một máy đặt xa mặt phẳng, thấy chéo từ khoảng 25°; đầu chỉ nhắm vào giao điểm của tia máy–đích với mặt vật, không nhắm thẳng đích 3D, để trên màn hình nó chỉ đúng.
    - Nhân vật quay người khi đang cận vật: nghiêng mặt vật về phía máy ở cả hai hướng, máy ống dài đặt xa, cú quay từ khoảng 0.6 giây.
- **Chữ** (tên phim, biển hiệu) không dựng trong previz khối, thêm ở hậu kỳ: chữ trong video dẫn sẽ lọt vào take.
- **Tự kiểm tra trong script:** máy không ra ngoài bối cảnh, không chui xuống đất (cảnh có dốc, hố thì truyền `ground` cho `check_in_frame`), đầu nhân vật luôn trong khung. Kiểm tra này không bắt được nhân vật bị che, vẫn phải xem ảnh tĩnh từng shot.
- Previz không có mặt: biểu cảm, mắt, miệng, tai, đuôi chỉ có trong prompt.

## Ảnh tham chiếu

- **Chọn ảnh đầy đủ nhất về hình**, mỗi asset một ảnh để tiết kiệm suất `@Image`: ảnh xoay (trước và sau trong một ảnh) hơn ảnh một mặt, ảnh 3/4 hơn ảnh nhìn thẳng, nền trơn hơn ảnh có bối cảnh. Ảnh sinh cho từng tập: `02_ASSET_LIBRARY/MODELING.md`, mục "Ảnh cho một tập".
- Mỗi nhân vật **một ảnh cố định cho mọi shot** để giữ nhân vật đồng nhất: ảnh xoay `02_ASSET_LIBRARY/Characters/<Tên>/concept/<tên>_turnaround.png` (nhìn trước bên trái, nhìn sau bên phải, nền trơn; ghép bằng `pipeline/turnaround.py`). Ảnh xoay của Piko ghép từ ảnh Piko đeo Pocket of Wonders. Nhân vật chưa có ảnh xoay thì dùng `<tên>_ref.png`.
  - Ghi trong ACTIVE REFERENCES: `@Image1 = Lumo turnaround sheet: left front view, right back view of ONE character. Layout, background and pose not inherited.`
  - Đã dùng từ take đầu Cảnh 1 tập 000A: không thấy hai bản của cùng nhân vật, mặt sau đúng khi quay lưng. Chi tiết nhỏ (chỏm lông) vẫn trôi: thêm ảnh cận đúng chi tiết đó.
- Bối cảnh: ảnh riêng của từng địa điểm, chưa có thì `01_BRAND/Brand_Guideline/world_key_art.png`. Đã có: Thung lũng Mây khô hạn (Cảnh 1 tập 01) `02_ASSET_LIBRARY/Environments/Cloud_Valley/concept/cloud_valley_dry_hero.png`; các địa điểm của EP000A (bảng "Tập 000A" trong `02_ASSET_LIBRARY/MODELING.md`).
- Đạo cụ: `02_ASSET_LIBRARY/Props/<Tên>/concept/<tên>_ref.png` (nhìn 3/4, nền trơn). Đạo cụ tập 01 chưa có `_ref` thì dùng `_front.png` (vật dài: `_side.png`), hoặc ảnh trạng thái khi trạng thái đó lên hình (`_frost.png`). Nhân vật nền (sinh vật nhỏ của thung lũng): `02_ASSET_LIBRARY/Characters/Valley_Critters/concept/valley_critters_ref.png`; ghi trong prompt tư thế nào dùng cho clip.
- **Seedance chép chiều của ảnh tham chiếu** (rõ nhất ở dòng 2.0). Vật lên hình ở chiều khác ảnh (bản đồ cầm ngược) thì tải lên ảnh đã xoay đúng chiều đó và ghi trong ACTIVE REFERENCES là ảnh đã ở đúng chiều của cả clip; chỉ dặn bằng chữ thì không đủ (take thử `sh010` Cảnh 1 tập 000A).
- Chỉ đưa ảnh của thứ có trong shot. Số `@Image` theo thứ tự tải lên: mỗi số một ảnh, ghi bảng số → file trong `prompt.md` và soát lại trước khi sinh (bài mẫu của Higgsfield có chỗ hai ảnh cùng ghi `@Image 2`).
- Mọi ảnh tham chiếu (nhân vật phụ, đạo cụ, bối cảnh) sinh bằng ChatGPT theo prompt trong `02_ASSET_LIBRARY/MODELING.md`, mục "Ảnh của từng tập" (bối cảnh: mục con "Bối cảnh" của mỗi tập).

### Gộp ảnh tham chiếu

Seedance 2.5 nhận tối đa 30 ảnh nên hiện chưa cần gộp. Đoạn cần hơn 30 ảnh thì ghép các món nhỏ, nhân vật nền, các trạng thái của một vật vào một tấm bằng `pipeline/turnaround.py --hop` (nền xám trơn, mỗi món một ô, tự xếp cho tỉ lệ trong giới hạn của API), lưu ở `seedance/` của shot tên `sheet_<nội dung>.png`, ghi lệnh ghép dưới bảng số trong `prompt.md`. Không gộp bốn nhân vật chính, ảnh bối cảnh, món chính có cận cảnh. Ghi trong ACTIVE REFERENCES: `@Image6 = prop sheet of separate objects, left to right: … Each object appears alone; layout, background and relative size not inherited.`

## Prompt theo giây

Viết tiếng Anh. Dựa theo bài mẫu của Higgsfield (nguồn cuối file), gồm các khối theo thứ tự:

1. **Tiêu đề và tóm tắt:** shot, thời lượng, video-to-video; 1–2 câu: ai, ở đâu, làm gì, kết thúc ra sao.
2. **ACTIVE REFERENCES:** mỗi `@Video`, `@Image` một dòng, nói nó **quyết định gì** và **không lấy gì** (nền, tư thế, ánh sáng của ảnh nhân vật; vật liệu, màu, ánh sáng của previz). Có bảng màu khối → nhân vật.
3. **STYLE:** khối chuẩn bên dưới, giống nhau ở mọi shot. Địa điểm, giờ trong ngày, ánh sáng riêng của cảnh viết ở tóm tắt và TIMELINE, không sửa khối chuẩn.
4. **CHARACTERS:** đặc điểm phải giữ của từng nhân vật lấy từ Character Bible (tỉ lệ, giới hạn khi diễn, đồ mang theo); đúng bao nhiêu nhân vật trong khung. **Cỡ tương đối:** mọi nhân vật, đạo cụ và vật bối cảnh đứng cạnh nhân vật (bụi cây, tảng đá, bệ, vách) ghi cỡ so với Lumo cao 1.00 m, bằng tỉ lệ chiều cao và một phép so dễ hình dung ("about one tenth of Lumo's height, the size of Lumo's fist"; "waist-high to Lumo"). Số lấy từ `02_ASSET_LIBRARY/MODELING.md`, mục "Bảng cỡ" (đơn vị L = chiều cao Lumo = 1.00 m) và kích thước khối trong previz, không ước bằng mắt; previz lệch bảng thì sửa previz hay bảng trước khi viết prompt. Chỉ ghi "cỡ nắm tay" thì chú chim ra cao gần một phần ba Lumo (take thử `sh010` Cảnh 1 tập 000A).
5. **CAMERA:** bám `@Video1` 1:1, khớp từng khung; một cú liền hay cắt ở giây nào.
6. **RULES:** luật đánh số. Đếm được thì ghi số (bao nhiêu nhân vật, đạo cụ nào ở đâu); không chữ, không logo; không có gì đáng sợ, bạo lực.
7. **TIMELINE:** chia khối 2–5 giây theo cú máy hoặc hành động (cảnh cắt nhanh thì mỗi shot một khối). Mỗi khối:
   - `0–3.5s —` cú máy theo `@Video1` (cỡ cảnh, hướng chuyển động, ví dụ "low frontal, retreating");
   - hành động, mốc nhấn ghi tới 0.1 giây ("at 9.7s Lumo turns the head toward camera");
   - biểu cảm (mắt, miệng, tai, đuôi);
   - `END 3.5s:` trạng thái cuối khối (ai ở đâu, đang làm gì).
8. **AUDIO:** tiếng động do Seedance sinh (`generate_audio` bật, mặc định của `seedance_gen.py`): tả tiếng động của đoạn và các mốc nhấn theo giây (Timed accents), trùng mốc hành động. Không nhạc, không bài hát (tránh nhạc có bản quyền lọt vào take; nhạc phim làm ở hậu kỳ) và không lời nói (lồng tiếng nhiều thứ tiếng ở hậu kỳ). Tiếng động và tiếng kêu không lời của nhân vật (thở hắt, "ồ", "hừm", cười khúc khích, tiếng hét vui khi trượt) được giữ.
9. **HOLD:** nhắc lại các khoá quan trọng nhất ở cuối.

Quy tắc viết:
- Mốc trong prompt phải trùng hằng số trong `build_shot.py`. Đối chiếu bằng ảnh tĩnh đúng khung của từng mốc: khung = giây × 24 + 1 (`run.ps1 stills 217,469 -Shot <shot>` cho 9.0 s và 19.5 s).
- Mỗi nhân vật luôn gọi đúng một tên, không thay bằng "the fox", "the hero".
- Mỗi mốc chỉ một hành động chính. Không nhồi nhiều việc hơn số giây cho phép.
- Chữ và video mâu thuẫn về chuyển động thì video thắng (ghi rõ trong prompt).
- **Lời thoại:** ghi khoảng giây nhân vật nói theo kịch bản ("3.0–4.5s Lumo talks, mouth moving, no spoken words"), lời lồng ở hậu kỳ. Câu nói không được tạo thêm cảnh: máy vẫn theo previz.
- **Thời lượng mỗi lần sinh, chỗ nối với đoạn trước và sau:** mục "Chia cảnh thành đoạn" (luật 2, 5).
- **Độ dài prompt:** không đặt trần, viết đủ những gì take cần (vị trí từng vật, cỡ cảnh, nhịp từng mốc). API không chặn prompt dài; BytePlus chỉ khuyên tối đa 1.000 từ tiếng Anh vì quá dài thì model có thể bỏ chi tiết (tra ngày 07/11/2026). Lỗi của take thử `sh010` Cảnh 1 tập 000A không do độ dài: cùng một prompt 997 từ, bản 2.5 làm đúng chỗ ba bản 2.0 làm sai. Cắt chữ cho vừa 1.000 từ lại làm mất những câu chặn lỗi.
- Ảnh đạo cụ vẽ thêm đồ (ảnh Pocket of Wonders có túi mở, tràn đồ): ghi trong ACTIVE REFERENCES chỉ lấy gì, không lấy gì.
- Những chỗ Seedance hay làm sai (rút từ các take thử; thêm vào đây sau mỗi lần review take có lỗi), nên ghi sẵn trong prompt:
  - Nhân vật chỉ lấp ló ở mép khung trong previz dễ bị bỏ, có khi biến mất giữa cú máy: ghi rõ ai ở mép nào, thêm luật "stay visible at that edge, partly cut".
  - Chữ gọi cỡ cảnh ("medium two-shot") làm Seedance kéo chặt khung: ghi thêm "exactly as framed in @Video1, never tighter, never wider".
  - Bố cục của ảnh bối cảnh có thể đè lên previz (cành khô dời chỗ, che mặt nhân vật; cả cú toàn chép y bố cục ảnh): ghi trong ACTIVE REFERENCES bố cục của ảnh không phải một cú trong clip, ghi vật nào đứng đúng chỗ `@Video1` đặt, không vật gì đi ngang trước mặt nhân vật.
  - Hành động chạy trước mốc, khoảng đứng yên giữa hai hành động bị bỏ: ghi rõ "holds still" cho khoảng đứng yên và "at 8.6s, not before" cho mốc nhấn; tách khối TIMELINE ở chỗ đứng yên.
  - Khối nhỏ bị chép nguyên hình (tay cầu của Piko thành bong bóng nước), vật nhỏ bị đổi loại (bông hoa thành mầm cây): ghi khối đó là gì, trông ra sao.
  - Đồ đeo xoay theo hướng mặt (túi Piko thành dây chuyền khi Piko nhìn thẳng): tả cách đeo bằng con số và chữ "never" (một dây chéo, không hai dây).
  - Hướng chỉ của một vật đối xứng (mũi sao tám cánh) không đọc ra: cho một dấu hiệu nhìn thấy, ví dụ tia sáng từ mũi tới vật được chỉ.
  - Vật cầm tay có thể đè lên mặt nhân vật: ghi vật ở đâu so với mặt.
  - Thêm "no spoken words" vào từng khoảng nói; không viết lời trong ngoặc kép (ví dụ "aha") ở chỗ nhân vật mở miệng.
  - **Seedance 2.5 vẫn sinh nhạc** dù AUDIO, HOLD, TIMELINE đều dặn "no music" (bản nháp `sh010`, `sh020` Cảnh 1 tập 000A: giai điệu ở cú toàn mở đầu, cú toàn cuối). Vẫn dặn trong prompt, nhưng coi việc thay tiếng ở các cú toàn mở và kết là việc hậu kỳ thường lệ (reviewer `audio` chỉ chỗ có nhạc); không sinh lại vì nhạc.
  - **Miệng không mấp máy trong khoảng nói** khi prompt chỉ ghi "talks, mouth moving, no voice" (cả hai bản nháp Cảnh 1 tập 000A: miệng khép, cười mỉm suốt câu): ghi "mouth clearly opening and closing on every syllable, about 4 times per second, for the whole <khoảng nói>", và tả nét mặt hợp câu nói thay vì cảm xúc của khoảng trước.
  - **Phản ứng tới trước nguyên nhân** (mặt hoảng, tay hất lên trước khi chân vấp): ghi rõ khoảng trước mốc là chưa phản ứng ("no surprise yet, not before 8.42s") rồi mới tả phản ứng ở mốc.
  - **Vật phẳng xoay trong cú nhìn** (xoay bản đồ) thành lật mặt, lộ mặt sau, tay buông: ghi "both paws never let go, spin it flat in its own plane like a steering wheel, it never flips over, its back is never seen".
  - **Hai cú cùng chỗ khác cỡ cảnh** mà prompt tả bằng chữ gần giống nhau thì take cho cùng cỡ (cú S7 chặt như S3): tả từng cú bằng số đo (nhân vật cao bao nhiêu phần khung, nằm bên nào, thấy những vật gì) và ghi cú nào rộng hơn cú nào.
  - **Hiệu ứng sáng ở một mốc nhấn thì ghép ở hậu kỳ:** viết luật phủ định ("no golden light before 23.7s") làm ánh sáng trễ gần 2 giây; viết mốc khẳng định và làm khối sáng hơn vẫn trễ khoảng 1.5 giây, nhân vật phản ứng trước. Prompt chỉ giữ chỗ (vật phát sáng nằm đó, mép sáng mỏng) và cho nhân vật nhìn vật khác tới đúng mốc.
  - **Câu cho phép gọi ra thứ không muốn:** "only the cheeks may blush", "cheeks blush only in this moment" làm má đỏ suốt cú. Đừng nhắc tới nét không muốn kể cả để cho phép; tả nét muốn có ("cream cheeks as in @Image1") và tả cảm xúc bằng động tác (cụp tai, rụt vai).
  - **Nhân vật trôi thiết kế giữa các đoạn** (chỏm lông kem thành nơ hồng, lông nhạt màu): câu chữ ("one tall cream swoosh of fur, never a bow or knot") không giữ được qua hai lần sinh; chi tiết nhỏ dễ trôi thì thêm một ảnh tham chiếu cận đúng chi tiết đó (cận đầu Lumo thấy rõ chỏm lông).
  - **Vật phẳng có hình vẽ xoay nhanh trộn hai ảnh tham chiếu** (bản đồ trước và sau khi xoay thành một tấm có hai rương, hai mũi tên): cú xoay ngắn mà cần đọc ra chiều thì ghép mặt vật ở hậu kỳ, hoặc sinh riêng cú đó với khung đầu, khung cuối; đừng đưa hai ảnh hai chiều của cùng vật vào một lần sinh.
  - **Hướng quay đầu viết theo màn hình và theo vật**, không theo trái phải của nhân vật: "muzzle points to screen left, at the sunny path; pupils in the left corners of the eyes; the bush is behind the head". "Over the LEFT shoulder" bị hiểu thành quay mặt ra máy, liếc sang bụi. Previz quay đầu quá tay một chút (Seedance kéo mặt về phía máy).
  - **Cỡ tương đối so với bộ phận thấy được trong cùng khung:** "the size of Lumo's finger" vẫn ra bướm to bằng hai phần ba đầu; viết "wingspan no wider than Lumo's eye".

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
No music, no songs, no spoken words; non-verbal character sounds are fine. Sound effects: ... Timed accents: <t>s ..., <t>s ...

HOLD
@Video1 camera 1:1 for all <N> seconds. Exactly <K> characters. @Image1 identity constant. No text, no logos, no watermarks.
```

## Soát take

| Kiểm tra | Sai thì |
|---|---|
| Cú máy, cỡ cảnh, chỗ cắt khớp previz từng giây | Nhấn mạnh CAMERA, HOLD; nếu vẫn lệch thì làm previz rõ hơn (khối to hơn, ít vật thừa) |
| Đúng số nhân vật, không người thừa | Thêm số vào RULES, HOLD |
| Nhân vật giống ảnh tham chiếu, đúng tỉ lệ | Sửa tỉ lệ khối trong previz; thêm ý vào CHARACTERS |
| Cỡ đạo cụ, nhân vật nền, vật bối cảnh so với Lumo đúng `02_ASSET_LIBRARY/MODELING.md`, mục "Bảng cỡ" (đo bằng đầu, mắt Lumo trong cùng khung) | Sửa cỡ khối trong previz trước (take thường còn to hơn previz); trong CHARACTERS, SIZES so với bộ phận thấy trong cùng khung ("wingspan as wide as Lumo's nose"); ảnh tham chiếu ghi "size not inherited" |
| Màu khối không lọt vào hình | Nhấn "do not take color from @Video1" |
| Hành động, biểu cảm, khoảng nói đúng mốc giây | Tách khối TIMELINE nhỏ hơn, mỗi mốc một việc |
| Không chữ, logo, cảnh đáng sợ | Thêm vào RULES |
| Tiếng động đúng mốc nhấn; không nhạc, không bài hát, không lời nói (tiếng kêu không lời được giữ) | Sửa Timed accents trong AUDIO cho trùng mốc hành động; nhấn "no music, no songs, no spoken words" ở AUDIO và HOLD. Lỗi nhỏ để hậu kỳ bù |

Ghi kết quả từng take (đạt, lỗi gì) vào cuối `seedance/prompt.md`.


## Nguồn

Tra ngày 06/11/2026 (tài liệu chính thức của BytePlus): [ModelArk: Create a video generation task](https://docs.byteplus.com/en/docs/modelark/create-video-generation-task-api) · [ModelArk: Retrieve a video generation task](https://docs.byteplus.com/en/docs/modelark/get-video-generation-task-api) · [ModelArk: Pricing](https://docs.byteplus.com/en/docs/modelark/model-pricing) · [Cloudflare R2: Presigned URLs](https://developers.cloudflare.com/r2/api/s3/presigned-urls/) · [Cloudflare R2: Object lifecycles](https://developers.cloudflare.com/r2/buckets/object-lifecycles/) · [Fuser: Seedance 2.5 prompt guide](https://fuser.studio/articles/seedance-2-5-prompt-guide)

Tra ngày 03/11/2026:

[Higgsfield: Blender + Higgsfield workflow (5 ví dụ prompt đầy đủ)](https://higgsfield.ai/@adilinthewild/blogs/this-blender-higgsfield-ai-workflow-changes-how-you-make-ai-video) · [Venice: Seedance 2.0 reference-to-video](https://docs.venice.ai/it/guides/media/seedance-2-0) · [MindStudio: timeline prompting](https://www.mindstudio.ai/blog/timeline-prompting-seedance-2-cinematic-ai-video)
