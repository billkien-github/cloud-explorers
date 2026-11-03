"""
TEST_Previz_Corridor sh010 — previz 30 giây một cú máy: người hộp đi dọc hành lang tường gạch, máy quay chạy
liên tục trên đường riêng, đổi cỡ cảnh và tiêu cự, tăng tốc rồi nhấn ở hai lần nhân vật dừng lại. Không cắt cảnh,
nhân vật luôn trong khung. Dùng làm video dẫn (video-to-video) cho model sinh video.
    .\\pipeline\\run.ps1 build -Shot 04_PRODUCTION\\TEST_Previz_Corridor\\sh010
    .\\pipeline\\run.ps1 final -Shot 04_PRODUCTION\\TEST_Previz_Corridor\\sh010     # 1920x1080, 24fps, MP4
Lưu bản sao sau mỗi giai đoạn vào backups/: stage1_corridor, stage2_hero, stage3_camera.
Màu người hộp để model đọc hướng: ĐỎ = mặt trước (hướng nhìn), ĐEN = lưng, XANH LÁ = hai bên và đỉnh.
Nhân vật đi theo +Y. Bố cục máy tính theo toạ độ tương đối với nhân vật (gốc ở chân, mặt nhìn +Y).
"""
import math
import pathlib

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = pathlib.Path(__file__).resolve().parent
OUT_BLEND = HERE / "sh010.blend"
BACKUPS = HERE / "backups"
FPS, SECONDS = 24, 30
FRAMES = FPS * SECONDS

# ---------------------------------------------------------------- kích thước hành lang (m)
HALF_W, HEIGHT = 3.5, 5.0              # rộng 7 m, cao 5 m
Y0, Y1 = -10.0, 40.0                   # tường đầu và tường cuối (cuối có cửa sáng)
RIB_STEP = 4.0                         # cột và dầm trần mỗi 4 m

# ---------------------------------------------------------------- nhân vật: tốc độ đi và hai lần dừng
WALK = 1.25                            # m/s
PAUSES = [(9.0, 11.0), (19.0, 21.0)]   # đứng yên trong khoảng này (giây)
RAMP = 0.7                             # thời gian hãm lại và đi tiếp
STRIDE = 1.4                           # m mỗi chu kỳ hai bước
LEG = 0.90                             # chiều dài chân, hông ở z = 0.92
# hướng đầu (giây, quay trái +độ, ngẩng +độ): dừng 1 quay sang phải nhìn về máy, dừng 2 ngẩng lên trần bên trái
HEAD_KEYS = [(0, 0, 0), (9.1, 0, 0), (9.7, -45, 4), (10.6, -45, 4), (11.3, 0, 0),
             (19.1, 0, 0), (19.7, 18, 32), (20.6, 18, 32), (21.3, 0, 0), (30, 0, 0)]

