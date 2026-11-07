"""
EP000A Cảnh 3 (Khám phá đầu tiên): previz 2D cutout (03_CONTENT/PREVIZ_2D.md, bộ nhân vật pipeline/cutout.py).
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #3# và #3A#. Mốc thời gian và CC: timing.py; mọi
keyframe tính từ các mốc đó (cộng trừ vài phần mười giây cho nhịp lấy đà, giữ tư thế).
    pipeline/run.sh build -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene03
    pipeline/run.sh preview -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene03
    blender -b --factory-startup -P pipeline/cc.py -- <cảnh>/renders/scene03_preview.mp4 <cảnh>/timing.py <cảnh>/renders/scene03_preview_cc.mp4
Phế tích dùng chung với Cảnh 2 (../ruins.py): Lumo bắt đầu ở đầu tường X -8.75 quay mặt sang trái như cuối Cảnh 2,
đi dọc tường tới mảng dây leo che phù điêu đám mây (-12), ngã lăn ra thảm rêu (-12.7) trước cửa thấp (-13.25).
Vòm đá dựng riêng ở X 38–48: cửa thấp vào ở bên phải (46.9), bệ đỡ trống mặt la bàn ở PED_X, cánh cửa đá khắc mây cuối
vòm bên trái (CLOUD_DOOR); ô cửa trên trần, ánh sáng tản đều, không luồng sáng. Mũi sao bám phù điêu, rồi cửa thấp,
rồi cánh cửa khắc mây: aim() của cutout tính góc từng khung từ ma trận thế giới của la bàn. Hai cú cận la bàn có hậu cảnh
dựng riêng, Lumo phóng to: X = 20 (ngồi trên thảm rêu, phù điêu và cửa thấp phía sau), X = 30 (vòm đá, cánh cửa khắc mây).
"""
import math
import pathlib
import random
import sys

import bpy
from mathutils import Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.dont_write_bytecode = True                                  # không để __pycache__ cạnh timing.py
sys.path[:0] = [str(HERE), str(HERE.parent), str(ROOT / "pipeline")]   # timing.py của cảnh, ruins.py của tập, cutout
from cutout import *  # noqa: E402,F403  bộ cutout: keyframe, hình, mặt, nhân vật, máy quay, la bàn và hàm diễn la bàn
from timing import *  # noqa: E402,F403  FPS, SECONDS, SHOTS, mốc hành động, CC của cảnh
import ruins  # noqa: E402  phế tích dùng chung với Cảnh 2
from ruins import LOW_Z, RELIEF, swirl  # noqa: E402

OUT_BLEND = HERE / f"{HERE.name}.blend"
start(FPS)
SHOT = {name: (t0, t1) for name, t0, t1 in SHOTS}
HOLD = 1.0 / FPS
FACES["dizzy"] = ("closed", "o", -14)
random.seed(9)
CR = 0.065
DOOR_IN = (ruins.DOOR_X, LOW_Z + 0.5)                           # mục tiêu sau khi cửa thấp mở: vào trong cửa

R = ruins.build_ruins()

# ================================================================ vòm đá (X 38–48, sàn Z 0)
V0, V1, VH = 37.8, 48.2, 1.75                                   # mép vòm, chiều cao tường bên
PED_X, PED_H, PED_R = 43.0, 0.38, 0.22                          # bệ đỡ: trụ đá thấp ngang ngực Lumo
CLOUD_DOOR = (39.9, 0.85)                                       # tâm cánh cửa đá khắc mây cuối vòm
CD_W, CD_H = 1.3, 1.7
ENT_X = 46.0                                                    # cửa thấp vào vòm
VST, VST_D, VST_L = "#D8C6A6", "#BBA684", "#E6D7BB"
part("V_Back", None, [(rect(V0, -0.5, V1, 4.4), "#A89575")], 1.4)
vb = [(rect(V0, 0, V1, VH), VST_D)]
for row, (z0, z1) in enumerate(((0.0, 0.42), (0.42, 0.86), (0.86, 1.3), (1.3, VH))):
    off = 0.0 if row % 2 else 0.35
    x = V0 - off
    k = 0
    while x < V1:
        x1 = min(x + 0.7, V1)
        x0 = max(x, V0)
        vb.append((rrect(x1 - x0 - 0.035, z1 - z0 - 0.035, 0.035, (x0 + x1) / 2, (z0 + z1) / 2), VST if (k + row) % 2 else VST_L))
        x, k = x + 0.7, k + 1
for cx in (41.6, 45.0):                                         # phù điêu mặt la bàn trên tường bên: sao hoa gió
    vb += [(ell(0.26, 0.26, cx, 1.05), VST_D), (ell(0.22, 0.22, cx, 1.05), VST), (rose(0.19, cx, 1.05), VST_D),
           (ell(0.04, 0.04, cx, 1.05), VST)]
vb += [s for cx in (41.2, 44.3, 45.8) for s in cloud_parts(0.5, 0.26, cx, 0.5, VST_D)]
vb += [(ell(rx, 0.07, cx, 0.02), ruins.MOSS) for rx, cx in ((0.5, 38.6), (0.4, 41.0), (0.3, 44.6), (0.5, 47.4))]
part("V_Wall", None, vb, 1.3)
# trần vòm: dải cong phía trên, ô cửa tròn nhìn ra trời (ánh sáng tản đều, không luồng sáng)
ceil = [(rect(V0, VH, V1, 4.4), "#C8B593")]
ceil += [(rect(x - 0.06, VH, x + 0.06, 4.4), "#B3A07E") for x in (39.0, 40.4, 41.8, 43.2, 44.6, 46.0, 47.4)]
for cx in (40.9, 43.2, 45.5):
    ceil += [(ell(0.42, 0.16, cx, 2.05), "#9E8B6B"), (ell(0.36, 0.12, cx, 2.06), "#CFEAF7"), (ell(0.12, 0.05, cx + 0.12, 2.1), "#8CC65A")]
ceil += [(band([(x, VH + 0.02), (x + 0.05, VH - 0.3), (x - 0.02, VH - 0.55)], 0.025), "#5E9437") for x in (39.4, 42.1, 46.3)]
part("V_Ceiling", None, ceil, 1.25)
part("V_Floor", None, [(rect(V0, -3, V1, 0.0), "#CDBB98")] + [(rect(x, -0.32, x + 0.03, 0.0), "#B6A27E") for x in
                                                               [V0 + 0.55 * k for k in range(19)]]
     + [(ell(0.25, 0.03, x, -0.02), ruins.MOSS) for x in (38.9, 41.9, 44.0, 46.2)], 1.0)
# cửa thấp vào (bên phải): ô sáng ban ngày, vệt sáng trên sàn
ent = [(ENT_X - 0.35, 0.0), (ENT_X - 0.35, 0.77)] + [(ENT_X - 0.35 * math.cos(math.pi * k / 12), 0.77 + 0.35 * math.sin(math.pi * k / 12))
                                                    for k in range(13)] + [(ENT_X + 0.35, 0.0)]
part("V_Entrance", None, [(ent, "#F2E7B8"), (ell(0.18, 0.08, ENT_X - 0.05, 0.25), "#A5CF63")], 1.28)
part("V_EntLight", None, [([(ENT_X - 0.35, -0.02), (ENT_X + 0.35, -0.02), (ENT_X + 0.1, -0.3), (ENT_X - 0.75, -0.3)], "#E6D7AE")], 0.95)
# cánh cửa đá khắc mây cuối vòm (bên trái): khung vòm, hai cánh, mây khắc; lấp lánh khi Lumo tới gần
cdx, cdz = CLOUD_DOOR
arch = [(cdx - CD_W / 2, 0.0), (cdx - CD_W / 2, CD_H - CD_W / 2)] + \
    [(cdx - CD_W / 2 * math.cos(math.pi * k / 16), CD_H - CD_W / 2 + CD_W / 2 * math.sin(math.pi * k / 16)) for k in range(17)] + \
    [(cdx + CD_W / 2, 0.0)]
