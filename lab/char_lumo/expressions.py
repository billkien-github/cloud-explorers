"""
Bảng biểu cảm + đoạn thử chuyển cảm xúc cho Lumo.
    blender -b lumo.blend -P expressions.py
      -> renders/expression_sheet.png  (9 biểu cảm, cận mặt)
      -> lumo_faces.blend               (đoạn 9 giây chuyển qua 9 biểu cảm, có chớp mắt) -> render bằng pipeline/render.py
Mỗi biểu cảm = các thuộc tính face rig (xem face_rig.py) + tư thế đầu, tai, ngực.
"""
import math
import os
import unicodedata

import bpy
import numpy as np
from mathutils import Quaternion, Vector

HERE = os.path.dirname(bpy.data.filepath)
OUT = os.path.join(HERE, "renders")
scene = bpy.context.scene
rig = bpy.data.objects["RIG-Lumo"]
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def both(prefix, v):
    return {f"{prefix}_L": v, f"{prefix}_R": v}


EXPRESSIONS = [  # (tên, thuộc tính mặt, tư thế {xương: [(trục, độ)]})
    ("Bình thường", {}, {}),
    ("Tò mò", {**both("eye_open", 1.12), "pupil": 1.2, "brow_raise_L": 0.9, "brow_raise_R": 0.3, "mouth_open": 0.3,
               "look_z": 0.3},
     {"head": [(Y, 14)], "ear.L": [(X, 12)], "ear.R": [(X, 12)]}),
    ("Bất ngờ", {**both("eye_open", 1.25), "pupil": 0.7, **both("brow_raise", 1.0), "mouth_open": 1.0},
     {"ear.L": [(Y, 10)], "ear.R": [(Y, -10)], "head": [(X, -10)]}),
    ("Phấn khích", {**both("eye_open", 1.1), **both("lower_lid", 0.35), "pupil": 1.25, **both("brow_raise", 0.8),
                    "mouth_grin": 1.0, "blush": 0.5},
     {"ear.L": [(Y, -8)], "ear.R": [(Y, 8)], "head": [(X, -8)]}),
    ("Bối rối", {"eye_open_L": 1.0, "eye_open_R": 0.85, "brow_raise_L": 0.9, "brow_raise_R": -0.5, "brow_tilt_R": 0.4,
                 "mouth_wavy": 1.0, "look_x": 0.5, "look_z": 0.4},
     {"head": [(Y, -16)], "ear.L": [(Y, 25)], "ear.R": [(X, -15)]}),
    ("Ngượng ngùng", {**both("eye_open", 0.75), **both("lower_lid", 0.55), **both("lid_tilt", -0.4),
                      **both("brow_raise", 0.4), **both("brow_tilt", -0.7), "mouth_wavy": 0.6, "mouth_smile": 0.4,
                      "blush": 1.0, "sweat": 1.0, "look_x": -0.6, "look_z": -0.5},
     {"head": [(X, 10), (Z, -12)], "ear.L": [(Y, 35), (X, -20)], "ear.R": [(Y, -35), (X, -20)]}),
    ("Buồn", {**both("eye_open", 0.72), **both("lid_tilt", -0.9), "pupil": 1.25, **both("brow_raise", 0.35),
              **both("brow_tilt", -1.0), "mouth_frown": 1.0, "look_z": -0.3},
     {"head": [(X, 14)], "ear.L": [(Y, 55), (X, -10)], "ear.001.L": [(Y, 15)],
      "ear.R": [(Y, -55), (X, -10)], "ear.001.R": [(Y, -15)]}),
    ("Quyết tâm", {**both("eye_open", 0.78), **both("lid_tilt", 0.6), **both("brow_raise", -0.5),
                   **both("brow_tilt", 0.9), "mouth_flat": 1.0, "mouth_frown": 0.15},
     {"head": [(X, 8)], "ear.L": [(X, -25)], "ear.R": [(X, -25)], "chest": [(X, 6)]}),
    ("Vui", {**both("eye_open", 0.95), **both("lower_lid", 0.75), **both("brow_raise", 0.45), "mouth_smile": 1.0,
             "blush": 0.55},
     {"head": [(Y, 6)], "ear.L": [(Y, -6)], "ear.R": [(Y, 6)]}),
]
FACE_PROPS = [k for k in rig.keys() if not k.startswith("_") and isinstance(rig[k], float)]
DEFAULTS = {k: rig.id_properties_ui(k).as_dict()["default"] for k in FACE_PROPS}
POSE_BONES = sorted({b for _, _, pose in EXPRESSIONS for b in pose})


