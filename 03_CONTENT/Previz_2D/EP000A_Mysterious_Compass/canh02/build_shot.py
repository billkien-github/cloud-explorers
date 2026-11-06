"""
EP000A Cảnh 2 (Ánh sáng lạ): previz 2D cutout (03_CONTENT/PREVIZ_2D.md, bộ nhân vật pipeline/cutout.py).
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #2#. Mốc thời gian và CC: timing.py; mọi
keyframe tính từ các mốc đó (cộng trừ vài phần mười giây cho nhịp lấy đà, giữ tư thế).
    pipeline/run.sh build -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh02
    pipeline/run.sh preview -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh02
    blender -b --factory-startup -P pipeline/cc.py -- <cảnh>/renders/canh02_preview.mp4 <cảnh>/timing.py <cảnh>/renders/canh02_preview_cc.mp4
Bố cục nối cuối Cảnh 1 (phế tích dùng chung với Cảnh 3: ../ruins.py): Lumo ngồi lút trong đống lá X -7.3, quay mặt sang
trái; phiến đá rêu con bướm đậu -8.05; phiến đá có ánh vàng trên bậc đá -8.75, la bàn trong hốc nông bên dưới; đầu tường
-9, tường chạy sang trái, mảng dây leo che phù điêu đám mây ở -12. Lumo ngồi xổm nhấc phiến đá ở -8.3, đi vòng qua phiến
đá tới đầu tường (-8.85), áp tai, gõ vào mặt đầu tường. Mũi sao luôn chỉ tâm phù điêu sau mảng dây leo: aim() của cutout
tính góc từng khung từ ma trận thế giới của la bàn (tay, người, lật gương, tung hứng đều đã tính). Cú cận la bàn có
tường ở hậu cảnh (S5, S7) dựng riêng ở X = 20: Lumo phóng to, tường và mảng dây leo vẽ thu gọn khoảng cách.
"""
import math
import pathlib
import random
import sys

import bpy

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.dont_write_bytecode = True                                  # không để __pycache__ cạnh timing.py
sys.path[:0] = [str(HERE), str(HERE.parent), str(ROOT / "pipeline")]   # timing.py của cảnh, ruins.py của tập, cutout
from cutout import *  # noqa: E402,F403  bộ cutout: keyframe, hình, mặt, nhân vật, máy quay, la bàn và hàm diễn la bàn
from timing import *  # noqa: E402,F403  FPS, SECONDS, SHOTS, mốc hành động, CC của cảnh
import ruins  # noqa: E402  phế tích dùng chung với Cảnh 3
from ruins import LOW_Z, RELIEF  # noqa: E402

OUT_BLEND = HERE / f"{HERE.name}.blend"
start(FPS)
SHOT = {name: (t0, t1) for name, t0, t1 in SHOTS}
HOLD = 1.0 / FPS
FACES["listen"] = ("closed", "smile", 16)                       # lắng nghe: nhắm mắt, mỉm, nhướng mày
FACES["open_listen"] = ("open", "closed", 16)
random.seed(5)

R = ruins.build_ruins()
CR = 0.065                                                      # bán kính vỏ la bàn trong tay Lumo


# ================================================================ nhân vật, đạo cụ
bfly = build_bfly("Butterfly", -0.6)
lumo = build_lumo(ruins.PILE_X, -0.32)
comp_hold, comp = build_holder(lumo, CR, "Compass")
dust = compass_bits(comp, CR)
far_hold, compF = build_holder(lumo, CR, "CompassFar", far=True)   # la bàn chuyền sang tay xa lúc gõ tường
gcomp = build_compass("GroundCompass", None, (ruins.COMPASS_SPOT[0], ruins.GLOW_Z - 0.02), 0.61, CR)   # la bàn nằm trong hốc
gcomp.root.scale = (1.0, 1.0, 0.72)                             # dưới phiến đá, nghiêng ngửa mặt
gdust = compass_bits(gcomp, CR)
ry(gcomp.needle, 0.0, 150)
cape_bit = part("Lumo_CapeCorner", lumo.arm_far, [([(-0.05, 0.0), (0.06, 0.02), (0.07, -0.07), (-0.02, -0.09)], "#FC6640"),
                                                  (band([(-0.02, -0.09), (0.07, -0.07)], 0.012), "#E8B33A")], -0.09, (0.0, -0.2))
puffs = [part(f"DustPuff{i}", None, [(ell(0.035 + 0.01 * (i % 3), 0.03 + 0.008 * (i % 2)), "#CDBE9F")], -0.7) for i in range(7)]
face_dust = part("Lumo_FaceDust", lumo.head, [(ell(0.13, 0.09, 0.16, 0.16), "#CDBE9F"), (ell(0.08, 0.06, 0.06, 0.24), "#D8CBB0"),
                                              (ell(0.07, 0.05, 0.25, 0.08), "#BFAF8E")], -0.03)
pebble = part("Pebble", None, [(ell(0.04, 0.035), "#9E9384"), (ell(0.016, 0.012, -0.01, 0.01), "#C4BAAB")], -0.6)
leaf_bits = [part(f"Leaf{i}", None, [(leaf_pts(0, 0, 1.8, 0), ruins.LEAF_COLS[i % 4])], -0.62) for i in range(6)]
slab_dust = [part(f"SlabDust{i}", None, [(ell(0.03, 0.022), "#CDBE9F")], 0.55) for i in range(4)]

