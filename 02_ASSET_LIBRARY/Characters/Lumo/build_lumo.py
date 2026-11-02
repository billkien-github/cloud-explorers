"""
Lumo bản Meshy -> lumo_rig.blend (dùng trong shot)
    blender -b --factory-startup -P build_lumo.py
1. Import FBX trong source/, bỏ animation đi kèm, đưa armature và mesh về tỉ lệ 1, trục Z lên, nhìn về -Y.
2. Thêm xương: root (gốc ở mặt đất), 2 chuỗi tai, 1 chuỗi đuôi; gán lại trọng số da cho tai và đuôi
   (Meshy gắn đuôi vào xương đùi phải).
3. Chân điều khiển bằng IK: IK_foot.L/R kéo cả chân và quyết định hướng bàn chân, pole_knee.L/R định hướng đầu gối.
   Tay có IK_hand.L/R (đi theo ngực) + pole_elbow.L/R, mặc định tắt (influence 0 trên ForeArm), shot nào cần thì bật.
4. Đồ rời: áo choàng (model Meshy, co về áo choàng ngắn tới hông để đuôi và chân không xuyên), túi (thân túi
   của Meshy, bỏ dây), dây đeo dựng bằng code chéo từ hông phải qua vai trái. Áo và dây chép trọng số da từ thân.
5. Mặt (bản đầu): mí mắt dạng rèm phủ lên mắt vẽ trên texture, miệng mở hình chữ D dưới đường cười vẽ sẵn.
   Điều khiển bằng thanh trượt trên RIG-Lumo: blink_L, blink_R, mouth_open (0..1).
6. Texture 4K -> 2K, gom mọi object vào collection "Lumo" (shot nạp cả collection).
"""
import math
import pathlib

import bmesh
import bpy
import numpy as np
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE / "source" / "lumo_meshy_v01" / "Meshy_AI_Lumo_APose_V2_Rigged_biped_Animation_Forward_Roll_and_Fire_withSkin.fbx"
CAPE_SRC = HERE / "source" / "lumo_cape_meshy_v01" / "Meshy_AI_Lumo_Cape_Quad_30k_1101160456_texture.fbx"
BAG_SRC = HERE / "source" / "lumo_bag_meshy_v01" / "Meshy_AI_Lumo_Bag_Quad_30k_1101160404_texture.fbx"
OUT_BLEND = HERE / "lumo_rig.blend"
TEX_SIZE = 2048
P = "mixamorig:"

# ---------------------------------------------------------------- đồ rời (mét)
COLLAR_TOP, HEM_BACK = 0.62, 0.31             # đỉnh cổ áo sau gáy, vạt sau (trên đuôi)
SHOULDER_C, SHOULDER_R = np.array((0.0, -0.12)), np.array((0.155, 0.095))   # mặt cắt vai: tâm, bán trục x/y
CAPE_CLEAR, CAPE_TAPER = 0.022, 0.55          # khe hở áo - người; độ xoè vạt áo so với model gốc
BAG_WIDTH, BAG_POS, BAG_YAW = 0.13, (-0.085, -0.272, 0.345), -18      # túi trước bụng, lệch sang phải
STRAP_TOP, STRAP_LOW = Vector((0.11, -0.10, 0.60)), Vector((-0.15, -0.12, 0.36))  # vai trái, hông phải

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

# ---------------------------------------------------------------- 2. xương mới
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
    # IK tay: điều khiển ở cổ tay, đi theo ngực (lắc người thì tay đi theo); pole sau khuỷu
    hand, elbow = eb[P + full + "Hand"], eb[P + full + "ForeArm"].head.copy()
    new_bone(f"IK_hand.{side}", hand.head, hand.tail, P + "Spine2", deform=False, roll=hand.roll)
    new_bone(f"pole_elbow.{side}", elbow + Vector((0, 0.30, 0)), elbow + Vector((0, 0.35, 0)), P + "Spine2", deform=False)
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

# ---------------------------------------------------------------- 3. IK chân (luôn bật), IK tay (mặc định tắt)
pose = arm.pose.bones


