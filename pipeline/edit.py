"""
Ghép nhiều video thành một: cắt đầu đuôi từng video, nối liền, thêm tiếng (lồng tiếng, nhạc), in CC từ timing.py của
cảnh và xuất .srt. Chạy bằng Blender, máy không cần ffmpeg:
    blender -b --factory-startup -P pipeline/edit.py -- <danh_sach_dung.py> [--clean] [--srt-only] [-o <out.mp4>]
    blender -b --factory-startup -P pipeline/edit.py -- <a.mp4> <b.mp4> ... -o <out.mp4>     (nối nguyên, không CC)

Danh sách dựng là một file .py, đường dẫn tính từ chính file đó:
    CLIPS = [
        "sh010/seedance/takes/sh010_take01.mp4",              # video của shot: cắt và CC theo build_shot.py của shot
        ("khac.mp4", 1.5, 6.0),                                # (video, giây vào, giây ra); giây ra None = tới hết
        ("khac.mp4", 0, None, ("scene03/timing.py", 12.0)),     # kèm CC: (timing.py, giây trong cảnh ứng với giây vào)
    ]
    AUDIO = [("long_tieng.wav", 0.0, 1.0)]  # tuỳ chọn: (file, giây bắt đầu trên bản dựng, âm lượng)
    CLIP_VOLUME = 1.0                        # tuỳ chọn: âm lượng tiếng có sẵn trong các video, 0 để tắt
    SIZE = (1920, 1080)                      # tuỳ chọn: mặc định theo video đầu tiên; video khác cỡ co giãn vừa khung
    OUT = "renders/scene01.mp4"               # tuỳ chọn: mặc định renders/<tên danh sách>.mp4 cạnh danh sách

Video nằm trong <shot>/seedance/takes/ hay <shot>/renders/: đọc build_shot.py của shot (không chạy), cắt từ 0 tới SEGMENT
(không có SEGMENT thì giữ nguyên), CC lấy từ TIMING dời theo OFFSET. Thư mục cảnh previz 2D có timing.py cạnh
build_shot.py thì lấy CC từ đó. Video chưa có file thì thay bằng khung tối ghi tên file, dài bằng giây ra, SEGMENT hay
SECONDS, để các đoạn sau và CC không lệch. Mọi video phải cùng fps.

Mặc định in CC lên hình (tên file ra thêm _cc) và ghi .srt cạnh video ra. --clean: không in CC lên hình, vẫn ghi .srt
(bản đăng YouTube, tải .srt lên làm phụ đề riêng). --srt-only: chỉ ghi .srt, không render.
"""
import ast
import importlib.util
import os
import sys

import bpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # gốc repo: TIMING trong build_shot.py tính từ đây


def fail(msg):
    raise SystemExit(f"edit.py: {msg}")


def clip(video, vin=0.0, vout=None, cc=None, length=None):
    """Một đoạn của bản dựng. cc = (timing.py, giây trong cảnh ứng với giây vào); length = độ dài khi thiếu file."""
    return {"video": os.path.abspath(video), "vin": float(vin), "vout": vout, "cc": cc, "length": length}


