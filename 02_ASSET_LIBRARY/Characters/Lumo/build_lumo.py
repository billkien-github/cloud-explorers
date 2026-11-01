"""
Lumo bản Meshy -> lumo_rig.blend (dùng trong shot)
    blender -b --factory-startup -P build_lumo.py
1. Import FBX trong source/, bỏ animation đi kèm, đưa armature và mesh về tỉ lệ 1, trục Z lên, nhìn về -Y.
2. Texture 4K -> 2K.
3. Thêm xương: root (gốc ở mặt đất), 2 chuỗi tai, 1 chuỗi đuôi; gán lại trọng số da cho tai và đuôi
   (Meshy gắn đuôi vào xương đùi phải).
4. Chân điều khiển bằng IK: IK_foot.L/R kéo cả chân và quyết định hướng bàn chân, pole_knee.L/R định hướng đầu gối.
"""
import math
import pathlib

import bpy
import numpy as np
from mathutils import Vector

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "source" / "lumo_meshy_v01" / "Meshy_AI_Lumo_APose_V2_Rigged_biped_Animation_Forward_Roll_and_Fire_withSkin.fbx"
OUT_BLEND = HERE / "lumo_rig.blend"
TEX_SIZE = 2048
P = "mixamorig:"

# ---------------------------------------------------------------- số đo trên mesh (mét, Lumo nhìn về -Y)
TAIL_BASE, TAIL_TIP, TAIL_BONES = Vector((0, 0.07, 0.262)), Vector((0, 0.36, 0.30)), 4
EAR_HINGE, EAR_TIP = Vector((0.15, -0.07, 0.88)), Vector((0.284, -0.078, 1.091))   # tai trái (x > 0)
HEAD_CENTER = np.array((0.0, -0.10, 0.80))     # tai = phần ngoài khối đầu (bán kính ~0.24), cao hơn má, sau trán


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def activate(obj):
    if bpy.context.object and bpy.context.object.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


# ---------------------------------------------------------------- 1. import, chuẩn hoá tỉ lệ
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=str(SOURCE))
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
body = next(o for o in bpy.data.objects if o.type == "MESH")
arm.name, arm.data.name, body.name = "RIG-Lumo", "RIG-Lumo", "LumoBody"
for o in (arm, body):
    o.animation_data_clear()
for act in list(bpy.data.actions):
    bpy.data.actions.remove(act)
for pb in arm.pose.bones:
    pb.location, pb.rotation_quaternion, pb.scale = (0, 0, 0), (1, 0, 0, 0), (1, 1, 1)

rest_before = np.array([body.matrix_world @ v.co for v in body.data.vertices])
mw = body.matrix_world.copy()
body.parent = None
body.matrix_world = mw
for o in (arm, body):                       # FBX của Meshy: armature scale 0.01 + xoay 90°, mesh scale 100
    activate(o)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
body.parent = arm
moved = np.abs(np.array([v.co[:] for v in body.data.vertices]) - rest_before).max()
assert moved < 1e-4, f"mesh lệch sau khi chuẩn hoá: {moved}"

# ---------------------------------------------------------------- 2. texture 2K
for img in bpy.data.images:
    if img.size[0] > TEX_SIZE:
        img.scale(TEX_SIZE, TEX_SIZE)
        img.pack()

# ---------------------------------------------------------------- 3. xương mới
activate(arm)
bpy.ops.object.mode_set(mode="EDIT")
eb = arm.data.edit_bones


def new_bone(name, head, tail, parent=None, deform=True, roll=0.0, connect=False):
    b = eb.new(name)
    b.head, b.tail, b.roll = head, tail, roll
    b.parent = eb[parent] if parent else None
    b.use_connect = connect
    b.use_deform = deform
    return b


new_bone("root", (0, 0, 0), (0, 0.25, 0), deform=False)
eb[P + "Hips"].parent = eb["root"]
for i in range(TAIL_BONES):
    a, b = TAIL_BASE.lerp(TAIL_TIP, i / TAIL_BONES), TAIL_BASE.lerp(TAIL_TIP, (i + 1) / TAIL_BONES)
    new_bone(f"tail.{i + 1:02d}", a, b, P + "Hips" if i == 0 else f"tail.{i:02d}", connect=i > 0)
for side, s, full in (("L", 1, "Left"), ("R", -1, "Right")):
    hinge, tip = Vector((s * EAR_HINGE.x, EAR_HINGE.y, EAR_HINGE.z)), Vector((s * EAR_TIP.x, EAR_TIP.y, EAR_TIP.z))
    mid = hinge.lerp(tip, 0.5)
    new_bone(f"ear.01.{side}", hinge, mid, P + "Head")
    new_bone(f"ear.02.{side}", mid, tip, f"ear.01.{side}", connect=True)
    # IK chân: điều khiển trùng hướng với xương bàn chân (để chép thẳng hướng xoay), pole trước đầu gối
    foot = eb[P + full + "Foot"]
    hip, knee = eb[P + full + "UpLeg"].head.copy(), eb[P + full + "Leg"].head.copy()
    d = (foot.head - hip).normalized()
    bend = knee - (hip + d * (knee - hip).dot(d))          # hướng đầu gối gập ra, trong mặt phẳng của chân
    bend = bend.normalized() if bend.length > 1e-3 else Vector((0, -1, 0))
    new_bone(f"IK_foot.{side}", foot.head, foot.tail, "root", deform=False, roll=foot.roll)
    new_bone(f"pole_knee.{side}", knee + bend * 0.35, knee + bend * 0.40, "root", deform=False)
