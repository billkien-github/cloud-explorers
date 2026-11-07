"""
EP000A Cảnh 5 (Tiếng gọi): previz 2D cutout (03_CONTENT/PREVIZ_2D.md, bộ nhân vật pipeline/cutout.py).
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #5#. Mốc thời gian và CC: timing.py; mọi
keyframe tính từ các mốc đó (cộng trừ vài phần mười giây cho nhịp lấy đà, giữ tư thế).
    pipeline/run.sh build -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene05
    pipeline/run.sh preview -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene05
    blender -b --factory-startup -P pipeline/cc.py -- <cảnh>/renders/scene05_preview.mp4 <cảnh>/timing.py <cảnh>/renders/scene05_preview_cc.mp4
Bố cục (X, mét; Z = 0 là mặt đỉnh đồi): chân đồi là bãi cỏ Z -1.0, sườn cỏ thoải lên tới đỉnh ở X -3.3; đỉnh đồi phẳng tới
mép bên kia X 1.6 (EDGE); tảng đá giữa đỉnh ở -0.7; dốc lá khô từ mép xuống thảm cỏ Z -0.9 ở X 4.0; lối mòn tách ra từ
X 1.2, thoai thoải xuống tới thảm cỏ ở 6.6, nằm trên một vai đồi phía sau dốc lá. Trời, mặt trời, biển mây và hòn đảo
ở chân trời là một bộ (SkyRig) đi theo máy quay của từng cú: vật ở rất xa không trôi khi máy lia, nên hòn đảo luôn ở đúng
hướng mũi sao chỉ. Cận la bàn (S1, S5) dựng ở X = 40 và 50, cận bản đồ (S10) ở X = 20, góc nhìn lối mòn (S13) ở X = 60,
khung đen cuối cảnh ở X = 90.
Hòn đảo có Wonder Hub (đài thiên văn dáng Hub_House ở previz 2D Cảnh 2 tập 01) và nhịp lóe: build_hub_island(),
glow_flash() của cutout, dùng chung với post-credit (scene06).
"""
import math
import pathlib
import random
import sys

import bpy

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.dont_write_bytecode = True                                  # không để __pycache__ cạnh timing.py
sys.path[:0] = [str(HERE), str(ROOT / "pipeline")]
from cutout import *  # noqa: E402,F403  bộ cutout: keyframe, hình, mặt, nhân vật, la bàn, chim, bản đồ, máy quay
from timing import *  # noqa: E402,F403  FPS, SECONDS, SHOTS, mốc hành động, CC của cảnh

OUT_BLEND = HERE / f"{HERE.name}.blend"
start(FPS)
SHOT = {name: (t0, t1) for name, t0, t1 in SHOTS}
HOLD = 1.0 / FPS                                                # một khung hình: key giữ đặt sớm hơn đúng một khung
FACES["awe"] = ("wide", "smile", -6)                            # mắt to, miệng cười nhẹ, nhướng mày: say mê, nói nhỏ
random.seed(5)


def line_z(pts, x):
    """Độ cao của đường gấp khúc pts (X tăng dần) tại x."""
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


# ================================================================ màu hoàng hôn (sunset_hill_hero.png, wonder_hub_island_hero.png)
GRASS, GRASS_D, GRASS_L, SHOULDER = "#A9CB61", "#8FB650", "#BCD878", "#B9D47F"
PATH_C, PATH_D = "#E4C28E", "#C9A472"
LEAF_COLS = ("#C97B3C", "#E09A52", "#B5642E", "#D98A45")
FUR, CREAM, CAPE = "#FD8A2B", "#FEECCF", "#FC6640"

# ================================================================ địa hình
EDGE, LOW, MEADOW = 1.6, -0.9, -1.0
HILL_L = [(-6.6, -1.0), (-6.3, -0.99), (-6.0, -0.95), (-5.7, -0.86), (-4.1, -0.17), (-3.8, -0.06), (-3.55, -0.01), (-3.3, 0.0)]
SLOPE = [(EDGE, 0.0), (1.68, -0.01), (1.78, -0.035), (1.9, -0.08), (2.05, -0.15), (3.5, -0.8), (3.65, -0.86), (3.8, -0.89),
         (4.0, LOW)]                                            # dốc lá khô thoải khoảng 24°, y như con dốc ở Cảnh 1
PATH = [(0.8, 0.0), (1.3, 0.0), (2.0, -0.05), (3.0, -0.2), (4.2, -0.42), (5.4, -0.66), (6.6, LOW)]   # lối mòn khoảng 11°
GROUND = [(-16.0, MEADOW)] + HILL_L + SLOPE + [(16.0, LOW)]


def ground_z(x):
    return line_z(GROUND, x)


def path_z(x):
    return line_z(PATH, x)


ROCK_X, ROCK_TOP = -0.7, 0.265                                  # tảng đá giữa đỉnh đồi, mặt trên ngang hông Lumo
MAP_SPOT = (-0.8, ROCK_TOP + 0.01)                              # chỗ tấm bản đồ nằm trên tảng đá
X_FOOT, X_ROCK_L, X_ROCK_R, X_EDGE, X_BACK = -6.3, -1.12, -0.46, 1.5, 1.3

# ================================================================ trời, mặt trời, biển mây, hòn đảo: một bộ đi theo máy quay
# Gốc của bộ là chân hòn đảo trên đường chân trời. Lớp trong bộ, từ sau ra trước: trời, mặt trời, mây cao, đảo,
# quầng lóe, đài thiên văn, sương chân đảo, hai tầng mây che đảo (tách ra ở S6), biển mây.
rig = node("SkyRig", None, (0.0, 0.0), 5.0)
part("Sky", rig, [(rect(-25, 2.2, 25, 14), "#A79BDB"), (rect(-25, 1.35, 25, 2.2), "#C7A3D6"), (rect(-25, 0.75, 25, 1.35), "#E8AAC6"),
                  (rect(-25, 0.3, 25, 0.75), "#F7BCA6"), (rect(-25, -14, 25, 0.3), "#FBD0A0")], 1.0)
SUN = (-7.0, 0.32)
part("Sun", rig, [(ell(0.75, 0.75, *SUN), "#FDDDA0"), (ell(0.5, 0.5, *SUN), "#FEE9B8"), (ell(0.3, 0.3, *SUN), "#FFF6DA")], 0.9)
part("HighClouds", rig, [(ell(rx, rz, cx, cz), col) for rx, rz, cx, cz, col in (
    (0.9, 0.07, -3.2, 1.75, "#F4B5BE"), (0.6, 0.05, -2.4, 1.85, "#F8C7B8"), (1.1, 0.08, 2.4, 2.05, "#F4B5BE"),
    (0.7, 0.05, 3.3, 1.95, "#F8C7B8"), (0.8, 0.06, -6.5, 1.5, "#F4B5BE"), (1.0, 0.07, 6.2, 1.6, "#F4B5BE"),
    (0.5, 0.04, 0.6, 2.4, "#F8C7B8"), (0.9, 0.06, -0.8, 2.7, "#F4B5BE"))], 0.8)
ISL_S = 0.6                                                     # đảo ở rất xa: thu nhỏ (post-credit còn xa hơn, 0.45)
ISLAND_C = (0.05 * ISL_S, 0.06 + 0.5 * ISL_S)                   # tâm hòn đảo trong bộ: chỗ mũi sao chỉ tới
island = node("IslandGroup", rig, (0.0, 0.06), 0.5)              # nhô khỏi mép biển mây một chút
island.scale = (ISL_S, 1.0, ISL_S)
hub = build_hub_island(island, "Island")                        # đảo và đài thiên văn (Wonder Hub), quầng lóe xanh ngọc
part("IslandMist", island, [(ell(0.32, 0.045, -0.45, 0.07), "#FBE6EE"), (ell(0.28, 0.04, 0.5, 0.05), "#FBE6EE"),
                         (ell(0.2, 0.035, 0.05, 0.11), "#FDF0F2")], -0.1)
