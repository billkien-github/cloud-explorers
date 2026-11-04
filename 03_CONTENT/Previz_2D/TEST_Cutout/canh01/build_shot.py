"""
TEST_Cutout canh01: thử bộ nhân vật cutout 2D (03_CONTENT/PREVIZ_2D.md) trên khoảnh khắc Cảnh 3 tập 01
(beat sheet: 03_CONTENT/Scripts/EP001_great_rain_experiment.md). Lumo vội với tay về nút đỏ, khựng lại; Piko bị nút
lấp lánh hút mắt, nhảy lên lưng Lumo, tay Lumo đè xuống nút. Mốc thời gian và CC: timing.py.
    .\\pipeline\\run.ps1 build -Shot 03_CONTENT\\Previz_2D\\TEST_Cutout\\canh01
    .\\pipeline\\run.ps1 preview -Shot 03_CONTENT\\Previz_2D\\TEST_Cutout\\canh01
    blender -b --factory-startup -P pipeline\\cc.py -- <cảnh>\\renders\\canh01_preview.mp4 <cảnh>\\timing.py <cảnh>\\renders\\canh01_preview_cc.mp4
Toạ độ: hình nằm trên mặt phẳng XZ (X sang phải, Z lên, mét), máy quay orthographic nhìn theo +Y, Y nhỏ hơn là lớp ở
trước. Mỗi nhân vật dựng quay mặt về +X; root.scale.x = -1 là quay sang trái. Xoay quanh Y: góc dương ngả về phía
trước mặt (tai ngả tới, đầu cúi, đuôi vểnh lên); tay buông là 0°, đưa thẳng ra trước là -90°, giơ cao là -150°.
Render bằng Workbench, màu phẳng: gần như tức thì.
"""
import math
import pathlib
import sys
from types import SimpleNamespace

import bmesh
import bpy

HERE = pathlib.Path(__file__).resolve().parent
sys.dont_write_bytecode = True                                  # không để __pycache__ cạnh timing.py
sys.path.insert(0, str(HERE))
from timing import *  # noqa: E402,F403  FPS, SECONDS, SHOTS, mốc hành động, CC của cảnh

OUT_BLEND = HERE / f"{HERE.name}.blend"
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene


# ================================================================ keyframe
def fr(t):
    return round(t * FPS) + 1


def key(target, path, t, value):
    setattr(target, path, value)
    target.keyframe_insert(path, frame=fr(t))


def ry(ob, t, deg):
    """Xoay quanh Y, độ."""
    key(ob, "rotation_euler", t, (0.0, math.radians(deg), 0.0))


def at(ob, t, x, z):
    key(ob, "location", t, (x, ob.location.y, z))


def lean(p, t, deg):
    """Nghiêng cả người quanh bàn chân; deg dương là chồm về phía trước mặt. Scale -1 của root áp trước phép xoay
    của chính nó, nên góc của root phải đổi dấu theo hướng mặt p.dir (1 quay phải, -1 quay trái)."""
    ry(p.root, t, deg * p.dir)


def scl(ob, t, sx, sz):
    key(ob, "scale", t, (sx, 1.0, sz))


def show(ob, t, on):
    for path in ("hide_render", "hide_viewport"):
        key(ob, path, t, not on)


def loop(ob, t0, t1, period, a, b):
    """Lắc qua lại giữa góc a và b (đuôi, cánh)."""
    t, flip = t0, False
    while t <= t1 + 1e-6:
        ry(ob, t, b if flip else a)
        t, flip = t + period / 2, not flip


# ================================================================ hình cutout
MATS = {}


