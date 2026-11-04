"""
Chuẩn bị một video shot cho skill /review: khung hình mẫu, điểm cắt, mức tiếng.
    blender -b --factory-startup -P extract_shot.py -- <video.mp4> <out_dir> [khung/giây, mặc định 1]
Ghi vào out_dir (xoá sạch trước): frames/t<giây>.jpg và review.json
(thông số video, danh sách khung, điểm cắt, độ chuyển động từng giây, mức tiếng theo từng 0.1 giây).
"""
import json
import os
import shutil
import sys

import bpy
import numpy as np

args = sys.argv[sys.argv.index("--") + 1:]
video, out = os.path.abspath(args[0]), os.path.abspath(args[1])  # Blender cần đường dẫn tuyệt đối
rate = float(args[2]) if len(args) > 2 else 1.0

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
# video đã được chỉnh màu lúc render -> giữ nguyên, không để AgX áp thêm lần nữa
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
clip = bpy.data.movieclips.load(video)
w, h, n, fps = clip.size[0], clip.size[1], clip.frame_duration, clip.fps
r = sc.render
r.fps, r.fps_base = round(fps), round(fps) / fps
r.resolution_x, r.resolution_y = w, h
sc.frame_start, sc.frame_end = 1, n
sc.sequence_editor_create().strips.new_movie("Video", video, 1, 1)
im = r.image_settings
im.media_type = "IMAGE"
im.file_format = "JPEG"
im.quality = 85

if os.path.isdir(out):
    shutil.rmtree(out)
os.makedirs(os.path.join(out, "frames"))

# 1) khung mẫu cho reviewer xem, rộng khoảng 768 px
r.resolution_percentage = max(1, min(100, round(76800 / w)))
frames, k = [], 0
while (f := 1 + round(k * fps / rate)) <= n:
    t = (f - 1) / fps
    name = f"frames/t{t:06.2f}.jpg"
    sc.frame_set(f)
    r.filepath = os.path.join(out, name)
    bpy.ops.render.render(write_still=True)
    frames.append({"file": name, "frame": f, "time_s": round(t, 2)})
    k += 1

# 2) điểm cắt: so từng cặp khung liền nhau ở bản rất nhỏ (rộng khoảng 96 px)
tiny = os.path.join(out, "_tiny")
os.makedirs(tiny)
r.resolution_percentage = max(1, round(9600 / w))
r.filepath = os.path.join(tiny, "f####")
bpy.ops.render.render(animation=True)
prev, diffs = None, []
for f in range(1, n + 1):
    img = bpy.data.images.load(os.path.join(tiny, f"f{f:04d}.jpg"))
    px = np.empty(len(img.pixels), dtype=np.float32)
    img.pixels.foreach_get(px)
    bpy.data.images.remove(img)
    px = px.reshape(-1, 4)[:, :3]
    if prev is not None:
        diffs.append(float(np.abs(px - prev).mean()))
    prev = px
shutil.rmtree(tiny)
limit = max(0.08, 4 * float(np.median(diffs))) if diffs else 1.0
cuts = [{"frame": i + 2, "time_s": round((i + 1) / fps, 2), "diff": round(d, 3)}
        for i, d in enumerate(diffs) if d > limit]
# độ chuyển động trung bình từng giây (bỏ các cặp khung là điểm cắt): gần 0 là hình đứng yên
cut_pairs = {c["frame"] - 2 for c in cuts}
motion = []
for s in range(int(np.ceil(n / fps))):
    ds = [d for i, d in enumerate(diffs) if s <= (i + 1) / fps < s + 1 and i not in cut_pairs]
    motion.append(round(float(np.mean(ds)), 4) if ds else 0.0)


# 3) tiếng: chỉ đo được mức, không nghe được chất lượng
def db(x):
    return round(float(20 * np.log10(max(float(x), 1e-6))), 1)


audio = None
try:
    import aud
    snd = aud.Sound(video)
    data = snd.data()
except Exception:
    data = None
if data is not None and data.size and np.abs(data).max() > 1e-4:  # render luôn kèm rãnh AAC, rãnh câm coi như không có tiếng
    data = data.reshape(len(data), -1)
    sr = snd.specs[0]
    win = int(sr * 0.1)
    seg = data[: len(data) // win * win].reshape(-1, win, data.shape[1])
    rms = np.sqrt((seg ** 2).mean(axis=(1, 2)))
    quiet = rms < 10 ** (-50 / 20)
    silent, start = [], None
    for i, q in enumerate(list(quiet) + [False]):
        if q and start is None:
            start = i
        elif not q and start is not None:
            if i - start >= 5:  # im lặng từ 0.5 giây
                silent.append([round(start * 0.1, 1), round(i * 0.1, 1)])
            start = None
    audio = {
        "sample_rate": sr,
        "channels": int(data.shape[1]),
        "peak_dbfs": db(np.abs(data).max()),
        "clipped_samples": int((np.abs(data) >= 0.999).sum()),
        "rms_dbfs_overall": db(np.sqrt((data ** 2).mean())),
        "window_s": 0.1,
        "rms_dbfs": [db(v) for v in rms],
        "silent_ranges_s": silent,
    }

info = {
    "video": video, "width": w, "height": h, "fps": round(fps, 3), "frame_count": n,
    "duration_s": round(n / fps, 2), "sample_frames_per_s": rate,
    "frames": frames, "cuts": cuts, "motion_per_s": motion, "audio": audio,
}
with open(os.path.join(out, "review.json"), "w", encoding="utf-8") as fh:
    json.dump(info, fh, ensure_ascii=False, indent=1)
print("REVIEW_READY", out, f"{len(frames)} khung, {len(cuts)} điểm cắt, tiếng: {'có' if audio else 'không'}")
