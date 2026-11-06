"""
Phế tích cổ ngoài trời của EP000A, dùng chung cho previz 2D Cảnh 2 và Cảnh 3 (canh02/build_shot.py, canh03/build_shot.py
nạp file này từ thư mục tập). Nối tiếp bố cục cuối Cảnh 1 (canh01/build_shot.py): nền rêu Z = LOW_Z, đống lá X -7.3,
phiến đá rêu -8.05, phiến đá có ánh vàng trên bậc đá chân tường -8.75, tường phế tích từ -9 sang trái (đầu tường ở -9 là
mặt đứng Lumo áp tai, gõ). Tường kéo dài tới -16.6: mảng dây leo rủ che phù điêu đám mây ở RELIEF, cửa thấp ở DOOR_X
(bên trái phù điêu, mở vào vòm đá), thảm rêu dày chân tường. Ký hiệu khắc chỉ là mây, sao hoa gió (rose), mặt la bàn;
không dáng nơi thờ tự. Gọi build_ruins() sau start(FPS); trả về namespace các mảnh cần diễn. Mây khắc (cloud_parts), bướm
phát sáng và các hàm diễn la bàn nằm ở pipeline/cutout.py.
"""
import math
import random

import bmesh
from cutout import SimpleNamespace, WHITE, band, cloud_parts, ell, leaf_pts, mat, node, part, rect, rose, rrect, star

SKY, CLOUD, GRASS = "#CDE9F7", "#F1F6FA", "#A5CF63"
LEAF_COLS = ("#C97B3C", "#E09A52", "#B5642E", "#D98A45")
STONE, STONE_D, STONE_L, MOSS = "#C9BBA2", "#A8987E", "#D9CCB4", "#86B24C"
LOW_Z = -1.3                                                    # nền rêu dưới chân dốc (Cảnh 1)
GLOW_Z = LOW_Z + 0.14                                           # mặt bậc đá chân tường
WALL_END, WALL_TOP, WALL_LEFT = -9.0, 0.12, -16.6
SLAB = (-8.75, GLOW_Z + 0.03)                                   # tâm phiến đá có ánh vàng (Cảnh 1)
SLAB_W, SLAB_H = 0.42, 0.07
COMPASS_SPOT = (-8.73, GLOW_Z + 0.05)                           # la bàn nằm trong hốc dưới phiến đá
MOSS_STONE = -8.05                                              # phiến đá rêu con bướm đậu
STONE_TOP = (-8.03, LOW_Z + 0.215)
PILE_X = -7.3
RELIEF = (-12.0, -0.7)                                          # tâm phù điêu đám mây (khớp xoay)
VINES = (-12.6, -11.4)                                          # mảng dây leo rủ che phù điêu
DOOR_X, DOOR_W, DOOR_H = -13.25, 0.7, 1.12                      # cửa thấp vừa tầm Lumo
CARPET = (-14.1, -11.3)                                         # thảm rêu dày chân tường
CARPET_H = 0.13
SLOPE = [(-3.85, 0.02), (-3.95, 0.01), (-4.05, -0.02), (-4.15, -0.06), (-4.3, -0.12), (-6.6, -1.18),
         (-6.8, -1.25), (-7.0, -1.29), (-7.2, LOW_Z)]


def ground_z(x):
    if x >= SLOPE[0][0]:
        return 0.0
    for (x0, z0), (x1, z1) in zip(SLOPE, SLOPE[1:]):
        if x1 <= x <= x0:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return LOW_Z


def swirl(r, cx, cz, th, a0=200, a1=520):
    """Xoắn mây (nét khắc)."""
    pts = []
    for k in range(25):
        a = math.radians(a0 + (a1 - a0) * k / 24)
        rr = r * (0.35 + 0.65 * k / 24)
        pts.append((cx + rr * math.cos(a), cz + rr * math.sin(a)))
    return band(pts, th)