# ---------------------------------------------------------------- máy quay
# (giây, vị trí máy, điểm nhìn, tiêu cự mm, dừng): toạ độ tương đối với nhân vật. "dừng" = vận tốc về 0 tại khoá,
# máy hãm lại rồi tăng tốc. Hai lần nhân vật dừng: máy lao vào cận mặt (9–11 s) và bổ nhào xuống góc thấp (19–21 s).
CAM_KEYS = [
    (0.0,  (0.3, 4.6, 1.25),   (0.0, 0.0, 1.30), 24, False),   # toàn, chính diện, lùi trước mặt
    (3.5,  (0.7, 3.3, 0.85),   (0.0, 0.0, 1.35), 28, False),   # hạ thấp, áp sát dần
    (7.0,  (2.9, 1.3, 1.45),   (0.0, 0.0, 1.40), 35, False),   # vòng sang 3/4 bên phải
    (8.8,  (2.8, -0.1, 1.60),  (0.0, 0.0, 1.45), 40, True),    # trung cảnh ngang, hãm lại khi anh ta dừng
    (9.7,  (1.45, 0.75, 1.70), (0.0, 0.05, 1.72), 62, True),   # NHẤN 1: lao vào cận mặt khi anh ta quay nhìn
    (10.8, (1.30, 0.95, 1.72), (0.0, 0.05, 1.74), 66, True),   #   trôi rất chậm, giữ cận
    (13.0, (1.3, -2.6, 2.20),  (0.0, 0.3, 1.40), 32, False),   # vòng ra sau, qua vai, cao
    (16.0, (-0.9, -3.2, 3.60), (0.0, 0.6, 1.00), 24, False),   # cao sau lưng
    (18.6, (-0.3, 1.9, 4.30),  (0.0, 0.3, 0.80), 20, True),    # bay qua đầu, gần như nhìn thẳng xuống
    (19.6, (-1.9, 2.3, 0.35),  (0.0, 0.0, 1.55), 18, True),    # NHẤN 2: bổ nhào xuống sát sàn, ngước lên
    (20.8, (-1.7, 2.5, 0.40),  (0.0, 0.0, 1.60), 21, True),    #   giữ góc thấp
    (23.5, (0.4, 3.0, 0.50),   (0.0, 0.0, 1.30), 24, False),   # góc thấp chính diện, lùi theo
    (26.0, (2.5, 0.1, 1.30),   (0.0, 0.0, 1.30), 30, False),   # anh ta đi ngang qua, máy quét sang hông
    (30.0, (0.5, -4.6, 1.70),  (0.0, 2.0, 1.20), 40, True),    # bám sau lưng, chậm dần, hướng về cửa sáng
]


def ss(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def hermite(keys, t, values, hold=None):
    """Nội suy Hermite theo thời gian (C1, vận tốc liền), tiếp tuyến Catmull-Rom; khoá có hold thì vận tốc = 0."""
    ts = [k[0] for k in keys]
    i = min(len(keys) - 2, max([j for j in range(len(ts)) if ts[j] <= t], default=0))
    t0, t1 = ts[i], ts[i + 1]
    h = t1 - t0
    u = min(max((t - t0) / h, 0.0), 1.0)

    def tangent(j):
        if j == 0 or j == len(keys) - 1 or (hold and hold(keys[j])):
            return values(keys[j]) * 0
        return (values(keys[j + 1]) - values(keys[j - 1])) / (ts[j + 1] - ts[j - 1])

    p0, p1, m0, m1 = values(keys[i]), values(keys[i + 1]), tangent(i), tangent(i + 1)
    h00, h10 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u
    h01, h11 = -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
    return h00 * p0 + h10 * h * m0 + h01 * p1 + h11 * h * m1


def save_stage(name):
    BACKUPS.mkdir(exist_ok=True)
    path = BACKUPS / f"sh010_{name}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(path), compress=True, copy=True)
    print("STAGE_SAVED", path)


# ---------------------------------------------------------------- dọn scene
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, FRAMES


def material(name, color, rough=0.6):
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    return m


def emit_material(name, color, strength):
    m = bpy.data.materials.new(name)
    nt = m.node_tree
    nt.nodes.remove(nt.nodes["Principled BSDF"])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = color
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], nt.nodes["Material Output"].inputs["Surface"])
    return m


