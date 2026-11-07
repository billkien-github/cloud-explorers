"""
Previz khối Cảnh 2 tập 000A (Ánh sáng lạ) dẫn Seedance (04_PRODUCTION/SEEDANCE.md): bối cảnh phế tích, Lumo, Wonder
Compass, con bướm, ánh vàng dạng khối (pipeline/blocks.py), máy quay từng cú. Mọi mốc lấy từ timing.py của previz 2D
(TIMING trong build_shot.py của đoạn), không gõ lại số. Diễn theo previz 2D đã chốt:
03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene02/.
Hai đoạn (Seedance 2.5, tối đa 30 giây) gọi build() với giây bắt đầu và độ dài của đoạn:
    sh030: 0–23.0 s của cảnh (S1–S5: chui khỏi đống lá, nhấc phiến đá, la bàn trong hốc, "Ồ! Kho báu!", thổi bụi, hắt
           xì, lau kính, mũi sao rung rồi xoay phắt, TÍT… TÍT…, suýt đánh rơi; cận la bàn, bức tường ở hậu cảnh)
    sh040: 23.0–44.8 s (S6–S10: đi vòng qua phiến đá tới đầu tường, quay lại, mũi sao xoay theo, "Hừm…", áp tai, gõ ba
           lần, hòn sỏi rơi trúng đầu, "Mình nghĩ bức tường không thích bị làm phiền.", liếc la bàn)
Diễn dựng cho cả cảnh để các đoạn nối liền; khung 1 của đoạn = giây bắt đầu (blocks.T0), chỉ dựng máy quay của các cú
trong đoạn.
Nối ngay cuối Cảnh 1 (scene01_blocks.py): Lumo nhổm tới ngực trong đống lá PILE_AT, quay mặt sang trái; con bướm đậu trên
phiến đá rêu (STONE_TOP); ánh vàng le lói dưới phiến đá trên bậc đá chân tường (GLOW_AT). Bối cảnh chung: ruins_blocks.py.
Bố trí 3D (máy phía -Y nhìn về +Y): Lumo bước lên đầu phải bậc đá (SQ, quay mặt sang trái, nghiêng về máy), ngồi xổm,
nhấc phiến đá bằng mép phải (bản lề ở mép trái, phía thân tường), la bàn nằm trong hốc dưới phiến đá; đứng trên bậc đá,
xoay ba phần tư về máy. Đi vòng qua đầu phải bậc đá ra sau, tới sát đầu tường (mặt đứng ở X -9, quay về +X), đứng nghiêng
mặt vào đầu tường rồi quay lại (qua mặt trước) nhìn về phía vừa đi. Áp tai: người quay vào đầu tường, đầu ngoảnh ra máy,
nghiêng cho một bên tai ép vào mặt đầu tường. Gõ bằng tay phía máy, la bàn chuyền sang tay xa để bên hông. Hòn sỏi nằm
sẵn trên đá đỉnh tường từ đầu cảnh, nảy theo mỗi tiếng gõ, lăn khỏi đá đỉnh tường, rơi trúng đầu, nảy ra, nằm lại trên nền.
Ngồi xổm (crouch): thân ngả, khối chân chĩa ra trước và dạng sang hai bên phiến đá, hông hạ cho bàn chân chạm bậc đá; độ
ngả chọn cho bàn tay bám mép phiến đá, rút la bàn trong hốc cách vai đúng ARM.
S5 là cú nhìn dựng riêng (InsertCompass, hai khối tay ngắn hơn ARM trước máy, máy lùi ra khỏi mặt tường). S7: máy thấp phía
trước (-Y) nhìn chéo về đầu tường; la bàn cầm ở phía máy của thân, gần như đứng yên (P7), Lumo xoay quanh nó và chuyền tay
(trái → hai tay → phải); mặt la bàn quay về máy, quai theo hướng mặt Lumo nên vỏ xoay, mũi sao đứng chỉ về tường.
La bàn: vỏ tròn vàng to hơn cỡ thật (bán kính CR), mặt kính xanh, bụi phủ tới lúc lau; mũi sao tám cánh: bảy cánh ngắn
trắng, đầu chỉ là một khối dài vàng sáng có viên đá xanh ở mút, quay trong mặt la bàn. Sau cú xoay phắt, mũi sao chỉ tâm
phù điêu sau mảng dây leo (RELIEF) ở mọi khung: góc tính từ ma trận thế giới của la bàn từng khung. Kính sáng, nhấp
nháy lúc kêu bằng key cường độ phát sáng.
Màu: Lumo cam (ô trắng = hướng mặt); bối cảnh xám; la bàn vàng, kính xanh; vạt áo choàng đỏ; bướm, ánh vàng phát sáng.
"""
import math
import pathlib
import sys
from types import SimpleNamespace

import bpy
from mathutils import Euler, Matrix, Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.path[:0] = [str(ROOT / "pipeline"), str(HERE)]
from blocks import *  # noqa: E402,F403  khối, vật liệu, nhân vật dạng khối, keyframe theo giây, máy quay
from ruins_blocks import (GLOW_AT, LOW_Z, PILE_AT, RELIEF, SLAB_SIZE, STEP_TOP, STONE_TOP, WALL_END,  # noqa: E402
                          bfly, build_far_wall, build_ruins, flap, ground_z)

LEFT = -62
HOLD = 1 / 24                                                    # một khung: key ẩn và key hiện cách nhau ít hơn thì rơi vào cùng khung
CR = 0.08                                                        # bán kính vỏ la bàn (to hơn cỡ thật cho đọc được)
ARM = 0.29                                                       # khối tay Lumo, vai tới đầu bàn tay
SHOULDER = {"l": Vector((0.20, 0, 0.55)), "r": Vector((-0.20, 0, 0.55))}
HINGE = Vector((GLOW_AT.x - SLAB_SIZE[0] / 2, GLOW_AT.y, LOW_Z + 0.18))   # bản lề phiến đá: mép trái, mặt dưới
LIFT_DEG = 35                                                    # mép phải nhấc lên 35°
SPOT = Vector((-9.25, 0.5, STEP_TOP - 0.004))                    # la bàn trong hốc, nửa chìm trong bậc đá
SQ = Vector((-8.75, 0.55, STEP_TOP))                             # chỗ Lumo đứng, ngồi xổm trên đầu phải bậc đá
SIDE = Vector((-8.68, 1.13, LOW_Z))                              # sát đầu tường, sau bậc đá
KNOCK = Vector((WALL_END + ARM - 0.005, 1.2, LOW_Z))             # tay phía máy chạm mặt đầu tường


