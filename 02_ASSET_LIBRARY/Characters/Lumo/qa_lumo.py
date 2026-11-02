"""
Kiểm tra rig Lumo: đặt các tư thế khó, đo độ méo lưới và số đỉnh áo choàng, dây đeo lún vào người, render bảng ảnh.
    blender -b lumo_rig.blend -P qa_lumo.py      -> qa/rig_sheet.png + qa/rig_qa.txt
Mỗi ô của bảng: chính diện chếch 30° | nhìn ngang, theo thứ tự trong POSES (trái sang phải, trên xuống dưới).
"""
import math
import pathlib
import sys

import bmesh
import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = pathlib.Path(bpy.data.filepath).parent
STUDIO = HERE.parents[2]
sys.path.insert(0, str(STUDIO / "pipeline"))
from rig_qa import apply_pose, distortion, mesh_stats, reset_pose  # noqa: E402

OUT = HERE / "qa"
OUT.mkdir(exist_ok=True)
P = "mixamorig:"
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)      # Lumo nhìn về -Y: xoay quanh +X là cúi về trước

POSES = [
    ("Nghi", {}),
    ("Gio hai tay", {P + "LeftArm": {"rot": [(Y, -70)]}, P + "RightArm": {"rot": [(Y, 70)]}}),
    ("Ngoi xom", {P + "Hips": {"loc": (0, 0.02, -0.09)}, P + "Spine": {"rot": [(X, 15)]}}),
    ("Cui nguoi", {P + "Spine": {"rot": [(X, 20)]}, P + "Spine1": {"rot": [(X, 20)]}, P + "Neck": {"rot": [(X, -15)]}}),
    ("Ngoai dau", {P + "Spine2": {"rot": [(Z, 25)]}, P + "Neck": {"rot": [(Z, 25)]}, P + "Head": {"rot": [(Z, 30)]}}),
    ("Nhac chan", {"IK_foot.L": {"loc": (0, -0.10, 0.12), "rot": [(X, -30)]}, P + "Hips": {"rot": [(Y, -6)]}}),
    ("Chay", {"IK_foot.L": {"loc": (0, -0.12, 0.08), "rot": [(X, -20)]}, "IK_foot.R": {"loc": (0, 0.10, 0.04), "rot": [(X, 40)]},
              P + "Hips": {"loc": (0, -0.01, -0.03)}, P + "Spine1": {"rot": [(X, 10), (Z, -10)]},
              P + "LeftArm": {"rot": [(Y, -20), (X, 45)]}, P + "RightArm": {"rot": [(Y, 20), (X, -40)]},
              P + "LeftForeArm": {"rot": [(X, 50)]}, P + "RightForeArm": {"rot": [(X, 50)]}}),
    ("Tai cup", {"ear.01.L": {"rot": [(X, 45)]}, "ear.02.L": {"rot": [(X, 30)]},
                 "ear.01.R": {"rot": [(X, 45)]}, "ear.02.R": {"rot": [(X, 30)]}}),
    ("Duoi vay", {**{f"tail.{i:02d}": {"rot": [(Z, 18), (X, -12)]} for i in range(1, 5)}}),
]

scene = bpy.context.scene
rig = bpy.data.objects["RIG-Lumo"]
body = bpy.data.objects["LumoBody"]
OUTFIT = [bpy.data.objects[n] for n in ("LumoCape", "LumoStrap")]
rig.hide_render = True

sun = bpy.data.objects.new("QA_Sun", bpy.data.lights.new("QA_Sun", "SUN"))
scene.collection.objects.link(sun)
sun.data.energy, sun.rotation_euler = 3.0, (math.radians(50), 0, math.radians(25))
world = bpy.data.worlds.new("QA_World")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
cam = bpy.data.objects.new("QA_Cam", bpy.data.cameras.new("QA_Cam"))
scene.collection.objects.link(cam)
scene.camera = cam
cam.data.type, cam.data.ortho_scale = "ORTHO", 1.35
r = scene.render
r.engine, r.resolution_x, r.resolution_y = "BLENDER_EEVEE", 300, 360
r.image_settings.file_format = "PNG"
scene.view_settings.view_transform = "Standard"
CENTER = Vector((0, 0, 0.56))
VIEWS = [math.radians(-30), math.radians(90)]


def evaluated_points(obj):
    ev = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
    me = ev.to_mesh()
    pts = [obj.matrix_world @ v.co for v in me.vertices]
    ev.to_mesh_clear()
    return pts


def sunk(obj):
    """Số đỉnh của obj nằm bên trong thân (tư thế hiện tại)."""
    ev = body.evaluated_get(bpy.context.evaluated_depsgraph_get())
    bm = bmesh.new()
    bm.from_mesh(ev.to_mesh())
    bm.transform(body.matrix_world)
    ev.to_mesh_clear()
    bvh = BVHTree.FromBMesh(bm)
    bm.free()
    n = 0
    for p in evaluated_points(obj):
        loc, nrm, _, _ = bvh.find_nearest(p, 0.05)
        n += loc is not None and (p - loc).dot(nrm) < -0.002
    return n


def shot(yaw):
    cam.location = CENTER + Vector((math.sin(yaw) * 5, -math.cos(yaw) * 5, 0.25))
    cam.rotation_euler = (math.radians(87), 0, yaw)
    path = str(OUT / "_tmp.png")
    r.filepath = path
    bpy.ops.render.render(write_still=True)
    img = bpy.data.images.load(path)
    px = np.array(img.pixels[:], dtype=np.float32).reshape(img.size[1], img.size[0], 4)
    bpy.data.images.remove(img)
    return px


reset_pose(rig)
bpy.context.view_layer.update()
rest = mesh_stats(body)
rows, tiles = [], []
for name, pose in POSES:
    apply_pose(rig, pose)
    bpy.context.view_layer.update()
    rows.append((name, *distortion(rest, body), *(sunk(o) for o in OUTFIT)))
    tiles.append(np.concatenate([shot(v) for v in VIEWS], axis=1))
reset_pose(rig)

cols = 3
h, w = tiles[0].shape[:2]
nrows = (len(tiles) + cols - 1) // cols
sheet = np.ones((nrows * h, cols * w, 4), np.float32)
for i, t in enumerate(tiles):
    rr, cc = i // cols, i % cols
    sheet[(nrows - 1 - rr) * h:(nrows - rr) * h, cc * w:(cc + 1) * w] = t
img = bpy.data.images.new("sheet", cols * w, nrows * h, alpha=True)
img.pixels = sheet.ravel()
img.filepath_raw, img.file_format = str(OUT / "rig_sheet.png"), "PNG"
img.save()
(OUT / "_tmp.png").unlink()

lines = [f"{'Tư thế':14s} {'bad%':>6s} {'vol':>6s} {'amin':>6s} {'amax':>6s} {'áo lún':>7s} {'dây lún':>7s}"]
lines += [f"{n:14s} {b:6.2f} {v:6.3f} {a0:6.2f} {a1:6.2f} {c:7d} {s:7d}" for n, b, v, a0, a1, c, s in rows]
lines.append(f"(áo choàng {len(OUTFIT[0].data.vertices)} đỉnh, dây đeo {len(OUTFIT[1].data.vertices)} đỉnh)")
(OUT / "rig_qa.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