def add_ik(upper, lower, target, pole, influence):
    """IK 2 đốt; chọn góc pole sao cho ở tư thế nghỉ IK không làm lệch hay xoắn chi, rồi đặt influence."""
    ik = pose[lower].constraints.new("IK")
    ik.target, ik.subtarget = arm, target
    ik.pole_target, ik.pole_subtarget = arm, pole
    ik.chain_count = 2
    rest = {b: arm.data.bones[b].matrix_local.copy() for b in (upper, lower)}
    best = None
    for deg in range(-180, 180):
        ik.pole_angle = math.radians(deg)
        bpy.context.view_layer.update()
        err = max(pose[b].matrix.col[k].xyz.normalized().angle(rest[b].col[k].xyz.normalized())
                  for b in rest for k in (0, 1))          # lệch hướng xương (trục Y) và độ xoắn (trục X)
        if best is None or err < best[0]:
            best = (err, deg)
    ik.pole_angle = math.radians(best[1])
    ik.influence = influence
    print("IK", lower, "pole_angle", best[1], "lệch tối đa (độ)", round(math.degrees(best[0]), 2))


for side, full in (("L", "Left"), ("R", "Right")):
    add_ik(P + full + "UpLeg", P + full + "Leg", f"IK_foot.{side}", f"pole_knee.{side}", 1.0)
    cr = pose[P + full + "Foot"].constraints.new("COPY_ROTATION")
    cr.target, cr.subtarget = arm, f"IK_foot.{side}"
    # tay: shot nào cần đặt bàn tay chính xác (vỗ tay, chạm đồ vật) thì bật influence của IK trên ForeArm
    add_ik(P + full + "Arm", P + full + "ForeArm", f"IK_hand.{side}", f"pole_elbow.{side}", 0.0)

for b in arm.data.bones:
    if b.name.startswith(("IK_", "pole_", "root")):
        b.color.palette = "THEME09"
arm.data.display_type = "STICK"
arm.show_in_front = True


# ---------------------------------------------------------------- 4. đồ rời
def import_mesh(path, name):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=str(path))
    obj = next(o for o in bpy.data.objects if o not in before)
    activate(obj)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    obj.name = obj.data.name = name
    for mat in obj.data.materials:
        mat.name = f"M_{name}"
    return obj


def mesh_neighbors_smooth_max(me, D, rounds=6):
    """Lan độ dời D ra các đỉnh lân cận (giữ độ dời lớn hơn) để mặt trong và mặt ngoài của vải cùng dịch."""
    e = np.array([ed.vertices[:] for ed in me.edges])
    for _ in range(rounds):
        acc, cnt = np.zeros_like(D), np.zeros(len(D))
        np.add.at(acc, e[:, 0], D[e[:, 1]]); np.add.at(acc, e[:, 1], D[e[:, 0]])
        np.add.at(cnt, e[:, 0], 1); np.add.at(cnt, e[:, 1], 1)
        avg = acc / np.maximum(cnt, 1)[:, None]
        D = np.where((np.linalg.norm(avg, axis=1) > np.linalg.norm(D, axis=1))[:, None], avg, D)
    return D


bm = bmesh.new()
bm.from_mesh(body.data)
body_bvh = BVHTree.FromBMesh(bm)                # tư thế nghỉ, toạ độ thế giới = toạ độ mesh
bm.free()

# áo choàng: co bán kính theo từng hướng quanh cổ sao cho lỗ cổ ôm mặt cắt vai, giữ nếp và viền của model
cape = import_mesh(CAPE_SRC, "LumoCape")
V = np.array([v.co[:] for v in cape.data.vertices])
top = V[:, 2].max()
sz = (COLLAR_TOP - HEM_BACK) / (top - V[V[:, 1] > 0.3][:, 2].min())
rel = V[:, :2] - np.array((0.0, -0.10))
r, th = np.hypot(rel[:, 0], rel[:, 1]), np.arctan2(rel[:, 1], rel[:, 0])
bins = np.linspace(-np.pi, np.pi, 37)
upper = V[:, 2] > 0.30                           # phần trên khuy áo của model gốc
r_hole = np.array([np.percentile(r[upper & (th >= a) & (th < b)], 3) if (upper & (th >= a) & (th < b)).any() else np.nan
                   for a, b in zip(bins, bins[1:])])