part("CD_Frame", None, [([(x * 1.0 + (0.12 if x > cdx else -0.12 if x < cdx else 0), z + (0.1 if z > 0.1 else 0)) for x, z in arch],
                         "#9E8B6B")], 1.27)
cd = [(arch, "#D9C9A8"), (rect(cdx - 0.012, 0.0, cdx + 0.012, CD_H), "#A8957A")]
for cx, cz, w in ((cdx - 0.3, 1.25, 0.42), (cdx + 0.28, 1.0, 0.44), (cdx - 0.28, 0.7, 0.44), (cdx + 0.3, 0.42, 0.4), (cdx - 0.3, 0.2, 0.36)):
    cd += cloud_parts(w, w * 0.55, cx, cz, "#C2AE88") + [(swirl(0.05, cx - w * 0.15, cz + 0.01, 0.014), "#A8957A"),
           (swirl(0.06, cx + w * 0.12, cz + 0.04, 0.014), "#A8957A")]
cd_door = part("CD_Door", None, cd, 1.26)
cd_glints = [part(f"CD_Glint{i}", None, [(star(0.07, 0, 0, 4, 0.3), "#FFE27A")], 1.2, (cx, cz)) for i, (cx, cz) in
             enumerate(((cdx - 0.42, 1.38), (cdx + 0.15, 1.1), (cdx - 0.12, 0.78), (cdx + 0.42, 0.5), (cdx - 0.38, 0.28),
                        (cdx + 0.1, 1.5)))]
cd_crack = part("CD_Crack", None, [(rect(-0.02, -CD_H / 2 + 0.03, 0.02, CD_H / 2 - 0.05), "#FFF4C8")], 1.255, (cdx, CD_H / 2))
# bệ đỡ trống: trụ đá thấp, mặt khắc hình la bàn (nhìn chếch từ trên), quanh thân khắc mây và sao hoa gió
PED, PED_D, PED_T = "#B3A891", "#857B67", "#C9C0AB"                # đá xám, sẫm hơn tường để nổi lên, không ra gốc cây
ped = [(rect(PED_X - PED_R, 0.0, PED_X + PED_R, PED_H), PED), (ell(PED_R, 0.06, PED_X, 0.0, 180, 360), PED),
       (rect(PED_X - PED_R, 0.0, PED_X - PED_R + 0.05, PED_H), "#A6895F"),
       (rose(0.07, PED_X, 0.19), PED_D), (ell(0.022, 0.022, PED_X, 0.19), PED)]
ped += cloud_parts(0.13, 0.07, PED_X - 0.12, 0.08, PED_D) + cloud_parts(0.13, 0.07, PED_X + 0.12, 0.29, PED_D)
ped += [(rrect(2 * PED_R + 0.06, 0.06, 0.015, PED_X, 0.03), PED_D), (rrect(2 * PED_R + 0.05, 0.05, 0.015, PED_X, PED_H - 0.02), PED_D),
        (ell(PED_R + 0.04, 0.05, PED_X, 0.02, 180, 360), "#7FB045"),
        (ell(PED_R, 0.065, PED_X, PED_H), PED_T), (ell(0.12, 0.035, PED_X, PED_H), PED_D),
        (ell(0.1, 0.028, PED_X, PED_H), "#B39A70"), (rose(0.09, PED_X, PED_H), PED_D)]
part("Pedestal", None, ped, 0.2)
# hai mép tường bên che khi máy đứng ở vòm
part("V_Ferns", None, [(leaf_pts(x, 0.06, 3.2, a), "#6FAE45") for x, a in ((38.4, 60), (38.6, 120), (47.7, 70), (47.9, 115))]
     + [(ell(0.025, 0.025, x, 0.12), col) for x, col in ((38.8, "#F7A8C8"), (47.2, WHITE))], -0.6)

# ================================================================ cú cận ở thảm rêu (X 20): phù điêu đã xoay, cửa thấp mở
IX, VX = 20.0, 30.0
part("I1_Sky", None, [(rect(IX - 2, -1, IX + 2, 1.2), ruins.SKY)], 1.6)
iw = [(rect(IX - 2, -1, IX + 2, 0.75), ruins.STONE_D)]
for row, (z0, z1, xs) in enumerate(((-1.0, -0.35, (17.9, 18.8, 19.7, 20.6, 21.5, 22.1)), (-0.35, 0.2, (18.1, 19.0, 19.95, 20.9, 22.1)),
                                    (0.2, 0.75, (18.0, 18.9, 19.8, 20.7, 21.6, 22.1)))):
    for x0, x1 in zip(xs, xs[1:]):
        iw.append((rrect(x1 - x0 - 0.06, z1 - z0 - 0.06, 0.06, (x0 + x1) / 2, (z0 + z1) / 2), ruins.STONE if (row + int(x0 * 2)) % 2 else ruins.STONE_L))
I_DOOR = (18.95, -0.95)
idw, idh = 0.95, 1.5
idoor = [(I_DOOR[0] - idw / 2, I_DOOR[1]), (I_DOOR[0] - idw / 2, I_DOOR[1] + idh - idw / 2)] + \
    [(I_DOOR[0] - idw / 2 * math.cos(math.pi * k / 12), I_DOOR[1] + idh - idw / 2 + idw / 2 * math.sin(math.pi * k / 12)) for k in range(13)] + \
    [(I_DOOR[0] + idw / 2, I_DOOR[1])]
iw += [(idoor, "#5E5040"), ([(I_DOOR[0] - 0.42, I_DOOR[1]), (I_DOOR[0] + 0.42, I_DOOR[1]), (I_DOOR[0] + 0.15, I_DOOR[1] + 0.55),
                             (I_DOOR[0] - 0.12, I_DOOR[1] + 0.55)], "#E8D7A6"),
       ([(x - I_DOOR[0] - idw / 2, z) for x, z in []] or [(I_DOOR[0] - idw / 2, I_DOOR[1]), (I_DOOR[0] - idw / 2 + 0.12, I_DOOR[1]),
                                                          (I_DOOR[0] - idw / 2 + 0.12, I_DOOR[1] + idh - 0.3),
                                                          (I_DOOR[0] - idw / 2, I_DOOR[1] + idh - 0.25)], ruins.STONE)]
I_RELIEF = (21.05, 0.25)
iw += [(ell(0.62, 0.48, *I_RELIEF), "#8E7F67")] + cloud_parts(1.1, 0.7, *I_RELIEF, "#D6C7AB", 25)
iw += [(turn(swirl(0.13, I_RELIEF[0] + dx, I_RELIEF[1] + dz, 0.03), 25, *I_RELIEF), ruins.STONE_D)
       for dx, dz in ((-0.27, 0.0), (0.1, 0.08), (0.36, -0.05))]
part("I1_Wall", None, iw, 1.2)
part("I1_Moss", None, [(rect(IX - 2, -1.0, IX + 2, -0.45), "#7FB045")]
     + [(ell(0.2, 0.08, IX - 1.8 + 0.42 * k, -0.45 + 0.015 * (k % 3)), "#7FB045") for k in range(10)], -0.9)   # thảm rêu che chân
I1_DOOR_T = (I_DOOR[0], I_DOOR[1] + 0.5)

