"""
Render bảng xem trước (contact sheet) cho một thư mục model.
    blender -b --factory-startup -P make_previews.py -- <thư mục model> <ảnh output.png> [số cột]
Nhận .gltf/.glb/.fbx, mỗi model được co về cùng một ô, có nhãn tên bên dưới.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
src, out = argv[0], argv[1]
cols = int(argv[2]) if len(argv) > 2 else 8
CELL, LABEL = 2.0, 0.16

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

files = []
for r, _, fs in os.walk(src):
    for f in sorted(fs):
        if f.lower().endswith((".gltf", ".glb", ".fbx")):
            files.append(os.path.join(r, f))
files.sort(key=lambda p: os.path.basename(p).lower())

text_mat = bpy.data.materials.new("Label")
text_mat.diffuse_color = (0.1, 0.1, 0.12, 1)
tb = text_mat.node_tree.nodes["Principled BSDF"]
tb.inputs["Base Color"].default_value = (0.05, 0.05, 0.06, 1)

for i, path in enumerate(files):
    before = set(bpy.data.objects)
    try:
        if path.lower().endswith(".fbx"):
            bpy.ops.import_scene.fbx(filepath=path)
        else:
            bpy.ops.import_scene.gltf(filepath=path)
    except Exception as e:
        print("SKIP", path, e)
        continue
    new = [o for o in bpy.data.objects if o not in before]
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    pts = []
    for o in new:
        if o.type == "MESH":
            ev = o.evaluated_get(dg)
            pts += [ev.matrix_world @ Vector(c) for c in ev.bound_box]
    if not pts:
        continue
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    size = max((hi - lo).x, (hi - lo).z, 1e-4)
    s = CELL * 0.8 / size
    grp = bpy.data.objects.new(f"G{i}", None)
    scene.collection.objects.link(grp)
    for o in new:
        if o.parent is None:
            o.parent = grp
    col, row = i % cols, i // cols
    base = Vector((col * CELL, 0, -row * (CELL + 0.4)))
    center = Vector(((lo.x + hi.x) / 2, (lo.y + hi.y) / 2, lo.z))
    grp.scale = (s, s, s)
    grp.location = base - center * s
    cu = bpy.data.curves.new(f"T{i}", "FONT")
    cu.body = os.path.splitext(os.path.basename(path))[0][:22]
    cu.size, cu.align_x = LABEL, "CENTER"
    cu.materials.append(text_mat)
    t = bpy.data.objects.new(f"T{i}", cu)
    scene.collection.objects.link(t)
    t.location = base + Vector((0, -1.5, -0.3))
    t.rotation_euler = (math.radians(90), 0, 0)

rows = math.ceil(len(files) / cols)
cd = bpy.data.cameras.new("Cam")
cd.type = "ORTHO"
w, h = cols * CELL, rows * (CELL + 0.4)
cd.ortho_scale = max(w, h * 16 / 9) + 0.6
cam = bpy.data.objects.new("Cam", cd)
scene.collection.objects.link(cam)
cam.location = ((cols - 1) * CELL / 2, -40, -(rows - 1) * (CELL + 0.4) / 2 + CELL * 0.35 + 4.0)
cam.rotation_euler = (math.radians(84), 0, 0)
scene.camera = cam

sd = bpy.data.lights.new("Sun", "SUN")
sd.energy, sd.angle = 3.0, math.radians(8)
sun = bpy.data.objects.new("Sun", sd)
scene.collection.objects.link(sun)
sun.rotation_euler = (math.radians(50), 0, math.radians(-30))
world = bpy.data.worlds.new("W")
scene.world = world
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.92, 0.92, 0.94, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9

r = scene.render
r.engine = "BLENDER_EEVEE"
r.resolution_x = 1920
r.resolution_y = max(540, int(1920 * h / w * 1.02))
r.resolution_percentage = 100
scene.eevee.taa_render_samples = 16
scene.view_settings.view_transform = "Standard"
cd.ortho_scale = w + 0.6 if r.resolution_y >= 1920 * h / w else (h + 0.6) * r.resolution_x / r.resolution_y
r.filepath = out
bpy.ops.render.render(write_still=True)
print("PREVIEW", out, len(files), "models")
