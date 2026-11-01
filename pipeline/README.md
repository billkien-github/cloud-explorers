# Pipeline: code dùng chung

| File | Vai trò |
|---|---|
| `lablib.py` | Hàm dùng chung cho build script: keyframe, driver, material, camera + marker cắt cảnh, import asset (`import_file`, `asset_collection`, `instance`, `nla_sequence`), thiết lập render (EEVEE, AgX, bloom) |
| `render.py` | Render mọi shot theo chế độ `stills` / `preview` / `final`, ghi vào `renders/` cạnh file `.blend` |
| `mux_audio.py` | Ghép file âm thanh vào video đã render, không render lại hình (giữ nguyên màu) |
| `run.ps1` | Lệnh chạy nhanh cho một shot |
| `sound/sfx.py` | Thư viện tiếng hoạt hình viết bằng numpy: dao động, lọc, bao âm, hiệu ứng (boing, bloop, sấm, mưa, gió…), bộ trộn `Track`, xuất WAV |
| `rigging/face_rig.py` | Face rig: mắt, mí, đồng tử, lông mày, 7 hình miệng, má hồng, mồ hôi, điều khiển bằng 21 thanh trượt trên rig |
| `rigging/skin.py` | Sửa da sau khi gắn tự động: giữ thể tích, làm mượt trọng số, khối đầu đi cứng theo xương đầu, Corrective Smooth |
| `rigging/rig_qa.py` | Kiểm tra rig: đặt tư thế theo trục thế giới, đo % mặt lưới bị bóp hay giãn và thể tích |
| `tools/make_previews.py` | Render bảng xem trước cho một thư mục model (`.gltf`, `.glb`, `.fbx`) |

## Dùng trong build script

Đường dẫn tính lùi từ vị trí script lên thư mục gốc `studio/`. Ví dụ script ở `04_PRODUCTION/EP001_.../sh010/build_shot.py`:

```python
HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(STUDIO, "pipeline"))
sys.path.insert(0, os.path.join(STUDIO, "pipeline", "rigging"))
from lablib import ...
```

## Module rigging

Ba module trong `rigging/` được viết và kiểm tra trên một bản Lumo rig bằng Rigify. Khi dùng với rig Meshy (khung Mixamo) cần lưu ý:
- `face_rig.py`: vị trí mắt, lông mày, miệng đang đặt theo tọa độ khuôn mặt của bản Lumo đó, và gắn vào xương `DEF-spine.006`. Với nhân vật mới phải đo lại vị trí theo mặt từng nhân vật, và đổi xương đầu thành `mixamorig:Head`.
- `skin.py`: truyền `head_bone="mixamorig:Head"` và `head_zones` đo theo đầu từng nhân vật.
- `rig_qa.py`: tư thế viết theo tên xương của rig đang kiểm tra.

## `run.ps1`

Chạy từ thư mục gốc dự án. `-Shot` là đường dẫn thư mục shot tính từ gốc. Tên file `.blend` lấy theo phần đầu tên thư mục, ví dụ `sh010` thành `sh010.blend`.

```powershell
$S = "04_PRODUCTION\EP001_Great_Rain_Experiment\sh010"
.\pipeline\run.ps1 build -Shot $S              # dựng lại sh010.blend từ build_shot.py
.\pipeline\run.ps1 stills -Shot $S             # các khung mẫu định sẵn của shot
.\pipeline\run.ps1 stills 300,540 -Shot $S     # chỉ các khung muốn xem
.\pipeline\run.ps1 preview -Shot $S            # cả shot 960x540 -> renders\sh010_preview.mp4
.\pipeline\run.ps1 final -Shot $S              # 1920x1080 + motion blur (vài giờ)
.\pipeline\run.ps1 audio -Shot $S              # tạo lại âm thanh (build_audio.py) rồi ghép vào video preview
.\pipeline\run.ps1 open -Shot $S               # mở trong Blender GUI (Space để play)
.\pipeline\run.ps1 mcp -Shot $S                # mở kèm --online-mode để add-on MCP tự bật
```

## Blender MCP (bản chính thức của Blender Lab)

Cho phép Claude điều khiển trực tiếp Blender đang mở: đọc scene, chạy Python, chụp viewport.

| Thành phần | Vị trí |
|---|---|
| Add-on `MCP` v1.0.3 | Đã cài và bật trong Blender 5.2 (repo `user_default`) |
| MCP server | `C:\Users\APC\blender_mcp_src\.venv\Scripts\blender-mcp.exe` (venv riêng, mã nguồn v1.0.3 cạnh đó) |
| Đăng ký với Claude Code | Scope `local` cho thư mục `studio` (`claude mcp get blender`) |

Cách dùng:
1. Mở Blender với `.\pipeline\run.ps1 mcp -Shot <shot>`. Add-on chỉ tự bật khi Blender được phép truy cập mạng. Lệnh này dùng cờ `--online-mode` cho riêng lần chạy đó. Nếu muốn mở Blender bình thường, bật **Edit → Preferences → System → Network → Allow Online Access**.
2. Mở một phiên Claude **mới** trong thư mục `studio`. Phiên mới sẽ có các tool `execute_blender_code`, `get_objects_summary`, `get_screenshot_of_window_as_image`…
3. Add-on chỉ lắng nghe ở `127.0.0.1:9876` (trong máy, không mở ra ngoài).

⚠️ MCP chạy code do AI viết **không có lớp bảo vệ**. Hãy lưu file trước khi thử, và chép những thay đổi ưng ý vào build script để giữ lâu dài.

## Lưu ý kỹ thuật (Blender 5.2)

- **Không dùng World Volume** trong EEVEE: nó được tính là vô hạn và chặn toàn bộ bầu trời. Dùng một khối hộp có material volume thay thế.
- `ShaderNodeMix` ở chế độ màu có nhiều socket trùng tên. Phải chọn đúng socket kiểu `RGBA` (hàm `rgba()` trong `lablib.py`).
- Vật thể chỉ có Emission mà emission ≈ 0 sẽ render thành khối đen. Cộng thêm Transparent BSDF.
- Action trong 5.x là layered: lấy fcurves qua `anim_utils.action_get_channelbag_for_slot` (hàm `fcurves_of()`).
- Xuất video: đặt `image_settings.media_type = "VIDEO"` trước rồi mới đặt `file_format = "FFMPEG"`.
- Ghép tiếng vào video đã render phải dùng view transform `Standard`, nếu không AgX áp thêm lần nữa làm bạc màu (`mux_audio.py` đã xử lý).
- Avast quét HTTPS làm hỏng `pip install` và tải gói (lỗi `InvalidChunkLength`). Khi cần cài thư viện, tạm tắt Avast shields 10 phút.
