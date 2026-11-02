# Cloud Explorers

Phim hoạt hình 3D cho trẻ em, phát hành YouTube-first. Bốn người bạn Lumo, Tavi, Nori, Piko phiêu lưu qua những vùng đất kỳ diệu. Dựng bằng **Blender**, phần lớn bằng **code Python**. Hình nhân vật và đạo cụ sinh bằng **Meshy**.

## Dự án

| | |
|---|---|
| Mô hình | Studio nhỏ (2–5 người), **YouTube-first** |
| Khán giả | Trẻ em, Việt Nam + quốc tế (một bộ hình, nhiều bản lồng tiếng) |
| Mục tiêu năm 1 | Views. Sau 12 tháng cần **1 IP có tiềm năng + 1 pipeline 3D hiệu quả + 1 format đã được kiểm chứng** |
| Nguyên tắc số 1 | **Content đi trước production**: chốt câu chuyện rồi mới modeling |
| Lộ trình 12 tháng | Foundation (T1–2) → Prototype (T3–4) → Validation (T5–6) → Growth (T7–8) → Brand (T9–10) → Scale (T11–12) |

Chính sách YouTube: nội dung cho trẻ phải khai báo **Made for Kids** (mất bình luận, thông báo, quảng cáo cá nhân hoá). Chính sách **inauthentic content** nhắm vào nội dung hàng loạt, lặp lại: tái sử dụng asset được, nhưng mỗi tập phải có câu chuyện riêng thật sự.

## Trạng thái

- Có: concept 4 nhân vật, 4 bảo bối, ảnh thế giới; ảnh đầu vào Meshy cho cả 8 asset (Lumo đã đạt cả A-pose và T-pose; Tavi, Nori, Piko cần sửa ảnh bằng GPT trước, prompt trong `02_ASSET_LIBRARY/MESHY.md`); beat sheet tập 01 đã chốt (khoảng 7 phút); code dùng chung trong `pipeline/`.
- Lumo: `02_ASSET_LIBRARY/Characters/Lumo/lumo_rig.blend` dựng từ bản Meshy v01 bằng `build_lumo.py`: thêm xương đuôi, tai, IK chân và tay (IK tay mặc định tắt), texture 2K; mặc áo choàng ngắn, đeo túi và dây chéo; mặt bản đầu: chớp mắt, mở miệng (thanh trượt `blink_L`, `blink_R`, `mouth_open`); qua kiểm tra `qa_lumo.py` (bad% ≤ 2.4%). Chưa có: lông mày, đồng tử, hình miệng khác; áo choàng và túi chưa có chuyển động riêng.
- Shot dựng thử `04_PRODUCTION/EP001_Great_Rain_Experiment/sh030`: Lumo vấp vết nứt (7 giây, animation hoàn toàn bằng code, chưa có tiếng).
- Clip thử `04_PRODUCTION/TEST_Lumo_Dance/sh010`: Lumo nhảy kiểu "Baby Shark" 16 giây, có hát (mở miệng theo nốt), chớp mắt, nhạc nền tự sáng tác (`build_audio.py`).
- Chưa có: kịch bản, model của Tavi, Nori, Piko và đạo cụ.
- **Bước tiếp theo:** viết kịch bản tập 01 bằng Fountain (`03_CONTENT/Scripts/template.fountain`). Song song: hoàn thiện face rig Lumo (lông mày, đồng tử, hình miệng), xương vạt áo choàng để áo bay khi chạy.

## Tài liệu