def textured_material(name, kind):
    """Vân thủ tục theo UV tính bằng mét: brick (tường), tiles (sàn), concrete (cột, trần)."""
    m = bpy.data.materials.new(name)
    nt = m.node_tree
    n, ln = nt.nodes, nt.links
    bsdf = n["Principled BSDF"]
    uv = n.new("ShaderNodeTexCoord")
    noise = n.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 3.0
    noise.inputs["Detail"].default_value = 8.0
    ln.new(uv.outputs["UV"], noise.inputs["Vector"])
    grime = n.new("ShaderNodeValToRGB")                          # vệt bẩn loang lổ
    grime.color_ramp.elements[0].position, grime.color_ramp.elements[1].position = 0.35, 0.75
    grime.color_ramp.elements[0].color = (0.55, 0.55, 0.55, 1)
    ln.new(noise.outputs["Fac"], grime.inputs["Fac"])
    mul = n.new("ShaderNodeMix")
    mul.data_type, mul.blend_type = "RGBA", "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    a = next(s for s in mul.inputs if s.name == "A" and s.type == "RGBA")
    b = next(s for s in mul.inputs if s.name == "B" and s.type == "RGBA")
    out = next(s for s in mul.outputs if s.type == "RGBA")
    ln.new(grime.outputs["Color"], b)
    ln.new(out, bsdf.inputs["Base Color"])
    if kind == "brick":
        tex = n.new("ShaderNodeTexBrick")
        tex.inputs["Scale"].default_value = 1.0
        tex.inputs["Brick Width"].default_value = 0.6
        tex.inputs["Row Height"].default_value = 0.22
        tex.inputs["Mortar Size"].default_value = 0.012
        tex.inputs["Color1"].default_value = (0.42, 0.20, 0.13, 1)
        tex.inputs["Color2"].default_value = (0.30, 0.14, 0.10, 1)
        tex.inputs["Mortar"].default_value = (0.55, 0.52, 0.48, 1)
        ln.new(uv.outputs["UV"], tex.inputs["Vector"])
        ln.new(tex.outputs["Color"], a)
        bsdf.inputs["Roughness"].default_value = 0.85
    elif kind == "tiles":
        tex = n.new("ShaderNodeTexChecker")
        tex.inputs["Scale"].default_value = 1.0
        tex.inputs["Color1"].default_value = (0.32, 0.32, 0.30, 1)
        tex.inputs["Color2"].default_value = (0.14, 0.14, 0.14, 1)
        ln.new(uv.outputs["UV"], tex.inputs["Vector"])
        ln.new(tex.outputs["Color"], a)
        bsdf.inputs["Roughness"].default_value = 0.35
    else:
        a.default_value = (0.36, 0.36, 0.37, 1)
        bsdf.inputs["Roughness"].default_value = 0.9
    return m


def add_obj(name, bm, mats, parent=None):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for m in mats:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    ob.parent = parent
    return ob


def box_bm(size, center):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0] + center[0], v.co.y * size[1] + center[1], v.co.z * size[2] + center[2]))
    return bm


def metric_uv(bm, axes):
    """UV = toạ độ mét theo hai trục (axes = (0, 1) là x, y …) để vân không bị kéo giãn."""
    uv = bm.loops.layers.uv.new()
    for f in bm.faces:
        for lp in f.loops:
            lp[uv].uv = (lp.vert.co[axes[0]], lp.vert.co[axes[1]])
    return bm


def quad(name, corners, mat, axes):
    bm = bmesh.new()
    bm.faces.new([bm.verts.new(c) for c in corners])
    return add_obj(name, metric_uv(bm, axes), [mat])


# ================================================================ GIAI ĐOẠN 1: hành lang
m_brick = textured_material("M_Brick", "brick")
m_tiles = textured_material("M_Tiles", "tiles")
m_conc = textured_material("M_Concrete", "concrete")
m_panel = emit_material("M_LightPanel", (1.0, 0.86, 0.68, 1), 6.0)
m_door = emit_material("M_DoorGlow", (0.80, 0.90, 1.0, 1), 5.0)