def build(timing, offset, seconds, out_blend, segment=None):
    """seconds: độ dài video render (số nguyên giây Seedance nhận); segment: độ dài đoạn trong cảnh. Từ segment tới
    seconds chỉ giữ cú máy cuối (diễn vẫn chạy tiếp), lúc dựng cắt bỏ."""
    segment = seconds if segment is None else segment
    tm = load_timing(ROOT / timing)
    start(tm.FPS, seconds, offset)
    T_END = tm.SECONDS
    S = {n: (a, b) for n, a, b in tm.SHOTS}

    # ============================================================ bối cảnh
    W = build_ruins()
    build_far_wall()
    slab, glow, pile = W.slab, W.glow, W.pile
    hinge = empty("SlabHinge", "SET", loc=HINGE)                   # phiến đá xoay quanh mép trái
    slab.parent = hinge
    slab.matrix_parent_inverse = Matrix.Translation(-HINGE)
    hollow_m = material("M_Hollow", (0.06, 0.055, 0.05), 0.9)
    add_obj("Hollow", cyl_bm(0.105, 0.004, (SPOT.x, SPOT.y, STEP_TOP + 0.001), segs=32), hollow_m, "SET")   # hốc nông dưới phiến đá
    prop_dark = material("M_PropDark", (0.12, 0.12, 0.13), 0.6)
    dust_m = material("M_Dust", (0.62, 0.58, 0.5), 0.95)
    cape_m = material("M_Cape_Red", (0.85, 0.12, 0.08), 0.7)
    pebble_m = material("M_Pebble", (0.22, 0.21, 0.2), 0.8)
    gold_m = material("M_Compass_Gold", (1.0, 0.68, 0.12), 0.35, emit=((1.0, 0.65, 0.1), 0.3))
    glass_m = material("M_Compass_Glass", (0.06, 0.22, 0.75), 0.15, emit=((0.25, 0.55, 1.0), 0.0))
    point_m = material("M_Compass_Pointer", (1.0, 0.85, 0.15), 0.3, emit=((1.0, 0.78, 0.1), 2.5))
    star_m = material("M_Compass_Star", (0.85, 0.93, 1.0), 0.4, emit=((0.85, 0.93, 1.0), 0.4))
    gem_m = material("M_Compass_Gem", (0.1, 0.8, 1.0), 0.2, emit=((0.1, 0.8, 1.0), 1.5))

    lit_gold_m = material("M_Compass_GoldLit", (1.0, 0.68, 0.12), 0.35, emit=((1.0, 0.65, 0.1), 2.5))   # la bàn trong hốc: nguồn ánh vàng

    def build_compass(name, parent=None, loc=(0, 0, 0), case_m=None):
        """Mặt la bàn = mặt XY cục bộ, pháp tuyến +Z; quai ở +Y. Mũi sao quay quanh Z, đầu chỉ dọc +Y của mũi sao."""
        case_m = case_m or gold_m
        root = empty(name, "PROPS", parent=parent, loc=loc)
        add_obj(name + "_Case", cyl_bm(CR, 0.032, segs=32), case_m, "PROPS", parent=root)
        add_obj(name + "_Bail", box_bm((0.034, 0.03, 0.02), (0, CR + 0.01, 0)), case_m, "PROPS", parent=root)
        add_obj(name + "_Glass", cyl_bm(CR * 0.82, 0.004, (0, 0, 0.016), segs=32), glass_m, "PROPS", parent=root)
        needle = empty(name + "_Needle", "PROPS", parent=root, loc=(0, 0, 0.02))
        bm = box_bm((0.016, 0.046, 0.006), (0, 0.023, 0))           # đầu chỉ: thân dài…
        n = len(bm.verts)
        bm = box_bm((0.017, 0.017, 0.006), (0, 0, 0), bm=bm)        # …mũi hình thoi
        bm.verts.ensure_lookup_table()
        for v in bm.verts[n:]:
            v.co = Matrix.Rotation(math.radians(45), 3, "Z") @ v.co + Vector((0, 0.05, 0))
        add_obj(name + "_Pointer", bm, point_m, "PROPS", parent=needle)
        add_obj(name + "_Gem", sphere_bm(0.008, (0, 0.058, 0.0), (1, 1, 0.45), segs=8), gem_m, "PROPS", parent=needle)
        bm = cyl_bm(0.011, 0.007, segs=12)                          # tâm sao
        for k in range(1, 8):                                       # bảy cánh ngắn
            n = len(bm.verts)
            bm = box_bm((0.009, 0.026, 0.004), (0, 0.016, 0), bm=bm)
            bm.verts.ensure_lookup_table()
            for v in bm.verts[n:]:
                v.co = Matrix.Rotation(math.radians(45 * k), 3, "Z") @ v.co
        add_obj(name + "_Star", bm, star_m, "PROPS", parent=needle)
        dust = add_obj(name + "_Dust", cyl_bm(CR * 0.82, 0.009, (0, 0, 0.0235), segs=32), dust_m, "PROPS", parent=root)   # phủ kín mũi sao
        return SimpleNamespace(root=root, needle=needle, dust=dust)

    # ============================================================ Lumo, la bàn, đồ vật nhỏ, bướm
    L = build_lumo((PILE_AT.x, 0.0, LOW_Z + 0.06))
    lumo = Act(L, PILE_AT.x, 0.0, LEFT)
    add_obj("Lumo_Bag", box_bm((0.1, 0.06, 0.09)), prop_dark, "CAST", parent=L.root, loc=(-0.2, -0.1, 0.3))
    hold = empty("Lumo_CompassHold", "PROPS", parent=L.root)        # la bàn cầm tay: vị trí, góc trong khung gốc của Lumo
    comp = build_compass("Compass", hold)
    gcomp = build_compass("GroundCompass", loc=SPOT, case_m=lit_gold_m)   # la bàn nằm ngửa trong hốc, vỏ sáng: ánh vàng ở S1 là từ nó
    icomp = build_compass("InsertCompass")                          # cú nhìn S5: la bàn dựng riêng trước máy (dưới)
    cape = add_obj("Lumo_CapeCorner", box_bm((0.11, 0.012, 0.1), (0, 0, -0.05)), cape_m, "CAST", parent=L.arm_r,
                   loc=(0, -0.02, -ARM))                            # vạt áo choàng kéo ra lau kính
    face_dust = add_obj("Lumo_FaceDust", sphere_bm(0.075, scale=(1.3, 0.3, 0.7), segs=12), dust_m, "CAST", parent=L.head,
                        loc=(0, -0.25, 0.1))                        # bụi bám trên mõm
    puffs = [add_obj(f"DustPuff{i}", sphere_bm(0.035 + 0.008 * (i % 3), segs=10), dust_m, "PROPS") for i in range(7)]
    slab_dust = [add_obj(f"SlabDust{i}", sphere_bm(0.025, segs=8), dust_m, "PROPS") for i in range(4)]
    leaf_bits = [add_obj(f"Leaf{i}", box_bm((0.07, 0.04, 0.01)), W.mats.litter, "PROPS") for i in range(6)]
    pebble = add_obj("Pebble", sphere_bm(0.07, scale=(1.0, 0.9, 0.8), segs=12), pebble_m, "PROPS")   # to hơn cỡ thật cho đọc được
    hero, hero_w = bfly("Butterfly")
    hero.scale = (1.6, 1.6, 1.6)                                    # như con bướm dẫn mắt cuối Cảnh 1

    for ob in (cape, face_dust, pebble, *puffs, *slab_dust, *leaf_bits, comp.root, gcomp.root, icomp.root, icomp.dust):
        key(ob, "scale", -1.0, Vector((0, 0, 0)))                   # ẩn bằng scale 0 tới lúc xuất hiện

    def show(ob, t, on, s=1.0):
        key(ob, "scale", t - HOLD, Vector((s, s, s)) if not on else Vector((0, 0, 0)))
        key(ob, "scale", t, Vector((s, s, s)) if on else Vector((0, 0, 0)))

    def head(t, pitch=0.0, yaw=0.0, roll=0.0):
        rot(L.head, [(t, (pitch, roll, yaw))])

    def ears(t, a):
        for ear, side in L.ears:
            rot(ear, [(t, (a, 0, 0))])

    def tail(t, up, side=0.0):
        rot(L.tail, [(t, (up, 0, side))])

    def squash(t, sx, sz):
        key(L.root, "scale", t, Vector((sx, sx, sz)))

    def pose(t, lean=None, yaw=None, roll=None):
        """lumo.pose, hướng chọn vòng gần nhất với hướng trước đó (không xoay vòng dài)."""
        if yaw is not None:
            yaw += 360 * round((lumo.yaw - yaw) / 360)
        lumo.pose(t, lean, yaw, roll)

    def rootm():
        """Ma trận gốc Lumo theo trạng thái vừa key (gọi ngay sau lumo.go/pose ở cùng giây)."""
        e = Euler([math.radians(a) for a in (lumo.lean, lumo.roll, lumo.yaw)], "XYZ")
        return Matrix.Translation((lumo.x, lumo.y, lumo.z)) @ e.to_matrix().to_4x4()

    prev = {}

    def arm_to(side, t, p):
        """Chĩa tay (l: tay trái, phía +X cục bộ; r: tay phải) về điểm p trong khung gốc của Lumo."""
        arm = L.arm_l if side == "l" else L.arm_r
        d = (Vector(p) - SHOULDER[side]).normalized()
        e = Vector((0, 0, -1)).rotation_difference(d).to_euler("XYZ", prev.get(side, Euler()))
        prev[side] = e
        rot(arm, [(t, tuple(math.degrees(a) for a in e))])

    def arms_down(t, a=6, sides="lr"):
        for side in sides:
            e = Euler((math.radians(a), 0, 0))
            prev[side] = e
            rot(L.arm_l if side == "l" else L.arm_r, [(t, (a, 0, 0))])

    def grip(t, c, tilt=37, yaw=0.0, roll=0.0, hands="lr"):
        """La bàn ở c (khung gốc Lumo), mặt nghiêng tilt độ (0: ngửa, 90: dựng đứng quay ra trước); tay trong hands bám
        mép vỏ hai bên (tay đi theo la bàn)."""
        key(hold, "location", t, Vector(c))
        rot(hold, [(t, (tilt, roll, yaw))])
        m = Matrix.Translation(c) @ Euler([math.radians(a) for a in (tilt, roll, yaw)], "XYZ").to_matrix().to_4x4()
        for side in hands:
            arm_to(side, t, m @ Vector(((1 if side == "l" else -1) * (CR + 0.012), 0, 0)))

    def local(p):
        return rootm().inverted() @ Vector(p)

    CHEST = (0.0, -0.26, 0.45)                                      # la bàn ngang ngực, mặt ngửa chếch về trước
    RAISE = (0.0, -0.25, 0.6)                                       # giơ lên, dưới tầm tai
    LIFT = (0.0, -0.25, 0.5)                                        # đưa lên gần mặt nhìn (dưới mõm)
    ONE = (0.13, -0.25, 0.43)                                       # một tay phía máy cầm
    HIP_R = (-0.27, -0.06, 0.29)                                    # tay xa, để bên hông

    # ============================================================ ánh vàng, bướm: tiếp đúng cuối Cảnh 1
    l0, l1 = tm.SLAB_LIFT
    t, i = 0.0, 0
    while t < l0:                                                   # le lói qua khe phiến đá như cuối Cảnh 1
        key(glow, "scale", t, Vector((0.9, 0.9, 1.0)) if i % 2 == 0 else Vector((1.2, 1.2, 1.0)))
        t, i = t + 0.6, i + 1
    key(glow, "scale", l0 + 0.4, Vector((1.0, 1.0, 1.0)))
    key(glow, "scale", l1, Vector((1.3, 1.25, 1.0)))                # ánh vàng bung ra khi phiến đá nhấc lên
    SEE = S["S2"][0]                                                # sang cú cận hốc: tắt lớp sáng phẳng, lộ la bàn sáng
    key(glow, "scale", SEE - HOLD, Vector((1.3, 1.25, 1.0)))
    key(glow, "scale", SEE, Vector((0, 0, 0)))
    show(gcomp.root, SEE, True)

    bf0, bf1 = tm.BFLY_OFF
    key(hero, "location", 0.0, STONE_TOP)
    rot(hero, [(0.0, (0, 0, 60))])
    flap(hero_w, 0.0, bf0, 0.9, 20, 55)                             # đậu: cánh khép mở chậm như cuối Cảnh 1
    key(hero, "location", bf0, STONE_TOP)
    for t, p in ((bf0 + 0.3, (-8.2, 0.0, -0.9)), (bf0 + 0.7, (-8.6, 0.3, -0.62)), (bf0 + 1.1, (-9.1, 0.7, -0.3)),
                 (bf0 + 1.5, (-9.7, 1.0, 0.05)), (bf1, (-10.6, 1.4, 0.55))):
        key(hero, "location", t, Vector(p))                         # bay lên, qua phế tích, ra khỏi khung phía trên trái
    rot(hero, [(bf0, (0, 0, 60)), (bf0 + 0.3, (0, 0, 120))])
    flap(hero_w, bf0, bf1)
    show(hero, bf1 + 0.05, False, 1.6)

    # ============================================================ S1: chui ra khỏi đống lá, bước tới phiến đá, ngồi xổm
    POP = LOW_Z + 0.06
    lumo.go(0.0, PILE_AT.x, POP, 0.0)
    pose(0.0, lean=0, yaw=LEFT, roll=0)
    head(0.0, -6, -30)                                              # như khung cuối Cảnh 1: nhìn ánh vàng
    ears(0.0, 16)
    arms_down(0.0)
    tail(0.0, 30)
    c0, c1 = tm.CLIMB_OUT
    lumo.go(c0, PILE_AT.x, POP)
    squash(c0, 1, 1)
    lumo.go(c0 + 0.2, PILE_AT.x, POP - 0.1)                         # lấy đà
    squash(c0 + 0.2, 1.08, 0.9)
    pose(c0 + 0.2, lean=10)
    ears(c0 + 0.2, -15)
    lumo.go(c0 + 0.45, -7.45, LOW_Z + 0.45, 0.15)                   # bật khỏi đống lá
    squash(c0 + 0.45, 0.94, 1.08)
    pose(c0 + 0.45, lean=-8, yaw=-95)
    ears(c0 + 0.45, 18)
    head(c0 + 0.45, 6, 0)
    for side in "lr":
        rot(L.arm_l if side == "l" else L.arm_r, [(c0 + 0.45, (-60, 0, 0))])
    lumo.go(c0 + 0.75, -7.82, LOW_Z + 0.32, 0.34)                   # bước qua mép đống lá
    pose(c0 + 0.75, lean=8)
    lumo.go(c0 + 0.95, -8.0, LOW_Z, 0.42)                           # chạm đất
    squash(c0 + 0.95, 1.08, 0.9)
    lumo.go(c1, -8.0, LOW_Z, 0.42)
    squash(c1 - 0.2, 1, 1)
    pose(c1, lean=0)
    arms_down(c1 - 0.2)
    ears(c1, 8)
    tail(c1, 30)
    wag(L.tail, c1, tm.WALK_SLAB[1], 0.5, 18, base=(30, 0, 0))
    keys(pile, "scale", [(c0 + 0.3, Vector((1, 1, 1))), (c0 + 0.5, Vector((1.1, 1.1, 0.88))),
                         (c0 + 0.8, Vector((0.96, 0.96, 1.05))), (c1, Vector((1, 1, 1)))])
    for i, ob in enumerate(leaf_bits):                              # lá rơi khỏi người
        ts = c0 + 0.45 + 0.05 * i
        pa = Vector((-7.45 + 0.04 * i, 0.12 - 0.04 * i, LOW_Z + 0.75 - 0.05 * i))
        pb = Vector((-7.6 - 0.12 * i, -0.15 - 0.05 * (i % 3), LOW_Z + 0.01))
        show(ob, ts, True)
        for k in range(5):
            u = k / 4
            key(ob, "location", ts + 0.8 * u, pa.lerp(pb, u) + Vector((0.08 * math.sin(4 * u), 0, 0.12 * math.sin(math.pi * u))))
            rot(ob, [(ts + 0.8 * u, (0, 240 * u, 90 * u))])
        show(ob, ts + 1.4, False)
    # bước tới đầu phải bậc đá, bước lên
    w0, w1 = tm.WALK_SLAB
    for t, x, y, z in ((w0, -8.0, 0.42, LOW_Z), (w0 + 0.3, -8.18, 0.46, LOW_Z + 0.04), (w0 + 0.6, -8.36, 0.5, LOW_Z),
                       (w0 + 0.85, -8.55, 0.53, LOW_Z + 0.04), (w0 + 1.05, -8.7, 0.55, STEP_TOP + 0.05), (w1, SQ.x, SQ.y, SQ.z)):
        lumo.go(t, x, z, y)
    steps(L.legs, w0, w1, 6, 25)
    pose(w0, yaw=-95)
    pose(w1, yaw=-90)
    head(w0, 10, 0)
    head(w1, 16, 0)                                                 # mắt không rời ánh vàng
    q0, q1 = tm.SQUAT
    SQ_X = SQ.x
    KNEE, SPREAD = -65, 20                                          # khối chân chĩa ra trước 65° và dạng 20° (gối gập, hai chân hai bên phiến đá)

    def crouch(t, lean):
        """Ngồi xổm: thân ngả lean độ, khối chân giữ góc KNEE so với phương đứng, hông hạ cho bàn chân chạm mặt bậc đá."""
        z = STEP_TOP + 0.29 * (math.cos(math.radians(KNEE)) * math.cos(math.radians(SPREAD)) - math.cos(math.radians(lean)))
        lumo.go(t, SQ_X, z, SQ.y)
        pose(t, lean=lean)
        for leg, sd in zip(L.legs, (1, -1)):
            rot(leg, [(t, (KNEE - lean, 0, sd * SPREAD))])

    lumo.go(q0, SQ.x, SQ.z, SQ.y)
    pose(q0, lean=0)
    for leg in L.legs:
        rot(leg, [(q0, (0, 0, 0))])
    squash(q0, 1, 1)
    crouch(q1, 36)                                                  # ngồi xổm, chồm tới mép phiến đá
    squash(q1, 1.03, 0.95)
    head(q1, 14, 0)
    ears(q1, 4)

    # ============================================================ nhấc phiến đá: bản lề mép trái, mép phải lên 35°
    def slab_pt(a, u, dy):
        """Điểm ở mặt dưới phiến đá, cách bản lề u (m) dọc phiến đá, lệch dy theo Y, khi phiến đá nhấc a độ."""
        r = math.radians(a)
        return HINGE + Vector((u * math.cos(r), dy, u * math.sin(r)))

    def hold_slab(t, a, sides="lr"):
        """Bàn tay bám mặt dưới phiến đá ở chỗ tay với tới (vai cách ARM), gần mép phải nhất có thể."""
        m = rootm()
        for side in sides:
            sh = m @ SHOULDER[side]
            dy = -0.1 if side == "l" else 0.1
            best = min((abs((sh - slab_pt(a, u, dy)).length - ARM), -u) for u in [SLAB_SIZE[0] * k / 40 for k in range(41)])
            arm_to(side, t, local(slab_pt(a, -best[1], dy)))

    rot(hinge, [(0.0, (0, 0, 0)), (l0 + 0.1, (0, 0, 0))])
    hold_slab(l0 - 0.25, 0)                                         # bám mép phiến đá (thân đã ở tư thế q1)
    crouch(l0, 36)
    hold_slab(l0, 0)
    rot(hinge, [(l0 + 0.35, (0, -8, 0))])                           # nặng, nhích lên chút
    crouch(l0 + 0.35, 34)
    hold_slab(l0 + 0.35, 8)
    rot(hinge, [(l1, (0, -LIFT_DEG, 0))])
    crouch(l1, 30)                                                  # ngả người lên theo mép phiến đá
    hold_slab(l1, LIFT_DEG)
    squash(l0 + 0.35, 1.03, 0.95)
    squash(l1, 1.05, 0.92)
    squash(l1 + 0.3, 1, 1)
    ears(l0 + 0.2, -12)                                             # gắng sức
    head(l0 + 0.2, 10, 0)
    for i, ob in enumerate(slab_dust):                              # bụi bung ra quanh mép phiến đá
        pa = Vector((GLOW_AT.x + 0.2 - 0.05 * i, GLOW_AT.y - 0.15 + 0.1 * i, STEP_TOP + 0.03))
        pb = pa + Vector((0.15 - 0.1 * i, -0.15, 0.12))
        show(ob, l0 + 0.4, True)
        key(ob, "location", l0 + 0.4, pa)
        key(ob, "location", l0 + 1.0, pb)
        show(ob, l0 + 1.05, False)
    ears(tm.COMPASS_SEE - 0.05, -10)
    ears(tm.COMPASS_SEE + 0.12, 18)                                 # thấy la bàn: tai bật dựng
    ears(tm.COMPASS_SEE + 0.3, 8)
    head(tm.COMPASS_SEE, 24, 0)                                     # cúi nhìn vào hốc
    wag(L.tail, tm.COMPASS_SEE, tm.GRAB[0], 0.3, 25, base=(40, 0, 0))   # đuôi ngoe nguẩy

    # ============================================================ S2: thò tay rút la bàn ra, phiến đá rơi về chỗ
    g0, g1 = tm.GRAB
    crouch(g0, 30)
    hold_slab(g0, LIFT_DEG)
    crouch(g0 + 0.25, 54)                                           # chồm tới thò tay phía máy vào hốc
    hold_slab(g0 + 0.25, LIFT_DEG, "r")                             # tay xa vẫn đỡ phiến đá
    grab_p = local(SPOT + Vector((0, 0, 0.02)))
    arm_to("l", g0 + 0.25, grab_p)
    head(g0 + 0.25, 20, 0)
    GRAB_T = g0 + 0.3
    show(gcomp.root, GRAB_T, False)
    show(comp.root, GRAB_T, True)
    d = (grab_p - SHOULDER["l"]).normalized()
    key(hold, "location", GRAB_T - HOLD, SHOULDER["l"] + d * (ARM + 0.04))
    key(hold, "location", GRAB_T, SHOULDER["l"] + d * (ARM + 0.04))   # la bàn nằm ngay dưới bàn tay
    rot(hold, [(GRAB_T - HOLD, (0, 0, 0)), (GRAB_T, (0, 0, 0))])
    arm_to("l", GRAB_T, grab_p)
    crouch(GRAB_T, 54)
    hold_slab(GRAB_T, LIFT_DEG, "r")
    crouch(g1, 30)
    hold_slab(g1, LIFT_DEG, "r")
    grip(g1, ONE, tilt=50, hands="l")                               # rút ra, giơ lên trước ngực
    head(g1, 12, 0)
    sd = tm.SLAB_DROP
    rot(hinge, [(sd - 0.12, (0, -LIFT_DEG, 0)), (sd, (0, 0, 0)), (sd + 0.06, (0, -3, 0)), (sd + 0.12, (0, 0, 0))])   # CỘP
    crouch(sd - 0.14, 30)
    hold_slab(sd - 0.14, LIFT_DEG, "r")
    arms_down(sd - 0.02, -40, "r")                                  # buông tay đỡ
    ears(sd, 20)
    ears(sd + 0.2, 8)
    for i, ob in enumerate(slab_dust[:2]):                          # bụi phụt ra khi phiến đá đập xuống
        pa = Vector((GLOW_AT.x + 0.22, GLOW_AT.y - 0.1 + 0.2 * i, STEP_TOP + 0.03))
        show(ob, sd, True)
        key(ob, "location", sd, pa)
        key(ob, "location", sd + 0.5, pa + Vector((0.1, -0.1 + 0.2 * i, 0.08)))
        show(ob, sd + 0.55, False)
    # đứng dậy trên bậc đá, xoay ba phần tư về máy, giữ la bàn ngang ngực
    s0, s1 = tm.STAND
    FACE = -40
    crouch(s0, 30)
    pose(s0, yaw=-90)
    grip(s0, ONE, tilt=50, hands="l")
    lumo.go(s1, SQ.x, SQ.z, SQ.y)
    pose(s1, lean=-4, yaw=FACE)
    for leg in L.legs:
        rot(leg, [(s1, (0, 0, 0))])
    squash(s0, 1.05, 0.92)
    squash(s1, 1, 1)
    grip(s1, CHEST)
    head(s1, 14, 0)                                                 # nhìn la bàn, tròn mắt
    ears(s1, 12)

    # ============================================================ S3: "Ồ! Kho báu!", thổi bụi, hắt xì, lau kính
    o0, o1 = tm.LUMO_LINE1
    ears(o0, 22)
    ears(o0 + 0.2, 8)
    head(o0, 4, 0)
    lumo.go(o0 + 0.4, SQ.x, SQ.z, SQ.y)
    lumo.go(o0 + 0.55, SQ.x, SQ.z + 0.07, SQ.y)                     # nhón người lên ở "Kho báu!"
    pose(o0 + 0.55, lean=-10)
    grip(o0 + 0.4, CHEST)
    grip(o0 + 0.6, RAISE)                                           # giơ la bàn lên (dưới tầm tai)
    lumo.go(o1, SQ.x, SQ.z, SQ.y)
    pose(o1 + 0.2, lean=-2)
    grip(o1 + 0.2, CHEST)
    head(o1 + 0.2, 12, 0)
    wag(L.tail, o0, tm.BLOW[0], 0.3, 25, base=(45, 0, 0))
    # cúi mõm thổi bụi: FOOOO!
    b0, b1 = tm.BLOW
    head(b0 - 0.3, 12, 0)
    head(b0, 26, 0)                                                 # mõm cúi sát mặt kính
    pose(b0, lean=6)
    grip(b0 - 0.2, CHEST)
    squash(b0 - 0.1, 0.97, 1.04)                                    # hít vào
    squash(b0 + 0.1, 1.04, 0.96)                                    # thổi
    squash(b1, 1, 1)
    grip(b1, CHEST)
    bpy.context.scene.frame_set(fr(b0))
    cpos = comp.root.matrix_world.translation.copy()
    nrm = (comp.root.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()
    bpy.context.scene.frame_set(fr(tm.DUST_BACK[1]))
    face_p = L.head.matrix_world @ Vector((0, -0.25, 0.14))
    for i, ob in enumerate(puffs):                                  # bụi bay khỏi mặt kính, ra xa…
        a = math.radians(360 * i / 7)
        out = cpos + nrm * 0.15 + Vector((0.16 * math.cos(a), 0.16 * math.sin(a), 0.1 + 0.04 * (i % 2)))
        show(ob, b0 + 0.05, True)
        key(ob, "location", b0 + 0.05, cpos + nrm * 0.03)
        key(ob, "location", b1, out)
        key(ob, "scale", b1, Vector((1.3, 1.3, 1.3)))
        key(ob, "location", tm.DUST_BACK[0], out + Vector((0, 0, 0.04)))   # …lơ lửng một nhịp…
        key(ob, "location", tm.DUST_BACK[1], face_p + Vector((0.04 * math.cos(a), 0.03 * math.sin(a), 0.03 * (i % 3))))   # …bay ngược vào mặt
        key(ob, "scale", tm.DUST_BACK[1], Vector((1.5, 1.5, 1.5)))
        show(ob, tm.DUST_BACK[1] + 0.05, False, 1.5)
    show(face_dust, tm.DUST_BACK[1], True)
    show(face_dust, tm.SNEEZE[0], False)                            # bụi tan, lộ mũi nhăn
    head(tm.DUST_BACK[0] + 0.2, 8, 0)
    ears(tm.DUST_BACK[1], -25)
    pose(tm.DUST_BACK[1], lean=-4)
    # hắt xì: nhăn mũi, tai giật lên
    z0, z1 = tm.SNEEZE
    hit = tm.SNEEZE_HIT
    t, i = z0, 0
    while t < hit - 0.2:                                            # mũi khịt khịt
        head(t, 4 if i % 2 else -2, 0)
        t, i = t + 0.12, i + 1
    pose(z0, lean=-2)
    pose(hit - 0.15, lean=-12)                                 # "Hắt…": ngửa ra lấy đà
    head(hit - 0.15, -16, 0)
    ears(z0 + 0.2, 10)
    ears(hit - 0.15, 24)
    squash(hit - 0.15, 0.95, 1.06)
    pose(hit, lean=12)                                         # "xì!": cả người giật tới
    head(hit, 26, 0)
    squash(hit, 1.07, 0.9)
    ears(hit + 0.04, -40)
    ears(hit + 0.12, 32)                                            # tai giật lên
    ears(hit + 0.3, 8)
    squash(hit + 0.2, 1, 1)
    grip(hit - 0.15, CHEST)
    grip(hit, (0.0, -0.28, 0.4), tilt=45)                           # la bàn giật theo
    grip(z1, CHEST)
    pose(z1, lean=0)
    head(z1, 10, 0)
    # lau mặt kính bằng vạt áo choàng: tay phía máy cầm la bàn, tay xa chà vạt áo qua lại trên mặt kính
    p0, p1 = tm.WIPE
    WIPE_C = (0.08, -0.27, 0.45)
    grip(p0 - 0.25, WIPE_C, tilt=45, hands="l")
    head(p0, 18, 0)
    show(cape, p0, True)
    t, i = p0, 0
    while t < p1 - 0.2:
        m = Matrix.Translation(WIPE_C) @ Euler((math.radians(45), 0, 0)).to_matrix().to_4x4()
        arm_to("r", t, m @ Vector((-0.04 if i % 2 else 0.05, 0.0, 0.05)))
        t, i = t + 0.15, i + 1
    show(cape, p1, False)
    arm_to("r", p1 + 0.1, (-0.2, -0.1, 0.27))
    show(comp.dust, p1 - 0.35, False)
    wag(L.tail, p0, p1, 0.4, 20, base=(35, 0, 0))
    grip(p1 + 0.2, CHEST)

    # ============================================================ S4: kính sáng le lói, sao rung rung, xoay phắt, TÍT… TÍT…
    gg = tm.GLASS_GLOW
    grip(gg - 0.3, CHEST)
    grip(gg, LIFT, tilt=40)                                         # đưa la bàn lên gần mặt nhìn
    head(gg, 16, 0)
    ears(gg + 0.1, 14)
    glass_e = bsdf_in(glass_m, "Emission Strength")

    def glass(t, v):
        glass_e.default_value = v
        glass_e.keyframe_insert("default_value", frame=fr(t))

    glass(0.0, 0.0)
    glass(gg - 0.2, 0.0)
    glass(gg + 0.3, 0.5)                                            # mặt kính lộ ra đang sáng le lói
    t, i = gg + 0.7, 0
    while t < tm.NEEDLE_SNAP[1]:
        glass(t, 0.3 if i % 2 else 0.6)
        t, i = t + 0.45, i + 1
    n0, n1 = tm.NEEDLE_WOBBLE
    head(n0 + 0.3, 20, 0, -8)                                       # nghiêng đầu, ngờ ngợ
    ears(n0 + 0.3, 4)
    st0, st1 = tm.STARTLE                                           # giật mình, la bàn tuột khỏi tay, chụp lại được
    back = Vector((math.sin(math.radians(-FACE)), math.cos(math.radians(FACE)), 0)) * 0.12   # lùi ra sau theo hướng mặt
    lumo.go(st0 - 0.05, SQ.x, SQ.z, SQ.y)
    lumo.go(st0 + 0.12, SQ.x + back.x, SQ.z + 0.16, SQ.y + back.y)   # bật lùi, nhảy dựng
    lumo.go(st0 + 0.35, SQ.x + back.x, SQ.z, SQ.y + back.y)
    lumo.go(st0 + 1.2, SQ.x, SQ.z, SQ.y)                            # bước lại chỗ cũ khi đã chụp được la bàn
    pose(st0 - 0.05, lean=0)
    pose(st0 + 0.12, lean=-22)
    pose(st0 + 0.6, lean=-10)
    pose(st0 + 1.2, lean=0)
    squash(st0 + 0.12, 0.92, 1.1)
    squash(st0 + 0.35, 1.06, 0.92)
    squash(st0 + 0.5, 1, 1)
    head(st0, -4, 0)
    ears(st0, 40)                                                   # tai dựng thẳng
    ears(st0 + 0.35, 30)
    ears(st0 + 0.7, -5)
    grip(st0, LIFT, tilt=40)
    for t, c, tl in ((st0 + 0.3, (0.05, -0.3, 0.76), 170), (st0 + 0.6, (-0.03, -0.29, 0.48), 290),
                     (st0 + 0.85, (0.03, -0.3, 0.66), 350), (st0 + 1.1, LIFT, 400)):
        key(hold, "location", t, Vector(c))                         # tung lên, rơi, nảy, chụp lại
        rot(hold, [(t, (tl, 0, 0))])
        for side, dx in (("l", 0.07), ("r", -0.07)):                # hai tay chới với theo la bàn
            arm_to(side, t, Vector(c) + Vector((dx, 0.0, -0.03)))
        head(t, 10 if c[2] < 0.6 else -12, 0)
    grip(st0 + 1.1, LIFT, tilt=40)
    head(st0 + 1.15, 10, 0)
    ears(st0 + 1.15, -12)
    grip(st1, LIFT, tilt=40)
    head(st1, 16, 0)
    ears(st1, 10)

    def beep(t, v=2.0, base=0.5):
        glass(t - 0.05, base)
        glass(t, v)
        glass(t + 0.18, base)

    for b in tm.BEEPS1:
        beep(b)

    # ============================================================ S5: cận la bàn, bức tường ở hậu cảnh
    i0, i1 = S["S5"]                                                # cú nhìn của Lumo: máy ở chỗ mắt, đầu ẩn (dưới)
    S5_C = (0.0, -0.28, 0.64)                                       # giơ la bàn lên trước mắt, mặt quay về mắt
    pose(i0 - 0.3, yaw=FACE)
    grip(i0 - 0.3, LIFT, tilt=40)
    pose(i0, lean=0, yaw=-88)                                       # quay về phía bức tường, dọc theo mũi sao
    grip(i0, S5_C, tilt=-48)
    grip(i1, S5_C, tilt=-48)
    pose(i1, yaw=-88)                                               # giữ hướng thân tới lúc đi vòng
    for b in tm.INSERT_BEEPS:
        beep(b)

    # ============================================================ S6–S8: đi vòng qua phiến đá tới đầu tường, quay lại
    a0, a1 = tm.AROUND
    path = [(a0, SQ.x, SQ.y, SQ.z), (a0 + 0.35, -8.62, 0.66, STEP_TOP + 0.04), (a0 + 0.7, -8.45, 0.8, LOW_Z),
            (a0 + 1.1, -8.42, 1.02, LOW_Z + 0.04), (a0 + 1.5, -8.55, 1.13, LOW_Z), (a1, SIDE.x, SIDE.y, SIDE.z)]
    pose(a0, yaw=-70)
    for k, (t, x, y, z) in enumerate(path):
        lumo.go(t, x, z, y)
        if k:
            pose(t, lean=4, yaw=yaw_to(path[k - 1][1:3], (x, y)) if k < len(path) - 1 else -90)
        grip(t, CHEST)
    steps(L.legs, a0, a1, 6, 25)
    pose(a1, lean=0, yaw=-90)                                  # tới sát đầu tường, mặt nghiêng vào tường
    head(a0, 14, 0)
    head(a1, 12, 0)
    wag(L.tail, a0, a1, 0.4, 18, base=(32, 0, 0))
    tb0, tb1 = tm.TURN_BACK
    # S7: máy thấp phía trước (-Y) nhìn chéo về đầu tường, tường (mặt trước, đầu tường) ở nửa trái khung. La bàn cầm ở phía máy
    # của thân (trước quay: tay trái; giữa cú: hai tay trước ngực; sau quay: tay phải) nên thân Lumo không nằm giữa mũi sao
    # và bức tường trên màn hình. Mặt la bàn luôn quay về máy, quai theo hướng mặt Lumo: vỏ xoay theo người, mũi sao đứng.
    s7a, s7b = S["S7"]
    CAM7, LOOK7 = Vector((-8.55, 0.22, -0.68)), Vector((-9.05, 0.85, -1.0))

    def grip_world(t, sides, wc):
        """La bàn ở điểm wc (thế giới), mặt quay về CAM7, quai theo hướng mặt Lumo; tay trong sides bám mép vỏ."""
        m = rootm()
        r = m.to_3x3()
        wc = Vector(wc)
        n = (CAM7 - wc).normalized()
        f = r @ Vector((0, -1, 0))
        bail = (f - n * f.dot(n)).normalized()
        wr = Matrix((bail.cross(n), bail, n)).transposed()
        key(hold, "location", t, m.inverted() @ wc)
        e = (r.inverted() @ wr).to_euler("XYZ", prev.get("hold", Euler()))
        prev["hold"] = e
        rot(hold, [(t, tuple(math.degrees(a) for a in e))])
        for sd in "lr":
            if sd not in sides:
                arms_down(t, 6, sd)
                continue
            sh = m @ SHOULDER[sd]
            d = sh - wc
            d = (d - n * d.dot(n)).normalized()
            rim = wc + d * (CR + 0.012)
            arm_to(sd, t, local(rim))

    P7 = (-8.745, 0.645, LOW_Z + 0.39)                                # la bàn gần như đứng yên phía máy, thân xoay quanh nó
    BEFORE, AFTER, MID = P7, P7, (-8.71, 0.865, LOW_Z + 0.46)
    pose(s7a, yaw=-70)                                              # đứng nghiêng mặt vào đầu tường
    grip_world(s7a, "l", BEFORE)
    pose(tb0, yaw=-70)
    grip_world(tb0, "l", BEFORE)
    tmid = (tb0 + tb1) / 2
    pose(tmid, yaw=-4)                                              # giữa cú quay: hai tay trước ngực, chuyền tay
    grip_world(tmid, "lr", MID)
    pose(tb1, yaw=62)                                               # quay lại nhìn phía vừa đi, qua mặt trước
    grip_world(tb1, "r", AFTER)
    pose(s7b - 0.05, yaw=62)
    grip_world(s7b - 0.05, "r", AFTER)
    head(tb1, 14, 0)
    ears(tb1, 16)
    ears(tb1 + 0.3, 6)
    head(tb1 + 0.8, 8, -60)                                         # liếc ra sau lưng theo mũi sao
    head(S["S7"][1] - 0.3, 14, 0)
    for b in (tb1 + 0.2, tb1 + 1.1):
        beep(b)
    # "Hừm… la bàn phải chỉ hướng Bắc chứ. Sao lại chỉ vào tường?"
    h0, h1 = tm.LUMO_LINE2
    lw = tm.LOOK_WALL
    pose(h0, yaw=62)
    pose(h0 + 0.6, yaw=25)                                     # nói về phía máy
    head(h0, 10, 0)
    head(h0 + 0.4, 12, 0, 16)                                       # "Hừm…": nghiêng đầu
    t, i = h0 + 1.0, 0
    while t < lw - 0.4:                                             # lắc lắc la bàn
        grip(t, CHEST, tilt=37 + (10 if i % 2 else -10))
        t, i = t + 0.3, i + 1
    grip(lw - 0.3, CHEST)
    ears(h0 + 1.0, -6)
    head(lw - 0.1, 12, 0)
    pose(lw - 0.1, yaw=25)
    pose(lw + 0.2, lean=-4, yaw=5)
    head(lw + 0.2, -6, -95)                                         # ngoái nhìn đầu tường sau lưng: mõm về phía tường
    ears(lw + 0.2, 10)
    head(h1 + 0.3, 10, 0)
    pose(h1 + 0.3, lean=0, yaw=20)
    grip(h1 + 0.3, CHEST)
    for b in (h0 + 1.1, lw + 0.5):
        beep(b)
    wag(L.tail, tb1, h1, 0.6, 16, base=(30, 0, 0))

    # ============================================================ S9: quay vào đầu tường, áp tai, gõ ba lần, hòn sỏi
    fw = tm.FACE_WALL
    sw1 = fw + 0.25                                                 # chuyền la bàn sang tay xa, để bên hông
    pose(fw - 0.15, yaw=20)
    lumo.go(fw - 0.15, SIDE.x, SIDE.z, SIDE.y)
    pose(fw + 0.15, yaw=-90)
    grip(fw, CHEST)
    grip(sw1, (-0.12, -0.2, 0.4), tilt=60, hands="lr")
    grip(sw1 + 0.25, HIP_R, tilt=80, yaw=-70, hands="r")
    arms_down(sw1 + 0.3, 8, "l")
    grip(sw1 + 0.3, HIP_R, tilt=80, yaw=-70, hands="r")
    head(fw, 6, 0)
    e0, e1 = tm.EAR_PRESS
    EAR_ROLL = -32
    lumo.go(e0, SIDE.x, SIDE.z, SIDE.y + 0.02)
    pose(e0, lean=0)
    head(e0, 6, 0)
    pose(e0 + 0.35, lean=8)                                    # nghiêng người về phía đầu tường
    head(e0 + 0.35, 0, 90, EAR_ROLL)                                # đầu ngoảnh ra máy, nghiêng: tai phải ép vào mặt đầu tường
    ear_r = next(e for e, s in L.ears if s < 0)
    rot(ear_r, [(e0 + 0.35, (-6, 0, 0))])
    key(ear_r, "scale", e0, Vector((1, 1, 1)))
    key(ear_r, "scale", e0 + 0.35, Vector((0.75, 1, 1)))            # tai bị ép dẹt
    lumo.go(e0 + 0.35, SIDE.x, SIDE.z, SIDE.y + 0.02)
    bpy.context.scene.frame_set(fr(e0 + 0.35))                      # dời người cho tai chạm đúng mặt đầu tường
    ear_minx = min((ear_r.matrix_world @ v.co).x for v in ear_r.data.vertices)
    EAR_X = SIDE.x + (WALL_END - 0.01) - ear_minx
    lumo.go(e0 + 0.35, EAR_X, SIDE.z, SIDE.y + 0.02)
    lumo.go(e1 - 0.2, EAR_X, SIDE.z, SIDE.y + 0.02)
    for t, a in ((e0 + 1.0, -6), (e0 + 1.1, 8), (e0 + 1.2, -6)):     # tai nhích một cái: không có gì
        rot(ear_r, [(t, (a, 0, 0))])
    head(e0 + 1.25, -6, 90, EAR_ROLL)                               # liếc lên
    head(e1 - 0.2, 0, 90, EAR_ROLL)
    head(e1, 4, 0, 0)
    key(ear_r, "scale", e1 - 0.2, Vector((0.75, 1, 1)))
    key(ear_r, "scale", e1, Vector((1, 1, 1)))
    pose(e1 - 0.2, lean=8)
    pose(e1, lean=0)
    ears(e1, 4)
    # gõ ba lần: TOK. TOK. TOK. (tay phía máy)
    lumo.go(e1, EAR_X, SIDE.z, SIDE.y + 0.02)
    lumo.go(e1 + 0.3, KNOCK.x, KNOCK.z, KNOCK.y)
    rot(L.arm_l, [(e1 + 0.3, (-20, 0, 0))])
    for k in tm.KNOCKS:
        rot(L.arm_l, [(k - 0.18, (-55, 0, 0)), (k, (-90, 0, 0)), (k + 0.12, (-70, 0, 0))])   # rút tay lấy đà, chạm mặt tường
        head(k, 8, 0)
        head(k + 0.1, 2, 0)
    ears(tm.KNOCKS[0], 12)
    # hòn sỏi lăn khỏi đá đỉnh tường, rơi trúng đỉnh đầu, nảy ra
    pb0, pb1 = tm.PEBBLE
    bpy.context.scene.frame_set(fr(pb1))
    top = L.head.matrix_world @ Vector((0, -0.02, 0.33))
    TOP_Z = 0.15 + 0.065                                            # mặt đá đỉnh tường ở đầu tường + bán kính hòn sỏi
    REST = Vector((-9.28, 1.0, TOP_Z))                              # nằm sẵn trên mép trước đá đỉnh tường, gần đầu tường
    pts = [(0.0, tuple(REST))]
    for k in tm.KNOCKS:                                             # mỗi tiếng gõ: sỏi nảy tại chỗ (gõ thì sỏi động)
        pts += [(k, tuple(REST)), (k + 0.07, tuple(REST + Vector((0.02, 0, 0.035)))), (k + 0.16, tuple(REST + Vector((0.02, 0, 0))))]
        REST = REST + Vector((0.02, 0, 0))
    pts += [(tm.KNOCKS[-1] + 0.2, tuple(REST)), (pb0 - 0.05, (-9.05, 1.0, TOP_Z)), (pb0, (-8.99, 1.0, TOP_Z - 0.02)),
           (pb0 + 0.2, (-8.9, 1.05, (TOP_Z + top.z) / 2 + 0.05)), (pb1, tuple(top)), (pb1 + 0.12, tuple(top + Vector((0, 0, 0.01)))),
           (pb1 + 0.3, (top.x + 0.2, top.y - 0.1, top.z + 0.15)), (pb1 + 0.6, (top.x + 0.45, top.y - 0.25, LOW_Z + 0.065)),
           (pb1 + 0.75, (top.x + 0.52, top.y - 0.3, LOW_Z + 0.1)), (pb1 + 0.9, (top.x + 0.58, top.y - 0.34, LOW_Z + 0.065))]
    for t, p in pts:
        key(pebble, "location", t, Vector(p))
    rot(pebble, [(tm.KNOCKS[-1] + 0.2, (0, 0, 0)), (pb1 + 0.9, (0, 720, 0))])
    show(pebble, HOLD, True)                                        # có sẵn trên đỉnh tường từ đầu cảnh, nằm lại trên nền tới hết cảnh
    head(pb1 - HOLD, 2, 0)
    head(pb1, 14, 0)                                                # cú cốc vào đầu
    squash(pb1 - HOLD, 1, 1)
    squash(pb1, 1.07, 0.9)
    squash(pb1 + 0.2, 1, 1)
    ears(pb1 - HOLD, 12)
    ears(pb1 + 0.05, 30)
    rot(L.arm_l, [(pb1 - 0.2, (6, 0, 0))])
    ed = tm.EARS_DROOP
    ears(ed, -55)                                                   # cụp tai
    head(ed + 0.3, -14, 30)                                         # ngước nhìn mép tường
    tail(ed, -10)
    # quay ba phần tư về máy, la bàn về tay phía máy (ngang bụng)
    pose(ed + 0.5, yaw=-90)
    pose(ed + 1.0, yaw=-5)                                          # ba phần tư mặt về máy S10 (yaw 15 = nhìn thẳng máy)
    grip(ed + 0.5, HIP_R, tilt=80, yaw=-70, hands="r")
    grip(ed + 1.0, (0.0, -0.24, 0.36), tilt=55, hands="lr")
    head(ed + 1.0, 8, 0)

    # ============================================================ S10: "Mình nghĩ bức tường không thích bị làm phiền."
    m0, m1 = tm.LUMO_LINE3
    BELLY = (0.14, -0.22, 0.38)                                     # mép vỏ cách vai trái ≤ ARM
    grip(m0 - 0.4, BELLY, tilt=55, hands="l")
    arms_down(m0 - 0.4, 6, "r")
    head(m0 - 0.4, 6, 0)
    ears(m0, -45)
    ears(m1, -50)
    t = m0 + 0.9                                                    # nhún vai sau "Mình nghĩ": chân giữ trên nền, nhún bằng thân, xoè tay, giữ dáng
    SPREAD_L = (0.25, -0.2, 0.42)                                   # la bàn chìa ra một chút (mép vỏ cách vai trái ≤ ARM)
    squash(t, 1, 1)
    squash(t + 0.2, 0.92, 1.1)
    squash(t + 0.75, 0.92, 1.1)
    squash(t + 1.0, 1, 1)
    head(t + 0.2, -6, 0, -10)                                       # rụt đầu, hơi nghiêng
    head(t + 0.75, -6, 0, -10)
    arms_down(t, 6, "r")
    arm_to("r", t + 0.2, (-0.42, -0.18, 0.32))                      # tay phải xoè chéo xuống dưới vai, ló ra ngoài viền thân (dưới khối đầu)
    arm_to("r", t + 0.75, (-0.42, -0.18, 0.32))
    arms_down(t + 1.0, 6, "r")
    grip(t, BELLY, tilt=55, hands="l")
    grip(t + 0.2, SPREAD_L, tilt=55, hands="l")
    grip(t + 0.75, SPREAD_L, tilt=55, hands="l")
    grip(t + 1.0, BELLY, tilt=55, hands="l")
    ears(t + 0.2, -60)
    ears(t + 0.75, -60)
    head(m0 + 0.5, 4, 0, -8)
    head(t + 1.0, 4, 0, -8)
    head(m1, 6, 0)
    gl = tm.GLANCE                                                  # liếc la bàn: mũi sao vẫn chỉ dọc tường
    grip(gl - 0.4, BELLY, tilt=55, hands="l")
    grip(gl, ONE, tilt=45, hands="l")
    head(gl, 18, 0)
    ears(gl + 0.2, -20)
    ears(gl + 0.5, 8)
    tail(gl + 0.2, 25)
    beep(gl + 0.4)
    pose(T_END, lean=0)

    # ============================================================ mũi sao: rung rung rồi xoay phắt, sau đó luôn chỉ phù điêu
    REST = 150
    rot(gcomp.needle, [(0.0, (0, 0, REST))])
    rot(comp.needle, [(0.0, (0, 0, REST)), (n0, (0, 0, REST))])
    t, i = n0 + 0.08, 0
    while t < n1:                                                   # rung rung, mạnh dần tới lúc xoay phắt
        rot(comp.needle, [(t, (0, 0, REST + (1 if i % 2 else -1) * (15 + 12 * (t - n0) / (n1 - n0))))])
        t, i = t + 0.08, i + 1
    sn0, sn1 = tm.NEEDLE_SNAP
    rot(comp.needle, [(sn0, (0, 0, REST)), (sn0 + 0.1, (0, 0, REST - 120)), (sn0 + 0.2, (0, 0, REST - 300))])

    def aim_angle(f, t):
        bpy.context.scene.frame_set(f)
        mw = comp.root.matrix_world
        if mw.to_scale().length < 1e-3:
            return None
        tgt = RELIEF
        if s7a <= t < s7b:                                          # cú S7: chỉ đúng phù điêu trên màn hình (giao điểm tia máy–đích)
            nrm = (mw.to_3x3() @ Vector((0, 0, 1))).normalized()
            ray = RELIEF - CAM7
            tgt = CAM7 + ray * ((mw.translation - CAM7).dot(nrm) / ray.dot(nrm))
        p = mw.inverted() @ tgt
        return math.degrees(math.atan2(-p.x, p.y))

    f_end = fr(T_END + 1.5)
    a_prev = None
    for f in range(fr(sn1), f_end + 1):
        a = aim_angle(f, (f - 1 + round(T0 * FPS)) / FPS)
        if a is None:
            continue
        if a_prev is None:                                          # xoay phắt hơn một vòng rồi mới dừng ở đích
            a -= 360 * math.ceil((a - (REST - 400)) / 360)
        else:
            a -= 360 * round((a - a_prev) / 360)
        a_prev = a
        t = (f - 1 + round(T0 * FPS)) / FPS
        off = -16 if t < sn1 + 0.08 else 7 if t < sn1 + 0.16 else 0   # vọt quá rồi về
        comp.needle.rotation_euler = (0, 0, math.radians(a + off))
        comp.needle.keyframe_insert("rotation_euler", frame=f)

    # ============================================================ cú nhìn của Lumo (S5), dựng riêng
    # Lumo đứng sát tường (cách mặt tường 0.35 m) nên máy ở chỗ mắt chỉ thấy mặt tường gần song song, mảng dây leo thành
    # một sợi. Máy lùi ra phía -Y (cách mặt tường khoảng 1.6 m) để thấy tường chéo khoảng 25°, phù điêu và dây leo ở nửa
    # trên khung; la bàn và hai khối tay dựng riêng trước máy ở nửa dưới khung, coi như la bàn Lumo giơ trước mắt. Lumo
    # thật nằm ngoài khung. Mũi sao trên màn hình hướng về phù điêu trên màn hình: chỉ vào giao điểm của tia máy–RELIEF
    # với mặt la bàn.
    end_t = offset + segment
    CAM5 = Vector((-8.6, -0.7, -0.3))
    h5 = (RELIEF - CAM5)
    h5.z = 0
    h5.normalize()

    def dir5(pitch):
        return (h5 * math.cos(math.radians(pitch)) + Vector((0, 0, math.sin(math.radians(pitch))))).normalized()

    rel_pitch = math.degrees(math.atan2((RELIEF - CAM5).z, ((RELIEF - CAM5).to_2d()).length))
    look5 = CAM5 + dir5(rel_pitch - 10)                             # phù điêu ở trên tâm khung 10°
    fwd5 = dir5(rel_pitch - 10)
    right5 = fwd5.cross(Vector((0, 0, 1))).normalized()
    up5 = right5.cross(fwd5)
    ic = CAM5 + dir5(rel_pitch - 16) * 0.38                         # la bàn dưới tâm khung 9°, trên dải CC; trong tầm tay thật
    nrm5 = ((CAM5 - ic).normalized() + up5 * 0.45).normalized()     # mặt la bàn quay về máy, ngửa lên một chút như cầm trước mắt
    yax5 = (up5 - nrm5 * up5.dot(nrm5)).normalized()
    m5 = Matrix((yax5.cross(nrm5), yax5, nrm5)).transposed().to_4x4()
    m5.translation = ic
    icomp.root.matrix_world = m5
    hit = RELIEF - CAM5                                             # giao điểm tia máy–phù điêu với mặt la bàn
    hit = CAM5 + hit * ((ic - CAM5).dot(nrm5) / hit.dot(nrm5))
    pl = m5.inverted() @ hit
    rot(icomp.needle, [(0.0, (0, 0, math.degrees(math.atan2(-pl.x, pl.y))))])
    lumo_m = cast_materials()["lumo"]
    ipaws = []
    for sx in (-1, 1):                                              # hai khối tay từ đáy khung bám mép vỏ hai bên
        p1 = m5 @ Vector((sx * (CR + 0.012), -0.01, 0))
        p0 = CAM5 + fwd5 * 0.14 - up5 * 0.2 + right5 * sx * 0.12    # gốc tay ở đáy khung, gần mắt như vai thật
        ln = (p1 - p0).length
        ob = add_obj(f"InsertPaw{'R' if sx > 0 else 'L'}", box_bm((0.08, 0.08, ln), (0, 0, ln / 2)), lumo_m, "PROPS")
        ob.matrix_world = Matrix.Translation(p0) @ Vector((0, 0, 1)).rotation_difference(p1 - p0).to_matrix().to_4x4()
        key(ob, "scale", -1.0, Vector((0, 0, 0)))
        ipaws.append(ob)
    if offset - 1e-6 <= i0 < end_t - 1e-6:
        hide_to = i1 if i1 < end_t - 1e-6 else offset + seconds + 1   # cú cuối của đoạn: giữ luôn qua phần đuôi
        for ob in (icomp.root, *ipaws):
            show(ob, i0, True)
            show(ob, hide_to, False)

    # ============================================================ máy quay (một máy mỗi cú; chỉ dựng các cú trong đoạn)
    CAMS = {   # (giây, vị trí máy, điểm nhìn, tiêu cự mm)
        "S1": [(S["S1"][0], (-8.35, -4.3, -0.6), (-8.4, 0.4, -0.85), 35)],                 # trung toàn: đống lá, phiến đá rêu, bậc đá
        "S2": [(S["S2"][0], (-9.6, -0.1, -0.72), (-9.27, 0.5, -1.12), 40)],                  # cận hốc từ trước bên trái: la bàn, tay rút ra
        "S3": [(S["S3"][0], (-8.97, -1.5, -0.55), (-8.82, 0.5, -0.8), 30),                  # mở cú thấp, bắt Lumo đang đứng dậy…
               (tm.STAND[1], (-8.97, -1.25, -0.32), (-8.8, 0.5, -0.45), 35)],               # …nâng lên trung cận, Lumo ba phần tư
        "S4": [(S["S4"][0], (-9.17, -0.5, -0.42), (-8.95, 0.32, -0.46), 32)],                # cận la bàn và mặt Lumo
        "S5": [(S["S5"][0], tuple(CAM5), tuple(look5), 24)],                                 # cú nhìn: la bàn trước mắt, tường và dây leo nhìn chéo
        "S6": [(S["S6"][0], (-7.55, -1.75, -0.55), (-8.6, 0.85, -0.88), 30)],                # trung: đi vòng qua phiến đá
        "S7": [(S["S7"][0], tuple(CAM7), tuple(LOOK7), 28)],                                 # cận la bàn, máy thấp phía trước nhìn chéo về đầu tường; tường nửa trái khung
        "S8": [(S["S8"][0], (-8.05, -1.05, -0.6), (-8.75, 1.1, -0.85), 32)],                 # trung: "Hừm…"
        "S9": [(S["S9"][0], (-7.55, -1.15, -0.45), (-8.9, 1.05, -0.55), 26)],                # trung ở đầu tường, nhìn chéo mặt đầu tường, đá đỉnh tường ở phần ba trên
        "S10": [(S["S10"][0], (-8.1, -1.1, -0.6), (-8.75, 1.15, -0.85), 32)],               # trung: chống chế, liếc la bàn
    }
    shots = [(n, a, b) for n, a, b in tm.SHOTS if a < end_t - 1e-6 and b > offset + 1e-6]
    cams = cameras(shots, {n: CAMS[n] for n, _, _ in shots})
    H = Vector((0, 0, 0.2))
    must = {"S1": [(L.head, H), (pile, Vector())], "S2": [(gcomp.root, Vector())], "S3": [(L.head, H)],
            "S4": [(L.head, Vector((0, -0.2, 0.1)))], "S5": [(icomp.root, Vector())], "S6": [(L.head, H)],
            "S7": [(comp.root, Vector())],
            "S8": [(L.head, H)], "S9": [(L.head, H)], "S10": [(L.head, H)]}
    extra = [("S1", hero, S["S1"][0], bf0 + 1.0), ("S2", comp.root, GRAB_T, S["S2"][1]), ("S3", comp.root, tm.STAND[1], S["S3"][1]),
             ("S4", comp.root, S["S4"][0], S["S4"][1]), ("S9", pebble, S["S9"][0], pb1 + 0.3)]
    check_in_frame(shots, cams, must, extra, ground=lambda p: ground_z(p.x))
    stills = [round((a + b) / 2, 2) for _, a, b in shots]
    stills += [t for t in (tm.CLIMB_OUT[0] + 0.5, tm.SLAB_LIFT[1], tm.GRAB[0] + 0.3, tm.LUMO_LINE1[0] + 0.6, tm.BLOW[0] + 0.4,
                           tm.DUST_BACK[1], tm.SNEEZE_HIT, tm.WIPE[0] + 0.5, tm.NEEDLE_SNAP[1] + 0.3, tm.STARTLE[0] + 0.3,
                           tm.INSERT_BEEPS[0], tm.AROUND[0] + 1.0, tm.TURN_BACK[0] - 0.3, tm.TURN_BACK[1] + 0.5,
                           tm.LOOK_WALL + 0.4, tm.EAR_PRESS[0] + 0.8, tm.KNOCKS[1], tm.PEBBLE[1], tm.EARS_DROOP + 0.4,
                           tm.GLANCE + 0.3, tm.LUMO_LINE3[0] + 1.3) if offset <= t < end_t]
    finish(out_blend, sorted(set(stills)))
