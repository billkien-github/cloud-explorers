"""
Vòng đi bộ cho Lumo (rig Rigify), dựng hoàn toàn bằng code.
    blender -b lumo.blend -P walk_cycle.py        -> lumo_walk.blend (rồi render bằng pipeline/render.py)
Một vòng = 18 frame (2 bước, kiểu bước lũn cũn của sinh vật chân ngắn). Video gồm 3 đoạn:
  1-72    đi tại chỗ, góc nghiêng      (xem dáng chân, nhún người)
  73-144  đi tại chỗ, góc 3/4 trước    (xem lắc hông, vung tay, tai, đuôi)
  145-264 đi thật trên sàn ô vuông     (xem chân có bị trượt không)
"""
import math
import os

import bmesh
import bpy
import numpy as np
from mathutils import Quaternion, Vector

HERE = os.path.dirname(bpy.data.filepath)
scene = bpy.context.scene
rig = bpy.data.objects["RIG-Lumo"]
body = bpy.data.objects["LumoBody"]
CYCLE, STEP = 18, 9
STRIDE = 0.06                       # bàn chân đi từ -0.03 (trước) tới +0.03 (sau) trong một bước
SPEED = STRIDE / STEP               # m/frame khi đi thật -> chân chạm đất đứng yên so với sàn
TRAVEL0, END = 145, 264
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def smooth(s):
    return s * s * (3 - 2 * s)


def foot(t):
    """Một bàn chân theo pha t (0..18): (dịch y, nâng z, gập mũi chân quanh X theo độ)."""
    t %= CYCLE
    if t < STEP:                                   # chạm đất: trượt đều về sau (đất đứng yên khi đi thật)
        y = -STRIDE / 2 + STRIDE * t / STEP
        rot = np.interp(t, [0, 2, 7, 9], [-12, 0, 0, 20])   # gót chạm -> bàn phẳng -> nhón gót đẩy
        return y, 0.0, rot
    s = (t - STEP) / STEP                          # nhấc chân đưa ra trước
    y = STRIDE / 2 - STRIDE * smooth(s)
    z = 0.024 * math.sin(math.pi * s)
    return y, z, 20 - 32 * s


def wave(t, period, delay, amp):
    return amp * math.sin(2 * math.pi * (t - delay) / period)


def pose_at(t):
    """Trạng thái toàn thân tại pha t. {xương: (dịch theo trục thế giới, [(trục, độ)])}."""
    c = math.cos(2 * math.pi * t / CYCLE)
    bob = -0.004 - 0.005 * math.cos(2 * math.pi * (t - 1) / STEP)     # thấp nhất ngay sau khi chạm đất
    sway = 0.006 * math.sin(math.pi * (t % CYCLE) / STEP) * (1 if (t % CYCLE) < STEP else -1)
    p = {}
    for side, phase in (("L", 0), ("R", STEP)):
        y, z, rot = foot(t + phase)
        p[f"foot_ik.{side}"] = ((0, y, z), [(X, rot)])
    p["torso"] = ((sway, 0, bob), [(Z, 5 * c)])
    p["chest"] = ((0, 0, 0), [(X, 4), (Z, -7 * c)])
    p["head"] = ((0, 0, 0), [(Z, 3 * c), (X, wave(t, STEP, 2, 3))])
    p["hand_ik.L"] = ((0, 0.022 * c, 0.004 * (1 - c)), [])
    p["hand_ik.R"] = ((0, -0.022 * c, 0.004 * (1 + c)), [])
    # chuyển động thứ cấp: tai nảy theo nhịp nhún nhưng trễ dần từ gốc ra chóp
    for side, sgn in (("L", 1), ("R", -1)):
        for k, name in enumerate((f"ear.{side}", f"ear.001.{side}", f"ear.002.{side}")):
            p[name] = ((0, 0, 0), [(X, wave(t, STEP, 3 + 2 * k, 7 - k)), (Y, sgn * wave(t, CYCLE, 2 + 2 * k, 3))])
    # đuôi vẫy ngang như sóng, mỗi đốt trễ 2 frame
    for k, name in enumerate(["tail"] + [f"tail.{i:03d}" for i in range(1, 5)]):
        p[name] = ((0, 0, 0), [(Z, wave(t, CYCLE, 2 * k, 9)), (X, wave(t, STEP, 2 + k, 3))])
    return p


def key_pose(frame, pose):
    for name, (loc, rots) in pose.items():
        pb = rig.pose.bones[name]
        pb.rotation_mode = "QUATERNION"
        inv = pb.bone.matrix_local.to_3x3().inverted()
        pb.location = inv @ Vector(loc)
        q = Quaternion()
        for axis, deg in rots:
            q = Quaternion(inv @ Vector(axis), math.radians(deg)) @ q
        pb.rotation_quaternion = q
        pb.keyframe_insert("location", frame=frame)
        pb.keyframe_insert("rotation_quaternion", frame=frame)


def channel_fcurves(id_data):
    ad = id_data.animation_data
    if hasattr(ad.action, "fcurves"):
        return ad.action.fcurves
    from bpy_extras import anim_utils
    return anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves


# ---------------------------------------------------------------- hoạt hình
for t in range(CYCLE + 1):                         # lấy mẫu mỗi frame của một vòng, rồi cho lặp vô hạn
    key_pose(1 + t, pose_at(t))
for fc in channel_fcurves(rig):
    fc.modifiers.new("CYCLES")
root = rig.pose.bones["root"]
root.location = (0, 0, 0)
root.keyframe_insert("location", frame=1)
root.keyframe_insert("location", frame=TRAVEL0)
root.location = root.bone.matrix_local.to_3x3().inverted() @ Vector((0, -SPEED * (END - TRAVEL0), 0))
root.keyframe_insert("location", frame=END)
for fc in channel_fcurves(rig):
    if fc.data_path == 'pose.bones["root"].location':
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"

# ---------------------------------------------------------------- sàn ô vuông, đèn, camera
bpy.ops.mesh.primitive_plane_add(size=6, location=(0, -1.0, 0))
floor = bpy.context.active_object
fm = bpy.data.materials.new("Checker")
N, L = fm.node_tree.nodes, fm.node_tree.links
ck = N.new("ShaderNodeTexChecker")
ck.inputs["Scale"].default_value = 60                  # ô 10cm trên sàn 6m
ck.inputs["Color1"].default_value = (0.78, 0.8, 0.84, 1)
ck.inputs["Color2"].default_value = (0.62, 0.65, 0.7, 1)
L.new(ck.outputs["Color"], N["Principled BSDF"].inputs["Base Color"])
N["Principled BSDF"].inputs["Roughness"].default_value = 0.8
floor.data.materials.append(fm)

sd = bpy.data.lights.new("Key", "SUN")
sd.energy, sd.angle = 3.2, math.radians(8)
key = bpy.data.objects.new("Key", sd)
scene.collection.objects.link(key)
key.rotation_euler = Vector((0.4, 0.6, -0.75)).to_track_quat("-Z", "Y").to_euler()
w = bpy.data.worlds.new("W")
scene.world = w
w.node_tree.nodes["Background"].inputs["Color"].default_value = (0.84, 0.87, 0.92, 1)


def cam(name, loc, aim, lens, frame):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    o = bpy.data.objects.new(name, cd)
    scene.collection.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(aim) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    scene.timeline_markers.new(name, frame=frame).camera = o
    return o


scene.camera = cam("CamSide", (2.0, -0.02, 0.3), (0, -0.02, 0.28), 50, 1)
cam("CamFront34", (1.15, -1.7, 0.45), (0, 0, 0.28), 50, 73)
cam("CamTravel", (1.55, -0.45, 0.36), (0, -0.45, 0.2), 38, TRAVEL0)

scene.frame_start, scene.frame_end = 1, END
scene.render.fps = 24
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x, scene.render.resolution_y = 1920, 1080
scene.view_settings.view_transform = "AgX"
scene["lab_stills"] = "1,5,10,14,100,150,155,159,164,168"

# ---------------------------------------------------------------- đo trượt chân khi đi thật
me0 = body.data
soles = {s: [v.index for v in me0.vertices if v.co.z < 0.012 and v.co.x * sgn > 0.02]
         for s, sgn in (("L", 1), ("R", -1))}
track = {s: [] for s in soles}
for f in range(TRAVEL0, END + 1):
    scene.frame_set(f)
    dg = bpy.context.evaluated_depsgraph_get()
    ev = body.evaluated_get(dg)
    m = ev.to_mesh()
    co = np.array([ev.matrix_world @ v.co for v in m.vertices])
    ev.to_mesh_clear()
    for s, idx in soles.items():
        track[s].append(co[idx].mean(axis=0))
report = []
for s, pts in track.items():
    pts = np.array(pts)
    phase = STEP if s == "R" else 0
    # bàn chân đặt phẳng trên đất khi pha nằm trong [2, 7] (xem foot()) -> lúc này nó phải đứng yên so với sàn
    ground = np.array([2 <= (f - 1 + phase) % CYCLE <= 7 for f in range(TRAVEL0, END + 1)])
    slides = [np.linalg.norm(pts[i + 1, :2] - pts[i, :2]) for i in range(len(pts) - 1) if ground[i] and ground[i + 1]]
    report.append(f"chân {s}: chạm đất {int(ground.sum())}/{len(pts)} frame, trượt lớn nhất {max(slides) * 1000:.2f} mm/frame, "
                  f"trung bình {np.mean(slides) * 1000:.2f} mm/frame (Lumo đi {SPEED * 1000:.1f} mm/frame)")
scene.frame_set(1)
txt = "\n".join(report)
os.makedirs(os.path.join(HERE, "renders"), exist_ok=True)
open(os.path.join(HERE, "renders", "walk_qa.txt"), "w", encoding="utf-8").write(txt + "\n")
print("WALK_QA\n" + txt)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "lumo_walk.blend"))
print("SAVED lumo_walk.blend")