def mat(hexcol, unique=None):
    """Màu phẳng từ mã sRGB (Workbench lấy diffuse_color, tuyến tính)."""
    name = unique or hexcol
    if name not in MATS:
        c = [int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        m = bpy.data.materials.new(name)
        m.diffuse_color = (*[x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c], 1.0)
        MATS[name] = m
    return MATS[name]


def ell(rx, rz, cx=0.0, cz=0.0, a0=0.0, a1=360.0, n=36):
    if a1 - a0 >= 360:
        return [(cx + rx * math.cos(2 * math.pi * i / n), cz + rz * math.sin(2 * math.pi * i / n)) for i in range(n)]
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cz + rz * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def arc(r, a0, a1, th, cx=0.0, cz=0.0, n=16):
    """Vệt cong dày th (miệng, mắt nhắm)."""
    angs = [math.radians(a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    return ([(cx + (r + th / 2) * math.cos(a), cz + (r + th / 2) * math.sin(a)) for a in angs]
            + [(cx + (r - th / 2) * math.cos(a), cz + (r - th / 2) * math.sin(a)) for a in reversed(angs)])


def rrect(w, h, r, cx=0.0, cz=0.0, n=6):
    pts = []
    for qx, qz, a in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90),
                      (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        pts += [(cx + qx + r * math.cos(math.radians(a + 90 * i / n)),
                 cz + qz + r * math.sin(math.radians(a + 90 * i / n))) for i in range(n + 1)]
    return pts


def star(r, cx=0.0, cz=0.0, k=5, inner=0.45):
    return [(cx + (r if i % 2 == 0 else r * inner) * math.cos(math.pi / 2 + math.pi * i / k),
             cz + (r if i % 2 == 0 else r * inner) * math.sin(math.pi / 2 + math.pi * i / k)) for i in range(2 * k)]


def turn(pts, deg, cx=0.0, cz=0.0):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(cx + (x - cx) * c - (z - cz) * s, cz + (x - cx) * s + (z - cz) * c) for x, z in pts]


def node(name, parent, loc=(0.0, 0.0), y=0.0):
    ob = bpy.data.objects.new(name, None)
    scene.collection.objects.link(ob)
    ob.parent, ob.location, ob.empty_display_size = parent, (loc[0], y, loc[1]), 0.05
    return ob


def part(name, parent, shapes, y=0.0, loc=(0.0, 0.0), unique=None):
    """Một mảnh cutout, gốc (khớp xoay) ở loc. shapes = [(điểm, màu)]: hình sau đè hình trước."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for i, (pts, col) in enumerate(shapes):
        m = mat(col, unique)
        if m not in list(me.materials):
            me.materials.append(m)
        f = bm.faces.new([bm.verts.new((x, -0.0005 * i, z)) for x, z in pts])
        f.material_index = list(me.materials).index(m)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    ob.parent, ob.location = parent, (loc[0], y, loc[1])
    return ob


# ================================================================ mặt dùng chung
DARK, MOUTH_IN, TONGUE, WHITE = "#2B1B14", "#5A1E24", "#E8707E", "#FFFFFF"
# biểu cảm: (mắt, miệng, góc lông mày; âm = đầu lông mày phía trước nhướng lên, kiểu lo lắng)
FACES = {
    "neutral": ("open", "closed", 0), "eager": ("wide", "smile", 10), "happy": ("happy", "smile", 0),
    "worried": ("wide", "frown", -24), "shock": ("wide", "o", -12), "sad": ("open", "frown", -16),
    "shout": ("wide", "open", 20),
}


def add_face(p, head, eye, eye_r, iris, mouth, s=1.0, brow=DARK):
    rx, rz = eye_r
    e = node(f"{p.name}_Eye", head, eye, -0.012)
    p.eyes = {
        "open": part(f"{p.name}_EyeOpen", e, [(ell(rx, rz), iris), (ell(rx * 0.32, rz * 0.3, rx * 0.3, rz * 0.35), WHITE)]),
        "wide": part(f"{p.name}_EyeWide", e, [(ell(rx * 1.45, rz * 1.35), WHITE), (ell(rx * 1.05, rz * 1.05, rx * 0.15), iris),
                                              (ell(rx * 0.32, rz * 0.3, rx * 0.45, rz * 0.4), WHITE)]),
        "closed": part(f"{p.name}_EyeClosed", e, [(rrect(rx * 2.2, rz * 0.35, rz * 0.15), DARK)]),
        "happy": part(f"{p.name}_EyeHappy", e, [(arc(rx * 0.9, 20, 160, rz * 0.35, 0, -rz * 0.3), DARK)]),
    }
    p.brow = part(f"{p.name}_Brow", head, [(rrect(rx * 2.2, rz * 0.32, rz * 0.15), brow)], -0.013,
                  (eye[0], eye[1] + rz * 1.7))
    m = node(f"{p.name}_Mouth", head, mouth, -0.014)
    p.mouths = {
        "closed": part(f"{p.name}_MouthClosed", m, [(arc(0.03 * s, 205, 335, 0.008 * s), DARK)]),
        "smile": part(f"{p.name}_MouthSmile", m, [(arc(0.04 * s, 200, 340, 0.012 * s, 0, 0.01 * s), DARK)]),
        "open": part(f"{p.name}_MouthOpen", m, [(ell(0.028 * s, 0.034 * s), MOUTH_IN),
                                                (ell(0.018 * s, 0.012 * s, 0, -0.018 * s), TONGUE)]),
        "o": part(f"{p.name}_MouthO", m, [(ell(0.016 * s, 0.02 * s), MOUTH_IN)]),
        "frown": part(f"{p.name}_MouthFrown", m, [(arc(0.03 * s, 25, 155, 0.009 * s, 0, -0.028 * s), DARK)]),
    }


def face(p, t, name):
    eyes, mouth, brow = FACES[name]
    for k, ob in p.eyes.items():
        show(ob, t, k == eyes)
    for k, ob in p.mouths.items():
        show(ob, t, k == mouth)
    ry(p.brow, t, brow)


def blink(p, t, back="open"):
    for k, ob in p.eyes.items():
        show(ob, t, k == "closed")
        show(ob, t + 0.1, k == back)


def talk(p, t0, t1, rest="closed"):
    t, on = t0, True
    while t < t1:
        for k, ob in p.mouths.items():
            show(ob, t, k == ("open" if on else rest))
        t, on = t + 0.12, not on
    for k, ob in p.mouths.items():
        show(ob, t1, k == rest)


# ================================================================ bốn nhân vật (màu, chiều cao: Character Bible)
def build_lumo(x, layer):
    fur, shade, cream, cape, pink, brown = "#FD8A2B", "#E07722", "#FEECCF", "#FC6640", "#F4A6B0", "#8A5A35"
    p = SimpleNamespace(name="Lumo")
    p.root = node("Lumo", None, (x, 0.0), layer)
    p.tail = part("Lumo_Tail", p.root, [(ell(0.15, 0.07, -0.13, 0.05), fur), (ell(0.06, 0.05, -0.25, 0.08), cream)],
                  0.03, (-0.11, 0.2))
    p.arm_far = part("Lumo_ArmFar", p.root, [(rrect(0.065, 0.2, 0.03, 0, -0.1), shade), (ell(0.04, 0.035, 0, -0.21), cream)],
                     0.025, (-0.01, 0.46))
    part("Lumo_Cape", p.root, [([(0.0, 0.48), (-0.19, 0.42), (-0.22, 0.16), (-0.02, 0.2)], cape)], 0.015)
    part("Lumo_Legs", p.root, [(rrect(0.07, 0.14, 0.03, -0.05, 0.08), shade), (rrect(0.07, 0.14, 0.03, 0.05, 0.08), fur),
                               (ell(0.06, 0.035, -0.03, 0.02), cream), (ell(0.06, 0.035, 0.07, 0.02), cream)], 0.005)
    part("Lumo_Body", p.root, [(ell(0.15, 0.2, 0, 0.3), fur), (ell(0.09, 0.14, 0.05, 0.29), cream)])
    part("Lumo_Bag", p.root, [([(-0.06, 0.44), (0.1, 0.24), (0.11, 0.26), (-0.05, 0.46)], brown),
                              (rrect(0.08, 0.07, 0.015, 0.1, 0.2), brown)], -0.008)
    p.head = node("Lumo_Head", p.root, (0.02, 0.5), -0.01)                    # khớp cổ; đỉnh đầu ở 0.90
    tri, inner = [(-0.07, 0.0), (0.07, 0.0), (0.0, 0.26)], [(-0.04, 0.03), (0.04, 0.03), (0.0, 0.2)]
    p.ear_far = part("Lumo_EarFar", p.head, [(tri, shade), (inner, pink)], 0.02, (-0.07, 0.33))
    part("Lumo_Skull", p.head, [(ell(0.2, 0.2, 0, 0.2), fur), (ell(0.06, 0.05, -0.02, 0.39), WHITE),
                                (ell(0.11, 0.08, 0.14, 0.12), cream), (ell(0.03, 0.025, 0.245, 0.15), DARK)])
    p.ear_near = part("Lumo_EarNear", p.head, [(tri, fur), (inner, pink)], -0.005, (0.02, 0.33))  # chóp tai ở 1.09
    add_face(p, p.head, (0.09, 0.24), (0.04, 0.055), "#5A3218", (0.17, 0.07))
    p.arm = part("Lumo_ArmNear", p.root, [(rrect(0.065, 0.2, 0.03, 0, -0.1), fur), (ell(0.04, 0.035, 0, -0.21), cream)],
                 -0.02, (0.03, 0.46))                                          # vai tới cổ tay 0.22
    return p


def build_tavi(x, layer):
    green, shade, snout, crystal, cap, vest = "#7EA258", "#6B8E4A", "#93B86C", "#14F5F4", "#7A4A2A", "#EFE2C4"
    p = SimpleNamespace(name="Tavi")
    p.root = node("Tavi", None, (x, 0.0), layer)
    p.tail = part("Tavi_Tail", p.root, [([(0.0, 0.06), (-0.36, -0.12), (-0.37, -0.15), (0.0, -0.04)], green)], 0.03, (-0.07, 0.16))
    part("Tavi_Pack", p.root, [(rrect(0.12, 0.2, 0.03, -0.15, 0.32), "#8A6A45"), (ell(0.025, 0.025, -0.15, 0.38), crystal)], 0.025)
    p.arm_far = part("Tavi_ArmFar", p.root, [(rrect(0.06, 0.17, 0.028, 0, -0.085), shade), (ell(0.035, 0.03, 0, -0.18), shade)],
                     0.02, (-0.01, 0.36))
    part("Tavi_Spikes", p.root, [([(bx, bz + 0.035), (bx - 0.08, bz + 0.01), (bx, bz - 0.035)], crystal)
                                 for bx, bz in ((-0.11, 0.42), (-0.14, 0.32), (-0.13, 0.22))], 0.015)
    part("Tavi_Legs", p.root, [(rrect(0.08, 0.11, 0.035, -0.04, 0.06), shade), (rrect(0.08, 0.11, 0.035, 0.05, 0.06), green)], 0.005)
    part("Tavi_Body", p.root, [(ell(0.14, 0.17, 0, 0.26), green), (rrect(0.2, 0.16, 0.04, -0.01, 0.3), vest),
                               (rrect(0.23, 0.03, 0.01, 0.0, 0.21), cap)])
    p.head = node("Tavi_Head", p.root, (0.03, 0.42), -0.01)                   # đỉnh mũ ở khoảng 0.82
    part("Tavi_Skull", p.head, [(ell(0.17, 0.16, 0.02, 0.17), green), (ell(0.1, 0.07, 0.15, 0.1), snout),
                                (ell(0.18, 0.1, 0.0, 0.26, 0, 180), cap),
                                (ell(0.045, 0.04, -0.04, 0.34), "#5A5A5A"), (ell(0.032, 0.028, -0.04, 0.34), "#7FD6E6"),
                                (ell(0.045, 0.04, 0.06, 0.33), "#5A5A5A"), (ell(0.032, 0.028, 0.06, 0.33), "#7FD6E6")])
    add_face(p, p.head, (0.11, 0.2), (0.035, 0.045), "#3D7A2E", (0.17, 0.05), 0.9)
    p.arm = part("Tavi_ArmNear", p.root, [(rrect(0.06, 0.17, 0.028, 0, -0.085), green), (ell(0.035, 0.03, 0, -0.18), green)],
                 -0.02, (0.03, 0.36))
    return p


def build_nori(x, z, layer):
    body, wing, star_c = "#A787F6", "#D3ABFC", "#FEF7A0"
    p = SimpleNamespace(name="Nori")
    p.root = node("Nori", None, (x, z), layer)                                # gốc ở tâm thân; bay, không chân
    part("Nori_Glow", p.root, [(ell(0.27, 0.27), "#DCCFFF")], 0.04)
    p.wings = [part(f"Nori_Wing{i}", p.root, [(turn(ell(0.17, 0.08, -0.15, 0.1), 25), col), (turn(ell(0.12, 0.06, -0.13, -0.05), -20), col)],
                    y, (-0.05, 0.04)) for i, (col, y) in enumerate((("#C49BF0", 0.035), (wing, 0.03)))]
    part("Nori_Trail", p.root, [([(-0.08, -0.12), (0.08, -0.12), (0.0, -0.42)], "#E6D9FF")], 0.01)   # vệt sáng thay chân
    p.antennae = [part(f"Nori_Antenna{i}", p.root, [(rrect(0.015, 0.16, 0.007, 0, 0.08), "#8E6FE0"), (star(0.045, 0, 0.17), star_c)],
                       y, (dx, 0.17)) for i, (dx, y) in enumerate(((-0.05, 0.02), (0.04, -0.016)))]
    part("Nori_Body", p.root, [(ell(0.2, 0.2), body), (ell(0.1, 0.06, -0.07, 0.09), "#BCA6F9")])
    p.head = node("Nori_Face", p.root, (0.0, 0.0), 0.0)
    add_face(p, p.head, (0.08, 0.04), (0.04, 0.055), "#5B3FA8", (0.13, -0.06), 0.9, "#6D52C2")
    p.arm = part("Nori_Arm", p.root, [(ell(0.03, 0.045, 0, -0.04), "#9A78F0")], -0.02, (0.09, -0.06))
    return p


def build_piko(x, layer):
    body, horn, drop = "#3BDCFD", "#1F5FB4", "#9BEBFF"
    p = SimpleNamespace(name="Piko")
    p.root = node("Piko", None, (x, 0.0), layer)                              # không chân, chỉ nảy và co giãn
    blob = []
    for i in range(48):
        a = 2 * math.pi * i / 48
        bx, bz = 0.25 * math.cos(a), 0.34 + 0.34 * math.sin(a)
        blob.append((bx * (1 + 0.2 * max(0.0, -math.sin(a))), bz))          # đáy phình ra
    part("Piko_Horns", p.root, [([(-0.1, 0.6), (-0.03, 0.62), (-0.08, 0.78)], horn), ([(0.03, 0.63), (0.1, 0.6), (0.07, 0.79)], horn)], 0.01)
    part("Piko_Body", p.root, [(blob, body), (ell(0.07, 0.05, -0.08, 0.52), "#E8FBFF")])
    p.head = node("Piko_Face", p.root, (0.0, 0.0), 0.0)
    add_face(p, p.head, (0.1, 0.46), (0.05, 0.07), "#1E78D2", (0.16, 0.33), 1.0, horn)
    p.arm = part("Piko_Arm", p.root, [(ell(0.035, 0.05, 0.02, -0.03), "#2FC4EA")], -0.02, (0.2, 0.2))
    part("Piko_Drops", p.root, [(ell(0.018, 0.024, 0.32, 0.55), drop), (ell(0.014, 0.019, -0.3, 0.45), drop),
                                (ell(0.012, 0.016, 0.3, 0.2), drop)], -0.025)
    return p


# ================================================================ bối cảnh: đỉnh đồi, máy, vườn mầm, mây
part("Sky", None, [([(-4, -1), (8, -1), (8, 6), (-4, 6)], "#BFE4F7")], 3.0)
part("Ground", None, [([(-4, -1), (8, -1), (8, 0.02), (-4, 0.02)], "#E9D9B6")], 2.0)
part("Garden", None, [([(1.45, -0.05), (3.2, -0.05), (3.2, 0.03), (1.45, 0.03)], "#6B4A33"),
                      ([(3.2, -0.05), (3.65, -0.05), (3.65, 0.03), (3.2, 0.03)], "#C2A27A")], 0.6)   # dải khô ở mép phải
sprouts = []
for i in range(9):
    sx = 1.55 + i * 0.18
    sprouts += [(rrect(0.012, 0.09, 0.005, sx, 0.07), "#5FA544"), (ell(0.03, 0.015, sx - 0.025, 0.11), "#6DBB4E"),
                (ell(0.03, 0.015, sx + 0.025, 0.12), "#6DBB4E")]
sprouts += [([(3.42, 0.02), (3.44, 0.02), (3.47, 0.07), (3.52, 0.05), (3.52, 0.06), (3.46, 0.09)], "#8B6A3E")]  # mầm héo
part("Sprouts", None, sprouts, 0.55)

machine = node("Machine", None, (0.0, 0.0), 0.3)
part("Machine_Body", machine, [(rrect(0.08, 0.14, 0.02, -0.3, 0.07), "#6E6E6E"), (rrect(0.08, 0.14, 0.02, 0.3, 0.07), "#6E6E6E"),
                               (rrect(0.9, 1.0, 0.08, 0, 0.62), "#D9C6AA"), (rrect(0.9, 0.08, 0.02, 0, 0.3), "#BFA98A"),
                               (ell(0.33, 0.28, 0, 1.12, 0, 180), "#A8E0F2"),
                               ([(0, 1.18), (0.07, 1.27), (0, 1.36), (-0.07, 1.27)], "#4FB3E8"),
                               (rrect(0.1, 0.16, 0.02, 0, 1.46), "#9A9A9A")])
part("Machine_Knob", machine, [(ell(0.06, 0.06), "#4A4A4A"), (rrect(0.012, 0.05, 0.005, 0, 0.02), WHITE)], -0.02, (-0.33, 0.48))
part("Machine_Gauge", machine, [(ell(0.1, 0.1), "#F5F5F5"), (arc(0.075, 45, 170, 0.02), "#7BC67B"), (arc(0.075, 10, 45, 0.02), "#E05050")],
     -0.02, (-0.28, 0.84))
needle = part("Machine_Needle", machine, [(rrect(0.01, 0.08, 0.004, 0, 0.04), "#333333")], -0.03, (-0.28, 0.84))
part("Machine_Button", machine, [(ell(0.075, 0.075), "#B71C1C"), (ell(0.06, 0.06, 0.005, 0.005), "#E53935"),
                                 (ell(0.02, 0.02, 0.02, 0.03), "#FF9A9A")], -0.02, (0.45, 0.5))   # ngang ngực Lumo
glint = part("Machine_Glint", machine, [(star(0.07), "#FFF27A")], -0.04, (0.49, 0.57))

cloud = part("Cloud", None, [(ell(0.32, 0.16), WHITE), (ell(0.2, 0.15, -0.25, 0.05), WHITE), (ell(0.22, 0.17, 0.22, 0.06), WHITE),
                             (ell(0.18, 0.15, 0.0, 0.14), WHITE)], 1.0, (2.45, 1.75), unique="CloudMat")
part("Rain", cloud, [(rrect(0.008, 0.07, 0.003, rx, rz), "#7FC4E8")
                     for rx, rz in ((-0.3, -0.3), (-0.15, -0.5), (0.0, -0.35), (0.15, -0.6), (0.3, -0.4), (-0.22, -0.8),
                                    (0.08, -0.85), (0.25, -0.95))], 0.05)

tavi = build_tavi(-0.82, -0.3)
lumo = build_lumo(1.12, -0.32)
piko = build_piko(1.95, -0.28)                                 # sau Lumo: khi đáp lên lưng vẫn thấy mặt Lumo
nori = build_nori(2.6, 1.05, -0.2)
tavi.dir, lumo.dir, piko.dir, nori.dir = 1, 1, -1, -1

# ================================================================ diễn
for p in (lumo, tavi, nori, piko):
    face(p, 0.0, "neutral")
    ry(p.arm, 0.0, 6)
    lean(p, 0.0, 0)

# --- Tavi: nhìn đồng hồ, giật mình, bước ra, hô muộn một nhịp
ry(tavi.arm_far, 0.0, -6)
loop(tavi.tail, 0.0, SECONDS, 1.6, -4, 4)
ry(tavi.head, 0.3, -18)                                       # ngước nhìn đồng hồ
for t in (2.0, 4.3):
    blink(tavi, t)
ry(tavi.head, MAX_POWER[0], -18)
face(tavi, MAX_POWER[0] + 0.05, "shock")
ry(tavi.head, MAX_POWER[0] + 0.2, 0)
at(tavi.root, TAVI_STEP[0], -0.82, 0)                         # bước ra đứng trước thân máy
at(tavi.root, TAVI_STEP[0] + 0.15, -0.6, 0.04)
at(tavi.root, TAVI_STEP[1], -0.3, 0)
for arm, rest, up in ((tavi.arm, 6, -95), (tavi.arm_far, -6, -150)):   # tay gần chỉ về Lumo, tay xa giơ cao
    ry(arm, TAVI_STEP[1], rest)
    ry(arm, TAVI_SHOUT[0] + 0.1, up)
    ry(arm, TAVI_SHOUT[1], up)
    ry(arm, TAVI_SHOUT[1] + 0.4, rest)
lean(tavi, TAVI_STEP[1], 0)
lean(tavi, TAVI_SHOUT[0] + 0.1, 6)
lean(tavi, TAVI_SHOUT[1] + 0.4, 0)
face(tavi, TAVI_SHOUT[0], "shout")
face(tavi, TAVI_SHOUT[1] + 0.2, "worried")
ry(tavi.head, CLOUD_SWELL[0], 0)
face(tavi, CLOUD_SWELL[0] + 0.2, "shock")
ry(tavi.head, CLOUD_SWELL[0] + 0.5, -22)

# --- Nori: lơ lửng trên vườn, giảng về mưa, bị MAX POWER cắt ngang
scl(nori.root, 0.0, -1, 1)
for i in range(int(SECONDS) + 1):
    at(nori.root, i, 2.6, 1.05 + (0.03 if i % 2 else -0.03))
for w in nori.wings:
    loop(w, 0.0, SECONDS, 0.24, -14, 14)
for a in nori.antennae:
    loop(a, 0.0, SECONDS, 1.4, -6, 6)
talk(nori, NORI_TALK[0], NORI_TALK[1])
ry(nori.arm, NORI_TALK[0], 6)
ry(nori.arm, NORI_TALK[0] + 0.4, -60)                          # tay nhỏ minh hoạ khi giảng
ry(nori.arm, NORI_TALK[1], -60)
face(nori, NORI_TALK[1] + 0.05, "shock")
ry(nori.arm, NORI_TALK[1] + 0.3, 10)
lean(nori, CLOUD_SWELL[0], 0)
lean(nori, CLOUD_SWELL[0] + 0.5, -14)                          # ngửa lên nhìn mây

# --- Lumo: nhìn dải khô, vội với tay, khựng lại, bị đè xuống nút, nhận ra
scl(lumo.root, 0.0, 1, 1)
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, 0.0, -4)
ry(lumo.arm_far, 0.0, -6)
loop(lumo.tail, 0.0, LUMO_REACH[0], 0.5, 6, 20)
ry(lumo.head, LUMO_LOOK_DRY[0], 0)
ry(lumo.head, LUMO_LOOK_DRY[0] + 0.3, 12)                      # nhìn xuống dải khô
face(lumo, LUMO_LOOK_DRY[0] + 0.2, "sad")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, LUMO_LOOK_DRY[0] + 0.4, -32)
scl(lumo.root, LUMO_TURN, 1, 1)
scl(lumo.root, LUMO_TURN + 0.15, -1, 1)                        # quay sang trái, về phía nút
lumo.dir = -1
ry(lumo.head, LUMO_TURN, 0)
face(lumo, LUMO_TURN + 0.1, "eager")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, LUMO_TURN + 0.1, 4)
at(lumo.root, LUMO_REACH[0], 1.12, 0)                          # vội: bước nhanh, nhún
at(lumo.root, LUMO_REACH[0] + 0.15, 1.02, 0.04)
at(lumo.root, LUMO_REACH[1] - 0.2, 0.9, 0)
lean(lumo, LUMO_REACH[0], 0)
lean(lumo, LUMO_REACH[1] - 0.2, 4)                             # chồm tới
ry(lumo.arm, LUMO_REACH[0], 6)
ry(lumo.arm, LUMO_REACH[1] - 0.15, -92)                        # vươn tay, còn cách nút vài phân
ry(lumo.arm_far, LUMO_REACH[1] - 0.15, -40)
talk(lumo, LUMO_REACH[0], LUMO_REACH[1] + 0.2, "smile")
ry(lumo.tail, LUMO_REACH[0] + 0.3, 24)
# khựng lại: mặt lo, tai cụp hẳn ra sau, người ngả lại, tay lơ lửng
face(lumo, LUMO_FREEZE[0], "worried")
for e, deg in ((lumo.ear_near, -72), (lumo.ear_far, -78)):
    ry(e, LUMO_FREEZE[0], 4)
    ry(e, LUMO_FREEZE[0] + 0.15, deg)
lean(lumo, LUMO_FREEZE[0], 4)
lean(lumo, LUMO_FREEZE[0] + 0.25, -3)
ry(lumo.head, LUMO_FREEZE[0] + 0.25, -8)
ry(lumo.arm, LUMO_FREEZE[0], -92)
ry(lumo.arm, LUMO_PULL[0], -90)
ry(lumo.tail, LUMO_FREEZE[0] + 0.2, -28)                       # đuôi cụp
# bắt đầu rụt tay
ry(lumo.arm, LUMO_PULL[1] - 0.05, -55)
at(lumo.root, LUMO_PULL[0], 0.9, 0)
at(lumo.root, LUMO_PULL[1] - 0.05, 0.94, 0)
# Piko đáp lên lưng: chúi tới, tay đè xuống nút
at(lumo.root, CLICK, 0.94, 0)
at(lumo.root, CLICK + 0.1, 0.8, 0)
lean(lumo, CLICK, -3)
lean(lumo, CLICK + 0.1, 12)
ry(lumo.arm, CLICK, -55)
ry(lumo.arm, CLICK + 0.08, -100)
face(lumo, CLICK, "shock")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, CLICK, -72)
    ry(e, CLICK + 0.1, 8)                                      # tai bật dựng vì giật mình
lean(lumo, MAX_POWER[1], 9)
ry(lumo.arm, LUMO_REALIZE[0], -100)
# nhận ra: nhìn tay mình trên nút, tai cụp
ry(lumo.head, LUMO_REALIZE[0], -8)
ry(lumo.head, LUMO_REALIZE[0] + 0.3, 22)
face(lumo, LUMO_REALIZE[0] + 0.2, "sad")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, LUMO_REALIZE[0], 8)
    ry(e, LUMO_REALIZE[0] + 0.4, -48)
ry(lumo.head, CLOUD_SWELL[0], 22)
ry(lumo.head, CLOUD_SWELL[0] + 0.4, -25)                       # ngước lên mây
face(lumo, CLOUD_SWELL[0] + 0.2, "shock")

# --- Piko: nút lấp lánh hút mắt, nén người, bật nhảy, đáp lên lưng Lumo
scl(piko.root, 0.0, -1, 1)
for i in range(7):                                             # nảy nhẹ tại chỗ
    t = i * 0.6
    at(piko.root, t, 1.95, 0)
    at(piko.root, t + 0.3, 1.95, 0.035)
at(piko.root, GLINT, 1.95, 0)
face(piko, GLINT + 0.05, "eager")
lean(piko, GLINT + 0.2, 8)                                     # chồm về phía nút
scl(piko.root, PIKO_CROUCH[0], -1, 1)
scl(piko.root, PIKO_CROUCH[1] - 0.05, -1.25, 0.72)             # nén
at(piko.root, PIKO_JUMP[0], 1.95, 0)
scl(piko.root, PIKO_JUMP[0] + 0.1, -0.85, 1.2)                 # giãn khi bật
at(piko.root, PIKO_JUMP[0] + 0.35, 1.5, 0.62)
lean(piko, PIKO_JUMP[0] + 0.35, -10)
at(piko.root, CLICK, 1.2, 0.3)                                 # đáp vào lưng Lumo, ở lớp sau
scl(piko.root, CLICK, -1, 1)
scl(piko.root, CLICK + 0.06, -1.22, 0.8)                       # bẹp khi đáp
at(piko.root, CLICK + 0.1, 1.1, 0.26)
scl(piko.root, CLICK + 0.25, -1, 1)
lean(piko, CLICK + 0.1, 0)
face(piko, CLICK + 0.1, "happy")
ry(piko.arm, CLICK + 0.1, -60)
face(piko, CLOUD_SWELL[0] + 0.2, "shock")
lean(piko, CLOUD_SWELL[0] + 0.4, -12)

# --- máy: kim chỉ NHẸ, lấp lánh, rung khi MAX POWER; mây phồng, sẫm lại
ry(needle, 0.0, -35)
ry(needle, MAX_POWER[0], -35)
ry(needle, MAX_POWER[0] + 0.25, 78)
for t0, t1, amp in ((MAX_POWER[0], MAX_POWER[1], 0.02), (CLOUD_SWELL[0], CLOUD_SWELL[1], 0.012)):
    t, flip = t0, False
    while t < t1:
        at(machine, t, amp if flip else -amp, 0)
        ry(needle, t, 74 if flip else 82)
        t, flip = t + 0.08, not flip
    at(machine, t1, 0.0, 0)
scl(glint, 0.0, 0, 0)
for t, s in ((GLINT - 0.05, 0), (GLINT + 0.1, 1.0), (GLINT + 0.3, 0.55), (GLINT + 0.5, 1.0), (PIKO_JUMP[0], 0)):
    scl(glint, t, s, s)
cm = MATS["CloudMat"]
for t, s, x, col in ((0.0, 1.0, 2.45, (1, 1, 1)), (MAX_POWER[0], 1.0, 2.45, (1, 1, 1)), (MAX_POWER[1], 1.15, 2.4, (0.85, 0.87, 0.9)),
                     (CLOUD_SWELL[0], 1.15, 2.4, (0.85, 0.87, 0.9)), (CLOUD_SWELL[1], 1.9, 1.7, (0.27, 0.29, 0.33))):
    scl(cloud, t, s, s)
    at(cloud, t, x, 1.75 + 0.1 * (s - 1))
    key(cm, "diffuse_color", t, (*col, 1.0))

# ================================================================ máy quay: mỗi shot một máy orthographic, cắt bằng marker
CAMS = {"S1": (1.25, 1.1, 5.0), "S2": (1.12, 0.6, 2.5), "S3": (1.2, 1.25, 5.4)}   # tâm X, tâm Z, bề ngang khung (m)
for name, t0, t1 in SHOTS:
    cx, cz, width = CAMS[name]
    cd = bpy.data.cameras.new(f"Cam_{name}")
    cd.type, cd.ortho_scale, cd.clip_start, cd.clip_end = "ORTHO", width, 0.1, 50
    cam = bpy.data.objects.new(f"Cam_{name}", cd)
    scene.collection.objects.link(cam)
    cam.location, cam.rotation_euler = (cx, -10.0, cz), (math.radians(90), 0, 0)
    scene.timeline_markers.new(name, frame=fr(t0)).camera = cam
    if name == "S1":
        scene.camera = cam

r = scene.render
r.engine = "BLENDER_WORKBENCH"
r.resolution_x, r.resolution_y, r.fps = 1920, 1080, FPS
scene.frame_start, scene.frame_end = 1, round(SECONDS * FPS)
scene.display.shading.light = "FLAT"
scene.display.shading.color_type = "MATERIAL"
scene.display.shading.show_object_outline = True               # viền tối: tay nổi trên thân, đầu cùng màu
scene.display.render_aa = "8"
scene.view_settings.view_transform = "Standard"                # giữ đúng mã màu tham chiếu
scene["stills"] = ",".join(str(fr(t)) for t in (1.5, 2.9, 3.4, 4.2, 5.1, 5.65, 6.9, 8.4, 10.6))

bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND), compress=True)
print("SAVED", OUT_BLEND)
