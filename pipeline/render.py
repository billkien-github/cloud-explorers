"""
Render một shot theo 3 chế độ (dùng chung cho mọi shot):
    blender -b <shot>.blend -P render.py -- stills [frame,frame,...]   # vài khung PNG để duyệt look
    blender -b <shot>.blend -P render.py -- preview                    # cả shot, 960x540, ít sample -> MP4
    blender -b <shot>.blend -P render.py -- final                      # 1920x1080, chất lượng cao -> MP4
    blender -b <shot>.blend -P render.py -- ref                        # 1920x1080, ít sample -> MP4 dẫn cho Seedance
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
    if len(argv) > 1:
        frames = [int(f) for f in argv[1].split(",")]
    elif "stills" in scene:                       # shot tự đặt khung mẫu: scene["stills"] = "1,120,240"
        frames = [int(f) for f in scene["stills"].split(",")]
    else:                                         # mặc định: 6 khung rải đều cả shot
        s, e = scene.frame_start, scene.frame_end
        frames = sorted({round(s + (e - s) * i / 5) for i in range(6)})
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

elif mode == "ref":                               # video tham chiếu cho Seedance: đủ 1080p, không cần đẹp
    r.resolution_percentage = 100
    ee.taa_render_samples = 8
    r.use_motion_blur = False
    video(os.path.join(out_dir, f"{stem}_ref.mp4"))
    r.ffmpeg.audio_codec = "NONE"                 # không kèm tiếng: rãnh AAC dài hơn hình vài phần trăm giây, đoạn 15 s vượt giới hạn video của Seedance
    bpy.ops.render.render(animation=True)

else:
    raise SystemExit(f"unknown mode: {mode}")
