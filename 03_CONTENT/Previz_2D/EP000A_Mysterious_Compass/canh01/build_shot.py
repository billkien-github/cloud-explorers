"""
EP000A Cảnh 1 (Nhà thám hiểm nhỏ): previz 2D cutout (03_CONTENT/PREVIZ_2D.md, bộ nhân vật pipeline/cutout.py).
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #1#. Mốc thời gian và CC: timing.py; mọi
keyframe tính từ các mốc đó (cộng trừ vài phần mười giây cho nhịp lấy đà, giữ tư thế).
    pipeline/run.sh build -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh01
    pipeline/run.sh preview -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh01
    blender -b --factory-startup -P pipeline/cc.py -- <cảnh>/renders/canh01_preview.mp4 <cảnh>/timing.py <cảnh>/renders/canh01_preview_cc.mp4
Bố cục (X, mét; Z = 0 là mặt đường rừng): Lumo bước vào từ X -3.8, dừng ở 1.68 trước bụi gai (tâm 2.5), vách đá từ
2.6 sang phải; cây có cành chú chim đậu ở 0.75, chim ở 1.43 cao 1.25. Đường rẽ vào rừng ở -3.55…-2.5, mép dốc lá khô ở
-3.9, dốc xuống tới nền rêu Z -1.3 ở X -7.2; đống lá ở -7.3, phiến đá rêu con bướm đậu -8.05, phiến đá có ánh vàng
-8.75, tường phế tích từ -9 sang trái. Hai cú cận bản đồ (S2, S6) dựng riêng, phóng to, ở X = 20.
"""
import math
import pathlib
import random
import sys

import bmesh
import bpy

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.dont_write_bytecode = True                                  # không để __pycache__ cạnh timing.py
sys.path[:0] = [str(HERE), str(ROOT / "pipeline")]
from cutout import *  # noqa: E402,F403  bộ cutout: keyframe, hình, mặt, nhân vật, máy quay
from timing import *  # noqa: E402,F403  FPS, SECONDS, SHOTS, mốc hành động, CC của cảnh

OUT_BLEND = HERE / f"{HERE.name}.blend"
start(FPS)
SHOT = {name: (t0, t1) for name, t0, t1 in SHOTS}
HOLD = 1.0 / FPS                                                # một khung hình: key giữ đặt sớm hơn đúng một khung
random.seed(7)


# ================================================================ bối cảnh
SKY, CLOUD, GRASS, DIRT = "#CDE9F7", "#F1F6FA", "#A5CF63", "#DDB680"
LEAF_COLS = ("#C97B3C", "#E09A52", "#B5642E", "#D98A45")
STONE, STONE_D, STONE_L = "#C9BBA2", "#A8987E", "#D9CCB4"
LOW_Z = -1.3                                                    # nền rêu dưới chân dốc
SLOPE = [(-3.85, 0.02), (-3.95, 0.01), (-4.05, -0.02), (-4.15, -0.06), (-4.3, -0.12), (-6.6, -1.18),
         (-6.8, -1.25), (-7.0, -1.29), (-7.2, LOW_Z)]          # mép tròn, dốc thoải khoảng 25°, chân dốc êm


def ground_z(x):
    if x >= SLOPE[0][0]:
        return 0.0
    for (x0, z0), (x1, z1) in zip(SLOPE, SLOPE[1:]):
        if x1 <= x <= x0:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return LOW_Z


part("Sky", None, [(rect(-16, -5, 26, 7), SKY)], 3.6)
part("SkyClouds", None, [(ell(0.45, 0.16, cx, cz), "#F7FBFD") for cx, cz in ((-3.0, 3.35), (-2.5, 3.45), (3.1, 3.2), (3.6, 3.3),
                                                                          (-6.8, 1.55), (-6.3, 1.62), (-9.6, 1.45))], 3.55)
# đảo lơ lửng và thác đổ xuống biển mây (xa nhất, sau biển mây để chân thác chìm vào mây)
islands = []
for cx, cz, s, fall in ((-1.4, 2.6, 0.75, True), (1.9, 2.95, 0.5, True), (0.25, 3.25, 0.3, False), (-4.1, 2.25, 0.45, True),
                        (-8.9, 1.25, 0.4, True)):
    rock = [(cx - 0.55 * s, cz), (cx + 0.55 * s, cz), (cx + 0.42 * s, cz - 0.22 * s), (cx + 0.2 * s, cz - 0.42 * s), (cx, cz - 0.62 * s),
            (cx - 0.22 * s, cz - 0.45 * s), (cx - 0.45 * s, cz - 0.25 * s)]
    islands += [(rock, "#B48E72"), (turn(ell(0.2 * s, 0.08 * s, cx - 0.15 * s, cz - 0.25 * s), 20, cx, cz), "#A27E63"),
                (ell(0.58 * s, 0.1 * s, cx, cz), "#93C95A")]
    islands += [(ell(0.13 * s, 0.12 * s, cx + dx * s, cz + 0.16 * s), col) for dx, col in ((-0.3, "#7DB843"), (0.05, "#86C04E"), (0.32, "#F2B3CB"))]
    if fall:
        islands += [(rect(cx + 0.28 * s, 1.0, cx + 0.38 * s, cz - 0.02), "#E4F5FF"), (rect(cx + 0.3 * s, 1.0, cx + 0.33 * s, cz - 0.02), WHITE)]
part("Islands", None, islands, 3.3)
part("CloudSea", None, [(rect(-16, -5, 26, 0.95), CLOUD)] + [(ell(0.5, 0.2, -16 + 0.7 * i, 0.95 + 0.04 * (i % 3)), CLOUD) for i in range(60)],
     3.2)
FAR = [(26, 0.45), (-3.0, 0.45), (-4.2, 0.25), (-5.6, -0.25), (-7.0, -0.55), (-16, -0.55)]


def far_z(x):
    for (x0, z0), (x1, z1) in zip(FAR, FAR[1:]):
        if x1 <= x <= x0:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return FAR[-1][1]


part("FarTrees", None, [(ell(0.3, 0.2, x, far_z(x) + 0.13), "#C6E4A6" if i % 2 else "#B9DD97")
                        for i, x in enumerate(-16 + 0.42 * k for k in range(100)) if i % 7 not in (3, 4)], 2.62)
part("FarFloor", None, [(FAR + [(-16, -5), (26, -5)], "#C2E2A0")], 2.6)
part("PathFork", None, [([(-3.55, 0.02), (-2.85, 0.02), (-2.62, 0.18), (-2.5, 0.36), (-2.55, 0.44), (-2.68, 0.44), (-2.8, 0.3),
                          (-3.1, 0.14)], "#E2BE8A")], 2.45)     # đường rừng rẽ vào trong rừng; mép dốc ở thẳng phía trước


def tree(name, x, z0, h, r, col, y, lean_x=0.05):
    trunk = [(x - 0.09, z0), (x + 0.09, z0), (x + 0.06 + lean_x, z0 + h), (x - 0.06 + lean_x, z0 + h)]
    cx, cz = x + lean_x, z0 + h + r * 0.35
    canopy = [(ell(r, r * 0.72, cx, cz), col), (ell(r * 0.7, r * 0.55, cx - r * 0.7, cz - r * 0.2), col),
              (ell(r * 0.7, r * 0.55, cx + r * 0.75, cz - r * 0.15), col), (ell(r * 0.45, r * 0.3, cx - r * 0.2, cz + r * 0.35), "#FFFFFF" if col == "#F4AFC9" else "#A3D45E")]
    part(name, None, [(trunk, "#8B5E3C")] + canopy, y)


tree("Tree_Fork", -3.2, 0.06, 1.25, 0.6, "#86C04E", 2.3)
tree("Tree_Pink", -1.85, 0.06, 1.05, 0.5, "#F4AFC9", 2.32)
tree("Tree_Mid", -0.55, 0.05, 1.35, 0.62, "#7DB843", 2.3)
tree("Tree_Low", -6.0, far_z(-6.0) + 0.02, 1.2, 0.55, "#86C04E", 2.3)

