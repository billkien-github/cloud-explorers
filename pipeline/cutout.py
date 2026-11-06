"""
Bộ nhân vật cutout 2D cho previz 2D (03_CONTENT/PREVIZ_2D.md): hàm keyframe, hình phẳng, bộ mặt, bốn nhân vật,
máy quay theo SHOTS và cài đặt render Workbench. build_shot.py của cảnh dùng:
    sys.path.insert(0, str(<gốc dự án> / "pipeline"))
    from cutout import *
    start(FPS)                      # file trống, đặt FPS cho các hàm keyframe
    ...dựng bối cảnh, nhân vật, diễn...
    cameras(SHOTS, CAMS)
    finish(SECONDS, OUT_BLEND, stills)
Toạ độ: hình nằm trên mặt phẳng XZ (X sang phải, Z lên, mét), máy quay orthographic nhìn theo +Y, Y nhỏ hơn là lớp ở
trước. Mỗi nhân vật dựng quay mặt về +X; root.scale.x = -1 là quay sang trái (đặt p.dir = -1). Xoay quanh Y: góc
dương ngả về phía trước mặt (tai ngả tới, đầu cúi, đuôi vểnh lên); tay buông là 0°, đưa thẳng ra trước là -90°,
giơ cao là -150°. Màu, chiều cao, đồ đeo: 01_BRAND/Character_Bible/README.md.
"""
import math
from types import SimpleNamespace

import bmesh
import bpy

__all__ = ["start", "fr", "key", "ry", "at", "lean", "scl", "show", "loop", "jitter", "mat", "MATS", "ell", "arc",
           "rrect", "star", "turn", "band", "curve", "node", "part", "text", "DARK", "MOUTH_IN", "TONGUE", "WHITE", "FACES",
           "add_face", "face", "blink", "talk", "look", "build_lumo", "build_tavi", "build_nori", "build_piko", "cameras",
           "finish", "SimpleNamespace", "math"]

FPS = 24
MATS = {}


def start(fps):
    """Mở file trống và đặt FPS cho các hàm keyframe."""
    global FPS
    FPS = fps
    MATS.clear()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


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
    """Hiện hay ẩn một mảnh, kèm mọi mảnh con của nó (ẩn một node rỗng không tự ẩn con)."""
    for o in (ob, *ob.children_recursive):
        for path in ("hide_render", "hide_viewport"):
            key(o, path, t, not on)


def loop(ob, t0, t1, period, a, b):
    """Lắc qua lại giữa góc a và b (đuôi, cánh, túi)."""
    t, flip = t0, False
    while t <= t1 + 1e-6:
        ry(ob, t, b if flip else a)
        t, flip = t + period / 2, not flip


def jitter(ob, t0, t1, amp, step=0.06):
    """Rung tại chỗ quanh vị trí hiện tại (máy rung, túi rung, run rẩy)."""
    x, z = ob.location.x, ob.location.z
    t, flip = t0, False
    while t < t1:
        at(ob, t, x + (amp if flip else -amp), z)
        t, flip = t + step, not flip
    at(ob, t1, x, z)


# ================================================================ hình cutout
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


def band(pts, th):
    """Dải dày th chạy theo đường gấp khúc pts (dây, vệt)."""
    left, right = [], []
    for i, (x, z) in enumerate(pts):
        (x0, z0), (x1, z1) = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        n = math.hypot(x1 - x0, z1 - z0) or 1.0
        nx, nz = -(z1 - z0) / n * th / 2, (x1 - x0) / n * th / 2
        left.append((x + nx, z + nz))
        right.append((x - nx, z - nz))
    return left + right[::-1]


def curve(p0, c, p1, n=10):
    """Đường cong bậc hai từ p0 qua điểm kéo c tới p1."""
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]) for t in (i / n for i in range(n + 1))]


def turn(pts, deg, cx=0.0, cz=0.0):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(cx + (x - cx) * c - (z - cz) * s, cz + (x - cx) * s + (z - cz) * c) for x, z in pts]


def node(name, parent, loc=(0.0, 0.0), y=0.0):
    ob = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(ob)
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
    bpy.context.scene.collection.objects.link(ob)
    ob.parent, ob.location = parent, (loc[0], y, loc[1])
    return ob