r_hole = np.where(np.isnan(r_hole), np.nanmean(r_hole), r_hole)
r_hole = (np.roll(r_hole, 1) + 2 * r_hole + np.roll(r_hole, -1)) / 4
centers = (bins[:-1] + bins[1:]) / 2
rh = np.interp(th, np.r_[centers[-1] - 2 * np.pi, centers, centers[0] + 2 * np.pi], np.r_[r_hole[-1], r_hole, r_hole[0]])
rb = 1 / np.sqrt((np.cos(th) / SHOULDER_R[0]) ** 2 + (np.sin(th) / SHOULDER_R[1]) ** 2) + CAPE_CLEAR
s = rb / rh
r_new = np.where(r <= rh, r * s, rb + (r - rh) * s * CAPE_TAPER)
V = np.stack([SHOULDER_C[0] + r_new * np.cos(th), SHOULDER_C[1] + r_new * np.sin(th), COLLAR_TOP - (top - V[:, 2]) * sz], axis=1)
for it in range(3):                              # đẩy phần lún vào người ra ngoài
    D = np.zeros_like(V)
    for i, c in enumerate(V):
        loc, nrm, _, _ = body_bvh.find_nearest(Vector(c), 0.08)
        if loc is not None:
            sd = (Vector(c) - loc).dot(nrm)
            if sd < CAPE_CLEAR * 0.6:
                D[i] = np.array(nrm) * (CAPE_CLEAR * 0.6 - sd)
    V = V + mesh_neighbors_smooth_max(cape.data, D)
for i, v in enumerate(cape.data.vertices):
    v.co = V[i]

# túi: giữ thân túi của Meshy (bỏ dây), mặt sau áp vào bụng
bag = import_mesh(BAG_SRC, "LumoBag")
bm = bmesh.new()
bm.from_mesh(bag.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not (v.co.z < 0.17 and v.co.y < -0.40)], context="VERTS")
bm.to_mesh(bag.data)
bm.free()
G = np.array([v.co[:] for v in bag.data.vertices])
lo, hi = G.min(0), G.max(0)
bag.data.transform(Matrix.Translation(BAG_POS) @ Matrix.Rotation(math.radians(BAG_YAW), 4, "Z")
                   @ Matrix.Scale(BAG_WIDTH / (hi[0] - lo[0]), 4)
                   @ Matrix.Translation(Vector((-(lo[0] + hi[0]) / 2, -hi[1], -(lo[2] + hi[2]) / 2))))

# dây đeo: vòng elip chéo qua thân, bám mặt da, tiết diện chữ nhật
c = (STRAP_TOP + STRAP_LOW) / 2
u = (STRAP_TOP - STRAP_LOW).normalized()
w = Vector((0, 1, 0))
w = (w - u * w.dot(u)).normalized()
N_SEG, HALF_W, THICK = 64, 0.014, 0.005
pts = []
for k in range(N_SEG):
    t = 2 * math.pi * k / N_SEG
    loc, nrm, _, _ = body_bvh.find_nearest(c + u * (0.16 * math.cos(t)) + w * (0.16 * math.sin(t)))
    pts.append((loc + nrm * 0.008, nrm))
bm = bmesh.new()
rings = []
for k, (p, n) in enumerate(pts):
    side = (pts[(k + 1) % N_SEG][0] - pts[k - 1][0]).normalized().cross(n).normalized()
    rings.append([bm.verts.new(p + side * a + n * b) for a, b in ((-HALF_W, 0), (HALF_W, 0), (HALF_W, THICK), (-HALF_W, THICK))])
for k in range(N_SEG):
    r0, r1 = rings[k], rings[(k + 1) % N_SEG]
    for j in range(4):
        bm.faces.new((r0[j], r0[(j + 1) % 4], r1[(j + 1) % 4], r1[j]))
strap = bpy.data.objects.new("LumoStrap", bpy.data.meshes.new("LumoStrap"))
bm.to_mesh(strap.data)
bm.free()
bpy.context.scene.collection.objects.link(strap)
leather = bpy.data.materials.new("M_LumoStrap")
leather.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.36, 0.15, 0.05, 1)
leather.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.55
strap.data.materials.append(leather)