bpy.ops.object.mode_set(mode="OBJECT")

# ---------------------------------------------------------------- trọng số da cho đuôi và tai
me = body.data
co = np.array([v.co[:] for v in me.vertices])
groups = body.vertex_groups
for name in [b.name for b in arm.data.bones if b.name.startswith(("tail.", "ear."))]:
    groups.new(name=name)
names = [g.name for g in groups]
W = np.zeros((len(co), len(groups)))
for v in me.vertices:
    for g in v.groups:
        W[v.index, g.group] = g.weight


def blend_into(mask, bone_names, split):
    """Chuyển phần `mask` (0..1) của mỗi đỉnh sang các xương mới, chia theo `split` (n, k), tổng mỗi hàng = 1."""
    W[:] *= (1 - mask)[:, None]
    for j, name in enumerate(bone_names):
        W[:, names.index(name)] += mask * split[:, j]


def chain_split(t, k):
    """Chia tham số t (0..1 dọc chuỗi) cho k đốt, chuyển tiếp tuyến tính giữa tâm các đốt."""
    centers = (np.arange(k) + 0.5) / k
    tc = np.clip(t, centers[0], centers[-1])
    idx = np.clip(np.searchsorted(centers, tc) - 1, 0, k - 2)
    f = (tc - centers[idx]) / (centers[idx + 1] - centers[idx])
    out = np.zeros((len(t), k))
    out[np.arange(len(t)), idx] = 1 - f
    out[np.arange(len(t)), idx + 1] = f
    return out


# đuôi: sau lưng, mảnh, ở độ cao hông
tail_mask = smoothstep(0.06, 0.10, co[:, 1]) * (np.abs(co[:, 0]) < 0.07) * ((co[:, 2] > 0.17) & (co[:, 2] < 0.34))
t = (co[:, 1] - TAIL_BASE.y) / (TAIL_TIP.y - TAIL_BASE.y)
blend_into(tail_mask, [f"tail.{i + 1:02d}" for i in range(TAIL_BONES)], chain_split(t, TAIL_BONES))

# tai: ngoài khối đầu, cao hơn má, sau trán; chia 2 đốt theo khoảng cách dọc trục tai
dist = np.linalg.norm(co - HEAD_CENTER, axis=1)
for side, s in (("L", 1), ("R", -1)):
    hinge = np.array((s * EAR_HINGE.x, EAR_HINGE.y, EAR_HINGE.z))
    tip = np.array((s * EAR_TIP.x, EAR_TIP.y, EAR_TIP.z))
    length = np.linalg.norm(tip - hinge)
    ear_mask = (smoothstep(0.22, 0.27, dist) * smoothstep(0.76, 0.82, co[:, 2])
                * smoothstep(-0.20, -0.16, co[:, 1]) * (s * co[:, 0] > 0.05))
    u = (co - hinge) @ ((tip - hinge) / length) / length
    s2 = smoothstep(0.35, 0.65, u)
    blend_into(ear_mask, [f"ear.01.{side}", f"ear.02.{side}"], np.stack([1 - s2, s2], axis=1))

W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
allv = list(range(len(co)))
for gi, vg in enumerate(groups):
    vg.remove(allv)
    for i in np.nonzero(W[:, gi] > 1e-4)[0]:
        vg.add([int(i)], float(W[i, gi]), "REPLACE")

# ---------------------------------------------------------------- 4. IK chân
pose = arm.pose.bones
for side, full in (("L", "Left"), ("R", "Right")):
    ik = pose[P + full + "Leg"].constraints.new("IK")
    ik.target, ik.subtarget = arm, f"IK_foot.{side}"
    ik.pole_target, ik.pole_subtarget = arm, f"pole_knee.{side}"
    ik.chain_count = 2
    cr = pose[P + full + "Foot"].constraints.new("COPY_ROTATION")
    cr.target, cr.subtarget = arm, f"IK_foot.{side}"
    # chọn góc pole sao cho ở tư thế nghỉ IK không làm lệch hay xoắn chân
    rest = {b: arm.data.bones[P + full + b].matrix_local.copy() for b in ("UpLeg", "Leg")}
    best = None
    for deg in range(-180, 180):
        ik.pole_angle = math.radians(deg)
        bpy.context.view_layer.update()
        err = max(pose[P + full + b].matrix.col[k].xyz.normalized().angle(rest[b].col[k].xyz.normalized())
                  for b in rest for k in (0, 1))          # lệch hướng xương (trục Y) và độ xoắn (trục X)
        if best is None or err < best[0]:
            best = (err, deg)
    ik.pole_angle = math.radians(best[1])
    print("IK", side, "pole_angle", best[1], "lệch tối đa (độ)", round(math.degrees(best[0]), 2))

for b in arm.data.bones:
    if b.name.startswith(("IK_", "pole_", "root")):
        b.color.palette = "THEME09"
arm.data.display_type = "STICK"
arm.show_in_front = True
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND), compress=True)
print("LUMO_RIG", OUT_BLEND, "bones", len(arm.data.bones), "verts", len(me.vertices),
      "tail verts", int((tail_mask > 0.5).sum()), "texture", [tuple(i.size) for i in bpy.data.images])
