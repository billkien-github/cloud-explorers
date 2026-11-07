"""
Bộ nhân vật cutout 2D cho previz 2D (03_CONTENT/PREVIZ_2D.md): hàm keyframe (kèm chống trôi giữa hai key thưa), hình
phẳng, bộ mặt, bốn nhân vật (Lumo có tuỳ chọn chân tách hai mảnh, áo choàng khớp ở cổ), hàm diễn dùng chung (đi, quay
mặt, co giãn, tai, vị trí bàn tay và góc tay với tới, lóe, lấp lánh, mảnh văng), Wonder Compass và hàm diễn của nó (cầm ở
tay gần hay tay xa luôn đứng thẳng, bụi phủ, mức sáng, kêu, rung, lóe, mũi sao ngắm mục tiêu từng khung), nhân vật nền và
đạo cụ của EP000A (chú chim nhỏ, bướm phát sáng, mây khắc, bản đồ giấy và bản đồ khắc trên đá, hòn đảo có Wonder Hub,
xanh ngọc tín hiệu), sao hoa gió, máy quay theo SHOTS và cài đặt render Workbench. build_shot.py của cảnh dùng:
    sys.path.insert(0, str(<gốc dự án> / "pipeline"))
    from cutout import *
    start(FPS)                      # file trống, đặt FPS cho các hàm keyframe
    ...dựng bối cảnh, nhân vật, diễn...
    aim(...)                        # mũi sao la bàn: chạy sau cùng, khi mọi chuyển động khác đã key xong
    cameras(SHOTS, CAMS)
    finish(SECONDS, OUT_BLEND, stills)
Toạ độ: hình nằm trên mặt phẳng XZ (X sang phải, Z lên, mét), máy quay orthographic nhìn theo +Y, Y nhỏ hơn là lớp ở
trước. Mỗi nhân vật dựng quay mặt về +X; root.scale.x = -1 là quay sang trái (đặt p.dir = -1). Xoay quanh Y: góc
dương ngả về phía trước mặt (tai ngả tới, đầu cúi, đuôi vểnh lên); tay buông là 0°, đưa thẳng ra trước là -90°,
giơ cao là -150°. Màu, chiều cao, đồ đeo: 01_BRAND/Character_Bible/README.md.
Cảnh ghi đè hay thêm biểu cảm riêng bằng FACES["tên"] = (mắt, miệng, góc lông mày) ngay sau start().
"""
import math
from types import SimpleNamespace

import bmesh
import bpy
from bpy_extras import anim_utils
from mathutils import Vector

__all__ = ["start", "fr", "key", "ry", "at", "lean", "scl", "show", "loop", "jitter", "fcurves", "ease_gaps", "mat", "MATS",
           "ell", "arc", "rrect", "rect", "star", "turn", "band", "curve", "node", "part", "text", "DARK", "MOUTH_IN", "TONGUE",
           "WHITE", "FACES", "add_face", "face", "fc", "blink", "bl", "talk", "look", "build_lumo", "build_tavi", "build_nori",
           "build_piko", "cameras", "finish", "SimpleNamespace", "math", "steps", "mouth", "facing", "squash", "walk", "ears",
           "hand", "reach", "flash", "glow_flash", "twinkle", "fly_bit", "rose", "leaf_pts", "build_compass", "palm",
           "build_holder", "chold", "compass_bits", "glow", "beep", "buzz", "compass_flash", "glide", "swing", "aim",
           "build_bird", "bird_beak", "bird_eyes", "build_bfly", "flap", "cloud_parts", "map_card", "map_big", "MAP_OBS",
           "map_obs_glow", "TEAL", "TEAL_L", "TEAL_M", "hub_shapes", "build_hub_island"]

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


def fcurves(ob):
    """Các kênh keyframe của một object (action nhiều lớp của Blender 5.x); chưa có key thì trả về danh sách rỗng."""
    ad = ob.animation_data
    if not ad or not ad.action:
        return []
    return anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves


def ease_gaps(obs, gap=0.6, lead=0.25):
    """Chống trôi giữa hai key thưa: hai key cùng kênh cách nhau quá gap giây mà khác giá trị thì giữ giá trị cũ tới lead
    giây trước key sau, nên tư thế đứng yên rồi mới chuyển chứ không trôi chậm suốt quãng giữa hai hành động. Chạy sau khi
    đã key xong các object trong obs; bỏ qua kênh bật tắt (hide_*)."""
    for ob in obs:
        for cv in fcurves(ob):
            if cv.data_path.startswith("hide"):
                continue
            pts = sorted((kp.co[0], kp.co[1]) for kp in cv.keyframe_points)
            for (f0, v0), (f1, v1) in zip(pts, pts[1:]):
                if f1 - f0 > gap * FPS and abs(v1 - v0) > 1e-4:
                    cv.keyframe_points.insert(f1 - round(lead * FPS), v0)
            cv.update()


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


def rect(x0, z0, x1, z1):
    """Hình chữ nhật theo hai góc (nền, trời, mảng tường)."""
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


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
    "wonder": ("wide", "o", -8),                                              # tròn mắt, miệng chữ O: ngạc nhiên thích thú
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


def fc(p, t, name, tilt=0.0):
    """face() và nhớ biểu cảm đang dùng (p.cur) để bl() chớp mắt xong mở lại đúng mắt của biểu cảm đó."""
    face(p, t, name, tilt)
    p.cur = name


def look(p, t, dx=0.0, dz=0.0):
    """Hướng nhìn: dx, dz trong khoảng -1..1 (dx dương là về phía trước mặt, dz dương là nhìn lên)."""
    for n, ax, az in p.pupils:
        key(n, "location", t, (dx * ax, n.location.y, dz * az))


def blink(p, t, back="open"):
    for k, ob in p.eyes.items():
        show(ob, t, k == "closed")
        show(ob, t + 0.1, k == back)


def bl(p, t):
    """Chớp mắt, mở lại về mắt của biểu cảm đặt bằng fc() gần nhất (p.cur)."""
    blink(p, t, FACES[p.cur][0])


def talk(p, t0, t1, rest="closed"):
    t, on = t0, True
    while t < t1:
        for k, ob in p.mouths.items():
            show(ob, t, k == ("open" if on else rest))
        t, on = t + 0.12, not on
    for k, ob in p.mouths.items():
        show(ob, t1, k == rest)