# --- cú cận la bàn có tường ở hậu cảnh (S5, S7): X = 20, mảng dây leo ở mép trái, cách Lumo vài hàng đá
IX = 20.0
INS_TOP, INS_END = 0.5, 20.35                                   # đỉnh tường, đầu tường trong cú cận
INS_VINE = (18.68, 19.08)
INS_TARGET = (18.88, 0.05)                                       # phù điêu sau mảng dây leo (khuất)
part("Ins_Sky", None, [(rect(IX - 2, -1, IX + 2, 1), ruins.SKY), (ell(0.5, 0.18, IX + 0.9, 0.62), "#F7FBFD")], 1.6)
iblocks = [(rect(IX - 2, -1, INS_END, INS_TOP), ruins.STONE_D)]
for row, (z0, z1, xs) in enumerate(((-1.0, -0.35, (17.9, 18.7, 19.6, 20.35)), (-0.35, 0.1, (18.1, 19.05, 19.95, 20.35)),
                                    (0.1, INS_TOP, (18.0, 18.85, 19.75, 20.35)))):
    for x0, x1 in zip(xs, xs[1:]):
        iblocks.append((rrect(x1 - x0 - 0.06, z1 - z0 - 0.06, 0.06, (x0 + x1) / 2, (z0 + z1) / 2),
                        ruins.STONE if (row + int(x0 * 2)) % 2 else ruins.STONE_L))
iblocks += [(rect(INS_END - 0.12, -1, INS_END, INS_TOP), "#9A8B72"), (ell(0.6, 0.08, 19.5, INS_TOP + 0.02), ruins.MOSS),
            (ell(0.4, 0.07, 20.1, INS_TOP + 0.02), ruins.MOSS)]
part("Ins_Wall", None, iblocks, 1.2)
ivines = []
for k in range(7):
    vx = INS_VINE[0] + (INS_VINE[1] - INS_VINE[0]) * (k + 0.5) / 7
    pts = [(vx + 0.03 * math.sin(j * 1.3 + k), INS_TOP - (0.85 + 0.12 * math.sin(k * 1.7)) * j / 8) for j in range(9)]
    ivines.append((band(pts, 0.04), "#4F8A2E"))
    ivines += [(leaf_pts(x + (0.035 if j % 2 else -0.035), z, 3.0, 35 if j % 2 else -35), "#6FAE45" if (j + k) % 2 else "#86C04E")
               for j, (x, z) in enumerate(pts) if j > 0]
part("Ins_Vines", None, ivines + [(ell(0.28, 0.09, sum(INS_VINE) / 2, INS_TOP), "#5E9437")], 1.1)
part("Ins_Floor", None, [(rect(IX - 2, -1.0, IX + 2, -0.62), "#9CC85A")], 1.0)
BIG_S = 2.4
big_scale = node("BigLumo_Scale", None, (IX + 0.7, -1.26), -0.3)
big_scale.scale = (BIG_S, BIG_S, BIG_S)
big = build_lumo(0.0, 0.0)
big.root.parent = big_scale
big.root.location = (0.0, 0.0, 0.0)
big_hold, bcomp = build_holder(big, 0.13, "BigCompass")
for ob in (cape_bit, face_dust, pebble, *puffs, *leaf_bits, *slab_dust):
    show(ob, 0.0, False)


# ================================================================ trạng thái đầu cảnh (khớp khung cuối Cảnh 1)
POP_Z = LOW_Z - 0.1
lumo.dir = -1
scl(lumo.root, 0.0, -1, 1)
at(lumo.root, 0.0, ruins.PILE_X, POP_Z)
lean(lumo, 0.0, 0)
fc(lumo, 0.0, "wonder")
look(lumo, 0.0, 1.0, -0.3)
ears(lumo, 0.0, 8)
ry(lumo.head, 0.0, 0)
chold(lumo, comp_hold, 0.0, 6, -6)
ry(lumo.tail, 0.0, 20)
show(comp.root, 0.0, False)
show(gcomp.root, 0.0, False)                                    # lộ ra khi phiến đá nhấc lên
for ob in (gcomp.glow, comp.glow, bcomp.glow, compF.glow):
    show(ob, 0.0, False)

# ================================================================ S1: chui ra khỏi đống lá, bước tới phiến đá, ngồi xổm nhấc lên
c0, c1 = CLIMB_OUT
at(lumo.root, c0, ruins.PILE_X, POP_Z)
at(lumo.root, c0 + 0.2, ruins.PILE_X, POP_Z - 0.06)             # lấy đà
squash(lumo, c0, 1, 1)
squash(lumo, c0 + 0.2, 1.06, 0.92)
at(lumo.root, c0 + 0.45, ruins.PILE_X - 0.05, LOW_Z + 0.12)      # bật lên khỏi đống lá
squash(lumo, c0 + 0.45, 0.95, 1.06)
at(lumo.root, c0 + 0.8, ruins.PILE_X - 0.35, LOW_Z + 0.2)        # bước qua mép đống lá
at(lumo.root, c1 - 0.2, -7.85, LOW_Z)
squash(lumo, c1 - 0.2, 1.05, 0.95)
squash(lumo, c1, 1, 1)
lean(lumo, c0 + 0.45, -6)
lean(lumo, c0 + 0.8, 8)
lean(lumo, c1, 0)
ears(lumo, c0 + 0.2, -10)
ears(lumo, c0 + 0.45, 14)
ears(lumo, c1, 6)
fc(lumo, c0 + 0.45, "eager")
look(lumo, c0 + 0.45, 1.0, -0.4)                               # mắt không rời ánh vàng
ry(lumo.arm, c0 + 0.45, -40)
ry(lumo.arm_far, c0 + 0.45, -30)
chold(lumo, comp_hold, c1, 4, -4)
scl(R.pile, c0 + 0.3, 1, 1)
scl(R.pile, c0 + 0.5, 1.1, 0.88)
scl(R.pile, c0 + 0.8, 0.96, 1.05)
scl(R.pile, c1, 1, 1)
for i, ob in enumerate(leaf_bits):                              # lá rơi khỏi người
    fly_bit(ob, c0 + 0.45 + 0.05 * i, (ruins.PILE_X - 0.1 + 0.05 * i, LOW_Z + 0.6 - 0.05 * i),
            (ruins.PILE_X - 0.5 + 0.12 * i, LOW_Z + 0.02), c0 + 1.2 + 0.08 * i, 240, 0.15)
