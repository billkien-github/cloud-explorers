"""
In CC (thoại + hành động) lên một video previz đã render và xuất file .srt, không render lại hình:
    blender -b --factory-startup -P cc.py -- <video.mp4> <timing.py> <out.mp4> [giây bắt đầu trong cảnh]
timing.py là file mốc thời gian của cảnh (03_CONTENT/PREVIZ_2D.md), có CC = [(bắt đầu, kết thúc, "chữ"), ...]
tính theo giây trong cảnh. Previz khối của một đoạn thì truyền giây bắt đầu của đoạn để dời CC về 0.
Ghi thêm <out>.srt cạnh video. Là edit.py với một video, không cắt.
"""
import os
import sys

sys.dont_write_bytecode = True  # không để __pycache__ trong pipeline/ hay cạnh timing.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edit  # noqa: E402

args = sys.argv[sys.argv.index("--") + 1:]
video, timing_path, out = (os.path.abspath(a) for a in args[:3])  # Blender cần đường dẫn tuyệt đối
offset = float(args[3]) if len(args) > 3 else 0.0
edit.assemble([edit.clip(video, cc=(timing_path, offset))], out)