# ================================================================ bốn nhân vật (màu, chiều cao, đồ đeo: Character Bible)
def build_lumo(x, layer, split_legs=False, cape_pivot=False):
    """Lumo, gốc ở chân. split_legs: hai chân tách mảnh, khớp ở hông (p.leg_near, p.leg_far; ry âm là nhấc chân về phía
    trước) thay cho một mảnh chân liền. cape_pivot: áo choàng khớp ở cổ (p.cape_pivot; ry dương là bay ngược ra sau) để
    bay trong gió. Mặc định là Lumo chân liền, áo choàng liền thân."""
    fur, shade, cream, cape, pink, brown = "#FD8A2B", "#E07722", "#FEECCF", "#FC6640", "#F4A6B0", "#8A5A35"
    p = SimpleNamespace(name="Lumo", dir=1)
    p.root = node("Lumo", None, (x, 0.0), layer)
    p.tail = part("Lumo_Tail", p.root, [(ell(0.15, 0.07, -0.13, 0.05), fur), (ell(0.06, 0.05, -0.25, 0.08), cream)],
                  0.03, (-0.11, 0.2))
    p.arm_far = part("Lumo_ArmFar", p.root, [(rrect(0.065, 0.2, 0.03, 0, -0.1), shade), (ell(0.04, 0.035, 0, -0.21), cream)],
                     0.025, (-0.01, 0.46))
    cape_shape = [([(0.0, 0.48), (-0.19, 0.42), (-0.22, 0.16), (-0.02, 0.2)], cape)]
    if cape_pivot:
        p.cape_pivot = node("Lumo_CapePivot", p.root, (-0.02, 0.47), 0.015)
        part("Lumo_Cape", p.cape_pivot, cape_shape, 0.0, (0.02, -0.47))
    else:
        part("Lumo_Cape", p.root, cape_shape, 0.015)
    if split_legs:
        p.leg_far = part("Lumo_LegFar", p.root, [(rrect(0.07, 0.14, 0.03, 0.0, -0.06), shade), (ell(0.06, 0.035, 0.02, -0.12), cream)],
                         0.007, (-0.05, 0.14))
        p.leg_near = part("Lumo_LegNear", p.root, [(rrect(0.07, 0.14, 0.03, 0.0, -0.06), fur), (ell(0.06, 0.035, 0.02, -0.12), cream)],
                          0.004, (0.05, 0.14))
    else:
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
    green, shade, snout, crystal, cap, vest, belly = "#84B746", "#70A03B", "#E8CF9E", "#14F5F4", "#7A4A2A", "#EFE2C4", "#EFCB99"
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
    body, wing, star_c = "#E8C3FB", "#D3ABFC", "#FEF7A0"
    p = SimpleNamespace(name="Nori", dir=1)
    p.root = node("Nori", None, (x, z), layer)                                # gốc ở tâm thân; bay, không chân
    part("Nori_Glow", p.root, [(ell(0.27, 0.27), "#F6E7FF")], 0.04)
    # 4 cánh: mỗi mảnh một cặp (cánh trên to chếch lên, cánh dưới nhỏ chếch xuống); cặp phía xa lệch lên trước để ló ra
    p.wings = [part(f"Nori_Wing{i}", p.root, [(turn(ell(0.17, 0.08, -0.15, 0.1), -25 + extra), col),
                                              (turn(ell(0.12, 0.06, -0.13, -0.05), 20 + extra / 2), col)], y, (-0.05 + dx, 0.04))
               for i, (col, y, dx, extra) in enumerate((("#C49BF0", 0.035, 0.05, -14), (wing, 0.03, 0.0, 0)))]
    part("Nori_Trail", p.root, [([(-0.08, -0.12), (0.08, -0.12), (0.0, -0.42)], "#E6D9FF")], 0.01)   # vệt sáng thay chân
    p.antennae = [part(f"Nori_Antenna{i}", p.root, [(rrect(0.015, 0.16, 0.007, 0, 0.08), "#C5A0E5"), (star(0.045, 0, 0.17), star_c)],
                       y, (dx, 0.17)) for i, (dx, y) in enumerate(((-0.05, 0.02), (0.04, -0.016)))]
    part("Nori_Body", p.root, [(ell(0.2, 0.2), body), (ell(0.1, 0.06, -0.07, 0.09), "#EDD2FC")])
    p.head = node("Nori_Face", p.root, (0.0, 0.0), 0.0)
    add_face(p, p.head, (0.08, 0.04), (0.04, 0.055), "#5B3FA8", (0.13, -0.06), 0.9, "#6D52C2")
    p.arm = part("Nori_Arm", p.root, [(ell(0.03, 0.045, 0, -0.04), "#D6ADF5")], -0.02, (0.02, -0.14))  # dưới thân, xa miệng
    return p


def build_piko(x, layer):
    body, horn, drop, gold, purple = "#44DAFC", "#1F5FB4", "#9BEBFF", "#E8B33A", "#7B3FB5"
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
    p.arm = part("Piko_Arm", p.root, [(ell(0.035, 0.05, 0.02, -0.03), "#36C2E9")], -0.029, (0.24, 0.22))  # tay thấp dưới miệng,
    # lớp giữa dây đeo và túi: thò tay vào túi thì bàn tay khuất trong túi
    p.drops = part("Piko_Drops", p.root, [(ell(0.018, 0.024, -0.33, 0.55), drop), (ell(0.014, 0.019, -0.36, 0.22), drop),
                                (ell(0.012, 0.016, 0.37, 0.45), drop)], -0.025)        # giọt nước bắn quanh người, tránh vùng mặt
    return p


# ================================================================ hàm diễn dùng chung
def steps(t0, t1, step):
    return [t0 + i * step for i in range(int(round((t1 - t0) / step)) + 1)]


def mouth(p, t, k):
    for name, ob in p.mouths.items():
        show(ob, t, name == k)


def facing(p, t, d, turn=0.0):
    """Quay mặt (d = 1 phải, -1 trái); turn = 0 là đổi tức thì ở điểm cắt (key giữ sớm hơn một khung), > 0 là quay
    trong turn giây. Đặt lại scale của root về (d, 1)."""
    scl(p.root, t - (turn or 1.0 / FPS), p.dir, 1)
    scl(p.root, t, d, 1)
    p.dir = d


def squash(p, t, sx, sz):
    """Co giãn thân, giữ đúng hướng mặt."""
    scl(p.root, t, sx * p.dir, sz)


def walk(ob, t0, t1, x0, x1, n=4, hop=0.04, z=0.0):
    """Đi từ x0 tới x1 trong n bước, nhún hop ở các bước lẻ."""
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        at(ob, t, x0 + (x1 - x0) * i / n, z + (hop if i % 2 else 0.0))


def hand(p, x, z, a, lean_deg=0.0, shoulder=(0.03, 0.46), arm=0.21):
    """Vị trí bàn tay trong thế giới khi root ở (x, z), tay xoay a độ, người nghiêng lean_deg (theo hướng p.dir).
    Mặc định là vai và tay của Lumo."""
    hx, hz = shoulder[0] - arm * math.sin(math.radians(a)), shoulder[1] - arm * math.cos(math.radians(a))
    L = math.radians(lean_deg)
    return (x + p.dir * (hx * math.cos(L) + hz * math.sin(L)), z - hx * math.sin(L) + hz * math.cos(L))


