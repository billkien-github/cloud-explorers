"""
Bài kiểm tra rig: đặt Lumo vào các tư thế khó, render 2 góc mỗi tư thế, đo độ méo lưới.
    blender -b lumo.blend -P pose_test.py      -> renders/pose_sheet.png + renders/pose_qa.txt
Chỉ số (so với tư thế nghỉ):
  bad%   = % mặt lưới bị bóp (< 40% diện tích) hoặc kéo giãn (> 250%)
  vol    = thể tích sau / trước (lý tưởng ~1.0; thấp = bị xẹp)
  amin/amax = mặt bị bóp/giãn nhiều nhất
"""
import math
import os
import unicodedata

import sys

import bpy
import numpy as np
from mathutils import Vector

HERE = os.path.dirname(bpy.data.filepath)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "pipeline", "rigging"))
from rig_qa import apply_pose, distortion, mesh_stats, reset_pose  # noqa: E402
OUT = os.path.join(HERE, "renders")
os.makedirs(OUT, exist_ok=True)
scene = bpy.context.scene
rig = bpy.data.objects["RIG-Lumo"]
meshes = [bpy.data.objects["LumoBody"], bpy.data.objects["LumoTail"]]
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)
EARS = ["ear.L", "ear.001.L", "ear.002.L", "ear.R", "ear.001.R", "ear.002.R"]
TAILS = ["tail"] + [f"tail.{i:03d}" for i in range(1, 5)]

# tư thế: tên -> {xương: {"loc": dịch chuyển theo trục thế giới (m), "rot": [(trục thế giới, độ), ...]}}
POSES = [
    ("01 Nghỉ", {}),
    ("02 Ngồi xổm", {"torso": {"loc": (0, 0, -0.035)}}),
    ("03 Bật nhảy", {"torso": {"loc": (0, 0, 0.03)}, "foot_ik.L": {"loc": (0, 0, 0.03), "rot": [(X, -30)]},
                     "foot_ik.R": {"loc": (0, 0, 0.03), "rot": [(X, -30)]},
                     "hand_ik.L": {"loc": (0.03, 0, 0.13)}, "hand_ik.R": {"loc": (-0.03, 0, 0.13)}}),
    ("04 Cúi người", {"chest": {"rot": [(X, 30)]}, "head": {"rot": [(X, 10)]}}),
    ("05 Ngửa người", {"chest": {"rot": [(X, -25)]}, "head": {"rot": [(X, -15)]}}),
    ("06 Quay đầu", {"head": {"rot": [(Z, 45), (Y, 15)]}}),
    ("07 Gật đầu", {"head": {"rot": [(X, 30)]}}),
    ("08 Giơ hai tay", {"hand_ik.L": {"loc": (0.02, -0.01, 0.14)}, "hand_ik.R": {"loc": (-0.02, -0.01, 0.14)}}),
    ("09 Vẫy tay", {"hand_ik.L": {"loc": (0.03, -0.02, 0.15)}}),
    ("10 Tai cụp (buồn)", {"ear.L": {"rot": [(Y, 55), (X, -15)]}, "ear.001.L": {"rot": [(Y, 20)]},
                           "ear.R": {"rot": [(Y, -55), (X, -15)]}, "ear.001.R": {"rot": [(Y, -20)]}}),
    ("11 Tai xoay nghe ngóng", {"ear.L": {"rot": [(Z, 45)]}, "ear.001.L": {"rot": [(X, 15)]},
                                "ear.R": {"rot": [(Z, -45)]}, "ear.001.R": {"rot": [(X, 15)]}}),
    ("12 Đuôi cuộn", {t: {"rot": [(X, 25)]} for t in TAILS}),
    ("13 Đuôi vẫy ngang", {t: {"rot": [(Z, 18), (Y, 10)]} for t in TAILS}),
    ("14 Chạy", {"foot_ik.L": {"loc": (0, -0.04, 0.035), "rot": [(X, 20)]}, "foot_ik.R": {"loc": (0, 0.035, 0)},
                 "torso": {"loc": (0, 0, -0.008)}, "chest": {"rot": [(Z, 15)]},
                 "hand_ik.L": {"loc": (0, 0.04, 0.0)}, "hand_ik.R": {"loc": (0, -0.04, 0.02)}}),
    ("15 Bẹp mạnh", {"torso": {"loc": (0, 0, -0.05)}, "hand_ik.L": {"loc": (0.01, 0, -0.03)},
                     "hand_ik.R": {"loc": (-0.01, 0, -0.03)}}),
    ("16 Ngoái đầu", {"head": {"rot": [(Z, -60), (X, 20)]}, "neck": {"rot": [(Z, -15)]}}),
]