# ================================================================ cú cận trong vòm (X 30): cánh cửa khắc mây ở hậu cảnh
part("I2_Back", None, [(rect(VX - 2, -1, VX + 2, 1.2), VST_D)]
     + [(rrect(0.66, 0.4, 0.04, VX - 1.7 + 0.7 * k + (0.35 if r % 2 else 0), -0.75 + 0.45 * r), VST if (k + r) % 2 else VST_L)
        for r in range(5) for k in range(6)], 1.3)
I_CD = (28.75, 0.15)
icw, ich = 1.0, 1.35
iarch = [(I_CD[0] - icw / 2, I_CD[1] - ich / 2), (I_CD[0] - icw / 2, I_CD[1] + ich / 2 - icw / 2)] + \
    [(I_CD[0] - icw / 2 * math.cos(math.pi * k / 16), I_CD[1] + ich / 2 - icw / 2 + icw / 2 * math.sin(math.pi * k / 16)) for k in range(17)] + \
    [(I_CD[0] + icw / 2, I_CD[1] - ich / 2)]
icd = [([(x + (0.08 if x > I_CD[0] else -0.08), z + 0.06) for x, z in iarch], "#9E8B6B"), (iarch, "#D9C9A8"),
       (rect(I_CD[0] - 0.01, I_CD[1] - ich / 2, I_CD[0] + 0.01, I_CD[1] + ich / 2), "#A8957A")]
for cx, cz, w in ((-0.22, 0.38, 0.34), (0.22, 0.15, 0.34), (-0.22, -0.12, 0.34), (0.22, -0.38, 0.32)):
    icd += cloud_parts(w, w * 0.55, I_CD[0] + cx, I_CD[1] + cz, "#C2AE88")
part("I2_Door", None, icd, 1.25)
part("I2_Floor", None, [(rect(VX - 2, -1.0, VX + 2, -0.55), "#CDBB98")], 1.2)
I2_DOOR_T = I_CD

# ================================================================ nhân vật, đạo cụ
lumo = build_lumo(-8.75, -0.32)
comp_hold, comp = build_holder(lumo, CR, "Compass")                # la bàn ở tay gần
far_hold, compF = build_holder(lumo, CR, "CompassFar", far=True)    # la bàn chuyền sang tay xa (vạch dây leo, ấn, kéo, đẩy)
ped_comp = build_compass("PedCompass", None, (PED_X, PED_H + 0.012), 0.19, CR * 1.2)   # la bàn ấn khớp vào mặt bệ
ped_comp.root.scale = (1.0, 1.0, 0.32)
BIG_S = 2.4
big_scale = node("BigLumo_Scale", None, (IX + 0.41, -1.27), -0.3)
big_scale.scale = (BIG_S, BIG_S, BIG_S)
big = build_lumo(0.0, 0.0)
big.root.parent = big_scale
big.root.location = (0.0, 0.0, 0.0)
big_hold, bcomp = build_holder(big, 0.13, "BigCompass")
pebble = part("Pebble", None, [(ell(0.03, 0.026), "#9E9384"), (ell(0.012, 0.009, -0.008, 0.008), "#C4BAAB")], -0.6)
moss_bits = [part(f"MossBit{i}", None, [(leaf_pts(0, 0, 1.6, 0), "#6FAE45" if i % 2 else "#86C04E")], -0.62) for i in range(6)]
eye_spark = [part(f"Lumo_EyeSpark{i}", lumo.head, [(star(s, 0, 0, 4, 0.3), WHITE)], -0.03, loc) for i, (loc, s) in
             enumerate((((0.1, 0.27), 0.03), ((0.065, 0.22), 0.018)))]   # ánh lấp lánh trắng trong tròng mắt
for ob in (pebble, *moss_bits, *eye_spark, *cd_glints, cd_crack, ped_comp.root, compF.root, R.relief_glow, R.glow, R.glint):
    show(ob, 0.0, False)
for c in (comp, compF, ped_comp, bcomp):
    show(c.glow, 0.0, False)

# ================================================================ trạng thái đầu cảnh (khớp cuối Cảnh 2)
lumo.dir = -1
scl(lumo.root, 0.0, -1, 1)
at(lumo.root, 0.0, -8.75, LOW_Z)
fc(lumo, 0.0, "eager", 10)
look(lumo, 0.0, 0.8, -0.6)
ears(lumo, 0.0, 8)
ry(lumo.head, 0.0, 10)
chold(lumo, comp_hold, 0.0, -75, -70)
ry(far_hold, 0.0, 80)
ry(lumo.tail, 0.0, 25)
show(comp.root, 0.0, True)
glow(comp, 0.0, 0.7)

# ================================================================ S1–S2: đi dọc bức tường, càng gần càng sáng, rung, kêu dày
STOP_X = -11.3
w0, w1 = WALK_WALL
pts = [-8.75, -9.1, -9.45, -9.8, -10.15, -10.48, -10.78, -11.03, -11.2, STOP_X]   # bước ngắn dần khi tới gần
for i, x in enumerate(pts):
    t = w0 + (w1 - w0) * (i / (len(pts) - 1)) ** 0.9
    at(lumo.root, t, x, LOW_Z + (0.035 if i % 2 else 0.0))
loop(lumo.tail, w0, w1, 0.55, 18, 34)
look(lumo, w0, 0.8, -0.5)
ry(lumo.head, w0 + 1.0, 4)
look(lumo, w0 + 1.6, 1.0, 0.1)                                  # ngẩng lên nhìn theo mũi sao về phía trước
look(lumo, w0 + 2.6, 0.8, -0.5)
look(lumo, BEEPS_DENSE[0], 1.0, 0.2)
fc(lumo, BEEPS_DENSE[0], "wonder")
ears(lumo, BEEPS_DENSE[0], 16)
look(lumo, BEEPS_DENSE[0] + 1.2, 0.8, -0.6)
ry(lumo.head, BEEPS_DENSE[0] + 1.2, 10)
look(lumo, w1, 1.0, 0.3)
ry(lumo.head, w1, -4)
for t in BEEPS_SPARSE:
    beep(comp, t, 0.7, 0.95)
dense = [BEEPS_DENSE[0] + d for d in (0.0, 0.55, 1.0, 1.35, 1.65, 1.88, 2.08, 2.25, 2.4)]
for i, t in enumerate(dense):                                   # sáng dần, kêu dày dần
    s0 = 0.75 + 0.4 * i / (len(dense) - 1)
    beep(comp, t, s0, s0 + 0.25)
VIB1, VIB2 = BEEPS_DENSE[0] - 0.8, BEEPS_DENSE[0] + 1.0          # các nấc rung mạnh dần khi tới gần
jitter(comp.root, 0.0, VIB1, 0.0025, 0.07)                      # rung khẽ
jitter(comp.root, VIB1, VIB2, 0.004, 0.06)
jitter(comp.root, VIB2, SWAP_FAR, 0.007, 0.05)                  # rung mạnh dần
chold(lumo, comp_hold, VIB2, -76, -70)

# ================================================================ S3: vạch dây leo, phù điêu ánh lên
# chuyền la bàn sang tay xa (để ngang bụng), tay gần vạch dây leo
show(comp.root, SWAP_FAR, False)
show(compF.root, SWAP_FAR, True)
glow(compF, SWAP_FAR, 1.15)
chold(lumo, comp_hold, SWAP_FAR - 0.15, -80, -78)
ry(far_hold, SWAP_FAR - 0.15, 78)
ry(lumo.arm_far, SWAP_FAR + 0.25, -45)
ry(far_hold, SWAP_FAR + 0.25, 45)
v0, v1 = PART_VINES
ry(lumo.arm, SWAP_FAR, -80)
ry(lumo.arm, v0, -125)                                          # với tay lên ngang tai
lean(lumo, v0, 8)
ry(lumo.arm, v0 + 0.35, -118)
ry(lumo.arm, v1, -55)                                           # gạt sang bên
lean(lumo, v1, 2)
for nd, a, sx in ((R.vines[0], 34, 0.5), (R.vines[1], -42, 0.5)):
    ry(nd, v0 + 0.1, 0)
    scl(nd, v0 + 0.1, 1, 1)
    ry(nd, v1, a)
    scl(nd, v1, sx, 1)
    ry(nd, v1 + 0.25, a * 0.9)
