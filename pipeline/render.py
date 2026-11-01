"""
Render một shot theo 3 chế độ (dùng chung cho mọi shot):
    blender -b <shot>.blend -P render.py -- stills [frame,frame,...]   # vài khung PNG để duyệt look
    blender -b <shot>.blend -P render.py -- preview                    # cả shot, 960x540, ít sample -> MP4
    blender -b <shot>.blend -P render.py -- final                      # 1920x1080, chất lượng cao -> MP4
Ảnh/video ghi vào thư mục renders/ cạnh file .blend, đặt tên theo tên file.
"""
import bpy
import os
import sys

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
mode = argv[0] if argv else "stills"
here = os.path.dirname(bpy.data.filepath)
stem = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
out_dir = os.path.join(here, "renders")
os.makedirs(out_dir, exist_ok=True)

scene = bpy.context.scene
r = scene.render
ee = scene.eevee


def video(path):
    im = r.image_settings
    im.media_type = "VIDEO"
    im.file_format = "FFMPEG"
    r.ffmpeg.format = "MPEG4"
    r.ffmpeg.codec = "H264"
    r.ffmpeg.constant_rate_factor = "HIGH"
    r.ffmpeg.audio_codec = "AAC"          # kèm âm thanh nếu scene có sound strip
    r.ffmpeg.audio_bitrate = 192
    r.ffmpeg.audio_channels = "STEREO"
    r.ffmpeg.audio_mixrate = 48000
    r.filepath = path


if mode == "stills":
    default = scene.get("lab_stills", "1,180,360,480,600,720")
    frames = [int(f) for f in (argv[1] if len(argv) > 1 else default).split(",")]
    r.resolution_percentage = 50
    ee.taa_render_samples = 16
    r.image_settings.media_type = "IMAGE"
    r.image_settings.file_format = "PNG"
    for f in frames:
        scene.frame_set(f)
        r.filepath = os.path.join(out_dir, "stills", f"f{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        print("WROTE", r.filepath)

elif mode == "preview":
    r.resolution_percentage = 50
    ee.taa_render_samples = 8
    ee.volumetric_samples = 32
    video(os.path.join(out_dir, f"{stem}_preview.mp4"))
    bpy.ops.render.render(animation=True)

elif mode == "final":
    r.resolution_percentage = 100
    ee.taa_render_samples = 64
    r.use_motion_blur = True
    video(os.path.join(out_dir, f"{stem}_final.mp4"))
    bpy.ops.render.render(animation=True)

else:
    raise SystemExit(f"unknown mode: {mode}")