def no_accents(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------- cảnh chụp
def camera(name, loc, aim, lens):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cam = bpy.data.objects.new(name, cd)
    scene.collection.objects.link(cam)
    cam.location = loc
    d = Vector(aim) - Vector(loc)
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    return cam


cams = [camera("CamFront", (0.72, -1.28, 0.42), (0, 0, 0.285), 62),
        camera("CamSide", (1.48, 0.06, 0.34), (0, 0.06, 0.285), 62)]
sd = bpy.data.lights.new("Key", "SUN")
sd.energy, sd.angle = 3.2, math.radians(10)
key = bpy.data.objects.new("Key", sd)
scene.collection.objects.link(key)
key.rotation_euler = Vector((0.4, 0.6, -0.7)).to_track_quat("-Z", "Y").to_euler()
w = bpy.data.worlds.new("W")
scene.world = w
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.82, 0.84, 0.88, 1)
bpy.ops.mesh.primitive_plane_add(size=4)
floor = bpy.context.active_object
fm = bpy.data.materials.new("Floor")
fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.7, 0.72, 0.75, 1)
floor.data.materials.append(fm)
cu = bpy.data.curves.new("Label", "FONT")
cu.size = 0.045
label = bpy.data.objects.new("Label", cu)
scene.collection.objects.link(label)
tm = bpy.data.materials.new("LabelMat")
tm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.05, 0.08, 1)
cu.materials.append(tm)

r = scene.render
r.engine = "BLENDER_EEVEE"
r.resolution_x = r.resolution_y = 380
r.resolution_percentage = 100
scene.eevee.taa_render_samples = 16
scene.view_settings.view_transform = "AgX"
r.image_settings.file_format = "PNG"

# ---------------------------------------------------------------- chạy bài kiểm tra
reset_pose(rig)
rest = {o.name: mesh_stats(o) for o in meshes}
rows, tiles = [], []
for idx, (name, pose) in enumerate(POSES):
    apply_pose(rig, pose)
    bpy.context.view_layer.update()
    worst = []
    for o in meshes:
        worst.append((o.name.replace("Lumo", ""), *distortion(rest[o.name], o)))
    rows.append((name, worst))
    pair = []
    for cam in cams:
        scene.camera = cam
        label.hide_render = cam.name != "CamFront"
        cu.body = no_accents(name)      # font mặc định của Blender thiếu dấu tiếng Việt
        label.location = (-0.33, -0.25, 0.0)
        label.rotation_euler = (math.radians(90), 0, math.radians(30))
        r.filepath = os.path.join(OUT, f"pose_{idx:02d}_{cam.name}.png")
        bpy.ops.render.render(write_still=True)
        pair.append(r.filepath)
    tiles.append(pair)

# ghép bảng ảnh: 4 cột x 4 hàng, mỗi ô = góc 3/4 + góc nghiêng
S, COLS = 380, 4
rows_n = math.ceil(len(tiles) / COLS)
sheet = np.ones((rows_n * S, COLS * 2 * S, 4), dtype=np.float32)
for i, pair in enumerate(tiles):
    rr, cc = i // COLS, i % COLS
    for j, path in enumerate(pair):
        img = bpy.data.images.load(path)
        px = np.array(img.pixels[:], dtype=np.float32).reshape(S, S, 4)
        y0 = (rows_n - 1 - rr) * S
        x0 = (cc * 2 + j) * S
        sheet[y0:y0 + S, x0:x0 + S] = px
        bpy.data.images.remove(img)
out_img = bpy.data.images.new("pose_sheet", sheet.shape[1], sheet.shape[0], alpha=True)
out_img.pixels = sheet.ravel()
out_img.filepath_raw = os.path.join(OUT, "pose_sheet.png")
out_img.file_format = "PNG"
out_img.save()

lines = [f"{'Tư thế':24s} | " + " | ".join(f"{p:5s} bad%  vol   amin  amax" for p in ("Body", "Tail"))]
for name, worst in rows:
    lines.append(f"{name:24s} | " + " | ".join(f"{b:5.1f}% {v:5.2f} {mn:5.2f} {mx:5.2f}" for _, b, v, mn, mx in worst))
txt = "\n".join(lines)
open(os.path.join(OUT, "pose_qa.txt"), "w", encoding="utf-8").write(txt + "\n")
print("QA\n" + txt)
print("SHEET", os.path.join(OUT, "pose_sheet.png"))
