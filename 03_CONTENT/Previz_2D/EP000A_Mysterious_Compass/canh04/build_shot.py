"""
EP000A Cảnh 4 (Cây cầu sập): previz 2D cutout (03_CONTENT/PREVIZ_2D.md, bộ nhân vật pipeline/cutout.py).
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #4#. Mốc thời gian và CC: timing.py; mọi
keyframe tính từ các mốc đó (cộng trừ vài phần mười giây cho nhịp lấy đà, giữ tư thế).
    pipeline/run.sh build -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh04
    pipeline/run.sh preview -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh04
    blender -b --factory-startup -P pipeline/cc.py -- <cảnh>/renders/canh04_preview.mp4 <cảnh>/timing.py <cảnh>/renders/canh04_preview_cc.mp4
Bố cục: mặt cắt ngang khe núi (X, mét; Z = 0 là mặt cầu). Vách trái có cánh cửa đá khắc mây (tâm X -0.75, quay mặt
ra máy theo lối vẽ cắt cảnh); bậc cửa phủ rêu tới X 0.9, bụi cây bên cạnh cửa ở 0…0.8 che chân lối nhỏ. Cầu ván cổ
0.9…5.84 (26 tấm ván, 10 cột, thành cầu ngang ngực Lumo); lưới dây leo dưới mặt cầu khoảng một tầm người (mép trước
Z -0.8…-1.05), mặt lưới dâng dần về phía vách sau tới chân lối nhỏ. Lối nhỏ men vách sau (đầu khe núi): 5 bậc lên từ
X 0.15, gờ phẳng Z 0.9 từ 1.65 tới 4.6, 5 bậc xuống tới bãi đất bên phải ở 6.1. Bệ đá 6.75…7.45, mặt bệ cao 0.45 (ngang
ngực Lumo) nhìn chếch, ngôi sao đá ở trái mặt bệ, bản đồ khắc ở phải; sau bệ là chân trời biển mây (bờ có rặng cây).
Cú cận la bàn sau vai (S4, S11) là la bàn to đặt trước cảnh, chỉ hiện trong cú của nó; cú cận mặt bệ nhìn từ trên
(S17, S19, S21) dựng riêng ở X = 60.
Mũi sao của mọi la bàn được ngắm sau khi diễn xong bằng aim() của cutout: đọc ma trận thế giới của vỏ la bàn từng khung
rồi xoay mũi sao về mục tiêu (ngôi sao đá, đảo khắc, chân trời), nên tay xoay, người nghiêng hay lật gương đều tự bù.
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
from cutout import *  # noqa: E402,F403  bộ cutout: keyframe, hình, mặt, nhân vật, la bàn, chim, máy quay
from timing import *  # noqa: E402,F403  FPS, SECONDS, SHOTS, mốc hành động, CC của cảnh

OUT_BLEND = HERE / f"{HERE.name}.blend"
start(FPS)
SHOT = {name: (t0, t1) for name, t0, t1 in SHOTS}
HOLD = 1.0 / FPS                                                # một khung hình: key giữ đặt sớm hơn đúng một khung
FACES["focus"] = ("open", "closed", 12)                         # nhìn kỹ: mắt mở, mày hạ nhẹ
FACES["calm"] = ("open", "smile", 8)                            # bình tĩnh, mỉm cười
random.seed(4)


def squeeze(shapes, cx, cz, sx, sz):
    """Ép một bộ hình nhìn thẳng thành mặt nằm ngang nhìn chếch (mặt bệ, bản đồ khắc trong cú ngang)."""
    return [([(cx + x * sx, cz + z * sz) for x, z in pts], col) for pts, col in shapes]


def cloud(cx, cz, s):
    """Đám mây khắc: ba vòm tròn trên một đế phẳng, rộng khoảng 0.3 * s."""
    return [ell(0.075 * s, 0.06 * s, cx - 0.075 * s, cz), ell(0.095 * s, 0.08 * s, cx + 0.005 * s, cz + 0.035 * s),
            ell(0.07 * s, 0.055 * s, cx + 0.085 * s, cz), rrect(0.3 * s, 0.07 * s, 0.035 * s, cx + 0.005 * s, cz - 0.03 * s)]


def pos(ob, t, x, z, y=None):
    key(ob, "location", t, (x, ob.location.y if y is None else y, z))


# ================================================================ bối cảnh
SKY, CLOUD = "#CDE9F7", "#F1F6FA"
STONE, STONE_D, STONE_L = "#C9BBA2", "#A8987E", "#D9CCB4"     # đá phế tích như Cảnh 1
ROCK, ROCK_D, ROCK_L, BACK = "#BFA88F", "#B39A81", "#CDB9A0", "#C9B9A4"
MOSS, VINE, LEAF, LEAF_L = "#86B24C", "#5E9437", "#7DB843", "#A3D45E"
WOOD, WOOD_D, ROPE = "#B9834F", "#8B5E3C", "#9C7A4E"
STAR_STONE = "#EAD9AE"                                          # ngôi sao đá sáng màu hơn mặt bệ, như ảnh bệ đá

BRIDGE = (0.9, 5.84)
PLANK_W, PITCH = 0.17, 0.19
PLANKS = [BRIDGE[0] + PITCH * i for i in range(26)]             # mép trái từng tấm ván
POSTS = [0.96 + 0.54 * k for k in range(10)]                    # cột thành cầu; 0, 1 sát cửa, 8, 9 bên kia
RAIL_Z, POST_TOP = 0.45, 0.55
CREAK_PLANK, FALL = 3, range(4, 22)                             # tấm ván bật lên; dãy ván rơi (1.66…5.06)
FALL_POSTS = range(2, 8)
LEDGE_Z, LEDGE_END = 0.9, 4.6                                   # gờ phẳng của lối nhỏ


def net_z(x):
    """Mép trước của lưới dây leo dưới cầu: buộc vào hai vách ở Z -0.8, võng xuống -1.05 giữa khe."""
    u = min(1.0, max(0.0, (x - BRIDGE[0]) / (BRIDGE[1] - BRIDGE[0])))
    return -0.8 - 0.25 * math.sin(math.pi * u)


def path_z(x):
    """Mặt lối nhỏ: 5 bậc lên (rộng 0.3, cao 0.15) từ X 0.15, gờ phẳng tới 4.6, 5 bậc xuống tới bãi đất ở 6.1."""
    if x < 0.15 or x >= LEDGE_END + 1.5:
        return 0.0
    if x < 1.65:
        return 0.15 * math.ceil((x - 0.15) / 0.3 + 1e-9)
    if x < LEDGE_END:
        return LEDGE_Z
    return LEDGE_Z - 0.15 * math.ceil((x - LEDGE_END) / 0.3 + 1e-9)


PROFILE = [(0.15, 0.0)]
for k in range(1, 6):
    PROFILE += [(0.15 + 0.3 * (k - 1), 0.15 * k), (0.15 + 0.3 * k, 0.15 * k)]
PROFILE += [(LEDGE_END, LEDGE_Z)]
for k in range(1, 6):
    PROFILE += [(LEDGE_END + 0.3 * (k - 1), LEDGE_Z - 0.15 * k), (LEDGE_END + 0.3 * k, LEDGE_Z - 0.15 * k)]
PROFILE += [(LEDGE_END + 1.8, 0.0)]                              # mặt bậc nhìn ngang, từ chân bậc trái tới bãi đất phải

# --- trời, đảo xa, biển mây (chân trời bên phải để trống: hòn đảo thật còn ẩn trong mây tới Cảnh 5)
part("Sky", None, [(rect(-6, -6, 70, 8), SKY)], 4.0)
part("SkyClouds", None, [(ell(0.5, 0.17, cx, cz), "#F7FBFD") for cx, cz in ((-1.5, 3.2), (-0.9, 3.3), (2.2, 3.05), (2.8, 3.15),
                                                                          (7.0, 2.6), (7.6, 2.7), (10.2, 2.2), (11.0, 2.3))], 3.9)
islands = []
for cx, cz, s in ((1.2, 2.75, 0.6), (3.6, 3.0, 0.4), (-2.0, 2.4, 0.5), (5.4, 2.6, 0.32)):
    rock = [(cx - 0.55 * s, cz), (cx + 0.55 * s, cz), (cx + 0.42 * s, cz - 0.22 * s), (cx + 0.2 * s, cz - 0.42 * s), (cx, cz - 0.62 * s),
            (cx - 0.22 * s, cz - 0.45 * s), (cx - 0.45 * s, cz - 0.25 * s)]
    islands += [(rock, "#B48E72"), (ell(0.58 * s, 0.1 * s, cx, cz), "#93C95A")]
    islands += [(ell(0.13 * s, 0.12 * s, cx + dx * s, cz + 0.16 * s), col) for dx, col in ((-0.3, "#7DB843"), (0.05, "#86C04E"), (0.32, "#F2B3CB"))]
    islands += [(rect(cx + 0.28 * s, 1.0, cx + 0.38 * s, cz - 0.02), "#E4F5FF")]
part("Islands", None, islands, 3.6)
part("CloudSea", None, [(rect(-6, -6, 70, 0.8), CLOUD)] + [(ell(0.55, 0.22, -6 + 0.75 * i, 0.8 + 0.05 * (i % 3)), CLOUD) for i in range(100)]
     + [(ell(0.9, 0.42, cx, 1.0), "#FAFCFE") for cx in (9.0, 10.4, 12.0, 13.8, 15.4)], 3.5)

# --- vách sau (đầu khe núi): lối nhỏ lùi vào vách, tay vịn dây leo, gờ đá thấp
BACK_TOP = [(0.0, 2.35), (1.0, 2.3), (2.2, 2.45), (3.4, 2.3), (4.6, 2.4), (5.8, 2.1), (6.35, 1.5), (6.55, 0.6), (6.6, -0.3)]
part("BackWall", None, [([(0.0, -1.5)] + BACK_TOP + [(6.6, -1.5)], BACK)]
     + [(ell(rx, rz, cx, cz), col) for rx, rz, cx, cz, col in ((0.6, 0.3, 1.0, 2.0, "#BFAE98"), (0.7, 0.25, 3.0, 2.1, "#BFAE98"),
                                                             (0.5, 0.25, 5.0, 1.95, "#D3C4AF"))]
     + [(ell(0.45, 0.13, x, z + 0.04), LEAF) for x, z in BACK_TOP[:5]] + [(ell(0.3, 0.12, 5.8, 2.12), "#86C04E")]
     + [(band([(x, 2.3), (x + 0.04, 1.95), (x - 0.02, 1.7)], 0.03), VINE) for x in (0.7, 2.6, 4.1, 5.5)], 1.6)
recess = [(x, z + 0.04) for x, z in PROFILE] + [(x, z + 0.75) for x, z in reversed(PROFILE)]
part("PathRecess", None, [(recess, "#A39079")], 1.55)            # vệt lõm tối trong vách: lối nhỏ lùi sâu vào trong
stone = [(x, z) for x, z in PROFILE] + [(x, z - 0.14) for x, z in reversed(PROFILE)]
part("PathStone", None, [(stone, STONE_L)] + [(rect(x0 - 0.006, z0 - 0.14, x0 + 0.006, z0), STONE_D) for x0, z0 in PROFILE[2:-1:2]],
     0.95)
RAIL_PTS = [(x, z + 0.44) for x, z in PROFILE[::2]] + [(PROFILE[-1][0], 0.44)]
handrail = [(band(RAIL_PTS, 0.04), "#5E8F35")]
handrail += [(rrect(0.028, 0.14, 0.01, x, z + 0.41), WOOD_D) for x, z in PROFILE[1::4]]   # cọc giữ tay vịn
handrail += [(leaf_pts(x + 0.05, z + 0.47, 1.8, 30 * (i % 2 * 2 - 1)), LEAF) for i, (x, z) in enumerate(PROFILE[::2])]
part("Handrail", None, handrail, 1.0)
lip = [(x, z + 0.06) for x, z in PROFILE] + [(x, z - 0.02) for x, z in reversed(PROFILE)]
part("PathLip", None, [(lip, STONE)] + [(ell(0.08, 0.025, x + 0.1, z + 0.06), MOSS) for x, z in PROFILE[3::4]], 0.7)

# --- lưới dây leo: mặt lưới dâng từ mép trước (dưới cầu) lên chân lối nhỏ, mắt lưới dẹt dần về phía vách (xa);
# dưới mép trước là khối dây leo dày, không thấy đáy
XS = [BRIDGE[0] + (BRIDGE[1] - BRIDGE[0]) * i / 60 for i in range(61)]


def net_surf(x, v):
    """Điểm trên mặt lưới: v = 0 ở mép trước, v = 1 ở chân lối nhỏ."""
    zb, zt = net_z(x), path_z(x) - 0.13
    return zb + (zt - zb) * (1 - (1 - v) ** 1.8)


top = [(x, z - 0.13) for x, z in PROFILE if BRIDGE[0] < x < BRIDGE[1]]
net_back = ([(BRIDGE[0], net_z(BRIDGE[0])), (BRIDGE[0], path_z(BRIDGE[0]) - 0.13)] + top
            + [(BRIDGE[1], path_z(BRIDGE[1]) - 0.13), (BRIDGE[1], net_z(BRIDGE[1]))] + [(x, net_z(x)) for x in reversed(XS)])
near = [(x, net_z(x)) for x in XS] + [(x, net_surf(x, 0.45)) for x in reversed(XS)]
mesh = []
for d in (-1, 1):                                               # hai họ dây chéo: mắt lưới hình thoi
    for k in range(-8, 40):
        run = []
        for j in range(13):
            v = j / 12
            x = BRIDGE[0] + 0.24 * k + d * 1.1 * v
            if BRIDGE[0] + 0.01 < x < BRIDGE[1] - 0.01:
                run.append((x, net_surf(x, v), v))
            elif run:
                break
        for (x0, z0, v0), (x1, z1, v1) in zip(run, run[1:]):
            mesh.append((band([(x0, z0), (x1, z1)], 0.022 - 0.012 * v0), "#CFE2A2"))
for v, th in ((0.12, 0.02), (0.35, 0.016), (0.62, 0.012)):      # vài hàng dây ngang
    mesh.append((band([(x, net_surf(x, v)) for x in XS], th), "#CFE2A2"))
net_leaves = []
for k in range(80):
    x, v = random.uniform(BRIDGE[0] + 0.1, BRIDGE[1] - 0.1), random.random()
    net_leaves.append((leaf_pts(x, net_surf(x, v), 1.8 - 0.8 * v, random.uniform(-60, 60)), LEAF if k % 2 else LEAF_L))
part("NetBack", None, [(net_back, "#6F9650"), (near, "#7FA85A")] + mesh + net_leaves, 1.3)
net_front = node("NetFront", None, ((BRIDGE[0] + BRIDGE[1]) / 2, -0.8), 0.6)   # khớp ở chỗ buộc; lưới nảy thì giãn Z
NX = (BRIDGE[0] + BRIDGE[1]) / 2
deep = [(x - NX, net_z(x) + 0.8) for x in XS] + [(BRIDGE[1] - NX, -4.2), (BRIDGE[0] - NX, -4.2)]
hang = []
for k, x in enumerate(XS[1:-1:2]):                              # dây leo buông xuống từ mép lưới, dài ngắn khác nhau
    z0 = net_z(x) + 0.78
    length = 0.35 + 0.3 * ((k * 7) % 5) / 4
    pts = [(x - NX + 0.03 * math.sin(3 * j + k), z0 - length * j / 6) for j in range(7)]
    hang += [(band(pts, 0.022), "#4F8030")] + [(leaf_pts(px + 0.03, pz, 1.7, 40 * (j % 2 * 2 - 1)), LEAF) for j, (px, pz) in enumerate(pts[2::2])]
clumps = [(ell(random.uniform(0.18, 0.3), random.uniform(0.1, 0.16), x - NX, net_z(x) + 0.8 - random.uniform(0.5, 1.1)), "#668F41")
          for x in (BRIDGE[0] + 0.4 * i + 0.2 for i in range(13))]
edge = [(band([(x - NX, net_z(x) + 0.8) for x in XS], 0.055), "#C7DC97")]
edge += [(arc(0.06, 200, 340, 0.018, x - NX, net_z(x) + 0.8 + 0.01), "#C7DC97") for x in XS[1:-1:2]]   # mép võng có vòng dây
edge += [(leaf_pts(x - NX, net_z(x) + 0.82, 1.9, 30 * (i % 3 - 1)), LEAF_L) for i, x in enumerate(XS[::3])]
part("NetFront_Shape", net_front, [(deep, "#5F8A3E")] + clumps + hang + edge)

# --- vách trái có cánh cửa đá khắc mây, bậc cửa phủ rêu; vách phải và bãi đất có bệ đá
DX, DW, DJ = -0.75, 0.74, 1.0                                   # tâm cửa, bề rộng lỗ cửa, chiều cao thân cửa (vòm ở trên)


def door_shape(w, h, cx=0.0):
    r = w / 2
    return [(cx - r, 0.0), (cx + r, 0.0)] + [(cx + r * math.cos(math.radians(a)), h + r * math.sin(math.radians(a))) for a in range(0, 181, 10)]


LCLIFF = [(-6, -4.5), (BRIDGE[0], -4.5), (BRIDGE[0], -0.2), (BRIDGE[0] - 0.05, 0.0), (0.05, 0.0), (0.05, 0.6), (0.1, 1.4), (0.0, 2.2),
          (0.15, 2.9), (0.0, 3.6), (-6, 3.6)]
LINTEL = [(DX, DJ + 0.46, 0.7), (DX - 0.42, DJ + 0.1, 0.42), (DX + 0.43, DJ + 0.1, 0.42)]      # mây khắc trên khung cửa
part("CliffLeft", None, [(LCLIFF, ROCK)] + [(ell(rx, rz, cx, cz), col) for rx, rz, cx, cz, col in
                                           ((0.5, 0.6, -2.2, 0.9, ROCK_D), (0.6, 0.5, -1.6, 2.7, ROCK_D), (0.35, 0.4, -0.25, 2.3, ROCK_L),
                                            (0.4, 0.3, -2.6, 2.1, ROCK_L), (0.3, 0.6, 0.4, -1.6, ROCK_D))]
     + [(band([(0.08, 2.9), (0.15, 2.3), (0.06, 1.7)], 0.04), VINE), (ell(0.5, 0.15, -0.6, 3.6), LEAF)]
     + [(door_shape(DW + 0.3, DJ, DX), STONE), (door_shape(DW + 0.12, DJ, DX), STONE_D), (door_shape(DW, DJ, DX), "#7D6E5A")]
     + [(s, STONE_D) for c in LINTEL for s in cloud(c[0], c[1], c[2] * 1.15)] + [(s, STONE_L) for c in LINTEL for s in cloud(*c)], 0.2)
lintel_glow = {k: part(f"LintelGlow_{k}", None, [(s, col) for c in LINTEL for s in cloud(*c)], 0.15)
               for k, col in (("bright", "#FFE47A"), ("dim", "#EFE3C2"))}
part("Threshold", None, [(rect(-1.6, -0.2, BRIDGE[0], 0.0), STONE), (rect(-1.6, -0.03, BRIDGE[0], 0.0), STONE_L),
                         (rect(BRIDGE[0] - 0.04, -0.2, BRIDGE[0], 0.0), STONE_D)], 0.05)
moss = [(rrect(1.15, 0.2, 0.08, -0.2, -0.09), MOSS)] + [(ell(0.15, 0.05, x, 0.0), c) for x, c in ((-0.66, "#94C25A"), (-0.38, MOSS),
                                                                                                (-0.08, "#94C25A"), (0.22, MOSS))]
part("ThresholdMoss", None, moss, -0.4)                         # đệm rêu dày trên bậc cửa: che chân khi Lumo ngồi phịch xuống

# cánh cửa: bản lề ở mép trái lỗ cửa; mở về phía máy thì hẹp dần về bản lề
door = node("DoorSlab", None, (DX - DW / 2, 0.0), -0.42)
SLAB_CLOUDS = [(DW / 2, 0.98, 1.45), (DW / 2 - 0.12, 0.52, 1.0), (DW / 2 + 0.13, 0.3, 1.0)]
part("DoorSlab_Shape", door, [(door_shape(DW, DJ, DW / 2), STONE_D), (door_shape(DW - 0.05, DJ - 0.02, DW / 2), STONE_L)]
     + [(s, STONE_D) for c in SLAB_CLOUDS for s in cloud(c[0], c[1], c[2] * 1.15)] + [(s, STONE) for c in SLAB_CLOUDS for s in cloud(*c)])
door_glow = {k: part(f"DoorGlow_{k}", door, [(s, col) for c in SLAB_CLOUDS for s in cloud(*c)], -0.03)
             for k, col in (("bright", "#FFE47A"), ("dim", "#EFE3C2"))}
sparks = [part(f"DoorSpark{i}", None, [(star(0.04, 0, 0, 4, 0.3), "#FFE27A")], -0.5, loc) for i, loc in
          enumerate(((DX - 0.22, 1.12), (DX + 0.3, 0.62), (DX - 0.05, 1.52), (DX + 0.45, 1.2), (DX - 0.45, 1.45)))]

PX0, PX1, PTOP, PDEPTH = 6.75, 7.45, 0.45, 0.26                 # bệ đá; mặt bệ nhìn chếch cao PDEPTH
part("GroundRight", None, [([(BRIDGE[1], 0.0), (14, 0.0), (14, -4.5), (BRIDGE[1], -4.5)], ROCK), (rect(BRIDGE[1], -0.12, 14, 0.0), "#A5CF63"),
                           (rect(BRIDGE[1], -0.03, 14, 0.0), "#B5D97A")]
     + [(ell(0.3, 0.5, BRIDGE[1] + 0.15, -1.5), ROCK_D), (band([(BRIDGE[1] + 0.02, -0.1), (BRIDGE[1] + 0.06, -0.6), (BRIDGE[1], -1.1)], 0.04), VINE)],
     0.05)
part("Hedge", None, [(ell(0.45, 0.34, x, 0.12), "#7DB843" if i % 2 else "#6FA83E") for i, x in enumerate(8.7 + 0.55 * k for k in range(14))]
     + [(ell(0.05, 0.05, x + 0.1, 0.34), "#F2B3CB") for x in (9.0, 10.1, 11.7)], -0.1)
part("Tufts", None, [s for gx in (6.3, 6.5, 7.6, 8.1, -1.3, -1.0) for s in
                     (([(gx - 0.03, 0.0), (gx + 0.03, 0.0), (gx + 0.005, 0.08)], LEAF), ([(gx + 0.01, 0.0), (gx + 0.05, 0.0), (gx + 0.06, 0.06)], LEAF))]
     + [(ell(0.022, 0.022, x, 0.03), c) for x, c in ((6.4, "#F7A8C8"), (7.9, WHITE), (-1.2, "#F7A8C8"))], -0.2)

# --- bụi cây bên cạnh cửa, che chân lối nhỏ; vạch ra thì hai nửa ngả sang hai bên
bush = []
for name, px, blobs in (("BushL", 0.18, ((-0.08, 0.3, 0.26, 0.3), (0.06, 0.62, 0.22, 0.26), (0.0, 0.12, 0.28, 0.15), (0.14, 0.38, 0.18, 0.26))),
                        ("BushR", 0.6, ((-0.06, 0.4, 0.24, 0.3), (0.06, 0.66, 0.2, 0.24), (0.12, 0.2, 0.22, 0.2), (-0.1, 0.78, 0.16, 0.16)))):
    b = node(name, None, (px, 0.0), 0.5)
    part(f"{name}_Shape", b, [(ell(rx, rz, cx, cz), "#6E9F3F" if i % 2 else "#7DB04A") for i, (cx, cz, rx, rz) in enumerate(blobs)]
         + [(leaf_pts(cx + 0.06, cz + 0.1, 2.2, 40 * (i % 3 - 1)), "#94C85E") for i, (cx, cz, rx, rz) in enumerate(blobs)]
         + [(ell(0.022, 0.022, cx - 0.05, cz + 0.05), "#F2B3CB") for cx, cz, rx, rz in blobs[1:2]])
    bush.append(b)

# --- bệ đá bên kia khe: mặt bệ nhìn chếch; ngôi sao đá ở trái, bản đồ khắc ở phải dưới một phiến đá trượt được
STAR_C = (6.9, PTOP + 0.12)
MAP_C, MAP_SX, MAP_SZ = (7.27, PTOP + 0.13), 0.44, 0.3          # bản đồ khắc map_big(stone=True) (rộng 0.78) ép vào mặt bệ

STAR_W = (STAR_C[0], STAR_C[1] + 0.02)                          # mục tiêu của mũi sao trong cú ngang
ISLAND_W = (MAP_C[0] + MAP_OBS[0] * MAP_SX, MAP_C[1] + MAP_OBS[1] * MAP_SZ + 0.01)
HORIZON_W = (60.0, 1.1)
SIDE_TARGETS = (STAR_W, ISLAND_W, HORIZON_W)

TOPBAND = [(PX0, PTOP), (PX1, PTOP), (PX1 + 0.05, PTOP + PDEPTH), (PX0 + 0.05, PTOP + PDEPTH)]
part("Plinth", None, [(rect(PX0, 0.0, PX1, PTOP), STONE), (rect(PX0, 0.0, PX1, 0.05), STONE_D)]
     + [(s, STONE_D) for s in cloud((PX0 + PX1) / 2, 0.22, 1.25)] + [(s, STONE_L) for s in cloud((PX0 + PX1) / 2 + 0.005, 0.225, 1.05)]
     + [(ell(0.09, 0.03, PX0 + 0.08, PTOP - 0.02), MOSS), (ell(0.06, 0.025, PX1 - 0.05, 0.05), MOSS), (TOPBAND, STONE_L)], 0.3)
# part() dời mỗi hình về phía máy 0.0005: bản đồ khắc có vài chục hình, nên phiến che, phiến sao đặt hẳn trước nó
side_map = part("Plinth_Map", None, squeeze(map_big(stone=True), *MAP_C, MAP_SX, MAP_SZ), 0.25)
SLAB_X = 7.08                                                   # ranh giữa phiến sao (trái) và bản đồ (phải)
part("Plinth_StarSlab", None, [([(PX0, PTOP), (SLAB_X, PTOP), (SLAB_X + 0.05, PTOP + PDEPTH), (PX0 + 0.05, PTOP + PDEPTH)], "#D2C4AB")]
     + squeeze([(arc(0.15, 0, 360, 0.02), STONE_D)], *STAR_C, 1.0, 0.55), 0.19)
cover = node("Plinth_Cover", None, (0.0, 0.0), 0.2)            # phiến đá che bản đồ khắc, trượt sang trái vào dưới phiến sao
part("Plinth_CoverShape", cover, [([(SLAB_X + 0.01, PTOP + 0.005), (PX1 - 0.01, PTOP + 0.005), (PX1 + 0.04, PTOP + PDEPTH - 0.005),
                                    (SLAB_X + 0.06, PTOP + PDEPTH - 0.005)], STONE), (rect(SLAB_X + 0.02, PTOP + 0.005, SLAB_X + 0.035, PTOP + 0.2), STONE_D)])
pstar = node("Plinth_Star", None, STAR_C, 0.18)                # ngôi sao nổi như cái nút; ấn thì lún xuống
part("Plinth_StarShape", pstar, squeeze([(rose(0.15), STONE_D)], 0.0, -0.03, 1.0, 0.55)
     + squeeze([(rose(0.145), STAR_STONE), (ell(0.02, 0.02), STONE)], 0.0, 0.0, 1.0, 0.55))
click = part("Plinth_Click", None, [(band([(0, 0.0), (dx, dz)], 0.012), WHITE) for dx, dz in ((-0.12, 0.06), (0.0, 0.12), (0.12, 0.06))],
             0.05, (STAR_C[0], STAR_C[1] + 0.06))
side_flash = part("Plinth_Flash", None, squeeze(map_obs_glow(TEAL, TEAL_L), 0.0, 0.0, MAP_SX * 1.3, MAP_SZ * 1.6), 0.05, ISLAND_W)

# ================================================================ cầu ván cổ: ván, cột, thành cầu dây leo
planks = []
for i, x0 in enumerate(PLANKS):
    pivot = node(f"Plank{i}", None, (x0, 0.0), 0.0)
    part(f"Plank{i}_Shape", pivot, [(rrect(PLANK_W, 0.07, 0.012, PLANK_W / 2, -0.035), WOOD),
                                    (rect(0.0, -0.07, PLANK_W, -0.055), WOOD_D), (ell(0.008, 0.008, 0.03, -0.02), "#8C8C8C")])
    planks.append(pivot)
halves = [part(f"PlankHalf{k}", None, [(rrect(PLANK_W / 2, 0.07, 0.012, (-1) ** k * PLANK_W / 4, -0.035), WOOD)], -0.01,
               (PLANKS[FALL[0]] + PLANK_W / 2, 0.0)) for k in (1, 0)]     # tấm ván trước mũi chân gãy làm hai
posts = {}
for side, y, col in (("near", -0.6, WOOD), ("far", 0.3, "#A9774A")):
    for k, x in enumerate(POSTS):
        pv = node(f"Post_{side}{k}", None, (x, 0.0), y)
        part(f"Post_{side}{k}_Shape", pv, [(rrect(0.075, 0.62, 0.02, 0, -0.07 + 0.31), col), (ell(0.04, 0.012, 0, POST_TOP), WOOD_D),
                                            (band([(-0.04, 0.38), (0.04, 0.43), (-0.04, 0.48)], 0.02), VINE)])
        posts[side, k] = pv


def rail_shape(p0, p1, sag):
    pts = curve(p0, ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - sag), p1, 16)
    return ([(band(pts, 0.035), ROPE), (band([(x, z + 0.012 * math.sin(9 * x)) for x, z in pts], 0.018), VINE)]
            + [(leaf_pts(x, z + 0.02, 1.5, 35 * (i % 2 * 2 - 1)), LEAF) for i, (x, z) in enumerate(pts[2:-1:4])])


rails = {}
for side, y in (("near", -0.61), ("far", 0.29)):
    for k in range(9):
        rails[side, k] = part(f"Rail_{side}{k}", None, rail_shape((POSTS[k], RAIL_Z), (POSTS[k + 1], RAIL_Z), 0.03), y)
    rails[side, "droop"] = part(f"Rail_{side}_Droop", None, rail_shape((POSTS[1], RAIL_Z), (POSTS[8], RAIL_Z), 0.75), y)

# ================================================================ cận mặt bệ nhìn từ trên (S17, S19, S21), dựng riêng ở X = 60
TX = 60.0
TMAP = (TX + 0.25, 0.36)                                        # bản đồ khắc
TSTAR = (TX - 0.62, 0.36)                                       # ngôi sao đá
PMAP = (TX + 0.25, -0.34)                                       # bản đồ giấy Lumo cầm, ngay dưới (phía Lumo)
part("Top_Slab", None, [(rrect(2.9, 2.2, 0.12, TX + 0.1, 0.1), STONE_D), (rrect(2.8, 2.1, 0.1, TX + 0.1, 0.1), STONE_L)]
     + [(ell(rx, rz, cx, cz), MOSS) for rx, rz, cx, cz in ((0.18, 0.06, TX - 1.1, 1.05), (0.12, 0.05, TX + 1.3, -0.6), (0.1, 0.04, TX + 1.2, 1.1))]
     + [(ell(0.03, 0.025, TX + dx, dz), "#C7B89C") for dx, dz in ((-1.2, -0.4), (1.25, 0.4), (-0.3, -0.9), (0.9, -0.95))], 1.0)
top_map_carved = part("Top_Map", None, [([(TMAP[0] + x, TMAP[1] + z) for x, z in pts], col) for pts, col in map_big(stone=True)], 0.95)
top_cover = node("Top_Cover", None, TMAP, 0.9)
part("Top_CoverShape", top_cover, [(rrect(0.82, 0.76, 0.05), STONE_D), (rrect(0.79, 0.73, 0.045), STONE),
                                   (band([(-0.2, 0.25), (-0.05, 0.1), (0.02, 0.12)], 0.008), STONE_D)])
part("Top_StarSlab", None, [(rrect(0.86, 0.82, 0.06, *TSTAR), STONE_D), (rrect(0.82, 0.78, 0.05, *TSTAR), "#D2C4AB"),
                            (arc(0.31, 0, 360, 0.03, *TSTAR), STONE_D), (ell(0.27, 0.27, *TSTAR), "#C4B597")], 0.88)
top_star = node("Top_Star", None, TSTAR, 0.87)                  # ngôi sao nổi; ấn thì thu nhỏ (lún xuống)
part("Top_StarShape", top_star, [([(x - 0.012, z - 0.018) for x, z in rose(0.27)], STONE_D), (rose(0.26), STAR_STONE)])
top_click = part("Top_Click", None, [(band([(0.0, 0.0), (dx, dz)], 0.02), WHITE) for dx, dz in
                                     ((-0.2, 0.12), (0.0, 0.22), (0.2, 0.12), (0.22, -0.05))], 0.8, (TSTAR[0], TSTAR[1] + 0.3))
top_flash = part("Top_Flash", None, map_obs_glow(TEAL, TEAL_L), 0.86, (TMAP[0] + MAP_OBS[0], TMAP[1] + MAP_OBS[1]))
SHOULDER = (TX - 1.55, -0.45)                                   # bàn tay Lumo ấn ngôi sao, vươn vào từ góc dưới trái
REACH = math.dist(SHOULDER, TSTAR)
REACH_DIR = ((TSTAR[0] - SHOULDER[0]) / REACH, (TSTAR[1] - SHOULDER[1]) / REACH)
press_arm = node("Top_PressArm", None, SHOULDER, 0.5)
part("Top_PressArmShape", press_arm, [(rrect(REACH, 0.15, 0.07, REACH / 2 - 0.05, 0.0), "#FD8A2B"), (ell(0.095, 0.085, REACH, 0.0), "#FD8A2B"),
                                      (ell(0.05, 0.035, REACH + 0.01, 0.0), "#FEECCF")])
press_arm.rotation_euler = (0.0, -math.atan2(REACH_DIR[1], REACH_DIR[0]), 0.0)
top_hold = node("Top_Hold", None, PMAP, 0.6)                    # tay và bản đồ giấy nhích theo nhịp thở
top_map = node("Top_PaperMap", top_hold, (0.0, 0.0), 0.0)
part("Top_PaperShape", top_map, map_big())
top_paws = []
for side in (-1, 1):
    pw = node(f"Top_Paw{side}", top_hold, (side * 0.33, -0.27), -0.05)
    part(f"Top_PawShape{side}", pw, [(rrect(0.13, 0.42, 0.06, side * 0.02, -0.2), "#FD8A2B"), (ell(0.075, 0.06, 0, 0), "#FD8A2B"),
                                     (ell(0.045, 0.03, 0, 0.01), "#FEECCF")])
    top_paws.append(pw)
TOP_TARGETS = (TSTAR, (TMAP[0] + MAP_OBS[0], TMAP[1] + MAP_OBS[1] + 0.03), (TX + 100.0, 0.3))

# ================================================================ nhân vật: Lumo, chú chim; la bàn, bản đồ trong tay
lumo = build_lumo(-0.72, -0.3)
hand_hold = palm(lumo, "Lumo_HandHold")                          # đồ cầm ở tay gần: luôn đứng thẳng dù tay xoay
compass = build_compass("CompassHand", hand_hold, (0.045, 0.02), -0.002, 0.06)   # ngang ngực khi tay ở -72 (như Cảnh 1)
map_sheet = node("Lumo_Map", hand_hold, (0.045, 0.04), -0.004)
part("Lumo_MapShape", map_sheet, map_card())
far_hold = palm(lumo, "Lumo_FarHold", True, -0.002)
map_far = node("Lumo_MapFar", far_hold, (0.045, 0.04), 0.0)
compass_far = build_compass("CompassFar", far_hold, (0.045, 0.02), 0.0, 0.06)   # chuyển sang tay xa lúc tay gần túm dây leo
part("Lumo_MapFarShape", map_far, map_card())
bag_glow = part("Lumo_BagGlow", lumo.root, [(ell(0.045, 0.022, 0.1, 0.236), "#FFF1A6")], -0.0095)   # ánh la bàn lọt ra miệng túi
bag_beep = part("Lumo_BagBeep", lumo.root, [(arc(0.035, -45, 45, 0.01), "#FFE27A"), (arc(0.06, -45, 45, 0.01), "#FFE27A")],
                -0.03, (0.16, 0.2))                             # vạch sóng TÍT cạnh túi
moss_bits = [part(f"MossBit{i}", None, [(leaf_pts(0, 0, 1.6, 0), MOSS if i % 2 else "#94C25A")], -0.45) for i in range(6)]
bird = build_bird(3.0, 4.6, -0.63)


def pov_compass(name, x, z, r, y):
    """La bàn to cho cú cận sau vai: hai bàn tay Lumo cầm từ dưới, vạch sóng TÍT hai bên."""
    n = node(name, None, (x, z), y)
    c = build_compass(f"{name}_C", n, (0.0, 0.0), 0.0, r)
    for side in (-1, 1):
        part(f"{name}_Paw{side}", n, [(rrect(0.32 * r, 0.9 * r, 0.14 * r, side * 0.72 * r, -1.25 * r), "#FD8A2B"),
                                     (ell(0.24 * r, 0.2 * r, side * 0.7 * r, -0.78 * r), "#FD8A2B"),
                                     (ell(0.14 * r, 0.09 * r, side * 0.66 * r, -0.74 * r), "#FEECCF")], -0.02)
    c.beep = part(f"{name}_Beep", c.root, [(arc(1.25 * r, -50, 50, 0.18 * r), "#FFE27A"), (arc(1.25 * r, 130, 230, 0.18 * r), "#FFE27A")], -0.01)
    c.node = n
    return c


pov1 = pov_compass("POV1", 2.35, 0.5, 0.5, -2.0)                 # trước cảnh cầu, nhìn sang bệ đá
pov2 = pov_compass("POV2", TX - 0.05, -0.14, 0.22, 0.5)          # trên mặt bệ nhìn từ trên


def hold(t, near, far=None):
    """Tay gần cầm la bàn hay bản đồ, tay xa cầm đồ ở far_hold: đồ trong tay luôn đứng thẳng theo thân; tay xa mặc định
    theo tay gần, lệch 5°."""
    chold(lumo, hand_hold, t, near, far, far_hold, 5)


def beep_wave(ob, t, big=1.0):
    """Một tiếng TÍT vẽ bằng vạch sóng (cạnh túi da, hai bên la bàn to): vạch bật ra rồi tắt. Khác beep() của cutout
    (quầng la bàn nháy)."""
    show(ob, t, True)
    scl(ob, t, 0.5 * big, 0.5 * big)
    scl(ob, t + 0.08, 1.15 * big, 1.15 * big)
    scl(ob, t + 0.16, 1.0 * big, 1.0 * big)
    show(ob, t + 0.18, False)


def lumo_at(t, x, z=0.0, y=None):
    pos(lumo.root, t, x, z, y)


for ob in (bird.root, compass.root, compass_far.root, side_map, top_map_carved, top_click, press_arm, map_sheet, map_far, bag_glow, bag_beep, click, side_flash, top_flash, top_map, *top_paws,
           *halves, *sparks, *moss_bits, pov1.node, pov2.node, lintel_glow["dim"], door_glow["dim"], rails["near", "droop"],
           rails["far", "droop"]):
    show(ob, 0.0, False)
for c in (compass, compass_far, pov1, pov2):
    show(c.glow, 0.0, False)
for ob in (door_glow["bright"], lintel_glow["bright"], planks[FALL[0]], *(rails[side, k] for side in ("near", "far") for k in range(1, 8))):
    show(ob, 0.0, True)                                         # mảnh tắt giữa cảnh: hiện từ giây 0
lumo.cur = "squint"

# ================================================================ S1: cánh cửa mở hẳn, hình mây tắt dần; Lumo loạng choạng ra bậc cửa
o0, o1 = DOOR_OPEN
scl(door, 0.0, 0.85, 1)
scl(door, o0 + 0.25, 0.6, 1)
scl(door, o1, 0.1, 1)                                           # mở hẳn: chỉ còn cạnh cửa ở bản lề
for d in (door_glow, lintel_glow):                              # sáng → dịu → tắt
    show(d["bright"], CLOUDS_FADE[0], False)
    show(d["dim"], CLOUDS_FADE[0], True)
    show(d["dim"], CLOUDS_FADE[1], False)
for i, sp in enumerate(sparks):
    twinkle(sp, 0.0, CLOUDS_FADE[0] - 0.1, 1.3, 0.7, 0.18 + 0.03 * i)
    show(sp, CLOUDS_FADE[0], False)
lumo_at(0.0, -0.72)
lean(lumo, 0.0, 14)                                             # đang đẩy hết sức
hold(0.0, -95, -100)
fc(lumo, 0.0, "squint", 14)
ears(lumo, 0.0, -30)
s0, s1 = LUMO_STUMBLE
lumo_at(s0, -0.72)
lumo_at(s0 + 0.25, -0.58, 0.04)                                 # hụt tay, chúi tới
lumo_at(s0 + 0.5, -0.46, 0.0)
lumo_at(s0 + 0.75, -0.4, 0.03)
lumo_at(s1, -0.35)
lean(lumo, s0, 14)
lean(lumo, s0 + 0.25, 24)
lean(lumo, s0 + 0.6, -10)                                       # bật ngửa lại giữ thăng bằng
lean(lumo, s1, 0)
for i, t in enumerate(steps(s0 + 0.1, s1 - 0.15, 0.12)):         # tay quơ giữ thăng bằng
    hold(t, -140 if i % 2 else -80, -70 if i % 2 else -135)
hold(s1, -10, -5)
fc(lumo, s0 + 0.1, "shock", 20)
ears(lumo, s0 + 0.1, 20)
ears(lumo, s1, 2)
ry(lumo.tail, s0, 20)
ry(lumo.tail, s0 + 0.3, 55)
ry(lumo.tail, s1, 25)
fc(lumo, s1 + 0.1, "neutral")
look(lumo, s1 + 0.1, 0.3, 0.0)
bl(lumo, 1.9)
fc(lumo, LUMO_WOW, "wonder")                                    # thấy cây cầu
look(lumo, LUMO_WOW, 1.0, 0.0)
ears(lumo, LUMO_WOW - 0.05, 2)
ears(lumo, LUMO_WOW + 0.12, 16)
ears(lumo, LUMO_WOW + 0.3, 8)
squash(lumo, LUMO_WOW, 1, 1)
squash(lumo, LUMO_WOW + 0.12, 0.97, 1.04)
squash(lumo, LUMO_WOW + 0.3, 1, 1)
loop(lumo.tail, LUMO_WOW, 9.0, 0.7, 18, 34)

# ================================================================ S2: toàn cảnh; mắt đi dọc cây cầu sang bệ đá
look(lumo, LOOK_ACROSS[0], 0.6, -0.3)                            # nhìn mặt cầu ngay trước chân
look(lumo, LOOK_ACROSS[0] + 0.8, 0.9, -0.1)
look(lumo, LOOK_ACROSS[1], 1.0, 0.1)                             # tới bệ đá bên kia
ry(lumo.head, LOOK_ACROSS[0], 8)
ry(lumo.head, LOOK_ACROSS[1], -4)
fc(lumo, LOOK_ACROSS[1] + 0.2, "eager")
bl(lumo, 7.6)

# ================================================================ S3: túi da rung, TÍT… TÍT…; rút la bàn
for t in BEEPS_BAG:
    beep_wave(bag_beep, t)
    jitter(lumo.bag, t, t + 0.3, 0.004, 0.05)                   # rung khẽ
show(bag_glow, BEEPS_BAG[0], True)
twinkle(bag_glow, BEEPS_BAG[0], COMPASS_OUT[0], 1.2, 0.8, 0.2)
ears(lumo, BEEPS_BAG[0], 8)
ears(lumo, BEEPS_BAG[0] + 0.1, 22)                               # tai giật lên khi nghe TÍT
ears(lumo, BEEPS_BAG[0] + 0.3, 6)
fc(lumo, BEEPS_BAG[0] + 0.15, "puzzled")
look(lumo, BEEPS_BAG[0] + 0.3, 0.3, -1.0)                        # liếc xuống túi
ry(lumo.head, BEEPS_BAG[0] + 0.3, 14)
c0, c1 = COMPASS_OUT
CHEST, PUSH = -72, -80                                           # tay chìa la bàn ngang ngực; đẩy tới thêm ở câu hô (như Cảnh 1)
hold(c0 - 0.2, -10, -5)
hold(c0 + 0.1, -15, -5)                                          # tay vào túi
show(bag_glow, c0 + 0.15, False)
show(compass.root, c0 + 0.15, True)
glow(compass, c0 + 0.15, 0.62)                                   # sáng le lói: quầng chỉ nhô khỏi vỏ
hold(c1, CHEST, -5)                                              # nâng lên ngang ngực
look(lumo, c1, 0.8, -0.45)
ry(lumo.head, c1, 10)
fc(lumo, c1 + 0.05, "eager", 10)
ears(lumo, c1, -12)
jitter(compass.root, c0 + 0.2, STOW_COMPASS[0], 0.0025, 0.07)   # rung khẽ suốt lúc cầm (còn cách cả khe)
twinkle(compass.glow, c0 + 0.2, STOW_COMPASS[0], 0.66, 0.56, 0.35)
bl(lumo, 12.2)

# ================================================================ S4: cận la bàn sau vai (la bàn to trước cảnh)


def pov(c, t0, t1, g=0.6, amp=0.0):
    show(c.node, t0, True)
    show(c.beep, t0, False)
    glow(c, t0, g)
    twinkle(c.glow, t0, t1, g * 1.1, g * 0.92, 0.35)
    if amp:
        jitter(c.root, t0, t1, amp, 0.07)
    show(c.node, t1, False)


pov(pov1, SHOT["S4"][0], SHOT["S4"][1], 0.62, 0.008)
beep_wave(pov1.beep, SHOT["S4"][0] + 0.9)                       # còn cách cả khe: kêu thưa

# ================================================================ S5: dựng tai, chìa la bàn; "Ngay phía trước!"; lấy đà
p0, p1 = POSE
ears(lumo, p0 - 0.25, -12)
ears(lumo, p0, -30)                                              # tai cụp hẳn trước câu hô
ears(lumo, p0 + 0.15, 14)                                        # bật dựng thẳng hai tai
ears(lumo, p1, 0)
hold(p0, -65, -5)
hold(p0 + 0.25, CHEST, -5)                                       # chìa la bàn thẳng ra trước, ngang ngực
ry(lumo.head, p0, 10)
ry(lumo.head, p0 + 0.2, -6)
ry(lumo.head, p1, 0)
lean(lumo, p0, -3)
lean(lumo, p0 + 0.25, -6)
squash(lumo, p0, 1, 1)
squash(lumo, p0 + 0.12, 1.08, 0.92)                              # nhún mạnh
squash(lumo, p0 + 0.25, 0.95, 1.06)
squash(lumo, p1, 1, 1)
fc(lumo, p0 + 0.15, "eager")
look(lumo, p0 + 0.15, 1.0, 0.05)                                 # mắt dán vào bệ đá bên kia
l0, l1 = LINE_AHEAD
fc(lumo, l0 - 0.05, "shout")
talk(lumo, l0, l1, "smile")
hold(l0 + 0.3, CHEST, -5)
hold(l0 + 0.5, PUSH, -5)                                         # đẩy la bàn tới thêm ở "ngay phía trước"
lean(lumo, l0 + 0.3, -6)
lean(lumo, l0 + 0.55, 2)
ry(lumo.head, l0 + 0.3, 0)
ry(lumo.head, l0 + 0.55, -8)
bl(lumo, l1 + 0.05)
r0, r1 = RUSH
STAND_X = 1.2                                                    # chỗ Lumo khựng lại trên cầu (tấm ván 1, 2)
squash(lumo, r0, 1, 1)
squash(lumo, r0 + 0.15, 1.06, 0.92)                              # lấy đà
squash(lumo, r0 + 0.3, 0.97, 1.04)
squash(lumo, r0 + 0.45, 1, 1)
lean(lumo, r0, 2)
lean(lumo, r0 + 0.15, 10)
lean(lumo, r0 + 0.35, 14)                                        # lao tới
ears(lumo, r0 + 0.2, -22)                                        # tai bạt ra sau vì gió
hold(r0 + 0.2, -60, 20)
lumo_at(r0, -0.35)
lumo_at(r0 + 0.2, -0.35)
walk(lumo.root, r0 + 0.2, r1, -0.35, STAND_X, 5, 0.06)           # mấy bước chạy lên cầu
fc(lumo, r0 + 0.1, "eager", 14)
look(lumo, r0 + 0.1, 1.0, 0.1)
ry(lumo.head, r0 + 0.1, 0)
loop(lumo.tail, r0, r1, 0.25, 30, 50)
loop(lumo.arm_far, r0 + 0.3, r1, 0.2, 30, -40)

# ================================================================ S6: CREAAAAK, chờ sỏi, "Không sao…", mắt vẫn ngước mà bước tiếp
creak = planks[CREAK_PLANK]
ry(creak, CREAK - 0.02, 0)
ry(creak, CREAK + 0.08, -40)                                    # tấm ván trước mặt bật lên
ry(creak, CREAK + 0.3, -4)
ry(creak, CREAK + 0.42, -12)
ry(creak, CREAK + 0.6, -3)
lumo_at(CREAK, STAND_X)
lumo_at(CREAK + 0.1, STAND_X - 0.03, 0.03)                      # khựng lại
lumo_at(CREAK + 0.25, STAND_X - 0.03)
lean(lumo, CREAK, 14)
lean(lumo, CREAK + 0.1, -10)
lean(lumo, CREAK + 0.3, -2)
fc(lumo, CREAK + 0.03, "shock")
ears(lumo, CREAK + 0.03, 25)
hold(CREAK + 0.05, -75, -60)
hold(CREAK + 0.4, -45, -20)
ry(lumo.tail, CREAK, 30)
ry(lumo.tail, CREAK + 0.1, 60)                                   # đuôi dựng đứng
look(lumo, CREAK + 0.1, 0.8, -0.8)                               # nhìn tấm ván
w0, w1 = WAIT_PEBBLE
ears(lumo, w0, 10)
ears(lumo, w0 + 0.15, -55)                                       # cụp tai
look(lumo, w0 + 0.1, 0.2, 1.0)                                   # ngước nhìn trời, chờ hòn sỏi
ry(lumo.head, w0, 0)
ry(lumo.head, w0 + 0.2, -16)
fc(lumo, w0 + 0.1, "worried", -18)
squash(lumo, w0, 1, 1)
squash(lumo, w0 + 0.2, 1.04, 0.95)                              # rụt cổ
ry(lumo.tail, w0 + 0.2, 10)
hold(w0 + 0.2, -20, -15)
bl(lumo, w0 + 1.1)
fc(lumo, NO_PEBBLE, "happy", -16)                                # không có sỏi: thở phào
ears(lumo, NO_PEBBLE, -55)
ears(lumo, NO_PEBBLE + 0.2, 6)
squash(lumo, NO_PEBBLE, 1.04, 0.95)
squash(lumo, NO_PEBBLE + 0.25, 0.98, 1.03)
squash(lumo, NO_PEBBLE + 0.45, 1, 1)
ry(lumo.tail, NO_PEBBLE + 0.2, 28)
e0, e1 = LINE_OLD
fc(lumo, e0 - 0.3, "calm", -18)                                  # mắt mở: thấy tròng mắt vẫn ngước nhìn trời
look(lumo, e0 - 0.3, 0.4, 0.95)
ry(lumo.head, e0, -18)
talk(lumo, e0, e0 + 0.7, "smile")                                # "Không sao."
talk(lumo, e0 + 0.9, e1, "smile")                                # "Một chiếc cầu hơi cũ thôi."
hold(e0, -20, -15)
hold(e0 + 0.3, -55, -15)
hold(e0 + 0.6, -30, -15)                                         # phẩy tay cầm la bàn: không sao
for t, a in ((e0 + 0.9, -16), (e0 + 1.3, -22), (e1 - 0.4, -18)):
    ry(lumo.head, t, a)
loop(lumo.tail, e0, e1, 0.6, 18, 34)
st0, st1 = STEP_ON
ry(lumo.head, st0, -22)
look(lumo, st0, 0.4, 1.0)                                        # vẫn ngước trời
lean(lumo, st0, -2)
lean(lumo, st0 + 0.3, -6)
lumo_at(st0, STAND_X - 0.03)
lumo_at(st0 + 0.35, STAND_X + 0.06, 0.07)                        # nhấc chân thong thả
lumo_at(st1 - 0.1, STAND_X + 0.2, 0.0)
STEP_X = STAND_X + 0.2                                           # mũi chân trên tấm ván 3; tấm 4 ngay trước mũi chân
hold(st0, -30, -15)
hold(st0 + 0.4, -40, 10)
fc(lumo, st0, "calm", -22)

# ================================================================ S7, S8: CRACK, dãy ván rơi xuống lưới; chới với, túm dây leo, ngã ngồi
SWAP = SHOT["S7"][0]                                            # cắt cảnh: la bàn sang tay xa để tay gần túm dây leo
show(compass.root, SWAP, False)
show(compass_far.root, SWAP, True)
glow(compass_far, SWAP, 0.62)
twinkle(compass_far.glow, SWAP, LOOK_COMPASS, 0.66, 0.56, 0.35)
jitter(compass_far.root, SWAP, LOOK_COMPASS, 0.0025, 0.07)
show(planks[FALL[0]], CRACK, False)                             # tấm ván trước mũi chân gãy làm hai
for k, h in enumerate(halves):
    side = -1 if k == 0 else 1
    x0 = PLANKS[FALL[0]] + PLANK_W / 2
    show(h, CRACK, True)
    pos(h, CRACK, x0, 0.0)
    ry(h, CRACK, 0)
    ry(h, CRACK + 0.12, 35 * side)
    for t, dz, a in ((CRACK + 0.25, -0.25, 80), (CRACK + 0.5, net_z(x0) + 0.03, 150), (CRACK + 0.65, net_z(x0) + 0.1, 160),
                     (CRACK + 0.85, net_z(x0) + 0.03, 170)):
        pos(h, t, x0 + side * 0.08, dz)
        ry(h, t, a * side)
for n, i in enumerate(FALL[1:]):
    t0 = CRACK + 0.05 + 0.045 * n                               # kéo theo cả dãy, từ gần tới xa
    x0 = PLANKS[i]
    xc = x0 + PLANK_W / 2
    a = random.choice((-1, 1)) * random.uniform(15, 55)
    pos(planks[i], t0, x0, 0.0)
    ry(planks[i], t0, 0)
    pos(planks[i], t0 + 0.2, x0 + 0.01, -0.22)
    pos(planks[i], t0 + 0.42, x0 + 0.02, net_z(xc) + 0.04)      # rơi xuống lưới
    pos(planks[i], t0 + 0.58, x0 + 0.02, net_z(xc) + 0.12)      # nảy
    pos(planks[i], t0 + 0.78, x0 + 0.02, net_z(xc) + 0.03)
    pos(planks[i], t0 + 0.95, x0 + 0.02, net_z(xc) + 0.07)      # bập bềnh
    pos(planks[i], t0 + 1.15, x0 + 0.02, net_z(xc) + 0.04)
    ry(planks[i], t0 + 0.42, a)
    ry(planks[i], t0 + 1.15, a * 0.6)
for side in ("near", "far"):
    for n, k in enumerate(FALL_POSTS):
        t0 = CRACK + 0.08 + 0.13 * n
        x = POSTS[k]
        pos(posts[side, k], t0, x, 0.0)
        ry(posts[side, k], t0, 0)
        pos(posts[side, k], t0 + 0.45, x + 0.15, net_z(x) + 0.08)
        ry(posts[side, k], t0 + 0.45, 75 if n % 2 else -80)
        pos(posts[side, k], t0 + 0.65, x + 0.15, net_z(x) + 0.14)
        pos(posts[side, k], t0 + 0.85, x + 0.15, net_z(x) + 0.08)
    for k in range(1, 8):
        show(rails[side, k], CRACK + 0.25, False)
    show(rails[side, "droop"], CRACK + 0.25, True)              # dây thành cầu chùng xuống giữa khe
for t, s in ((CRACK + 0.35, 1.0), (CRACK + 0.55, 1.35), (CRACK + 0.8, 0.85), (CRACK + 1.05, 1.15), (CRACK + 1.3, 0.95), (CRACK + 1.6, 1.0)):
    scl(net_front, t, 1.0, s)                                   # lưới võng xuống đỡ ván, nảy bập bềnh
# Lumo: mắt giật xuống, chới với ở mép khoảng trống
fc(lumo, CRACK + 0.02, "shock", 10)
look(lumo, CRACK + 0.02, 0.7, -1.0)
ry(lumo.head, CRACK + 0.02, 10)
ears(lumo, CRACK + 0.02, 28)
ry(lumo.tail, CRACK, 30)
ry(lumo.tail, CRACK + 0.08, 65)
lumo_at(CRACK, STEP_X)
lean(lumo, CRACK, -4)
lean(lumo, CRACK + 0.15, 16)                                    # chúi về phía khoảng trống
f0, f1 = FLAIL
for i, t in enumerate(steps(f0, f1 - 0.1, 0.13)):
    hold(t, -145 if i % 2 else -85, -90 if i % 2 else -145)     # hai tay quay tít, không quá ngang tai
    lean(lumo, t, 14 if i % 2 else 4)
    ears(lumo, t, 30 if i % 2 else 10)
loop(lumo.tail, f0, f1, 0.13, 40, 70)
lumo_at(f1 - 0.3, STEP_X - 0.04, 0.02)
# túm dây leo ở thành cầu sát cửa (đoạn giữa cột 0 và 1) bằng tay gần, vòng ra sau; bàn tay bám yên trên dây
ROPE = (0.5 * (POSTS[0] + POSTS[1]) - 0.01, RAIL_Z - 0.02)
GX = STEP_X - 0.04


def grip(t, lean_deg, far):
    a = reach(lumo, GX, 0.0, lean_deg, ROPE, lo=-60, hi=120)
    hold(t, a, far)
    lean(lumo, t, lean_deg)


g0, g1 = GRAB
lumo_at(g0 - 0.12, GX)
hold(g0 - 0.12, 20, -120)                                        # tay gần vung ra sau
grip(g0, 10, -110)                                               # túm dây leo: vẫn chúi về khoảng trống
fc(lumo, g0, "squint", 10)
ears(lumo, g0, 30)
grip(g0 + 0.2, 2, -90)
grip(g0 + 0.4, -6, -80)                                          # kéo người ngả về phía cửa
grip(g1, -10, -75)
lumo_at(g1, GX)
fc(lumo, g1 - 0.15, "shock", -10)
hold(g1 + 0.1, -70, -100)                                        # buông dây, loạng choạng lùi
lumo_at(g1 + 0.15, GX - 0.2, 0.03)
lumo_at(g1 + 0.35, 0.62, 0.04)
lumo_at(g1 + 0.48, 0.2, 0.0)
lean(lumo, g1 + 0.2, -20)
lean(lumo, g1 + 0.45, -26)
ears(lumo, g1 + 0.2, 20)
SIT_X, SIT_Z = -0.15, -0.17
lumo_at(PHICH - 0.08, -0.02, 0.05)
lumo_at(PHICH, SIT_X, SIT_Z)                                     # ngã ngồi trên đệm rêu: PHỊCH
lean(lumo, PHICH - 0.08, -30)
lean(lumo, PHICH, -12)
squash(lumo, PHICH, 1.14, 0.84)
squash(lumo, PHICH + 0.15, 0.96, 1.05)
squash(lumo, PHICH + 0.35, 1, 1)
lean(lumo, PHICH + 0.35, -8)
hold(PHICH - 0.05, -110, -120)
hold(PHICH + 0.1, -125, -130)                                    # tay hất lên theo cú dội
hold(PHICH + 0.45, -35, -25)
ry(lumo.tail, PHICH - 0.1, 40)
ry(lumo.tail, PHICH, 0)                                          # đáp lên cái đuôi bông, đuôi bẹp trên đệm rêu
scl(lumo.tail, PHICH - 0.02, 1, 1)
scl(lumo.tail, PHICH + 0.05, 1.3, 0.62)
scl(lumo.tail, PHICH + 0.25, 0.92, 1.12)
scl(lumo.tail, PHICH + 0.45, 1, 1)
ry(lumo.tail, PHICH + 0.5, 14)
fc(lumo, PHICH, "squint", -12)
ears(lumo, PHICH, 30)
ears(lumo, PHICH + 0.15, -40)
ears(lumo, PHICH + 0.4, -20)
for k, ob in enumerate(moss_bits):
    fly_bit(ob, PHICH + 0.02 * k, (SIT_X - 0.25 + 0.1 * k, 0.04), (SIT_X - 0.6 + 0.24 * k, 0.03), PHICH + 0.6, 240, 0.18 + 0.03 * (k % 3))
fc(lumo, PHICH + 0.7, "shock", -8)                               # ngơ ngác
look(lumo, PHICH + 0.7, 0.9, -0.3)
bl(lumo, PHICH + 1.4)

# ================================================================ S9, S10: chú chim đáp xuống cột cầu, cười; "Được rồi! Một chiếc cầu… rất cũ!"
BX, BZ = POSTS[1], POST_TOP + 0.005                              # đỉnh cột cầu sát cửa còn đứng
bird_eyes(bird, 0.0, "open")
bird_beak(bird, 0.0, "closed")
ry(bird.wing, 0.0, 0)
ry(bird.wing_far, 0.0, 0)
b0, b1 = BIRD_LAND
show(bird.root, b0, True)
scl(bird.root, b0, -1, 1)                                        # bay từ phải sang, quay mặt về phía Lumo
bird.dir = -1
for t, x, z in ((b0, BX + 0.8, 1.3), (b0 + 0.25, BX + 0.45, 0.95), (b0 + 0.5, BX + 0.12, 0.66), (b1, BX, BZ)):
    pos(bird.root, t, x, z)
for i, t in enumerate(steps(b0, b1 - 0.1, 0.06)):
    ry(bird.wing, t, 65 if i % 2 else -35)
    ry(bird.wing_far, t, 70 if i % 2 else -30)
ry(bird.wing, b1, 0)
ry(bird.wing_far, b1, 0)
scl(bird.root, b1, -1.1, 0.88)                                   # đáp xuống, nhún
scl(bird.root, b1 + 0.15, -1, 1)
ry(bird.head, BIRD_LOOK - 0.2, 0)
ry(bird.head, BIRD_LOOK, 22)                                     # nghiêng đầu nhìn Lumo


def bird_laugh(c, big=True):
    ry(bird.wing, c - 0.18, -55)
    ry(bird.wing, c, -100)
    ry(bird.wing, c + 0.1, -70)
    ry(bird.wing, c + 0.2, -100 if big else -80)
    ry(bird.wing, c + 0.3, -60 if big else 0)
    bird_beak(bird, c - 0.02, "open")
    bird_beak(bird, c + 0.22, "closed")
    if big:
        pos(bird.root, c - 0.1, BX, BZ)
        pos(bird.root, c + 0.05, BX, BZ + 0.025)
        pos(bird.root, c + 0.25, BX, BZ)
        scl(bird.root, c - 0.1, -1.08, 0.92)
        scl(bird.root, c + 0.05, -0.95, 1.06)
        scl(bird.root, c + 0.25, -1, 1)
        ry(bird.head, c, -14)                                    # ngửa đầu cười
        ry(bird.head, c + 0.3, 6)


bird_eyes(bird, BIRD_LAUGH[0], "happy")
for c in CHIRPS:
    bird_laugh(c)
ry(bird.wing, BIRD_LAUGH[1], -60)
ry(bird.wing, BIRD_LAUGH[1] + 0.2, 0)
ry(bird.head, BIRD_LAUGH[1] + 0.2, 16)
for c in (35.2, 36.1, 39.6, 41.0, 42.3):                         # còn khúc khích trong lúc Lumo chống chế, nhìn quanh
    bird_laugh(c, False)
ry(bird.wing, 42.7, 0)
bird_eyes(bird, BIRD_STOP, "open")                               # thôi cười, nghiêng đầu
bird_beak(bird, BIRD_STOP, "closed")
ry(bird.head, BIRD_STOP, 0)
ry(bird.head, BIRD_STOP + 0.25, 26)
for t in (34.0, 38.0, 45.0):
    bird_eyes(bird, t, "closed")
    bird_eyes(bird, t + 0.1, "happy" if t < BIRD_STOP else "open")
# Lumo: nghe CHÍP, nhìn chú chim, ngượng; "Được rồi! Một chiếc cầu… rất cũ!"
fc(lumo, BIRD_LAUGH[0] + 0.1, "puzzled", -8)
look(lumo, BIRD_LAUGH[0] + 0.1, 1.0, 0.3)
ry(lumo.head, BIRD_LAUGH[0] + 0.3, -6)
fc(lumo, BIRD_LAUGH[0] + 0.8, "sheepish", -8)
ears(lumo, BIRD_LAUGH[0] + 0.8, -20)
ears(lumo, BIRD_LAUGH[0] + 1.1, -48)                             # cụp tai ngượng
v0, v1 = LINE_VERY_OLD
ears(lumo, v0 - 0.1, -48)
ears(lumo, v0 + 0.15, 4)
fc(lumo, v0 - 0.05, "sheepish", -8)
talk(lumo, v0, v0 + 0.6, "frown")                                # "Được rồi!"
hold(v0, -35, -25)
hold(v0 + 0.25, -60, -60)                                        # xòe hai tay: chịu thua
hold(v0 + 0.7, -40, -30)
squash(lumo, v0, 1, 1)
squash(lumo, v0 + 0.2, 1.03, 0.97)
squash(lumo, v0 + 0.5, 1, 1)
look(lumo, v0 + 0.8, 1.0, -0.3)                                  # liếc khoảng trống
fc(lumo, v0 + 0.8, "neutral", -8)
talk(lumo, v0 + 0.9, v1, "frown")                                # "Một chiếc cầu… rất cũ!"
for t, a in ((v1 - 0.6, -6), (v1 - 0.4, 8), (v1 - 0.2, -2), (v1, 4)):
    ry(lumo.head, t, a)                                          # gật mạnh ở "rất cũ!"
ears(lumo, v1 - 0.45, 8)
ears(lumo, v1 - 0.3, -25)
ears(lumo, v1, -10)
fc(lumo, v1 + 0.05, "sheepish", -8)
hold(LOOK_COMPASS - 0.2, -45, -45)                               # chụm hai tay: la bàn về tay gần
show(compass_far.root, LOOK_COMPASS - 0.05, False)
show(compass.root, LOOK_COMPASS - 0.05, True)
hold(LOOK_COMPASS + 0.3, -75, -30)                               # nâng la bàn lên nhìn
look(lumo, LOOK_COMPASS + 0.2, 0.8, -0.5)
ry(lumo.head, LOOK_COMPASS + 0.3, 10)
fc(lumo, LOOK_COMPASS + 0.2, "puzzled", 2)

# ================================================================ S11: cận la bàn qua khoảng trống
pov(pov1, SHOT["S11"][0], SHOT["S11"][1], 0.62, 0.008)
beep_wave(pov1.beep, SHOT["S11"][0] + 1.1)

# ================================================================ S12: đứng dậy, nhìn khoảng trống, vách đá, bụi cây; vạch bụi cây
u0, u1 = STAND_UP
lumo_at(u0, SIT_X, SIT_Z)
lumo_at(u0 + 0.2, SIT_X, SIT_Z + 0.04)
lumo_at(u1, SIT_X, 0.0)
lean(lumo, u0, -8)
lean(lumo, u0 + 0.2, 14)
lean(lumo, u1, 0)
ry(lumo.tail, u1, 22)
hold(u0, -75, -30)
hold(u1, -40, -10)
fc(lumo, u1, "focus")
for (t0, t1), (dx, dz), head in ((LOOK_GAP, (1.0, -0.45), 6), (LOOK_WALL, (0.6, 1.0), -18), (LOOK_BUSH, (0.9, -0.7), 12)):
    look(lumo, t0, dx, dz)
    ry(lumo.head, t0, head * 0.5)
    ry(lumo.head, t0 + 0.25, head)
    fc(lumo, t0, "focus", head)
    bl(lumo, t1 - 0.12)
ears(lumo, LOOK_WALL[0], 12)
ears(lumo, LOOK_BUSH[0], 4)
ears(lumo, LOOK_BUSH[0] + 0.3, 14)                               # thấy gì đó sau bụi cây
b0, b1 = TO_BUSH
BUSH_X = -0.12                                                   # đứng sát mép trái bụi cây
lumo_at(b0, SIT_X)
lumo_at((b0 + b1) / 2, (SIT_X + BUSH_X) / 2, 0.03)
lumo_at(b1, BUSH_X)
ry(lumo.head, b1, 4)
look(lumo, b1, 1.0, -0.2)
q0, q1 = PART_BUSH
hold(q0, -90, -95)                                               # đưa hai tay vào bụi cây
hold(q0 + 0.3, -100, -90)
hold(q1, -125, -45)                                              # vạch ra hai bên
lean(lumo, q0, 4)
lean(lumo, q1, 8)
for b, (a, dx) in zip(bush, ((-30, -0.12), (40, 0.24))):
    ry(b, q0 + 0.2, 0)
    pos(b, q0 + 0.2, b.location.x, 0.0)
    ry(b, q1, a)
    pos(b, q1, b.location.x + dx, 0.0)
    ry(b, q1 + 0.15, a * 1.08)
    ry(b, q1 + 0.3, a)
fc(lumo, q1 + 0.05, "wonder")                                    # những bậc đá rộng hiện ra
ears(lumo, q1, 4)
ears(lumo, q1 + 0.12, 18)
ears(lumo, q1 + 0.3, 8)
look(lumo, q1 + 0.05, 0.9, 0.4)
hold(q1 + 0.5, -60, -50)
lean(lumo, q1 + 0.5, 0)
loop(lumo.tail, q1, LINE_LOOK[0], 0.6, 16, 34)

# ================================================================ S13: "Nhìn kỹ trước đã."
k0, k1 = LINE_LOOK
fc(lumo, k0 - 0.3, "focus")
look(lumo, k0 - 0.3, 0.9, 0.35)
ears(lumo, k0 - 0.2, 0)
talk(lumo, k0, k1, "closed")
ry(lumo.head, k0, 0)
ry(lumo.head, k1 - 0.3, 8)                                       # gật nhẹ
ry(lumo.head, k1, 0)
hold(k0, -60, -50)
hold(k1, -45, -35)
fc(lumo, k1 + 0.05, "calm")

# ================================================================ S14: cất la bàn, bám tay vịn, đi chậm từng bậc; chim bắt chước
m0, m1 = STOW_COMPASS
hold(m0, -45, -35)
hold(m0 + 0.3, -15, -35)                                         # tay xuống túi
show(compass.root, m0 + 0.32, False)
hold(m1, 6, -35)
look(lumo, m0, 0.4, -0.9)
ry(lumo.head, m0 + 0.2, 12)
g0, g1 = GRAB_RAIL
hold(g0, 6, -40)
hold(g1, -30, -84)                                               # tay xa đặt lên tay vịn dây leo (ngang ngực)
ry(lumo.head, g1, 10)
look(lumo, g1, 0.8, -0.6)
fc(lumo, g1, "focus", 12)
PATH_Y = 0.8
lumo_at(CLIMB[0] - HOLD, BUSH_X, 0.0, -0.3)
lumo_at(CLIMB[0], BUSH_X, 0.0, PATH_Y)                           # bước vào lối nhỏ (sau bụi cây)
STEP_T = (CLIMB[1] - CLIMB[0]) / 5
x_prev, z_prev = BUSH_X, 0.0
lumo_steps = []                                                  # (nhấc chân, đặt chân, x, z): chú chim bắt chước theo


def lumo_step(t0, t1, x, z, lift=0.06):
    global x_prev, z_prev
    lumo_at(t0, x_prev, z_prev)
    lumo_at((t0 + t1) / 2, (x_prev + x) / 2, max(z_prev, z) + lift)   # nhấc chân chậm
    lumo_at(t1, x, z)
    lean(lumo, t0, 2)
    lean(lumo, (t0 + t1) / 2, 6)
    lean(lumo, t1, 2)
    lumo_steps.append((t0, t1, x, z))
    x_prev, z_prev = x, z


for k in range(1, 6):
    t = CLIMB[0] + STEP_T * (k - 1)
    lumo_step(t, t + 0.4, 0.3 * k, 0.15 * k)
    hold(t, -30, -84)
    hold(t + 0.4, -25, -86)
loop(lumo.tail, CLIMB[0], CLIMB[1], 0.7, 12, 24)
for i, t in enumerate(steps(CLIMB[0], CLIMB[1], 0.35)):
    ry(lumo.head, t, 12 if i % 2 else 8)
bl(lumo, 50.4)

# ================================================================ S15: men vách, vòng qua đầu khe; la bàn trong túi kêu dày dần
WALK = [(2.7 + 0.3 * k, LEDGE_Z) for k in range(1, 7)] + [(LEDGE_END + 0.15 + 0.3 * k, LEDGE_Z - 0.15 * (k + 1)) for k in range(3)]
w0, w1 = PATH_WALK                                               # gờ phẳng 3.0 … 4.5, rồi ba bậc xuống tới 5.35
period = (w1 - w0) / len(WALK)
lumo_at(w0 - HOLD, 1.5, 0.75)
lumo_at(w0, 2.7, LEDGE_Z)                                        # cắt cảnh: đã đi được nửa gờ
x_prev, z_prev = 2.7, LEDGE_Z
for i, (x, z) in enumerate(WALK):
    t0 = w0 + 0.05 + i * period
    lumo_step(t0, t0 + 0.6 * period, x, z, 0.05)
hold(w0, -25, -86)
look(lumo, w0, 0.9, -0.3)
ry(lumo.head, w0, 6)
loop(lumo.tail, w0, w1, 0.6, 14, 26)
fc(lumo, BEEPS_PATH[0] + 0.1, "eager", 6)
for k, tb in enumerate(BEEPS_PATH):                              # rung mạnh dần, kêu dày dần
    beep_wave(bag_beep, tb, 1.0 + 0.08 * k)
    jitter(lumo.bag, tb, tb + 0.16, 0.003 + 0.0012 * k, 0.04)
show(bag_glow, BEEPS_PATH[0], True)
twinkle(bag_glow, BEEPS_PATH[0], PRESS_STAR[0], 1.5, 0.9, 0.2)
ears(lumo, BEEPS_PATH[0], 4)
ears(lumo, BEEPS_PATH[0] + 0.1, 16)
ears(lumo, BEEPS_PATH[0] + 0.3, 6)
look(lumo, BEEPS_PATH[0] + 0.1, 0.3, -1.0)                       # liếc túi
look(lumo, BEEPS_PATH[0] + 0.7, 1.0, -0.2)                       # rồi nhìn bệ đá phía trước
bl(lumo, 57.4)

# ================================================================ S16: xuống bãi đất, tới bệ đá (cắt cảnh: hai bậc cuối)
END_X = 6.6
a0, a1 = ARRIVE
lumo_at(a0 - HOLD, x_prev, z_prev)
lumo_at(a0, 5.65, 0.3)                                           # cắt cảnh: hai bậc cuối
lumo_at(a0 + 0.2, 5.95, 0.15)
lumo_at(a0 + 0.35, 6.15, 0.05, PATH_Y)
lumo_at(a0 + 0.35 + HOLD, 6.17, 0.04, -0.3)                      # xuống bãi đất, ra trước bệ đá
lumo_at(a0 + 0.5, 6.4, 0.03)
lumo_at(a1, END_X, 0.0)
lean(lumo, a1, 0)
hold(a0, -20, -10)

# ================================================================ chú chim nhảy theo sau, bắt chước bước chậm
pos(bird.root, BIRD_FOLLOW - 0.4, BX, BZ)
scl(bird.root, BIRD_FOLLOW - 0.35, -1, 1)
scl(bird.root, BIRD_FOLLOW - 0.3, 1, 1)                          # quay theo hướng Lumo đi
bird.dir = 1
BIRD_Y = 0.45                                                   # mép ngoài bậc đá: trước bụi cây, sau thành cầu
pos(bird.root, BIRD_FOLLOW - HOLD, BX, BZ, -0.63)
pos(bird.root, BIRD_FOLLOW, BX - 0.1, BZ + 0.15, BIRD_Y)         # bay xuống bậc đầu sau lưng Lumo
pos(bird.root, BIRD_FOLLOW + 0.15, 0.8, 0.45)
pos(bird.root, BIRD_FOLLOW + 0.3, 0.3, 0.15)
for i, t in enumerate(steps(BIRD_FOLLOW, BIRD_FOLLOW + 0.25, 0.06)):
    ry(bird.wing, t, 65 if i % 2 else -35)
    ry(bird.wing_far, t, 70 if i % 2 else -30)
ry(bird.wing_far, BIRD_FOLLOW + 0.3, 0)
for t0, t1, x, z in [s for s in lumo_steps if s[0] > BIRD_FOLLOW + 0.2]:
    bx = x - 0.35                                                # sát sau Lumo, mỗi bước nhấc chân y hệt, chậm nửa nhịp
    bz = path_z(bx)
    d = 0.22
    pos(bird.root, t0 + d, bird.root.location.x, bird.root.location.z)
    scl(bird.root, t0 + d, 1, 1)
    scl(bird.root, t0 + d + 0.08, 0.92, 1.1)                     # nhón người, nhấc chân cao
    pos(bird.root, t0 + d + 0.12, (bird.root.location.x + bx) / 2, max(bird.root.location.z, bz) + 0.07)
    pos(bird.root, t1 + d, bx, bz)
    scl(bird.root, t1 + d, 1.08, 0.92)
    scl(bird.root, t1 + d + 0.1, 1, 1)
    ry(bird.wing, t0 + d, 0)
    ry(bird.wing, t0 + d + 0.12, 25)                              # cánh giang như tay giữ thăng bằng
    ry(bird.wing, t1 + d, 0)
pos(bird.root, ARRIVE[0] - HOLD, bird.root.location.x, bird.root.location.z)
pos(bird.root, ARRIVE[0], 5.3, 0.45)                             # cắt cảnh: theo xuống bậc
pos(bird.root, ARRIVE[0] + 0.35, 5.65, 0.3)
pos(bird.root, ARRIVE[0] + 0.55 - HOLD, 5.95, 0.15, BIRD_Y)
pos(bird.root, ARRIVE[0] + 0.55, 6.0, 0.08, -0.35)               # xuống bãi đất, ra trước
pos(bird.root, ARRIVE[1] + 0.2, 6.15, 0.0)

# ================================================================ S16: ấn ngôi sao đá, CẠCH; S17: phiến đá trượt mở
for t in (58.1, 58.25):                                          # sát bệ: kêu dày, rung mạnh
    beep_wave(bag_beep, t, 1.6)
    jitter(lumo.bag, t, t + 0.15, 0.014, 0.04)
show(bag_glow, PRESS_STAR[0], False)
a0, a1 = PRESS_STAR
lean(lumo, a0, 0)
lean(lumo, a0 + 0.3, 18)
a_star = reach(lumo, END_X, 0.0, 18, (STAR_C[0], STAR_C[1] + 0.03), lo=-150)
hold(a0, -20, -10)
hold(a0 + 0.3, a_star, -10)                                      # với tay đặt lên ngôi sao
hold(a1, a_star + 6, -10)                                        # ấn xuống
look(lumo, a0, 0.9, -0.6)
ry(lumo.head, a0 + 0.3, 12)
fc(lumo, a0 + 0.1, "eager", 30)
pos(pstar, CACH - 0.05, *STAR_C)
pos(pstar, CACH, STAR_C[0], STAR_C[1] - 0.03)                    # lún xuống
flash(click, CACH, 1.0)
for t, k in ((a0 + 0.45 - HOLD, -0.45), (a0 + 0.45, -0.3), (a0 + 0.65, 0.0), (CACH - 0.05, 0.0), (CACH, 0.04), (CACH + 0.35, 0.04),
             (CACH + 0.6, -0.5)):                                # cú nhìn từ trên: bàn tay vươn vào, ấn, rút ra
    pos(press_arm, t, SHOULDER[0] + REACH_DIR[0] * k, SHOULDER[1] + REACH_DIR[1] * k)
show(press_arm, a0 + 0.45, True)
show(press_arm, CACH + 0.65, False)
scl(top_star, CACH - 0.05, 1, 1)
scl(top_star, CACH, 0.86, 0.86)                                  # ngôi sao lún xuống
flash(top_click, CACH, 1.0)
show(top_map_carved, SLAB_SLIDE[0], True)
show(side_map, SLAB_SLIDE[0], True)
fc(lumo, CACH + 0.05, "wonder", 24)
ears(lumo, CACH, 5)
ears(lumo, CACH + 0.1, 20)
ears(lumo, CACH + 0.3, 8)
hold(CACH + 0.3, -40, -10)
lean(lumo, CACH + 0.4, 4)
sl0, sl1 = SLAB_SLIDE
pos(cover, sl0, 0.0, 0.0)
pos(cover, sl1, -(PX1 - SLAB_X), 0.0)                            # trượt vào dưới phiến sao
pos(top_cover, sl0, *TMAP)
pos(top_cover, sl1, TSTAR[0], TMAP[1])
look(lumo, sl0, 0.9, -0.7)

# ================================================================ S18: chú chim đậu lên mép bệ; Lumo rút bản đồ giấy
e0, e1 = BIRD_PERCH
PERCH = (PX1 - 0.02, PTOP + PDEPTH)
pos(bird.root, e0, 6.15, 0.0)
scl(bird.root, e0, 1.1, 0.9)
pos(bird.root, e0 + 0.15 - HOLD, 6.3, 0.45, -0.35)
pos(bird.root, e0 + 0.15, 6.3, 0.45, 0.0)                        # bay vòng ra sau Lumo, lên mép bệ
for t, x, z in ((e0 + 0.3, 6.9, 0.95), (e1, *PERCH)):
    pos(bird.root, t, x, z)
for i, t in enumerate(steps(e0 + 0.05, e1 - 0.05, 0.06)):
    ry(bird.wing, t, 65 if i % 2 else -35)
    ry(bird.wing_far, t, 70 if i % 2 else -30)
ry(bird.wing, e1, 0)
ry(bird.wing_far, e1, 0)
scl(bird.root, e1, -1.1, 0.88)                                   # đậu, quay về phía Lumo
scl(bird.root, e1 + 0.15, -1, 1)
bird.dir = -1
ry(bird.head, e1 + 0.3, 14)
n0, n1 = MAP_OUT
look(lumo, e0 + 0.2, 0.9, 0.3)                                   # nhìn chú chim
hold(n0, -15, -10)                                               # tay vào túi
show(map_sheet, n0 + 0.2, True)
ry(map_sheet, n0 + 0.2, 180)                                     # lại cầm ngược: rương lộn ngược
scl(map_sheet, n0 + 0.2, 0.4, 0.4)
scl(map_sheet, n1, 1, 1)
hold(n1, CHEST, -10)                                             # cầm ngang ngực
look(lumo, n1, 0.8, -0.4)
ry(lumo.head, n1, 10)
fc(lumo, n1, "eager", 10)

# ================================================================ S19: hai bản đồ; giấy cầm ngược, xoay lại: khớp; đài thiên văn chỉ có trên đá, lóe
s19 = SHOT["S21"][0]
show(top_map, s19, True)
for pw in top_paws:
    show(pw, s19, True)
ry(top_map, s19, 180)
for i, t in enumerate(steps(s19, 67.8, 0.45)):                   # nhích theo nhịp thở
    pos(top_hold, t, PMAP[0] + (0.006 if i % 2 else -0.006), PMAP[1] + (0.008 if i % 2 else -0.004))
fc(lumo, s19 + 0.2, "puzzled", 10)                               # không khớp
t0, t1 = MAP_TURN
ry(top_map, t0, 180)
ry(top_map, t1, 360)
ry(map_sheet, t0, 180)
ry(map_sheet, t1, 360)
for side, pw in zip((-1, 1), top_paws):
    pos(pw, t0 - 0.1, side * 0.33, -0.27)
    pos(pw, t0 + 0.05, side * 0.47, -0.33)                       # buông ra để xoay
    pos(pw, t1 - 0.05, side * 0.47, -0.33)
    pos(pw, t1 + 0.12, side * 0.33, -0.27)
pos(top_hold, t1 + 0.1, *PMAP)
pos(top_hold, t1 + 0.25, PMAP[0], PMAP[1] + 0.03)                # khớp: nhún một cái
pos(top_hold, t1 + 0.45, *PMAP)
hold(t0, CHEST, -10)
hold((t0 + t1) / 2, -80, -10)
hold(t1, CHEST, -10)
fc(lumo, t1 + 0.1, "happy", 10)
fc(lumo, CAM_EDGE[1], "puzzled", 10)                             # đảo này không có trên bản đồ giấy
look(lumo, CAM_EDGE[1], 0.9, -0.7)
f0, f1 = OBS_FLASH
for ob in (top_flash, side_flash):                               # lóe xanh ngọc, nhấp nháy, rồi tắt
    show(ob, f0, True)
    for i, t in enumerate(steps(f0, f1 - 0.2, 0.2)):
        s = 0.9 if i == 0 else 1.18 if i % 2 else 1.0
        scl(ob, t, s, s)
    show(ob, f1, False)

# ================================================================ S20: cùng lúc, la bàn trong túi rung TÍT TÍT TÍT; rút la bàn
for t in BEEPS_FLASH + (SHOT["S22"][0] + 0.1, SHOT["S22"][0] + 0.35):   # còn rung, kêu khi cắt về Lumo
    beep_wave(bag_beep, t, 1.6)
jitter(lumo.bag, BEEPS_FLASH[0], f1 - 0.2, 0.014, 0.04)          # rung mạnh: ngay cạnh
show(bag_glow, BEEPS_FLASH[0], True)
twinkle(bag_glow, BEEPS_FLASH[0], f1, 1.6, 1.0, 0.15)
show(bag_glow, COMPASS_OUT2[0] + 0.15, False)
fc(lumo, BEEPS_FLASH[0], "shock", 10)
ears(lumo, BEEPS_FLASH[0], 25)
ears(lumo, BEEPS_FLASH[0] + 0.3, 10)
look(lumo, BEEPS_FLASH[0] + 0.25, 0.3, -1.0)                     # nhìn túi da
ry(lumo.head, BEEPS_FLASH[0] + 0.25, 16)
lean(lumo, BEEPS_FLASH[0], 4)
lean(lumo, BEEPS_FLASH[0] + 0.1, -6)
lean(lumo, BEEPS_FLASH[0] + 0.4, 0)
x0, x1 = COMPASS_OUT2
hold(x0 - 0.4, CHEST, -10)
hold(x0 - 0.2, -60, -60)                                         # chuyển bản đồ sang tay xa
show(map_sheet, x0 - 0.15, False)
show(map_far, x0 - 0.15, True)
hold(x0 + 0.05, -15, -55)                                        # tay gần vào túi
show(compass.root, x0 + 0.15, True)
glow(compass, x0 + 0.15, 1.1)                                    # còn sáng mạnh: ngay cạnh đài thiên văn vừa lóe
hold(x1, -75, -55)
look(lumo, x1, 0.8, -0.45)
ry(lumo.head, x1, 10)
fc(lumo, x1, "eager", 10)
jitter(compass.root, x0 + 0.2, NEEDLE_ISLAND[0], 0.005, 0.05)

# ================================================================ S21: cận mặt bệ từ trên: mũi sao về đảo khắc, rồi ra chân trời; dịu xuống
s21 = SHOT["S23"]
for ob in (top_map, *top_paws):
    show(ob, s21[0], False)                                      # bản đồ giấy đã sang tay xa, ra khỏi khung
show(pov2.node, s21[0], True)
show(pov2.beep, s21[0], False)
glow(pov2, s21[0], 0.95)
twinkle(pov2.glow, s21[0], NEEDLE_ISLAND[0], 1.0, 0.9, 0.2)
jitter(pov2.root, s21[0], NEEDLE_ISLAND[0], 0.012, 0.05)         # rung mạnh tới khi mũi sao rời ngôi sao đá
jitter(pov2.root, NEEDLE_ISLAND[0], NEEDLE_HORIZON[0], 0.004, 0.07)
for c in (pov2, compass):
    for t, s in ((NEEDLE_ISLAND[1], 0.9), (DIM[0], 0.85), (DIM[1], 0.62)):
        scl(c.glow, t, s, s)                                     # dịu xuống, chỉ còn le lói
twinkle(pov2.glow, DIM[1], s21[1], 0.66, 0.56, 0.35)
twinkle(compass.glow, DIM[1], SECONDS, 0.66, 0.56, 0.35)
show(pov2.node, s21[1], False)

# ================================================================ S22, S23: "Chưa từng có hòn đảo này…"; chú chim bay đi
fc(lumo, s21[0] + 0.3, "wonder", 10)
look(lumo, NEEDLE_HORIZON[1], 1.0, 0.25)                         # nhìn ra chân trời
ry(lumo.head, NEEDLE_HORIZON[1], -4)
hold(NEEDLE_HORIZON[1], -85, -55)
ears(lumo, NEEDLE_HORIZON[1], 14)
i0, i1 = LINE_ISLAND
fc(lumo, i0 - 0.05, "eager", -4)
talk(lumo, i0, i0 + 1.3, "smile")                                # "Chưa từng có hòn đảo này…"
talk(lumo, i0 + 1.45, i1, "smile")                               # "…trên bản đồ của mình!"
hold(i0 + 0.3, -95, -55)                                         # giơ la bàn về phía chân trời
hold(i0 + 1.45, -80, -55)
hold(i0 + 1.7, -80, -85)                                         # giơ bản đồ giấy lên ở "bản đồ của mình"
hold(i1, -80, -60)
squash(lumo, i0 + 1.7, 1.03, 0.97)
squash(lumo, i0 + 1.9, 0.98, 1.03)
squash(lumo, i1, 1, 1)
look(lumo, i0 + 1.6, 0.6, -0.3)                                  # liếc bản đồ giấy
look(lumo, i1 - 0.2, 1.0, 0.25)
loop(lumo.tail, i0, SECONDS, 0.5, 22, 42)
ry(bird.head, i0 + 0.2, 0)
ry(bird.head, i0 + 0.5, 20)
fl0, fl1 = BIRD_FLY
scl(bird.root, fl0, -1, 1)
scl(bird.root, fl0 + 0.1, -1.12, 0.85)
scl(bird.root, fl0 + 0.18, 1, 1)                                 # quay về phía chân trời
bird.dir = 1
for t, x, z in ((fl0 + 0.18, PERCH[0], PERCH[1] + 0.02), (fl0 + 0.4, PERCH[0] + 0.3, PERCH[1] + 0.25),
                (fl0 + 0.7, PERCH[0] + 0.9, PERCH[1] + 0.6), (fl1, PERCH[0] + 2.2, PERCH[1] + 1.1), (SECONDS, PERCH[0] + 3.1, PERCH[1] + 1.5)):
    pos(bird.root, t, x, z)
for i, t in enumerate(steps(fl0 + 0.15, SECONDS, 0.06)):
    ry(bird.wing, t, 65 if i % 2 else -35)
    ry(bird.wing_far, t, 70 if i % 2 else -30)
look(lumo, fl0 + 0.3, 1.0, 0.6)                                  # nhìn theo chú chim
ry(lumo.head, fl0 + 0.4, -10)
fc(lumo, fl0 + 0.3, "happy", -10)
ears(lumo, fl0 + 0.3, 10)
bl(lumo, 85.6)

# ================================================================ mũi sao: ngắm mục tiêu trong thế giới, từng khung
# chỉ ngôi sao đá, chuyển sang đảo khắc (NEEDLE_ISLAND) rồi ra chân trời (NEEDLE_HORIZON): quay theo góc, lắc khi tới nơi;
# mỗi hai khung một key
bear_side = swing(SIDE_TARGETS, (NEEDLE_ISLAND, NEEDLE_HORIZON))              # cú ngang
bear_top = swing(TOP_TARGETS, (NEEDLE_ISLAND, NEEDLE_HORIZON))                # cú nhìn mặt bệ từ trên
aim(compass, COMPASS_OUT[0] + 0.15, SWAP, bearing=bear_side, step=2)   # bắt đầu ở khung la bàn vừa hiện
aim(compass_far, SWAP, LOOK_COMPASS, bearing=bear_side, step=2)
aim(compass, LOOK_COMPASS - 0.1, STOW_COMPASS[0] + 0.4, bearing=bear_side, step=2)
aim(compass, COMPASS_OUT2[0] + 0.1, SECONDS, bearing=bear_side, step=2)
aim(pov1, SHOT["S4"][0], SHOT["S4"][1], bearing=bear_side, step=2)
aim(pov1, SHOT["S11"][0], SHOT["S11"][1], bearing=bear_side, step=2)
aim(pov2, SHOT["S23"][0], SHOT["S23"][1], bearing=bear_top, step=2)
bpy.context.scene.frame_set(1)

# ================================================================ máy quay, render
CAMS = {"S1": (-0.4, 0.62, 3.2), "S2": (3.35, 0.75, 9.8), "S3": (-0.1, 0.48, 2.4), "S4": (4.6, 0.13, 6.0), "S5": (-0.1, 0.48, 2.4),
        "S6": (0.55, 0.6, 3.2), "S7": (2.9, 0.0, 6.0), "S8": (0.55, 0.5, 2.8), "S9": (BX, 0.66, 0.9), "S10": (0.65, 0.5, 2.4),
        "S11": (4.6, 0.13, 6.0), "S12": (0.25, 0.62, 2.8), "S13": (BX, 0.66, 0.9), "S14": (0.0, 0.62, 1.7), "S15": (0.45, 0.75, 3.0),
        "S16": (0.65, 0.35, 1.4), "S17": (4.1, 0.5, 7.4), "S18": (6.3, 0.55, 2.6), "S19": (TX - 0.15, 0.36, 2.3), "S20": (6.85, 0.62, 2.4),
        "S21": (TX + 0.3, -0.06, 2.9), "S22": (6.85, 0.62, 2.4), "S23": (TX, 0.1, 2.6), "S24": (7.35, 0.75, 3.2), "S25": (8.0, 0.95, 4.0)}
cameras(SHOTS, CAMS)


def track(shot, keys):
    """Máy của một cú đi qua các key (giây, (tâm X, tâm Z, bề ngang)); key đầu là khung của CAMS."""
    cam = bpy.data.objects[f"Cam_{shot}"]
    for t, (cx, cz, w) in [(keys[0][0], CAMS[shot])] + keys[1:]:
        key(cam, "location", t, (cx, -10.0, cz))
        key(cam.data, "ortho_scale", t, w)


track("S15", [(CLIMB[0], None), (SHOT["S15"][1], (0.75, 0.85, 3.0))])            # lia lên theo Lumo
track("S16", [(SHOT["S16"][0], None), (SHOT["S16"][1], (1.5, 0.8, 1.4))])          # theo chú chim lên từng bậc
track("S21", [(CAM_EDGE[0], None), (CAM_EDGE[1], (TX + 0.32, 0.02, 1.7)),          # tới mép phải hai bản đồ,
              (CAM_PAN[0] + 1.1, (TX + 0.45, 0.17, 1.45)), (CAM_PAN[0] + 2.2, (TX + 0.45, -0.06, 1.45)),   # đài thiên văn khắc, xuống mây trống
              (CAM_PAN[1], (TX + 0.38, 0.02, 1.7))])                               # lùi ra thấy cả hai cho cú lóe
finish(SECONDS, OUT_BLEND, tuple(round(t0 + 0.6 * (t1 - t0), 2) for _, t0, t1 in SHOTS))
