# Lab — thử nghiệm làm film ngắn bằng Blender

Đây là nơi thử nghiệm: mọi cảnh đều được **dựng bằng script Python**, nên có thể sửa → build lại → render lại mà không sợ hỏng file `.blend`.

- Blender: 5.2.3 LTS (`C:\Program Files\Blender Foundation\Blender 5.2`)
- Engine: **EEVEE**. Máy chỉ có Ryzen 5 3400G với card tích hợp Vega 11, nên Cycles sẽ quá chậm cho 720 frame.

## Các thử nghiệm

| Thư mục | Nội dung |
|---|---|
| `shot01_dawn/` | Shot 01 "Bình minh": cảnh thiên nhiên 30s, kiểm tra quy trình dựng và render bằng code |
| `shot02_max_power/` | Shot 02 "MAX POWER": demo 30s của tập 01, Piko dựng bằng code, có asset Quaternius và âm thanh |
| `char_lumo/` | Rig Lumo hoàn toàn bằng code: Rigify, sửa da, vòng đi bộ, face rig và 9 biểu cảm (xem `char_lumo/README.md`) |

Code dùng chung (`lablib.py`, `render.py`, `run.ps1`, thư viện âm thanh) nằm ở `pipeline/`, xem `pipeline/README.md`. Chạy từ thư mục gốc dự án:

```powershell
.\pipeline\run.ps1 build                           # dựng lại shot02 sau khi sửa build_shot.py
.\pipeline\run.ps1 stills 300,540                  # chỉ các khung muốn xem
.\pipeline\run.ps1 preview -Shot lab\shot01_dawn   # làm việc với shot 01
```

## Shot 02 — "MAX POWER" (`shot02_max_power/`)

Demo đầu tiên của *The Wonderlings* (xem `docs/BRIEF.md`), trích Act 2→3 của tập 01. Dài 30s, không thoại. Piko vô tình đè nút MAX POWER của máy Rain-O-Matic 3000, mây kéo về, mưa trút, rồi một giọt to "BOP" làm Piko xẹp lép. Nhịp 7 shot nằm trong [`SHOTLIST.md`](shot02_max_power/SHOTLIST.md).

**Núm vặn chính** ở đầu `build_shot.py`: `SHOTS` (frame từng shot), `PRESS` (lúc đè nút), `STORM0/1` (trời chuyển bão), `RAIN_*`, `FLASHES` (sét), `BOP`. Diễn xuất của Piko nằm trong `animate_piko()`: mỗi dòng `(frame, giá trị)` là một keyframe.

**Asset Quaternius (CC0) trong shot** (lấy từ `02_ASSET_LIBRARY/Third_Party/quaternius/`, xem `02_ASSET_LIBRARY/Third_Party/README.md`):
- `build_vegetation()`: cây khô, cây xanh và thông (Nature MegaKit), cỏ khô, đá, sỏi, nấm quanh nhà, cùng đạo cụ (xô gỗ, thùng, sọt cà rốt, ghế). Tất cả là **collection instance**, dùng chung một mesh nên rất nhẹ.
- `build_critters()`: 4 sinh vật (Cactus, Chicken, Mushroom, Pig từ Cute Monsters). Diễn xuất xếp bằng NLA: đứng `Idle` → máy gầm thì `No` → mưa xuống thì `Dance`.
- Các hàm import nằm trong `pipeline/lablib.py`: `import_file`, `asset_collection`, `instance`, `nla_sequence`.

**Âm thanh:** tổng hợp hoàn toàn bằng code. `pipeline/sound/sfx.py` là thư viện tiếng hoạt hình viết bằng numpy (boing, bloop, beep, còi, sấm, mưa, gió, kèn buồn…). `build_audio.py` đặt từng tiếng đúng frame theo `timing.py` rồi xuất `audio/shot02_mix.wav` cùng 4 stem (amb, machine, piko, fx). Chạy `.\pipeline\run.ps1 audio` để tạo lại tiếng và ghép vào video preview trong khoảng 20 giây, không phải render lại hình. File `.blend` đã gắn sẵn track âm thanh, mở Blender bấm Space là nghe.

**Cách dựng Piko bằng code:** thân là một quả cầu nắn thành hình giọt nước. Mắt, miệng, má, sừng và ngôi sao được "dán" lên bề mặt bằng ray-cast. Phần co giãn (squash & stretch) dùng scale. Cú đè nút dùng shape key `Bulge`. Không cần rig xương.

## Shot 01 — "Bình minh" (`shot01_dawn/`)

Một cú máy liền 30s (720 frame @ 24fps), phong cách low-poly:

| Thời điểm | Frame | Nội dung |
|---|---|---|
| 0–8s | 1–200 | Đêm. Camera trôi chậm qua rừng thông, đom đóm nhấp nháy, trời đầy sao |
| 8–20s | 200–480 | Trời hửng tím → hồng, sao tắt dần, đom đóm tàn, hồ hiện ra giữa rừng |
| 20–30s | 480–720 | Mặt trời ló qua khe núi, sương sớm phủ mặt hồ, camera nâng lên toàn cảnh |

`build_shot.py` dựng toàn bộ cảnh (địa hình, hồ, rừng, đom đóm, bầu trời, sương, đèn, camera) rồi lưu `shot01.blend`. Chạy bằng các lệnh ở trên, thêm `-Shot lab\shot01_dawn`.

### Các "núm vặn" chính trong `build_shot.py`

- **CONFIG** ở đầu file: số cây, số đom đóm, vị trí và bán kính hồ, seed ngẫu nhiên.
- `NIGHT, PREDAWN, SUNRISE, END`: các mốc thời gian trong ngày.
- `CAM_KEYS` / `AIM_KEYS`: đường đi của camera và điểm nhìn. Độ cao camera tính *trên mặt đất*.
- `height(x, y)`: hàm địa hình (đồi, hồ, núi, khe núi cho mặt trời mọc).
- `build_world()`: màu trời theo từng mốc (Zenith / Horizon / Glow) và sao.
- `build_mist()`: mật độ sương sát mặt đất và haze.

### Bài học kỹ thuật (Blender 5.2)

- **Không dùng World Volume** trong EEVEE: nó được tính là vô hạn và chặn toàn bộ bầu trời. Dùng một khối hộp có material volume thay thế.
- `ShaderNodeMix` ở chế độ màu có nhiều socket trùng tên (`A`, `B`, `Result` bản float, vector và color). Phải chọn đúng socket kiểu `RGBA` (xem hàm `rgba()`).
- Vật thể chỉ có Emission mà emission ≈ 0 sẽ render thành khối đen. Cộng thêm Transparent BSDF để nó "biến mất" khi tắt.
- Action trong 5.x là layered: lấy fcurves qua `anim_utils.action_get_channelbag_for_slot` (xem hàm `fcurves_of()`).
- Xuất video: `image_settings.media_type = "VIDEO"` rồi mới đặt `file_format = "FFMPEG"`.

## Blender MCP

Đã chuyển sang `pipeline/README.md`.

## Ý tưởng tiếp theo (cho shot 01)

- Âm thanh: tiếng côn trùng đêm → chim hót lúc mặt trời lên (dựng trong VSE).
- Gió lay ngọn cây (modifier Simple Deform + driver theo frame).
- Một nhân vật/điểm nhấn: con nai bên hồ, chiếc thuyền, căn chòi.
- Chim bay ngang khung khi mặt trời ló lên.
