# Pipeline: code dùng chung

| File | Vai trò |
|---|---|
| `run.ps1`, `run.sh` | Lệnh chạy nhanh cho một shot: build, render, mở Blender. `run.ps1` cho Windows, `run.sh` cho macOS |
| `render.py` | Render một `.blend` theo 4 chế độ `stills` / `preview` / `final` / `ref`, ghi vào `renders/` cạnh file |
| `cutout.py` | Bộ nhân vật cutout 2D cho previz 2D: hình phẳng, bộ mặt, bốn nhân vật, hàm keyframe, máy quay theo `SHOTS`, render Workbench. Cách dùng ở docstring, quy ước dựng ở `03_CONTENT/PREVIZ_2D.md` |
| `blocks.py` | Bộ khối 3D cho previz khối dẫn Seedance: hình khối, vật liệu, bốn nhân vật dạng khối đúng tỉ lệ, keyframe theo giây của cảnh (đoạn cắt ra từ cảnh dài vẫn trùng khung), máy quay theo `SHOTS`, tự kiểm nhân vật trong khung, cài đặt render. Quy ước previz khối: `04_PRODUCTION/SEEDANCE.md` |
| `edit.py` | Ghép nhiều video thành một theo danh sách dựng: cắt đầu đuôi, nối, co giãn video khác cỡ, thêm tiếng, in CC từ `timing.py` và xuất `.srt` (`--clean`: chỉ `.srt`, không in lên hình). Take trong thư mục shot tự cắt theo `SEGMENT`, lấy CC theo `TIMING`, `OFFSET` của `build_shot.py`; take chưa có thì thay bằng khung tối đúng độ dài. Cách dùng ở docstring |
| `cc.py` | In CC từ `timing.py` của cảnh lên một video previz (2D hay khối) và xuất `.srt`, không render lại hình. Là `edit.py` với một video. Cách viết CC: `03_CONTENT/PREVIZ_2D.md` |
| `turnaround.py` | Ghép nhiều ảnh thành một tấm tham chiếu Seedance (mỗi tấm một suất `@Image`): ảnh xoay `<tên>_turnaround.png` của một nhân vật (ảnh trước trái, ảnh sau phải, cùng chiều cao, chân cùng một đường), hoặc với `--hop` là tấm gộp nhiều món để đoạn không quá 9 ảnh (`04_PRODUCTION/SEEDANCE.md`, mục "Gộp ảnh tham chiếu"). Cân nền về cùng màu xám, mép ghép mờ dần, tự xếp hàng cho tỉ lệ trong giới hạn của API. Cách chạy ở docstring |
| `seedance_gen.py` | Sinh clip Seedance của một shot qua API BytePlus ModelArk: đọc `seedance/prompt.md`, chọn model theo số ảnh tham chiếu (dòng 2.0 bắt đầu ở bản mini, hoặc 2.5), kiểm giới hạn của model, ước tính chi phí (`--dry-run`), tải video previz lên bucket Cloudflare R2 (chuẩn S3), gửi, chờ, tải take về `seedance/`, ghi chi phí vào `04_PRODUCTION/seedance_log.csv`. Chỉ dùng thư viện chuẩn, không cần Blender. Cách dùng: `04_PRODUCTION/SEEDANCE.md`, mục "Sinh qua API"; tuỳ chọn ở docstring |
| `seedance_upload.py` | Đọc bảng số tham chiếu và khối prompt trong `seedance/prompt.md` (hàm `load()`, `seedance_gen.py` dùng chung). Chạy riêng thì tạo thư mục tải lên `renders/seedance_upload/` để sinh tay trên console: chép video previz, từng ảnh với tên theo số, và `prompt.txt`. Chạy bằng Python thường, không cần Blender. Cách chạy ở docstring |

Code riêng của từng asset hay shot (build script) nằm cạnh asset hay shot đó, không để ở đây. Chỉ chuyển một hàm vào `pipeline/` khi đã có từ hai nơi trở lên cần dùng.

## `run.ps1`, `run.sh`

Chạy từ thư mục gốc dự án. `-Shot` là thư mục shot tính từ gốc. Shot cần có `build_shot.py`. Tên file `.blend` lấy theo phần đầu tên thư mục (`sh010` → `sh010.blend`).