fc(lumo, v0, "eager")
look(lumo, v0, 1.0, 0.2)
twinkle(R.relief_glow, RELIEF_ON, PUSH[0], 1.0, 1.0, 0.3)       # các đường mây ánh lên
for i, t in enumerate(steps(RELIEF_ON, DOOR_OPEN[1], 0.3)):
    scl(R.relief_glow, t, 1.0 if i % 2 else 0.96, 1.0 if i % 2 else 0.96)
fc(lumo, RELIEF_ON + 0.1, "wonder")
ears(lumo, RELIEF_ON + 0.05, 22)
ears(lumo, RELIEF_ON + 0.3, 12)
squash(lumo, RELIEF_ON, 1, 1)
squash(lumo, RELIEF_ON + 0.12, 0.96, 1.05)
squash(lumo, RELIEF_ON + 0.3, 1, 1)
look(lumo, RELIEF_ON + 0.1, 1.0, 0.3)
ry(lumo.arm, RELIEF_ON + 0.4, 4)
for i, t in enumerate(steps(SWAP_FAR + 0.4, DOOR_OPEN[0], 0.32)):   # sát phù điêu: sáng mạnh, kêu dày
    beep(compF, t, 1.15, 1.4)
jitter(compF.root, SWAP_FAR + 0.3, TUMBLE[0], 0.007, 0.05)

# ================================================================ S4: thử ấn, thử kéo
P_X = -11.38
HAND_Z = LOW_Z + 0.4                                            # tay chạm đế phù điêu ngang ngực, dưới cằm
a_press = reach(lumo, P_X, LOW_Z, 6, (-11.6, HAND_Z))
p0, p1 = PRESS
at(lumo.root, p0 - 0.3, STOP_X, LOW_Z)
at(lumo.root, p0, P_X, LOW_Z)
ry(lumo.arm, p0, a_press + 10)
ry(lumo.arm, p0 + 0.25, a_press)                                # ấn vào
lean(lumo, p0 + 0.25, 6)
ry(lumo.arm, p0 + 0.45, a_press + 4)
ry(lumo.arm, p0 + 0.6, a_press)                                 # ấn thêm lần nữa
fc(lumo, p0, "eager")
look(lumo, p0, 1.0, 0.0)
ry(lumo.arm, p1, a_press)
n0, n1 = PRESS_NOTHING
ry(lumo.arm, n0 + 0.1, -10)
lean(lumo, n0 + 0.1, 0)
fc(lumo, n0, "puzzled")
ears(lumo, n0, -6)
for t in (n0 + 0.2,):
    squash(lumo, t, 1, 1)
    squash(lumo, t + 0.12, 0.98, 1.04)                          # nhún vai
    squash(lumo, t + 0.3, 1, 1)
look(lumo, n0 + 0.3, 0.5, -0.8)
look(lumo, n1, 1.0, 0.1)
k0, k1 = PULL
PULL_X = -11.45
a_grip = reach(lumo, PULL_X, LOW_Z, -2, (-11.62, HAND_Z))
at(lumo.root, k0 - 0.2, P_X, LOW_Z)
at(lumo.root, k0, PULL_X, LOW_Z)
ry(lumo.arm, k0, a_grip)
lean(lumo, k0, -2)
fc(lumo, k0 + 0.1, "squint")
ears(lumo, k0 + 0.1, -20)
for i, t in enumerate(steps(k0 + 0.3, k1, 0.25)):               # kéo giật giật
    lp, xp = (-14, PULL_X + 0.03) if i % 2 else (-6, PULL_X)
    lean(lumo, t, lp)
    ry(lumo.arm, t, reach(lumo, xp, LOW_Z, lp, (-11.62, HAND_Z)))   # tay vẫn bám mép phù điêu
    at(lumo.root, t, xp, LOW_Z)
m0, m1 = PULL_NOTHING
ry(lumo.arm, m0, -15)
lean(lumo, m0, 0)
at(lumo.root, m0, STOP_X, LOW_Z)
fc(lumo, m0, "puzzled")
ears(lumo, m0, -18)
look(lumo, m0 + 0.2, 1.0, 0.0)
ry(lumo.head, m0 + 0.2, 12)                                     # nghiêng đầu nhìn phù điêu

# ================================================================ S5: lấy đà đẩy, phù điêu xoay, ngã lăn ra thảm rêu, cửa thấp mở
u0, u1 = RUNUP
RUN_X = -10.85
walk(lumo.root, u0, u1, STOP_X, RUN_X, 2, 0.03, LOW_Z)         # lùi lại hai bước
ry(lumo.head, u0, 0)
fc(lumo, u0, "eager", 0)
ears(lumo, u0, -30)                                             # tai ép ra sau, quyết tâm
squash(lumo, u1 - 0.1, 1, 1)
squash(lumo, u1, 1.07, 0.9)                                     # khom người lấy đà
lean(lumo, u1, 10)
ry(lumo.arm, u1, -20)
pu0, pu1 = PUSH
CONTACT_X = -11.36
squash(lumo, pu0, 0.96, 1.04)
at(lumo.root, pu0, RUN_X, LOW_Z)
at(lumo.root, pu0 + 0.18, (RUN_X + CONTACT_X) / 2, LOW_Z + 0.05)
at(lumo.root, pu1, CONTACT_X, LOW_Z)
lean(lumo, pu1, 10)
ry(lumo.arm, pu0 + 0.15, -100)
ry(lumo.arm, pu1, reach(lumo, CONTACT_X, LOW_Z, 10, (-11.62, HAND_Z)))
fc(lumo, pu0, "shout")
squash(lumo, pu1, 1, 1)
# phù điêu đột nhiên xoay nhẹ
rt0, rt1 = RELIEF_TURN
ry(R.relief, rt0, 0)
ry(R.relief, rt1, 25)
ry(R.relief, rt1 + 0.08, 22)
ry(R.relief, rt1 + 0.16, 25)
# mất thăng bằng, lăn một vòng trên thảm rêu, ngồi phịch xuống
tm0, tm1 = TUMBLE
SIT_X, SIT_Z = -12.72, LOW_Z - 0.06
fc(lumo, tm0 + 0.05, "shock")
ears(lumo, tm0 + 0.05, 25)
at(lumo.root, tm0 + 0.2, -11.6, LOW_Z)
lean(lumo, tm0 + 0.2, 42)                                       # chúi tới
ry(lumo.arm, tm0 + 0.2, -140)
H_C = 0.42                                                      # tâm người cao 0.42 trên gốc: lăn quanh tâm
for k in range(13):
    u = k / 12
    t = tm0 + 0.3 + (tm1 - 0.25 - tm0 - 0.3) * u
    L = 42 + 318 * u
    cx, cz = -11.72 + (SIT_X + 0.1 + 11.72) * u, LOW_Z + 0.36 - 0.08 * math.sin(math.pi * u)
    at(lumo.root, t, cx + H_C * math.sin(math.radians(L)), cz - H_C * math.cos(math.radians(L)))
    lean(lumo, t, L)
