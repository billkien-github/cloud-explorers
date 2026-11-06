"""
Bộ khối 3D cho previz dẫn Seedance (quy ước: 04_PRODUCTION/SEEDANCE.md, mục Previz).
- Hình khối, vật liệu, thêm object vào collection.
- Bốn nhân vật dạng khối đúng tỉ lệ Character Bible, màu nhận diện: Lumo cam, Tavi xanh lá, Nori tím nhạt, Piko xanh
  ngọc; ô trắng trước đầu = hướng mặt. Mặt trước của mọi khối là -Y cục bộ. Hướng (yaw): 0 = nhìn -Y (về phía máy
  quay đặt ở -Y), 90 = nhìn +X, 180 = nhìn +Y, 270 = nhìn -X. Nghiêng (X) dương = chồm về phía trước mặt.
- Keyframe theo giây: fr(t) = khung của t trong cảnh - khung của T0 + 1, T0 = giây trong cảnh của khung 1 (đoạn cắt ra
  từ một cảnh dài).
- Máy quay theo SHOTS (mỗi shot một camera, cắt bằng timeline marker), kiểm tra nhân vật trong khung, cài đặt render.
Dùng: blocks.start(fps, seconds, offset), dựng bối cảnh, gọi build_lumo()…, diễn bằng key/rot, cameras(), finish().
"""
import math

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Matrix, Vector

FPS, T0 = 24, 0.0
COLS = {}


def start(fps, seconds, offset=0.0, collections=("SET", "PROPS", "CAST", "CAMERAS")):
    """Scene trống, khung 1 = giây offset của cảnh, dài seconds giây."""
    global FPS, T0
    bpy.ops.wm.read_factory_settings(use_empty=True)
    FPS, T0 = fps, offset
    scene = bpy.context.scene
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, round(seconds * fps)
    COLS.clear()
    for name in collections:
        COLS[name] = bpy.data.collections.new(name)
        scene.collection.children.link(COLS[name])
    return scene


def fr(t):
    """Khung của giây t trong cảnh. Làm tròn theo khung của cả cảnh để các đoạn cắt từ một cảnh có key trùng khung."""
    return round(t * FPS) - round(T0 * FPS) + 1


