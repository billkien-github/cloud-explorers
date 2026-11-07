"""
Previz khối post-credit tập 000A (cảnh 6, 5 giây, gài EP000B) dẫn Seedance (04_PRODUCTION/SEEDANCE.md): bãi phế liệu
lúc hoàng hôn, hộp kim loại phủ bụi nắp hé, Inventor Pack trong hộp, hòn đảo có Wonder Hub ở chân trời; dạng khối
(pipeline/blocks.py). Mọi mốc lấy từ timing.py của previz 2D (TIMING trong build_shot.py của đoạn), không gõ lại số.
Diễn theo previz 2D đã chốt: 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh06/.
Một đoạn: sh150 (0–5 s, S1). Không có nhân vật: chỉ máy đẩy chậm vào chiếc hộp và hai cú lóe cùng nhịp.
Toạ độ (m): đất ở Z 0, hộp ở giữa (X ±0.45, Y ±0.28, cao 0.46), bản lề nắp ở mép sau; máy phía -Y nhìn về +Y. Hai đống
phế liệu hai bên hộp; mép bãi ở Y 8, sau đó là biển mây (Z -3). Hòn đảo có đài thiên văn ở Y 60, lệch phải (X 12): ở chân
trời, phía trên bên phải quai hộp như ảnh junkyard_hero.png; mặt trời sát chân trời bên trái.
Lóe (HUB_FLASH = PACK_FLASH): cùng một nhịp PULSE của previz 2D (pipeline/cutout.py) cho quầng đài thiên văn và quầng ở
khe nắp; mái vòm và lòng hộp sáng bừng 0.7 giây cùng nhịp; sau đó khe nắp còn le lói xanh tới hết cảnh. Mọi khối sáng ẩn
bằng scale 0 ngoài lúc lóe.
Màu: bối cảnh, đạo cụ xám (không có nhân vật); ánh lóe xanh ngọc phát sáng.
"""
import importlib.util
import math
import pathlib
import sys

import bmesh
import bpy
from bpy_extras import anim_utils
from mathutils import Matrix, Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.path.insert(0, str(ROOT / "pipeline"))
from blocks import *  # noqa: E402,F403  khối, vật liệu, keyframe theo giây, máy quay

HOLD = 1 / 24                                                    # một khung: key ẩn và key hiện cách nhau ít hơn thì rơi vào cùng khung
PULSE = ((0.0, 0.25), (0.1, 1.25), (0.3, 0.95), (0.5, 1.12), (0.85, 0.0))   # nhịp lóe của Wonder Hub, như PULSE của cutout.py
LIT = 0.7                                                        # mái vòm, lòng hộp sáng bừng 0.7 giây (glow_flash của cutout.py)
HINGE = Vector((0.0, 0.28, 0.46))                                # bản lề nắp hộp, mép sau trên
LID_OPEN = -16                                                   # nắp hé: mép trước nhấc lên khoảng 0.16
GAP = Vector((0.0, -0.30, 0.54))                                 # giữa khe nắp, mặt trước
DOME = Vector((12.0, 60.0, -0.9))                                 # tâm mái vòm đài thiên văn trên hòn đảo
SEA_Z = -3.0


def load_timing(timing):
    spec = importlib.util.spec_from_file_location("canh06_timing", ROOT / timing)
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    return tm


def cube(bm, size, mat=Matrix.Identity(4)):
    """Hộp cỡ size, đặt theo ma trận mat (dời, xoay)."""
    bmesh.ops.create_cube(bm, size=1.0, matrix=mat @ Matrix.Diagonal((*size, 1)))
    return bm


def ring_bm(r, th, depth, center, n=20, bm=None):
    """Vành tròn trong mặt XZ (mặt hướng về máy): n đoạn hộp, dày th, sâu depth theo Y."""
    bm = bm or bmesh.new()
    seg = 2 * math.pi * r / n * 1.15
    for i in range(n):
        a = 2 * math.pi * i / n
        m = Matrix.Translation(Vector(center) + Vector((r * math.cos(a), 0, r * math.sin(a)))) @ Matrix.Rotation(-a, 4, "Y")
        cube(bm, (th, depth, seg), m)
    return bm