def text(name, body, size, loc, col, y=-1.0):
    """Chữ phẳng căn giữa (tên phim, biển). Font mặc định của Blender có dấu tiếng Việt."""
    cu = bpy.data.curves.new(name, "FONT")
    cu.body, cu.size, cu.align_x, cu.align_y = body, size, "CENTER", "CENTER"
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.location, ob.rotation_euler = (loc[0], y, loc[1]), (math.radians(90), 0, 0)
    cu.materials.append(mat(col))
    return ob


# ================================================================ mặt dùng chung
DARK, MOUTH_IN, TONGUE, WHITE = "#2B1B14", "#5A1E24", "#E8707E", "#FFFFFF"
# biểu cảm: (mắt, miệng, góc lông mày; âm = đầu lông mày phía trước nhướng lên, kiểu lo lắng)
FACES = {
    "neutral": ("open", "closed", 0), "eager": ("wide", "smile", 10), "happy": ("happy", "smile", 0),
    "worried": ("wide", "frown", -24), "shock": ("wide", "o", -12), "sad": ("open", "frown", -16),
    "shout": ("wide", "open", 20), "sheepish": ("happy", "frown", -16), "puzzled": ("open", "o", 14),
    "grin": ("happy", "smile", -16), "squint": ("closed", "frown", -20),
}


def add_face(p, head, eye, eye_r, iris, mouth, s=1.0, brow=DARK, tongue=TONGUE):
    rx, rz = eye_r
    e = node(f"{p.name}_Eye", head, eye, -0.012)
    op = node(f"{p.name}_EyeOpen", e)                                         # tròng nằm trong node con để dời hướng nhìn
    po = node(f"{p.name}_PupilOpen", op)
    part(f"{p.name}_IrisOpen", po, [(ell(rx, rz), iris), (ell(rx * 0.32, rz * 0.3, rx * 0.3, rz * 0.35), WHITE)])
    wide = node(f"{p.name}_EyeWide", e)
    part(f"{p.name}_EyeWhite", wide, [(ell(rx * 1.45, rz * 1.35), WHITE)])
    pw = node(f"{p.name}_PupilWide", wide, (0.0, 0.0), -0.002)
    part(f"{p.name}_IrisWide", pw, [(ell(rx * 1.05, rz * 1.05, rx * 0.15), iris), (ell(rx * 0.32, rz * 0.3, rx * 0.45, rz * 0.4), WHITE)])
    p.pupils = [(po, rx * 0.35, rz * 0.3), (pw, rx * 0.4, rz * 0.32)]
    p.eyes = {
        "open": op, "wide": wide,
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
                                                (ell(0.018 * s, 0.012 * s, 0, -0.018 * s), tongue)]),
        "o": part(f"{p.name}_MouthO", m, [(ell(0.016 * s, 0.02 * s), MOUTH_IN)]),
        "frown": part(f"{p.name}_MouthFrown", m, [(arc(0.03 * s, 25, 155, 0.009 * s, 0, -0.028 * s), DARK)]),
    }


def face(p, t, name, tilt=0.0):
    """tilt: góc người và đầu đang cúi (lean + góc đầu) để bù cho lông mày, giữ đúng nét mặt khi nhân vật cúi hay chồm."""
    eyes, mouth, brow = FACES[name]
    for k, ob in p.eyes.items():
        show(ob, t, k == eyes)
    for k, ob in p.mouths.items():
        show(ob, t, k == mouth)
    last = getattr(p, "brow_last", None)
    if last and t - 0.12 > last[0]:                                           # giữ nét cũ tới sát lúc đổi: lông mày đổi
        ry(p.brow, t - 0.12, last[1])                                         # nhanh, không trôi dần giữa hai lần face()
    ry(p.brow, t, brow - tilt)
    p.brow_last = (t, brow - tilt)


def look(p, t, dx=0.0, dz=0.0):
    """Hướng nhìn: dx, dz trong khoảng -1..1 (dx dương là về phía trước mặt, dz dương là nhìn lên)."""
    for n, ax, az in p.pupils:
        key(n, "location", t, (dx * ax, n.location.y, dz * az))


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