def reach(p, x, z, lean_deg, target, shoulder=(0.03, 0.46), lo=-170, hi=30):
    """Góc tay (độ nguyên, trong lo…hi) để bàn tay chạm target khi root ở (x, z), người nghiêng lean_deg; shoulder như
    hand() (vai tay xa của Lumo là (-0.01, 0.46))."""
    return min(range(lo, hi + 1), key=lambda a: math.dist(hand(p, x, z, a, lean_deg, shoulder), target))


def ears(p, t, near, far=None):
    """Hai tai Lumo (độ, dương là ngả tới, âm là cụp ra sau); tai xa mặc định theo tai gần, lệch 4° để thấy hai tai."""
    ry(p.ear_near, t, near)
    ry(p.ear_far, t, near - 4 if far is None else far)


FLASH = ((0.0, 0.2), (0.12, 1.4), (0.3, 0.7), (0.45, 1.1), (0.6, 0.0))            # lóe: bung to, thu lại, tắt
PULSE = ((0.0, 0.25), (0.1, 1.25), (0.3, 0.95), (0.5, 1.12), (0.85, 0.0))         # một nhịp lóe của Wonder Hub


def flash(ob, t, size=1.0, env=FLASH):
    """Lóe sáng một cái: hiện, co giãn theo env [(giây sau t, tỉ lệ)], tắt ở mốc cuối của env."""
    show(ob, t, True)
    for dt, s in env:
        scl(ob, t + dt, s * size, s * size)
    show(ob, t + env[-1][0], False)


def glow_flash(ob, t, size=1.0, lit=None):
    """Một nhịp lóe của Wonder Hub (PULSE), dùng chung cho đài thiên văn và mọi thứ lóe theo nó (la bàn, Inventor Pack):
    quầng ob bung ra rồi tắt; lit là mảnh sáng bừng 0.7 giây cùng nhịp (mái vòm, mặt kính la bàn, khe nắp hộp)."""
    flash(ob, t, size, PULSE)
    if lit is not None:
        show(lit, t, True)
        show(lit, t + 0.7, False)


def twinkle(ob, t0, t1, big=1.3, small=0.8, step=0.15):
    """Lấp lánh liên tục trong một quãng (vẫn hiện sau t1, tự ẩn nếu cần)."""
    show(ob, t0, True)
    for i, t in enumerate(steps(t0, t1, step)):
        s = 0.3 if i == 0 else big if i % 2 else small
        scl(ob, t, s, s)


def fly_bit(ob, t0, p0, p1, t1, spin=180, lift=0.2):
    """Một mảnh nhỏ (lá, gai, sỏi) văng từ p0 theo đường cong, rơi tới p1, ẩn sau t1 + 0.3."""
    show(ob, t0, True)
    mid = ((p0[0] + p1[0]) / 2, max(p0[1], p1[1]) + lift)
    for k in range(5):
        u = k / 4
        x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * mid[0] + u * u * p1[0]
        z = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * mid[1] + u * u * p1[1]
        at(ob, t0 + (t1 - t0) * u, x, z)
        ry(ob, t0 + (t1 - t0) * u, spin * u)
    show(ob, t1 + 0.3, False)


def rose(r, cx=0.0, cz=0.0, short=0.55, inner=0.2):
    """Sao tám cánh kiểu hoa gió (bốn cánh dài xen bốn cánh ngắn): mọi ngôi sao khắc trong phế tích EP000A."""
    pts = []
    for i in range(16):
        a = math.pi / 2 + math.pi * i / 8
        rr = r if i % 4 == 0 else r * short if i % 4 == 2 else r * inner
        pts.append((cx + rr * math.cos(a), cz + rr * math.sin(a)))
    return pts


def leaf_pts(cx, cz, s, ang):
    """Chiếc lá nhỏ hình thoi dài khoảng 0.07 * s."""
    return turn([(cx - 0.035 * s, cz), (cx, cz + 0.016 * s), (cx + 0.035 * s, cz), (cx, cz - 0.016 * s)], ang, cx, cz)


# ================================================================ Wonder Compass (Character Bible, mục Bảo bối)
def build_compass(name, parent, loc, y, r, flash=False):
    """Wonder Compass nhìn thẳng, bán kính vỏ r (cầm tay Lumo khoảng 0.06, cú cận 0.3–0.4): vỏ vàng có khoen, mặt kính
    xanh, đá xanh trên vành, mây kem ở chân vỏ. c.needle là mũi sao (xoay bằng ry, độ theo chiều kim đồng hồ, 0 là đầu
    chỉ hướng lên trong hệ của cha; cha lật gương thì góc trên hình đổi dấu; cho chỉ mục tiêu bằng aim()): bảy cánh ngắn
    trắng xanh, một cánh đầu chỉ vàng kim dài gấp rưỡi, đầu có viên đá xanh. c.glow là quầng sáng sau vỏ, mặc định ẩn,
    đặt mức bằng glow() (le lói thì nhỏ, sáng mạnh thì bung to), kêu TÍT bằng beep(); rung thì jitter(c.root, …).
    flash=True: thêm quầng tia vàng sau vỏ (c.flash) và mặt kính sáng bừng (c.bright) để lóe theo đài thiên văn
    (compass_flash()); mặc định hiện, cảnh tự ẩn từ giây 0."""
    gold, gold_l, glass, gem, cream = "#E2A52C", "#F4C552", "#3D8FE3", "#63D3FF", "#F5EBDD"
    c = SimpleNamespace(name=name)
    c.root = node(name, parent, loc, y)
    c.glow = part(f"{name}_Glow", c.root, [(ell(1.7 * r, 1.7 * r), "#FFF1A6"), (ell(1.25 * r, 1.25 * r), "#FFF8D2")], 0.006)

    def diamond(cx, cz, s):
        return [(cx, cz + s), (cx + 0.75 * s, cz), (cx, cz - s), (cx - 0.75 * s, cz)]

    part(f"{name}_Case", c.root, [(arc(0.17 * r, 0, 360, 0.07 * r, 0, 1.2 * r), gold),        # khoen treo
                                  (rrect(0.34 * r, 0.22 * r, 0.06 * r, 0, 1.0 * r), gold_l),
                                  (ell(r, r), gold), (ell(0.9 * r, 0.9 * r), gold_l), (ell(0.78 * r, 0.78 * r), glass),
                                  (arc(0.62 * r, 105, 160, 0.07 * r), "#9FCBF5"),               # ánh trên mặt kính
                                  (ell(0.2 * r, 0.09 * r, -0.4 * r, -0.42 * r), "#CFE6FA"), (ell(0.18 * r, 0.08 * r, 0.42 * r, -0.4 * r), "#CFE6FA"),
                                  (diamond(0, 0.89 * r, 0.1 * r), gem), (diamond(-0.89 * r, 0, 0.1 * r), gem),
                                  (diamond(0.89 * r, 0, 0.1 * r), gem),
                                  (ell(0.3 * r, 0.17 * r, -0.28 * r, -0.86 * r), cream), (ell(0.34 * r, 0.2 * r, 0.12 * r, -0.9 * r), cream),
                                  (diamond(0, -0.96 * r, 0.1 * r), gem)])
    c.needle = node(f"{name}_Needle", c.root, (0.0, 0.0), -0.004)
    R = 0.42 * r
    part(f"{name}_Star", c.needle, [(star(R, 0, 0, 8, 0.42), "#DDEFFF"),
                                    ([(0, 1.5 * R), (0.17 * R, 0.12 * R), (0, -0.12 * R), (-0.17 * R, 0.12 * R)], "#FFD54A"),   # đầu chỉ
                                    (diamond(0, 1.5 * R, 0.13 * R), gem), (ell(0.2 * R, 0.2 * R), "#F6FBFF")])
    if flash:
        k = r / 0.065                                                         # cỡ đo theo la bàn cầm tay (r = 0.065)
        c.flash = part(f"{name}_Flash", c.root, [(ell(0.09 * k, 0.09 * k), "#FFE27A")]   # quầng nhỏ sau vỏ, nhô ra thành tia
                       + [(band([(0.075 * k * math.cos(a), 0.075 * k * math.sin(a)), (0.125 * k * math.cos(a), 0.125 * k * math.sin(a))],
                                0.016 * k), "#FFE27A") for a in (math.radians(j * 45 + 22.5) for j in range(8))], 0.008)
        c.bright = part(f"{name}_Bright", c.root, [(ell(0.051 * k, 0.051 * k), "#FFF3B0"), (ell(0.03 * k, 0.03 * k), "#FFFBE6")],
                        -0.0035)                                              # mặt kính sáng bừng (sau mũi sao)
    return c