# gắn vào rig: áo và dây chép trọng số từ thân rồi chỉ giữ ảnh hưởng của thân; túi đi cứng theo hông
for obj in (cape, strap):
    for name in body.vertex_groups.keys():
        obj.vertex_groups.new(name=name)
    dt = obj.modifiers.new("WeightsFromBody", "DATA_TRANSFER")
    dt.object = body
    dt.use_vert_data, dt.data_types_verts = True, {"VGROUP_WEIGHTS"}
    dt.vert_mapping = "POLYINTERP_NEAREST"
    dt.layers_vgroup_select_src, dt.layers_vgroup_select_dst = "ALL", "NAME"
    activate(obj)
    bpy.ops.object.modifier_apply(modifier=dt.name)
    names = [g.name for g in obj.vertex_groups]
    Wo = np.zeros((len(obj.data.vertices), len(names)))
    for v in obj.data.vertices:
        for g in v.groups:
            Wo[v.index, g.group] = g.weight
    keep = np.array([0.35 if n in (P + "LeftArm", P + "RightArm") else 0.3 if "UpLeg" in n else
                     1.0 if n in (P + "Hips", P + "Spine", P + "Spine1", P + "Spine2", P + "Neck", P + "LeftShoulder", P + "RightShoulder")
                     else 0.0 for n in names])              # đầu, tai, đuôi, cẳng tay, cẳng chân: không kéo áo
    lost = (Wo * (1 - keep)).sum(1)
    Wo = Wo * keep
    Wo[:, names.index(P + "Spine2")] += lost
    Wo /= np.maximum(Wo.sum(1, keepdims=True), 1e-9)
    for gi, vg in enumerate(obj.vertex_groups):
        vg.remove(list(range(len(Wo))))
        for i in np.nonzero(Wo[:, gi] > 1e-4)[0]:
            vg.add([int(i)], float(Wo[i, gi]), "REPLACE")
bag.vertex_groups.new(name=P + "Hips").add(list(range(len(bag.data.vertices))), 1.0, "REPLACE")
for obj in (cape, strap, bag):
    obj.parent = arm
    obj.modifiers.new("Armature", "ARMATURE").object = arm

# ---------------------------------------------------------------- 5. mặt: mí mắt, miệng
EYES = {"L": (0.090, 0.756), "R": (-0.089, 0.756)}     # tâm mắt vẽ trên texture (x, z), nhìn từ phía trước
EYE_RX, EYE_RZ = 0.053, 0.046
MOUTH_Z, MOUTH_HALF_W, MOUTH_DEPTH = 0.672, 0.036, 0.034


def on_face(x, z, off):
    """Điểm trên mặt da nhìn thẳng từ phía trước tại (x, z), đẩy ra theo pháp tuyến một khoảng off."""
    hit, nrm, _, _ = body_bvh.ray_cast(Vector((x, -0.6, z)), Vector((0, 1, 0)))
    return hit + nrm * off


def fur_color_near_eyes():
    """Màu lông quanh mắt lấy từ texture (đổi sRGB -> linear), dùng cho mí mắt."""
    img = next(n.image for n in body.data.materials[0].node_tree.nodes if n.type == "TEX_IMAGE" and "baseColor" in n.image.name)
    w, h = img.size
    px = np.array(img.pixels[:], np.float32).reshape(h, w, 4)
    uv = np.zeros(len(me.loops) * 2)
    me.uv_layers.active.data.foreach_get("uv", uv)
    uv = uv.reshape(-1, 2)
    vi = np.zeros(len(me.loops), int)
    me.loops.foreach_get("vertex_index", vi)
    col = px[np.clip(((uv[:, 1] % 1) * h).astype(int), 0, h - 1), np.clip(((uv[:, 0] % 1) * w).astype(int), 0, w - 1), :3]
    ring = np.zeros(len(vi), bool)
    for cx, cz in EYES.values():
        d = np.hypot((co[vi, 0] - cx) / EYE_RX, (co[vi, 2] - cz) / EYE_RZ)
        ring |= (d > 1.3) & (d < 1.8) & (co[vi, 1] < -0.2)
    good = ring & (col.min(1) < 0.75) & (col.max(1) > 0.35)        # bỏ lòng trắng, viền đen
    srgb = np.median(col[good], axis=0)
    return tuple(np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + 0.055) / 1.055) ** 2.4)) + (1.0,)


def flat_material(name, color, rough=0.6):
    mat = bpy.data.materials.new(name)
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    return mat