loop(lumo.ear_near, tm0 + 0.3, tm1 - 0.25, 0.14, -60, 10)
loop(lumo.ear_far, tm0 + 0.35, tm1 - 0.25, 0.14, -60, 10)
fc(lumo, tm0 + 0.35, "squint")
at(lumo.root, tm1 - 0.1, SIT_X, SIT_Z + 0.04)
lean(lumo, tm1 - 0.1, 360 - 18)
at(lumo.root, tm1, SIT_X, SIT_Z)                                # ngồi phịch xuống thảm rêu: PHỊCH
lean(lumo, tm1, 360 - 10)
squash(lumo, tm1 - HOLD, 1, 1)
squash(lumo, tm1, 1.1, 0.88)
squash(lumo, tm1 + 0.2, 0.97, 1.03)
squash(lumo, tm1 + 0.4, 1, 1)
ry(lumo.arm, tm1, -30)
ears(lumo, tm1, -40)
ears(lumo, tm1 + 0.3, -10)
for i, ob in enumerate(moss_bits):                              # rêu tung lên
    fly_bit(ob, tm1, (SIT_X - 0.1 + 0.05 * i, LOW_Z + 0.1), (SIT_X - 0.45 + 0.17 * i, LOW_Z + 0.05), tm1 + 0.6, 200, 0.25)
look(lumo, tm1 + 0.4, 0.3, 0.2)
bl(lumo, tm1 + 0.5)
fc(lumo, tm1 + 0.6, "sheepish")
# cửa thấp mở ra bên cạnh phù điêu, ánh sáng ban ngày lọt vào; phù điêu tắt
d0, d1 = DOOR_OPEN
scl(R.door, d0, 1, 1)
scl(R.door, d1, 0.12, 1)                                        # cánh đá xoay vào trong (bản lề mép trái)
jitter(R.door, d0, d0 + 0.4, 0.004, 0.05)
fc(lumo, d0 + 0.1, "shock")
ears(lumo, d0 + 0.1, 20)
look(lumo, d0 + 0.1, 1.0, 0.2)
ry(lumo.head, d0 + 0.1, -4)
lean(lumo, d0 + 0.1, 360 - 4)
fc(lumo, d1, "wonder")
ears(lumo, d1 + 0.2, 12)
show(R.relief_glow, RELIEF_OFF, False)
bl(lumo, d1 + 0.9)

# ================================================================ S6: cận la bàn, ngồi trên thảm rêu: dịu đi, mũi sao quay vào cửa thấp
big.dir = -1
scl(big.root, 0.0, -1, 1)
big.cur = "wonder"
fc(big, 0.0, "wonder", 6)
look(big, 0.0, 0.8, -0.6)
ears(big, 0.0, 12)
ry(big.head, 0.0, 6)
chold(big, big_hold, 0.0, -60, -55)
ry(big.tail, 0.0, 10)
i0, i1 = SHOT["S6"]
glow(bcomp, i0 - HOLD, 1.25)
glow(bcomp, COMPASS_DIM, 1.25)
scl(bcomp.glow, COMPASS_DIM + 0.5, 0.65, 0.65)                  # dịu đi, còn le lói
for t in BEEPS_INSERT:
    beep(bcomp, t, 0.65, 0.9)
jitter(bcomp.root, i0, COMPASS_DIM + 0.4, 0.012, 0.05)
jitter(bcomp.root, COMPASS_DIM + 0.4, i1, 0.005, 0.07)
nt0, nt1 = NEEDLE_TO_DOOR
look(big, nt0, 0.8, -0.6)
look(big, nt1, 1.0, -0.2)                                       # mắt theo mũi sao về phía cửa thấp
ry(big.head, nt1, -2)
ears(big, nt1 + 0.1, 20)
fc(big, nt1 + 0.2, "eager", -2)
ears(big, nt1 + 0.4, 10)
look(big, i1 - 0.5, 0.9, -0.5)

# ================================================================ S7: "Mình tìm được rồi!", bước vào cửa thấp
# đổi la bàn về tay gần ở điểm cắt
c7 = SHOT["S7"][0]
show(compF.root, c7, False)
show(comp.root, c7, True)
glow(comp, c7, 0.7)
chold(lumo, comp_hold, c7 - HOLD, -30, -45)
chold(lumo, comp_hold, c7, -40, -30)
ry(far_hold, c7, 0)
g0, g1 = GET_UP
lean(lumo, c7 - HOLD, 360 - 4)
lean(lumo, c7, -4)                                              # cùng tư thế, góc về khoảng 0 (360 = 0)
at(lumo.root, g0, SIT_X, SIT_Z)
lean(lumo, g0, -4)
squash(lumo, g0, 1.06, 0.92)
at(lumo.root, g0 + 0.2, SIT_X - 0.05, LOW_Z + 0.12)             # bật dậy
lean(lumo, g0 + 0.2, 4)
squash(lumo, g0 + 0.2, 0.95, 1.06)
at(lumo.root, g1, SIT_X - 0.08, LOW_Z)
lean(lumo, g1, 0)
squash(lumo, g1, 1, 1)
fc(lumo, g0, "happy")
ears(lumo, g0 + 0.15, 22)
ears(lumo, g1, 10)
o0, o1 = LUMO_LINE1
fc(lumo, o0 - 0.05, "shout")
talk(lumo, o0, o1, "smile")
chold(lumo, comp_hold, o0, -70, -60)
chold(lumo, comp_hold, o0 + 0.3, -74, -66)                      # chìa la bàn ra trước, ngang ngực
chold(lumo, comp_hold, o1 + 0.1, -72, -66)
squash(lumo, o0 + 0.1, 1.06, 0.92)                              # lấy đà
squash(lumo, o0 + 0.25, 0.94, 1.08)
at(lumo.root, o0 + 0.1, SIT_X - 0.08, LOW_Z)
at(lumo.root, o0 + 0.45, SIT_X - 0.08, LOW_Z + 0.26)              # nhảy cẫng
at(lumo.root, o0 + 0.8, SIT_X - 0.08, LOW_Z)
squash(lumo, o0 + 0.8, 1.06, 0.93)
squash(lumo, o0 + 1.0, 1, 1)
ears(lumo, o0 + 0.4, 26)
ears(lumo, o0 + 0.9, 12)
loop(lumo.tail, g1, INTO_DOOR[1], 0.3, 25, 50)
fc(lumo, o1 + 0.05, "happy")
look(lumo, o1 + 0.2, 1.0, 0.0)
e0, e1 = INTO_DOOR
walk(lumo.root, e0, e1, SIT_X - 0.08, ruins.DOOR_X + 0.02, 3, 0.03, LOW_Z)
fc(lumo, e0, "eager")
ry(lumo.head, e0, 6)
squash(lumo, e1 - 0.3, 1, 1)
squash(lumo, e1, 0.97, 0.94)                                    # khom vào cửa thấp
glow(comp, c7 + 0.4, 0.7)
for t in (c7 + 0.6, c7 + 1.7, c7 + 2.8):
    beep(comp, t, 0.7, 0.95)
jitter(comp.root, c7, SHOT["S8"][0], 0.0025, 0.07)