bank_l = node("CloudBankL", rig, (-0.42, 0.0), 0.3)
bank_r = node("CloudBankR", rig, (0.5, 0.0), 0.28)
part("CloudBankL_Shape", bank_l, [(ell(0.6, 0.4, 0.0, 0.36), "#F6D3E0"), (ell(0.45, 0.36, -0.32, 0.5), "#F9DDE5"),
                                  (ell(0.42, 0.34, 0.22, 0.66), "#FBE4E3"), (ell(0.32, 0.26, -0.05, 0.9), "#FCE9E2"),
                                  (ell(0.55, 0.12, 0.0, 0.12), "#E8C0D6")])
part("CloudBankR_Shape", bank_r, [(ell(0.62, 0.42, 0.0, 0.38), "#F6D3E0"), (ell(0.46, 0.38, 0.3, 0.55), "#F9DDE5"),
                                  (ell(0.44, 0.36, -0.25, 0.7), "#FBE4E3"), (ell(0.34, 0.28, 0.08, 0.95), "#FCE9E2"),
                                  (ell(0.58, 0.12, 0.0, 0.12), "#E8C0D6")])
sea = [(rect(-25, -14, 25, 0.0), "#EFC9DE")]
for i in range(92):
    x = -25 + 0.55 * i
    sea += [(ell(0.5, 0.11, x, 0.02 + 0.03 * (i % 3)), "#F4D3E3"), (ell(0.28, 0.06, x + 0.12, 0.07 + 0.03 * (i % 3)), "#FBE2E2")]
    sea += [(ell(0.55, 0.12, x + 0.25, -0.38 - 0.04 * (i % 2)), "#EAC1DA"), (ell(0.6, 0.14, x, -0.85), "#E6BBD6")]
part("CloudSea", rig, sea, 0.0)

# ================================================================ đồi: nền trước, vai đồi có lối mòn phía sau, lá khô, cỏ
ground = part("Ground", None, [(GROUND + [(16, -8), (-16, -8)], GRASS),
                               (band([(x, ground_z(x) - 0.03) for x in [-16 + 0.25 * k for k in range(129)]], 0.05), GRASS_L)], 2.0)
part("Shoulder", None, [([(0.8, 0.0)] + PATH[1:] + [(16, LOW), (16, -8), (0.8, -8)], SHOULDER)], 2.3)
dense = [(0.8 + 0.1 * k, path_z(0.8 + 0.1 * k)) for k in range(59)]
part("Path", None, [(band(dense, 0.1), PATH_C), (band([(x, z - 0.045) for x, z in dense], 0.014), PATH_D)]
     + [(ell(0.018, 0.01, x, path_z(x) + 0.005), PATH_D) for x in (2.4, 3.3, 4.6, 5.7)], 2.25)