loop(lumo.tail, c1, WALK_SLAB[1], 0.5, 18, 36)
# bước tới phiến đá
w0, w1 = WALK_SLAB
SQ_X, SQ_Z, SQ_LEAN = -8.12, LOW_Z - 0.05, 28                # đủ xa để tay với được mép phiến đá
walk(lumo.root, w0, w1, -7.85, SQ_X, 2, 0.035, LOW_Z)
q0, q1 = SQUAT
at(lumo.root, q0, SQ_X, LOW_Z)
at(lumo.root, q1, SQ_X, SQ_Z)
squash(lumo, q0, 1, 1)
squash(lumo, q1, 1.05, 0.9)
lean(lumo, q0, 0)
lean(lumo, q1, SQ_LEAN)
ry(lumo.head, q1, 6)
look(lumo, q1, 0.9, -0.9)
fc(lumo, q1, "eager", SQ_LEAN + 6)
bl(lumo, 2.6)
# nhấc phiến đá: khớp ở mép sát tường, mép gần Lumo nâng lên 45°
l0, l1 = SLAB_LIFT
near_edge = (ruins.SLAB[0] + ruins.SLAB_W / 2 - 0.02, ruins.SLAB[1])
a_edge = reach(lumo, SQ_X, SQ_Z, SQ_LEAN, near_edge)
LIFT_DEG = 28                                                  # mép gần nâng lên tới ngang ngực, không lên mặt
lift_edge = (ruins.SLAB[0] - ruins.SLAB_W / 2 + (ruins.SLAB_W - 0.02) * math.cos(math.radians(LIFT_DEG)),
             ruins.SLAB[1] - ruins.SLAB_H / 2 + (ruins.SLAB_W - 0.02) * math.sin(math.radians(LIFT_DEG)) + ruins.SLAB_H)
a_up = reach(lumo, SQ_X, SQ_Z, SQ_LEAN, lift_edge)
a_up_far = reach(lumo, SQ_X, SQ_Z, SQ_LEAN, lift_edge, (-0.01, 0.46))
chold(lumo, comp_hold, l0 - 0.3, 4, -4)
chold(lumo, comp_hold, l0, a_edge, a_edge + 4)
ry(R.slab, l0 + 0.1, 0)
ry(R.slab, l0 + 0.35, -8)                                       # nặng, nhích lên chút
ry(R.slab, l1, -LIFT_DEG)
chold(lumo, comp_hold, l0 + 0.35, a_edge - 6, a_edge - 2)
chold(lumo, comp_hold, l1, a_up, a_up_far)
lean(lumo, l0 + 0.35, SQ_LEAN + 4)
lean(lumo, l1, SQ_LEAN - 4)
fc(lumo, l0 + 0.2, "squint", SQ_LEAN)                           # gắng sức
ears(lumo, l0 + 0.2, -10)
for i, ob in enumerate(slab_dust):                              # bụi bung ra quanh mép phiến đá
    fly_bit(ob, l0 + 0.4, (ruins.SLAB[0] - 0.1 + 0.07 * i, ruins.SLAB[1]), (ruins.SLAB[0] - 0.3 + 0.2 * i, ruins.SLAB[1] + 0.05),
            l0 + 1.0, 90, 0.12)
for i, t in enumerate(steps(0.0, l0, 0.6)):                     # ánh vàng le lói qua khe phiến đá (như cuối Cảnh 1)
    scl(R.glow, t, 1.0 if i % 2 else 0.85, 1.0 if i % 2 else 0.85)
twinkle(R.glint, 0.0, l0, 1.4, 0.6, 0.35)
scl(R.glow, l0 + 0.4, 1.0, 1.0)
scl(R.glow, l1, 1.5, 1.35)                                      # ánh vàng bung ra
show(gcomp.root, l0 + 0.3, True)
show(gcomp.glow, l0 + 0.3, False)
show(R.glint, l0 + 0.4, False)
fc(lumo, COMPASS_SEE, "wonder", SQ_LEAN)
ears(lumo, COMPASS_SEE - 0.05, -10)
ears(lumo, COMPASS_SEE + 0.12, 16)
ears(lumo, COMPASS_SEE + 0.3, 8)
look(lumo, COMPASS_SEE, 0.8, -1.0)
loop(lumo.tail, COMPASS_SEE, GRAB[0], 0.3, 25, 45)              # đuôi ngoe nguẩy