def palm(p, name, far=False, y=-0.008):
    """Nút ở lòng bàn tay gần (far=True: tay xa) của Lumo để gắn đồ cầm (la bàn, bản đồ); xoay ngược góc tay bằng chold()
    để đồ luôn đứng thẳng theo thân."""
    return node(name, p.arm_far if far else p.arm, (0.0, -0.21), y)


def build_holder(p, r, name, far=False):
    """La bàn bán kính r đứng thẳng trên lòng bàn tay gần (far=True: tay xa). Trả về (nút cầm, la bàn)."""
    h = palm(p, f"{name}_Hold", far)
    return h, build_compass(name, h, (0.0, r + 0.004), -0.004, r)


def chold(p, h, t, near=None, far=None, hf=None, off=6):
    """Xoay tay gần (near) và tay xa (far), độ; nút cầm h ở tay gần, hf ở tay xa (nếu có) xoay ngược lại nên đồ trong tay
    luôn đứng thẳng theo thân dù tay xoay. far bỏ trống: tay xa theo tay gần, lệch off độ (off=None: để yên tay xa).
    near bỏ trống: để yên tay gần."""
    if near is not None:
        ry(p.arm, t, near)
        if h is not None:
            ry(h, t, -near)
        if far is None and off is not None:
            far = near + off
    if far is not None:
        ry(p.arm_far, t, far)
        if hf is not None:
            ry(hf, t, -far)


def compass_bits(c, r):
    """Lớp bụi phủ mặt kính la bàn bán kính r (che cả mũi sao); lau sạch thì show(…, False)."""
    return part(f"{c.name}_Dust", c.root, [(ell(0.82 * r, 0.82 * r), "#BBA98A"), (ell(0.5 * r, 0.3 * r, -0.2 * r, 0.25 * r), "#C9B999"),
                                           (ell(0.25 * r, 0.18 * r, 0.35 * r, -0.3 * r), "#A99678"),
                                           (ell(0.12 * r, 0.1 * r, -0.4 * r, -0.35 * r), "#A99678")], -0.008)


def glow(c, t, s):
    """Mức sáng của la bàn (quầng c.glow): s = 0 tắt; 0.55–0.8 le lói (quầng vừa nhô khỏi vỏ, còn xa); 1.0–1.4 sáng mạnh
    (ngay sát điều kỳ lạ)."""
    show(c.glow, t, s > 0)
    if s > 0:
        scl(c.glow, t, s, s)


def beep(c, t, s0=0.65, s1=1.0):
    """Một tiếng TÍT: quầng nháy từ mức s0 lên s1 rồi về s0. Kêu dày dần, sáng dần là đang tới gần."""
    scl(c.glow, t - 0.05, s0, s0)
    scl(c.glow, t + 0.04, s1, s1)
    scl(c.glow, t + 0.2, s0, s0)


def buzz(spans, amp=3.0, step=0.07):
    """Hàm rung cho aim(wob=…): mũi sao run ±amp độ nhân hệ số k trong các quãng (t0, t1, k)."""
    def wob(t):
        for t0, t1, k in spans:
            if t0 <= t <= t1:
                return amp * k * (1 if int(t / step) % 2 else -1)
        return 0.0
    return wob


def compass_flash(c, t):
    """La bàn lóe theo đài thiên văn (la bàn dựng với flash=True): tia nhỏ nhô quanh vỏ, mặt kính sáng bừng, cùng nhịp
    glow_flash(); không rung, không kêu."""
    glow_flash(c.flash, t, lit=c.bright)


def glide(a, b, t0, t1):
    """Mục tiêu cho aim(): trượt từ điểm a sang điểm b trong [t0, t1], êm đầu êm cuối (mũi sao chuyển sang điều kỳ lạ kế
    tiếp)."""
    def tgt(t):
        u = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
        u = u * u * (3 - 2 * u)
        return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)
    return tgt


def swing(targets, spans, wob=9.0):
    """Hướng cho aim(bearing=…): mũi sao lần lượt chuyển từ targets[0] sang targets[1], targets[2]… trong các quãng spans
    [(t0, t1)]: quay theo góc, đường ngắn nhất, êm đầu êm cuối, tới nơi thì lắc tắt dần (biên độ wob độ). Khác glide():
    glide trượt điểm mục tiêu, swing xoay hướng."""
    def bearing(t, p):
        angs = [math.degrees(math.atan2(q[0] - p[0], q[1] - p[1])) for q in targets]
        for (t0, t1), a, b in zip(spans, angs, angs[1:]):
            if t < t0:
                return a
            if t < t1 + 0.45:
                u = min(1.0, max(0.0, (t - t0) / (t1 - t0)))
                u = u * u * (3 - 2 * u)
                w = wob * math.exp(-6 * (t - t1)) * math.sin(18 * (t - t1)) if t > t1 else 0.0
                return a + ((b - a + 180) % 360 - 180) * u + w
        return angs[-1]
    return bearing