def build_ruins():
    random.seed(11)
    R = SimpleNamespace()
    # --- trời, đảo xa, biển mây, rừng xa (như Cảnh 1)
    part("Sky", None, [(rect(-24, -5, 6, 7), SKY)], 3.6)
    part("SkyClouds", None, [(ell(0.45, 0.16, cx, cz), "#F7FBFD") for cx, cz in ((-6.8, 1.55), (-6.3, 1.62), (-9.6, 1.45),
                                                                              (-12.5, 1.7), (-12.0, 1.62), (-15.2, 1.5))], 3.55)
    islands = []
    for cx, cz, s in ((-4.1, 2.25, 0.45), (-8.9, 1.25, 0.4), (-13.6, 1.35, 0.5)):
        rock = [(cx - 0.55 * s, cz), (cx + 0.55 * s, cz), (cx + 0.42 * s, cz - 0.22 * s), (cx + 0.2 * s, cz - 0.42 * s),
                (cx, cz - 0.62 * s), (cx - 0.22 * s, cz - 0.45 * s), (cx - 0.45 * s, cz - 0.25 * s)]
        islands += [(rock, "#B48E72"), (ell(0.58 * s, 0.1 * s, cx, cz), "#93C95A"),
                    (rect(cx + 0.28 * s, 1.0, cx + 0.38 * s, cz - 0.02), "#E4F5FF")]
        islands += [(ell(0.13 * s, 0.12 * s, cx + dx * s, cz + 0.16 * s), col) for dx, col in ((-0.3, "#7DB843"), (0.32, "#F2B3CB"))]
    part("Islands", None, islands, 3.3)
    part("CloudSea", None, [(rect(-24, -5, 6, 0.95), CLOUD)] + [(ell(0.5, 0.2, -24 + 0.7 * i, 0.95 + 0.04 * (i % 3)), CLOUD)
                                                                for i in range(44)], 3.2)
    far = [(6, -0.25), (-5.6, -0.25), (-7.0, -0.55), (-24, -0.55)]

    def far_z(x):
        for (x0, z0), (x1, z1) in zip(far, far[1:]):
            if x1 <= x <= x0:
                return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
        return far[-1][1]

    part("FarTrees", None, [(ell(0.3, 0.2, x, far_z(x) + 0.13), "#C6E4A6" if i % 2 else "#B9DD97")
                            for i, x in enumerate(-24 + 0.42 * k for k in range(72)) if i % 7 not in (3, 4)], 2.62)
    part("FarFloor", None, [(far + [(-24, -5), (6, -5)], "#C2E2A0")], 2.6)
    # --- nền: dốc lá khô từ Cảnh 1, nền rêu dưới chân dốc
    R.ground = part("Ground", None, [([(6, 0.02)] + SLOPE + [(-24, LOW_Z), (-24, -5), (6, -5)], GRASS)], 2.0)
    litter = [(SLOPE[1:-1] + [(x, max(z - 0.3, LOW_Z)) for x, z in reversed(SLOPE[1:-1])], "#CC8A4A")]
    for i in range(60):
        lx = -3.95 - (i % 30) * 0.105 - 0.05 * (i // 30)
        litter.append((leaf_pts(lx, max(ground_z(lx) - 0.1 * (i // 30), LOW_Z + 0.03) + random.uniform(-0.03, 0.03), 1.4,
                                random.uniform(-50, 50)), LEAF_COLS[i % 4]))
    part("SlopeLeaves", None, litter, 1.93)
    tufts = []
    for gx in (-5.5, -6.3, -8.5, -9.6, -10.9, -14.6, -15.4):
        gz = ground_z(gx) - 0.12
        tufts += [([(gx - 0.03, gz), (gx + 0.03, gz), (gx + 0.005, gz + 0.08)], "#7DB843"),
                  ([(gx + 0.01, gz), (gx + 0.05, gz), (gx + 0.06, gz + 0.06)], "#7DB843")]
    flowers = [(ell(0.022, 0.022, fx, fz), col) for fx, fz, col in ((-9.3, -1.42, "#F7A8C8"), (-7.9, -1.45, WHITE),
                                                                    (-10.6, -1.44, "#B79BE8"), (-14.8, -1.43, "#F7A8C8"),
                                                                    (-15.6, -1.46, WHITE))]
    part("Tufts", None, tufts + flowers, 1.85)

    # --- tường phế tích: từ -9 (đầu tường) sang trái tới -16.6
    blocks = [(rect(WALL_LEFT, LOW_Z, WALL_END, WALL_TOP), STONE_D)]
    rows = ((LOW_Z, -0.85, (-16.6, -15.7, -14.8, -13.9, -12.6, -11.7, -10.8, -9.9, -9.0)),
            (-0.85, -0.35, (-16.4, -15.4, -14.4, -13.4, -12.4, -11.3, -10.3, -9.25)),
            (-0.35, WALL_TOP, (-16.2, -15.0, -14.0, -13.0, -12.2, -11.0, -10.0, -9.45)))
    for row, (z0, z1, xs) in enumerate(rows):
        for x0, x1 in zip(xs, xs[1:]):
            blocks.append((rrect(x1 - x0 - 0.04, z1 - z0 - 0.04, 0.04, (x0 + x1) / 2, (z0 + z1) / 2),
                           STONE if (row + int(x0)) % 2 else STONE_L))
    blocks.append((rect(WALL_END - 0.07, LOW_Z, WALL_END, WALL_TOP), "#9A8B72"))   # mặt đầu tường (dày tường), chỗ áp tai
    for cx, cz in ((-9.95, -0.6), (-15.3, -0.62)):              # phù điêu mặt la bàn: sao hoa gió
        blocks += [(ell(0.2, 0.2, cx, cz), STONE_D), (ell(0.17, 0.17, cx, cz), STONE), (rose(0.15, cx, cz), STONE_D),
                   (ell(0.03, 0.03, cx, cz), STONE)]
    blocks += [(ell(0.12, 0.07, cx, -0.12), STONE_D) for cx in (-14.75, -14.6, -14.45)]   # mây khắc nhỏ
    blocks += [(ell(rx, 0.06, cx, WALL_TOP + 0.02), MOSS) for rx, cx in ((0.6, -15.6), (0.5, -13.9), (0.5, -11.8), (0.4, -10.6),
                                                                          (0.25, -9.6))]
    # cửa thấp lúc đóng: chỉ một đường khe mờ trên tường
    dx0, dx1, dtop = DOOR_X - DOOR_W / 2, DOOR_X + DOOR_W / 2, LOW_Z + DOOR_H
    seam = [(dx0, LOW_Z), (dx0, dtop - DOOR_W / 2)] + [(DOOR_X - DOOR_W / 2 * math.cos(math.pi * k / 12),
                                                        dtop - DOOR_W / 2 + DOOR_W / 2 * math.sin(math.pi * k / 12)) for k in range(13)]
    seam += [(dx1, LOW_Z)]
    blocks.append((band(seam, 0.012), "#B3A389"))
    R.wall = part("Ruins", None, blocks, 1.2)
    R.door_arch = [(dx0, LOW_Z)] + seam[1:-1] + [(dx1, LOW_Z)]
    # cửa thấp: khoảng tối bên trong, ánh sáng ban ngày lọt vào, cánh cửa đá xoay vào trong (bản lề mép trái)
    R.door_dark = part("Door_Dark", None, [(R.door_arch, "#5E5040"),
                                           ([(dx0 + 0.04, LOW_Z), (dx1 - 0.04, LOW_Z), (DOOR_X + 0.12, LOW_Z + 0.42),
                                             (DOOR_X - 0.1, LOW_Z + 0.42)], "#E8D7A6")], 1.17)
    R.door = node("Door", None, (dx0, LOW_Z), 1.15)
    door_blocks = [([(x - dx0, z - LOW_Z) for x, z in R.door_arch], STONE)]
    door_blocks += [(rrect(0.3, 0.42, 0.03, 0.18, 0.24), STONE_L), (rrect(0.3, 0.42, 0.03, 0.52, 0.24), STONE),
                    (rrect(0.3, 0.42, 0.03, 0.18, 0.7), STONE), (rrect(0.3, 0.42, 0.03, 0.52, 0.7), STONE_L)]
    R.door_panel = part("Door_Panel", R.door, door_blocks)
    # --- phù điêu đám mây: tấm mây xoay quanh tâm, hốc tròn tối phía sau; các đường mây ánh lên
    R.relief_back = part("Relief_Recess", None, [(ell(0.46, 0.36, *RELIEF), "#8E7F67")], 1.18)
    R.relief = node("Relief", None, RELIEF, 1.16)
    part("Relief_Cloud", R.relief, cloud_parts(0.82, 0.52, 0.0, 0.02) + [(swirl(0.09, -0.2, 0.0, 0.02), STONE_D), (swirl(0.11, 0.08, 0.06, 0.02), STONE_D),
                                   (swirl(0.07, 0.27, -0.04, 0.018), STONE_D), (rrect(0.66, 0.025, 0.012, 0.0, -0.21), STONE_D)])
    R.relief_glow = part("Relief_Glow", R.relief, [(swirl(0.09, -0.2, 0.0, 0.03), "#FFD95A"), (swirl(0.11, 0.08, 0.06, 0.03), "#FFD95A"),
                                                   (swirl(0.07, 0.27, -0.04, 0.028), "#FFD95A"),
                                                   (rrect(0.66, 0.035, 0.017, 0.0, -0.21), "#FFD95A")], -0.004)
    # --- mảng dây leo rủ che phù điêu: hai nửa, khớp ở mép trên, vạch ra hai bên
    R.vines = []
    for side, (x0, x1) in enumerate(((VINES[0], (VINES[0] + VINES[1]) / 2), ((VINES[0] + VINES[1]) / 2, VINES[1]))):
        pivot = (x0 if side == 0 else x1, WALL_TOP)
        nd = node(f"Vines{side}", None, pivot, 0.95)
        shapes = []
        for k in range(6):
            vx = x0 + (x1 - x0) * (k + 0.5) / 6 - pivot[0]
            length = 1.15 + 0.12 * math.sin(k * 1.7 + side)
            pts = [(vx + 0.025 * math.sin(j * 1.3 + k), -length * j / 8) for j in range(9)]
            shapes.append((band(pts, 0.03), "#4F8A2E"))
            shapes += [(leaf_pts(x + (0.025 if j % 2 else -0.025), z, 2.2, 35 if j % 2 else -35), "#6FAE45" if (j + k) % 2 else "#86C04E")
                       for j, (x, z) in enumerate(pts) if j > 0]
        shapes += [(ell(0.32, 0.1, (x0 + x1) / 2 - pivot[0], 0.0), "#5E9437")]
        part(f"Vines{side}_Shape", nd, shapes)
        R.vines.append(nd)
    # dây leo trên tường (Cảnh 1) và cây phủ rễ qua tường
    vines = []
    for vx, vz0, vz1 in ((-9.5, 0.12, -0.75), (-10.35, 0.15, -0.3), (-11.05, 0.12, -0.9), (-9.15, -0.3, -1.0), (-14.0, 0.12, -0.6),
                         (-15.9, 0.12, -0.8)):
        pts = [(vx + 0.03 * math.sin(k), vz0 + (vz1 - vz0) * k / 6) for k in range(7)]
        vines.append((band(pts, 0.025), "#5E9437"))
        vines += [(leaf_pts(x + 0.03, z, 1.3, 30 if k % 2 else -30), "#7DB843") for k, (x, z) in enumerate(pts) if k % 2]
    part("WallVines", None, vines, 1.15)
    part("RuinTree", None, [([(-10.75, LOW_Z), (-9.9, LOW_Z), (-10.05, -0.7), (-10.12, 0.2), (-10.18, 0.9), (-10.42, 0.9), (-10.45, 0.2),
                              (-10.5, -0.7)], "#8B5E3C"),
                            (band([(-10.1, 0.0), (-9.7, 0.12), (-9.5, -0.2), (-9.4, -0.8)], 0.06), "#8B5E3C"),
                            (band([(-10.4, 0.1), (-10.8, 0.14), (-11.0, -0.3)], 0.05), "#8B5E3C"),
                            (ell(1.0, 0.55, -10.3, 1.3), "#7DB843"), (ell(0.6, 0.4, -9.5, 1.0), "#86C04E"),
                            (ell(0.6, 0.4, -11.2, 1.05), "#86C04E")], 1.1)
    part("RuinTree2", None, [([(-16.2, LOW_Z), (-15.6, LOW_Z), (-15.75, 0.4), (-15.85, 1.0), (-16.05, 1.0), (-16.05, 0.4)], "#8B5E3C"),
                             (ell(0.9, 0.5, -15.9, 1.35), "#86C04E"), (ell(0.5, 0.35, -15.2, 1.1), "#7DB843")], 1.1)
    # --- bậc đá chân tường, phiến đá, ánh vàng, phiến đá rêu (Cảnh 1)
    part("Step", None, [(rrect(1.1, 0.16, 0.03, -9.0, LOW_Z + 0.06), STONE_D), (ell(0.3, 0.04, -9.2, GLOW_Z), MOSS)], 0.7)
    part("Slabs", None, [(rrect(0.3, 0.06, 0.02, -9.3, LOW_Z + 0.015), "#B8AA92"),
                         (rrect(0.25, 0.05, 0.02, -8.3, LOW_Z + 0.01), "#B8AA92")], 0.6)
    part("Hollow", None, [(ell(0.16, 0.035, COMPASS_SPOT[0], GLOW_Z + 0.01), "#7E6F58")], 0.66)   # hốc nông dưới phiến đá
    R.slab = node("Slab", None, (SLAB[0] - SLAB_W / 2, SLAB[1] - SLAB_H / 2), 0.6)          # khớp ở mép trái
    part("Slab_Shape", R.slab, [(rrect(SLAB_W, SLAB_H, 0.025, SLAB_W / 2, SLAB_H / 2), "#B8AA92"),
                                (ell(0.1, 0.02, SLAB_W * 0.7, SLAB_H * 0.9), MOSS)])
    R.glow = part("GoldGlow", None, [(ell(0.34, 0.11), "#FFE9A6"), (ell(0.2, 0.06), "#FFF6D2")]
                  + [(band([(dx * 0.4, 0.02), (dx, 0.32)], 0.025), "#FFF0B8") for dx in (-0.16, 0.0, 0.16)], 0.62, (SLAB[0], GLOW_Z + 0.05))
    R.glint = part("GoldGlint", None, [(star(0.08, 0, 0, 4, 0.3), "#FFD54F")], 0.58, (-8.6, GLOW_Z + 0.09))
    part("MossStone", None, [(ell(0.21, 0.2, MOSS_STONE, LOW_Z, 0, 180), "#A9A08F"), (ell(0.18, 0.05, MOSS_STONE, LOW_Z + 0.17), MOSS)],
         -0.55)
    # --- mảnh nền phía trước Lumo che phần người lún dưới mặt đất ở đống lá (chung mesh với nền, như Cảnh 1)
    bm = bmesh.new()
    bm.from_mesh(R.ground.data)
    bm.faces.new([bm.verts.new((x, -0.45 - R.ground.location.y, z)) for x, z in rect(-9.2, -5, -6.5, LOW_Z)])
    # thảm rêu dày chân tường: phía trước Lumo, che bàn chân khi Lumo lội trên thảm, đỡ Lumo khi ngã
    c0, c1 = CARPET
    carpet = [(c0, LOW_Z)] + [(c0 + (c1 - c0) * k / 30, LOW_Z + CARPET_H * (1 - abs(2 * k / 30 - 1) ** 6) + 0.012 * math.sin(k * 2.1))
                              for k in range(31)] + [(c1, LOW_Z), (c1, -5), (c0, -5)]
    R.ground.data.materials.append(mat("#7FB045"))
    f = bm.faces.new([bm.verts.new((x, -0.46 - R.ground.location.y, z)) for x, z in carpet])
    f.material_index = len(R.ground.data.materials) - 1
    bm.to_mesh(R.ground.data)
    bm.free()
    R.carpet_z = LOW_Z + CARPET_H
    R.pile = node("LeafPile", None, (PILE_X, LOW_Z), -0.5)
    part("PileLeaf", None, [(leaf_pts(0.0, 0.0, 2.6, 15), "#9A4B1F"), (band([(-0.08, -0.02), (0.08, 0.02)], 0.006), "#6E3415")],
         -0.6, (-6.98, -0.97)).rotation_euler = (0.0, math.radians(25), 0.0)   # chiếc lá rơi khỏi trán cuối Cảnh 1
    part("LeafPile_Shape", R.pile, [(ell(0.52, 0.45, 0, 0, 0, 180), "#C9803F")]
         + [(leaf_pts(0.45 * math.cos(math.radians(a)) * rr, 0.4 * math.sin(math.radians(a)) * rr, 1.6, a * 1.7), LEAF_COLS[k % 4])
            for k, (a, rr) in enumerate((a, rr) for rr in (0.95, 0.7, 0.4) for a in range(15, 170, 22))])
    return R