# ================================================================ S8: vào vòm đá, bệ đỡ trống, khựng lại, cụp tai
c8 = SHOT["S8"][0]
STAND_X = PED_X + 0.36                                          # đứng sát bệ, bên phải, vừa tầm tay
at(lumo.root, c8 - HOLD, ruins.DOOR_X + 0.02, LOW_Z)
at(lumo.root, c8, ENT_X, 0.0)
squash(lumo, c8 - HOLD, 0.97, 0.94)
squash(lumo, c8, 1, 1)
en0, en1 = ENTER_VAULT
at(lumo.root, en0, ENT_X, 0.0)
walk(lumo.root, en0 + 0.1, en1, ENT_X, STAND_X, 6, 0.04, 0.0)
fc(lumo, c8, "eager")
look(lumo, c8, 1.0, -0.1)
ry(lumo.head, c8, 0)
chold(lumo, comp_hold, c8, -75, -70)
look(lumo, en0 + 0.8, 1.0, 0.4)                                 # nhìn quanh vòm
look(lumo, en0 + 1.5, 1.0, -0.5)                                # nhìn bệ đỡ
fc(lumo, en0 + 1.5, "eager", 6)
ry(lumo.head, en0 + 1.5, 6)
loop(lumo.tail, en0, en1, 0.4, 22, 40)
fc(lumo, SEE_EMPTY, "wonder", 12)
look(lumo, SEE_EMPTY, 0.8, -0.9)
ry(lumo.head, SEE_EMPTY, 8)
ry(lumo.tail, SEE_EMPTY, 30)
fc(lumo, EARS_DOWN1, "sad", 12)
ears(lumo, EARS_DOWN1 - 0.05, 8)
ears(lumo, EARS_DOWN1 + 0.25, -66)                              # cụp tai
squash(lumo, EARS_DOWN1, 1, 1)
squash(lumo, EARS_DOWN1 + 0.25, 1.04, 0.94)                     # thân xệ xuống
squash(lumo, PED_PRESS[0], 1, 1)
ry(lumo.tail, EARS_DOWN1 + 0.25, -30)
chold(lumo, comp_hold, EARS_DOWN1 + 0.25, -45, -30)
for t in (en0 + 0.4, en0 + 1.6):
    beep(comp, t, 0.7, 0.95)
jitter(comp.root, c8, PED_PRESS[0], 0.0025, 0.07)

# ================================================================ S9: ấn la bàn vào bệ; gõ bệ, chờ sỏi, thở phào, PLOP; nhìn bệ, nhìn la bàn
pp0, pp1 = PED_PRESS
a_ped = reach(lumo, STAND_X, 0.0, 6, (PED_X + 0.05, PED_H + 0.02))   # tay ấn chúc xuống, dưới cằm
at(lumo.root, pp0, STAND_X, 0.0)
at(lumo.root, pp0 + 0.3, STAND_X, 0.0)
fc(lumo, pp0, "eager", 14)
ears(lumo, pp0 - 0.2, -58)
ears(lumo, pp0 + 0.3, -20)
chold(lumo, comp_hold, pp0, -45, -30)
chold(lumo, comp_hold, pp0 + 0.35, a_ped, -20)
lean(lumo, pp0 + 0.35, 6)
ry(lumo.head, pp0 + 0.35, -8)                                  # ngửa đầu, mõm tránh khỏi tay
show(comp.root, pp0 + 0.4, False)
show(ped_comp.root, pp0 + 0.4, True)
glow(ped_comp, pp0 + 0.4, 0.7)
ry(lumo.arm, pp0 + 0.55, a_ped - 4)                            # ấn khớp vào
ry(lumo.arm, pp1, a_ped)
look(lumo, pp0 + 0.2, 0.7, -1.0)
no0, no1 = PED_NOTHING
look(lumo, no0, 0.4, 0.6)                                       # chờ, nhìn quanh: không có gì
look(lumo, no0 + 0.45, 1.0, 0.4)
look(lumo, no1, 0.7, -1.0)
fc(lumo, no0 + 0.3, "puzzled", 14)
ry(lumo.arm, no1, -10)
lean(lumo, no1, 6)
# gõ lên bệ: TOK. TOK. TOK.
a_knock = reach(lumo, STAND_X, 0.0, 6, (PED_X + 0.08, 0.22))      # mặt trước bệ, chỗ thân Lumo không che
for k in PED_KNOCKS:
    ry(lumo.arm, k - 0.18, a_knock - 32)                        # vung tay lên rồi gõ xuống
    ry(lumo.arm, k, a_knock)
    ry(lumo.arm, k + 0.12, a_knock - 12)
fc(lumo, PED_KNOCKS[0] - 0.2, "eager", 6)
# cụp tai, ngước nhìn trần, chờ hòn sỏi
wp0, wp1 = WAIT_PEBBLE
ry(lumo.arm, wp0, 0)
lean(lumo, wp0, 0)
ears(lumo, wp0, -10)
ears(lumo, wp0 + 0.2, -50)
ry(lumo.head, wp0 + 0.25, -16)
look(lumo, wp0 + 0.25, 0.3, 1.0)                                # ngước nhìn trần
fc(lumo, wp0 + 0.25, "worried", -16)
squash(lumo, wp0 + 0.2, 1.03, 0.96)                             # rụt cổ chờ
bl(lumo, wp0 + 1.0)
look(lumo, wp0 + 1.2, -0.3, 1.0)
look(lumo, wp1 - 0.2, 0.3, 1.0)
# không có gì: thở phào, hai tai dựng lên
s0, s1 = RELIEF_SIGH
squash(lumo, s0, 1.03, 0.96)
squash(lumo, s0 + 0.3, 0.97, 1.03)
squash(lumo, s1, 1, 1)
ry(lumo.head, s0 + 0.2, 4)
fc(lumo, s0 + 0.15, "happy", 4)
ears(lumo, s0 + 0.15, -20)
ears(lumo, s1, 14)                                              # hai tai dựng lên
look(lumo, s1, 0.5, 0.0)
# PLOP! hòn sỏi rơi trúng đỉnh đầu (đo đỉnh đầu thật ở khung PLOP), đầu giật ngửa lên chứ không gục xuống bệ
pr0, pr1 = PLOP_REACT
fc(lumo, PLOP, "squint", -10)
ry(lumo.head, PLOP - HOLD, 0)
ry(lumo.head, PLOP + 0.08, -10)
squash(lumo, PLOP, 1, 1)
squash(lumo, PLOP + 0.08, 1.07, 0.9)                            # sỏi chạm đầu trước, người mới co lại
squash(lumo, PLOP + 0.28, 1, 1)
bpy.context.scene.frame_set(fr(PLOP))
hp = lumo.head.matrix_world @ Vector((0.0, 0.0, 0.42))
head_top = (hp.x, hp.z)
show(pebble, PLOP - 0.4, True)
for t, x, z in ((PLOP - 0.4, head_top[0], 2.1), (PLOP, *head_top), (PLOP + 0.08, head_top[0], head_top[1] - 0.04),
                (PLOP + 0.23, head_top[0] + 0.22, 1.05), (PLOP + 0.53, head_top[0] + 0.48, 0.03), (PLOP + 0.68, head_top[0] + 0.58, 0.09),
                (PLOP + 0.83, head_top[0] + 0.66, 0.03)):
    at(pebble, t, x, z)
ry(pebble, PLOP + 0.83, 500)
show(pebble, PLOP + 1.4, False)
ears(lumo, PLOP - HOLD, 14)
ears(lumo, PLOP + 0.05, 30)
ears(lumo, PLOP + 0.25, -50)                                    # cụp tai, nhắm tịt mắt
ry(lumo.tail, PLOP + 0.25, -15)
ry(lumo.head, pr1, 6)
# nhấc la bàn lên, nhìn bệ trống, rồi nhìn la bàn trong tay, nghiêng đầu
l0, l1 = LIFT_COMPASS
chold(lumo, comp_hold, l0 - 0.3, 0, -10)
chold(lumo, comp_hold, l0, a_ped, -20)
lean(lumo, l0, 6)
fc(lumo, l0, "sad", 14)
show(ped_comp.root, l0 + 0.1, False)
show(comp.root, l0 + 0.1, True)
glow(comp, l0 + 0.1, 0.7)
chold(lumo, comp_hold, l1, -72, -60)
lean(lumo, l1, 0)
look(lumo, LOOK_PED, 0.8, -1.0)                                 # nhìn bệ trống
ry(lumo.head, LOOK_PED, 16)
look(lumo, LOOK_COMPASS, 0.6, -0.6)                             # nhìn la bàn trong tay
ry(lumo.head, LOOK_COMPASS, 8)
fc(lumo, LOOK_COMPASS, "puzzled", 8)
ry(lumo.head, HEAD_TILT, -14)                                   # nghiêng đầu
ears(lumo, HEAD_TILT, -8, -20)
jitter(comp.root, l0 + 0.2, SECONDS, 0.0025, 0.07)

