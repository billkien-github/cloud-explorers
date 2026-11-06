# Asset Library

| | |
|---|---|
| [`MODELING.md`](MODELING.md) | Làm nhân vật, đạo cụ 3D: bộ ảnh tham chiếu và hiện trạng, prompt ChatGPT, dựng và rig trong Blender |

## Quy ước cho mỗi asset

```
Characters/<Tên>/
├── concept/          Ảnh 2D: ảnh hero, ảnh tham chiếu dựng model (nhìn trước, sau; A-pose, T-pose)
├── build_<tên>.py    Script: dựng lưới, xương, face rig, material -> <tên>_rig.blend
├── <tên>_rig.blend   File đã rig, do script tạo ra (dùng trong shot)
├── qa_<tên>.py       Script kiểm tra rig (dùng pipeline/rig_qa.py)
└── qa/               Bảng ảnh tư thế, số liệu độ méo
```

- Ảnh trong `concept/`:
  - `<tên>_hero.png`: ảnh minh hoạ có bối cảnh (nhân vật chính, bối cảnh). Đạo cụ không có ảnh hero, dùng `_ref`.
  - `<tên>_ref.png`: ảnh concept nền trơn, nhìn 3/4 hoặc nhiều tư thế (đạo cụ, sinh vật nhỏ); ảnh gốc để sinh các ảnh tham chiếu. Ảnh gốc của nhân vật đã xoá sau khi sinh xong bộ ảnh tham chiếu.
  - `<tên>_apose_body.png`, `<tên>_tpose_body.png`: chỉ phần thân, A-pose / T-pose. `<tên>_outfit.png`: thân A-pose mặc đủ đồ.
  - `<tên>_<bộ phận>_ref.png`: một bộ phận làm riêng (đuôi, cánh, áo choàng, túi).
  - Đạo cụ, thú bốn chân và nhân vật phụ không có A-pose: đặt tên theo hướng nhìn, `<tên>_front.png`, `_back.png`, `_side.png`, `_top.png`; ảnh trạng thái đặt theo trạng thái (`_frost`, `_bent`, `_closed`…).
  - Ảnh nhìn sau thêm hậu tố `_back` vào cuối tên ảnh nhìn trước: `lumo_apose_body_back.png`, `piko_pouch_ref_back.png`. Bộ ảnh cần có: `MODELING.md`.
  - `<tên>_turnaround.png`: ảnh xoay làm tham chiếu Seedance, ảnh đủ đồ nhìn trước (trái) và nhìn sau (phải) ghép bằng `pipeline/turnaround.py`. Không sửa tay; ảnh nguồn đổi thì chạy lại script.
  - Tiền tố là tên vật trong ảnh: thư mục chứa nhiều vật thì mỗi vật một tiền tố (`Environments/Noah_Story/`: `noah_ark_…`, `plank_bridge_…`; nắp che nút trong `Props/Rain_O_Matic/`: `button_cover_…`). Ảnh cả nhóm dùng số nhiều (`valley_critters_ref.png`, `baby_elephants_ref.png`), ảnh một cá thể dùng số ít (`valley_critter_apose_body.png`, `baby_elephant_front.png`).
- Shot dùng asset bằng cách import hoặc link `<tên>_rig.blend`, không sửa asset ngay trong shot.
- `Props/`, `Environments/` theo cùng cách. `Materials/` chứa material dùng chung, `Animation_Library/` chứa animation dùng lại cho nhiều nhân vật.
