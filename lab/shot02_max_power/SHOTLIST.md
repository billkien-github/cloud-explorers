# Shot 02 — "MAX POWER" (demo The Wonderlings)

Trích Act 2 → 3 của tập 01 *The Great Rain Experiment*. Dài 30s (720 frame @ 24fps), không thoại, kể bằng hành động.

**Bối cảnh rút gọn cho demo:** máy Rain-O-Matic 3000 được đặt ngay giữa khu vườn khô ở Thung lũng Mây (bản kịch bản gốc đặt máy trong Wonder Hub). Máy đang chạy ở **Level 1**: một đám mây tí hon nhỏ giọt tưới cho đúng một bông hoa.

| Shot | Frame | Cỡ cảnh | Nội dung |
|---|---|---|---|
| S1 | 1–96 | Toàn cảnh | Thung lũng khô nắng gắt, hoa héo rũ. Máy phì phò nhả hơi lên đám mây tí hon, mây nhỏ giọt tưới một bông hoa. Piko đứng cạnh máy, nhún nhảy tò mò |
| S2 | 97–216 | Trung cận Piko + bảng điều khiển | Nút đỏ **MAX POWER** nhấp nháy. Mắt Piko dán vào nút, cả người rướn tới… rồi lắc đầu "không được", ngả người lại |
| S3 | 217–300 | Trung cảnh | Piko quay lưng bỏ đi cho ngoan, nhảy tưng tưng vui vẻ. Cú nhảy thứ hai đáp đất bẹp mạnh, thân thạch phình ra phía sau |
| S4 | 301–340 | Đặc tả nút | Phần thân phình ra **đè trúng nút**. BEEP! Màn hình đổi từ "LEVEL 1" sang **"MAX POWER!"** đỏ nhấp nháy |
| S5 | 341–420 | Trung cảnh máy | Máy rung bần bật, lõi tinh thể sáng rực, hơi nước phụt thành cột. Piko quay lại, đứng hình, phồng to người vì sốc |
| S6 | 421–576 | Toàn cảnh góc thấp | Cột hơi bốc lên trời, mây khắp nơi kéo về, trời tối sầm. Mưa lắc rắc rồi trút xuống, sấm chớp, hoa ngẩng đầu dậy |
| S7 | 577–720 | Trung cận Piko trong mưa | Piko khoái chí há miệng hứng mưa… một **giọt mưa to "BOP"** trúng đỉnh đầu, Piko xẹp lép như cái gối. Hết |

## Âm thanh (tổng hợp bằng code: `build_audio.py`, thư viện `pipeline/sound/sfx.py`)

Không dùng file thu âm nào, nên không vướng bản quyền. Mốc thời gian lấy chung từ `timing.py`.

| Lúc | Frame | Tiếng |
|---|---|---|
| Nền S1–S3 | 1–306 | Gió nhẹ, **ve sầu** trong nắng, máy Level 1 kêu ù ù, mỗi làn hơi "phù", mây tí hon nhỏ giọt "tách" |
| S2 | 97–306 | Nút đỏ "bíp" khẽ theo nhịp nhấp nháy. Piko rướn người (tiếng cao su căng), lắc đầu "wub-wub" |
| Piko nhảy | các cú nhảy | "Boing" lúc bật lên, "bloop" lúc đáp. Cú đáp đè nút là tiếng "bẹp" to |
| **Đè nút** | 305–310 | "Tách" (nút lún) → **BEEP-BEEP** → tiếng máy rít lên + còi hú. **Ve sầu im bặt** |
| S5–S7 | 312–720 | Máy gầm rung bần bật, hơi nước xì liên tục. Piko phồng người "phùuu". 4 sinh vật kêu "chíp" lúc lắc đầu |
| Bão | 380–720 | Gió mạnh dần, mưa lắc rắc rồi ào ào, **sấm** ở frame 528 và 566 (khớp tia chớp) |
| Hoa ngẩng đầu | 548–625 | Tiếng chuông lấp lánh |
| S7 | 614–720 | Mưa lộp độp vào miệng Piko → **"BOP"** → "bẹp" → xì hơi "pffft" → kèn buồn "wah wah wah waaah" |

**Nguyên tắc hình ảnh** (theo BRIEF): soft stylized, pastel, hình khối tròn. Máy dùng bảng màu của Tavi (mint, cam). Cảnh nước ngập/bão giữ ở mức vui nhộn, không đáng sợ.