def aim(c, t0, t1, target=None, wob=None, prev=None, step=1, bearing=None, flat=False):
    """Key mũi sao của la bàn c (mỗi step khung một key trong [t0, t1]) để đầu chỉ luôn hướng về mục tiêu trong thế giới:
    từng khung frame_set rồi đọc ma trận thế giới của vỏ (đã gồm góc tay, nghiêng người, lật gương, tung hứng), đổi hướng
    tới mục tiêu về hệ của vỏ. Chạy sau khi đã key xong mọi chuyển động khác.
    target: điểm (x, z), hoặc hàm t -> (x, z) cho mục tiêu di chuyển (glide()); bearing: thay cho target, hàm
    (t, (x, z) của vỏ) -> hướng thế giới (độ, chiều kim đồng hồ, 0 là lên), như swing(). wob(t) cộng thêm độ (rung buzz(),
    vọt quá). prev: góc khung trước để nối liền, không quay vòng thừa. flat=True: chỉ bù góc xoay và lật gương của vỏ, bỏ
    qua co giãn của thân (lệch chút khi Lumo nhún; cách tính của Cảnh 5 tập 000A, giữ để hình không đổi). Trả về góc cuối.
    Khung la bàn đang ẩn (show False) thì ma trận không được cập nhật, key ở khung đó sai: step = 1 không lộ (khung hiện
    nào cũng có key riêng), step > 1 thì cho t0 rơi vào khung la bàn đã hiện, nếu không khung hiện đầu tiên bị nội suy lệch."""
    sc = bpy.context.scene
    dg = bpy.context.evaluated_depsgraph_get()
    for f in range(fr(t0), fr(t1) + 1, step):
        t = (f - 1) / FPS
        sc.frame_set(f)
        mw = c.root.evaluated_get(dg).matrix_world
        m = mw.to_3x3()
        if abs(m.determinant()) < 1e-7:                                       # đang lật gương, bề ngang bằng 0
            continue
        p = mw.translation
        if bearing is not None:
            a = math.radians(bearing(t, (p.x, p.z)))
            v = m.inverted() @ Vector((math.sin(a), 0.0, math.cos(a)))
            phi = math.degrees(math.atan2(v.x, v.z))
        else:
            tx, tz = target(t) if callable(target) else target
            if flat:
                up = m @ Vector((0.0, 0.0, 1.0))
                base = math.degrees(math.atan2(up.x, up.z))
                phi = (1 if m.determinant() > 0 else -1) * (math.degrees(math.atan2(tx - p.x, tz - p.z)) - base)
            else:
                d = m.inverted() @ Vector((tx - p.x, 0.0, tz - p.z))
                phi = math.degrees(math.atan2(d.x, d.z))
        if prev is not None:
            phi += 360 * round((prev - phi) / 360)
        prev = phi
        c.needle.rotation_euler = (0.0, math.radians(phi + (wob(t) if wob else 0.0)), 0.0)
        c.needle.keyframe_insert("rotation_euler", frame=f)
    return prev


# ================================================================ nhân vật nền, đạo cụ EP000A (Character Bible; ảnh trong 02_ASSET_LIBRARY)
def build_bird(x, z, layer):
    """Chú chim nhỏ cỡ nắm tay Lumo: nâu hạt dẻ, bụng kem, má hồng, chỏm lông, đuôi cuộn. Dựng quay mặt về +X, gốc ở
    chân. b.wing khớp ở vai: ry -60…-98 là vỗ lên bụng (cười), +60 là giương cánh; b.wing_far cho lúc bay. Mắt, mỏ:
    bird_eyes(b, t, "open" | "closed" | "happy"), bird_beak(b, t, "closed" | "open")."""
    brown, wingc, cream, cheek, beak, leg = "#B66A3C", "#8F4B27", "#F3DAB4", "#EF9A98", "#9C5428", "#8A4A26"
    b = SimpleNamespace(name="Bird", dir=1)
    b.root = node("Bird", None, (x, z), layer)
    b.wing_far = part("Bird_WingFar", b.root, [(ell(0.02, 0.011, -0.012, -0.008), wingc)], 0.006, (-0.002, 0.058))
    part("Bird_Tail", b.root, [(band(curve((-0.02, 0.03), (-0.05, 0.03), (-0.052, 0.06)), 0.012), brown),
                               (arc(0.009, -90, 200, 0.008, -0.044, 0.064), brown)], 0.004)
    part("Bird_Legs", b.root, [(rrect(0.005, 0.016, 0.0025, -0.007, 0.008), leg), (rrect(0.005, 0.016, 0.0025, 0.008, 0.008), leg),
                               (ell(0.007, 0.003, -0.005, 0.002), leg), (ell(0.007, 0.003, 0.01, 0.002), leg)], 0.002)
    part("Bird_Body", b.root, [(ell(0.034, 0.03, 0.0, 0.045), brown), (ell(0.022, 0.021, 0.011, 0.04), cream)])
    b.head = node("Bird_Head", b.root, (0.006, 0.068), -0.002)
    part("Bird_Skull", b.head, [(turn(ell(0.0045, 0.013, 0.0, 0.041), a, 0.0, 0.03), brown) for a in (12, 34, 56)]   # chỏm lông
                               + [(ell(0.028, 0.026, 0.0, 0.012), brown), (ell(0.018, 0.016, 0.012, 0.006), cream),
                                  (ell(0.0065, 0.005, 0.019, -0.002), cheek)])
    b.beak = {"closed": part("Bird_Beak", b.head, [([(0.026, 0.012), (0.026, 0.0), (0.04, 0.006)], beak)], -0.002),
              "open": part("Bird_BeakOpen", b.head, [([(0.026, 0.015), (0.026, 0.007), (0.041, 0.013)], beak),
                                                     ([(0.026, 0.004), (0.026, -0.003), (0.037, -0.002)], beak),
                                                     ([(0.026, 0.008), (0.026, 0.004), (0.034, 0.006)], MOUTH_IN)], -0.002)}
    eye = node("Bird_Eye", b.head, (0.013, 0.014), -0.003)
    b.eyes = {"open": part("Bird_EyeOpen", eye, [(ell(0.0055, 0.007), DARK), (ell(0.0018, 0.0022, 0.0015, 0.0025), WHITE)]),
              "closed": part("Bird_EyeClosed", eye, [(rrect(0.011, 0.0022, 0.001), DARK)]),
              "happy": part("Bird_EyeHappy", eye, [(arc(0.005, 20, 160, 0.0022, 0, -0.002), DARK)])}
    b.wing = part("Bird_Wing", b.root, [(ell(0.022, 0.012, -0.012, -0.01), wingc), (ell(0.008, 0.005, -0.028, -0.015), cream)],
                  -0.004, (-0.002, 0.058))
    return b