def ss(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def key(target, path, t, value):
    setattr(target, path, value)
    target.keyframe_insert(path, frame=fr(t))


def keys(target, path, pts):
    for t, v in pts:
        key(target, path, t, v)


def rot(ob, pts):
    """pts = [(giây, (x, y, z) độ)]."""
    for t, d in pts:
        key(ob, "rotation_euler", t, tuple(math.radians(a) for a in d))


def material(name, color, rough=0.6, emit=None):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = rough
    if emit:
        bsdf.inputs["Emission Color"].default_value = (*emit[0], 1)
        bsdf.inputs["Emission Strength"].default_value = emit[1]
    return m


def bsdf_in(m, name):
    return m.node_tree.nodes["Principled BSDF"].inputs[name]


def add_obj(name, bm, mat, col, parent=None, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me)
    COLS[col].objects.link(ob)
    ob.parent = parent
    ob.location = loc
    ob.rotation_mode = "XYZ"
    return ob


def empty(name, col, parent=None, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, None)
    COLS[col].objects.link(ob)
    ob.parent = parent
    ob.location = loc
    ob.rotation_mode = "XYZ"
    return ob


def box_bm(size, center=(0, 0, 0), bm=None):
    bm = bm or bmesh.new()
    res = bmesh.ops.create_cube(bm, size=1.0)
    for v in res["verts"]:
        v.co = Vector((v.co.x * size[0] + center[0], v.co.y * size[1] + center[1], v.co.z * size[2] + center[2]))
    return bm


def sphere_bm(radius, center=(0, 0, 0), scale=(1, 1, 1), bm=None, segs=24):
    bm = bm or bmesh.new()
    mat = Matrix.Translation(center) @ Matrix.Diagonal((*scale, 1))
    res = bmesh.ops.create_uvsphere(bm, u_segments=segs, v_segments=segs // 2, radius=radius, matrix=mat)
    for v in res["verts"]:
        for f in v.link_faces:
            f.smooth = True
    return bm


def cyl_bm(radius, depth, center=(0, 0, 0), axis="Z", bm=None, cone_top=None, segs=20):
    """Trụ (hoặc nón nếu cone_top là bán kính đỉnh) theo trục axis, tâm ở center."""
    bm = bm or bmesh.new()
    rotm = {"Z": Matrix.Identity(4), "Y": Matrix.Rotation(math.radians(90), 4, "X"),
            "X": Matrix.Rotation(math.radians(90), 4, "Y")}[axis]
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=radius,
                          radius2=radius if cone_top is None else cone_top, depth=depth,
                          matrix=Matrix.Translation(center) @ rotm)
    return bm


# ================================================================ bốn nhân vật dạng khối
def cast_materials():
    return {
        "lumo": material("M_Lumo_Orange", (0.95, 0.30, 0.03)),
        "tavi": material("M_Tavi_Green", (0.20, 0.40, 0.08)),
        "pack": material("M_Tavi_Pack", (0.25, 0.18, 0.12)),
        "nori": material("M_Nori_Lavender", (0.42, 0.26, 0.95), emit=((0.55, 0.40, 1.0), 0.3)),
        "wing": material("M_Nori_Wing", (0.75, 0.62, 1.0), 0.4),
        "star": material("M_Nori_Star", (1.0, 0.95, 0.45), 0.4, emit=((1.0, 0.92, 0.4), 0.0)),
        "piko": material("M_Piko_Aqua", (0.03, 0.70, 0.98), 0.25),
        "horn": material("M_Piko_Horn", (0.02, 0.10, 0.45), 0.4),
        "face": material("M_FaceMarker_White", (0.95, 0.95, 0.95), 0.5),
        "dark": material("M_Dark", (0.08, 0.08, 0.09), 0.5),
    }


def face_marker(name, parent, width, height, y, z):
    return add_obj(name, box_bm((width, 0.012, height), (0, y - 0.006, z)), cast_materials()["face"], "CAST", parent=parent)


class Rig:
    pass


def build_lumo(loc):
    """Tỉ lệ khối Lumo: hông 0.29–0.32, vai 0.55, cổ 0.58–0.63, đỉnh đầu 0.90, chóp tai 1.09, tay vai–cổ tay 0.22 (Character Bible), khối tay 0.29 gồm cả bàn tay."""
    m = cast_materials()["lumo"]
    r = Rig()
    r.root = empty("LUMO", "CAST", loc=loc)
    add_obj("Lumo_Body", box_bm((0.36, 0.30, 0.30), (0, 0, 0.43)), m, "CAST", parent=r.root)
    r.head = add_obj("Lumo_Head", box_bm((0.16, 0.10, 0.10), (0, -0.21, 0.09), bm=box_bm((0.42, 0.36, 0.32), (0, 0, 0.16))),
                     m, "CAST", parent=r.root, loc=(0, 0, 0.58))
    face_marker("Lumo_Face", r.head, 0.30, 0.12, -0.18, 0.21)
    r.ears = []
    for side in (-1, 1):
        ear = add_obj(f"Lumo_Ear_{'L' if side > 0 else 'R'}", box_bm((0.11, 0.04, 0.24), (0, 0, 0.12)), m, "CAST",
                      parent=r.head, loc=(side * 0.13, 0.02, 0.28))
        r.ears.append((ear, side))
    r.arm_l = add_obj("Lumo_Arm_L", box_bm((0.08, 0.08, 0.29), (0, 0, -0.145)), m, "CAST", parent=r.root, loc=(0.20, 0, 0.55))
    r.arm_r = add_obj("Lumo_Arm_R", box_bm((0.08, 0.08, 0.29), (0, 0, -0.145)), m, "CAST", parent=r.root, loc=(-0.20, 0, 0.55))
    r.legs = [add_obj(f"Lumo_Leg_{s}", box_bm((0.11, 0.13, 0.29), (0, 0, -0.145)), m, "CAST", parent=r.root,
                      loc=(x, 0, 0.29)) for s, x in (("L", 0.09), ("R", -0.09))]
    r.tail = add_obj("Lumo_Tail", box_bm((0.11, 0.30, 0.11), (0, 0.15, 0)), m, "CAST", parent=r.root, loc=(0, 0.14, 0.27))
    return r


def build_tavi(loc):
    """Cao 0.85: chân ngắn, đuôi dài kéo sát đất, Inventor Pack sau lưng, kính bảo hộ trên trán."""
    mats = cast_materials()
    m = mats["tavi"]
    r = Rig()
    r.root = empty("TAVI", "CAST", loc=loc)
    add_obj("Tavi_Body", box_bm((0.32, 0.28, 0.30), (0, 0, 0.33)), m, "CAST", parent=r.root)
    r.pack = add_obj("Tavi_Pack", box_bm((0.26, 0.12, 0.24), (0, 0.20, 0.36)), mats["pack"], "CAST", parent=r.root)
    r.head = add_obj("Tavi_Head", box_bm((0.36, 0.32, 0.30), (0, 0, 0.15)), m, "CAST", parent=r.root, loc=(0, 0, 0.48))
    face_marker("Tavi_Face", r.head, 0.26, 0.10, -0.16, 0.12)
    add_obj("Tavi_Goggles", box_bm((0.30, 0.06, 0.06), (0, -0.10, 0.33)), mats["dark"], "CAST", parent=r.head)
    r.arm_l = add_obj("Tavi_Arm_L", box_bm((0.07, 0.07, 0.26), (0, 0, -0.13)), m, "CAST", parent=r.root, loc=(0.195, 0, 0.45))
    r.arm_r = add_obj("Tavi_Arm_R", box_bm((0.07, 0.07, 0.26), (0, 0, -0.13)), m, "CAST", parent=r.root, loc=(-0.195, 0, 0.45))
    r.legs = [add_obj(f"Tavi_Leg_{s}", box_bm((0.10, 0.12, 0.18), (0, 0, -0.09)), m, "CAST", parent=r.root,
                      loc=(x, 0, 0.18)) for s, x in (("L", 0.08), ("R", -0.08))]
    r.tail = add_obj("Tavi_Tail", box_bm((0.10, 0.42, 0.10), (0, 0.21, 0)), m, "CAST", parent=r.root, loc=(0, 0.13, 0.16))
    return r


def build_nori(loc):
    """Cao 0.70, bay: thân tròn liền đầu, 2 râu sao, 4 cánh, vệt sáng thay chân. Gốc ở tâm thân."""
    mats = cast_materials()
    m = mats["nori"]
    r = Rig()
    r.root = empty("NORI", "CAST", loc=loc)
    add_obj("Nori_Body", sphere_bm(0.24), m, "CAST", parent=r.root)
    add_obj("Nori_Trail", cyl_bm(0.0, 0.16, (0, 0, -0.30), cone_top=0.09), m, "CAST", parent=r.root)
    face_marker("Nori_Face", r.root, 0.22, 0.10, -0.235, 0.03)
    r.arms = []
    for side in (-1, 1):
        add_obj(f"Nori_Antenna_{side:+d}", box_bm((0.02, 0.02, 0.16), (side * 0.10, 0, 0.29)), m, "CAST", parent=r.root)
        add_obj(f"Nori_Star_{side:+d}", sphere_bm(0.045, (side * 0.10, 0, 0.39), segs=12), mats["star"], "CAST", parent=r.root)
        arm = empty(f"Nori_ArmPivot_{side:+d}", "CAST", parent=r.root, loc=(side * 0.22, -0.04, -0.04))
        add_obj(f"Nori_Arm_{side:+d}", sphere_bm(0.045, (0, 0, -0.03), segs=12), m, "CAST", parent=arm)
        r.arms.append(arm)
    r.wings = []
    for sx in (-1, 1):
        for sz, zz in ((1, 0.10), (-1, -0.06)):
            w = add_obj(f"Nori_Wing_{sx:+d}{sz:+d}", box_bm((0.20, 0.015, 0.13 if sz > 0 else 0.10), (sx * 0.10, 0, 0)),
                        mats["wing"], "CAST", parent=r.root, loc=(sx * 0.12, 0.14, zz))
            r.wings.append((w, sx, sz))
    return r


def build_piko(loc):
    """Cao 0.80, không chân: khối thạch rộng đáy, 2 sừng, tay nhỏ. squash = điểm co giãn ở đáy."""
    mats = cast_materials()
    m = mats["piko"]
    r = Rig()
    r.root = empty("PIKO", "CAST", loc=loc)
    r.squash = empty("Piko_Squash", "CAST", parent=r.root)
    add_obj("Piko_Body", sphere_bm(0.36, (0, 0, 0.35), (1.05, 0.95, 0.97)), m, "CAST", parent=r.squash)
    face_marker("Piko_Face", r.squash, 0.26, 0.12, -0.335, 0.46)
    r.arms = []
    for side in (-1, 1):
        add_obj(f"Piko_Horn_{side:+d}", cyl_bm(0.05, 0.13, (side * 0.13, 0, 0.73), cone_top=0.0), mats["horn"], "CAST",
                parent=r.squash)
        arm = empty(f"Piko_ArmPivot_{side:+d}", "CAST", parent=r.squash, loc=(side * 0.36, -0.05, 0.34))
        add_obj(f"Piko_Arm_{side:+d}", sphere_bm(0.06, (0, 0, -0.04), segs=12), m, "CAST", parent=arm)
        r.arms.append(arm)
    return r


# ================================================================ diễn: vài động tác dùng chung
def wag(ob, t0, t1, period, amp, base=(0, 0, 0), axis=2):
    t, s = t0, 1
    while t < t1:
        d = list(base)
        d[axis] += s * amp
        rot(ob, [(t, d)])
        t += period / 2
        s = -s
    rot(ob, [(t1, base)])


def steps(legs, t0, t1, n, amp=25):
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        a = 0 if i == n else amp * (1 if i % 2 else -1)
        rot(legs[0], [(t, (a, 0, 0))])
        rot(legs[1], [(t, (-a, 0, 0))])


# ================================================================ máy quay, kiểm tra khung, render
def cameras(shots, cams, sensor=36):
    """cams[tên] = [(giây, vị trí máy, điểm nhìn, tiêu cự mm)]; mỗi shot một camera, cắt bằng marker."""
    scene = bpy.context.scene
    out = {}
    for name, t0, t1 in shots:
        cam = bpy.data.objects.new(f"Cam_{name}", bpy.data.cameras.new(f"Cam_{name}"))
        COLS["CAMERAS"].objects.link(cam)
        aim = empty(f"Aim_{name}", "CAMERAS")
        cam.data.sensor_width = sensor
        cam.data.clip_start, cam.data.clip_end = 0.02, 200
        tt = cam.constraints.new("TRACK_TO")
        tt.target, tt.track_axis, tt.up_axis = aim, "TRACK_NEGATIVE_Z", "UP_Y"
        for t, loc, target, lens in cams[name]:
            key(cam, "location", t, Vector(loc))
            key(aim, "location", t, Vector(target))
            key(cam.data, "lens", t, lens)
        scene.timeline_markers.new(name, frame=fr(t0)).camera = cam
        out[name] = cam
    scene.camera = out[shots[0][0]]
    return out


def check_in_frame(shots, cams, must_see, extra=()):
    """must_see[shot] = [(object, điểm cục bộ)]; extra = [(shot, object, từ giây, tới giây)]. In PREVIZ_CHECK."""
    scene = bpy.context.scene
    problems = {}
    for name, t0, t1 in shots:
        cam = cams[name]
        for f in range(fr(t0), fr(t1)):
            scene.frame_set(f)
            t = (f - 1 + round(T0 * FPS)) / FPS
            checks = list(must_see.get(name, [])) + [(ob, Vector()) for s, ob, a, b in extra if s == name and a <= t < b]
            for ob, local in checks:
                p = world_to_camera_view(scene, cam, ob.matrix_world @ local)
                if not (0.03 < p.x < 0.97 and 0.03 < p.y < 0.97 and p.z > 0.05):
                    problems.setdefault(f"{name}: {ob.name} ra khỏi khung", []).append(f)
            if cam.matrix_world.translation.z < 0.05:
                problems.setdefault(f"{name}: máy dưới đất", []).append(f)
    for label, fs in problems.items():
        print("PREVIZ_CHECK", label, f"{len(fs)} khung, từ {fs[0]} đến {fs[-1]}")
    if not problems:
        print("PREVIZ_CHECK OK")
    scene.frame_set(1)
    return problems


def finish(out_blend, stills=(), samples=32):
    """EEVEE 1920x1080, giữ màu khối rực (Standard), lưu .blend. stills: các giây để run.ps1 stills render mẫu."""
    scene = bpy.context.scene
    r = scene.render
    r.engine = "BLENDER_EEVEE"
    r.resolution_x, r.resolution_y = 1920, 1080
    scene.eevee.taa_render_samples = samples
    scene.view_settings.view_transform = "Standard"
    if stills:
        scene["stills"] = ",".join(str(fr(t)) for t in stills)
    bpy.ops.wm.save_as_mainfile(filepath=str(out_blend), compress=True)
    print("PREVIZ_SAVED", out_blend, scene.frame_end, "frames")