# ================================================================ bốn nhân vật (màu, chiều cao, đồ đeo: Character Bible)
def build_lumo(x, layer):
    fur, shade, cream, cape, pink, brown = "#FD8A2B", "#E07722", "#FEECCF", "#FC6640", "#F4A6B0", "#8A5A35"
    p = SimpleNamespace(name="Lumo", dir=1)
    p.root = node("Lumo", None, (x, 0.0), layer)
    p.tail = part("Lumo_Tail", p.root, [(ell(0.15, 0.07, -0.13, 0.05), fur), (ell(0.06, 0.05, -0.25, 0.08), cream)],
                  0.03, (-0.11, 0.2))
    p.arm_far = part("Lumo_ArmFar", p.root, [(rrect(0.065, 0.2, 0.03, 0, -0.1), shade), (ell(0.04, 0.035, 0, -0.21), cream)],
                     0.025, (-0.01, 0.46))
    part("Lumo_Cape", p.root, [([(0.0, 0.48), (-0.19, 0.42), (-0.22, 0.16), (-0.02, 0.2)], cape)], 0.015)
    part("Lumo_Legs", p.root, [(rrect(0.07, 0.14, 0.03, -0.05, 0.08), shade), (rrect(0.07, 0.14, 0.03, 0.05, 0.08), fur),
                               (ell(0.06, 0.035, -0.03, 0.02), cream), (ell(0.06, 0.035, 0.07, 0.02), cream)], 0.005)
    part("Lumo_Body", p.root, [(ell(0.15, 0.2, 0, 0.3), fur), (ell(0.09, 0.14, 0.05, 0.29), cream)])
    p.bag = part("Lumo_Bag", p.root, [([(-0.06, 0.44), (0.1, 0.24), (0.11, 0.26), (-0.05, 0.46)], brown),   # quai đeo chéo
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
    green, shade, snout, crystal, cap, vest, belly = "#7EA258", "#6B8E4A", "#E8CF9E", "#14F5F4", "#7A4A2A", "#EFE2C4", "#ECBA7B"
    p = SimpleNamespace(name="Tavi", dir=1)
    p.GOGGLES_DOWN = (0.06, -0.135)                                           # độ dời kính từ mũ xuống ngang mắt
    p.root = node("Tavi", None, (x, 0.0), layer)
    p.tail = part("Tavi_Tail", p.root, [([(0.0, 0.06), (-0.36, -0.12), (-0.37, -0.15), (0.0, -0.04)], green)]
                  + [([(tx - 0.03, tz), (tx + 0.02, tz + 0.005), (tx - 0.012, tz + 0.05)], crystal)      # gai tinh thể dọc đuôi
                     for tx, tz in ((-0.08, 0.02), (-0.17, -0.025), (-0.26, -0.07))], 0.03, (-0.07, 0.16))
    part("Tavi_Pack", p.root, [(rrect(0.12, 0.2, 0.03, -0.15, 0.32), "#8A6A45"), (ell(0.025, 0.025, -0.15, 0.38), crystal)], 0.025)
    p.arm_far = part("Tavi_ArmFar", p.root, [(rrect(0.06, 0.17, 0.028, 0, -0.085), shade), (ell(0.035, 0.03, 0, -0.18), shade)],
                     0.02, (-0.01, 0.36))
    part("Tavi_Spikes", p.root, [([(bx, bz + 0.035), (bx - 0.08, bz + 0.01), (bx, bz - 0.035)], crystal)
                                 for bx, bz in ((-0.11, 0.42), (-0.14, 0.32), (-0.13, 0.22))], 0.015)
    part("Tavi_Legs", p.root, [(rrect(0.08, 0.11, 0.035, -0.04, 0.06), shade), (rrect(0.08, 0.11, 0.035, 0.05, 0.06), green)], 0.005)
    part("Tavi_Body", p.root, [(ell(0.14, 0.17, 0, 0.26), green), (ell(0.085, 0.06, 0.035, 0.13), belly),
                               (rrect(0.2, 0.16, 0.04, -0.01, 0.3), vest),
                               (rrect(0.23, 0.03, 0.01, 0.0, 0.21), cap)])
    p.head = node("Tavi_Head", p.root, (0.03, 0.42), -0.01)                   # đỉnh mũ ở khoảng 0.82
    part("Tavi_Skull", p.head, [(ell(0.17, 0.16, 0.02, 0.17), green), (ell(0.1, 0.07, 0.15, 0.1), snout),
                                (ell(0.18, 0.1, 0.0, 0.26, 0, 180), cap)])
    add_face(p, p.head, (0.11, 0.2), (0.035, 0.045), "#3D7A2E", (0.17, 0.05), 0.9)
    # kính bảo hộ: node riêng, mặc định đẩy lên mũ; kéo xuống mắt thì dời location tới GOGGLES_DOWN và ẩn tròng màu
    # (p.goggle_lens) để vẫn thấy mắt qua vành kính
    p.goggles = node("Tavi_Goggles", p.head, (0.0, 0.0), -0.02)
    part("Tavi_GoggleRims", p.goggles, [(arc(0.038, 0, 360, 0.016, -0.04, 0.34), "#5A5A5A"),
                                        (arc(0.038, 0, 360, 0.016, 0.06, 0.33), "#5A5A5A")])
    p.goggle_lens = part("Tavi_GoggleLens", p.goggles, [(ell(0.032, 0.028, -0.04, 0.34), "#7FD6E6"),
                                                        (ell(0.032, 0.028, 0.06, 0.33), "#7FD6E6")], 0.001)
    p.pack = bpy.data.objects["Tavi_Pack"]
    p.arm = part("Tavi_ArmNear", p.root, [(rrect(0.06, 0.17, 0.028, 0, -0.085), green), (ell(0.035, 0.03, 0, -0.18), green)],
                 -0.02, (0.03, 0.36))
    return p


def build_nori(x, z, layer):
    body, wing, star_c = "#A787F6", "#D3ABFC", "#FEF7A0"
    p = SimpleNamespace(name="Nori", dir=1)
    p.root = node("Nori", None, (x, z), layer)                                # gốc ở tâm thân; bay, không chân
    part("Nori_Glow", p.root, [(ell(0.27, 0.27), "#DCCFFF")], 0.04)
    # 4 cánh: mỗi mảnh một cặp (cánh trên to chếch lên, cánh dưới nhỏ chếch xuống); cặp phía xa lệch lên trước để ló ra
    p.wings = [part(f"Nori_Wing{i}", p.root, [(turn(ell(0.17, 0.08, -0.15, 0.1), -25 + extra), col),
                                              (turn(ell(0.12, 0.06, -0.13, -0.05), 20 + extra / 2), col)], y, (-0.05 + dx, 0.04))
               for i, (col, y, dx, extra) in enumerate((("#C49BF0", 0.035, 0.05, -14), (wing, 0.03, 0.0, 0)))]
    part("Nori_Trail", p.root, [([(-0.08, -0.12), (0.08, -0.12), (0.0, -0.42)], "#E6D9FF")], 0.01)   # vệt sáng thay chân
    p.antennae = [part(f"Nori_Antenna{i}", p.root, [(rrect(0.015, 0.16, 0.007, 0, 0.08), "#8E6FE0"), (star(0.045, 0, 0.17), star_c)],
                       y, (dx, 0.17)) for i, (dx, y) in enumerate(((-0.05, 0.02), (0.04, -0.016)))]
    part("Nori_Body", p.root, [(ell(0.2, 0.2), body), (ell(0.1, 0.06, -0.07, 0.09), "#BCA6F9")])
    p.head = node("Nori_Face", p.root, (0.0, 0.0), 0.0)
    add_face(p, p.head, (0.08, 0.04), (0.04, 0.055), "#5B3FA8", (0.13, -0.06), 0.9, "#6D52C2")
    p.arm = part("Nori_Arm", p.root, [(ell(0.03, 0.045, 0, -0.04), "#9A78F0")], -0.02, (0.02, -0.14))  # dưới thân, xa miệng
    return p


def build_piko(x, layer):
    body, horn, drop, gold, purple = "#3BDCFD", "#1F5FB4", "#9BEBFF", "#E8B33A", "#7B3FB5"
    p = SimpleNamespace(name="Piko", dir=1)
    p.root = node("Piko", None, (x, 0.0), layer)                              # không chân, chỉ nảy và co giãn
    blob = []
    for i in range(48):                                                       # khối thạch bè, đáy rộng (concept)
        a = 2 * math.pi * i / 48
        blob.append((0.29 * math.cos(a) * (1 + 0.18 * max(0.0, -math.sin(a))), 0.31 + 0.31 * math.sin(a)))
    horn_l = [(-0.12, 0.58), (-0.04, 0.61), (-0.06, 0.665), (-0.095, 0.7), (-0.13, 0.72), (-0.155, 0.71), (-0.16, 0.685), (-0.14, 0.64)]
    part("Piko_Horns", p.root, [(horn_l, horn), ([(-x, z) for x, z in horn_l], horn)], 0.01)   # sừng ngắn, đầu tròn, cong ra ngoài
    part("Piko_Body", p.root, [(blob, body), (ell(0.07, 0.05, -0.09, 0.5), "#E8FBFF")])
    p.head = node("Piko_Face", p.root, (0.0, 0.0), 0.0)
    add_face(p, p.head, (0.1, 0.44), (0.05, 0.07), "#1E78D2", (0.16, 0.31), 1.0, horn, "#D23C55")
    # Pocket of Wonders đeo chéo: dây vàng quàng qua gốc sừng phía lưng, chạy dọc mép lưng xuống, vòng chéo dưới miệng; túi ở hông
    # phía mặt nhìn, ngang tầm tay (dây không vắt qua mặt)
    part("Piko_BagLoop", p.root, [(rrect(0.11, 0.024, 0.012, -0.095, 0.635), gold)], 0.005)   # vòng dây ở gốc sừng
    part("Piko_BagStrap", p.root, [(band(curve((-0.1, 0.6), (-0.36, 0.42), (-0.17, 0.06)), 0.013), gold),
                                   (band(curve((-0.17, 0.06), (0.1, 0.09), (0.3, 0.2)), 0.013), gold)], -0.028)
    p.bag = node("Piko_Bag", p.root, (0.3, 0.2), -0.03)                      # khớp ở miệng túi, lắc theo cú nảy
    part("Piko_BagSack", p.bag, [(ell(0.036, 0.016, 0, 0.006), purple), (ell(0.056, 0.055, 0, -0.07), purple),
                                 (rrect(0.05, 0.016, 0.008, 0, -0.012), gold), (ell(0.024, 0.014, 0, -0.072), "#F6EBD9")])
    p.arm = part("Piko_Arm", p.root, [(ell(0.035, 0.05, 0.02, -0.03), "#2FC4EA")], -0.029, (0.24, 0.22))  # tay thấp dưới miệng,
    # lớp giữa dây đeo và túi: thò tay vào túi thì bàn tay khuất trong túi
    p.drops = part("Piko_Drops", p.root, [(ell(0.018, 0.024, -0.33, 0.55), drop), (ell(0.014, 0.019, -0.36, 0.22), drop),
                                (ell(0.012, 0.016, 0.37, 0.45), drop)], -0.025)        # giọt nước bắn quanh người, tránh vùng mặt
    return p


# ================================================================ máy quay, render
def cameras(shots, cams):
    """Mỗi shot một máy orthographic, cắt bằng timeline marker. cams[tên] = (tâm X, tâm Z, bề ngang khung m)."""
    scene = bpy.context.scene
    for name, t0, t1 in shots:
        cx, cz, width = cams[name]
        cd = bpy.data.cameras.new(f"Cam_{name}")
        cd.type, cd.ortho_scale, cd.clip_start, cd.clip_end = "ORTHO", width, 0.1, 50
        cam = bpy.data.objects.new(f"Cam_{name}", cd)
        scene.collection.objects.link(cam)
        cam.location, cam.rotation_euler = (cx, -10.0, cz), (math.radians(90), 0, 0)
        scene.timeline_markers.new(name, frame=fr(t0)).camera = cam
        if t0 == shots[0][1]:
            scene.camera = cam


def finish(seconds, out_blend, stills=()):
    """Workbench màu phẳng có viền tối, 1920x1080, lưu .blend. stills: các giây để run.ps1 stills render mẫu."""
    scene = bpy.context.scene
    r = scene.render
    r.engine = "BLENDER_WORKBENCH"
    r.resolution_x, r.resolution_y, r.fps = 1920, 1080, FPS
    scene.frame_start, scene.frame_end = 1, round(seconds * FPS)
    scene.display.shading.light = "FLAT"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_object_outline = True               # viền tối: tay nổi trên thân, đầu cùng màu
    scene.display.render_aa = "8"
    scene.view_settings.view_transform = "Standard"                # giữ đúng mã màu tham chiếu
    if stills:
        scene["stills"] = ",".join(str(fr(t)) for t in stills)
    bpy.ops.wm.save_as_mainfile(filepath=str(out_blend), compress=True)
    print("SAVED", out_blend)
