# Pipeline: code dùng chung

| File | Vai trò |
|---|---|
| `lablib.py` | Hàm dùng chung cho build script: keyframe, driver, material, camera + marker cắt cảnh, import asset (`import_file`, `asset_collection`, `instance`, `nla_sequence`), thiết lập render (EEVEE, AgX, bloom) |
| `render.py` | Render mọi shot theo chế độ `stills` / `preview` / `final`, ghi vào `renders/` cạnh file `.blend` |
| `mux_audio.py` | Ghép file âm thanh vào video đã render, không render lại hình (giữ nguyên màu) |
| `run.ps1` | Lệnh chạy nhanh cho một shot |
| `sound/sfx.py` | Thư viện tiếng hoạt hình viết bằng numpy: dao động, lọc, bao âm, hiệu ứng (boing, bloop, sấm, mưa, gió…), bộ trộn `Track`, xuất WAV |
| `tools/make_previews.py` | Render bảng xem trước cho một thư mục model (`.gltf`, `.glb`, `.fbx`) |

## Dùng trong build script

Build script nằm ở `<studio>/<nhóm>/<thư mục>/` (ví dụ `lab/shot02_max_power/build_shot.py`):

```python
HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(STUDIO, "pipeline"))
from lablib import ...
```

Shot nằm sâu hơn (`04_PRODUCTION/EP001_.../sh010/`) thì lùi thêm một cấp thư mục.

## `run.ps1`

Chạy từ thư mục gốc dự án. `-Shot` là đường dẫn thư mục shot tính từ gốc (mặc định `lab\shot02_max_power`). Tên file `.blend` lấy theo phần đầu tên thư mục: `shot01_dawn` thành `shot01.blend`, `sh010` thành `sh010.blend`.

```powershell
.\pipeline\run.ps1 build                            # dựng lại <shot>.blend từ build_shot.py
.\pipeline\run.ps1 stills                           # các khung mẫu định sẵn của shot
.\pipeline\run.ps1 stills 300,540                   # chỉ các khung muốn xem
.\pipeline\run.ps1 preview                          # cả shot 960x540 -> renders\<shot>_preview.mp4
.\pipeline\run.ps1 final                            # 1920x1080 + motion blur (vài giờ)
.\pipeline\run.ps1 audio                            # tạo lại âm thanh (build_audio.py) rồi ghép vào video preview
.\pipeline\run.ps1 open                             # mở trong Blender GUI (Space để play)
.\pipeline\run.ps1 mcp                              # mở kèm --online-mode để add-on MCP tự bật
.\pipeline\run.ps1 preview -Shot lab\shot01_dawn    # làm việc với shot khác
```

## Blender MCP (bản chính thức của Blender Lab)

Cho phép Claude điều khiển trực tiếp Blender đang mở: đọc scene, chạy Python, chụp viewport.

| Thành phần | Vị trí |
|---|---|
| Add-on `MCP` v1.0.3 | Đã cài và bật trong Blender 5.2 (repo `user_default`) |
| MCP server | `C:\Users\APC\blender_mcp_src\.venv\Scripts\blender-mcp.exe` (venv riêng, mã nguồn v1.0.3 cạnh đó) |
| Đăng ký với Claude Code | Scope `local` cho thư mục `studio` (`claude mcp get blender`) |

Cách dùng:
1. Mở Blender với `.\pipeline\run.ps1 mcp`. Add-on chỉ tự bật khi Blender được phép truy cập mạng. Lệnh này dùng cờ `--online-mode` cho riêng lần chạy đó. Nếu muốn mở Blender bình thường, bật **Edit → Preferences → System → Network → Allow Online Access**.
2. Mở một phiên Claude **mới** trong thư mục `studio`. Phiên mới sẽ có các tool `execute_blender_code`, `get_objects_summary`, `get_screenshot_of_window_as_image`…
3. Add-on chỉ lắng nghe ở `127.0.0.1:9876` (trong máy, không mở ra ngoài).

⚠️ MCP chạy code do AI viết **không có lớp bảo vệ**. Hãy lưu file trước khi thử, và chép những thay đổi ưng ý vào build script để giữ lâu dài.

Ghi chú: Avast quét HTTPS làm hỏng `pip install` (lỗi `InvalidChunkLength`). Khi cần cài thư viện Python, tạm tắt Avast shields 10 phút.