W, H = HALF_W, HEIGHT
quad("Floor", [(-W, Y0, 0), (W, Y0, 0), (W, Y1, 0), (-W, Y1, 0)], m_tiles, (0, 1))
quad("Ceiling", [(-W, Y0, H), (-W, Y1, H), (W, Y1, H), (W, Y0, H)], m_conc, (0, 1))
quad("Wall_L", [(-W, Y0, 0), (-W, Y1, 0), (-W, Y1, H), (-W, Y0, H)], m_brick, (1, 2))
quad("Wall_R", [(W, Y0, 0), (W, Y0, H), (W, Y1, H), (W, Y1, 0)], m_brick, (1, 2))
# hai đầu là tường có cửa 2 x 3 m: đầu vào là bóng tối (nhân vật đi ra từ đó), cuối là mảng sáng
DOOR_W, DOOR_H = 1.0, 3.0
m_void = emit_material("M_Void", (0, 0, 0, 1), 1.0)
for tag, yw, back, mat in (("Start", Y0, Y0 - 1.0, m_void), ("End", Y1, Y1 + 1.0, m_door)):
    for name, x0, x1, z0, z1 in ((f"{tag}_L", -W, -DOOR_W, 0, H), (f"{tag}_R", DOOR_W, W, 0, H),
                                 (f"{tag}_Top", -DOOR_W, DOOR_W, DOOR_H, H)):
        quad(name, [(x0, yw, z0), (x1, yw, z0), (x1, yw, z1), (x0, yw, z1)], m_brick, (0, 2))
    quad(f"{tag}_DoorFill", [(-DOOR_W, back, 0), (DOOR_W, back, 0), (DOOR_W, back, DOOR_H), (-DOOR_W, back, DOOR_H)],
         mat, (0, 2))
    for side in (-1, 1):
        quad(f"{tag}_Jamb_{side:+d}", [(side * DOOR_W, yw, 0), (side * DOOR_W, back, 0), (side * DOOR_W, back, DOOR_H),
                                       (side * DOOR_W, yw, DOOR_H)], m_conc, (1, 2))

# cột hai bên + dầm trần mỗi 4 m (khung nhịp nhàng giúp đọc tốc độ và chiều sâu), đèn trần giữa hai dầm
y = Y0 + RIB_STEP
while y < Y1:
    for side in (-1, 1):
        add_obj(f"Pillar_{side:+d}_{y:.0f}", metric_uv(box_bm((0.4, 0.5, H), (side * (W - 0.2), y, H / 2)), (1, 2)), [m_conc])
    add_obj(f"Beam_{y:.0f}", metric_uv(box_bm((2 * W, 0.5, 0.4), (0, y, H - 0.2)), (0, 1)), [m_conc])
    if y + RIB_STEP / 2 < Y1:
        quad(f"Panel_{y:.0f}", [(-0.6, y + 1.0, H - 0.01), (-0.6, y + 3.0, H - 0.01), (0.6, y + 3.0, H - 0.01),
                                (0.6, y + 1.0, H - 0.01)], m_panel, (0, 1))
    y += RIB_STEP
for k, ly in enumerate(range(int(Y0) + 6, int(Y1), 8)):
    lamp = bpy.data.objects.new(f"Lamp_{k}", bpy.data.lights.new(f"Lamp_{k}", "POINT"))
    scene.collection.objects.link(lamp)
    lamp.data.energy, lamp.data.color, lamp.data.shadow_soft_size = 450, (1.0, 0.85, 0.68), 0.6
    lamp.location = (0, ly, H - 0.6)
door_light = bpy.data.objects.new("DoorLight", bpy.data.lights.new("DoorLight", "AREA"))
scene.collection.objects.link(door_light)
door_light.data.energy, door_light.data.color, door_light.data.size = 900, (0.75, 0.88, 1.0), 2.0
door_light.location, door_light.rotation_euler = (0, Y1 + 0.5, 1.5), (math.radians(90), 0, 0)
fill = bpy.data.objects.new("Fill", bpy.data.lights.new("Fill", "SUN"))       # sáng phụ không bóng cho mặt đứng
scene.collection.objects.link(fill)
fill.data.energy, fill.data.use_shadow, fill.data.specular_factor = 0.8, False, 0.0    # không loá trên sàn bóng
fill.rotation_euler = (math.radians(70), 0, math.radians(35))