GROUND = [(26, 0.02)] + SLOPE + [(-16, LOW_Z), (-16, -5), (26, -5)]
ground = part("Ground", None, [(GROUND, GRASS)], 2.0)
part("Path", None, [([(-3.55, -0.15), (2.7, -0.15), (2.7, 0.02), (-3.55, 0.02)], DIRT)], 1.9)
tufts = []
for gx in (-3.3, -2.6, -1.9, -1.0, -0.2, 0.6, 1.3, 2.1, -3.75, -5.5, -8.5, -9.6, -6.3):
    gz = -0.15 if gx > -3.6 else ground_z(gx) - 0.12
    tufts += [([(gx - 0.03, gz), (gx + 0.03, gz), (gx + 0.005, gz + 0.08)], "#7DB843"),
              ([(gx + 0.01, gz), (gx + 0.05, gz), (gx + 0.06, gz + 0.06)], "#7DB843")]
flowers = [(ell(0.022, 0.022, fx, fz), col) for fx, fz, col in ((-2.9, -0.2, "#B79BE8"), (-1.4, -0.22, WHITE), (0.2, -0.24, "#B79BE8"),
                                                                (1.0, -0.2, WHITE), (-9.3, -1.42, "#F7A8C8"), (-7.9, -1.45, WHITE))]