# ================================================================ S2–S3: rút la bàn ra, "Ồ! Kho báu!", thổi bụi, hắt xì, lau kính
g0, g1 = GRAB
spot = (ruins.COMPASS_SPOT[0] + 0.02, ruins.COMPASS_SPOT[1] - 0.02)
a_spot = reach(lumo, SQ_X, SQ_Z, SQ_LEAN + 17, spot)
ry(lumo.arm_far, g0, a_up_far)                                  # tay xa vẫn đỡ phiến đá
ry(lumo.arm, g0, a_up)
ry(comp_hold, g0, -a_up)
ry(lumo.arm, g0 + 0.25, a_spot)
ry(comp_hold, g0 + 0.25, -a_spot)
lean(lumo, g0 + 0.25, SQ_LEAN + 17)                             # chồm tới thò tay vào hốc
show(gcomp.root, g0 + 0.3, False)
show(comp.root, g0 + 0.3, True)
show(comp.glow, g0 + 0.3, True)
glow(comp, g0 + 0.3, 0.6)                                       # dưới lớp bụi đã sáng le lói
show(R.glow, g0 + 0.3, False)
ry(lumo.arm, g1, -70)
ry(comp_hold, g1, 70)
lean(lumo, g1, SQ_LEAN - 4)
fc(lumo, g0 + 0.3, "eager", SQ_LEAN)
look(lumo, g1, 0.7, -0.4)
# thả phiến đá rơi về chỗ: CỘP
ry(R.slab, SLAB_DROP - 0.12, -LIFT_DEG)
ry(R.slab, SLAB_DROP, 0)
ry(R.slab, SLAB_DROP + 0.06, -3)
ry(R.slab, SLAB_DROP + 0.12, 0)
ry(lumo.arm_far, SLAB_DROP - 0.14, a_up_far)
ry(lumo.arm_far, SLAB_DROP - 0.02, -40)
ears(lumo, SLAB_DROP, 18)
ears(lumo, SLAB_DROP + 0.2, 8)
bl(lumo, SLAB_DROP + 0.02)
# đứng dậy, giữ la bàn ngang ngực
s0, s1 = STAND
at(lumo.root, s0, SQ_X, SQ_Z)
at(lumo.root, s1, SQ_X, LOW_Z)
squash(lumo, s0, 1.05, 0.9)
squash(lumo, s1, 1, 1)
lean(lumo, s0, SQ_LEAN - 4)
lean(lumo, s1, -4)
chold(lumo, comp_hold, s1, -85, -78)
ry(lumo.head, s1, 4)
fc(lumo, s1, "wonder", 4)
look(lumo, s1, 0.8, -0.6)
# "Ồ! Kho báu!"
o0, o1 = LUMO_LINE1
fc(lumo, o0 - 0.05, "shout")
talk(lumo, o0, o0 + 0.3, "o")                                   # "Ồ!"
talk(lumo, o0 + 0.45, o1, "smile")                              # "Kho báu!"
ears(lumo, o0, 16)
ears(lumo, o0 + 0.2, 6)
at(lumo.root, o0 + 0.4, SQ_X, LOW_Z)
at(lumo.root, o0 + 0.55, SQ_X, LOW_Z + 0.06)                    # nhón người lên ở "Kho báu!"
at(lumo.root, o1, SQ_X, LOW_Z)
chold(lumo, comp_hold, o0 + 0.4, -85, -78)
chold(lumo, comp_hold, o0 + 0.6, -96, -90)                      # giơ la bàn lên (dưới tầm tai)
chold(lumo, comp_hold, o1 + 0.2, -80, -72)
lean(lumo, o0 + 0.55, -8)
lean(lumo, o1 + 0.2, -2)
loop(lumo.tail, o0, BLOW[0], 0.3, 25, 50)
fc(lumo, o1 + 0.05, "happy")
# cúi mõm thổi bụi: FOOOO!
b0, b1 = BLOW
ry(lumo.head, b0 - 0.3, 4)
ry(lumo.head, b0, 22)                                           # cúi mõm xuống mặt kính
lean(lumo, b0, 4)
chold(lumo, comp_hold, b0 - 0.2, -80, -72)
fc(lumo, b0 - 0.1, "neutral", 26)
look(lumo, b0 - 0.1, 0.6, -1.0)
mouth(lumo, b0, "o")
squash(lumo, b0 - 0.1, 0.98, 1.03)                              # hít vào
squash(lumo, b0 + 0.1, 1.03, 0.97)
squash(lumo, b1, 1, 1)
cpos = hand(lumo, SQ_X, LOW_Z, -80, 4)
cx, cz = cpos[0], cpos[1] + CR
for i, ob in enumerate(puffs):                                  # bụi bay khỏi mặt kính, ra xa...
    a = math.radians(140 + 25 * i)
    out = (cx + 0.18 * math.cos(a) - 0.05, cz + 0.12 * math.sin(a) + 0.08)
    show(ob, b0 + 0.05, True)
    at(ob, b0 + 0.05, cx, cz)
    at(ob, b1, *out)
    scl(ob, b0 + 0.05, 0.4, 0.4)
    scl(ob, b1, 1.2, 1.2)
    head_c = (SQ_X - 0.2 + 0.03 * (i % 3), LOW_Z + 0.68 + 0.03 * (i % 2))   # ...rồi bay ngược vào mặt
    at(ob, DUST_BACK[1], *head_c)
    scl(ob, DUST_BACK[1], 1.4, 1.4)
    show(ob, DUST_BACK[1] + 0.05, False)
show(face_dust, DUST_BACK[1], True)
show(face_dust, SNEEZE[0], False)                               # bụi tan, lộ mũi nhăn
mouth(lumo, b1, "closed")
fc(lumo, DUST_BACK[0] + 0.2, "squint", 10)
ry(lumo.head, DUST_BACK[0] + 0.2, 10)
ears(lumo, DUST_BACK[1], -20)
# hắt xì: nhăn mũi, tai giật lên
z0, z1 = SNEEZE
for t in steps(z0, SNEEZE_HIT - 0.15, 0.12):                    # mũi khịt khịt
    ry(lumo.head, t, -4 if int((t - z0) / 0.12) % 2 else -10)