# ================================================================ S10: quay lưng về phía cánh cửa, liếc la bàn
ta0, ta1 = TURN_AWAY
facing(lumo, ta1, 1, ta1 - ta0)
ry(lumo.head, ta1, 0)
ears(lumo, ta1, 4)
fc(lumo, ta1, "sad")
look(lumo, ta1, 0.6, 0.0)
look(lumo, GLANCE, 0.7, -0.8)                                   # liếc la bàn
ry(lumo.head, GLANCE, 10)
fc(lumo, GLANCE + 0.2, "puzzled", 10)
for t in (ta1 + 0.3, GLANCE + 0.5):
    beep(comp, t, 0.7, 0.95)

# ================================================================ S11: cận la bàn, cánh cửa ở hậu cảnh: xoay trái, xoay phải, xoay hai vòng
c11, e11 = SHOT["S11"]
key(big_scale, "location", c11 - HOLD, (IX + 0.41, -0.3, -1.27))
key(big_scale, "location", c11, (VX + 0.25, -0.3, -1.27))
scl(big.root, c11 - HOLD, -1, 1)
big.dir = 1
scl(big.root, c11, 1, 1)                                        # quay lưng về phía cánh cửa (bên trái)
glow(bcomp, c11, 0.7)
fc(big, c11, "puzzled", 8)
look(big, c11, 0.8, -0.6)
ears(big, c11, 4)
for t in (c11 + 0.5, c11 + 1.4):
    beep(bcomp, t, 0.7, 0.95)
look(big, c11 + 0.6, -1.0, 0.3)                                 # liếc ra sau lưng theo mũi sao
look(big, SPIN_LEFT - 0.3, 0.8, -0.6)
facing(big, SPIN_LEFT, -1, 0.12)                                # xoay phắt sang trái
fc(big, SPIN_LEFT + 0.05, "wonder", 8)
ears(big, SPIN_LEFT, 24)
ears(big, SPIN_LEFT + 0.25, 8)
look(big, SPIN_LEFT + 0.1, 0.8, -0.6)
facing(big, SPIN_RIGHT, 1, 0.12)                                # xoay phắt sang phải
fc(big, SPIN_RIGHT + 0.05, "shock", 8)
ears(big, SPIN_RIGHT, 24)
ears(big, SPIN_RIGHT + 0.25, 8)
look(big, SPIN_RIGHT + 0.1, 0.8, -0.6)
sp0, sp1 = SPINS
FLIPS = (sp0, sp0 + 0.25, sp0 + 1.05, sp0 + 1.3)                # một vòng = hai lần lật; ngừng nhìn la bàn rồi thêm vòng nữa
for i, t in enumerate(FLIPS):
    facing(big, t, -1 if i % 2 == 0 else 1, 0.09)
for g0 in (sp0, sp0 + 1.05):
    loop(big.ear_near, g0, g0 + 0.4, 0.2, -40, 30)
    loop(big.ear_far, g0 + 0.05, g0 + 0.4, 0.2, -40, 30)
    ears(big, g0 + 0.5, 10)
look(big, sp0 + 0.55, 0.8, -0.6)                                # giữa hai vòng: liếc la bàn, mũi sao vẫn chỉ cửa
fc(big, sp0, "wonder", 0)
fc(big, sp1 - 0.1, "dizzy", 0)
for t in (sp0 + 0.6, sp1 - 0.2):
    beep(bcomp, t, 0.7, 0.95)
jitter(bcomp.root, c11, e11, 0.005, 0.07)
# Lumo chính (ngoài khung) xoay theo cùng nhịp để khớp cú sau
facing(lumo, SPIN_LEFT, -1, 0.12)
facing(lumo, SPIN_RIGHT, 1, 0.12)
for i, t in enumerate(FLIPS):
    facing(lumo, t, -1 if i % 2 == 0 else 1, 0.09)

# ================================================================ S12: chóng mặt, loạng choạng, hai tai lắc lư
dz0, dz1 = DIZZY
fc(lumo, dz0 - 0.4, "dizzy", 0)
for i, t in enumerate(steps(dz0, dz1, 0.3)):
    lean(lumo, t, 10 if i % 2 else -10)
    at(lumo.root, t, STAND_X + (0.04 if i % 2 else -0.04), 0.0)
loop(lumo.ear_near, dz0, dz1, 0.3, -35, 25)
loop(lumo.ear_far, dz0 + 0.1, dz1, 0.3, -35, 25)
loop(lumo.head, dz0, dz1, 0.6, -14, 14)
lean(lumo, dz1 + 0.2, 0)
ry(lumo.head, dz1 + 0.2, 0)
ears(lumo, dz1 + 0.2, 6)
fc(lumo, dz1 - 0.2, "sheepish")
bl(lumo, dz1 + 0.1)

# ================================================================ S13: bước về phía cánh cửa, sáng thêm, rung mạnh dần; hình mây lấp lánh
DOOR_STOP = CLOUD_DOOR[0] + CD_W / 2 + 1.0                      # dừng cách cửa vài bước để còn chạy tới
td0, td1 = TO_DOOR
facing(lumo, td0, -1, 0.15)
look(lumo, td0, 0.8, -0.5)
fc(lumo, td0, "wonder", 6)
xs = [STAND_X, 42.75, 42.4, 42.05, 41.75, 41.48, DOOR_STOP]
for i, x in enumerate(xs):
    t = td0 + 0.15 + (td1 - td0 - 0.15) * i / (len(xs) - 1)
    at(lumo.root, t, x, 0.035 if i % 2 else 0.0)                # mỗi bước một nhịp
chold(lumo, comp_hold, td0, -72, -66)
bd0, bd1 = BEEPS_DOOR_DENSE
beeps = [BEEPS_DOOR[0], BEEPS_DOOR[0] + 0.9] + [bd0 + (bd1 - bd0) * u for u in (0.0, 0.3, 0.52, 0.7, 0.85, 1.0)]
for i, t in enumerate(beeps):
    s0 = 0.7 + 0.45 * i / (len(beeps) - 1)
    beep(comp, t, s0, s0 + 0.25)
jitter(comp.root, td0, BEEPS_DOOR[1], 0.003, 0.06)
jitter(comp.root, BEEPS_DOOR[1], td1, 0.006, 0.05)
jitter(comp.root, td1, STOW[0], 0.008, 0.05)
for i, ob in enumerate(cd_glints):
    twinkle(ob, DOOR_SPARKLE + 0.12 * i, RUN_PUSH[0], 1.3, 0.5, 0.25 + 0.03 * i)
look(lumo, DOOR_SPARKLE, 1.0, 0.4)
ears(lumo, DOOR_SPARKLE, 18)
loop(lumo.tail, td0, td1, 0.45, 20, 36)

