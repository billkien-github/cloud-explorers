"""
In CC (thoại + hành động) lên một video previz đã render và xuất file .srt, không render lại hình:
    blender -b --factory-startup -P cc.py -- <video.mp4> <timing.py> <out.mp4> [giây bắt đầu trong cảnh]
timing.py là file mốc thời gian của cảnh (03_CONTENT/PREVIZ_2D.md), có CC = [(bắt đầu, kết thúc, "chữ"), ...]
tính theo giây trong cảnh. Previz khối của một đoạn thì truyền giây bắt đầu của đoạn để dời CC về 0.
Ghi thêm <out>.srt cạnh video.
"""
import importlib.util
import os
import sys

import bpy

args = sys.argv[sys.argv.index("--") + 1:]
video, timing_path, out = (os.path.abspath(a) for a in args[:3])  # Blender cần đường dẫn tuyệt đối
offset = float(args[3]) if len(args) > 3 else 0.0

sys.dont_write_bytecode = True  # không để __pycache__ cạnh timing.py
spec = importlib.util.spec_from_file_location("timing", timing_path)
T = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
# video đã được chỉnh màu lúc render -> giữ nguyên, không để AgX áp thêm lần nữa
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
clip = bpy.data.movieclips.load(video)
w, h, n, fps = clip.size[0], clip.size[1], clip.frame_duration, clip.fps
r = sc.render
r.fps, r.fps_base = round(fps), round(fps) / fps
r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100
sc.frame_start, sc.frame_end = 1, n
dur = n / fps
ed = sc.sequence_editor_create()
ed.strips.new_movie("Video", video, 1, 1)
try:
    ed.strips.new_sound("Audio", video, 2, 1)  # giữ tiếng nếu video có
except RuntimeError:
    pass

# dời về giây của video; các dòng chồng nhau thì gộp: chia trục thời gian ở mọi mốc, mỗi đoạn hiện mọi dòng đang chạy
items = [(a - offset, b - offset, text) for a, b, text in T.CC if b - offset > 0 and a - offset < dur]
marks = sorted({min(max(0.0, t), dur) for a, b, _ in items for t in (a, b)})
segs = []
for a, b in zip(marks, marks[1:]):
    texts = [text for s, e, text in items if s < b and e > a]
    if not texts:
        continue
    if segs and segs[-1][2] == texts and abs(segs[-1][1] - a) < 1e-6:
        segs[-1] = (segs[-1][0], b, texts)
    else:
        segs.append((a, b, texts))

for i, (a, b, texts) in enumerate(segs):
    f0, f1 = 1 + round(a * fps), 1 + round(b * fps)
    if f1 <= f0:
        continue
    t = ed.strips.new_effect(f"CC{i:03d}", type="TEXT", channel=3, frame_start=f0, length=f1 - f0)
    t.text = "\n".join(texts)
    t.font_size = round(h * 0.045)
    t.location = (0.5, 0.05)
    t.anchor_x, t.anchor_y, t.alignment_x = "CENTER", "BOTTOM", "CENTER"
    t.wrap_width = 0.9
    t.color = (1, 1, 1, 1)
    t.use_box, t.box_color, t.box_margin = True, (0, 0, 0, 0.6), 0.01


def srt_time(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


with open(os.path.splitext(out)[0] + ".srt", "w", encoding="utf-8") as fh:
    for i, (a, b, texts) in enumerate(segs, 1):
        fh.write(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n" + "\n".join(texts) + "\n\n")

im = r.image_settings
im.media_type = "VIDEO"
im.file_format = "FFMPEG"
r.ffmpeg.format, r.ffmpeg.codec, r.ffmpeg.constant_rate_factor = "MPEG4", "H264", "HIGH"
r.ffmpeg.audio_codec = "AAC"
r.filepath = out
bpy.ops.render.render(animation=True)
print("CC_DONE", out, f"{len(segs)} đoạn CC")