def load_py(path):
    sys.dont_write_bytecode = True  # không để __pycache__ cạnh danh sách dựng, timing.py
    spec = importlib.util.spec_from_file_location("_edit_data", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def shot_consts(build_py):
    """Các hằng số gán bằng giá trị cố định ở cấp ngoài cùng của build_shot.py (TIMING, OFFSET, SEGMENT, SECONDS…)."""
    with open(build_py, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    out = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for tgt in node.targets:
            if isinstance(tgt, ast.Name):
                pairs = [(tgt, node.value)]
            elif isinstance(tgt, ast.Tuple) and isinstance(node.value, ast.Tuple) and len(tgt.elts) == len(node.value.elts):
                pairs = zip(tgt.elts, node.value.elts)  # FPS, SECONDS = 24, 27
            else:
                continue
            for name, value in pairs:
                if isinstance(name, ast.Name):
                    try:
                        out[name.id] = ast.literal_eval(value)
                    except (ValueError, TypeError):
                        pass
    return out


def shot_clip(video):
    """Video trong <shot>/seedance/takes/ hay <shot>/renders/: cắt và CC theo build_shot.py của shot."""
    up1 = os.path.dirname(video)
    for d in (up1, os.path.dirname(up1), os.path.dirname(os.path.dirname(up1))):
        if os.path.isfile(os.path.join(d, "build_shot.py")):
            break
    else:
        return clip(video)
    k = shot_consts(os.path.join(d, "build_shot.py"))
    if isinstance(k.get("TIMING"), str):
        timing = os.path.normpath(os.path.join(ROOT, k["TIMING"]))
    elif os.path.isfile(os.path.join(d, "timing.py")):
        timing = os.path.join(d, "timing.py")  # cảnh previz 2D: timing.py nằm cạnh build_shot.py
    else:
        timing = None
    cc = (timing, float(k.get("OFFSET", 0.0))) if timing else None
    return clip(video, 0.0, k.get("SEGMENT"), cc, k.get("SEGMENT", k.get("SECONDS")))


def parse_clip(entry, base):
    if isinstance(entry, str):
        return shot_clip(os.path.normpath(os.path.join(base, entry)))
    entry = tuple(entry)
    video = os.path.normpath(os.path.join(base, entry[0]))
    vin = entry[1] if len(entry) > 1 else 0.0
    vout = entry[2] if len(entry) > 2 else None
    cc = entry[3] if len(entry) > 3 else None
    if cc:
        cc = (os.path.normpath(os.path.join(base, cc[0])), float(cc[1]))
    return clip(video, vin, vout, cc)


def cc_segments(items):
    """items = [(giây bắt đầu, kết thúc, chữ)] trên bản dựng. Các dòng chồng nhau thì gộp: chia trục thời gian ở mọi
    mốc, mỗi đoạn hiện mọi dòng đang chạy; hai đoạn liền nhau cùng chữ (một dòng vắt qua chỗ nối) nối lại thành một."""
    marks = sorted({t for a, b, _ in items for t in (a, b)})
    segs = []
    for a, b in zip(marks, marks[1:]):
        texts = [text for s, e, text in items if s < b and e > a]
        if not texts:
            continue
        if segs and segs[-1][2] == texts and abs(segs[-1][1] - a) < 1e-6:
            segs[-1] = (segs[-1][0], b, texts)
        else:
            segs.append((a, b, texts))
    return segs


def srt_time(t):
    ms = round(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(path, segs):
    with open(path, "w", encoding="utf-8") as fh:
        for i, (a, b, texts) in enumerate(segs, 1):
            fh.write(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n" + "\n".join(texts) + "\n\n")


def assemble(clips, out, audio=(), clip_volume=1.0, size=None, burn_cc=True, render=True):
    """Dựng clips nối liền (đường dẫn tuyệt đối), ghi <out>.srt nếu có CC, rồi render ra out (trừ khi render=False)."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    # video đã được chỉnh màu lúc render -> giữ nguyên, không để AgX áp thêm lần nữa
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    ed = sc.sequence_editor_create()

    for c in clips:
        c["exists"] = os.path.isfile(c["video"])
        if c["exists"]:
            mc = bpy.data.movieclips.load(c["video"])
            c["fps"], c["size"], c["frames"] = mc.fps, tuple(mc.size), mc.frame_duration
            bpy.data.movieclips.remove(mc)
    real = [c for c in clips if c["exists"]]
    fps = real[0]["fps"] if real else 24.0
    for c in real:
        if abs(c["fps"] - fps) > 0.01:
            fail(f"{c['video']} là {c['fps']:g} fps, khác {fps:g} fps của video đầu. Đưa về cùng fps rồi mới ghép.")
    w, h = size or (real[0]["size"] if real else (1920, 1080))
    r = sc.render
    r.fps, r.fps_base = round(fps), round(fps) / fps
    r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100

    # kênh: 1 hình, 2 tiếng của video, 3 chữ báo thiếu file, 4.. AUDIO, trên cùng CC
    items, timings, t = [], {}, 1
    for i, c in enumerate(clips):
        name = os.path.relpath(c["video"], ROOT) if c["video"].startswith(ROOT) else c["video"]
        fin = round(c["vin"] * fps)
        if c["exists"]:
            fout = c["frames"] if c["vout"] is None else round(c["vout"] * fps)
            if fout > c["frames"]:
                print(f"  ! {name} chỉ dài {c['frames'] / fps:.2f} s, ngắn hơn giây ra {c['vout']:.2f} s: lấy tới hết")
                fout = c["frames"]
        else:
            end = c["vout"] if c["vout"] is not None else c["length"]
            if end is None:
                fail(f"Không có file {name}, cũng không biết đoạn dài bao nhiêu (ghi giây ra trong danh sách dựng).")
            fout = round(end * fps)
        n = fout - fin
        if n <= 0:
            fail(f"{name}: giây vào {c['vin']:g} không nhỏ hơn giây ra {fout / fps:g}.")

        if c["exists"]:
            # đặt ở t (sau mọi đoạn trước), cắt hai đầu, rồi dời về để giây vào rơi đúng t: không lúc nào đè đoạn trước
            v = ed.strips.new_movie(f"V{i:03d}", c["video"], 1, t, fit_method="FIT")
            v.left_handle_offset, v.right_handle_offset = fin, v.content_duration - fout
            v.content_start = t - fin
            if clip_volume > 0:
                try:
                    a = ed.strips.new_sound(f"A{i:03d}", c["video"], 2, t)
                except RuntimeError:
                    a = None
                if a is not None and a.content_duration <= 1:  # video không có tiếng
                    ed.strips.remove(a)
                elif a is not None:
                    a.left_handle_offset = min(fin, a.content_duration - 1)
                    a.right_handle_offset = max(0, a.content_duration - fout)
                    a.content_start = t - fin
                    a.volume = clip_volume
        else:
            print(f"  ! Chưa có {name}: thay bằng khung tối {n / fps:.2f} s")
            g = ed.strips.new_effect(f"Thieu{i:03d}", type="COLOR", channel=1, frame_start=t, length=n)
            g.color = (0.08, 0.08, 0.1)
            lab = ed.strips.new_effect(f"ThieuChu{i:03d}", type="TEXT", channel=3, frame_start=t, length=n)
            lab.text = f"CHƯA CÓ\n{os.path.basename(c['video'])}"
            lab.font_size = round(h * 0.05)
            lab.location = (0.5, 0.55)
            lab.anchor_x, lab.anchor_y, lab.alignment_x = "CENTER", "CENTER", "CENTER"
            lab.color = (0.6, 0.6, 0.6, 1)

        note = ""
        if c["cc"]:
            path, scene_in = c["cc"]
            if path not in timings:
                if not os.path.isfile(path):
                    fail(f"Không có file CC {path}")
                timings[path] = load_py(path)
            s0, s1, shift = scene_in, scene_in + n / fps, (t - 1) / fps - scene_in
            for a_, b_, text in timings[path].CC:
                a2, b2 = max(a_, s0), min(b_, s1)
                if b2 > a2:
                    items.append((a2 + shift, b2 + shift, text))
            note = f"  CC {os.path.relpath(path, ROOT)} từ {scene_in:g} s"
        print(f"  {i + 1:2d}. {(t - 1) / fps:7.2f}–{(t - 1 + n) / fps:6.2f} s  {name} [{fin / fps:g}–{fout / fps:g} s]{note}")
        t += n
    sc.frame_start, sc.frame_end = 1, t - 1
    dur = (t - 1) / fps

    for k, entry in enumerate(audio):
        path, start, vol = (tuple(entry) + (0.0, 1.0))[:3]
        if not os.path.isfile(path):
            fail(f"Không có file tiếng {path}")
        s = ed.strips.new_sound(f"Am{k:02d}", path, 4 + k, 1 + round(start * fps))
        s.volume = vol
        if s.right_handle > t:
            s.right_handle = t  # cắt phần thừa sau cuối bản dựng

    segs = cc_segments(items)
    if segs:
        cc_channel = 4 + len(audio)
        if burn_cc and render:
            for i, (a, b, texts) in enumerate(segs):
                f0, f1 = 1 + round(a * fps), 1 + round(b * fps)
                if f1 <= f0:
                    continue
                s = ed.strips.new_effect(f"CC{i:03d}", type="TEXT", channel=cc_channel, frame_start=f0, length=f1 - f0)
                s.text = "\n".join(texts)
                s.font_size = round(h * 0.045)
                s.location = (0.5, 0.05)
                s.anchor_x, s.anchor_y, s.alignment_x = "CENTER", "BOTTOM", "CENTER"
                s.wrap_width = 0.9
                s.color = (1, 1, 1, 1)
                s.use_box, s.box_color, s.box_margin = True, (0, 0, 0, 0.6), 0.01
        os.makedirs(os.path.dirname(out), exist_ok=True)
        write_srt(os.path.splitext(out)[0] + ".srt", segs)
        print(f"SRT {os.path.splitext(out)[0]}.srt, {len(segs)} đoạn CC")
    if not render:
        return

    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = r.image_settings
    im.media_type = "VIDEO"
    im.file_format = "FFMPEG"
    r.ffmpeg.format, r.ffmpeg.codec, r.ffmpeg.constant_rate_factor = "MPEG4", "H264", "HIGH"
    r.ffmpeg.audio_codec, r.ffmpeg.audio_bitrate = "AAC", 192
    r.ffmpeg.audio_channels, r.ffmpeg.audio_mixrate = "STEREO", 48000
    r.filepath = out
    bpy.ops.render.render(animation=True)
    print("EDIT_DONE", out, f"{w}x{h}, {dur:.2f} s, {len(segs)} đoạn CC" + (" in lên hình" if segs and burn_cc else ""))


def main(argv):
    flags = {a for a in argv if a in ("--clean", "--srt-only")}
    args, out = [], None
    it = iter(a for a in argv if a not in flags)
    for a in it:
        if a in ("-o", "--out"):
            out = next(it, None)
        else:
            args.append(a)
    if not args:
        fail(__doc__)
    render = "--srt-only" not in flags
    burn = render and "--clean" not in flags

    if len(args) == 1 and args[0].endswith(".py"):
        listing = os.path.abspath(args[0])
        base = os.path.dirname(listing)
        E = load_py(listing)
        clips = [parse_clip(e, base) for e in E.CLIPS]
        audio = [(os.path.normpath(os.path.join(base, a[0])),) + tuple(a[1:]) for a in getattr(E, "AUDIO", [])]
        clip_volume, size = getattr(E, "CLIP_VOLUME", 1.0), getattr(E, "SIZE", None)
        if out is None:
            stem = os.path.splitext(os.path.basename(listing))[0]
            out = os.path.join(base, getattr(E, "OUT", f"renders/{stem}.mp4"))
            if burn and any(c["cc"] for c in clips):
                out = os.path.splitext(out)[0] + "_cc.mp4"
    else:
        if out is None:
            fail("Nối video lẻ cần -o <file ra.mp4>.")
        clips = [clip(a) for a in args]
        audio, clip_volume, size = [], 1.0, None
    assemble(clips, os.path.abspath(out), audio, clip_volume, size, burn, render)


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])
