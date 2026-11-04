# Asset Library

| | |
|---|---|
| [`MESHY.md`](MESHY.md) | Cách làm nhân vật, đạo cụ bằng Meshy + Blender, prompt |
| [`Third_Party/README.md`](Third_Party/README.md) | Nguồn asset bên ngoài, giấy phép, gợi ý cho tập 01 |

## Quy ước cho mỗi asset

```
Characters/<Tên>/
├── concept/          Ảnh 2D: ảnh hero, turnaround, ảnh A-pose đưa vào Meshy
├── source/           File gốc tải từ Meshy, mỗi lần tải một thư mục <tên>_meshy_vNN/. Không sửa, chỉ thêm bản mới
├── build_<tên>.py    Script: import source, thêm xương, face rig, material -> <tên>_rig.blend
├── <tên>_rig.blend   File đã rig, do script tạo ra (dùng trong shot)
├── qa_<tên>.py       Script kiểm tra rig (dùng pipeline/rig_qa.py)
└── qa/               Bảng ảnh tư thế, số liệu độ méo
```

- Ảnh trong `concept/`:
  - `<tên>_hero.png`: ảnh minh hoạ có bối cảnh, để tham khảo.
  - `<tên>_apose.png`, `<tên>_tpose.png`: nhân vật 2 chân ở A-pose / T-pose, nền trơn, đầu vào Meshy.
  - `<tên>_ref.png`: một đối tượng, nền trơn (nhân vật không chân, đạo cụ), đầu vào Meshy.
  - Bản đã sửa cho Meshy thì thêm hậu tố mô tả: `lumo_apose_meshy.png`.
- Lần tải Meshy mới thì tạo thư mục phiên bản mới (`source/lumo_meshy_v02/`), giữ nguyên tên file của Meshy vì FBX gọi texture theo tên, không ghi đè bản cũ.
- Shot dùng asset bằng cách import hoặc link `<tên>_rig.blend`, không sửa asset ngay trong shot.
- `Props/`, `Environments/` theo cùng cách. `Materials/` chứa material dùng chung, `Animation_Library/` chứa animation dùng lại cho nhiều nhân vật.