def bird_beak(b, t, k):
    for name, ob in b.beak.items():
        show(ob, t, name == k)


def bird_eyes(b, t, k):
    for name, ob in b.eyes.items():
        show(ob, t, name == k)


def build_bfly(name, layer):
    """Bướm phát sáng cỡ một ngón tay Lumo (cao khoảng 0.06, nhỏ hơn chú chim): mỗi cánh hai thuỳ hồng đào, thuỳ trên lớn,
    lõi cánh sáng gần trắng thay cho quầng sáng (Workbench vẽ quầng thành một cái đĩa có viền); cánh xa sẫm hơn để thấy
    dáng hai cánh; hai râu cuộn. Dựng nhìn nghiêng, đầu về +X, gốc đặt ngoài khung (0, 6); cánh vỗ bằng flap()."""
    f = SimpleNamespace(name=name)
    f.root = node(name, None, (0.0, 6.0), layer)
    f.wings = [part(f"{name}_WingFar", f.root, [(turn(ell(0.02, 0.027, -0.014, 0.032), 22, 0, 0), "#E8957F"),
                                                (turn(ell(0.013, 0.015, -0.016, 0.008), -25, 0, 0), "#E8957F")], 0.004),
               part(f"{name}_Wing", f.root, [(turn(ell(0.022, 0.031, -0.007, 0.034), 15, 0, 0), "#F7A98F"),
                                             (turn(ell(0.015, 0.017, -0.011, 0.009), -30, 0, 0), "#F7A98F"),
                                             (turn(ell(0.012, 0.018, -0.007, 0.034), 15, 0, 0), "#FFF1E8"),
                                             (turn(ell(0.007, 0.008, -0.011, 0.009), -30, 0, 0), "#FFF1E8")], -0.004)]
    part(f"{name}_Body", f.root, [(ell(0.014, 0.006, -0.003, 0.0), "#F2C39C"), (ell(0.007, 0.007, 0.012, 0.004), "#F2C39C")]
         + [s for dx in (0.0, 0.006) for s in ((band(curve((0.013 + dx, 0.009), (0.016 + dx, 0.024), (0.024 + dx, 0.03)), 0.0025), "#E8A88A"),
                                                (arc(0.004, -90, 200, 0.0025, 0.024 + dx, 0.026), "#E8A88A"))])
    return f


def flap(f, t0, t1, period=0.14, low=-0.5):
    """Bướm vỗ cánh trong [t0, t1] bằng scale Z (âm là cánh đập xuống); đậu thì vỗ chậm, cánh dựng: period 0.9, low 0.55."""
    for i, t in enumerate(steps(t0, t1, period / 2)):
        for w in f.wings:
            scl(w, t, 1.0, low if i % 2 else 1.0)


def cloud_parts(w, h, cx=0.0, cz=0.0, col="#D6C7AB", ang=0.0):
    """Đám mây khắc ba múi đáy phẳng (phù điêu, cửa khắc mây, bệ đá trong phế tích EP000A): đế bo tròn và ba múi tròn
    cùng màu chồng lên nhau, Workbench chỉ vẽ viền quanh cả khối. ang: xoay quanh tâm (độ, theo chiều kim đồng hồ). Trả
    về danh sách (điểm, màu) cho part()."""
    shapes = [rrect(w, h * 0.42, h * 0.2, cx, cz - h * 0.29), ell(w * 0.21, h * 0.34, cx - w * 0.29, cz - h * 0.14),
              ell(w * 0.27, h * 0.5, cx - w * 0.04, cz), ell(w * 0.22, h * 0.38, cx + w * 0.26, cz - h * 0.08)]
    return [(turn(pts, -ang, cx, cz) if ang else pts, col) for pts in shapes]


def map_card(w=0.1, h=0.2):
    """Bản đồ giấy trong tay Lumo nhìn nghiêng (thu hẹp ngang), đúng chiều: mũi tên đỏ chỉ xuống, rương vàng dưới mũi
    tên. Cầm ngược là xoay nửa vòng (ry 180). Gắn vào tay thì đặt ở nút palm() của bàn tay, xoay tay bằng chold() để tấm
    bản đồ đứng thẳng."""
    return [(rrect(w + 0.01, h + 0.01, 0.012), "#C9A66E"), (rrect(w, h, 0.01), "#F2DDB0"),
            (rrect(0.004, h * 0.9, 0.002, -w * 0.2, 0), "#E2C793"), (rrect(0.004, h * 0.9, 0.002, w * 0.2, 0), "#E2C793"),
            (ell(0.016, 0.01, -w * 0.25, h * 0.32), "#8CC65A"), (ell(0.014, 0.009, w * 0.15, h * 0.2), "#8CC65A"),
            (rrect(0.018, 0.05, 0.004, 0.0, -0.002), "#E8503A"), ([(-0.026, -0.026), (0.026, -0.026), (0.0, -0.056)], "#E8503A"),
            (ell(0.019, 0.012, 0.0, -0.072, 0, 180), "#B07A44"), (rrect(0.038, 0.022, 0.004, 0.0, -0.083), "#E0A83A")]


MAP_ISLES = ((-0.22, 0.2, "water"), (0.05, 0.16, "mount"), (-0.22, 0.02, "ruin"), (0.05, -0.04, "crystal"), (-0.22, -0.16, "pink"))
MAP_OBS = (0.25, -0.02)                                                       # đảo có đài thiên văn: chỉ có trên bản đồ khắc
TEAL, TEAL_L, TEAL_M = "#35DCC8", "#A8FBEF", "#7FEBDD"                        # xanh ngọc tín hiệu của Wonder Hub (khác vàng của la bàn)


def _grow(pts, s, cx, cz):
    """Phóng to hay thu nhỏ một hình quanh (cx, cz) (viền nổi của hình khắc)."""
    return [(cx + (x - cx) * s, cz + (z - cz) * s) for x, z in pts]