def shaped_patch(name, closed_rows, open_rows, mats, mat_of_band):
    """Tấm lưới theo hàng: hình gốc = closed_rows, shape key "open" = open_rows; mỗi dải giữa 2 hàng một vật liệu."""
    bm = bmesh.new()
    rows = [[bm.verts.new(p) for p in row] for row in closed_rows]
    for j in range(len(rows) - 1):
        for i in range(len(rows[j]) - 1):
            f = bm.faces.new((rows[j][i], rows[j][i + 1], rows[j + 1][i + 1], rows[j + 1][i]))
            f.material_index = mat_of_band(j)
            f.smooth = True
    obj = bpy.data.objects.new(name, bpy.data.meshes.new(name))
    bm.to_mesh(obj.data)
    bm.free()
    for m in mats:
        obj.data.materials.append(m)
    obj.shape_key_add(name="Basis")
    key = obj.shape_key_add(name="open")
    flat = [p for row in open_rows for p in row]
    for i, p in enumerate(flat):
        key.data[i].co = p
    bpy.context.scene.collection.objects.link(obj)
    return obj


def drive(key, prop, expr):
    d = key.driver_add("value").driver
    d.type = "SCRIPTED"
    var = d.variables.new()
    var.name = "v"
    var.targets[0].id = arm
    var.targets[0].data_path = f'["{prop}"]'
    d.expression = expr


for prop in ("blink_L", "blink_R", "mouth_open"):
    arm[prop] = 0.0
    arm.id_properties_ui(prop).update(min=0.0, max=1.0, soft_min=0.0, soft_max=1.0)

lid_mat = flat_material("M_LumoLid", fur_color_near_eyes(), 0.7)
lash_mat = flat_material("M_LumoLash", (0.03, 0.015, 0.01, 1), 0.5)
face_parts = []
T = list(np.linspace(0, 0.91, 10)) + [1.0]             # dải cuối mỏng = viền mi khi nhắm
for side, (cx, cz) in EYES.items():
    us = np.linspace(-1, 1, 25)
    vt = np.sqrt(np.clip(1 - us ** 2, 0, 1))
    closed = [[on_face(cx + EYE_RX * u, cz + EYE_RZ * (v - t * 2 * v), 0.0022) for u, v in zip(us, vt)] for t in T]
    opened = [[on_face(cx + EYE_RX * u, cz + EYE_RZ * v + 0.003, 0.0018) for u, v in zip(us, vt)] for _ in T]
    lid = shaped_patch(f"LumoLid.{side}", closed, opened, [lid_mat, lash_mat], lambda j: 1 if j == len(T) - 2 else 0)
    drive(lid.data.shape_keys.key_blocks["open"], f"blink_{side}", "1 - v")
    face_parts.append(lid)

mouth_mat = flat_material("M_LumoMouth", (0.16, 0.025, 0.02, 1), 0.45)
tongue_mat = flat_material("M_LumoTongue", (0.75, 0.22, 0.25, 1), 0.45)
us = np.linspace(-1, 1, 21)
top = MOUTH_Z + 0.006 * us ** 2                         # khoé miệng hơi cao như đang cười
depth = MOUTH_DEPTH * np.sqrt(np.clip(1 - us ** 2, 0, 1))
TM = np.linspace(0, 1, 7)
closed = [[on_face(MOUTH_HALF_W * u, z, 0.0022) for u, z in zip(us, top)] for _ in TM]
opened = [[on_face(MOUTH_HALF_W * u, z - t * d, 0.0022) for u, z, d in zip(us, top, depth)] for t in TM]
mouth = shaped_patch("LumoMouth", closed, opened, [mouth_mat, tongue_mat], lambda j: 1 if j >= 4 else 0)
drive(mouth.data.shape_keys.key_blocks["open"], "mouth_open", "v")
face_parts.append(mouth)

for obj in face_parts:                                  # đi cứng theo xương đầu
    obj.vertex_groups.new(name=P + "Head").add(list(range(len(obj.data.vertices))), 1.0, "REPLACE")
    obj.parent = arm
    obj.modifiers.new("Armature", "ARMATURE").object = arm

# ---------------------------------------------------------------- 6. texture 2K, collection, lưu
for img in bpy.data.images:
    if img.size[0] > TEX_SIZE:
        img.scale(TEX_SIZE, TEX_SIZE)
        img.pack()
coll = bpy.data.collections.new("Lumo")
bpy.context.scene.collection.children.link(coll)
for obj in (arm, body, cape, bag, strap, *face_parts):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    coll.objects.link(obj)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND), compress=True)
print("LUMO_RIG", OUT_BLEND, "bones", len(arm.data.bones), "verts", len(me.vertices),
      "tail verts", int((tail_mask > 0.5).sum()), "outfit verts", [len(o.data.vertices) for o in (cape, bag, strap)],
      "texture", sorted({tuple(i.size) for i in bpy.data.images}))
