"""
EP001 sh030 (shot dựng thử) — Thung lũng khô. Lumo hăng hái sải bước, mũi chân mắc vào vết nứt, chúi người,
quờ tay quay vòng giữ thăng bằng, bước chặn lại, đứng vững, ngoái nhìn vết nứt rồi nhún vai cười trừ.
    .\\pipeline\\run.ps1 build -Shot 04_PRODUCTION\\EP001_Great_Rain_Experiment\\sh030
Animation tạo hoàn toàn bằng code, lấy mẫu từng khung. Mọi góc xoay tính theo trục thế giới
(Lumo nhìn về -Y: quanh +X là cúi về trước, quanh +Z là quay sang trái).
"""
import math
import pathlib
import random
import sys

import bmesh
import bpy
from mathutils import Vector

HERE = pathlib.Path(__file__).resolve().parent
STUDIO = HERE.parents[2]
sys.path.insert(0, str(STUDIO / "pipeline"))
from rig_qa import apply_pose  # noqa: E402

LUMO_BLEND = STUDIO / "02_ASSET_LIBRARY" / "Characters" / "Lumo" / "lumo_rig.blend"
OUT_BLEND = HERE / "sh030.blend"
P = "mixamorig:"
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)

# ---------------------------------------------------------------- nhịp (khung, 24 fps)
FPS, FRAMES = 24, 168
STEP, S = 7, 0.12               # mỗi bước 7 khung, dài 0.12 m (chân Lumo rất ngắn)
V = S / STEP
Y0 = 1.05                       # hông lùi về sau 1.05 m lúc bắt đầu
HIP_DROP, BOB = 0.012, 0.008
TS = 60                         # mũi chân phải mắc vào vết nứt
LOOK0, LOOK1, LOOK2 = 112, 130, 140     # ngoái lại, giữ, quay về
SCR0, SCR1 = 142, 168           # nhún vai cười trừ (tay Lumo quá ngắn để gãi đầu)