def _carved_isle(cx, cz, kind, fill, light, line):
    """Một đảo khắc trên đá (đế đá, mặt cỏ, vật trên đảo); mỗi hình đi sau một hình viền đậm to hơn chút."""
    rock = [(cx - 0.08, cz), (cx + 0.08, cz), (cx + 0.04, cz - 0.05), (cx, cz - 0.08), (cx - 0.045, cz - 0.05)]
    out = [(_grow(rock, 1.15, cx, cz - 0.03), line), (rock, fill), (ell(0.09, 0.024, cx, cz), line), (ell(0.084, 0.018, cx, cz), light)]
    if kind == "mount":
        out += [([(cx - 0.055, cz), (cx + 0.045, cz), (cx - 0.005, cz + 0.09)], line),
                ([(cx - 0.04, cz + 0.005), (cx + 0.03, cz + 0.005), (cx - 0.005, cz + 0.075)], fill)]
    elif kind == "ruin":
        out += [(rrect(0.016, 0.055, 0.003, cx - 0.03, cz + 0.028), line), (rrect(0.01, 0.048, 0.003, cx - 0.03, cz + 0.028), fill),
                (rrect(0.05, 0.016, 0.004, cx - 0.015, cz + 0.055), line), (rrect(0.044, 0.01, 0.003, cx - 0.015, cz + 0.055), fill)]
    elif kind == "crystal":
        out += [([(cx - 0.035, cz), (cx - 0.005, cz), (cx - 0.02, cz + 0.065)], line),
                ([(cx - 0.028, cz + 0.004), (cx - 0.012, cz + 0.004), (cx - 0.02, cz + 0.05)], fill)]
    elif kind == "obs":
        out += [(rrect(0.11, 0.035, 0.006, cx - 0.005, cz + 0.02), line), (rrect(0.1, 0.027, 0.005, cx - 0.005, cz + 0.02), fill),
                (ell(0.044, 0.042, cx - 0.01, cz + 0.035, 0, 180), line), (ell(0.037, 0.035, cx - 0.01, cz + 0.038, 0, 180), light),
                (rrect(0.038, 0.026, 0.004, cx + 0.065, cz + 0.014), line), (rrect(0.032, 0.02, 0.004, cx + 0.065, cz + 0.014), fill)]
    else:
        out += [(ell(0.044, 0.038, cx + 0.02, cz + 0.055), line), (ell(0.035, 0.029, cx + 0.02, cz + 0.057), fill)]
    if kind == "water":
        out += [(rrect(0.024, 0.064, 0.004, cx + 0.05, cz - 0.02), line), (rrect(0.016, 0.056, 0.004, cx + 0.05, cz - 0.02), light)]
    return out


def map_big(stone=False):
    """Bản đồ giấy nhìn thẳng cho cú cận (02_ASSET_LIBRARY/Props/Paper_Map/concept/paper_map_ref.png), rộng 0.72, đúng
    chiều: năm đảo, đường chấm, mũi tên đỏ chỉ xuống, rương; mép phải là biển mây trống (chỗ bản đồ khắc có thêm hòn đảo
    có đài thiên văn). stone=True: bản đồ khắc trên đá ở bệ đá (Cảnh 4 tập 000A), rộng 0.78: cùng năm đảo khắc nổi có
    viền, mây khắc, không đường chấm, mũi tên, rương; thêm đảo nhỏ có đài thiên văn mái vòm ở MAP_OBS (lóe bằng
    map_obs_glow())."""
    if stone:
        stone_c, stone_d, stone_l = "#C9BBA2", "#A8987E", "#D9CCB4"            # đá phế tích
        shapes = [(rrect(0.78, 0.72, 0.05), stone_d), (rrect(0.74, 0.68, 0.045), "#D6C8AE")]
        for cx, cz in ((0.05, 0.27), (-0.08, -0.27), (0.25, 0.22), (0.25, -0.24), (-0.32, 0.27)):   # mây khắc
            shapes += [(arc(0.035, 20, 160, 0.008, cx - 0.025, cz), stone_d), (arc(0.045, 20, 160, 0.008, cx + 0.03, cz + 0.005), stone_d)]
        for cx, cz, kind in MAP_ISLES + ((*MAP_OBS, "obs"),):
            shapes += _carved_isle(cx, cz, kind, stone_c, stone_l, stone_d)
        return shapes
    shapes = [(rrect(0.75, 0.69, 0.05), "#D8B784"), (rrect(0.72, 0.66, 0.05), "#F0D9A8"),
              (rrect(0.006, 0.62, 0.003, -0.12, 0), "#E3C48F"), (rrect(0.006, 0.62, 0.003, 0.12, 0), "#E3C48F")]
    dots = [(-0.22, 0.2), (0.05, 0.16), (-0.22, 0.02), (0.05, -0.04), (-0.22, -0.16), (0.05, -0.2)]
    for (x0, z0), (x1, z1) in zip(dots, dots[1:]):
        for k in range(1, 6):
            u = k / 6
            shapes.append((rrect(0.016, 0.008, 0.003, x0 + (x1 - x0) * u, z0 + (z1 - z0) * u - 0.03), "#9A6A3C"))
    for cx, cz, kind in MAP_ISLES:
        shapes += [([(cx - 0.08, cz), (cx + 0.08, cz), (cx + 0.04, cz - 0.05), (cx, cz - 0.08), (cx - 0.045, cz - 0.05)], "#B98F6A"),
                   (ell(0.085, 0.02, cx, cz), "#8CC65A")]
        if kind == "mount":
            shapes += [([(cx - 0.05, cz), (cx + 0.04, cz), (cx - 0.005, cz + 0.08)], "#B98F6A"),
                       ([(cx - 0.02, cz + 0.05), (cx + 0.01, cz + 0.05), (cx - 0.005, cz + 0.08)], WHITE)]
        elif kind == "ruin":
            shapes += [(rrect(0.012, 0.05, 0.003, cx - 0.03, cz + 0.025), "#E4D3B0"), (rrect(0.012, 0.05, 0.003, cx + 0.0, cz + 0.025), "#E4D3B0"),
                       (rrect(0.045, 0.012, 0.004, cx - 0.015, cz + 0.05), "#E4D3B0")]
        elif kind == "crystal":
            shapes += [([(cx - 0.03, cz), (cx - 0.01, cz), (cx - 0.02, cz + 0.06)], "#A8DDF2"),
                       ([(cx - 0.01, cz), (cx + 0.01, cz), (cx, cz + 0.045)], "#A8DDF2")]
        else:
            shapes += [(rrect(0.012, 0.04, 0.004, cx + 0.02, cz + 0.02), "#8B5E3C"),
                       (ell(0.035, 0.03, cx + 0.02, cz + 0.055), "#F2A7C3" if kind == "pink" else "#6FAE45")]
        if kind == "water":
            shapes.append((rrect(0.018, 0.06, 0.004, cx + 0.05, cz - 0.02), "#7CC6EE"))
    for cx, cz in ((0.25, 0.2), (0.24, 0.05), (0.26, -0.1), (0.24, -0.24), (0.0, 0.27), (-0.1, -0.28)):   # biển mây trống
        shapes += [(arc(0.035, 20, 160, 0.006, cx - 0.025, cz), "#9DB8D9"), (arc(0.045, 20, 160, 0.006, cx + 0.03, cz + 0.005), "#9DB8D9")]
    ax = 0.05
    shapes += [(rrect(0.05, 0.07, 0.008, ax, -0.125), "#E8503A"), ([(ax - 0.055, -0.155), (ax + 0.055, -0.155), (ax, -0.205)], "#E8503A"),
               (ell(0.05, 0.028, ax, -0.235, 0, 180), "#C28A4E"), (rrect(0.1, 0.05, 0.01, ax, -0.262), "#B07A44"),
               (rrect(0.104, 0.008, 0.003, ax, -0.237), "#E8B33A"), (rrect(0.104, 0.008, 0.003, ax, -0.284), "#E8B33A"),
               (rrect(0.02, 0.024, 0.004, ax, -0.245), "#E8B33A"), (ell(0.004, 0.005, ax, -0.247), DARK)]
    shapes += [(turn(rrect(0.022, 0.006, 0.003, ax + dx, -0.26 + dz), a, ax + dx, -0.26 + dz), "#F2C14E")
               for dx, dz, a in ((-0.085, 0.02, -20), (-0.085, -0.02, 20), (0.085, 0.02, 20), (0.085, -0.02, -20))]
    return shapes