part("Tufts", None, tufts + flowers, 1.85)
litter = [(SLOPE[1:-1] + [(x, max(z - 0.3, LOW_Z)) for x, z in reversed(SLOPE[1:-1])], "#CC8A4A")]   # lớp lá khô dày phủ kín sườn dốc
for i in range(90):
    lx = -3.95 - (i % 30) * 0.105 - 0.05 * (i // 30)
    litter.append((leaf_pts(lx, max(ground_z(lx) - 0.1 * (i // 30), LOW_Z + 0.03) + random.uniform(-0.03, 0.03), 1.4, random.uniform(-50, 50)), LEAF_COLS[i % 4]))
part("SlopeLeaves", None, litter, 1.93)

# --- cây có cành chú chim đậu (gần Lumo lúc quay lại)
BRANCH = curve((0.78, 1.1), (1.3, 1.25), (1.8, 1.21), 40)
BIRD_X = 1.43
BIRD_Z = min(BRANCH, key=lambda p: abs(p[0] - BIRD_X))[1] + 0.024
part("Tree_Bird", None, [([(0.66, 0.03), (0.86, 0.03), (0.84, 1.75), (0.7, 1.75)], "#8B5E3C"),
                         (ell(0.75, 0.42, 0.78, 2.15), "#7DB843"), (ell(0.48, 0.32, 0.22, 1.95), "#86C04E"),
                         (ell(0.5, 0.3, 1.3, 2.0), "#86C04E"), (ell(0.3, 0.18, 0.6, 2.35), "#A3D45E")], 1.5)
part("Branch", None, [(band(BRANCH, 0.05), "#8B5E3C"), (ell(0.11, 0.06, 1.84, 1.25), "#7DB843"),
                      (leaf_pts(1.7, 1.27, 1.4, 20), "#86C04E")], 1.0)

# --- vách đá cao chắn ngang lối, bụi gai trước chân vách
CLIFF = [(2.68, 0.0), (2.6, 0.4), (2.66, 0.9), (2.58, 1.5), (2.7, 2.1), (2.64, 2.7), (2.85, 3.3), (3.2, 3.9), (9, 3.9), (9, 0.0)]
part("Cliff", None, [(CLIFF, "#BFA88F")]
     + [(ell(rx, rz, cx, cz), col) for rx, rz, cx, cz, col in ((0.5, 0.7, 3.3, 0.7, "#B39A81"), (0.6, 0.8, 3.6, 2.2, "#B39A81"),
                                                             (0.35, 0.5, 2.95, 1.6, "#CDB9A0"), (0.4, 0.45, 3.1, 2.9, "#CDB9A0"))]
     + [(band([(2.66, 2.7), (2.72, 2.2), (2.65, 1.7)], 0.05), "#6E9E3C"), (ell(0.3, 0.12, 2.9, 3.35), "#8DB04F"),
        (band([(2.85, 3.3), (2.9, 2.6), (2.84, 2.1)], 0.04), "#6E9E3C")], 1.3)
bush = node("Bush", None, (2.5, 0.0), -0.5)
part("TripStone", None, [(ell(0.075, 0.05, 1.68, 0.01), "#9C968A"), (ell(0.045, 0.018, 1.66, 0.035), "#B8B2A6")],
     -0.45)                                                     # hòn đá nhô lên giữa đường, ngay trước bụi gai: Lumo vấp
BURRS = ((-0.3, 0.55), (-0.27, 0.78), (-0.05, 0.9), (0.17, 0.84), (0.3, 0.62), (-0.37, 0.33), (0.04, 0.62), (0.22, 0.3),
         (-0.14, 0.4))
part("Bush_Shape", bush, [(ell(0.42, 0.38, 0, 0.38), "#6E9F3F"), (ell(0.3, 0.3, -0.18, 0.5), "#7DB04A"),
                          (ell(0.28, 0.27, 0.15, 0.62), "#7DB04A"), (ell(0.22, 0.2, -0.05, 0.75), "#8CC055"),
                          (ell(0.2, 0.18, 0.25, 0.4), "#689A3D")]
     + [(leaf_pts(bx, bz, 2.6, a), "#94C85E") for bx, bz, a in ((-0.25, 0.2, 30), (0.1, 0.3, -20), (0.3, 0.8, 40), (-0.2, 0.65, -35))]
     + [s for bx, bz in BURRS for s in ((star(0.042, bx, bz, 12, 0.62), "#D8B887"), (ell(0.026, 0.026, bx, bz), "#E8CF9F"))])

# --- phế tích cổ dưới chân dốc, gần như bị cây cối nuốt chửng
blocks = [(rect(-12.6, LOW_Z, -9.0, 0.12), STONE_D)]
for row, (z0, z1, xs) in enumerate(((LOW_Z, -0.85, (-12.6, -11.7, -10.8, -9.9, -9.0)), (-0.85, -0.35, (-12.4, -11.3, -10.3, -9.25)),
                                    (-0.35, 0.12, (-12.2, -11.0, -10.0, -9.45)))):
    for x0, x1 in zip(xs, xs[1:]):
        blocks.append((rrect(x1 - x0 - 0.04, z1 - z0 - 0.04, 0.04, (x0 + x1) / 2, (z0 + z1) / 2), STONE if (row + int(x0)) % 2 else STONE_L))
blocks += [(ell(0.2, 0.2, -9.95, -0.6), STONE_D), (ell(0.17, 0.17, -9.95, -0.6), STONE), (rose(0.15, -9.95, -0.6), STONE_D),
           (ell(0.03, 0.03, -9.95, -0.6), STONE)]                # phù điêu mặt la bàn: sao tám cánh kiểu hoa gió
blocks += [(ell(0.12, 0.07, cx, -0.12), STONE_D) for cx in (-11.55, -11.4, -11.25)]   # phù điêu mây
blocks += [(ell(rx, 0.06, cx, cz), "#86B24C") for rx, cx, cz in ((0.5, -11.8, 0.14), (0.4, -10.6, 0.15), (0.25, -9.6, 0.14))]
part("Ruins", None, blocks, 1.2)
vines = []
for vx, vz0, vz1 in ((-9.5, 0.12, -0.75), (-10.35, 0.15, -0.3), (-11.1, 0.12, -0.9), (-9.15, -0.3, -1.0)):
    pts = [(vx + 0.03 * math.sin(k), vz0 + (vz1 - vz0) * k / 6) for k in range(7)]
    vines.append((band(pts, 0.025), "#5E9437"))
    vines += [(leaf_pts(x + 0.03, z, 1.3, 30 if k % 2 else -30), "#7DB843") for k, (x, z) in enumerate(pts) if k % 2]
part("Vines", None, vines, 1.15)
part("RuinTree", None, [([(-10.75, LOW_Z), (-9.9, LOW_Z), (-10.05, -0.7), (-10.12, 0.2), (-10.18, 0.9), (-10.42, 0.9), (-10.45, 0.2),
                          (-10.5, -0.7)], "#8B5E3C"),
                        (band([(-10.1, 0.0), (-9.7, 0.12), (-9.5, -0.2), (-9.4, -0.8)], 0.06), "#8B5E3C"),   # rễ phủ qua tường
                        (band([(-10.4, 0.1), (-10.8, 0.14), (-11.0, -0.3)], 0.05), "#8B5E3C"),
                        (ell(1.0, 0.55, -10.3, 1.3), "#7DB843"), (ell(0.6, 0.4, -9.5, 1.0), "#86C04E"),
                        (ell(0.6, 0.4, -11.2, 1.05), "#86C04E")], 1.1)
GLOW_Z = LOW_Z + 0.14                                           # mặt bậc đá chân tường
part("Step", None, [(rrect(1.1, 0.16, 0.03, -9.0, LOW_Z + 0.06), STONE_D), (ell(0.3, 0.04, -9.2, GLOW_Z), "#86B24C")], 0.7)
part("Slabs", None, [(rrect(0.42, 0.07, 0.025, -8.75, GLOW_Z + 0.03), "#B8AA92"), (rrect(0.3, 0.06, 0.02, -9.3, LOW_Z + 0.015), "#B8AA92"),
                     (rrect(0.25, 0.05, 0.02, -8.3, LOW_Z + 0.01), "#B8AA92")], 0.6)
glow = part("GoldGlow", None, [(ell(0.34, 0.11), "#FFE9A6"), (ell(0.2, 0.06), "#FFF6D2")]
            + [(band([(dx * 0.4, 0.02), (dx, 0.32)], 0.025), "#FFF0B8") for dx in (-0.16, 0.0, 0.16)], 0.62, (-8.75, GLOW_Z + 0.05))   # ánh vàng lọt
glint = part("GoldGlint", None, [(star(0.08, 0, 0, 4, 0.3), "#FFD54F")], 0.58, (-8.6, GLOW_Z + 0.09))   # qua khe phiến đá
part("MossStone", None, [(ell(0.21, 0.2, -8.05, LOW_Z, 0, 180), "#A9A08F"), (ell(0.18, 0.05, -8.05, LOW_Z + 0.17), "#86B24C")], -0.55)
# mảnh nền phía trước Lumo (y -0.45) che phần người lún dưới mặt đất ở đống lá; nằm chung object với nền để Workbench
# không vẽ viền tối ở mép mảnh
bm = bmesh.new()
bm.from_mesh(ground.data)
bm.faces.new([bm.verts.new((x, -0.45 - ground.location.y, z)) for x, z in rect(-9.2, -5, -6.5, LOW_Z)])
bm.to_mesh(ground.data)
bm.free()
pile = node("LeafPile", None, (-7.3, LOW_Z), -0.5)
part("LeafPile_Shape", pile, [(ell(0.52, 0.45, 0, 0, 0, 180), "#C9803F")]
     + [(leaf_pts(0.45 * math.cos(math.radians(a)) * rr, 0.4 * math.sin(math.radians(a)) * rr, 1.6, a * 1.7), LEAF_COLS[k % 4])
        for k, (a, rr) in enumerate((a, rr) for rr in (0.95, 0.7, 0.4) for a in range(15, 170, 22))])

# --- tên phim
title = [text("Title1", "CLOUD EXPLORERS", 0.42, (-1.3, 2.95), "#FC6640"),
         text("Title2", "LUMO: CHIẾC LA BÀN BÍ ẨN", 0.27, (-1.3, 2.45), "#7B3FB5")]


# ================================================================ bản đồ giấy (Props/Paper_Map: rương, mũi tên chỉ xuống khi đúng chiều)
# --- S2, S6: cận bản đồ Lumo cầm trước ngực, nhìn từ trên xuống (X = 20, phóng to)
IX = 20.0
part("Insert_Ground", None, [(rect(IX - 1.0, -0.6, IX + 1.0, 0.6), "#D9B07A"), (rect(IX - 1.0, -0.6, IX - 0.62, 0.6), GRASS),
                             (rect(IX + 0.62, -0.6, IX + 1.0, 0.6), GRASS)], 1.0)
insert_scroll = node("Insert_Scroll", None, (IX, 0.0), 0.95)    # sỏi, lá trên đường trôi xuống khi Lumo bước
part("Insert_Pebbles", insert_scroll, [(ell(0.025, 0.018, x, z), "#C49A66") for x, z in ((-0.5, -0.3), (0.45, 0.1), (-0.4, 0.45), (0.5, 0.8),
                                                                                       (-0.45, 1.1), (0.42, -0.4), (0.48, 1.4))]
     + [(leaf_pts(x, z, 2.0, a), LEAF_COLS[k % 4]) for k, (x, z, a) in enumerate(((-0.55, 0.2, 30), (0.52, 0.55, -20), (-0.5, 0.95, 60),
                                                                                  (0.55, 1.25, 10), (0.5, -0.15, -40)))])
part("Insert_Belly", None, [(ell(0.38, 0.16, IX, -0.56), "#FEECCF"), (rect(IX - 0.75, -0.6, IX - 0.42, -0.36), "#FC6640"),
                            (rect(IX + 0.42, -0.6, IX + 0.75, -0.36), "#FC6640")], 0.5)
insert_hold = node("Insert_Hold", None, (IX, 0.03), 0.3)        # tay và bản đồ nhún theo bước
insert_map = node("Insert_Map", insert_hold, (0.0, 0.0), 0.0)
part("Insert_MapShape", insert_map, map_big())
paws = []
for side in (-1, 1):
    paw = node(f"Insert_Paw{side}", insert_hold, (side * 0.33, -0.27), -0.05)
    part(f"Insert_PawShape{side}", paw, [(rrect(0.13, 0.3, 0.06, side * 0.02, -0.14), "#FD8A2B"), (ell(0.075, 0.06, 0, 0), "#FD8A2B"),
                                         (ell(0.045, 0.03, 0, 0.01), "#FEECCF")])
    paws.append(paw)


# ================================================================ nhân vật nền: chú chim nhỏ, bướm phát sáng (Character Bible)
def drift(f, t0, t1, cx, cz, ax, az, speed=0.35, phase=0.0, dt=0.4):
    """Bay lượn quanh (cx, cz) theo hình số 8."""
    for t in steps(t0, t1, dt):
        u = (t + phase) * speed
        at(f.root, t, cx + ax * math.sin(u), cz + az * math.sin(2 * u) + 0.03 * math.sin(7 * u))
        scl(f.root, t, 1 if math.cos(u) >= 0 else -1, 1)


bird = build_bird(BIRD_X, BIRD_Z, 0.9)
bflies = [build_bfly(f"Butterfly{i}", lay) for i, lay in enumerate((1.4, 1.42, -0.2, -0.6))]

# ================================================================ Lumo và đồ trong tay
lumo = build_lumo(-3.8, -0.32)
map_hold = palm(lumo, "Lumo_MapHold")
map_sheet = node("Lumo_Map", map_hold, (0.035, 0.07), -0.002)
part("Lumo_MapShape", map_sheet, map_card())
burr = part("Lumo_Burr", lumo.head, [(star(0.03, 0, 0, 12, 0.62), "#D8B887"), (ell(0.019, 0.019), "#E8CF9F")], -0.03, (0.262, 0.168))
LEAF_ON = [(leaf_pts(0.0, 0.0, 2.6, 15), "#9A4B1F"), (band([(-0.08, -0.02), (0.08, 0.02)], 0.006), "#6E3415")]   # lá sẫm, nổi trên lông cam
head_leaf = part("Lumo_Leaf", lumo.head, LEAF_ON,
                 -0.03, (0.1, 0.32))
burr_fly = part("BurrFly", None, [(star(0.03, 0, 0, 12, 0.62), "#D8B887"), (ell(0.019, 0.019), "#E8CF9F")], -0.6, (2.0, 0.65))
leaf_fall = part("LeafFall", None, LEAF_ON, -0.6, (-7.38, -0.62))
map_fly = node("MapFly", None, (-4.0, 0.5), -0.4)
part("MapFly_Shape", map_fly, map_card())
bits = [part(f"Leaf{i}", None, [(leaf_pts(0, 0, 1.8, 0), LEAF_COLS[i % 4])], -0.62 if i < 10 else -0.35) for i in range(16)]
bush_bits = [part(f"BushLeaf{i}", None, [(leaf_pts(0, 0, 2.2, 0), "#7DB04A")], -0.55) for i in range(4)]


def hold(t, near, far=None):
    """Tay cầm bản đồ: tấm bản đồ luôn đứng thẳng theo thân dù tay xoay; tay xa mặc định theo tay gần, lệch 5°."""
    chold(lumo, map_hold, t, near, far, off=5)


for ob in (burr, head_leaf, burr_fly, leaf_fall, map_fly, glint, *title, *bits, *bush_bits):
    show(ob, 0.0, False)
show(map_sheet, 0.0, True)

# ================================================================ Lumo: rừng mây, bụi gai
lumo.cur = "eager"
w0, w1 = LUMO_WALK_IN
at(lumo.root, 0.0, -3.8, 0)
fc(lumo, 0.0, "eager", 16)
hold(0.0, -65)
ry(map_sheet, 0.0, 180)                                         # cầm ngược: mũi tên chỉ lên, rương lộn ngược
ry(lumo.head, 0.0, 16)                                          # cắm mặt vào bản đồ
look(lumo, 0.0, 0.5, -0.9)
ears(lumo, 0.0, -30)
lean(lumo, 0.0, -3)                                             # ưỡn ngực, sải bước tự tin
walk(lumo.root, w0, SHOT["S2"][0], -3.8, -1.4, 6, 0.045)
walk(lumo.root, SHOT["S2"][0], SHOT["S3"][0], -1.4, 1.3, 6, 0.045)
at(lumo.root, SHOT["S3"][0] + 0.15, 1.52, 0.03)
STOP_X, SOT_X = 1.5, 1.8                                        # dừng cách bụi gai một bước, hòn đá ở giữa; SỘT: đầu lút trong bụi
at(lumo.root, w1, STOP_X, 0)
loop(lumo.tail, 0.0, w1, 0.5, 18, 36)                           # đuôi vểnh, ve vẩy theo bước
for i, t in enumerate(steps(w0, w1 - 0.2, 0.3)):                # đầu nhún theo bước
    ry(lumo.head, t, 16 if i % 2 else 12)
bl(lumo, 2.6)
# dựng thẳng hai tai, chìa bản đồ thẳng ra trước ngang ngực
p0, p1 = LUMO_POSE
CHEST, PUSH = -72, -80                                          # tay chìa bản đồ ngang ngực; đẩy tới thêm ở câu hô
MAP_UP, MAP_CHEST = (0.035, -0.002, 0.07), (0.045, -0.002, 0.02)   # tấm bản đồ: sát mặt khi đọc, hạ ngang ngực khi chìa ra
key(map_sheet, "location", 0.0, MAP_UP)
ears(lumo, p0, -30)
ears(lumo, p0 + 0.15, 14)                                       # bật dựng thẳng hai tai
ears(lumo, p1, 0)
hold(p0, -65)
hold(p0 + 0.25, CHEST)
key(map_sheet, "location", p0, MAP_UP)
key(map_sheet, "location", p0 + 0.25, MAP_CHEST)
ry(lumo.head, p0, 14)
ry(lumo.head, p0 + 0.2, -6)
ry(lumo.head, p1, 0)
lean(lumo, p0, -3)
lean(lumo, p0 + 0.25, -6)
squash(lumo, p0, 1, 1)
squash(lumo, p0 + 0.12, 1.08, 0.92)
squash(lumo, p0 + 0.25, 0.95, 1.06)
squash(lumo, p1, 1, 1)
fc(lumo, p0 + 0.15, "eager")
look(lumo, p0 + 0.15, 0.7, -0.4)                                # mắt vẫn trên bản đồ, không thấy bụi gai
ry(lumo.tail, w1, 30)
loop(lumo.tail, p1, LUMO_STEP[0], 0.6, 22, 40)
# "Kho báu cổ đại… ngay phía trước!"
l0, l1 = LUMO_LINE1
fc(lumo, l0 - 0.05, "shout")
talk(lumo, l0, l0 + 0.8, "smile")                               # "Kho báu cổ đại…"
talk(lumo, l0 + 1.0, l1, "smile")                               # "…ngay phía trước!"
hold(l0 + 0.9, CHEST)
hold(l0 + 1.1, PUSH)                                            # đẩy bản đồ tới thêm ở "ngay phía trước"
lean(lumo, l0 + 0.9, -6)
lean(lumo, l0 + 1.15, 2)
ry(lumo.head, l0 + 0.9, 0)
ry(lumo.head, l0 + 1.15, -8)
bl(lumo, l1 + 0.05)
# bước tới, mũi chân vấp hòn đá, chúi người ngã vào bụi gai: SỘT! (đà, quán tính, nảy lại; không ngả cứng như tấm ván)
s0, s1 = LUMO_STEP
at(lumo.root, s0, STOP_X, 0)
at(lumo.root, s0 + 0.16, STOP_X + 0.08, 0.04)                  # sải bước, nhổm lên
at(lumo.root, TRIP, STOP_X + 0.14, 0.02)                        # chân trước vướng hòn đá
at(lumo.root, SOT, SOT_X, 0)
lean(lumo, s0, -4)
lean(lumo, TRIP, 2)
lean(lumo, TRIP + 0.08, 16)                                     # chúi người tới
lean(lumo, SOT, 28)
lean(lumo, SOT + 0.1, 32)                                       # quán tính: còn chúi thêm sau lúc chạm
lean(lumo, SOT + 0.25, 27)
fc(lumo, TRIP, "shock", 2)                                      # vấp: tròn mắt, miệng chữ O
ry(lumo.head, TRIP, -10)
ry(lumo.head, SOT - 0.05, -4)
ry(lumo.head, SOT + 0.05, 6)
fc(lumo, SOT, "squint", 34)                                     # nhắm tịt mắt
hold(TRIP + 0.06, -125)                                         # hai tay hất lên theo cú vấp (thấp hơn tai)
ears(lumo, SOT - 0.05, 0)
ears(lumo, SOT + 0.05, -40)
ry(lumo.tail, SOT - 0.05, 30)
ry(lumo.tail, SOT + 0.05, 50)                                   # đuôi dựng đứng
squash(lumo, SOT, 1.05, 0.95)
squash(lumo, SOT + 0.15, 1, 1)
hold(SOT + 0.15, -40)                                           # tay buông xuống, bản đồ thõng thấp
jitter(bush, SOT, SOT + 0.4, 0.015, 0.05)
for i, ob in enumerate(bush_bits):                              # vài chiếc lá bụi gai bật ra
    fly_bit(ob, SOT, (2.2, 0.75 + 0.06 * i), (1.9 + 0.2 * i, 0.02), SOT + 0.9 + 0.1 * i, 220, 0.25)
# kẹt trong bụi gai, ngọ nguậy
for i, t in enumerate(steps(SOT + 0.3, BACK_OUT[0] - 0.1, 0.3)):
    lean(lumo, t, 31 if i % 2 else 25)                          # đầu vẫn lút trong bụi
    ears(lumo, t, -40 if i % 2 else -30)
loop(lumo.tail, SOT + 0.2, BACK_OUT[0], 0.25, 38, 55)
# lùi ra, quả gai dính trên chóp mũi
b0, b1 = BACK_OUT
at(lumo.root, b0, SOT_X, 0)
at(lumo.root, b0 + 0.18, 1.73, 0.03)
at(lumo.root, b1, 1.7, 0)
lean(lumo, b0, 26)
lean(lumo, b0 + 0.18, -8)
lean(lumo, b1, 0)
show(burr, b0 + 0.05, True)
fc(lumo, b0 + 0.18, "shock")
ry(lumo.head, b1, 4)
ears(lumo, b0 + 0.18, 6)
ry(lumo.tail, b1, 20)
hold(b1, CHEST)
# nhìn quả gai trên mũi (mắt dồn về chóp mũi)
fc(lumo, BURR_LOOK[0], "puzzled", 8)
look(lumo, BURR_LOOK[0], 1.0, -0.7)
ry(lumo.head, BURR_LOOK[0], 8)
bl(lumo, BURR_LOOK[1] - 0.2)
# lắc đầu, quả gai văng ra
h0, h1 = HEAD_SHAKE
fc(lumo, h0, "squint")
loop(lumo.head, h0, h1 - 0.05, 0.12, -16, 16)
loop(lumo.ear_near, h0, h1 - 0.05, 0.12, -45, 20)
loop(lumo.ear_far, h0 + 0.03, h1 - 0.05, 0.12, -45, 20)
ry(lumo.head, h1, 0)
ears(lumo, h1, -5)
show(burr, BURR_FLY, False)
fly_bit(burr_fly, BURR_FLY, (1.99, 0.66), (2.2, 0.02), BURR_FLY + 0.55, 300, 0.25)
fc(lumo, h1, "neutral")
look(lumo, h1, 0.0, 0.0)
# nhìn bụi gai, nhìn bản đồ
fc(lumo, LOOK_BUSH[0], "puzzled")
look(lumo, LOOK_BUSH[0], 1.0, 0.1)
bl(lumo, LOOK_BUSH[1] - 0.05)
look(lumo, LOOK_MAP[0], 0.7, -0.8)
ry(lumo.head, LOOK_MAP[0], 0)
ry(lumo.head, LOOK_MAP[1], 14)
fc(lumo, LOOK_MAP[1], "puzzled", 14)
hold(LOOK_MAP[0], CHEST)
hold(LOOK_MAP[1], -75)                                          # kéo bản đồ lại gần mặt
key(map_sheet, "location", LOOK_MAP[0], MAP_CHEST)
key(map_sheet, "location", LOOK_MAP[1], MAP_UP)
# xoay bản đồ nửa vòng: rương đứng thẳng, mũi tên chỉ xuống, ra sau lưng
t0, t1 = MAP_TURN
ry(map_sheet, t0, 180)
ry(map_sheet, t1, 360)
hold(t0, -75)
hold((t0 + t1) / 2, -80)
hold(t1, -75)
# "À… phía trước là phía sau."
a0, a1 = LUMO_LINE2
fc(lumo, a0 - 0.05, "wonder", 14)                               # "À…": hiểu ra
ears(lumo, a0, -5)
ears(lumo, a0 + 0.15, 12)
ears(lumo, a0 + 0.3, 5)
talk(lumo, a0, a0 + 0.45, "o")
ry(lumo.head, a0 + 0.5, 14)
ry(lumo.head, a0 + 0.8, 4)
fc(lumo, a0 + 0.6, "puzzled", 4)
talk(lumo, a0 + 0.6, a1, "o")                                   # "…phía trước là phía sau."
look(lumo, a0 + 0.6, 0.8, -0.3)
look(lumo, LOOK_BEHIND, 0.8, -0.3)
look(lumo, LOOK_BEHIND + 0.15, -1.0, 0.0)                       # mắt liếc ra sau lưng
look(lumo, a1, -1.0, 0.0)
ry(lumo.head, LOOK_BEHIND, 4)
ry(lumo.head, LOOK_BEHIND + 0.2, -6)
ry(lumo.tail, a0, 20)
# quay ngoắt lại: con đường rừng rộng mở
q0, q1 = LUMO_TURN
ears(lumo, q0, 5)
ears(lumo, q0 + 0.08, -25)
ears(lumo, q1 + 0.15, 10)
ears(lumo, q1 + 0.3, 2)
facing(lumo, q1, -1, q1 - q0)
lean(lumo, q0, 0)
lean(lumo, q1, 6)
lean(lumo, q1 + 0.25, 0)
ry(lumo.head, q1, 0)
fc(lumo, q1 + 0.05, "eager")
look(lumo, q1 + 0.05, 0.9, 0.2)
ry(lumo.tail, q0, 20)
ry(lumo.tail, q1, -10)
ry(lumo.tail, q1 + 0.2, 30)
hold(q1 + 0.2, -75)
hold(q1 + 0.5, -45)                                             # hạ bản đồ xuống ngang bụng
for t in (q1 + 0.4, q1 + 0.7):                                  # nhón chân hớn hở
    squash(lumo, t, 1, 1)
    squash(lumo, t + 0.1, 0.97, 1.04)
    squash(lumo, t + 0.22, 1, 1)
loop(lumo.tail, q1 + 0.3, BIRD_LAUGH[0], 0.6, 14, 34)
fc(lumo, TITLE[0] + 0.6, "happy")
j0, j1 = LUMO_HOP                                               # nhảy cẫng lên một cái, giơ bản đồ (không quá ngang tai)
at(lumo.root, j0, 1.7, 0)
squash(lumo, j0, 1, 1)
squash(lumo, j0 + 0.12, 1.1, 0.88)                              # nhún lấy đà
at(lumo.root, j0 + 0.12, 1.7, 0)
squash(lumo, j0 + 0.25, 0.92, 1.1)
at(lumo.root, j0 + 0.35, 1.7, 0.18)
at(lumo.root, j1 - 0.08, 1.7, 0)
squash(lumo, j1 - 0.08, 1.1, 0.9)                               # đáp
squash(lumo, j1 + 0.1, 1, 1)
ears(lumo, j0, 2)
ears(lumo, j0 + 0.2, 18)
ears(lumo, j1 + 0.15, 4)
hold(j0, -45)
hold(j0 + 0.25, -115)
hold(j1 + 0.25, -45)
ry(lumo.head, j0 + 0.2, -10)
ry(lumo.head, j1 + 0.2, 0)
fc(lumo, TITLE[0] + 2.0, "eager")
look(lumo, TITLE[0] + 2.0, 0.9, 0.2)
bl(lumo, TITLE[1] + 0.2)

# ================================================================ chú chim: đậu trên cành xem từ đầu, nghiêng đầu, vỗ bụng cười, bay đi
bird.cur = "open"


bird_eyes(bird, 0.0, "open")
bird_beak(bird, 0.0, "closed")
ry(bird.wing, 0.0, 0)
ry(bird.wing_far, 0.0, 0)
for t in (2.2, 6.0, 12.0, 16.5, 20.5):                          # chớp mắt
    bird_eyes(bird, t, "closed")
    bird_eyes(bird, t + 0.1, "open")
for t, a in ((0.0, 0), (4.0, 8), (7.0, 0), (SOT, 0), (SOT + 0.1, -14), (SOT + 0.5, 6), (14.0, 10), (18.0, 0)):
    ry(bird.head, t, a)                                         # ngó theo Lumo; giật mình lúc SỘT
ty0, ty1 = BIRD_TILT
ry(bird.head, ty0, 0)
ry(bird.head, ty1, 24)                                          # nghiêng đầu nhìn Lumo
ry(bird.head, BIRD_LAUGH[0], 24)
for c in CHIRPS:                                                # vỗ cánh vào bụng: CHÍP CHÍP CHÍP!
    ry(bird.wing, c - 0.18, -55)
    ry(bird.wing, c, -100)
    ry(bird.wing, c + 0.1, -70)
    ry(bird.wing, c + 0.2, -100)
    ry(bird.wing, c + 0.3, -60)
    bird_beak(bird, c - 0.02, "open")
    bird_beak(bird, c + 0.22, "closed")
    at(bird.root, c - 0.1, BIRD_X, BIRD_Z)
    at(bird.root, c + 0.05, BIRD_X, BIRD_Z + 0.025)
    at(bird.root, c + 0.25, BIRD_X, BIRD_Z)
    scl(bird.root, c - 0.1, 1.08, 0.92)
    scl(bird.root, c + 0.05, 0.95, 1.06)
    scl(bird.root, c + 0.25, 1, 1)
    ry(bird.head, c, -14)                                       # ngửa đầu cười
    ry(bird.head, c + 0.3, 6)
bird_eyes(bird, BIRD_LAUGH[0], "happy")
bird_eyes(bird, BIRD_LAUGH[1] + 0.2, "open")
ry(bird.wing, BIRD_LAUGH[1], -60)
ry(bird.wing, BIRD_LAUGH[1] + 0.2, 0)
ry(bird.head, BIRD_LAUGH[1] + 0.2, 18)
for c in (LUMO_PUFF[0] + 0.1, LUMO_LINE3[1] - 0.6):              # còn khúc khích khi Lumo chống chế
    bird_eyes(bird, c, "happy")
    bird_beak(bird, c, "open")
    ry(bird.wing, c, 0)
    ry(bird.wing, c + 0.12, -95)
    ry(bird.wing, c + 0.3, 0)
    bird_beak(bird, c + 0.25, "closed")
    bird_eyes(bird, c + 0.4, "open")
ry(bird.head, LUMO_LINE3[0], 18)
ry(bird.head, LUMO_LINE3[0] + 0.4, -10)
ry(bird.head, LUMO_LINE3[1] - 0.8, 20)
# bay đi: nhún lấy đà, quay sang trái, vỗ cánh bay lên
f0, f1 = BIRD_FLY
at(bird.root, f0, BIRD_X, BIRD_Z)
scl(bird.root, f0, 1, 1)
scl(bird.root, f0 + 0.1, 1.12, 0.85)
scl(bird.root, f0 + 0.18, -1, 1)
bird.dir = -1
for t, x, z in ((f0 + 0.18, BIRD_X, BIRD_Z + 0.02), (f0 + 0.35, BIRD_X - 0.25, BIRD_Z + 0.25), (f0 + 0.55, BIRD_X - 0.75, BIRD_Z + 0.55),
                (f1, BIRD_X - 1.6, BIRD_Z + 1.1), (f1 + 0.1, -5.0, 6.0)):
    at(bird.root, t, x, z)
for i, t in enumerate(steps(f0 + 0.15, f1, 0.06)):
    ry(bird.wing, t, 65 if i % 2 else -35)
    ry(bird.wing_far, t, 70 if i % 2 else -30)

# ================================================================ Lumo: chống chế với chú chim
fc(lumo, BIRD_TILT[0], "eager")
look(lumo, BIRD_LAUGH[0] + 0.3, 0.6, 0.9)                       # nghe CHÍP, ngước nhìn chú chim
ry(lumo.head, BIRD_LAUGH[0] + 0.2, 0)
ry(lumo.head, BIRD_LAUGH[0] + 0.5, -16)
y0, y1 = LUMO_SHY                                               # bị cười: cụp tai, rụt vai, liếc đi chỗ khác rồi liếc lại chim
ry(lumo.head, y0, -16)
fc(lumo, y0 + 0.1, "sheepish", -6)
ears(lumo, y0, 2)
ears(lumo, y0 + 0.35, -50)
ry(lumo.head, y0 + 0.35, -6)
squash(lumo, y0 + 0.1, 1, 1)
squash(lumo, y0 + 0.35, 1.05, 0.94)
look(lumo, y0 + 0.4, -0.6, -0.4)
look(lumo, y1 - 0.5, 0.6, 0.9)
ry(lumo.head, y1 - 0.5, -6)
ry(lumo.head, y1 - 0.2, -14)
squash(lumo, y1 - 0.1, 1.05, 0.94)
ry(lumo.tail, y0, 14)
ry(lumo.tail, y0 + 0.4, -15)                                    # đuôi rủ
# ưỡn ngực, dựng thẳng tai
u0, u1 = LUMO_PUFF
lean(lumo, u0, 0)
lean(lumo, u1, -9)
squash(lumo, u0 + 0.15, 1.0, 1.0)
squash(lumo, u1, 0.98, 1.04)
ears(lumo, u0, -50)
ears(lumo, u0 + 0.2, 12)
ears(lumo, u1, 0)
ry(lumo.head, u0, -14)
ry(lumo.head, u1, -12)                                          # hếch cằm
fc(lumo, u0 + 0.1, "happy", -12)
ry(lumo.tail, u0, -15)
ry(lumo.tail, u1, 35)
# gấp bản đồ nhét vào túi da
m0, m1 = MAP_STOW
hold(m0, -45)
scl(map_sheet, m0, 1, 1)
scl(map_sheet, m0 + 0.35, 0.5, 0.55)                            # gấp lại
scl(map_sheet, m0 + 0.6, 0.35, 0.35)
hold(m0 + 0.35, -50, -6)
hold(m0 + 0.65, -15, -6)                                        # tay đưa xuống túi ở hông
show(map_sheet, m0 + 0.7, False)
ry(lumo.arm, m1, 6)
ry(map_hold, m1, -6)
look(lumo, m0, 0.4, -0.9)                                       # liếc xuống túi
look(lumo, m1, 0.5, 0.6)
# "Mình biết chứ! Đang kiểm tra bản đồ thôi!"
e0, e1 = LUMO_LINE3
fc(lumo, e0 - 0.05, "happy", -12)
talk(lumo, e0, e0 + 0.8, "smile")                               # "Mình biết chứ!"
talk(lumo, e0 + 1.0, e1, "smile")                               # "Đang kiểm tra bản đồ thôi!"
for t, a in ((e0, -12), (e0 + 0.25, -4), (e0 + 0.5, -14), (e0 + 1.0, -12)):
    ry(lumo.head, t, a)                                         # gật mạnh đầu một cái ở "Mình biết chứ!"
ry(lumo.arm, e0 + 1.4, 6)
ry(lumo.arm, e0 + 1.6, -18)                                     # vỗ vỗ túi da ở "bản đồ"
ry(lumo.arm, e0 + 1.75, -8)
ry(lumo.arm, e0 + 1.9, -18)
ry(lumo.arm, e1, 6)
ry(lumo.head, e1, -12)
lean(lumo, e1, -9)
loop(lumo.tail, u1 + 0.1, e1, 0.5, 26, 42)
# chú chim bay đi: Lumo nhìn theo
fc(lumo, BIRD_FLY[0] + 0.1, "neutral")
look(lumo, BIRD_FLY[0] + 0.1, 0.5, 0.9)
look(lumo, BIRD_FLY[1], 0.2, 1.0)
ry(lumo.head, BIRD_FLY[1], -22)
lean(lumo, BIRD_FLY[0], -9)
lean(lumo, BIRD_FLY[1], 0)
squash(lumo, BIRD_FLY[0], 0.98, 1.04)
squash(lumo, BIRD_FLY[1], 1, 1)
ears(lumo, BIRD_FLY[1], -10)

# ================================================================ Lumo: lại rút bản đồ, sải bước, hụt chân ở mép dốc lá khô
o0, o1 = MAP_OUT
ry(lumo.head, o0, -22)
ry(lumo.head, o1, 18)                                           # cắm mặt vào bản đồ
fc(lumo, o0 + 0.1, "eager", 18)
look(lumo, o1, 0.5, -0.9)
hold(o0, 6, -6)
hold(o0 + 0.15, -15, -6)                                        # rút từ túi ra
show(map_sheet, o0 + 0.18, True)
scl(map_sheet, o0 + 0.18, 0.35, 0.35)
scl(map_sheet, o1, 1, 1)                                        # mở ra
hold(o1, -65)
ears(lumo, o1, -18)
lean(lumo, o1, -3)
st0, st1 = STRIDE
cut = SHOT["S12"][0]
walk(lumo.root, st0, cut - HOLD, 1.7, -0.7, 8, 0.05)            # sải bước thật nhanh ra khỏi khung
at(lumo.root, cut, -1.7, 0)                                     # vào cú S12 từ mép phải
walk(lumo.root, cut, st1, -1.7, -3.92, 6, 0.05)
for i, t in enumerate(steps(st0, st1 - 0.1, 0.25)):
    ry(lumo.head, t, 18 if i % 2 else 14)
loop(lumo.tail, o1, st1, 0.4, 18, 36)
bl(lumo, STRIDE[0] + 1.0)
# hụt chân: WHOOSH! bản đồ tuột tay
x0 = -3.92
fc(lumo, EDGE + 0.05, "shock", 20)
ears(lumo, EDGE + 0.05, 25)
lean(lumo, EDGE, -3)
lean(lumo, EDGE + 0.12, 22)                                     # chúi về trước, chân hụt
at(lumo.root, EDGE, x0, 0)
at(lumo.root, EDGE + 0.12, x0 - 0.18, -0.03)
ry(lumo.head, EDGE + 0.12, 0)
look(lumo, EDGE + 0.12, 0.6, -1.0)
hold(EDGE, -65)
hold(EDGE + 0.06, -140)                                         # hai tay hất lên (không quá ngang tai), bản đồ tuột
show(map_sheet, EDGE + 0.06, False)
mx, mz = hand(lumo, x0, 0.0, -140, 0)
show(map_fly, EDGE + 0.06, True)
for t, x, z, a in ((EDGE + 0.06, mx, mz, 0), (EDGE + 0.4, mx - 0.4, mz + 0.4, 60), (EDGE + 0.9, -5.1, 0.6, -30), (EDGE + 1.5, -5.9, 0.2, 40),
                   (EDGE + 2.1, -6.7, -0.4, -20), (EDGE + 2.5, -7.3, -0.75, 30), (MAP_DRIFT[1], -7.78, -1.04, 75)):
    at(map_fly, t, x, z)                                        # tấm bản đồ chao lượn rồi rơi xuống mép đống lá
    ry(map_fly, t, a)
for i, t in enumerate(steps(EDGE + 0.06, MAP_DRIFT[1] - 0.2, 0.15)):
    scl(map_fly, t, 1.0, 1.0 if i % 2 else 0.6)
scl(map_fly, MAP_DRIFT[1], 1, 1)
lean(lumo, WHOOSH[1] - 0.1, -35)
at(lumo.root, WHOOSH[1] - 0.1, -4.25, -0.06)
# trượt một mạch xuống dốc, ngồi bệt, chân trước: RUSTLE!
sl0, sl1 = SLIDE
END_X = -6.95
for i, t in enumerate(steps(sl0, sl1 - 0.25, 0.1)):
    u = min(1.0, (t - sl0) / (sl1 - 0.25 - sl0)) ** 1.3
    x = -4.45 + (END_X + 4.45) * u
    at(lumo.root, t, x, ground_z(x) + 0.1 + (0.02 if i % 2 else 0.0))
    lean(lumo, t, -55 + (4 if i % 2 else -4))
loop(lumo.arm, sl0, sl1 - 0.1, 0.16, -145, -95)                 # tay chới với
loop(lumo.arm_far, sl0 + 0.08, sl1 - 0.1, 0.16, -145, -95)
loop(lumo.ear_near, sl0, sl1 - 0.1, 0.14, -70, -40)             # tai bay ngược ra sau
loop(lumo.ear_far, sl0 + 0.05, sl1 - 0.1, 0.14, -70, -40)
loop(lumo.tail, EDGE, sl1, 0.12, 30, 60)
fc(lumo, sl0, "shock", -45)
look(lumo, sl0, 0.8, -0.2)
for k, ob in enumerate(bits[10:]):                              # lá khô tung lên dọc đường trượt
    ts = sl0 + 0.2 + 0.22 * k
    x = -4.45 + (END_X + 4.45) * min(1.0, (ts - sl0) / (sl1 - 0.25 - sl0)) ** 1.3
    fly_bit(ob, ts, (x + 0.1, ground_z(x) + 0.05), (x + 0.4, ground_z(x + 0.4) + 0.02), ts + 0.6, 260, 0.3)
# rơi vào đống lá: POOF!
at(lumo.root, sl1 - 0.12, -7.15, LOW_Z + 0.12)
lean(lumo, sl1 - 0.12, -50)
at(lumo.root, POOF, -7.3, LOW_Z - 0.75)                         # lún mất trong đống lá
lean(lumo, POOF, -15)
for ob in (lumo.arm, lumo.arm_far):
    ry(ob, POOF + 0.2, 6)
ry(map_hold, POOF + 0.2, -6)
ears(lumo, POOF + 0.2, -10)
scl(pile, POOF - 0.05, 1, 1)
scl(pile, POOF + 0.05, 1.18, 0.82)
scl(pile, POOF + 0.25, 0.94, 1.1)
scl(pile, POOF + 0.45, 1, 1)
for k, ob in enumerate(bits[:10]):                              # lá tung tóe
    a = math.radians(25 + 13 * k)
    p0 = (-7.3 + 0.2 * math.cos(a), LOW_Z + 0.35)
    p1 = (-7.3 + 0.75 * math.cos(a) + 0.1 * (k % 3), LOW_Z + 0.02 + 0.1 * (k % 2))
    fly_bit(ob, POOF + 0.02 * k, p0, p1, POOF + 1.0 + 0.05 * k, 300 + 30 * k, 0.45 + 0.05 * (k % 3))
show(head_leaf, POOF, True)
fc(lumo, POOF + 0.3, "squint")

# ================================================================ Lumo: ngẩng lên khỏi đống lá, lắc đầu, nhặt bản đồ
POP_Z = LOW_Z - 0.16
at(lumo.root, LUMO_POP - 0.05, -7.3, LOW_Z - 0.75)
at(lumo.root, LUMO_POP + 0.12, -7.3, POP_Z + 0.05)
at(lumo.root, LUMO_POP + 0.25, -7.3, POP_Z)
lean(lumo, LUMO_POP, -10)
lean(lumo, LUMO_POP + 0.25, 0)
ears(lumo, LUMO_POP, -40)
ears(lumo, LUMO_POP + 0.15, 15)                                 # tai bật lên
ears(lumo, LUMO_POP + 0.35, 4)
ry(lumo.head, LUMO_POP + 0.25, 0)
fc(lumo, LUMO_POP + 0.1, "shock")
look(lumo, LUMO_POP + 0.1, 0.3, 0.2)
bl(lumo, LUMO_POP + 0.55)
fc(lumo, LUMO_POP + 0.75, "puzzled")
look(lumo, LUMO_POP + 0.75, 0.2, 1.0)                           # ngước mắt nhìn chiếc lá trên trán
k0, k1 = HEAD_SHAKE2
fc(lumo, k0, "squint")
loop(lumo.head, k0, k1 - 0.05, 0.1, -18, 18)
loop(lumo.ear_near, k0, k1 - 0.05, 0.1, -50, 25)
loop(lumo.ear_far, k0 + 0.03, k1 - 0.05, 0.1, -50, 25)
ry(lumo.head, k1, 0)
ears(lumo, k1, 2)
show(head_leaf, LEAF_FALL[0], False)
show(leaf_fall, LEAF_FALL[0], True)
for t, x, z, a in ((LEAF_FALL[0], -7.42, -0.64, 0), (LEAF_FALL[0] + 0.25, -7.28, -0.6, 40), (LEAF_FALL[0] + 0.5, -7.12, -0.76, -30),
                   (LEAF_FALL[1], -6.98, -0.97, 25)):
    at(leaf_fall, t, x, z)                                      # chiếc lá chao ra sau lưng, nằm trên lưng đống lá
    ry(leaf_fall, t, a)
fc(lumo, k1, "neutral")
look(lumo, k1 + 0.3, 0.8, -0.7)                                 # thấy tấm bản đồ rơi cạnh đó
bl(lumo, k1 + 0.45)
n0, n1 = MAP_PICK
PICK_Z, PICK_LEAN = LOW_Z - 0.03, 30
at(lumo.root, n0, -7.3, POP_Z)
at(lumo.root, n0 + 0.2, -7.3, PICK_Z)
lean(lumo, n0, 0)
lean(lumo, n0 + 0.25, PICK_LEAN)
target = (-7.75, -1.0)
a_pick = reach(lumo, -7.3, PICK_Z, PICK_LEAN, target)
hold(n0, 6, -6)
hold(n0 + 0.3, a_pick, a_pick + 5)
key(lumo.arm, "location", n0, (0.03, -0.02, 0.46))
key(lumo.arm, "location", n0 + 0.05, (0.03, -0.22, 0.46))       # tay vươn qua mặt đống lá (lên lớp trước đống lá)
show(map_fly, n0 + 0.32, False)
show(map_sheet, n0 + 0.32, True)                                # nhặt lên
ry(lumo.head, n0 + 0.25, 10)
fc(lumo, n0 + 0.2, "eager", 40)
look(lumo, n0 + 0.2, 0.8, -0.8)
v0, v1 = MAP_STOW2
lean(lumo, v0, PICK_LEAN)
lean(lumo, v0 + 0.25, 0)
at(lumo.root, v0, -7.3, PICK_Z)
at(lumo.root, v0 + 0.25, -7.3, POP_Z)
hold(v0, a_pick, a_pick + 5)
hold(v0 + 0.3, -15, -6)                                         # nhét vào túi da (lút trong đống lá)
scl(map_sheet, v0, 1, 1)
scl(map_sheet, v0 + 0.25, 0.4, 0.4)
show(map_sheet, v0 + 0.3, False)
key(lumo.arm, "location", v0 + 0.3, (0.03, -0.22, 0.46))
key(lumo.arm, "location", v0 + 0.32, (0.03, -0.02, 0.46))      # tay về sau đống lá, chỗ túi da
ry(lumo.arm, v1, 6)
ry(map_hold, v1, -6)
ry(lumo.head, v1, 0)
fc(lumo, v1, "happy")
look(lumo, v1, 0.0, 0.0)

# ================================================================ phế tích: bướm đậu phiến đá rêu, ánh vàng le lói
# bướm bay lượn quanh các tán cây (S1, S8), một con quanh dốc lá và phế tích, đậu xuống phiến đá rêu
drift(bflies[0], 0.0, SECONDS, -1.0, 1.8, 2.2, 0.35, 0.3)
drift(bflies[1], 0.0, SECONDS, -1.9, 1.35, 0.6, 0.2, 0.5, 2.0)
drift(bflies[2], 0.0, SECONDS, -0.6, 0.75, 1.6, 0.18, 0.25, 4.0)
for f in bflies[:3]:
    flap(f, 0.0, SECONDS)
hero = bflies[3]
drift(hero, 0.0, BFLY_LAND[0] - 0.4, -8.6, 0.1, 0.5, 0.18, 0.4, 1.0)
l0, l1 = BFLY_LAND
STONE_TOP = (-8.03, LOW_Z + 0.215)
for t, x, z in ((l0 - 0.2, -8.7, -0.25), (l0 + 0.25, -8.35, -0.55), (l0 + 0.5, -8.1, -0.85), (l1, *STONE_TOP)):
    at(hero.root, t, x, z)
scl(hero.root, l0 - 0.2, 1, 1)
flap(hero, 0.0, l1)
flap(hero, l1, SECONDS, 0.9, 0.55)                              # đậu: cánh dựng lên, khép mở chậm
at(hero.root, SECONDS, *STONE_TOP)
fc(lumo, l0, "eager")
look(lumo, l0, 0.6, 0.6)
look(lumo, l0 + 0.4, 0.8, 0.0)
look(lumo, l1, 0.8, -0.6)                                       # nhìn con bướm đậu ngay trước mặt
ry(lumo.head, l1, 10)
bl(lumo, l1 + 0.6)
ry(lumo.head, CAM_REVEAL[0], 10)
ry(lumo.head, CAM_REVEAL[0] + 0.4, 0)
look(lumo, CAM_REVEAL[0] + 0.4, 1.0, -0.3)                      # nhìn qua con bướm, về phía phế tích
fc(lumo, LUMO_WONDER, "wonder")
ears(lumo, LUMO_WONDER - 0.05, 4)
ears(lumo, LUMO_WONDER + 0.12, 16)
ears(lumo, LUMO_WONDER + 0.3, 8)
at(lumo.root, LUMO_WONDER - 0.05, -7.3, POP_Z)
at(lumo.root, LUMO_WONDER + 0.25, -7.3, POP_Z + 0.06)           # nhổm lên trong đống lá
bl(lumo, LUMO_WONDER + 1.2)
show(glint, 0.0, False)
twinkle(glint, GOLD_GLOW[0], SECONDS, 1.4, 0.6, 0.35)          # ánh vàng le lói giữa những phiến đá
show(glow, 0.0, False)
show(glow, GOLD_GLOW[0], True)                                  # ánh vàng chỉ hiện khi máy lùi ra, sau con bướm
scl(glow, GOLD_GLOW[0], 0.3, 0.3)
for i, t in enumerate(steps(GOLD_GLOW[0] + 0.3, SECONDS, 0.6)):
    scl(glow, t, 1.0 if i % 2 else 0.85, 1.0 if i % 2 else 0.85)

# ================================================================ cú cận bản đồ (S2, S6)
for i, t in enumerate(steps(SHOT["S2"][0], SHOT["S2"][1], 0.3)):   # nhún theo bước, đường trôi xuống
    at(insert_hold, t, IX + (0.01 if i % 2 else -0.01), 0.03 + (0.012 if i % 2 else -0.012))
at(insert_hold, SHOT["S6"][0], IX, 0.03)
at(insert_scroll, SHOT["S2"][0], IX, 0.0)
at(insert_scroll, SHOT["S2"][1], IX, -0.75)
ry(insert_map, 0.0, 180)                                        # cầm ngược: mũi tên chỉ lên, về phía trước
ry(insert_map, SHOT["S6"][0], 180)
ry(insert_map, MAP_TURN[0], 180)
ry(insert_map, MAP_TURN[1], 360)                                         # xoay nửa vòng: mũi tên chỉ xuống, về phía Lumo
for side, paw in zip((-1, 1), paws):
    at(paw, MAP_TURN[0] - 0.1, side * 0.33, -0.27)
    at(paw, MAP_TURN[0] + 0.05, side * 0.45, -0.32)             # buông ra để xoay
    at(paw, MAP_TURN[1] - 0.05, side * 0.45, -0.32)
    at(paw, MAP_TURN[1] + 0.12, side * 0.33, -0.27)

# --- tên phim
for ob in title:
    show(ob, TITLE[0], True)
    show(ob, TITLE[1], False)

# ================================================================ máy quay, render
CAMS = {"S1": (0.4, 1.45, 7.2), "S2": (IX, 0.0, 1.5), "S3": (1.95, 0.48, 2.4), "S4": (2.5, 0.85, 4.0), "S5": (1.95, 0.66, 1.6),
        "S6": (IX, 0.0, 1.5), "S7": (1.75, 0.66, 1.6), "S8": (-1.1, 1.46, 7.4), "S9": (1.45, 1.33, 0.75), "S10": (1.55, 0.773, 2.3),
        "S11": (1.0, 0.59, 3.0), "S12": (-4.9, -0.1, 6.2), "S13": (-7.45, -0.9, 1.9),
        "S14": (-7.75, -0.98, 1.3)}                            # tâm X, tâm Z, bề ngang khung (m); đáy khung chừa cho CC
cameras(SHOTS, CAMS)
cam = bpy.data.objects["Cam_S14"]                               # S14: máy lùi ra, lộ phế tích và ánh vàng sau con bướm
for t, (cx, cz, w) in ((CAM_REVEAL[0], CAMS["S14"]), (CAM_REVEAL[1], (-8.3, -0.5, 4.2))):
    key(cam, "location", t, (cx, -10.0, cz))
    key(cam.data, "ortho_scale", t, w)
finish(SECONDS, OUT_BLEND, (1.0, 2.8, 4.3, 5.8, 7.5, 9.2, 10.8, 11.6, 12.5, 14.0, 14.8, 16.6, 17.9, 19.9, 22.3, 23.9, 25.0,
                            26.0, 27.0, 28.5, 30.3, 32.5, 34.8, 35.7, 36.5, 37.6, 38.6, 39.8, 40.8, 41.9, 42.6, 44.0, 45.8, 47.5))
