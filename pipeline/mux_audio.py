"""
Ghép một file âm thanh vào video đã render (không cần render lại hình):
    blender -b --factory-startup -P mux_audio.py -- <video.mp4> <audio.wav> <out.mp4>
"""
import sys

import bpy

video, audio, out = sys.argv[sys.argv.index("--") + 1:][:3]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
# video đã được chỉnh màu lúc render -> ghép lại phải giữ nguyên (mặc định AgX sẽ áp thêm lần nữa, làm bạc màu)
sc.view_settings.view_transform = "Standard"
sc.view_settings.look = "None"
sc.view_settings.exposure, sc.view_settings.gamma = 0.0, 1.0
clip = bpy.data.movieclips.load(video)
w, h, n = clip.size[0], clip.size[1], clip.frame_duration
sc.render.fps = 24
sc.frame_start, sc.frame_end = 1, n
r = sc.render
r.resolution_x, r.resolution_y, r.resolution_percentage = w, h, 100

ed = sc.sequence_editor_create()
ed.strips.new_movie("Video", video, 1, 1)
ed.strips.new_sound("Audio", audio, 2, 1)

im = r.image_settings
im.media_type = "VIDEO"
im.file_format = "FFMPEG"
r.ffmpeg.format, r.ffmpeg.codec, r.ffmpeg.constant_rate_factor = "MPEG4", "H264", "HIGH"
r.ffmpeg.audio_codec, r.ffmpeg.audio_bitrate = "AAC", 192
r.ffmpeg.audio_channels, r.ffmpeg.audio_mixrate = "STEREO", 48000
r.filepath = out
bpy.ops.render.render(animation=True)
print("MUXED", out, f"{w}x{h}", n, "frames")