```powershell
$S = "04_PRODUCTION\EP001_Great_Rain_Experiment\sh010"
.\pipeline\run.ps1 build -Shot $S              # dựng lại sh010.blend từ build_shot.py
.\pipeline\run.ps1 stills -Shot $S             # 6 khung rải đều (hoặc scene["stills"] = "1,120,240")
.\pipeline\run.ps1 stills 300,540 -Shot $S     # chỉ các khung muốn xem
.\pipeline\run.ps1 preview -Shot $S            # cả shot 960x540 -> renders\sh010_preview.mp4
.\pipeline\run.ps1 final -Shot $S              # 1920x1080 + motion blur
.\pipeline\run.ps1 ref -Shot $S                # 1920x1080, 8 sample, không motion blur: video dẫn cho Seedance
.\pipeline\run.ps1 open -Shot $S               # mở trong Blender GUI
.\pipeline\run.ps1 mcp -Shot $S                # mở kèm --online-mode cho Blender MCP
```

macOS dùng `pipeline/run.sh`, cùng chế độ và đối số; đường dẫn shot viết bằng `/`. Blender mặc định ở `/Applications/Blender.app`, để nơi khác thì đặt biến môi trường `BLENDER`.

```bash
S=04_PRODUCTION/EP001_Great_Rain_Experiment/sh010
pipeline/run.sh build -Shot $S
pipeline/run.sh stills 300,540 -Shot $S
```

**Giữ hai file đồng bộ:** `run.ps1` và `run.sh` phải có cùng chế độ, đối số, giá trị mặc định và tên file ra. Sửa hay thêm gì ở file này thì sửa luôn file kia trong cùng lần làm. Máy chỉ chạy được một bản (Mac chưa có PowerShell) thì chạy thử bản đó, soát bản kia bằng mắt và báo người dùng là bản đó chưa chạy thử.

## Blender MCP

Cho phép Claude điều khiển trực tiếp Blender đang mở: đọc scene, chạy Python, chụp viewport. Mới cài trên máy Windows; trên macOS chưa cài add-on và server.

| Thành phần | Vị trí (máy Windows) |
|---|---|
| Add-on `MCP` v1.0.3 | Đã cài và bật trong Blender 5.2 (repo `user_default`) |
| MCP server | `C:\Users\APC\blender_mcp_src\.venv\Scripts\blender-mcp.exe` |
| Đăng ký với Claude Code | Scope `local` cho thư mục `studio` (`claude mcp get blender`) |

1. Mở Blender bằng `run.ps1 mcp` hoặc `run.sh mcp` (dùng cờ `--online-mode` cho riêng lần chạy đó), hoặc bật **Edit → Preferences → System → Network → Allow Online Access**. Add-on chỉ tự bật khi Blender được phép truy cập mạng.
2. Mở một phiên Claude mới trong thư mục `studio` để có các tool `execute_blender_code`, `get_objects_summary`, `get_screenshot_of_window_as_image`…
3. Add-on chỉ lắng nghe ở `127.0.0.1:9876` (trong máy).

⚠️ MCP chạy code do AI viết không có lớp bảo vệ. Lưu file trước khi thử, và chép thay đổi ưng ý vào build script.

## Lưu ý kỹ thuật (Blender 5.2)

- **Engine:** EEVEE. Máy chỉ có card tích hợp Vega 11, Cycles quá chậm.
- **Không dùng World Volume** trong EEVEE: nó được tính là vô hạn và chặn toàn bộ bầu trời. Dùng một khối hộp có material volume.
- `ShaderNodeMix` ở chế độ màu có nhiều socket trùng tên (`A`, `B`, `Result` cho float, vector, color). Phải chọn socket theo kiểu `RGBA`, không theo tên.
- Vật thể chỉ có Emission mà cường độ ≈ 0 sẽ render thành khối đen. Cộng thêm Transparent BSDF để nó biến mất khi tắt.
- Action trong 5.x là layered: lấy fcurves qua `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot)`, không còn `action.fcurves`.
- VSE trong 5.x: `scene.sequence_editor.strips.new_sound / new_movie` (`new_movie` nhận `fit_method="FIT"` để co video khác cỡ vừa khung). `frame_final_*`, `frame_offset_*` sắp bỏ: cắt bằng `left_handle_offset`, `right_handle_offset`, dời bằng `content_start`. Video khác fps với scene bị phát từng khung (nhanh hay chậm đi), Blender không tự đổi. `new_sound` trên video không có tiếng không báo lỗi mà trả về strip dài 1 khung.
- Xuất video: đặt `image_settings.media_type = "VIDEO"` trước rồi mới đặt `file_format = "FFMPEG"`.
- Ghép tiếng vào video đã render phải dùng view transform `Standard`, nếu không AgX áp thêm lần nữa làm bạc màu (`edit.py` đã xử lý). Blender cần đường dẫn tuyệt đối khi nạp video.
- Avast quét HTTPS làm hỏng `pip install` và tải gói (lỗi `InvalidChunkLength`). Khi cần cài thư viện, tạm tắt Avast shields 10 phút.