lean(lumo, z0, -2)
lean(lumo, SNEEZE_HIT - 0.15, -10)                              # "Hắt…": ngửa ra lấy đà
ears(lumo, z0 + 0.2, 10)
ears(lumo, SNEEZE_HIT - 0.15, 22)
mouth(lumo, SNEEZE_HIT - 0.4, "o")
ry(lumo.head, SNEEZE_HIT - 0.15, -14)
ry(lumo.head, SNEEZE_HIT, 24)                                   # "xì!": đầu giật tới
lean(lumo, SNEEZE_HIT, 10)
mouth(lumo, SNEEZE_HIT, "open")
ears(lumo, SNEEZE_HIT - 0.05, 22)
ears(lumo, SNEEZE_HIT + 0.04, -35)
ears(lumo, SNEEZE_HIT + 0.12, 30)                               # tai giật lên
ears(lumo, SNEEZE_HIT + 0.3, 6)
squash(lumo, SNEEZE_HIT - 0.15, 0.96, 1.05)
squash(lumo, SNEEZE_HIT, 1.06, 0.92)
squash(lumo, SNEEZE_HIT + 0.2, 1, 1)
ry(lumo.head, z1, 6)
lean(lumo, z1, 0)
fc(lumo, z1, "sheepish", 6)
chold(lumo, comp_hold, SNEEZE_HIT - 0.15, -80, -72)
chold(lumo, comp_hold, SNEEZE_HIT, -70, -64)
chold(lumo, comp_hold, z1, -82, -60)
# lau mặt kính bằng vạt áo choàng
p0, p1 = WIPE
ry(lumo.head, p0, 14)
fc(lumo, p0, "neutral", 14)
look(lumo, p0, 0.7, -0.9)
show(cape_bit, p0, True)
for i, t in enumerate(steps(p0, p1 - 0.2, 0.15)):
    ry(lumo.arm_far, t, -76 if i % 2 else -96)                  # vạt áo choàng chà qua chà lại mặt kính
show(cape_bit, p1, False)
ry(lumo.arm_far, p1 + 0.1, -62)
show(dust, p1 - 0.35, False)
loop(lumo.tail, p0, p1, 0.4, 20, 34)

# ================================================================ S4: kính sáng le lói, ngôi sao rung rung, xoay phắt, TÍT… TÍT…
LIFT_A = -92                                                    # đưa la bàn lên sát mặt nhìn
chold(lumo, comp_hold, GLASS_GLOW - 0.3, -82, -60)
chold(lumo, comp_hold, GLASS_GLOW, LIFT_A, -70)
ry(lumo.head, GLASS_GLOW, 10)
fc(lumo, GLASS_GLOW + 0.1, "wonder", 10)
look(lumo, GLASS_GLOW + 0.1, 0.8, -0.4)
ears(lumo, GLASS_GLOW + 0.1, 12)
glow(comp, GLASS_GLOW, 0.75)
for i, t in enumerate(steps(GLASS_GLOW + 0.4, NEEDLE_SNAP[1], 0.45)):
    scl(comp.glow, t, 0.7 if i % 2 else 0.8, 0.7 if i % 2 else 0.8)
n0, n1 = NEEDLE_WOBBLE
REST = 150                                                      # mũi sao nằm yên khi còn bụi (chỉ bừa)
ry(comp.needle, 0.0, REST)
ry(comp.needle, n0, REST)
for i, t in enumerate(steps(n0 + 0.08, n1, 0.08)):              # rung rung, mạnh dần tới lúc xoay phắt (chỉ mũi sao)
    ry(comp.needle, t, REST + (1 if i % 2 else -1) * (15 + 10 * (t - n0) / (n1 - n0)))
ry(comp.needle, NEEDLE_SNAP[0], REST)
fc(lumo, n0 + 0.3, "puzzled", 10)
ry(lumo.head, n0 + 0.3, 16)
look(lumo, n0 + 0.3, 0.8, -0.6)
ears(lumo, n0 + 0.3, 4)
# giật mình, la bàn tuột khỏi tay, chụp lại được
st0, st1 = STARTLE
fc(lumo, st0, "shock")
ears(lumo, st0, 26)
ears(lumo, st0 + 0.15, -5)
at(lumo.root, st0, SQ_X, LOW_Z)
at(lumo.root, st0 + 0.12, SQ_X, LOW_Z + 0.08)
at(lumo.root, st0 + 0.3, SQ_X, LOW_Z)
squash(lumo, st0, 0.95, 1.06)
squash(lumo, st0 + 0.3, 1, 1)
lean(lumo, st0, -8)
ry(lumo.head, st0, -6)
REST_LOC = (0.0, CR + 0.004)
for t, (x, z), a in ((st0, REST_LOC, 0), (st0 + 0.3, (0.04, 0.24), 130), (st0 + 0.6, (-0.03, 0.02), 250), (st0 + 0.85, (0.03, 0.17), 310),
                     (st0 + 1.1, REST_LOC, 360)):
    key(comp.root, "location", t, (x, -0.004, z))               # tung lên, rơi, nảy, chụp lại
    ry(comp.root, t, a)
for t, a in ((st0, LIFT_A), (st0 + 0.3, -125), (st0 + 0.6, -70), (st0 + 0.85, -110), (st0 + 1.1, -95)):
    ry(lumo.arm, t, a)                                          # tay chới với theo la bàn
    ry(comp_hold, t, -a)
for t, a in ((st0 + 0.3, -110), (st0 + 0.6, -75), (st0 + 0.85, -100), (st0 + 1.1, -88)):
    ry(lumo.arm_far, t, a)
look(lumo, st0 + 0.3, 0.6, 0.4)
look(lumo, st0 + 0.6, 0.6, -0.6)
look(lumo, st0 + 0.85, 0.7, 0.0)
fc(lumo, st0 + 1.15, "sheepish")
ears(lumo, st0 + 1.15, -12)
look(lumo, st1, 0.8, -0.5)
fc(lumo, st1, "wonder", 6)
ry(lumo.head, st1, 6)
ears(lumo, st1, 10)
chold(lumo, comp_hold, st1, -90, -86)
for t in (BEEPS1[0], BEEPS1[1]):
    beep(comp, t, 0.75, 1.05)
jitter(comp.root, st1 + 0.1, SECONDS, 0.0025, 0.07)            # rung khẽ (mức "còn cách một quãng")

