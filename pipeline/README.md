# Pipeline: code dùng chung

| File | Vai trò |
|---|---|
| `run.ps1` | Lệnh chạy nhanh cho một shot: build, render, ghép tiếng, mở Blender |
| `render.py` | Render một `.blend` theo 4 chế độ `stills` / `preview` / `final` / `ref`, ghi vào `renders/` cạnh file |
| `mux_audio.py` | Ghép file âm thanh vào video đã render, không render lại hình, giữ nguyên màu |
| `cc.py` | In CC từ `timing.py` của cảnh lên video previz (2D hay khối) và xuất `.srt`, không render lại hình. Cách viết CC: `03_CONTENT/PREVIZ_2D.md` |
| `rig_qa.py` | Kiểm tra rig: đặt tư thế theo trục thế giới, đo % mặt lưới bị bóp (< 40% diện tích) hay giãn (> 250%) và tỉ lệ thể tích so với tư thế nghỉ. Đạt khi bad% dưới khoảng 2%, thể tích gần 1.0 |

Code riêng của từng asset hay shot (build script) nằm cạnh asset hay shot đó, không để ở đây. Chỉ chuyển một hàm vào `pipeline/` khi đã có từ hai nơi trở lên cần dùng.

## `run.ps1`

Chạy từ thư mục gốc dự án. `-Shot` là thư mục shot tính từ gốc. Shot cần có `build_shot.py`. Tên file `.blend` lấy theo phần đầu tên thư mục (`sh010` → `sh010.blend`).

```powershell
$S = "04_PRODUCTION\EP001_Great_Rain_Experiment\sh010"
.\pipeline\run.ps1 build -Shot $S              # dựng lại sh010.blend từ build_shot.py
.\pipeline\run.ps1 stills -Shot $S             # 6 khung rải đều (hoặc scene["stills"] = "1,120,240")
.\pipeline\run.ps1 stills 300,540 -Shot $S     # chỉ các khung muốn xem
.\pipeline\run.ps1 preview -Shot $S            # cả shot 960x540 -> renders\sh010_preview.mp4
.\pipeline\run.ps1 final -Shot $S              # 1920x1080 + motion blur
.\pipeline\run.ps1 ref -Shot $S                # 1920x1080, 8 sample, không motion blur: video dẫn cho Seedance
.\pipeline\run.ps1 audio -Shot $S              # ghép audio\sh010_mix.wav vào video preview
.\pipeline\run.ps1 open -Shot $S               # mở trong Blender GUI
.\pipeline\run.ps1 mcp -Shot $S                # mở kèm --online-mode cho Blender MCP
```

## Blender MCP

Cho phép Claude điều khiển trực tiếp Blender đang mở: đọc scene, chạy Python, chụp viewport.

| Thành phần | Vị trí |
|---|---|
| Add-on `MCP` v1.0.3 | Đã cài và bật trong Blender 5.2 (repo `user_default`) |
| MCP server | `C:\Users\APC\blender_mcp_src\.venv\Scripts\blender-mcp.exe` |
| Đăng ký với Claude Code | Scope `local` cho thư mục `studio` (`claude mcp get blender`) |

1. Mở Blender bằng `run.ps1 mcp` (dùng cờ `--online-mode` cho riêng lần chạy đó), hoặc bật **Edit → Preferences → System → Network → Allow Online Access**. Add-on chỉ tự bật khi Blender được phép truy cập mạng.
2. Mở một phiên Claude mới trong thư mục `studio` để có các tool `execute_blender_code`, `get_objects_summary`, `get_screenshot_of_window_as_image`…
3. Add-on chỉ lắng nghe ở `127.0.0.1:9876` (trong máy).

⚠️ MCP chạy code do AI viết không có lớp bảo vệ. Lưu file trước khi thử, và chép thay đổi ưng ý vào build script.

## Lưu ý kỹ thuật (Blender 5.2)

- **Engine:** EEVEE. Máy chỉ có card tích hợp Vega 11, Cycles quá chậm.
- **Không dùng World Volume** trong EEVEE: nó được tính là vô hạn và chặn toàn bộ bầu trời. Dùng một khối hộp có material volume.
- `ShaderNodeMix` ở chế độ màu có nhiều socket trùng tên (`A`, `B`, `Result` cho float, vector, color). Phải chọn socket theo kiểu `RGBA`, không theo tên.
- Vật thể chỉ có Emission mà cường độ ≈ 0 sẽ render thành khối đen. Cộng thêm Transparent BSDF để nó biến mất khi tắt.
- Action trong 5.x là layered: lấy fcurves qua `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, slot)`, không còn `action.fcurves`.
- VSE trong 5.x: `scene.sequence_editor.strips.new_sound / new_movie`.
- Xuất video: đặt `image_settings.media_type = "VIDEO"` trước rồi mới đặt `file_format = "FFMPEG"`.
- Ghép tiếng vào video đã render phải dùng view transform `Standard`, nếu không AgX áp thêm lần nữa làm bạc màu (`mux_audio.py` đã xử lý). Blender cần đường dẫn tuyệt đối khi nạp video.
- Avast quét HTTPS làm hỏng `pip install` và tải gói (lỗi `InvalidChunkLength`). Khi cần cài thư viện, tạm tắt Avast shields 10 phút.