# ================================================================ S14: "Khoan đã…", mắt sáng lên, "Cậu dẫn tới…", cất la bàn, đẩy cửa
k0, k1 = LUMO_LINE2
fc(lumo, k0 - 0.1, "puzzled", 8)
look(lumo, k0 - 0.1, 0.7, -0.7)                                 # nói với la bàn
ry(lumo.head, k0, 8)
chold(lumo, comp_hold, k0, -60, -55)
glow(comp, k0 - 0.1, 0.85)                                      # quầng thu nhỏ lúc nói, không che miệng
talk(lumo, k0, k0 + 0.7, "o")                                   # "Khoan đã…"
ry(lumo.head, k0 + 0.8, 6)
talk(lumo, k0 + 1.1, k1, "frown")                               # "cậu không dẫn tới kho báu."
ears(lumo, k0 + 1.1, -10)
eo0, eo1 = EYES_SHINE
look(lumo, eo0, 1.0, 0.3)                                       # nhìn cánh cửa lấp lánh
ry(lumo.head, eo0, -2)
fc(lumo, eo0 + 0.3, "wonder", -2)
ears(lumo, eo0 + 0.3, 20)
for ob in eye_spark:
    twinkle(ob, eo0 + 0.35, eo1 + 0.6, 1.4, 0.7, 0.18)
    show(ob, eo1 + 0.6, False)
q0, q1 = LUMO_LINE3
fc(lumo, q0 - 0.05, "eager", 0)
talk(lumo, q0, q0 + 1.6, "smile")                               # "Cậu dẫn tới những thứ…"
talk(lumo, q0 + 1.9, q1, "smile")                               # "…kỳ lạ!"
look(lumo, q0, 0.7, -0.6)
look(lumo, q0 + 1.7, 1.0, 0.3)
chold(lumo, comp_hold, q0 + 1.8, -62, -56)                      # chìa la bàn về phía cánh cửa, ngang ngực
at(lumo.root, q0 + 1.9, DOOR_STOP, 0.0)
at(lumo.root, q0 + 2.1, DOOR_STOP, 0.06)
at(lumo.root, q1, DOOR_STOP, 0.0)
fc(lumo, q1, "happy")
ears(lumo, q1, 14)
loop(lumo.tail, q0, STOW[0], 0.3, 25, 50)
# nhét la bàn vào túi da, chạy tới đẩy cánh cửa
st0, st1 = STOW
chold(lumo, comp_hold, st0, -72, -66)
chold(lumo, comp_hold, st0 + 0.35, -15, -20)
look(lumo, st0, 0.4, -0.9)
show(comp.root, st1 - 0.1, False)                               # vào túi da
chold(lumo, comp_hold, st1, -5, -10)
rp0, rp1 = RUN_PUSH
PUSH_X = CLOUD_DOOR[0] + CD_W / 2 + 0.2
fc(lumo, rp0, "shout")
ears(lumo, rp0, -25)
RUN_END = rp0 + 0.7
walk(lumo.root, rp0, RUN_END, DOOR_STOP, PUSH_X, 3, 0.06, 0.0)    # chạy ba bước
lean(lumo, rp0 + 0.2, 14)
lean(lumo, RUN_END, 10)
ry(lumo.head, RUN_END, -6)                                   # mõm ngẩng khỏi tay
a_door = reach(lumo, PUSH_X, 0.0, 10, (CLOUD_DOOR[0] + CD_W / 2 - 0.04, 0.3))
chold(lumo, comp_hold, rp0 + 0.3, -40, -40)
chold(lumo, comp_hold, RUN_END, a_door, a_door + 4)
jitter(cd_door, RUN_END, RUN_END + 0.3, 0.006, 0.05)               # cánh cửa nhúc nhích dưới tay
show(cd_crack, RUN_END + 0.1, True)                             # cánh cửa hé một khe sáng
scl(cd_crack, RUN_END + 0.1, 0.3, 1)
scl(cd_crack, SECONDS, 2.5, 1)

# ================================================================ mũi sao: phù điêu → cửa thấp → cánh cửa khắc mây
vib_soft = buzz([(0, VIB1, 0.8), (VIB1, VIB2, 1.6), (VIB2, TUMBLE[0], 3.0), (TUMBLE[0], SECONDS, 1.0)])
door_t = glide(RELIEF, DOOR_IN, *NEEDLE_TO_DOOR)
prev = aim(comp, 0.0, SWAP_FAR + 0.1, RELIEF, vib_soft)
prev = aim(compF, SWAP_FAR - 0.1, c7 + 0.1, door_t, vib_soft, prev)
aim(comp, c7 - 0.1, SHOT["S8"][0] - HOLD, DOOR_IN, vib_soft, prev)
inside = CLOUD_DOOR
prev = aim(comp, SHOT["S8"][0], PED_PRESS[0] + 0.45, inside, vib_soft)
aim(ped_comp, PED_PRESS[0] + 0.3, LIFT_COMPASS[0] + 0.2, inside, vib_soft)
vib_door = buzz([(0, BEEPS_DOOR[1], 1.0), (BEEPS_DOOR[1], TO_DOOR[1], 2.0), (TO_DOOR[1], SECONDS, 3.0)])
aim(comp, LIFT_COMPASS[0], STOW[1], inside, vib_door)
aim(bcomp, SHOT["S6"][0] - 0.1, SHOT["S6"][1] + 0.1, glide(I_RELIEF, I1_DOOR_T, *NEEDLE_TO_DOOR),
    buzz([(0, COMPASS_DIM + 0.4, 3.0), (COMPASS_DIM + 0.4, SECONDS, 1.0)]))
aim(bcomp, SHOT["S11"][0] - 0.1, SHOT["S11"][1] + 0.1, I2_DOOR_T, buzz([(0, SECONDS, 1.0)]))

# ================================================================ máy quay, render
CAMS = {"S1": (-9.55, -0.5, 3.2), "S2": (-10.3, -0.72, 1.9), "S3": (-11.6, -0.6, 2.0), "S4": (-11.6, -0.68, 1.8),
        "S5": (-12.1, -0.62, 2.8), "S6": (IX, 0.12, 2.8), "S7": (-12.95, -0.66, 2.1), "S8": (42.75, 1.45, 7.6),
        "S9": (43.25, 0.64, 2.0), "S10": (41.7, 0.82, 4.6), "S11": (VX, 0.12, 2.8), "S12": (43.3, 0.62, 2.0),
        "S13": (41.65, 0.8, 3.8), "S14": (40.75, 0.78, 2.8)}     # tâm X, tâm Z, bề ngang khung (m); đáy khung chừa cho CC
cameras(SHOTS, CAMS)
for name, keys in (("S1", ((SHOT["S1"][0], -9.55), (SHOT["S1"][1], -10.15))),
                   ("S2", ((SHOT["S2"][0], -10.25), (WALK_WALL[1], -11.45), (SHOT["S2"][1], -11.5)))):
    cam = bpy.data.objects[f"Cam_{name}"]
    cx, cz, w = CAMS[name]
    for t, x in keys:                                           # máy lia theo Lumo
        key(cam, "location", t, (x, -10.0, cz))
cam = bpy.data.objects["Cam_S8"]                                # toàn vòm (cửa vào, bệ, cánh cửa khắc mây), rồi đẩy vào bệ
for t, (cx, cz, w) in ((VAULT_PUSH, CAMS["S8"]), (SEE_EMPTY + 0.4, (43.35, 0.9, 4.2))):
    key(cam, "location", t, (cx, -10.0, cz))
    key(cam.data, "ortho_scale", t, w)
finish(SECONDS, OUT_BLEND, (0.3, 2.0, 4.4, 5.8, 7.4, 8.6, 10.8, 12.9, 15.9, 16.8, 17.5, 18.4, 19.5, 22.5, 23.9, 25.0, 27.0, 28.9,
                            30.5, 32.0, 33.5, 35.8, 38.0, 39.5, 41.0, 42.2, 44.4, 45.6, 47.6, 50.0, 51.4, 53.0, 54.6, 57.5,
                            61.0, 62.8, 65.5, 68.2, 70.5, 73.0, 74.5))