def no_accents(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def apply(face, pose, frame=None):
    for k in FACE_PROPS:
        rig[k] = face.get(k, DEFAULTS[k])
        if frame is not None:
            rig.keyframe_insert(f'["{k}"]', frame=frame)
    for name in POSE_BONES:
        pb = rig.pose.bones[name]
        pb.rotation_mode = "QUATERNION"
        inv = pb.bone.matrix_local.to_3x3().inverted()
        q = Quaternion()
        for axis, deg in pose.get(name, []):
            q = Quaternion(inv @ Vector(axis), math.radians(deg)) @ q
        pb.rotation_quaternion = q
        if frame is not None:
            pb.keyframe_insert("rotation_quaternion", frame=frame)


# ---------------------------------------------------------------- ánh sáng, nền
sd = bpy.data.lights.new("Key", "SUN")
sd.energy, sd.angle = 3.0, math.radians(12)
key = bpy.data.objects.new("Key", sd)
scene.collection.objects.link(key)
key.rotation_euler = Vector((0.35, 0.7, -0.6)).to_track_quat("-Z", "Y").to_euler()
w = bpy.data.worlds.new("W")
scene.world = w
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.86, 0.88, 0.93, 1)
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.1
scene.render.engine = "BLENDER_EEVEE"
scene.view_settings.view_transform = "AgX"
scene.eevee.taa_render_samples = 16


def camera(name, loc, aim, lens):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    o = bpy.data.objects.new(name, cd)
    scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return o


def label(text):
    cu = bpy.data.curves.new("L_" + text, "FONT")
    cu.body, cu.size, cu.align_x = no_accents(text), 0.022, "CENTER"
    m = bpy.data.materials.new("Lbl")
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.05, 0.08, 1)
    cu.materials.append(m)
    o = bpy.data.objects.new("L_" + text, cu)
    scene.collection.objects.link(o)
    o.rotation_euler = (math.radians(90), 0, 0)
    return o


# ---------------------------------------------------------------- 1) bảng biểu cảm 3x3
face_cam = camera("CamFace", (0.14, -0.85, 0.34), (0, 0, 0.35), 70)
scene.camera = face_cam
r = scene.render
r.resolution_x = r.resolution_y = 520
r.resolution_percentage = 100
r.image_settings.media_type = "IMAGE"
r.image_settings.file_format = "PNG"
tiles = []
for i, (name, face, pose) in enumerate(EXPRESSIONS):
    apply(face, pose)
    lb = label(name)
    lb.location = (0.0, -0.2, 0.232)
    bpy.context.view_layer.update()
    r.filepath = os.path.join(OUT, f"expr_{i:02d}.png")
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(lb)
    tiles.append(r.filepath)
S, COLS = 520, 3
rows = math.ceil(len(tiles) / COLS)
sheet = np.ones((rows * S, COLS * S, 4), np.float32)
for i, path in enumerate(tiles):
    img = bpy.data.images.load(path)
    px = np.array(img.pixels[:], np.float32).reshape(S, S, 4)
    rr, cc = i // COLS, i % COLS
    sheet[(rows - 1 - rr) * S:(rows - rr) * S, cc * S:(cc + 1) * S] = px
    bpy.data.images.remove(img)
out = bpy.data.images.new("expr_sheet", COLS * S, rows * S, alpha=True)
out.pixels = sheet.ravel()
out.filepath_raw = os.path.join(OUT, "expression_sheet.png")
out.file_format = "PNG"
out.save()
print("SHEET", out.filepath_raw)

# ---------------------------------------------------------------- 2) đoạn chuyển cảm xúc (9 x 24 frame) có chớp mắt
HOLD, EASE = 24, 5
anim_cam = camera("CamAnim", (0.3, -0.78, 0.39), (0, 0, 0.33), 55)
scene.camera = anim_cam
prev = EXPRESSIONS[0]
for i, (name, face, pose) in enumerate(EXPRESSIONS):
    start = 1 + i * HOLD
    if i:
        apply(prev[1], prev[2], start)               # giữ biểu cảm cũ tới đầu đoạn
    apply(face, pose, start + (EASE if i else 0))    # chuyển sang biểu cảm mới trong 5 frame
    apply(face, pose, start + HOLD - 1)
    lb = label(name)
    lb.location = (0.0, -0.32, 0.12)
    for f, hide in ((1, True), (start, False), (start + HOLD, True)):
        lb.hide_render = hide
        lb.keyframe_insert("hide_render", frame=max(1, f))
    if name not in ("Bất ngờ", "Ngượng ngùng", "Vui"):   # chớp mắt giữa đoạn giữ
        b = start + 14
        for side in "LR":
            k = f"eye_open_{side}"
            v = face.get(k, DEFAULTS[k])
            for f, val in ((b, v), (b + 2, 0.02), (b + 4, v)):
                rig[k] = val
                rig.keyframe_insert(f'["{k}"]', frame=f)
    prev = (name, face, pose)
scene.frame_start, scene.frame_end = 1, len(EXPRESSIONS) * HOLD
r.resolution_x, r.resolution_y = 1920, 1080
r.resolution_percentage = 50
scene.render.fps = 24
scene["lab_stills"] = "20,40,64,88,112"
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "lumo_faces.blend"))
print("SAVED lumo_faces.blend", scene.frame_end, "frames")