# ================================================================ S6–S8: đi vòng sang phía bên kia phiến đá, quay lại, "la bàn phải chỉ hướng Bắc"
SIDE_X = -8.78                                                  # giữa phiến đá và đầu tường: lưng sát đầu tường khi quay sang phải
a0, a1 = AROUND
walk(lumo.root, a0, a1, SQ_X, SIDE_X, 3, 0.04, LOW_Z)
chold(lumo, comp_hold, a0, -78, -72)
look(lumo, a0, 0.7, -0.7)
fc(lumo, a0, "puzzled")
loop(lumo.tail, a0, a1, 0.4, 18, 32)
tb0, tb1 = TURN_BACK
facing(lumo, tb1, 1, tb1 - tb0)
look(lumo, tb1, 0.7, -0.7)
ry(lumo.head, tb1, 10)
fc(lumo, tb1, "wonder", 10)
ears(lumo, tb1, 14)
ears(lumo, tb1 + 0.3, 6)
for t in (TURN_BACK[1] + 0.2, TURN_BACK[1] + 1.1):
    beep(comp, t, 0.72, 0.95)
# "Hừm… la bàn phải chỉ hướng Bắc chứ. Sao lại chỉ vào tường?"
h0, h1 = LUMO_LINE2
fc(lumo, h0 - 0.05, "puzzled", 10)
talk(lumo, h0, h0 + 0.5, "closed")                              # "Hừm…"
ry(lumo.head, h0, 10)
ry(lumo.head, h0 + 0.4, 18)                                     # nghiêng đầu
talk(lumo, h0 + 0.8, LOOK_WALL - 0.2, "o")                      # "la bàn phải chỉ hướng Bắc chứ."
for i, t in enumerate(steps(h0 + 1.0, LOOK_WALL - 0.4, 0.3)):  # lắc lắc la bàn
    chold(lumo, comp_hold, t, -76 + (6 if i % 2 else -6), -70)
ears(lumo, h0 + 1.0, -6)
look(lumo, LOOK_WALL - 0.1, 0.7, -0.7)
look(lumo, LOOK_WALL + 0.15, -1.0, 0.3)                         # ngoái nhìn bức tường sau lưng
ry(lumo.head, LOOK_WALL + 0.2, -12)
lean(lumo, LOOK_WALL + 0.2, -4)
fc(lumo, LOOK_WALL, "puzzled", -12)
talk(lumo, LOOK_WALL, h1, "o")                                  # "Sao lại chỉ vào tường?"
ears(lumo, LOOK_WALL + 0.2, 10)
chold(lumo, comp_hold, LOOK_WALL, -76, -70)
look(lumo, h1 + 0.3, 0.7, -0.6)
ry(lumo.head, h1 + 0.3, 6)
lean(lumo, h1 + 0.3, 0)
bl(lumo, h1 + 0.5)
for t in (LUMO_LINE2[0] + 1.1, LOOK_WALL + 0.5):
    beep(comp, t, 0.72, 0.95)

# ================================================================ S9: quay vào đầu tường, áp tai, gõ ba lần, hòn sỏi
# quay mặt vào đầu tường; chuyền la bàn sang tay xa (để bên hông) cho tay gần rảnh
EAR_X, KNOCK_X = -8.65, -8.75
facing(lumo, FACE_WALL, -1, 0.15)
at(lumo.root, FACE_WALL - 0.15, SIDE_X, LOW_Z)
at(lumo.root, FACE_WALL + 0.2, EAR_X, LOW_Z)
SWAP1 = FACE_WALL + 0.25
chold(lumo, comp_hold, FACE_WALL, -70, -60)
chold(lumo, comp_hold, SWAP1 - 0.1, -40, -40)
show(comp.root, SWAP1, False)
show(compF.root, 0.0, False)
show(compF.root, SWAP1, True)
glow(compF, SWAP1, 0.7)
jitter(compF.root, SWAP1, SHOT["S10"][0], 0.0025, 0.07)
ry(lumo.arm_far, SWAP1, -40)
ry(far_hold, SWAP1, 40)
ry(lumo.arm_far, SWAP1 + 0.25, -8)                              # la bàn để bên hông
ry(far_hold, SWAP1 + 0.25, 8)
ry(lumo.arm, SWAP1 + 0.1, -10)
look(lumo, FACE_WALL, 1.0, 0.0)
fc(lumo, FACE_WALL, "puzzled")
# nghiêng đầu, ép tai gần sát mặt đầu tường, mắt liếc ngang lắng nghe; không có gì
e0, e1 = EAR_PRESS
lean(lumo, e0, 0)
lean(lumo, e0 + 0.35, 6)                                        # nghiêng người về phía đầu tường
ry(lumo.head, e0, 0)
ry(lumo.head, e0 + 0.35, 22)                                    # nghiêng đầu, tai gần áp dọc mép đầu tường
ry(lumo.ear_near, e0 + 0.35, 12)                                # tai gần ngả vào, áp lên mép đầu tường
scl(lumo.ear_near, e0 + 0.35, 0.8, 1)                           # tai bị ép dẹt lại
ry(lumo.ear_far, e0 + 0.35, -10)
fc(lumo, e0 + 0.35, "open_listen", 28)                          # mắt mở liếc ngang, mím miệng
look(lumo, e0 + 0.35, -0.7, 0.4)
look(lumo, e0 + 0.9, -0.7, 0.4)
for t, a in ((e0 + 1.0, 12), (e0 + 1.1, -2), (e0 + 1.2, 12)):     # tai nhích một cái: không có gì
    ry(lumo.ear_near, t, a)