def spokes_bm(r, th, depth, center, n=3, a0=0.3, bm=None):
    """n nan hoa qua tâm, trong mặt XZ."""
    bm = bm or bmesh.new()
    for i in range(n):
        a = a0 + math.pi * i / n
        cube(bm, (2 * r, depth, th), Matrix.Translation(center) @ Matrix.Rotation(-a, 4, "Y"))
    return bm


def gear_bm(r, depth, center, teeth=10, bm=None):
    """Bánh răng mặt hướng về máy: đĩa trục Y, răng hộp quanh vành."""
    bm = cyl_bm(r, depth, center, axis="Y", bm=bm, segs=24)
    tw, tl = 2 * math.pi * r / teeth * 0.45, 0.22 * r
    for i in range(teeth):
        a = 2 * math.pi * i / teeth
        m = Matrix.Translation(Vector(center) + Vector(((r + tl / 2 - 0.02) * math.cos(a), 0, (r + tl / 2 - 0.02) * math.sin(a))))
        cube(bm, (tl, depth, tw), m @ Matrix.Rotation(-a, 4, "Y"))
    return bm


def prism_x(profile, x0, x1, bm=None):
    """Lăng trụ: đa giác (y, z) kéo dài theo X từ x0 tới x1."""
    bm = bm or bmesh.new()
    a = [bm.verts.new((x0, y, z)) for y, z in profile]
    b = [bm.verts.new((x1, y, z)) for y, z in profile]
    bm.faces.new(list(reversed(a)))
    bm.faces.new(b)
    n = len(profile)
    for i in range(n):
        bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    return bm


def linear(ob):
    """Mọi key của ob nội suy LINEAR (máy di chuyển đều: để ease thì Seedance dồn chuyển động thành một cú vụt)."""
    ad = ob.animation_data
    for fc in anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"


