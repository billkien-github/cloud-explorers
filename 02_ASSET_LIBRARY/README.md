# Asset Library

| | |
|---|---|
| [`MESHY.md`](MESHY.md) | Cách làm nhân vật, đạo cụ bằng Meshy + Blender, prompt |
| [`Third_Party/README.md`](Third_Party/README.md) | Nguồn asset bên ngoài, giấy phép, gợi ý cho tập 01 |

## Quy ước cho mỗi asset

```
Characters/Lumo/
├── concept/          Ảnh 2D: ảnh hero, turnaround, ảnh A-pose đưa vào Meshy
├── source/           File gốc tải từ Meshy (FBX + animation). Không sửa, chỉ thêm bản mới
├── build_lumo.py     Script: import source, thêm xương, face rig, material -> lumo_rig.blend
├── lumo_rig.blend    File đã rig, do script tạo ra (dùng trong shot)
└── qa/               Ảnh kiểm tra tư thế, biểu cảm, số liệu độ méo
```

- File Meshy mới thì tăng số phiên bản (`lumo_meshy_v02.fbx`), không ghi đè bản cũ.
- Shot dùng asset bằng cách import hoặc link `<tên>_rig.blend`, không sửa asset ngay trong shot.
- `Props/`, `Environments/` theo cùng cách. `Materials/` chứa material dùng chung, `Animation_Library/` chứa animation dùng lại cho nhiều nhân vật.