part("PathStart", None, [(band([(0.55, 0.0), (EDGE + 0.05, 0.0)], 0.07), PATH_C)], 1.97)   # lối mòn bắt đầu trên đỉnh đồi
litter = [(SLOPE[1:-1] + [(x, z - 0.26) for x, z in reversed(SLOPE[1:-1])], "#CC8A4A")]   # lớp lá khô phủ kín sườn dốc
for i in range(66):
    lx = 1.75 + (i % 22) * 0.105
    litter.append((leaf_pts(lx, ground_z(lx) - 0.03 - 0.08 * (i // 22) + random.uniform(-0.02, 0.02), 1.5, random.uniform(-50, 50)),
                   LEAF_COLS[i % 4]))
litter += [(leaf_pts(x, z, 1.4, a), LEAF_COLS[k % 4]) for k, (x, z, a) in enumerate(((1.35, 0.01, 20), (1.5, -0.01, -30),
                                                                                      (4.3, LOW - 0.02, 10), (4.7, LOW - 0.03, -40)))]
part("SlopeLeaves", None, litter, 1.95)
tufts = []
for gx in (-7.2, -6.8, -5.9, -5.2, -4.6, -3.9, -3.0, -2.4, -1.7, -0.1, 0.4, 1.0, 4.4, 5.0, 5.8, 6.5, 7.3):
    gz = ground_z(gx) - 0.02
    tufts += [([(gx - 0.03, gz), (gx + 0.03, gz), (gx + 0.005, gz + 0.08)], GRASS_D),
              ([(gx + 0.01, gz), (gx + 0.05, gz), (gx + 0.06, gz + 0.06)], GRASS_D)]
flowers = [(ell(0.022, 0.022, fx, ground_z(fx) - fz), col) for fx, fz, col in (
    (-7.0, 0.05, "#F7A8C8"), (-5.5, 0.04, WHITE), (-2.7, 0.04, "#B79BE8"), (-1.9, 0.05, WHITE), (0.2, 0.05, "#F7A8C8"),
    (0.75, 0.04, WHITE), (4.5, 0.05, "#F7A8C8"), (4.9, 0.06, WHITE), (5.5, 0.05, "#B79BE8"), (6.2, 0.05, "#F7A8C8"))]
flowers += [(ell(0.02, 0.02, fx, path_z(fx) + 0.07), col) for fx, col in ((2.7, WHITE), (3.6, "#F7A8C8"), (4.9, WHITE))]
part("Tufts", None, tufts + flowers, 1.9)
part("FootBushes", None, [(ell(0.32, 0.22, -7.4, -0.9), "#8FB650"), (ell(0.24, 0.17, -7.1, -0.86), "#A3C760"),
                          (ell(0.07, 0.06, -7.3, -0.75), "#F2B3CB")], 1.8)
wind_tufts = []                                                  # cỏ quanh tảng đá rạp xuống khi gió thổi tạt
for k, gx in enumerate((-1.9, -1.45, -0.3, 0.15, 0.6, 1.1)):
    wind_tufts.append(part(f"WindTuft{k}", None, [([(-0.035, 0.0), (0.035, 0.0), (0.0, 0.11)], GRASS_D),
                                                  ([(0.0, 0.0), (0.05, 0.0), (0.04, 0.08)], GRASS_D)], 1.85, (gx, -0.01)))

# --- tảng đá giữa đỉnh đồi (sunset_hill_hero.png: tảng đá phẳng có rêu)
part("Rock", None, [([(-1.15, 0.0), (-1.17, 0.08), (-1.12, 0.18), (-1.0, 0.245), (-0.7, ROCK_TOP + 0.02), (-0.4, 0.25),
                      (-0.27, 0.18), (-0.24, 0.08), (-0.27, 0.0)], "#B5A89B"),
                    (ell(0.41, 0.055, ROCK_X - 0.01, ROCK_TOP - 0.01), "#CEC2B5"),
                    ([(-0.5, 0.05), (-0.27, 0.04), (-0.25, 0.15), (-0.36, 0.2)], "#A3968A"),
                    (ell(0.12, 0.03, -1.0, 0.21), "#93B451"), (ell(0.08, 0.025, -0.42, 0.22), "#93B451"),
                    (ell(0.06, 0.035, -1.25, 0.02), "#A79A8D"), (ell(0.045, 0.03, -0.17, 0.015), "#A79A8D")], 0.6)
map_rock = node("MapOnRock", None, MAP_SPOT, 0.55)               # tấm bản đồ nằm trên mặt tảng đá
part("MapOnRock_Shape", map_rock, map_big())
scl(map_rock, 0.0, 0.3, 0.13)

# --- gió: vệt gió, lá bay; chiếc lá trượt dốc
streaks = [part(f"Wind{i}", None, [(band(curve((-0.35, 0.0), (0.0, 0.05), (0.35, 0.0), 12), 0.014), "#FFF8F4")], -0.9)
           for i in range(7)]
gust_leaves = [part(f"GustLeaf{i}", None, [(leaf_pts(0, 0, 1.8, 0), LEAF_COLS[i % 4])], -0.7) for i in range(4)]
SLIDE_LEAF = [(leaf_pts(0, 0, 4.2, 0), "#F6C445"), (band([(-0.13, 0.0), (0.13, 0.0)], 0.008), "#B5642E")]   # vàng sáng, nổi trên lớp lá
slide_leaf = part("SlideLeaf", None, SLIDE_LEAF, 1.6, (1.74, 0.012))

# ================================================================ cận (dựng riêng, phóng to)
PAW = [(rrect(0.13, 0.3, 0.06, 0.0, -0.14), FUR), (ell(0.075, 0.06, 0, 0), FUR), (ell(0.045, 0.03, 0, 0.01), CREAM)]


def compass_insert(name, cx):
    """La bàn to trong hai bàn tay Lumo (Lumo nhìn xuống la bàn), tâm ở (cx - 0.28, 0.3)."""
    c = build_compass(name, None, (cx - 0.28, 0.3), 0.5, 0.3)
    for side in (-1, 1):
        paw = node(f"{name}_Paw{side}", None, (cx - 0.28 + side * 0.31, 0.12), 0.45)
        part(f"{name}_PawShape{side}", paw, PAW)
        paw.rotation_euler = (0, math.radians(-side * 25), 0)
    part(f"{name}_Body", None, [(ell(0.5, 0.25, cx - 0.35, -0.32), CREAM), (rect(cx - 0.8, -0.6, cx - 0.62, -0.1), CAPE)], 0.7)
    return c


# --- S1 (X = 40): ngọn đồi chắn tầm nhìn sau la bàn
part("Ins1_Hill", None, [([(39.0, -0.4), (39.0, -0.05), (39.6, 0.08), (40.1, 0.25), (40.4, 0.38), (40.55, 0.42), (41.0, 0.43),
                           (41.0, -0.4)], "#9DC45A"),
                         (band([(39.0, -0.07), (39.6, 0.06), (40.1, 0.23), (40.4, 0.36), (40.55, 0.4), (41.0, 0.41)], 0.03), GRASS_L)]
     + [([(x - 0.02, z), (x + 0.02, z), (x, z + 0.06)], GRASS_D) for x, z in ((40.25, 0.31), (40.5, 0.41), (40.75, 0.42))], 1.0)
ins1 = compass_insert("Ins1_Compass", 40.0)
# --- S5 (X = 50): đỉnh đồi, biển mây và chân trời sau la bàn
part("Ins5_Grass", None, [(rect(49.0, -0.5, 51.0, 0.03), GRASS), (band([(49.0, 0.01), (51.0, 0.01)], 0.03), GRASS_L)]
     + [([(x - 0.02, 0.02), (x + 0.02, 0.02), (x, 0.08)], GRASS_D) for x in (50.2, 50.45, 50.7)], 1.0)
ins5 = compass_insert("Ins5_Compass", 50.0)

# --- S10 (X = 20): cận bản đồ Lumo cầm trước ngực, nhìn từ trên xuống
IX = 20.0
part("Insert_Ground", None, [(rect(IX - 1.0, -0.6, IX + 1.0, 0.6), GRASS)]
     + [([(IX + x - 0.02, z), (IX + x + 0.02, z), (IX + x, z + 0.05)], GRASS_D) for x, z in ((-0.55, 0.3), (0.5, 0.1), (-0.4, -0.2),
                                                                                     (0.55, 0.45), (-0.6, -0.4))]
     + [(leaf_pts(IX + x, z, 2.0, a), LEAF_COLS[k % 4]) for k, (x, z, a) in enumerate(((-0.5, 0.05, 30), (0.52, -0.3, -20)))], 1.0)
part("Insert_Belly", None, [(ell(0.38, 0.16, IX, -0.56), CREAM), (rect(IX - 0.75, -0.6, IX - 0.42, -0.36), CAPE),
                            (rect(IX + 0.42, -0.6, IX + 0.75, -0.36), CAPE)], 0.5)
insert_hold = node("Insert_Hold", None, (IX, 0.03), 0.3)
insert_map = node("Insert_Map", insert_hold, (0.0, 0.0), 0.0)
part("Insert_MapShape", insert_map, map_big())
ipaws = []
for side in (-1, 1):
    paw = node(f"Insert_Paw{side}", insert_hold, (side * 0.33, -0.27), -0.05)
    part(f"Insert_PawShape{side}", paw, PAW)
    ipaws.append(paw)

# --- S13 (X = 60): góc nhìn của Lumo từ mép đồi (sunset_hill_hero.png): dốc lá khô bên trái xuống thảm cỏ, chiếc lá vàng
# nằm ở chân dốc; lối mòn thoai thoải uốn xuống bên phải, hướng về phía hòn đảo
PX = 60.0
pov = [(rect(PX - 1.9, -0.8, PX + 1.9, 0.3), GRASS), (rect(PX - 1.9, -0.06, PX + 1.9, 0.3), GRASS_L),
       ([(PX - 1.9, -0.66), (PX - 0.2, -0.66), (PX - 0.62, -0.04), (PX - 1.55, -0.04)], "#CC8A4A")]
for i in range(40):                                             # lá khô phủ kín dốc
    u, v = (i % 8) / 7, (i // 8) / 4
    x = PX - 1.85 + 1.6 * u * (1 - 0.25 * v) + 0.35 * v
    pov.append((leaf_pts(x, -0.62 + 0.55 * v + random.uniform(-0.02, 0.02), 2.6 - 1.2 * v, random.uniform(-60, 60)), LEAF_COLS[i % 4]))
pov += [(leaf_pts(PX - 1.05, -0.0, 4.2 * 0.7, 10), "#F6C445")]   # chiếc lá vừa trượt, nằm ở chân dốc
for pts, th in (([(PX + 0.35, -0.8), (PX + 0.28, -0.55), (PX + 0.42, -0.4)], 0.2),
                ([(PX + 0.42, -0.4), (PX + 0.7, -0.27), (PX + 0.95, -0.17)], 0.14),
                ([(PX + 0.95, -0.17), (PX + 1.3, -0.06), (PX + 1.5, 0.0), (PX + 1.9, 0.08)], 0.08)):
    pov.append((band(pts, th), PATH_C))
pov += [(ell(0.025, 0.025, PX + x, z), col) for x, z, col in ((0.12, -0.5, "#F7A8C8"), (0.6, -0.42, WHITE), (0.68, -0.15, "#B79BE8"),
                                                              (1.1, -0.2, "#F7A8C8"), (1.2, 0.02, WHITE), (1.7, -0.02, "#F7A8C8"))]
pov += [([(PX + x - 0.025, z), (PX + x + 0.025, z), (PX + x, z + 0.07)], GRASS_D) for x, z in ((-0.1, -0.5), (0.05, -0.3), (0.9, -0.35),
                                                                                         (1.45, -0.12), (-1.3, 0.05), (0.3, 0.1))]
part("Pov_Ground", None, pov, 1.0)
part("Pov_Edge", None, [(rect(PX - 1.9, -0.9, PX + 1.9, -0.64), GRASS_D)]
     + [([(PX + x - 0.03, -0.645), (PX + x + 0.03, -0.645), (PX + x + 0.005, -0.56)], GRASS_D) for x in (-1.6, -0.9, -0.3, 0.6, 1.2, 1.7)],
     0.9)                                                       # mép đỉnh đồi ngay trước mắt Lumo

# --- S18 (X = 90): khung đen
part("Black", None, [(rect(87, -3, 93, 3), "#000000")], 0.0)

# ================================================================ Lumo và đồ trong tay
lumo = build_lumo(X_FOOT, -0.32, split_legs=True, cape_pivot=True)   # chân tách mảnh để nhấc chân ở mép dốc, áo choàng bay
near_hold = palm(lumo, "Lumo_NearHold")                         # bàn tay gần: la bàn, rồi bản đồ
far_hold = palm(lumo, "Lumo_FarHold", True, -0.004)             # bàn tay xa: bản đồ lúc leo đồi
comp = build_compass("Lumo_Compass", near_hold, (0.03, 0.0), -0.006, 0.065, flash=True)   # lóe theo đài thiên văn
map_far = node("Lumo_MapFar", far_hold, (0.03, 0.05), -0.002)
part("Lumo_MapFarShape", map_far, map_card())
map_near = node("Lumo_MapNear", near_hold, (0.035, 0.07), -0.002)
part("Lumo_MapNearShape", map_near, map_card())
bag_glow = part("Lumo_BagGlow", lumo.root, [(ell(0.07, 0.03), "#FFE27A"), (ell(0.045, 0.014), "#FFFBE0")]
                + [(band([(dx * 0.4, 0.01), (dx, 0.09)], 0.012), "#FFE27A") for dx in (-0.07, -0.025, 0.025, 0.07)],
                -0.013, (0.1, 0.236))                           # ánh la bàn lọt qua mép nắp túi da
bird = build_bird(-1.6, 1.2, 0.5)


def arms(t, near=None, far=None):
    """Xoay tay (bỏ trống là để yên tay đó); đồ trong tay xoay ngược lại để luôn đứng thẳng theo thân."""
    chold(lumo, near_hold, t, near, far, far_hold, None)


def legs(t, near, far=0.0):
    ry(lumo.leg_near, t, near)
    ry(lumo.leg_far, t, far)


def stride(t0, t1, period=0.3, amp=22):
    """Hai chân đánh qua lại theo bước."""
    for i, t in enumerate(steps(t0, t1, period / 2)):
        a = amp if i % 2 else -amp
        legs(t, a, -a)
    legs(t1 + 0.06, 0, 0)


def walk_on(t0, t1, x0, x1, n, hop, zf):
    """Đi trên mặt đất cong zf(x) từ x0 tới x1 trong n bước."""
    for i in range(n + 1):
        t, x = t0 + (t1 - t0) * i / n, x0 + (x1 - x0) * i / n
        at(lumo.root, t, x, zf(x) + (hop if i % 2 else 0.0))


for ob in (hub.flash, hub.tint, comp.flash, comp.bright, bag_glow, map_near, slide_leaf, *streaks, *gust_leaves):
    show(ob, 0.0, False)
for ob in (map_far, map_rock, comp.root):
    show(ob, 0.0, ob is not map_rock)
show(comp.flash, 0.0, False)
show(comp.bright, 0.0, False)
show(bird.root, 0.0, False)

# ================================================================ S1–S3: la bàn chỉ qua ngọn đồi, leo lên đỉnh
lumo.cur = "eager"
at(lumo.root, 0.0, X_FOOT, ground_z(X_FOOT))
fc(lumo, 0.0, "eager", 12)
ry(lumo.head, 0.0, 12)
look(lumo, 0.0, 0.6, -0.9)                                      # nhìn la bàn trong tay
arms(0.0, -75, -45)
ears(lumo, 0.0, 4)
ry(lumo.tail, 0.0, 20)
twinkle(comp.glow, 0.0, COMPASS_STOW[1], 0.8, 0.62, 0.45)       # le lói suốt: hòn đảo ở xa, không rung, không kêu
loop(lumo.tail, 0.0, CLIMB[0], 0.7, 16, 30)
bl(lumo, 1.2)
c0, c1 = COMPASS_LOWER
arms(c0, -75, -45)
arms(c1, -28, -30)                                              # hạ la bàn xuống ngang bụng
ry(lumo.head, c1, 0)
h0, h1 = LOOK_HILL
fc(lumo, h0, "eager", -8)
look(lumo, h0, 0.8, 0.7)                                        # ngẩng nhìn đỉnh đồi
ry(lumo.head, h1, -10)
ears(lumo, h0, 4)
ears(lumo, h0 + 0.15, 14)
ears(lumo, h1, 6)
squash(lumo, h0, 1, 1)
squash(lumo, h0 + 0.15, 1.04, 0.95)
squash(lumo, h1, 1, 1)
# leo lên sườn cỏ thoải, mắt nhìn phía trước
k0, k1 = CLIMB
walk_on(k0, k1, X_FOOT, -3.3, 8, 0.05, ground_z)
stride(k0, k1, 0.25, 26)
lean(lumo, k0, 0)
lean(lumo, k0 + 0.2, 10)                                        # chồm lên dốc
lean(lumo, k1 - 0.1, 10)
lean(lumo, k1 + 0.15, 0)
ry(lumo.head, k0, -10)
ry(lumo.head, k0 + 0.2, -4)
fc(lumo, k0, "eager", 6)
look(lumo, k0, 0.9, 0.4)
loop(lumo.tail, k0, TOP_WALK[1], 0.4, 20, 38)
loop(lumo.arm, k0, k1, 0.25, -40, -16)                          # tay đánh theo bước, la bàn và bản đồ vẫn trong tay
for i, t in enumerate(steps(k0, k1, 0.125)):
    ry(near_hold, t, 16 if i % 2 else 40)
loop(lumo.arm_far, k0 + 0.12, k1, 0.25, -40, -16)
for i, t in enumerate(steps(k0 + 0.12, k1, 0.125)):
    ry(far_hold, t, 16 if i % 2 else 40)
arms(k1, -28, -30)
w0, w1 = TOP_WALK
walk(lumo.root, w0, w1, -3.3, X_ROCK_L, 8, 0.035)
stride(w0, w1, 0.32, 20)
fc(lumo, w0 + 0.1, "eager")
look(lumo, w0 + 0.1, 0.9, 0.1)
ry(lumo.head, w0 + 0.1, 0)
bl(lumo, 6.9)
# dừng lại, nhìn ra biển mây
v0, v1 = VIEW_LOOK
fc(lumo, v0, "wonder", -6)
look(lumo, v0, 0.9, 0.35)
ry(lumo.head, v0, 0)
ry(lumo.head, v0 + 0.3, -8)
ears(lumo, v0, 6)
ears(lumo, v0 + 0.15, 16)
ears(lumo, v0 + 0.35, 8)
lean(lumo, v0, 0)
lean(lumo, v0 + 0.3, -4)
bl(lumo, v1 - 0.3)
loop(lumo.tail, w1, MAP_DOWN[0], 0.6, 18, 34)

# ================================================================ S4: đặt bản đồ lên tảng đá, hai tay nâng la bàn
m0, m1 = MAP_DOWN
PUT_LEAN = 22
a_put = reach(lumo, X_ROCK_L, 0.0, PUT_LEAN, MAP_SPOT, (-0.01, 0.46))
fc(lumo, m0, "eager", PUT_LEAN)
look(lumo, m0, 0.8, -0.9)                                       # nhìn chỗ đặt
ry(lumo.head, m0, -8)
ry(lumo.head, m0 + 0.3, 6)
lean(lumo, m0, -4)
lean(lumo, m0 + 0.3, PUT_LEAN)
arms(m0, -28, -30)
arms(m0 + 0.3, -20, a_put)
show(map_far, m0 + 0.35, False)                                 # buông tay: bản đồ nằm lại trên tảng đá
show(map_rock, m0 + 0.35, True)
scl(map_rock, m0 + 0.35, 0.3, 0.2)
scl(map_rock, m0 + 0.45, 0.3, 0.13)
lean(lumo, m1, 0)
arms(m1, -28, -20)
ry(lumo.head, m1, 0)
u0, u1 = COMPASS_UP
arms(u0, -28, -20)
arms(u1, -78, -62)                                              # hai tay nâng la bàn ngang ngực: tay xa đỡ dưới vỏ
fc(lumo, u0 + 0.1, "eager", 10)
look(lumo, u0 + 0.1, 0.5, -0.7)
ry(lumo.head, u1, 10)
ears(lumo, u0, 6)
ears(lumo, u1, 12)
fc(lumo, LOOK_HORIZON, "eager", -4)
look(lumo, LOOK_HORIZON, 1.0, 0.25)                             # nhìn theo mũi sao ra chân trời
ry(lumo.head, LOOK_HORIZON, -4)
bl(lumo, LOOK_HORIZON + 0.8)
ry(lumo.tail, u1, 26)

# ================================================================ S6: gió thổi tạt, mây tách, hòn đảo dần hiện, lóe lần 1
g0, g1 = GUST
for i, ob in enumerate(streaks):                                # vệt gió lướt từ phía chân trời về phía Lumo
    ts = g0 + 0.18 * i
    z = 0.2 + 0.22 * ((i * 3) % 7)
    show(ob, ts, True)
    at(ob, ts, 2.6, z)
    at(ob, ts + 0.55, -2.6, z + 0.06)
    show(ob, ts + 0.56, False)
for i, ob in enumerate(gust_leaves):
    ts = g0 + 0.25 + 0.3 * i
    fly_bit(ob, ts, (2.5, 0.5 + 0.18 * i), (-2.4, 0.3 + 0.1 * i), ts + 0.9, 540, 0.15)
for k, ob in enumerate(wind_tufts):                             # cỏ rạp về phía Lumo
    ry(ob, g0 + 0.1 * k / 3, 0)
    loop(ob, g0 + 0.15 + 0.03 * k, g1 - 0.1, 0.22, -28, -12)
    ry(ob, g1 + 0.1, 0)
fc(lumo, g0 + 0.1, "squint", 10)
ry(lumo.head, g0, 10)
ry(lumo.head, g0 + 0.2, 4)
for ob in (lumo.ear_near, lumo.ear_far):                        # tai bị gió thổi ngả ra sau
    loop(ob, g0 + 0.05, g1 - 0.1, 0.16, -38, -26)
ears(lumo, g1 + 0.05, 4)
ry(lumo.cape_pivot, g0, 0)
loop(lumo.cape_pivot, g0 + 0.05, g1, 0.14, 24, 38)              # áo choàng bay ngược ra sau
ry(lumo.cape_pivot, g1 + 0.2, 0)
loop(lumo.tail, g0, g1, 0.14, 40, 60)
lean(lumo, g0, 0)
lean(lumo, g0 + 0.2, 6)                                         # chồm vào gió
for i, t in enumerate(steps(g0 + 0.1, g1 - 0.2, 0.12)):         # bản đồ trên tảng đá phập phồng mép
    scl(map_rock, t, 0.3, 0.16 if i % 2 else 0.12)
scl(map_rock, g1, 0.3, 0.13)
p0, p1 = CLOUD_PART                                             # hai tầng mây tách ra hai bên, hòn đảo hiện dần
for ob, x0, dx in ((bank_l, -0.42, -1.55), (bank_r, 0.5, 1.6)):
    at(ob, p0, x0, 0.0)
    at(ob, p0 + (p1 - p0) * 0.4, x0 + dx * 0.25, -0.02)
    at(ob, p1, x0 + dx, -0.05)
l0, l1 = LUMO_LEAN
fc(lumo, l0, "wonder", 10)
look(lumo, l0, 1.0, 0.35)                                       # nhìn hòn đảo đang hiện ra
lean(lumo, g1, 6)
lean(lumo, l1, 9)
ry(lumo.head, l0, 4)
ry(lumo.head, l1, -6)
ears(lumo, l0, 4)
ears(lumo, l1, 12)
arms(l0, -78, -62)
arms(l1, -84, -66)
loop(lumo.tail, g1 + 0.1, LUMO_LINE1[0], 0.6, 20, 34)
bl(lumo, 18.4)
glow_flash(hub.flash, HUB_FLASH1, lit=hub.tint)                 # đài thiên văn lóe xanh ngọc
compass_flash(comp, HUB_FLASH1)                                 # đúng nhịp đó la bàn lóe theo (chỉ lóe: còn xa)
r0, r1 = LUMO_REACT
ears(lumo, r0, 12)
ears(lumo, r0 + 0.12, 24)                                       # tai bật dựng
ears(lumo, r1, 10)
squash(lumo, r0, 1, 1)
squash(lumo, r0 + 0.12, 0.96, 1.05)
squash(lumo, r1, 1, 1)
fc(lumo, r0, "wonder", 2)
look(lumo, r0 + 0.3, 0.6, -0.5)                                 # liếc xuống la bàn vừa lóe
look(lumo, r1 + 0.4, 1.0, 0.35)                                 # rồi lại nhìn hòn đảo
lean(lumo, r1, 6)

# ================================================================ S7: "Một nơi chưa ai khám phá…", "Được rồi, bạn la bàn."
a0, a1 = LUMO_LINE1
fc(lumo, a0 - 0.1, "awe", 2)
look(lumo, a0 - 0.1, 1.0, 0.35)
ry(lumo.head, a0, -4)
talk(lumo, a0, a0 + 0.95, "smile")                              # "Một nơi…" (nhỏ giọng)
talk(lumo, a0 + 1.15, a1, "smile")                              # "…chưa ai khám phá…"
ry(lumo.head, a1, -8)
bl(lumo, a1 - 0.5)
lean(lumo, a0, 6)
lean(lumo, a1, 2)
b0, b1 = LUMO_LINE2
look(lumo, LOOK_COMPASS, 0.5, -0.9)                             # cúi nhìn la bàn trong tay
ry(lumo.head, LOOK_COMPASS, 12)
fc(lumo, LOOK_COMPASS, "awe", 14)
talk(lumo, b0, b1, "smile")
for t, a in ((b0, 12), (b0 + 0.3, 18), (b0 + 0.55, 10)):        # gật nhẹ ở "Được rồi"
    ry(lumo.head, t, a)
ears(lumo, b0, 8)
ears(lumo, b1, 4)
arms(b0, -84, -66)
arms(b1, -76, -60)

# ================================================================ S8: câu hô lần 3, cất la bàn, kéo dây túi, lao đi
q0, q1 = LUMO_POSE
CHEST, PUSH = -72, -80                                          # như câu hô ở Cảnh 1: la bàn ngang ngực, đẩy tới ở câu hô
ears(lumo, q0, -30)                                             # tai cụp hẳn lấy đà
ears(lumo, q0 + 0.15, 14)                                       # bật dựng thẳng hai tai
ears(lumo, q1, 0)
arms(q0, -76, -60)
arms(q0 + 0.25, CHEST, -6)                                      # chìa la bàn thẳng ra trước ngang ngực, tay kia buông
ry(lumo.head, q0, 12)
ry(lumo.head, q0 + 0.2, -6)
ry(lumo.head, q1, 0)
lean(lumo, q0, 2)
lean(lumo, q0 + 0.25, -6)
squash(lumo, q0, 1, 1)
squash(lumo, q0 + 0.12, 1.08, 0.92)
squash(lumo, q0 + 0.25, 0.95, 1.06)
squash(lumo, q1, 1, 1)
fc(lumo, q0 + 0.15, "eager")
look(lumo, q0 + 0.15, 1.0, 0.3)                                 # mắt về phía hòn đảo
s0, s1 = LUMO_LINE3
fc(lumo, s0 - 0.05, "shout")
talk(lumo, s0, s0 + 0.8, "smile")                               # "Điều kỳ lạ…"
talk(lumo, s0 + 1.0, s1, "smile")                               # "…ngay phía trước!"
arms(s0 + 0.9, CHEST)
arms(s0 + 1.1, PUSH)                                            # đẩy la bàn tới thêm ở "ngay phía trước"
lean(lumo, s0 + 0.9, -6)
lean(lumo, s0 + 1.15, 3)
ry(lumo.head, s0 + 0.9, 0)
ry(lumo.head, s0 + 1.15, -8)
loop(lumo.tail, q1, s1, 0.4, 24, 44)
bl(lumo, s1 + 0.05)
t0, t1 = COMPASS_STOW
fc(lumo, t0, "happy", 10)
look(lumo, t0, 0.4, -0.9)                                       # liếc xuống túi
ry(lumo.head, t0 + 0.2, 10)
arms(t0, PUSH)
arms(t0 + 0.3, -18)                                             # tay đưa xuống túi ở hông
lean(lumo, t0, 3)
lean(lumo, t1, 0)
show(comp.root, t0 + 0.32, False)                               # la bàn vào túi da
k0, k1 = STRAP_TUG
arms(k0, -20)
arms(k0 + 0.15, -10)                                            # kéo dây túi cho ngay
arms(k1, -18)
key(lumo.bag, "location", k0, (0.0, lumo.bag.location.y, 0.0))
key(lumo.bag, "location", k0 + 0.15, (0.0, lumo.bag.location.y, -0.015))
key(lumo.bag, "location", k1, (0.0, lumo.bag.location.y, 0.0))
squash(lumo, k0, 1, 1)
squash(lumo, k0 + 0.15, 1.02, 0.97)
squash(lumo, k1, 1, 1)
d0, d1 = DASH
fc(lumo, d0, "eager", -6)
look(lumo, d0, 1.0, 0.2)
ry(lumo.head, d0, -4)
squash(lumo, d0, 1, 1)
squash(lumo, d0 + 0.1, 1.07, 0.9)                               # lấy đà
lean(lumo, d0, 0)
lean(lumo, d0 + 0.1, -10)
lean(lumo, d0 + 0.2, 18)                                        # lao đi
squash(lumo, d0 + 0.2, 0.96, 1.04)
squash(lumo, d0 + 0.3, 1, 1)
ears(lumo, d0 + 0.1, 0)
ears(lumo, d0 + 0.25, -32)
walk(lumo.root, d0 + 0.15, d1, X_ROCK_L, 1.9, 4, 0.06)
stride(d0 + 0.15, d1, 0.15, 34)
arms(d0 + 0.15, -18, -6)
loop(lumo.arm, d0 + 0.15, d1, 0.15, -50, 10)
loop(lumo.arm_far, d0 + 0.2, d1, 0.15, 10, -50)
ry(lumo.tail, d0 + 0.2, 55)

# ================================================================ S9: bản đồ nằm lại một mình; Lumo chạy ngược vào, chụp lấy
at(lumo.root, LUMO_BACK[0] - HOLD, 1.9, 0)
facing(lumo, LUMO_BACK[0], -1)                                  # ngoài khung: quay mặt sang trái
for i, t in enumerate(steps(MAP_ALONE[0] + 0.2, MAP_ALONE[1] - 0.2, 0.25)):   # gió nhẹ: mép bản đồ phập phồng
    scl(map_rock, t, 0.3, 0.14 if i % 2 else 0.125)
scl(map_rock, MAP_ALONE[1], 0.3, 0.13)
n0, n1 = LUMO_BACK
walk(lumo.root, n0, n1 - 0.08, 0.75, X_ROCK_R - 0.06, 3, 0.06)
at(lumo.root, n1, X_ROCK_R, 0.0)
stride(n0, n1 - 0.08, 0.15, 34)
lean(lumo, n0, 16)
lean(lumo, n1 - 0.08, 16)
lean(lumo, n1, -12)                                             # khựng lại
ears(lumo, n0, -32)
ears(lumo, n1, 12)
fc(lumo, n0, "shock", 16)
look(lumo, n0, 1.0, -0.4)
ry(lumo.head, n0, 0)
arms(n0, -20, -6)
loop(lumo.arm, n0, n1 - 0.08, 0.15, -50, 10)
loop(lumo.arm_far, n0 + 0.05, n1 - 0.08, 0.15, 10, -50)
arms(n1, -30, -10)
g0, g1 = MAP_GRAB
GRAB_LEAN = 24
a_grab = reach(lumo, X_ROCK_R, 0.0, GRAB_LEAN, MAP_SPOT)
fc(lumo, g0, "eager", GRAB_LEAN)
look(lumo, g0, 0.8, -0.9)
lean(lumo, g0, -12)
lean(lumo, g0 + 0.15, GRAB_LEAN)
arms(g0, -30, -10)
arms(g0 + 0.15, a_grab)
show(map_rock, g0 + 0.17, False)                                # chụp lấy tấm bản đồ
show(map_near, g0 + 0.17, True)
scl(map_near, g0 + 0.17, 0.6, 0.6)
scl(map_near, g1, 1, 1)
lean(lumo, g1, 0)
arms(g1, -70)
ry(lumo.tail, n1, 30)
# "Nhà thám hiểm Lumo không bao giờ quên bản đồ!": ưỡn ngực, hếch cằm
e0, e1 = LUMO_LINE4
lean(lumo, e0 - 0.2, 0)
lean(lumo, e0, -9)
squash(lumo, e0 - 0.2, 1, 1)
squash(lumo, e0, 0.98, 1.04)
ears(lumo, e0 - 0.2, 12)
ears(lumo, e0, 0)
ry(lumo.head, e0, -12)
fc(lumo, e0 - 0.05, "happy", -12)
look(lumo, e0 - 0.05, 0.4, 0.2)
arms(e0, -45)                                                   # giơ bản đồ trước ngực, không che mặt
talk(lumo, e0, e0 + 1.1, "smile")                               # "Nhà thám hiểm Lumo"
talk(lumo, e0 + 1.3, e1 - 0.25, "smile")                        # "không bao giờ quên bản đồ!"
for t, a in ((e0 + 1.3, -12), (e0 + 1.5, -4), (e0 + 1.7, -12)):
    ry(lumo.head, t, a)
loop(lumo.tail, e0, e1, 0.5, 26, 44)
f0, f1 = TURN_EDGE
facing(lumo, f1, 1, f1 - f0)                                    # quay về phía mép đồi
lean(lumo, f1, 0)
squash(lumo, f1, 1, 1)
ry(lumo.head, f1, 14)
arms(f1, -70)
fc(lumo, f1, "puzzled", 14)
look(lumo, f1, 0.6, -0.9)

# ================================================================ S10: cận bản đồ: xoay, xoay nữa, xoay thêm vòng nữa
for i, t in enumerate(steps(SHOT["S10"][0], SHOT["S10"][1], 0.4)):  # tay hơi nhún
    at(insert_hold, t, IX + (0.006 if i % 2 else -0.006), 0.03 + (0.006 if i % 2 else -0.006))
ANG = [0, 180, 270, 630]                                        # rương: đứng thẳng, lộn ngược, nằm ngang, quay một vòng rồi lại ngang
ry(insert_map, 0.0, ANG[0])
for (sa, sb), a, b in zip(MAP_SPINS, ANG, ANG[1:]):
    ry(insert_map, sa, a)
    ry(insert_map, sb, b)
    for side, paw in zip((-1, 1), ipaws):                       # buông ra để xoay
        at(paw, sa - 0.08, side * 0.33, -0.27)
        at(paw, sa + 0.04, side * 0.45, -0.32)
        at(paw, sb - 0.04, side * 0.45, -0.32)
        at(paw, sb + 0.1, side * 0.33, -0.27)
ry(map_near, 0.0, 0)
ry(map_near, MAP_SPINS[-1][0], 0)
ry(map_near, MAP_SPINS[-1][1], 90)                              # trong tay Lumo bản đồ cũng nằm ngang

# ================================================================ S11: nhún vai, gấp bản đồ nhét vào túi
h0, h1 = SHRUG
fc(lumo, h0, "sheepish", -6)
look(lumo, h0, 0.6, 0.3)
squash(lumo, h0, 1, 1)
squash(lumo, h0 + 0.15, 0.93, 1.09)                             # nhún vai
squash(lumo, h1, 1, 1)
arms(h0, -70, -6)
arms(h0 + 0.15, -45, 35)                                        # xòe tay: tay gần ra trước, tay xa ra sau
arms(h1 + 0.2, -65, -6)
ry(lumo.head, h0, 0)
ry(lumo.head, h0 + 0.15, -12)                                   # nghiêng đầu
ry(lumo.head, h1, -4)
ears(lumo, h0, 4)
ears(lumo, h0 + 0.15, -26)                                      # cụp tai
ears(lumo, h1, -8)
o0, o1 = MAP_STOW
fc(lumo, o0, "happy")
look(lumo, o0, 0.4, -0.9)
scl(map_near, o0, 1, 1)
scl(map_near, o0 + 0.35, 0.5, 0.55)                             # gấp lại
scl(map_near, o0 + 0.55, 0.35, 0.35)
arms(o0 + 0.35, -50)
arms(o0 + 0.6, -18)
show(map_near, o0 + 0.62, False)
ears(lumo, o1, 4)
ry(lumo.head, o1, 0)
look(lumo, o1, 1.0, 0.2)
fc(lumo, o1, "eager")

# ================================================================ S12–S14: sải bước ra mép, nhấc chân, khựng lại; chiếc lá; lối mòn; gật đầu
w0, w1 = STRIDE
walk(lumo.root, w0, w1, X_ROCK_R, X_EDGE, 6, 0.04)
stride(w0, w1, 0.2, 28)
lean(lumo, w0, 0)
lean(lumo, w0 + 0.15, 7)
loop(lumo.arm, w0, w1, 0.2, -40, 5)
loop(lumo.arm_far, w0 + 0.05, w1, 0.2, 5, -40)
loop(lumo.tail, w0, w1, 0.3, 24, 44)
look(lumo, w0, 1.0, 0.2)                                        # mắt nhìn phía trước, chưa nhìn xuống chân
lf0, lf1 = LEG_LIFT
legs(lf0, 0, 0)
legs(lf1, -82, 6)                                               # nhấc chân định lao xuống
lean(lumo, lf1, 4)
at(lumo.root, lf1, X_EDGE + 0.02, 0.035)
arms(lf0, -18, -6)
arms(lf1, -45, -40)
fz0, fz1 = FREEZE
lean(lumo, fz0 + 0.1, -10)                                      # khựng lại, người ngả ra sau, chân còn treo
legs(fz0 + 0.1, -76, 8)
arms(fz0 + 0.1, 20, 26)
fc(lumo, fz0 + 0.05, "shock", -10)
look(lumo, fz0 + 0.1, 0.8, -1.0)                                # nhìn xuống sườn dốc lá khô
ry(lumo.head, fz0 + 0.1, 8)
ears(lumo, fz0, 6)
ears(lumo, fz0 + 0.1, 26)
ears(lumo, fz1, 18)
ry(lumo.tail, fz0, 30)
ry(lumo.tail, fz0 + 0.1, 58)
legs(fz1, -78, 8)
s0, s1 = LEAF_SLIDE
streak = streaks[0]                                             # một làn gió nhẹ ở mép dốc
show(streak, s0 - 0.25, True)
at(streak, s0 - 0.25, 0.9, 0.25)
at(streak, s0 + 0.1, 2.4, 0.1)
show(streak, s0 + 0.12, False)
show(slide_leaf, 0.0, True)
for k in range(9):                                              # chiếc lá trượt vèo xuống dốc tới thảm cỏ: WHOOSH!
    u = k / 8
    x = 1.74 + (4.15 - 1.74) * u ** 1.15
    at(slide_leaf, s0 + (s1 - s0) * u, x, ground_z(x) + 0.012)
    ry(slide_leaf, s0 + (s1 - s0) * u, 24 * (0.3 + u) + (8 if k % 2 else -8))
at(slide_leaf, s1 + 0.15, 4.25, LOW + 0.012)
ry(slide_leaf, s1 + 0.15, 4)
look(lumo, s0 + 0.15, 1.0, -1.0)                                # mắt nhìn theo chiếc lá
look(lumo, s1, 1.0, -0.8)
ry(lumo.head, s0 + 0.1, 14)
fc(lumo, s1 - 0.1, "wonder", 4)
bk0, bk1 = LEG_BACK
legs(bk0, -78, 8)
legs(bk1, 0, 0)                                                 # rụt chân về
at(lumo.root, bk0, X_EDGE + 0.02, 0.035)
at(lumo.root, bk0 + 0.15, (X_EDGE + X_BACK) / 2, 0.04)
at(lumo.root, bk1, X_BACK, 0.0)                                 # lùi một bước
lean(lumo, bk0, -10)
lean(lumo, bk1, 0)
arms(bk0, 20, 26)
arms(bk1, -10, -4)
ry(lumo.tail, bk1, 30)
fc(lumo, bk1, "puzzled", 12)
ry(lumo.head, bk1, 12)                                          # vẫn nhìn chiếc lá ở chân dốc
ears(lumo, bk1, 6)
pp0, pp1 = LOOK_PATH
look(lumo, pp0, 1.0, -1.0)
look(lumo, pp1, 1.0, -0.45)                                     # nhìn sang bên: mắt rời chân dốc, sang lối mòn
ry(lumo.head, pp0, 12)
ry(lumo.head, pp1, 6)
fc(lumo, pp1, "eager", 6)
ears(lumo, pp0, 6)
ears(lumo, pp1, 16)                                             # tai dựng lên: thấy rồi (cắt sang góc nhìn S13)
ears(lumo, LUMO_NOD[0] - 0.1, 12)
look(lumo, LUMO_NOD[0] - 0.1, 1.0, -0.45)                       # S14: vẫn nhìn lối mòn, rồi gật đầu
nd0, nd1 = LUMO_NOD
fc(lumo, nd0, "happy", 6)
for t, a in ((nd0, 6), (nd0 + 0.2, 20), (nd0 + 0.4, 4), (nd0 + 0.6, 20), (nd1, 4)):   # gật đầu
    ry(lumo.head, t, a)
ears(lumo, nd1, 6)
loop(lumo.tail, nd0, SECONDS, 0.6, 18, 34)

# ================================================================ S15: chú chim đáp xuống tảng đá, nhìn theo Lumo, gật gù
BIRD_SPOT = (ROCK_X + 0.05, ROCK_TOP + 0.005)
bl0, bl1 = BIRD_LAND
show(bird.root, bl0 - 0.05, True)                               # hiện cả con chim rồi chọn lại mắt, mỏ cùng lúc
bird_eyes(bird, bl0 - 0.05, "open")
bird_beak(bird, bl0 - 0.05, "closed")
for t, x, z in ((bl0 - 0.05, -1.35, 0.78), (bl0 + 0.25, -1.05, 0.62), (bl0 + 0.5, -0.78, 0.42), (bl1, *BIRD_SPOT)):
    at(bird.root, t, x, z)
for i, t in enumerate(steps(bl0 - 0.05, bl1 - 0.05, 0.06)):
    ry(bird.wing, t, 65 if i % 2 else -35)
    ry(bird.wing_far, t, 70 if i % 2 else -30)
ry(bird.wing, bl1 + 0.05, 0)
ry(bird.wing_far, bl1 + 0.05, 0)
scl(bird.root, bl1, 1.12, 0.86)                                 # đáp xuống
scl(bird.root, bl1 + 0.12, 0.95, 1.06)
scl(bird.root, bl1 + 0.25, 1, 1)
ry(bird.head, bl1, 0)
ry(bird.head, bl1 + 0.3, -10)                                   # ngẩng nhìn theo Lumo ở mép đồi
bird_eyes(bird, bl1 + 0.4, "closed")
bird_eyes(bird, bl1 + 0.5, "open")
nb0, nb1 = BIRD_NOD
for t, a in ((nb0, -10), (nb0 + 0.25, 20), (nb0 + 0.5, -4), (nb0 + 0.75, 20), (nb1, 0)):   # gật gù chậm, mắt mở,
    ry(bird.head, t, a)                                         # cánh khép, mỏ ngậm: tán thành, không phải cười

# ================================================================ S16: rút la bàn, nhìn mũi sao, ngẩng nhìn hòn đảo, cất la bàn
x0, x1 = COMPASS_OUT
arms(x0, -10, -4)
arms(x0 + 0.15, -18)
show(comp.root, x0 + 0.17, True)                                # rút la bàn từ túi da
show(comp.flash, x0 + 0.17, False)
show(comp.bright, x0 + 0.17, False)
twinkle(comp.glow, x0 + 0.17, COMPASS_AWAY[1], 0.8, 0.62, 0.45)
arms(x1, -76, -40)
fc(lumo, x0, "eager", 12)
look(lumo, x1, 0.5, -0.9)                                       # nhìn mũi sao
ry(lumo.head, x1, 12)
li0, li1 = LOOK_ISLAND
ry(lumo.head, li0, 12)
ry(lumo.head, li1, -8)
look(lumo, li0 + 0.1, 1.0, 0.5)                                 # ngẩng lên nhìn hòn đảo
fc(lumo, li0 + 0.1, "eager", -8)
ears(lumo, li0, 6)
ears(lumo, li0 + 0.2, 16)
ears(lumo, li1, 8)
bl(lumo, li1 + 0.2)
y0, y1 = COMPASS_AWAY
arms(y0, -76, -40)
arms(y0 + 0.3, -18, -6)
show(comp.root, y0 + 0.35, False)                               # cất la bàn vào túi
ry(lumo.head, y1, 0)
look(lumo, y1, 1.0, 0.15)
fc(lumo, y1, "eager")

# ================================================================ S17: đi xuống theo lối mòn, mắt nhìn phía trước; lóe lần 2
wd0, wd1 = WALK_DOWN
X_END = 3.35
walk_on(wd0, wd1, X_BACK, X_END, 12, 0.03, path_z)
stride(wd0, wd1 - 0.05, 0.34, 18)
arms(wd0, -10, -4)
loop(lumo.arm, wd0, wd1, 0.68, 22, 6)                           # tay gần đánh ra sau, không che túi
loop(lumo.arm_far, wd0 + 0.34, wd1, 0.68, 6, -22)
lean(lumo, wd0, 0)
lean(lumo, wd0 + 0.3, 4)
look(lumo, wd0, 1.0, 0.15)
bl(lumo, 55.2)
glow_flash(hub.flash, HUB_FLASH2, lit=hub.tint)                 # hòn đảo lóe xanh ngọc lần nữa
glow_flash(bag_glow, HUB_FLASH2, 1.5)                           # la bàn lóe theo qua mép nắp túi da
ears(lumo, HUB_FLASH2 + 0.1, 6)
ears(lumo, HUB_FLASH2 + 0.25, 14)                               # tai khẽ dựng, vẫn đi tiếp
ears(lumo, HUB_FLASH2 + 0.5, 8)

# ================================================================ máy quay; bộ trời đi theo máy (vật ở rất xa không trôi)
CAMS = {"S1": (40.0, 0.3, 1.6), "S2": (-4.85, -0.2, 5.4), "S3": (0.6, 0.4, 7.8), "S4": (-0.85, 0.6, 2.6), "S5": (50.0, 0.3, 1.6),
        "S6": (0.15, 0.62, 4.4), "S7": (-0.98, 0.7, 1.7), "S8": (-0.35, 0.68, 3.0), "S9": (-0.62, 0.52, 2.1), "S10": (IX, 0.0, 1.7),
        "S11": (-0.3, 0.62, 2.4), "S12": (2.55, -0.02, 4.4), "S13": (PX - 0.45, -0.02, 2.4), "S14": (1.6, 0.6, 2.3),
        "S15": (-0.66, 0.42, 0.9), "S16": (1.75, 0.62, 2.6), "S17": (2.0, 0.5, 2.8), "S18": (90.0, 0.0, 2.0)}       # tâm X, tâm Z, bề ngang khung (m); đáy khung chừa cho CC
RIG = {"S1": (40.75, 0.55), "S2": (-2.6, -0.35), "S3": (3.2, 0.75), "S4": (1.6, 0.62), "S5": (50.55, 0.32), "S6": (1.25, 0.6),
       "S7": (0.6, 0.6), "S8": (0.55, 0.62), "S9": (1.6, 0.5), "S10": (IX, -5.0), "S11": (0.75, 0.62), "S12": (3.8, 0.2),
       "S13": (PX + 0.5, 0.33), "S14": (2.25, 0.55), "S15": (0.8, 0.45), "S16": (2.4, 0.55), "S17": (2.75, 0.15),
       "S18": (90.0, -5.0)}   # chân hòn đảo trên chân trời
cameras(SHOTS, CAMS)
PAN = {"S13": [(PATH_PAN[0], PX - 0.45, -0.02), (PATH_PAN[1], PX + 0.45, -0.02)],   # lia theo ánh mắt: chân dốc → lối mòn
       "S17": [(SHOT["S17"][0], 2.0, 0.5), (SHOT["S17"][1] - HOLD, 4.05, 0.22)]}     # lia theo Lumo xuống lối mòn
for name, t0, t1 in SHOTS:
    (cx0, cz0, _), (rx, rz) = CAMS[name], RIG[name]
    pan = PAN.get(name, [])
    keys = [(t0, cx0, cz0)] + pan + [(t1 - HOLD, *(pan[-1][1:] if pan else (cx0, cz0)))]
    for t, cx, cz in keys:                                      # bộ trời giữ nguyên vị trí so với máy suốt cú
        key(rig, "location", t, (rx + cx - cx0, rig.location.y, rz + cz - cz0))
        if pan:
            key(bpy.data.objects[f"Cam_{name}"], "location", t, (cx, -10.0, cz))
for ob in [rig] + [bpy.data.objects[f"Cam_{name}"] for name in PAN]:   # nội suy thẳng: bộ trời trượt đúng theo máy,
    for cv in fcurves(ob):
        for kp in cv.keyframe_points:                           # không vồng ra vì key cú kề bên
            kp.interpolation = "LINEAR"

# ================================================================ chống trôi giữa hai key thưa
ease_gaps([lumo.root, lumo.head, lumo.ear_near, lumo.ear_far, lumo.arm, lumo.arm_far, near_hold, far_hold, lumo.tail, lumo.leg_near,
           lumo.leg_far, lumo.cape_pivot, lumo.bag, map_near, *[n for n, _, _ in lumo.pupils]])
ease_gaps([n for n, _, _ in lumo.pupils], 0.3, 0.1)
ease_gaps([bird.root, bird.head])


# ================================================================ mũi sao luôn chỉ về hòn đảo
def island_at(t):
    """Tâm hòn đảo trong thế giới ở khung đang xét (bộ trời đi theo máy quay)."""
    r = rig.matrix_world.translation
    return (r.x + ISLAND_C[0], r.z + ISLAND_C[1])


for c, t0, t1 in ((ins1, *SHOT["S1"]), (ins5, *SHOT["S5"]), (comp, 0.0, COMPASS_STOW[0] + 0.35), (comp, COMPASS_OUT[0], COMPASS_AWAY[1])):
    aim(c, t0, t1, island_at, flat=True)
twinkle(ins1.glow, 0.0, SHOT["S1"][1], 0.8, 0.62, 0.45)
twinkle(ins5.glow, SHOT["S5"][0], SHOT["S5"][1], 0.8, 0.62, 0.45)
bpy.context.scene.frame_set(1)

finish(SECONDS, OUT_BLEND, (1.0, 3.0, 4.4, 7.5, 10.2, 11.8, 13.6, 15.5, 17.5, 19.95, 21.0, 23.0, 25.2, 27.5, 29.5, 30.2, 31.2,
                            32.6, 34.0, 36.2, 36.9, 37.9, 39.5, 40.5, 41.9, 42.9, 43.6, 44.4, 45.0, 46.6, 48.0, 49.3, 51.0,
                            52.2, 53.2, 55.0, 56.45, 57.5, 58.2))