| File | Nội dung |
|---|---|
| [`01_BRAND/Character_Bible/README.md`](01_BRAND/Character_Bible/README.md) | Nhân vật: tính cách, ngoại hình, màu, chiều cao, bảo bối, cách làm 3D |
| [`03_CONTENT/README.md`](03_CONTENT/README.md) | Hướng nội dung: công thức, 5 series, khung tập 6–8 phút, nhịp cho trẻ em, luật đạo cụ, cách viết kịch bản |
| [`03_CONTENT/Scripts/EP001_great_rain_experiment.md`](03_CONTENT/Scripts/EP001_great_rain_experiment.md) | Beat sheet tập 01 |
| [`02_ASSET_LIBRARY/README.md`](02_ASSET_LIBRARY/README.md) | Quy ước thư mục asset |
| [`02_ASSET_LIBRARY/MESHY.md`](02_ASSET_LIBRARY/MESHY.md) | Làm nhân vật, đạo cụ bằng Meshy + Blender, prompt |
| [`02_ASSET_LIBRARY/Third_Party/README.md`](02_ASSET_LIBRARY/Third_Party/README.md) | Nguồn asset bên ngoài, giấy phép |
| [`pipeline/README.md`](pipeline/README.md) | Code dùng chung, cách render, Blender MCP |
| [`CLAUDE.md`](CLAUDE.md) | Dặn dò cho agent: file nào sở hữu chủ đề nào, việc review và dọn tài liệu sau mỗi lần làm |

## Cấu trúc thư mục

```
studio/
├── 01_BRAND/                Logo/, Brand_Guideline/ (world_key_art.png), Character_Bible/
├── 02_ASSET_LIBRARY/        Characters/, Props/, Environments/, Materials/, Animation_Library/, Third_Party/
├── 03_CONTENT/              Scripts/, Storyboards/, Animatics/
├── 04_PRODUCTION/           Mỗi tập một thư mục, mỗi shot một thư mục con: EP001_Great_Rain_Experiment/sh010/; clip thử: TEST_<tên>/
├── 05_POST_PRODUCTION/      Editing/, Sound/, Dubbing/
├── 06_PUBLISHING/           Thumbnails/, Metadata/ (tiêu đề, mô tả, CREDITS.md), Final_Videos/
├── 07_ANALYTICS/            Monthly_Report/, Annual_Report/
└── pipeline/                Code dùng chung
```

## Quy ước

- **Dựng bằng script:** mỗi asset hay shot có script build nằm cạnh nó. Sửa script rồi build lại, không sửa tay file `.blend` do script tạo ra (thử bằng tay qua Blender MCP xong thì chép thay đổi vào script).
- **File gốc tải về không sửa:** file Meshy để trong `source/`, đồ bên thứ ba trong `Third_Party/`.
- **Đặt tên:** thư mục viết hoa chữ đầu, nối bằng gạch dưới (`EP001_Great_Rain_Experiment`, `Wonder_Compass`). File viết thường, không dấu, nối bằng gạch dưới (`lumo_hero.png`); riêng mã tập giữ viết hoa (`EP001_great_rain_experiment.md`). Không dùng dấu tiếng Việt trong tên file vì Blender và ffmpeg hay lỗi đường dẫn.
- **Shot:** `sh010/` gồm `build_shot.py`, `sh010.blend`, `renders/`. Đánh số cách 10 để còn chèn shot vào giữa.
- **Tài liệu chỉ ghi thông tin hiện hành**, mỗi thông tin chỉ nằm ở một file (bảng file sở hữu và cách giữ tài liệu: `CLAUDE.md`). Lịch sử đã có git.

## Công cụ

| Công cụ | Ghi chú |
|---|---|
| Blender 5.2.3 LTS | `C:\Program Files\Blender Foundation\Blender 5.2`. Render bằng EEVEE vì máy chỉ có card tích hợp Vega 11 |
| Python của Blender | `...\Blender 5.2\5.2\python\bin\python.exe`, có sẵn numpy |
| Meshy (gói Pro) | Sinh hình, Remesh, rig Humanoid, thư viện animation |
| Blender MCP | Cho Claude điều khiển Blender đang mở, xem `pipeline/README.md` |

## Git

- Repo: https://github.com/billkien-github/cloud-explorers
- File nhị phân (`.blend`, ảnh, video, âm thanh, FBX/GLB, zip) đi qua **Git LFS** (`.gitattributes`).
- Không đưa lên git (`.gitignore`): `*.blend1`, log, cache Python, mọi thư mục `renders/`, `06_PUBLISHING/Final_Videos/`.