world = bpy.data.worlds.new("Dark")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.02, 0.02, 0.025, 1)
save_stage("stage1_corridor")

# ================================================================ GIAI ĐOẠN 2: người hộp đi bộ
m_front = material("M_Hero_Front_Red", (0.80, 0.04, 0.03, 1))
m_back = material("M_Hero_Back_Black", (0.015, 0.015, 0.015, 1))
m_side = material("M_Hero_Side_Green", (0.10, 0.70, 0.16, 1))


def hero_box(name, size, center, parent):
    """Hộp tô màu theo hướng: mặt +Y đỏ, -Y đen, còn lại xanh lá."""
    bm = box_bm(size, center)
    for f in bm.faces:
        f.material_index = 0 if f.normal.y > 0.5 else 1 if f.normal.y < -0.5 else 2
    return add_obj(name, bm, [m_front, m_back, m_side], parent)


hero = bpy.data.objects.new("HERO", None)
scene.collection.objects.link(hero)
torso = hero_box("Hero_Torso", (0.46, 0.28, 0.66), (0, 0, 0.33), hero)       # gốc ở hông
torso.location = (0, 0, 0.92)
head = hero_box("Hero_Head", (0.27, 0.27, 0.27), (0, 0, 0.135), torso)      # gốc ở cổ, chạm đỉnh thân
head.location = (0, 0, 0.66)
legs = []
for side in (-1, 1):
    leg = hero_box(f"Hero_Leg_{'L' if side < 0 else 'R'}", (0.17, 0.19, LEG), (0, 0, -LEG / 2), hero)
    leg.location = (side * 0.12, 0, 0.92)
    legs.append(leg)
arms = []
for side in (-1, 1):
    arm = hero_box(f"Hero_Arm_{'L' if side < 0 else 'R'}", (0.12, 0.12, 0.62), (0, 0, -0.31), torso)
    arm.location = (side * 0.30, 0, 0.62)
    arms.append(arm)
for ob in [torso, head, *legs, *arms]:
    ob.rotation_mode = "XYZ"


def speed_factor(t):
    """1 khi đi, 0 khi dừng, hãm và tăng tốc mượt (cosine) trong RAMP giây."""
    for a, b in PAUSES:
        if a - RAMP <= t < a:
            return 0.5 * (1 + math.cos(math.pi * (t - (a - RAMP)) / RAMP))
        if a <= t < b:
            return 0.0
        if b <= t < b + RAMP:
            return 0.5 * (1 - math.cos(math.pi * (t - b) / RAMP))
    return 1.0


# quãng đường theo từng khung: tích phân tốc độ với bước nhỏ
dist, d, sub = [0.0], 0.0, 10
for f in range(2, FRAMES + 1):
    for s in range(sub):
        t = (f - 2 + (s + 0.5) / sub) / FPS
        d += WALK * speed_factor(t) / (FPS * sub)
    dist.append(d)


def hero_state(f):
    """(vị trí gốc, góc chân, góc tay, quay đầu, ngẩng đầu, nghiêng thân) của khung f."""
    t = (f - 1) / FPS
    amp = speed_factor(t)
    phase = 2 * math.pi * dist[f - 1] / STRIDE
    leg = math.radians(26) * amp * math.sin(phase)
    root = Vector((0.0, dist[f - 1], -LEG * (1 - math.cos(leg))))      # chân trụ luôn chạm sàn
    yaw, pitch = hermite(HEAD_KEYS, t, lambda k: Vector(k[1:]), hold=lambda k: True)
    return root, leg, math.radians(20) * amp * math.sin(phase), math.radians(yaw), math.radians(pitch), amp