def map_obs_glow(col=TEAL, light=TEAL_L):
    """Đài thiên văn trên bản đồ khắc lóe xanh ngọc: chính hình đảo và đài tô xanh, kèm vài tia ngắn (không dùng đĩa sáng
    che hình). Toạ độ tính từ tâm đảo: đặt part ở chỗ MAP_OBS của bản đồ."""
    sh = [(s, col if c == "line" else light) for s, c in _carved_isle(*MAP_OBS, "obs", "fill", "fill", "line")]
    cx, cz = MAP_OBS[0] - 0.005, MAP_OBS[1] + 0.04
    sh += [(band([(cx + dx * 0.55, cz + dz * 0.55), (cx + dx, cz + dz)], 0.012), col) for dx, dz in
           ((-0.15, 0.0), (-0.11, 0.1), (0.0, 0.15), (0.11, 0.1), (0.15, 0.0))]
    return [([(x - MAP_OBS[0], z - MAP_OBS[1]) for x, z in pts], c) for pts, c in sh]


def hub_shapes(cx, cz, s):
    """Wonder Hub nhìn từ xa (đài thiên văn mái vòm): dáng Hub_House ở previz 2D Cảnh 2 tập 01
    (Previz_2D/EP001_Great_Rain_Experiment/scene02/build_shot.py) thu theo s, gốc ở tâm nền nhà; nan hoa vàng trong ô cửa
    tròn như ảnh wonder_hub_island_hero.png."""
    gold = "#E8B33A"
    w = (cx, cz + 0.28 * s)
    spokes = [(band([(w[0] - 0.19 * s * math.cos(a), w[1] - 0.19 * s * math.sin(a)),
                     (w[0] + 0.19 * s * math.cos(a), w[1] + 0.19 * s * math.sin(a))], 0.025 * s), gold)
              for a in (0.0, math.pi / 3, 2 * math.pi / 3)]
    return ([(rrect(1.4 * s, 0.3 * s, 0.06 * s, cx, cz), "#EFE2C4"), (ell(0.66 * s, 0.55 * s, cx, cz + 0.15 * s, 0, 180), "#B9A6E8"),
             (arc(0.66 * s, 0, 180, 0.03 * s, cx, cz + 0.15 * s), gold), (rrect(0.24 * s, 0.3 * s, 0.1 * s, cx + 0.55 * s, cz), "#C9B48E"),
             (ell(0.24 * s, 0.24 * s, *w), gold), (ell(0.2 * s, 0.2 * s, *w), "#2E2347")]
            + spokes + [(ell(0.045 * s, 0.045 * s, *w), gold)])


def build_hub_island(root, name="Island"):
    """Hòn đảo có Wonder Hub ở chân trời, dựng vào node root (gốc ở chân đảo, cảnh tự đặt chỗ và scale thu nhỏ; đảo rộng
    khoảng 1.8, cao 1.0 trước khi thu): đảo đồi cỏ (part tên name), đài thiên văn mái vòm (hub_shapes), quầng xanh ngọc
    sau mái vòm nhô ra thành tia (h.flash) và mái vòm, ô cửa sáng xanh (h.tint). h.flash, h.tint mặc định hiện, cảnh tự ẩn
    từ giây 0; lóe bằng glow_flash(h.flash, t, lit=h.tint). Sương chân đảo do cảnh thêm."""
    hub_x, hub_z, hub_s = -0.12, 0.2, 0.42                                    # tâm nền đài thiên văn, cỡ (toạ độ đảo)
    hill = [(-0.78, 0.04), (-0.62, 0.2), (-0.45, 0.42), (-0.28, 0.66), (-0.12, 0.86), (0.02, 0.97), (0.14, 1.0), (0.26, 0.93),
            (0.42, 0.74), (0.58, 0.5), (0.74, 0.28), (0.9, 0.06)]
    h = SimpleNamespace(root=root)
    part(name, root, [(rect(-0.82, -0.14, 0.94, 0.08), "#B58C70"), (hill, "#82AE57"), (hill[:7] + [(0.02, 0.05), (-0.78, 0.04)], "#93BF63")]
         + [(ell(rx, rz, cx, cz), col) for rx, rz, cx, cz, col in (
             (0.09, 0.07, -0.5, 0.36, "#6F9E4A"), (0.08, 0.06, -0.3, 0.6, "#6F9E4A"), (0.07, 0.06, 0.28, 0.84, "#6F9E4A"),
             (0.09, 0.07, 0.52, 0.5, "#6F9E4A"), (0.06, 0.05, 0.7, 0.24, "#F0B3C8"), (0.06, 0.05, -0.62, 0.18, "#F0B3C8"),
             (0.05, 0.04, 0.1, 0.92, "#F0B3C8"))]
         + [(band([(x, -0.1), (x + 0.03, 0.06)], 0.012), "#9C7560") for x in (-0.6, -0.3, 0.1, 0.45, 0.75)], 0.1)
    h.flash = part("Hub_Flash", root, [(ell(0.34, 0.29), TEAL)]
                   + [(band([(0.3 * math.cos(a), 0.25 * math.sin(a)), (0.44 * math.cos(a), 0.37 * math.sin(a))], 0.03), TEAL)
                      for a in (math.radians(k * 30 + 15) for k in range(12))], 0.05, (hub_x, hub_z + 0.15 * hub_s))
    part("Hub", root, hub_shapes(hub_x, hub_z, hub_s), 0.0)
    h.tint = part("Hub_FlashDome", root, [(ell(0.66 * hub_s, 0.55 * hub_s, hub_x, hub_z + 0.15 * hub_s, 0, 180), TEAL_M),
                                          (ell(0.2 * hub_s, 0.2 * hub_s, hub_x, hub_z + 0.28 * hub_s), "#D2FFF8")], -0.01)
    return h


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
