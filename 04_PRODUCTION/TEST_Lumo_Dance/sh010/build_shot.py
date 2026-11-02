"""
TEST_Lumo_Dance sh010 — Lumo nhảy 16 giây theo kiểu "Baby Shark": tay khép mở như hàm cá theo 3 cỡ
(baby = hai bàn tay trước miệng, mommy = hai cẳng tay, daddy = cả cánh tay), nhún, bước, nhảy bật, xoay, hát.
    .\\pipeline\\run.ps1 build -Shot 04_PRODUCTION\\TEST_Lumo_Dance\\sh010
Nhịp và giai điệu ở timing.py (dùng chung với build_audio.py). Tay dùng IK (bật influence trong shot),
mặt dùng thanh trượt blink_L, blink_R, mouth_open của lumo_rig.blend. Góc xoay theo trục thế giới
(Lumo nhìn về -Y: quanh +X là cúi về trước, quanh +Y là nghiêng sang phải, quanh +Z là quay sang trái).
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
sys.path.insert(0, str(HERE))
from rig_qa import apply_pose  # noqa: E402
from timing import BEAT, BLINKS, FPS, FRAMES, MELODY, SECTIONS, SHOUTS, section  # noqa: E402

LUMO_BLEND = STUDIO / "02_ASSET_LIBRARY" / "Characters" / "Lumo" / "lumo_rig.blend"
OUT_BLEND = HERE / "sh010.blend"
P = "mixamorig:"
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def ss(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def beat_of(f):
    return (f - 1) / BEAT


def local(b):
    """(tên đoạn, nhịp tính từ đầu đoạn)."""
    name = section(b)
    return name, b - SECTIONS[name][0]


# ---------------------------------------------------------------- tay: vị trí cổ tay (toạ độ tư thế nghỉ, đi theo ngực)
# Vai -> cổ tay chỉ dài 0.22 m. Giữ mọi vị trí trong 0.195 m (khuỷu luôn gập, IK không lật), tránh má lông
# trước cằm và bụng tròn (trước ngực ở z 0.5 là y -0.23, trước bụng ở z 0.43 là y -0.25).
REACH = 0.195


def hands_in(name, t):
    clap_l, clap_r = Vector((0.045, -0.27, 0.51)), Vector((-0.045, -0.27, 0.51))
    if name == "intro":                                   # buông thả hai bên, đung đưa theo nhịp
        sw = 0.03 * math.sin(math.pi * t)
        return Vector((0.22, -0.12 + sw, 0.42)), Vector((-0.22, -0.12 - sw, 0.42))
    if name == "baby":                                    # vỗ nhỏ trước ngực, 2 lần mỗi nhịp
        o = abs(math.sin(2 * math.pi * t))
        return clap_l.lerp(Vector((0.11, -0.26, 0.52)), o), clap_r.lerp(Vector((-0.11, -0.26, 0.52)), o)
    if name == "mommy":                                   # dang rộng sang hai bên rồi vỗ, 1 lần mỗi nhịp
        o = abs(math.sin(math.pi * t))
        return clap_l.lerp(Vector((0.22, -0.19, 0.53)), o), clap_r.lerp(Vector((-0.22, -0.19, 0.53)), o)
    if name == "daddy":                                   # hàm lớn: tay trái vung lên, tay phải vung xuống, đập vào nhau
        o = abs(math.sin(math.pi * t))
        return clap_l.lerp(Vector((0.20, -0.16, 0.68)), o), Vector((-0.045, -0.27, 0.50)).lerp(Vector((-0.20, -0.17, 0.40)), o)
    if t < 2:                                             # xoay: dang tay
        return Vector((0.29, -0.12, 0.56)), Vector((-0.29, -0.12, 0.56))
    return Vector((0.24, -0.12, 0.68)), Vector((-0.24, -0.12, 0.68))     # "ta-da": giơ chữ V chéo ra hai bên


def within_reach(target, side):
    shoulder = rig.data.bones[P + ("Left" if side == "L" else "Right") + "Arm"].head_local
    d = target - shoulder
    return shoulder + d * min(1.0, REACH / d.length)


def hands(b):
    name, t = local(b)
    cur = hands_in(name, t)
    order = list(SECTIONS)
    if name == "finale" and 2 <= t < 2.5:                 # chuyển từ dang tay sang chữ V
        prev, k = hands_in("finale", 1.99), ss((t - 2) / 0.5)
    elif t < 0.5 and name != "intro":                     # nửa nhịp đầu mỗi đoạn: chuyển mượt từ đoạn trước
        before = order[order.index(name) - 1]
        prev, k = hands_in(before, SECTIONS[before][1] - SECTIONS[before][0] - 0.01), ss(t / 0.5)
    else:
        return cur
    return tuple(a.lerp(c, k) for a, c in zip(prev, cur))


# ---------------------------------------------------------------- chân, hông
def hop(t):
    """Nhảy bật mỗi nhịp: (độ cao chân, độ cao hông)."""
    u = t % 1
    air = math.sin(math.pi * u)
    land = math.exp(-((u / 0.12) ** 2)) + math.exp(-(((u - 1) / 0.12) ** 2))
    return 0.03 * air, 0.045 * air - 0.03 * land


def legs(b):
    """(hông x, hông z, chân trái (x, z), chân phải (x, z))."""
    name, t = local(b)
    dip = 0.5 + 0.5 * math.cos(2 * math.pi * t)          # thấp nhất đúng nhịp
    lx = rx = lz = rz = 0.0
    if name in ("intro", "baby"):
        hx, hz = (0.0 if name == "intro" else 0.02 * math.sin(math.pi * t)), -0.022 * dip
    elif name == "mommy":                                 # bước sang phải, về, sang trái, về
        k, u = int(t % 4), (t % 4) % 1
        out = [ss(u), 1 - ss(u), ss(u), 1 - ss(u)][k]
        lift = 0.03 * math.sin(math.pi * u)
        if k < 2:
            rx, rz = -0.06 * out, lift
        else:
            lx, lz = 0.06 * out, lift
        hx, hz = 0.03 * (lx + rx) / 0.06, -0.028 * dip
    elif name == "daddy":
        foot, hz = hop(t)
        lz = rz = foot
        hx = 0.0
    else:
        hx = 0.0
        hz = -0.02 * dip if t < 2 else 0.012 * ss((t - 2) / 0.5)
        if t >= 2:                                        # "ta-da": chân trái chĩa ra trước
            lx, lz = 0.02 * ss((t - 2) / 0.5), 0.0
    return hx, hz, (lx, lz), (rx, rz)


# ---------------------------------------------------------------- mặt
def mouth(b):
    v = 0.0
    for s, d, note in MELODY:
        if s <= b < s + d:
            amp = 0.55 if note >= 72 else 0.75 if note >= 60 else 1.0
            v = max(v, amp * math.sin(math.pi * (b - s) / d) ** 0.6)
    for s, d in SHOUTS:
        if s <= b < s + d:
            v = max(v, min(1.0, 4 * (b - s) / d, 4 * (s + d - b) / d))
    return v


def blinks(b):
    v = max([max(0.0, 1 - abs(b - x) / 0.22) for x in BLINKS] + [0.0])
    happy = 0.3 * ss((b - 30) / 0.5)                      # kết: mắt cười híp
    wink = 1.0 if 30.4 <= b < 31.2 else 0.0
    return min(1, v + happy), min(1, max(v + happy, wink))


# ---------------------------------------------------------------- tư thế từng khung
def pose_at(f):
    b = beat_of(f)
    name, t = local(b)
    hx, hz, (lx, lz), (rx, rz) = legs(b)
    nod = 5 * (0.5 + 0.5 * math.cos(2 * math.pi * t))
    tilt = 8 * math.sin(math.pi * t) if name != "finale" else 0.0
    spin = 360 * ss((b - 28) / 2) if b >= 28 else 0.0
    lean = {"intro": 2, "baby": 5, "mommy": 3, "daddy": 6, "finale": 0}[name]
    pose = {
        "root": {"rot": [(Z, spin)]},
        P + "Hips": {"loc": (hx, 0, hz), "rot": [(Y, -hx * 150)]},
        P + "Spine1": {"rot": [(X, lean), (Y, hx * 250)]},
        P + "Spine2": {"rot": [(X, lean * 0.5)]},
        P + "Neck": {"rot": [(Y, tilt * 0.4)]},
        P + "Head": {"rot": [(X, nod - lean), (Y, tilt), (Z, -tilt * 0.5)]},
        "IK_foot.L": {"loc": (lx, 0, lz)},
        "IK_foot.R": {"loc": (rx, 0, rz)},
    }
    rest = {s: rig.data.bones[f"IK_hand.{s}"].head_local for s in ("L", "R")}
    for s, target in zip(("L", "R"), hands(b)):
        pose[f"IK_hand.{s}"] = {"loc": tuple(within_reach(target, s) - rest[s])}
    flop = {"daddy": 14, "mommy": 9}.get(name, 6)
    for s, sg in (("L", 1), ("R", -1)):
        pose[f"ear.01.{s}"] = {"rot": [(X, flop * math.cos(2 * math.pi * t - 0.9)), (Y, -sg * tilt * 0.6)]}
        pose[f"ear.02.{s}"] = {"rot": [(X, flop * 0.8 * math.cos(2 * math.pi * t - 1.6))]}
    wag = {"intro": 14, "baby": 16, "mommy": 22, "daddy": 28, "finale": 10}[name]
    for k in range(1, 5):
        pose[f"tail.{k:02d}"] = {"rot": [(Z, wag * math.sin(math.pi * t - 0.55 * k)), (X, 10)]}
    return pose


# ---------------------------------------------------------------- cảnh
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, FRAMES
random.seed(10)

with bpy.data.libraries.load(str(LUMO_BLEND), link=False) as (src, dst):
    dst.collections = ["Lumo"]
scene.collection.children.link(dst.collections[0])
rig = bpy.data.objects["RIG-Lumo"]
rig.hide_render = True
for s in ("Left", "Right"):                               # bật IK tay cho cả shot
    rig.pose.bones[P + s + "ForeArm"].constraints["IK"].influence = 1.0


def material(name, color, rough=0.6):
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    return m


def add_obj(name, bm, mat, smooth=False):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        me.shade_smooth()
    obj = bpy.data.objects.new(name, me)
    scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return obj


bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=15)
add_obj("Ground", bm, material("M_Ground", (0.42, 0.78, 0.66, 1), 0.9))
bm = bmesh.new()
bmesh.ops.create_cone(bm, segments=64, radius1=0.75, radius2=0.72, depth=0.04, cap_ends=True)
stage = add_obj("Stage", bm, material("M_Stage", (0.98, 0.92, 0.82, 1), 0.5), smooth=True)
stage.location.z = -0.019

# bong bóng bay lên ở phía sau
bubble_mats = [material(f"M_Bubble{i}", c, 0.15) for i, c in
               enumerate([(0.55, 0.80, 1.0, 1), (1.0, 0.70, 0.85, 1), (0.75, 0.65, 1.0, 1), (1.0, 0.90, 0.55, 1)])]
for k in range(18):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=12, radius=random.uniform(0.03, 0.09))
    bub = add_obj(f"Bubble_{k}", bm, random.choice(bubble_mats), smooth=True)
    x0, y0, z0 = random.uniform(-2.6, 2.6), random.uniform(1.2, 3.5), random.uniform(-0.3, 2.2)
    speed = random.uniform(0.08, 0.16)
    for f in range(1, FRAMES + 1, 6):
        z = -0.3 + (z0 + 0.3 + speed * (f - 1) / FPS) % 2.6
        bub.location = (x0 + 0.05 * math.sin(f / 20 + k), y0, z)
        bub.keyframe_insert("location", frame=f)

world = bpy.data.worlds.new("Sky")
scene.world = world
world.use_nodes = True
wn, wl = world.node_tree.nodes, world.node_tree.links
tc, sep, ramp = wn.new("ShaderNodeTexCoord"), wn.new("ShaderNodeSeparateXYZ"), wn.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].color = (1.0, 0.80, 0.70, 1)
ramp.color_ramp.elements[1].position = 0.45
ramp.color_ramp.elements[1].color = (0.40, 0.65, 1.0, 1)
wl.new(tc.outputs["Generated"], sep.inputs[0])
wl.new(sep.outputs["Z"], ramp.inputs["Fac"])
wl.new(ramp.outputs["Color"], wn["Background"].inputs["Color"])
wn["Background"].inputs["Strength"].default_value = 0.8
sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
scene.collection.objects.link(sun)
sun.data.energy, sun.data.color, sun.data.angle = 3.0, (1.0, 0.92, 0.80), math.radians(8)
sun.rotation_euler = (math.radians(50), 0, math.radians(25))
rim = bpy.data.objects.new("Rim", bpy.data.lights.new("Rim", "AREA"))
scene.collection.objects.link(rim)
rim.data.energy, rim.data.color, rim.data.size = 120, (0.75, 0.85, 1.0), 1.5
rim.location, rim.rotation_euler = (-0.8, 1.6, 1.8), (math.radians(-50), 0, math.radians(200))

aim = bpy.data.objects.new("CamAim", None)
scene.collection.objects.link(aim)
aim.location = (0, 0, 0.52)
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
scene.collection.objects.link(cam)
scene.camera = cam
cam.data.lens = 40
tt = cam.constraints.new("TRACK_TO")
tt.target, tt.track_axis, tt.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
for f in (1, FRAMES):                                     # đẩy máy vào chậm suốt clip
    k = (f - 1) / (FRAMES - 1)
    cam.location = (1.05 - 0.10 * k, -2.30 + 0.20 * k, 0.60)
    cam.keyframe_insert("location", frame=f)

# ---------------------------------------------------------------- keyframe cho Lumo
prev = {}
for f in range(1, FRAMES + 1):
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
    b = beat_of(f)
    rig["mouth_open"] = mouth(b)
    rig["blink_L"], rig["blink_R"] = blinks(b)
    for prop in ("mouth_open", "blink_L", "blink_R"):
        rig.keyframe_insert(f'["{prop}"]', frame=f)

r = scene.render
r.engine = "BLENDER_EEVEE"
r.resolution_x, r.resolution_y = 1920, 1080
scene.eevee.taa_render_samples = 32
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Punchy"
scene["stills"] = "20,40,70,100,170,200,260,290,350,375"
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND), compress=True)
print("DANCE_SAVED", OUT_BLEND, FRAMES, "frames")