for f in range(1, FRAMES + 1):
    root, leg, arm, yaw, pitch, amp = hero_state(f)
    hero.location = root
    hero.keyframe_insert("location", frame=f)
    torso.rotation_euler = (math.radians(4) * amp, 0, 0.35 * yaw)            # hơi đổ người tới khi đi
    torso.keyframe_insert("rotation_euler", frame=f)
    head.rotation_euler = (pitch - math.radians(4) * amp, 0, 0.65 * yaw)
    head.keyframe_insert("rotation_euler", frame=f)
    for ob, sgn in zip(legs, (1, -1)):
        ob.rotation_euler = (sgn * leg, 0, 0)
        ob.keyframe_insert("rotation_euler", frame=f)
    for ob, sgn in zip(arms, (-1, 1)):
        ob.rotation_euler = (sgn * arm, 0, 0)
        ob.keyframe_insert("rotation_euler", frame=f)
save_stage("stage2_hero")

# ================================================================ GIAI ĐOẠN 3: máy quay một cú, không cắt
aim = bpy.data.objects.new("CamAim", None)
scene.collection.objects.link(aim)
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
scene.collection.objects.link(cam)
scene.camera = cam
cam.data.sensor_width = 36
cam.data.clip_start, cam.data.clip_end = 0.05, 120
tt = cam.constraints.new("TRACK_TO")
tt.target, tt.track_axis, tt.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
for f in range(1, FRAMES + 1):
    t = (f - 1) / FPS
    base = Vector((0.0, dist[f - 1], 0.0))                                   # bám theo quãng đường, bỏ nhún
    cam.location = base + hermite(CAM_KEYS, t, lambda k: Vector(k[1]), hold=lambda k: k[4])
    aim.location = base + hermite(CAM_KEYS, t, lambda k: Vector(k[2]), hold=lambda k: k[4])
    cam.data.lens = hermite(CAM_KEYS, t, lambda k: Vector((k[3], 0)), hold=lambda k: k[4])[0]
    cam.keyframe_insert("location", frame=f)
    aim.keyframe_insert("location", frame=f)
    cam.data.keyframe_insert("lens", frame=f)

r = scene.render
r.engine = "BLENDER_EEVEE"
r.resolution_x, r.resolution_y = 1920, 1080
scene.eevee.taa_render_samples = 32
scene.view_settings.view_transform = "AgX"
scene["stills"] = "1,84,190,234,300,384,447,470,560,624,720"

# ---------------------------------------------------------------- kiểm tra: máy trong hành lang, đầu luôn trong khung
# (ngực được phép ra khỏi khung ở cảnh cận mặt, chỉ báo để biết)
problems = {}
for f in range(1, FRAMES + 1):
    scene.frame_set(f)
    c = cam.matrix_world.translation
    if not (-W + 0.25 < c.x < W - 0.25 and Y0 + 0.3 < c.y < Y1 - 0.3 and 0.2 < c.z < H - 0.5):
        problems.setdefault("LỖI máy ngoài hành lang", []).append(f)
    if (c - head.matrix_world.translation).length < 0.8:
        problems.setdefault("LỖI máy sát người", []).append(f)
    for label, ob, local in (("LỖI đầu", head, Vector((0, 0, 0.135))),("ngực", torso, Vector((0, 0, 0.45)))):
        p = world_to_camera_view(scene, cam, ob.matrix_world @ local)
        if not (0.05 < p.x < 0.95 and 0.05 < p.y < 0.95 and p.z > 0.5):
            problems.setdefault(f"{label} ra khỏi khung", []).append(f)
for label, fs in problems.items():
    print("PREVIZ_CHECK", label, f"{len(fs)} khung, từ {fs[0]} đến {fs[-1]}")
if not any(k.startswith("LỖI") for k in problems):
    print("PREVIZ_CHECK OK")

scene.frame_set(1)
save_stage("stage3_camera")
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND), compress=True)
print("PREVIZ_SAVED", OUT_BLEND, FRAMES, "frames", "hero đi", round(dist[-1], 2), "m")