look(lumo, e0 + 1.25, 0.2, 0.7)                                 # liếc lên
bl(lumo, e0 + 1.45)
look(lumo, e1 - 0.2, 0.2, 0.7)
ry(lumo.head, e1 - 0.2, 22)
ry(lumo.head, e1, 0)
scl(lumo.ear_near, e1 - 0.2, 0.8, 1)
scl(lumo.ear_near, e1, 1, 1)
lean(lumo, e1, 0)
ears(lumo, e1, 4)
fc(lumo, e1, "puzzled")
look(lumo, e1, 1.0, 0.0)
# gõ ba lần: TOK. TOK. TOK.
at(lumo.root, e1, EAR_X, LOW_Z)
at(lumo.root, e1 + 0.25, KNOCK_X, LOW_Z)
a_knock = reach(lumo, KNOCK_X, LOW_Z, -2, (ruins.WALL_END - 0.01, LOW_Z + 0.5))
ry(lumo.arm, SWAP1 + 0.1, -40)
for k in KNOCKS:
    ry(lumo.arm, k - 0.18, a_knock + 16)                        # rút tay lấy đà
    ry(lumo.arm, k, a_knock)                                    # chạm mặt tường
    ry(lumo.arm, k + 0.12, a_knock + 8)
    ry(lumo.head, k, 2)
    ry(lumo.head, k + 0.1, -2)
lean(lumo, KNOCKS[0] - 0.3, -2)
fc(lumo, KNOCKS[0] - 0.3, "eager")
ears(lumo, KNOCKS[0], 10)
# hòn sỏi lăn khỏi mép tường, rơi trúng đầu, nảy ra
pb0, pb1 = PEBBLE
CAMS_S9 = (-8.85, -0.64, 1.75)
head_top = (KNOCK_X - 0.05, LOW_Z + 0.9)
S9_TOP = CAMS_S9[1] + CAMS_S9[2] * 9 / 32                      # mép trên khung S9
for t, x, z in ((pb0 - 0.3, ruins.WALL_END - 0.05, ruins.WALL_TOP + 0.03), (pb0 - 0.05, ruins.WALL_END + 0.01, S9_TOP + 0.05),
                (pb0, ruins.WALL_END + 0.03, S9_TOP - 0.02),     # lăn khỏi mép đầu tường, rơi trong khung suốt PEBBLE
                (pb0 + 0.2, ruins.WALL_END + 0.12, S9_TOP - 0.1), (pb1, *head_top), (pb1 + 0.14, *head_top),   # nằm trên đỉnh đầu
                (pb1 + 0.3, KNOCK_X + 0.25, LOW_Z + 1.0), (pb1 + 0.6, KNOCK_X + 0.55, LOW_Z + 0.03),
                (pb1 + 0.75, KNOCK_X + 0.65, LOW_Z + 0.1), (pb1 + 0.9, KNOCK_X + 0.72, LOW_Z + 0.03)):
    at(pebble, t, x, z)
ry(pebble, pb0, 0)
ry(pebble, pb1 + 0.9, 540)
show(pebble, pb0 - 0.25, True)
show(pebble, pb1 + 1.2, False)
ry(lumo.arm, pb1 - 0.2, -10)
fc(lumo, pb1, "squint", 4)
squash(lumo, pb1 - HOLD, 1, 1)
squash(lumo, pb1, 1.06, 0.92)
squash(lumo, pb1 + 0.2, 1, 1)
ry(lumo.head, pb1, 10)
ears(lumo, pb1 - HOLD, 10)
ears(lumo, pb1 + 0.05, 28)
ears(lumo, EARS_DROOP, -48)                                     # cụp tai
look(lumo, EARS_DROOP + 0.3, 0.3, 0.8)                          # ngước nhìn mép tường
fc(lumo, EARS_DROOP + 0.3, "sad", 4)
ry(lumo.head, EARS_DROOP + 0.3, -8)
ry(lumo.tail, EARS_DROOP, -10)
# sang cú S10: la bàn đã về tay gần, ngang bụng (đổi ở điểm cắt)
SWAP2 = SHOT["S10"][0]
show(compF.root, SWAP2, False)
show(comp.root, SWAP2, True)
show(dust, SWAP2, False)
glow(comp, SWAP2, 0.7)
chold(lumo, comp_hold, SWAP2 - HOLD, -10, -8)
chold(lumo, comp_hold, SWAP2, -30, -40)
ry(far_hold, SWAP2, 0)

# ================================================================ S10: "Mình nghĩ bức tường không thích bị làm phiền."
m0, m1 = LUMO_LINE3
ry(lumo.head, m0 - 0.4, 0)
look(lumo, m0 - 0.4, 0.4, 0.0)
fc(lumo, m0 - 0.1, "sheepish")
talk(lumo, m0, m1, "frown")
ears(lumo, m0, -40)
ears(lumo, m1, -45)
for t in (m0 + 0.9, m1 - 0.4):                                  # nhún vai
    squash(lumo, t, 1, 1)
    squash(lumo, t + 0.12, 0.98, 1.04)
    squash(lumo, t + 0.3, 1, 1)
bl(lumo, m1 + 0.2)
# liếc la bàn: mũi sao vẫn chỉ dọc tường, tai nhổm lên (dẫn sang Cảnh 3)
chold(lumo, comp_hold, GLANCE - 0.4, -30, -40)
chold(lumo, comp_hold, GLANCE, -85, -80)
look(lumo, GLANCE, 0.8, -0.6)
ry(lumo.head, GLANCE, 10)
fc(lumo, GLANCE + 0.2, "eager", 10)
ears(lumo, GLANCE + 0.2, -20)
ears(lumo, GLANCE + 0.5, 8)
ry(lumo.tail, GLANCE + 0.2, 25)
beep(comp, GLANCE + 0.4, 0.72, 0.95)