def ss(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def keys(f, pts):
    """Nội suy mượt (dừng ở mỗi mốc) giữa các mốc (khung, giá trị)."""
    if f <= pts[0][0]:
        return pts[0][1]
    for (f0, v0), (f1, v1) in zip(pts, pts[1:]):
        if f <= f1:
            return v0 + (v1 - v0) * ss((f - f0) / (f1 - f0))
    return pts[-1][1]


def hermite(s, p1, m0):
    """Từ 0 tới p1, vận tốc đầu m0, vận tốc cuối 0 (s = 0..1)."""
    s = min(max(s, 0.0), 1.0)
    return (s ** 3 - 2 * s ** 2 + s) * m0 + (-2 * s ** 3 + 3 * s ** 2) * p1


# ---------------------------------------------------------------- đi bộ
def walk_hips_y(f):
    return Y0 - V * (f - 1)


def plant(k):
    """Vị trí (theo trục y) chân đặt xuống sau bước k; k = -2, -1 là hai chân lúc bắt đầu."""
    return walk_hips_y(1 + (k + 1) * STEP) - S / 2


def walk_foot(f, side):
    """(y, z, góc gập mũi chân) của chân ở khung f. Chân phải bước ở bước chẵn, chân trái ở bước lẻ."""
    n = int((f - 1) // STEP)
    u = ((f - 1) - n * STEP) / STEP
    swing = "R" if n % 2 == 0 else "L"
    if side != swing:
        return plant(n - 1), 0.0, 0.0
    a, b = plant(n - 2), plant(n)
    return a + (b - a) * ss(u), 0.045 * math.sin(math.pi * u), 20 * math.sin(2 * math.pi * u)


# ---------------------------------------------------------------- vấp và đứng lại (sau TS)
HY_TS = walk_hips_y(TS)
FOOT_R_TS = walk_foot(TS, "R")
Y_END = HY_TS - 0.22                     # hông dừng ở đây
L_LAND, R_LAND = Y_END + 0.035, Y_END - 0.02


def hips_y(f):
    if f <= TS:
        return walk_hips_y(f)
    return HY_TS - hermite((f - TS) / 34, 0.22, V * 34)


def foot_after(f, side):
    if side == "R":                       # mắc ở vết nứt tới TS+12, rồi bước lên ngang chân trái
        if f <= TS + 12:
            t = ss((f - TS) / 4)
            return FOOT_R_TS[0] + (FOOT_R_TS[0] - 0.01 - FOOT_R_TS[0]) * t, FOOT_R_TS[1] * (1 - t) - 0.012 * t, 15 + 10 * t
        u = ss((f - TS - 12) / 12)
        return FOOT_R_TS[0] + (R_LAND - FOOT_R_TS[0]) * u, 0.06 * math.sin(math.pi * min(1, (f - TS - 12) / 12)), keys(f, [(TS + 12, 25), (TS + 18, 10), (TS + 24, 0)])
    y_l = plant(7)                        # chân trái: đang trụ, nhảy lên chặn ở TS+8..TS+16
    u = min(max((f - TS - 8) / 8, 0), 1)
    return y_l + (L_LAND - y_l) * ss(u), 0.07 * math.sin(math.pi * u), keys(f, [(TS + 8, 0), (TS + 10, 15), (TS + 15, -15), (TS + 17, 0)])


def foot(f, side):
    return walk_foot(f, side) if f <= TS else foot_after(f, side)


# ---------------------------------------------------------------- lò xo cho tai và đuôi (đi trễ theo thân)
def spring(series, k=0.22, damp=0.72):
    out, x, v = [], series[0], 0.0
    for target in series:
        v = damp * v + k * (target - x)
        x += v
        out.append(x)
    return out


def body_pitch(f):
    """Độ chúi về trước của thân (độ), dùng cho cả hông và lò xo của tai, đuôi."""
    return keys(f, [(TS, 0), (TS + 7, 32), (TS + 13, 40), (TS + 21, 0), (TS + 27, -12), (TS + 33, 5), (TS + 40, 0)])


FR = range(1, FRAMES + 1)
PITCH = [body_pitch(f) for f in FR]
PITCH_LAG = spring(PITCH)
YAW_HEAD = [keys(f, [(LOOK0, 0), (LOOK0 + 10, 110), (LOOK1, 110), (LOOK2, 15)]) for f in FR]
YAW_LAG = spring(YAW_HEAD, 0.18, 0.7)


def pose_at(f):
    i = f - 1
    phi = math.pi * (f - 1) / STEP
    w = 1 - ss((f - TS) / 6)                 # còn bao nhiêu nhịp đi bộ
    pose = {}

    # hông: tiến về trước, nhún, lắc, chúi khi vấp
    hz = -HIP_DROP - w * BOB * math.cos(2 * phi) + keys(f, [(TS, 0), (TS + 10, -0.06), (TS + 16, -0.085), (TS + 24, 0.01), (TS + 32, 0.0)])
    hx = w * 0.012 * math.sin(phi)
    pose[P + "Hips"] = {"loc": (hx, hips_y(f), hz),
                        "rot": [(Z, -w * 7 * math.cos(phi)), (Y, w * 3 * math.sin(phi)), (X, PITCH[i])]}
    lean = keys(f, [(TS, 0), (TS + 8, 10), (TS + 22, 0)])
    pose[P + "Spine"] = {"rot": [(X, lean)]}
    pose[P + "Spine1"] = {"rot": [(Z, w * 5 * math.cos(phi) + keys(f, [(LOOK0, 0), (LOOK0 + 10, 15), (LOOK1, 15), (LOOK2, 0)])),
                                  (X, lean)]}
    proud = -6 * keys(f, [(1, 1), (TS, 1), (TS + 4, 0), (TS + 60, 0), (TS + 70, 0.3)])
    look = YAW_HEAD[i]
    pose[P + "Spine2"] = {"rot": [(Z, look * 0.18), (X, proud)]}
    pose[P + "Neck"] = {"rot": [(Z, look * 0.25)]}
    head_up = keys(f, [(TS, -4), (TS + 8, -20), (TS + 22, -4), (LOOK0, -4), (LOOK0 + 10, 16), (LOOK1, 16),
                       (LOOK2, -4), (SCR0, -4), (SCR0 + 8, 6)])     # vấp: ngẩng nhìn trước; ngoái: cúi nhìn vết nứt
    head_tilt = keys(f, [(SCR0, 0), (SCR0 + 8, 10), (SCR1, 10)])                             # cười trừ: nghiêng đầu
    pose[P + "Head"] = {"rot": [(Z, look * 0.35), (X, head_up), (Y, head_tilt)]}

    # chân: IK, pole đi theo hông để đầu gối luôn hướng về trước
    for side in ("L", "R"):
        fy, fz, roll = foot(f, side)
        pose[f"IK_foot.{side}"] = {"loc": (0, fy, fz), "rot": [(X, roll)]}
        pose[f"pole_knee.{side}"] = {"loc": (0, hips_y(f), 0)}

    # tay: vung khi đi, quay vòng khi vấp, dang ra giữ thăng bằng, rồi buông; tay phải lên gãi đầu
    swing = 22 * w * math.cos(phi)
    m = ss((f - TS - 4) / 26)
    mill = 720 * m
    offset = 180 * math.sin(math.pi * m)               # hai tay lệch pha nhau giữa lúc quay
    out = keys(f, [(TS, 25), (TS + 4, -60), (TS + 30, -60), (TS + 36, -75), (TS + 46, -75), (TS + 58, 25)])   # dương = khép xuống
    shrug = keys(f, [(SCR0, 0), (SCR0 + 8, 1)])           # dang tay ngang, cẳng tay dựng lên, vai nhún 2 nhịp
    hehe = 6 * abs(math.sin(math.pi * (f - SCR0 - 8) / 6)) if SCR0 + 8 <= f <= SCR0 + 20 else 0
    pose[P + "LeftArm"] = {"rot": [(X, swing - mill), (Y, out - 75 * shrug)]}
    pose[P + "RightArm"] = {"rot": [(X, -swing - mill - offset), (Y, -out + 75 * shrug)]}
    pose[P + "LeftForeArm"] = {"rot": [(X, -20 * w), (Y, -70 * shrug)]}
    pose[P + "RightForeArm"] = {"rot": [(X, -20 * w), (Y, 70 * shrug)]}
    pose[P + "LeftShoulder"] = {"rot": [(Y, -(8 * shrug + hehe))]}
    pose[P + "RightShoulder"] = {"rot": [(Y, 8 * shrug + hehe)]}

    # tai: nảy theo nhịp nhún, đi trễ khi thân chúi, cụp nhẹ khi ngượng
    shy = keys(f, [(SCR0, 0), (SCR0 + 8, 1)])
    for side, s in (("L", 1), ("R", -1)):
        lag = PITCH_LAG[i] - PITCH[i]
        b1 = w * 6 * math.cos(2 * phi - 0.6)
        b2 = w * 5 * math.cos(2 * phi - 1.2)
        pose[f"ear.01.{side}"] = {"rot": [(X, b1 + 1.2 * lag + 18 * shy), (Y, s * 12 * shy)]}
        pose[f"ear.02.{side}"] = {"rot": [(X, b2 + 1.6 * lag + 10 * shy)]}

    # đuôi: vẫy theo bước, vểnh lên khi đang hãnh diện, giật lên khi vấp, quất theo lúc ngoái
    pride = 12 * keys(f, [(1, 1), (TS, 1), (TS + 40, 0.3), (SCR0, 0.3), (SCR0 + 8, -0.3)])
    whip = YAW_LAG[i] - YAW_HEAD[i]
    for k in range(1, 5):
        sway = w * 10 * (1 + 0.3 * k) * math.sin(phi - 0.5 * k)
        pose[f"tail.{k:02d}"] = {"rot": [(Z, sway + 0.12 * k * whip),
                                         (X, pride / 2 + (PITCH[i] - PITCH_LAG[i]) * 0.6 * k * 0.5)]}
    return pose


# ---------------------------------------------------------------- dựng cảnh
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, FRAMES
random.seed(30)

with bpy.data.libraries.load(str(LUMO_BLEND), link=False) as (src, dst):
    dst.objects = ["RIG-Lumo", "LumoBody"]
for o in dst.objects:
    scene.collection.objects.link(o)
rig = bpy.data.objects["RIG-Lumo"]
rig.hide_render = True
rig.data.display_type = "STICK"


def material(name, color, rough=0.9):
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    return m


def sock(sockets, name, kind):
    """ShaderNodeMix có nhiều socket trùng tên: chọn theo kiểu."""
    return next(s for s in sockets if s.name == name and s.type == kind)


def ground_material():
    """Đất khô nứt nẻ: màu loang theo noise, vết nứt = mép ô Voronoi bị nhiễu nhẹ."""
    m = bpy.data.materials.new("M_DryEarth")
    n, links = m.node_tree.nodes, m.node_tree.links
    bsdf = n["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = 0.95
    tc = n.new("ShaderNodeTexCoord")
    noise = n.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 3.0
    ramp = n.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.40, 0.23, 0.11, 1)
    ramp.color_ramp.elements[1].color = (0.60, 0.38, 0.19, 1)
    warp = n.new("ShaderNodeTexNoise")
    warp.inputs["Scale"].default_value = 6.0
    mixv = n.new("ShaderNodeMix")
    mixv.data_type = "VECTOR"
    mixv.inputs[0].default_value = 0.08
    vor = n.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 2.2
    edge = n.new("ShaderNodeMapRange")                 # 1 ở mép vết nứt, 0 ở giữa ô đất
    edge.inputs["From Min"].default_value, edge.inputs["From Max"].default_value = 0.025, 0.0
    mixc = n.new("ShaderNodeMix")
    mixc.data_type = "RGBA"
    sock(mixc.inputs, "B", "RGBA").default_value = (0.22, 0.13, 0.07, 1)
    bump = n.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.35
    bump.invert = True
    links.new(tc.outputs["Object"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
    links.new(tc.outputs["Object"], warp.inputs["Vector"])
    links.new(tc.outputs["Object"], sock(mixv.inputs, "A", "VECTOR"))
    links.new(warp.outputs["Color"], sock(mixv.inputs, "B", "VECTOR"))
    links.new(sock(mixv.outputs, "Result", "VECTOR"), vor.inputs["Vector"])
    links.new(vor.outputs["Distance"], edge.inputs["Value"])
    links.new(edge.outputs["Result"], mixc.inputs[0])
    links.new(ramp.outputs["Color"], sock(mixc.inputs, "A", "RGBA"))
    links.new(sock(mixc.outputs, "Result", "RGBA"), bsdf.inputs["Base Color"])
    links.new(edge.outputs["Result"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def add_mesh(name, bm, mat):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


# mặt đất
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=12)
add_mesh("Ground", bm, ground_material())

# vết nứt chỗ Lumo vấp: dải zigzag tối, ngay trước mũi chân phải lúc TS
toe_y = -0.119 + FOOT_R_TS[0] - 0.13
crack_mat = material("M_Crack", (0.05, 0.03, 0.02, 1), 1.0)
bm = bmesh.new()
pts = [(-0.75 + 0.1 * k, toe_y + (0.025 if k % 2 else -0.02) + random.uniform(-0.01, 0.01)) for k in range(16)]
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    wdt = 0.03
    vs = [bm.verts.new((x0, y0 - wdt, 0.002)), bm.verts.new((x1, y1 - wdt, 0.002)),
          bm.verts.new((x1, y1 + wdt, 0.002)), bm.verts.new((x0, y0 + wdt, 0.002))]
    bm.faces.new(vs)
add_mesh("Crack", bm, crack_mat)

# đá và cỏ khô
rock_mat = material("M_Rock", (0.42, 0.33, 0.25, 1), 0.85)
grass_mat = material("M_DryGrass", (0.74, 0.58, 0.28, 1), 0.9)
for k in range(14):
    x = random.choice([-1, 1]) * random.uniform(0.6, 3.5)
    y = random.uniform(-2.0, 5.0)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=random.uniform(0.06, 0.22))
    r = add_mesh(f"Rock_{k}", bm, rock_mat)
    r.location = (x, y, 0.0)
    r.scale = (1, random.uniform(0.7, 1.3), random.uniform(0.45, 0.7))
    r.rotation_euler = (0, 0, random.uniform(0, 6.28))
    bpy.ops.object.select_all(action="DESELECT")
for k in range(22):
    cx, cy = random.choice([-1, 1]) * random.uniform(0.45, 3.0), random.uniform(-1.5, 5.0)
    for j in range(5):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, segments=4, radius1=0.008, radius2=0.0, depth=random.uniform(0.08, 0.18))
        g = add_mesh(f"Grass_{k}_{j}", bm, grass_mat)
        g.location = (cx + random.uniform(-0.05, 0.05), cy + random.uniform(-0.05, 0.05), 0.05)
        g.rotation_euler = (random.uniform(-0.4, 0.4), random.uniform(-0.4, 0.4), 0)

# đồi xa
hill_mat = material("M_Hill", (0.70, 0.52, 0.38, 1), 1.0)
for k, (x, y, rx, rz) in enumerate([(-14, 22, 10, 3.0), (2, 26, 12, 4.0), (16, 20, 9, 2.6), (-26, 18, 9, 2.4)]):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=32, radius=1.0)
    for face in bm.faces:
        face.smooth = True
    h = add_mesh(f"Hill_{k}", bm, hill_mat)
    h.location, h.scale = (x, y, -0.5), (rx, rx * 0.6, rz)

# trời, nắng
world = bpy.data.worlds.new("Sky")
scene.world = world
world.use_nodes = True
wn, wl = world.node_tree.nodes, world.node_tree.links
bg = wn["Background"]
grad_tc = wn.new("ShaderNodeTexCoord")
sep = wn.new("ShaderNodeSeparateXYZ")
sky_ramp = wn.new("ShaderNodeValToRGB")
sky_ramp.color_ramp.elements[0].color = (0.98, 0.78, 0.55, 1)
sky_ramp.color_ramp.elements[1].position = 0.45
sky_ramp.color_ramp.elements[1].color = (0.30, 0.55, 0.92, 1)
wl.new(grad_tc.outputs["Generated"], sep.inputs[0])
wl.new(sep.outputs["Z"], sky_ramp.inputs["Fac"])
wl.new(sky_ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 0.7
sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
scene.collection.objects.link(sun)
sun.data.energy, sun.data.color, sun.data.angle = 3.2, (1.0, 0.86, 0.68), math.radians(4)
sun.rotation_euler = (math.radians(52), 0, math.radians(-35))

# máy quay: chếch 3/4 phía trước bên trái của Lumo (thấy rõ cú chúi người), lia theo hông
aim = bpy.data.objects.new("CamAim", None)
scene.collection.objects.link(aim)
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
scene.collection.objects.link(cam)
scene.camera = cam
cam.data.lens = 40
tt = cam.constraints.new("TRACK_TO")
tt.target, tt.track_axis, tt.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
for f in FR:
    hy = -0.102 + hips_y(f)
    aim.location = (0.0, 0.7 * hy, 0.55)
    aim.keyframe_insert("location", frame=f)
    cam.location = (2.0, -1.75 + 0.15 * hy, 0.58)
    cam.keyframe_insert("location", frame=f)

# ---------------------------------------------------------------- keyframe cho Lumo
prev = {}
for f in FR:
    pose = pose_at(f)
    apply_pose(rig, pose)
    for name in pose:
        pb = rig.pose.bones[name]
        q = pb.rotation_quaternion.copy()
        if name in prev and prev[name].dot(q) < 0:          # giữ dấu quaternion liền mạch giữa các khung
            q.negate()
            pb.rotation_quaternion = q
        prev[name] = q
        pb.keyframe_insert("location", frame=f)
        pb.keyframe_insert("rotation_quaternion", frame=f)

# ---------------------------------------------------------------- render
r = scene.render
r.engine = "BLENDER_EEVEE"
r.resolution_x, r.resolution_y = 1920, 1080
scene.eevee.taa_render_samples = 32
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Punchy"
scene["stills"] = "1,30,58,66,74,84,96,124,150,166"
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND), compress=True)
print("SH030_SAVED", OUT_BLEND, "crack y", round(toe_y, 3), "hips end", round(Y_END, 3))