def build(timing, offset, seconds, out_blend, segment=None):
    """seconds: độ dài video render (số nguyên giây Seedance nhận); segment: độ dài đoạn trong cảnh. Từ segment tới
    seconds máy vẫn đẩy tiếp cùng tốc độ (chỗ cắt không rơi vào lúc máy dừng), lúc dựng cắt bỏ."""
    segment = seconds if segment is None else segment
    tm = load_timing(timing)
    start(tm.FPS, seconds, offset)
    S = {n: (a, b) for n, a, b in tm.SHOTS}

    # ============================================================ vật liệu
    ground_m = material("M_Ground", (0.42, 0.41, 0.39), 0.9)
    slab_m = material("M_Slab", (0.6, 0.59, 0.57), 0.8)
    junk_m = material("M_Junk", (0.5, 0.49, 0.48), 0.6)
    junk_d = material("M_JunkDark", (0.33, 0.32, 0.31), 0.6)
    junk_l = material("M_JunkLight", (0.66, 0.65, 0.63), 0.5)
    box_m = material("M_Box", (0.42, 0.43, 0.44), 0.5)
    trim_m = material("M_BoxTrim", (0.62, 0.61, 0.58), 0.4)         # góc bọc, khoá, quai: sáng hơn thân hộp cho đọc ra hình
    inside_m = material("M_BoxInside", (0.1, 0.1, 0.1), 0.8)
    pack_m = material("M_Pack", (0.3, 0.29, 0.28), 0.7)
    strap_m = material("M_Strap", (0.1, 0.1, 0.1), 0.6)
    island_m = material("M_Island", (0.45, 0.46, 0.44), 0.9)
    rock_m = material("M_IslandRock", (0.55, 0.53, 0.5), 0.9)
    hub_m = material("M_Hub", (0.85, 0.85, 0.84), 0.5)
    sea_m = material("M_CloudSea", (0.86, 0.88, 0.9), 0.9, emit=((0.9, 0.92, 0.95), 0.4))
    sun_m = material("M_SunDisc", (1.0, 0.95, 0.8), 0.5, emit=((1.0, 0.93, 0.75), 3.0))
    teal = ((0.15, 1.0, 0.85), 3.0)
    flash_m = material("M_TealFlash", (0.2, 1.0, 0.85), 0.3, emit=teal)
    dim_m = material("M_TealDim", (0.02, 0.1, 0.09), 0.8, emit=((0.1, 0.8, 0.7), 0.25))

    # ============================================================ nền, biển mây, mặt trời
    add_obj("Ground", box_bm((16.0, 14.0, 1.0), (0.0, 1.0, -0.5)), ground_m, "SET")              # X -8…8, Y -6…8
    add_obj("CloudSea", box_bm((500.0, 190.0, 0.1), (0.0, 103.0, SEA_Z)), sea_m, "SET")          # Y 8…198, trong clip_end 200
    bm = None
    for cx, cy, sx, sz in ((-14, 30, 9, 1.4), (-3, 40, 10, 1.6), (9, 34, 8, 1.3), (22, 45, 12, 1.8), (-26, 52, 12, 1.8),
                           (-20, 75, 16, 2.2), (-40, 90, 20, 3.0), (40, 85, 22, 3.0)):
        bm = sphere_bm(1.0, (cx, cy, SEA_Z), (sx, sx * 0.5, sz), bm=bm, segs=16)               # gợn mây trên biển mây
    add_obj("CloudSea_Puffs", bm, sea_m, "SET")
    add_obj("SunDisc", sphere_bm(6.0, (-42.0, 160.0, 7.0), (1.0, 0.2, 1.0), segs=24), sun_m, "SET")   # mặt trời sát chân trời, bên trái
    bm = None
    for cx, cy, sx, sz in ((-4.0, 6.5, 1.4, 0.6), (-2.7, 7.0, 0.9, 0.45), (3.6, 6.5, 1.2, 0.5), (5.0, 7.2, 1.5, 0.6)):
        bm = sphere_bm(1.0, (cx, cy, 0.0), (sx, 0.6, sz), bm=bm, segs=12)                     # đống phế liệu xa, thấp, hai bên
    add_obj("FarJunk", bm, junk_d, "SET")
    bm = None
    for k, (cx, cy, w) in enumerate(((-1.05, -0.75, 0.42), (-0.5, -1.0, 0.38), (0.05, -0.8, 0.44), (0.6, -1.05, 0.4),
                                     (1.1, -0.7, 0.42), (-0.25, -1.35, 0.36), (0.35, -1.5, 0.4), (-1.3, -0.25, 0.3),
                                     (1.35, -0.3, 0.3), (-0.75, -1.7, 0.4), (0.9, -1.6, 0.38))):
        bm = box_bm((w, 0.28, 0.03), (cx, cy, 0.015), bm=bm)                                   # phiến đá lát trước hộp
    add_obj("Slabs", bm, slab_m, "SET")

    # ============================================================ đống phế liệu bên trái
    wheel = add_obj("JunkL_Wheel", spokes_bm(0.4, 0.05, 0.05, (0, 0, 0), bm=ring_bm(0.4, 0.07, 0.07, (0, 0, 0))), junk_m, "SET",
                    loc=(-1.4, 0.45, 0.45))                                                    # bánh xe lớn dựng nghiêng
    wheel.rotation_euler = (0, math.radians(8), math.radians(-25))
    add_obj("JunkL_WheelHub", cyl_bm(0.08, 0.12, axis="Y"), junk_d, "SET", parent=wheel)
    add_obj("JunkL_Stone", box_bm((0.6, 0.5, 0.4), (-1.9, 0.9, 0.2)), slab_m, "SET")           # khối đá rêu
    add_obj("JunkL_Boiler", cyl_bm(0.26, 0.45, (-1.9, 0.9, 0.62), bm=sphere_bm(0.26, (-1.9, 0.9, 0.85), (1, 1, 0.5))),
            junk_d, "SET")                                                                     # nồi hơi cũ trên khối đá
    bm = None
    for k in range(7):
        bm = ring_bm(0.12, 0.03, 0.03, (0, 0.07 * k + 0.02, 0), n=12, bm=bm)
    for v in bm.verts:                                                                         # vành nằm ngang, chồng lên nhau theo Z
        v.co = Vector((v.co.x, v.co.z, v.co.y))
    add_obj("JunkL_Spring", bm, junk_l, "SET", loc=(-2.05, 0.15, 0.0))                          # lò xo đứng
    add_obj("JunkL_Gear", gear_bm(0.24, 0.07, (0, 0, 0)), junk_l, "SET", loc=(-0.85, 0.15, 0.27)).rotation_euler = (0, 0.2, -0.35)
    add_obj("JunkL_Bucket", cyl_bm(0.17, 0.24, (-1.0, -0.35, 0.12)), slab_m, "SET")            # xô đá rêu
    add_obj("JunkL_Pipe", cyl_bm(0.07, 0.4, (-0.62, 0.35, 0.2)), junk_m, "SET")
    add_obj("JunkL_PipeTop", cyl_bm(0.07, 0.25, (-0.7, 0.35, 0.4), axis="X"), junk_m, "SET")

    # ============================================================ đống phế liệu bên phải (thấp dưới hòn đảo để không che đảo)
    wheel_r = add_obj("JunkR_Wheel", spokes_bm(0.3, 0.04, 0.05, (0, 0, 0), bm=ring_bm(0.3, 0.06, 0.06, (0, 0, 0))), junk_m, "SET",
                      loc=(1.45, 0.55, 0.34))
    wheel_r.rotation_euler = (0, math.radians(-6), math.radians(20))
    add_obj("JunkR_WheelHub", cyl_bm(0.06, 0.1, axis="Y"), junk_d, "SET", parent=wheel_r)
    add_obj("JunkR_Gear", gear_bm(0.25, 0.07, (0, 0, 0), teeth=9), junk_l, "SET", loc=(1.62, -0.15, 0.27)).rotation_euler = (0, 0.3, 0.3)
    add_obj("JunkR_Pipe", cyl_bm(0.16, 0.32, (1.0, 0.15, 0.16)), junk_d, "SET")                # khúc ống đứng
    add_obj("JunkR_Elbow", cyl_bm(0.07, 0.35, (0.72, 0.3, 0.42), axis="X",
                                  bm=cyl_bm(0.07, 0.4, (0.56, 0.3, 0.2))), junk_m, "SET")      # ống cong
    crate = add_obj("JunkR_Crate", box_bm((0.46, 0.4, 0.4), (0, 0, 0.2)), junk_m, "SET", loc=(1.95, 0.25, 0.0))
    add_obj("JunkR_CrateSlats", box_bm((0.48, 0.42, 0.03), (0, 0, 0.12), bm=box_bm((0.48, 0.42, 0.03), (0, 0, 0.3))), junk_d, "SET",
            parent=crate)
    add_obj("FG_Gear", gear_bm(0.4, 0.09, (0, 0, 0), teeth=12), junk_l, "SET", loc=(-1.5, -1.4, 0.22)).rotation_euler = (0.25, 0, 0.4)

    # ============================================================ hộp kim loại: thân rỗng, nắp hé quanh bản lề sau
    bm = box_bm((0.9, 0.56, 0.04), (0, 0, 0.02))                                               # đáy
    bm = box_bm((0.9, 0.04, 0.46), (0, -0.26, 0.23), bm=bm)                                    # vách trước
    bm = box_bm((0.9, 0.04, 0.46), (0, 0.26, 0.23), bm=bm)                                     # vách sau
    for s in (-1, 1):
        bm = box_bm((0.04, 0.56, 0.46), (s * 0.43, 0, 0.23), bm=bm)                            # hai vách bên
    add_obj("Box_Body", bm, box_m, "PROPS")
    add_obj("Box_Inside", box_bm((0.8, 0.46, 0.02), (0, 0, 0.05)), inside_m, "PROPS")         # lòng hộp tối
    bm = None
    for x in (-0.43, 0.43):
        for y in (-0.26, 0.26):
            for z in (0.05, 0.41):
                bm = box_bm((0.1, 0.1, 0.1), (x, y, z), bm=bm)                                 # góc bọc đồng
    bm = box_bm((0.16, 0.03, 0.13), (0, -0.285, 0.33), bm=bm)                                  # ổ khoá
    add_obj("Box_Trim", bm, trim_m, "PROPS")
    lid = empty("Box_Lid", "PROPS", loc=HINGE)
    bm = box_bm((0.94, 0.6, 0.05), (0, -0.29, 0.025))                                          # nắp phẳng
    vault = cyl_bm(0.3, 0.94, (0, -0.29, 0.04), axis="X", segs=24)                              # mái nắp cong (cong trước – sau)
    for v in vault.verts:
        v.co.z = max(0.04 + (v.co.z - 0.04) * 0.4, 0.0)
    add_obj("Box_LidShape", vault, box_m, "PROPS", parent=lid)
    add_obj("Box_LidSlab", bm, box_m, "PROPS", parent=lid)
    bm = None
    for x in (-0.44, 0.44):
        bm = box_bm((0.1, 0.62, 0.08), (x, -0.29, 0.06), bm=bm)                                 # đai đồng hai đầu nắp
    for x in (-0.14, 0.14):
        bm = box_bm((0.04, 0.04, 0.12), (x, -0.29, 0.2), bm=bm)                                 # quai xách: hai chân…
    bm = box_bm((0.32, 0.05, 0.05), (0, -0.29, 0.27), bm=bm)                                   # …và tay cầm
    bm = box_bm((0.08, 0.03, 0.07), (0, -0.59, 0.0), bm=bm)                                    # khoá nắp
    add_obj("Box_LidTrim", bm, trim_m, "PROPS", parent=lid)
    lid.rotation_euler = (math.radians(LID_OPEN), 0, 0)

    # Inventor Pack trong hộp: qua khe nắp thấy mặt trên ba lô, quai da có khoá, cuộn bản vẽ
    add_obj("Pack_Body", box_bm((0.58, 0.34, 0.32), (0, 0.03, 0.2)), pack_m, "PROPS")
    add_obj("Pack_Roll", cyl_bm(0.06, 0.5, (0, 0.1, 0.42), axis="X"), pack_m, "PROPS")
    strap = add_obj("Pack_Strap", box_bm((0.56, 0.05, 0.03)), strap_m, "PROPS", loc=(0, -0.13, 0.385))
    strap.rotation_euler = (0, math.radians(-4), math.radians(6))
    add_obj("Pack_Buckle", box_bm((0.08, 0.03, 0.06)), trim_m, "PROPS", loc=(0.05, -0.155, 0.39))

    # ánh lóe ở hộp: lòng hộp sáng bừng (lit), quầng và tia lọt ra khe nắp (halo), khe le lói sau lóe (dim)
    lit = add_obj("Pack_Lit", prism_x([(-0.235, 0.36), (0.235, 0.36), (0.235, 0.47), (-0.235, 0.59)], -0.41, 0.41),
                  flash_m, "PROPS")
    dim = add_obj("Pack_Dim", prism_x([(-0.235, 0.37), (0.235, 0.37), (0.235, 0.465), (-0.235, 0.58)], -0.41, 0.41),
                  dim_m, "PROPS")
    bm = sphere_bm(1.0, (0, 0, 0), (0.42, 0.03, 0.06), segs=24)                                # dải sáng ngay khe nắp
    for s in (-1, 1):
        for dz, ang in ((-0.07, -12), (0.0, 0), (0.08, 14)):                                   # tia hẹp lọt ra hai đầu khe
            a = math.radians(ang) * s
            m = Matrix.Translation((s * 0.6, 0.0, dz)) @ Matrix.Rotation(-a, 4, "Y")
            bm = cube(bm, (0.32, 0.02, 0.03), m)
    halo = add_obj("Pack_Halo", bm, flash_m, "PROPS", loc=GAP)
    pack_light = bpy.data.objects.new("Pack_Light", bpy.data.lights.new("Pack_Light", "POINT"))
    COLS["PROPS"].objects.link(pack_light)
    pack_light.location = GAP + Vector((0, -0.12, -0.02))
    pack_light.data.color, pack_light.data.shadow_soft_size = (0.2, 1.0, 0.85), 0.1

    # ============================================================ hòn đảo có đài thiên văn ở chân trời
    # đồi cỏ dáng nón tròn đỉnh, mái vòm lớn ở sườn trước, dãy nhà bên phải (như wonder_hub_island_hero.png)
    bm = sphere_bm(1.0, (DOME.x + 0.8, DOME.y + 3.0, SEA_Z + 0.5), (6.5, 4.5, 7.5), segs=20)
    for v in bm.verts:                                                                         # vuốt nhọn dần lên đỉnh
        h = (v.co.z - SEA_Z) / 8.0
        if h > 0:
            v.co.x = DOME.x + 0.8 + (v.co.x - DOME.x - 0.8) * max(1.0 - 0.75 * h, 0.15)
            v.co.y = DOME.y + 3.0 + (v.co.y - DOME.y - 3.0) * max(1.0 - 0.75 * h, 0.15)
    add_obj("Island_Hill", bm, island_m, "SET")
    add_obj("Island_Rock", cyl_bm(7.0, 1.6, (DOME.x + 0.8, DOME.y + 3.0, SEA_Z + 0.4), cone_top=6.6, segs=20), rock_m, "SET")
    bm = cyl_bm(2.3, 1.4, (DOME.x, DOME.y, DOME.z - 0.7), segs=24)                              # tầng có vòm cửa dưới mái vòm
    bm = sphere_bm(2.1, (DOME.x, DOME.y, DOME.z), (1, 1, 0.95), bm=bm, segs=24)                # mái vòm
    bm = box_bm((3.0, 1.8, 1.1), (DOME.x + 3.4, DOME.y + 0.6, DOME.z - 0.85), bm=bm)           # dãy nhà bên phải
    add_obj("Hub", bm, hub_m, "SET")
    bm = None
    for cx, cz, sx in ((-5.5, 0.0, 4.5), (5.0, 0.2, 5.0)):
        bm = sphere_bm(1.0, (DOME.x + cx, DOME.y - 4.0, SEA_Z + cz), (sx, 1.5, 0.8), bm=bm, segs=12)
    add_obj("Island_Mist", bm, sea_m, "SET")                                                   # sương chân đảo
    tint = add_obj("Hub_Tint", sphere_bm(2.2, (0, 0, 0), (1, 1, 0.95), segs=24), flash_m, "PROPS", loc=DOME)   # mái vòm sáng bừng
    bm = sphere_bm(1.0, (0, 0, 0), (2.8, 0.3, 2.6), segs=24)                                    # quầng sau mái vòm…
    for k in range(12):                                                                        # …nhô ra thành 12 tia
        a = math.radians(k * 30 + 15)
        m = Matrix.Translation((3.6 * math.cos(a), 0.0, 3.4 * math.sin(a))) @ Matrix.Rotation(-a, 4, "Y")
        bm = cube(bm, (2.0, 0.2, 0.4), m)
    hub_flash = add_obj("Hub_Flash", bm, flash_m, "PROPS", loc=DOME + Vector((0, 1.0, 0.3)))

    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    COLS["SET"].objects.link(sun)
    sun.data.energy, sun.data.angle = 2.2, math.radians(4)
    sun.rotation_euler = (math.radians(55), 0, math.radians(-30))
    world = bpy.data.worlds.new("Sky")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.62, 0.6, 0.75, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.7

    # ============================================================ diễn: hai cú lóe cùng nhịp
    def scale(ob, t, s):
        key(ob, "scale", t, Vector((s, s, s)))

    def show(ob, t, on):
        scale(ob, t - HOLD, 0 if on else 1)
        scale(ob, t, 1 if on else 0)

    def pulse(ob, t):
        """Một nhịp lóe: hiện từ t, co giãn theo PULSE rồi tắt."""
        scale(ob, t - HOLD, 0)
        for dt, s in PULSE:
            scale(ob, t + dt, s)

    for ob in (lit, dim, halo, tint, hub_flash):
        scale(ob, -1.0, 0)                                          # ẩn bằng scale 0 ngoài lúc lóe
    pulse(hub_flash, tm.HUB_FLASH)                                  # hòn đảo lóe xanh ngọc
    show(tint, tm.HUB_FLASH, True)
    show(tint, tm.HUB_FLASH + LIT, False)
    pulse(halo, tm.PACK_FLASH)                                      # cùng nhịp đó, Inventor Pack lóe qua khe nắp
    show(lit, tm.PACK_FLASH, True)
    show(lit, tm.PACK_FLASH + LIT, False)
    show(dim, tm.PACK_FLASH + LIT, True)                            # le lói tới hết cảnh
    key(pack_light.data, "energy", -1.0, 0.0)
    key(pack_light.data, "energy", tm.PACK_FLASH - HOLD, 0.0)
    for dt, s in PULSE:
        key(pack_light.data, "energy", tm.PACK_FLASH + dt, 8.0 * s)   # hắt xanh lên nắp, phiến đá trước hộp

    # ============================================================ máy quay: đẩy chậm, đều vào chiếc hộp
    p0, p1 = tm.PUSH
    A = ((0.08, -3.6, 0.92), (0.08, 0.0, 0.6))                      # toàn bãi phế liệu: hộp giữa khung, đảo trên phải quai hộp
    B = ((0.08, -2.75, 0.8), (0.08, 0.0, 0.5))                      # hộp to hơn, đảo vẫn trong khung
    end_t = offset + seconds

    def lerp(u):
        return tuple(tuple(a + (b - a) * u for a, b in zip(pa, pb)) for pa, pb in zip(A, B))

    u_end = (end_t - p0) / (p1 - p0)                                # đuôi: đẩy tiếp cùng tốc độ tới hết video
    CAMS = {"S1": [(p0, *lerp(0.0), 35), (end_t, *lerp(u_end), 35)]}
    shots = [(n, a, b) for n, a, b in tm.SHOTS if a < offset + segment - 1e-6 and b > offset + 1e-6]
    cams = cameras(shots, {n: CAMS[n] for n, _, _ in shots})
    for n, _, _ in shots:
        linear(cams[n])
        linear(bpy.data.objects[f"Aim_{n}"])
    must = {"S1": [(halo, Vector()), (lid, Vector((0, -0.29, 0.27))), (tint, Vector()),
                   (hub_flash, Vector((0, 0, 4.5))), (hub_flash, Vector((4.5, 0, 0)))]}
    check_in_frame(shots, cams, must)
    finish(out_blend, [t for t in (0.5, 2.0, tm.HUB_FLASH + 0.1, tm.HUB_FLASH + 0.3, tm.HUB_FLASH + 0.6, 4.5)
                       if offset <= t < offset + segment])