# ================================================================ bướm bay khỏi phiến đá rêu
bf0, bf1 = BFLY_OFF
at(bfly.root, 0.0, *ruins.STONE_TOP)
scl(bfly.root, 0.0, 1, 1)
flap(bfly, 0.0, bf0, 0.9, 0.55)                                 # đậu: cánh dựng lên, khép mở chậm (như cuối Cảnh 1)
for t, x, z in ((bf0, *ruins.STONE_TOP), (bf0 + 0.3, -8.15, -0.95), (bf0 + 0.7, -8.5, -0.6), (bf0 + 1.1, -9.1, -0.2),
                (bf0 + 1.5, -9.7, 0.3), (bf1, -10.6, 0.9), (bf1 + 0.1, -12, 6.0)):
    at(bfly.root, t, x, z)
scl(bfly.root, bf0, -1, 1)
flap(bfly, bf0, bf1)

# ================================================================ chớp mắt, đuôi
for t in (13.1, 22.3, GLANCE + 0.8):
    bl(lumo, t)
loop(lumo.tail, STAND[1], LUMO_LINE1[0], 0.5, 20, 34)
loop(lumo.tail, TURN_BACK[1], LUMO_LINE2[1], 0.6, 16, 30)

# ================================================================ cú cận la bàn, tường ở hậu cảnh (S5, S7)
big.cur = "wonder"
fc(big, 0.0, "wonder", 8)
big.dir = -1
scl(big.root, 0.0, -1, 1)
look(big, 0.0, 0.8, -0.6)
ears(big, 0.0, 10)
ry(big.head, 0.0, 8)
chold(big, big_hold, 0.0, -60, -55)
ry(big.tail, 0.0, 20)
glow(bcomp, 0.0, 0.65)
i0, i1 = SHOT["S5"]
look(big, i0 + 1.7, -0.2, 0.9)                                  # nhìn theo mũi sao về phía mảng dây leo
ry(big.head, i0 + 1.7, -6)
fc(big, i0 + 1.7, "wonder", -6)
ears(big, i0 + 1.8, 18)
look(big, i1 - 0.4, 0.8, -0.6)
ry(big.head, i1 - 0.4, 8)
for t in INSERT_BEEPS:
    beep(bcomp, t, 0.65, 0.9)
jitter(bcomp.root, i0, i1, 0.006, 0.07)
# S7: Lumo đứng ở đầu tường, quay lại; mũi sao xoay theo, vẫn chỉ về phía bức tường
j0, j1 = SHOT["S7"]
key(big_scale, "location", j0 - HOLD, (IX + 0.7, -0.3, -1.26))
key(big_scale, "location", j0, (IX + 0.45, -0.3, -1.26))
look(big, j0, 0.8, -0.6)
fc(big, j0, "puzzled", 8)
facing(big, TURN_BACK[1], 1, TURN_BACK[1] - TURN_BACK[0])
look(big, TURN_BACK[1] + 0.1, 0.8, -0.6)
fc(big, TURN_BACK[1] + 0.1, "wonder", 8)
ears(big, TURN_BACK[1] + 0.1, 16)
look(big, TURN_BACK[1] + 0.8, -0.9, 0.4)                       # liếc ra sau lưng theo mũi sao
ry(big.head, TURN_BACK[1] + 0.8, -8)
look(big, j1 - 0.3, 0.8, -0.6)
for t in (TURN_BACK[1] + 0.2, TURN_BACK[1] + 1.1):
    beep(bcomp, t, 0.65, 0.9)
jitter(bcomp.root, j0, j1, 0.006, 0.07)

# ================================================================ mũi sao: rung rung rồi xoay phắt, sau đó luôn chỉ phù điêu
sn0, sn1 = NEEDLE_SNAP
bpy.context.scene.frame_set(fr(sn1))
vib = [(st1, SECONDS, 1.0)]
target_now = aim(comp, sn1, sn1, RELIEF)
spin = target_now - 360 * math.ceil((target_now - (REST - 400)) / 360)   # xoay phắt hơn một vòng, ngược chiều kim đồng hồ
for t, a in ((sn0, REST), (sn0 + 0.1, REST - 120), (sn0 + 0.2, REST - 300)):
    ry(comp.needle, t, a)
aim(comp, sn1, SECONDS, RELIEF,
    lambda t: (-16 if t < sn1 + 0.08 else 7 if t < sn1 + 0.16 else 0) + buzz(vib)(t), spin)   # vọt quá rồi về
aim(compF, FACE_WALL, SHOT["S10"][0] + 0.1, RELIEF, buzz(vib))
aim(bcomp, SHOT["S5"][0] - 0.1, SHOT["S7"][1] + 0.1, INS_TARGET, buzz([(0, SECONDS, 1.0)]))

# ================================================================ máy quay, render
CAMS = {"S1": (-8.15, -0.72, 3.4), "S2": (-8.74, -1.1, 0.85), "S3": (-8.22, -0.7, 1.6), "S4": (-8.32, -0.64, 0.95),
        "S5": (IX, 0.12, 2.8), "S6": (-8.55, -0.78, 2.3), "S7": (IX, 0.12, 2.8), "S8": (-8.75, -0.76, 1.9),
        "S9": CAMS_S9, "S10": (-8.6, -0.78, 2.3)}                               # tâm X, tâm Z, bề ngang khung (m); đáy khung chừa cho CC
cameras(SHOTS, CAMS)
finish(SECONDS, OUT_BLEND, (0.2, 1.2, 2.8, 4.6, 5.5, 6.3, 6.9, 8.0, 9.4, 10.4, 11.3, 11.6, 13.0, 14.6, 15.6, 16.4, 17.0, 17.6,
                            18.6, 20.5, 24.3, 25.8, 27.0, 29.5, 31.8, 34.4, 35.2, 35.9, 37.3, 38.8, 39.5, 41.5, 44.2))
