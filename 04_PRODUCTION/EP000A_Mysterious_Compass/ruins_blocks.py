"""
Bối cảnh khối dùng chung của tập 000A (previz khối, 04_PRODUCTION/SEEDANCE.md): mặt đất rừng mây, dốc lá khô, nền rêu,
biển mây, đảo lơ lửng, thác, hàng cây, phế tích cổ (tường, đá đỉnh tường, cây mọc trên tường, bậc đá, phiến đá có ánh
vàng, phiến đá rêu, đống lá), mặt trời, bầu trời; con bướm phát sáng. canh01_blocks.py và canh02_blocks.py dựng chung
từ đây nên chỗ nối hai cảnh khớp nhau; phần chỉ có ở một cảnh (đường rừng, vách đá của Cảnh 1; tường kéo dài, mảng dây
leo của Cảnh 2) nằm ở file của cảnh đó hoặc ở build_far_wall().
Toạ độ (m): đất (mặt đường rừng) ở Z 0, máy quay phía -Y nhìn về +Y. Mép dốc lá khô -3.85, chân dốc nền rêu Z LOW_Z ở
-7.2; đống lá PILE_AT; phiến đá rêu -8.05 (Y -0.1, mặt trên STONE_TOP); bậc đá X -9.75…-8.65, Y 0.3…0.9, cao 0.16;
phiến đá có ánh vàng GLOW_AT (-9.35, Y 0.55) trên bậc đá; tường phế tích Y 0.9…1.3, đỉnh Z 0.12, đầu tường (mặt đứng
quay về +X) ở X WALL_END = -9, Cảnh 1 dựng tới -12.6, build_far_wall() kéo tiếp tới -16.6 (mảng dây leo che phù điêu
đám mây ở RELIEF, như previz 2D ../../03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/ruins.py).
"""
import math
from types import SimpleNamespace

import bpy
from mathutils import Vector

from blocks import COLS, add_obj, box_bm, cyl_bm, empty, material, prism, rod, rot, sphere_bm

LOW_Z = -1.3                                                     # nền rêu dưới chân dốc
SLOPE = [(-3.85, 0.0), (-3.95, -0.01), (-4.05, -0.04), (-4.15, -0.08), (-4.3, -0.14), (-6.6, -1.18), (-6.8, -1.25),
         (-7.0, -1.29), (-7.2, LOW_Z)]                           # mép tròn, dốc thoải khoảng 25°, chân dốc êm
PILE_AT = Vector((-7.3, 0.0, LOW_Z))
STONE_TOP = Vector((-8.03, -0.1, LOW_Z + 0.22))
GLOW_AT = Vector((-9.35, 0.55, LOW_Z + 0.2))
STEP_TOP = LOW_Z + 0.16                                          # mặt bậc đá chân tường
SLAB_SIZE = (0.42, 0.3, 0.06)                                    # phiến đá có ánh vàng, tâm (GLOW_AT.x, GLOW_AT.y, LOW_Z + 0.21)
WALL_END, WALL_Y, WALL_TOP = -9.0, (0.9, 1.3), LOW_Z + 1.42      # đầu tường, mặt trước và sau, đỉnh tường
WALL_LEFT = -16.6
RELIEF = Vector((-12.0, WALL_Y[0], -0.7))                        # tâm phù điêu đám mây sau mảng dây leo (mũi sao chỉ vào đây)
VINES = (-12.6, -11.4)                                           # mảng dây leo rủ che phù điêu


def ground_z(x):
    if x >= SLOPE[0][0]:
        return 0.0
    for (x0, z0), (x1, z1) in zip(SLOPE, SLOPE[1:]):
        if x1 <= x <= x0:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return LOW_Z


def set_materials():
    """Vật liệu bối cảnh xám (đặt tên cố định: material() trả lại cái đã có)."""
    return SimpleNamespace(
        grey=material("M_Ground", (0.42, 0.41, 0.39), 0.9),
        moss=material("M_MossStone", (0.27, 0.29, 0.26), 0.9),
        litter=material("M_LeafLitter", (0.26, 0.25, 0.24), 0.95),
        trunk=material("M_Trunk", (0.27, 0.26, 0.25), 0.9),
        canopy=material("M_Canopy", (0.46, 0.47, 0.45), 0.9),
        stone=material("M_Stone", (0.6, 0.59, 0.57), 0.8),
        island=material("M_Island", (0.52, 0.51, 0.5), 0.9),
        sea=material("M_CloudSea", (0.86, 0.88, 0.9), 0.9, emit=((0.9, 0.92, 0.95), 0.4)),
        fall=material("M_Waterfall", (0.85, 0.88, 0.92), 0.5, emit=((0.9, 0.93, 0.96), 0.4)),
        gold=material("M_GoldGlow", (1.0, 0.75, 0.15), 0.3, emit=((1.0, 0.7, 0.1), 5.0)),
        step=material("M_StepDark", (0.33, 0.32, 0.3), 0.9),       # bậc đá, phiến đá sẫm để viền vàng nổi lên
    )


def build_ruins():
    """Mặt đất, dốc, nền rêu, biển mây, đảo, thác, hàng cây, phế tích, mặt trời, bầu trời. Trả về các vật cần diễn."""
    m = set_materials()
    add_obj("Ground", box_bm((18.0, 18.0, 1.0), (5.08, -1.0, -0.5)), m.grey, "SET")                # X -3.85…14, Y -10…8
    add_obj("Slope", prism(SLOPE + [(-7.2, -2.5), (-3.85, -2.5)], -10.0, 8.0), m.grey, "SET")
    add_obj("Lowland", box_bm((9.0, 18.0, 1.0), (-11.7, -1.0, LOW_Z - 0.5)), m.grey, "SET")
    add_obj("SlopeLeaves", prism([(x + 0.0, z + 0.02) for x, z in SLOPE[1:-1]] + [(x, z - 0.05) for x, z in reversed(SLOPE[1:-1])],
                                 -2.5, 3.0), m.litter, "SET")      # lớp lá khô dày phủ kín sườn dốc
    add_obj("CloudSea", box_bm((120.0, 80.0, 0.1), (0, 50.0, -4.0)), m.sea, "SET")             # biển mây sau mép đảo (Y 8)
    bm = None
    ISL = ((-3.0, 26.0, 11.0, 4.5), (7.0, 30.0, 13.5, 3.2), (1.5, 34.0, 16.0, 2.0), (-11.0, 28.0, 9.0, 3.0))   # giữa khung lúc máy ngửa
    for cx, cy, cz, s in ISL:
        bm = cyl_bm(0.0, s * 1.4, (cx, cy, cz - s * 0.7), bm=bm, cone_top=s, segs=12)          # đảo lơ lửng: nón chúc xuống
        bm = sphere_bm(s, (cx, cy, cz), (1.0, 1.0, 0.2), bm=bm, segs=12)
    add_obj("Islands", bm, m.island, "SET")
    bm = None
    for cx, cy, cz, s in (ISL[0], ISL[1], ISL[3]):
        bm = box_bm((0.5 * s, 0.2, cz + 4.0), (cx + 0.5 * s, cy - 0.3 * s, (cz - 4.0) / 2), bm=bm)   # thác đổ xuống biển mây
    add_obj("Waterfalls", bm, m.fall, "SET")
    for i, (x, y, h, r) in enumerate(((-3.2, 1.6, 1.3, 0.6), (-1.85, 1.9, 1.1, 0.5), (-0.55, 1.5, 1.4, 0.62), (-5.0, 3.0, 1.5, 0.7),
                                      (2.0, 3.5, 1.6, 0.7), (-2.5, 4.5, 1.5, 0.7), (0.8, 5.0, 1.6, 0.8), (-6.0, 2.2, 1.2, 0.55))):
        z0 = ground_z(x) if y < 2.5 else 0.0
        rod(f"Tree{i}_Trunk", (x, y, z0 - 0.1), (x + 0.05, y, z0 + h), 0.09, m.trunk, "SET")
        add_obj(f"Tree{i}_Canopy", sphere_bm(r, (x + 0.05, y, z0 + h + r * 0.5), (1.3, 1.0, 0.75)), m.canopy, "SET")
    # phế tích cổ dưới chân dốc, cây cối phủ; bậc đá, phiến đá có ánh vàng, phiến đá rêu, đống lá
    add_obj("Ruins_Wall", box_bm((3.6, 0.4, 1.42), (-10.8, 1.1, LOW_Z + 0.71)), m.stone, "SET")
    bm = None
    for cx, cz, w, h in ((-9.3, 0.0, 0.6, 0.3), (-10.4, 0.15, 0.8, 0.25), (-11.8, 0.05, 0.9, 0.3)):
        bm = box_bm((w, 0.42, h), (cx, 1.05, cz), bm=bm)            # đá đỉnh tường lởm chởm
    add_obj("Ruins_Top", bm, m.stone, "SET")
    rod("RuinTree_Trunk", (-10.3, 1.5, LOW_Z), (-10.25, 1.5, 0.9), 0.22, m.trunk, "SET")
    add_obj("RuinTree_Canopy", sphere_bm(1.0, (-10.25, 1.5, 1.3), (1.4, 1.0, 0.6)), m.canopy, "SET")
    rod("RuinTree_Root", (-10.1, 1.35, 0.1), (-9.4, 0.9, -0.8), 0.06, m.trunk, "SET")             # rễ phủ qua tường
    add_obj("Step", box_bm((1.1, 0.6, 0.16), (-9.2, 0.6, LOW_Z + 0.08)), m.step, "SET")
    slab = add_obj("Slab", box_bm(SLAB_SIZE, (GLOW_AT.x, GLOW_AT.y, LOW_Z + 0.21)), m.step, "SET")
    glow = add_obj("GoldGlow", box_bm((0.6, 0.48, 0.02)), m.gold, "PROPS", loc=(GLOW_AT.x, GLOW_AT.y, LOW_Z + 0.165))   # dưới phiến đá
    add_obj("MossStone", sphere_bm(0.22, (-8.05, -0.1, LOW_Z), (1.0, 0.8, 1.0)), m.moss, "SET")
    pile = add_obj("LeafPile", sphere_bm(0.55, scale=(1.0, 0.8, 0.85)), m.litter, "SET", loc=PILE_AT)

    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    COLS["SET"].objects.link(sun)
    sun.data.energy, sun.data.angle = 3.5, math.radians(4)
    sun.rotation_euler = (math.radians(50), 0, math.radians(-25))
    world = bpy.data.worlds.new("Sky")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.50, 0.66, 0.92, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9
    return SimpleNamespace(mats=m, slab=slab, glow=glow, pile=pile)


def build_far_wall():
    """Tường phế tích kéo tiếp từ -12.6 tới WALL_LEFT, đá đỉnh tường, mảng dây leo rủ che phù điêu (Cảnh 2 trở đi; Cảnh
    1 không thấy đoạn này). Dây leo là nhiều sợi dọc sẫm, dày, phủ kín một mảng tường, rủ từ đỉnh tới quá nửa tường:
    nhìn xiên dọc tường vẫn thấy rõ."""
    m = set_materials()
    vine_m = material("M_Vines", (0.22, 0.25, 0.21), 0.95)
    add_obj("Ruins_WallFar", box_bm((-12.6 - WALL_LEFT, 0.4, 1.42), ((WALL_LEFT - 12.6) / 2, 1.1, LOW_Z + 0.71)), m.stone, "SET")
    bm = None
    for cx, cz, w, h in ((-13.3, 0.0, 0.7, 0.28), (-14.6, 0.12, 0.9, 0.25), (-15.9, 0.02, 0.8, 0.3)):
        bm = box_bm((w, 0.42, h), (cx, 1.05, cz), bm=bm)
    add_obj("Ruins_TopFar", bm, m.stone, "SET")
    bm = None
    n = 14
    for k in range(n):
        x = VINES[0] + (VINES[1] - VINES[0]) * (k + 0.5) / n
        length = 0.95 + 0.18 * math.sin(k * 1.7)
        bm = box_bm((0.08, 0.12, length), (x, WALL_Y[0] - 0.06 - 0.03 * (k % 2), WALL_TOP - length / 2 + 0.05), bm=bm)
    bm = box_bm((VINES[1] - VINES[0] + 0.1, 0.12, 0.14), ((VINES[0] + VINES[1]) / 2, WALL_Y[0] + 0.02, WALL_TOP + 0.02), bm=bm)
    add_obj("Vines", bm, vine_m, "SET")


def bfly(name):
    """Bướm phát sáng dạng khối: thân, hai cánh. Ẩn ở dưới đất tới khi được key."""
    m = material("M_Butterfly", (1.0, 0.55, 0.45), 0.4, emit=((1.0, 0.5, 0.4), 1.3))
    root = empty(name, "CAST", loc=(0, 0, -20))
    add_obj(name + "_Body", sphere_bm(0.012, scale=(1.0, 2.0, 1.0), segs=8), m, "CAST", parent=root)
    wings = [add_obj(f"{name}_Wing{s:+d}", box_bm((0.035, 0.03, 0.003), (s * 0.018, 0, 0)), m, "CAST", parent=root)
             for s in (-1, 1)]
    return root, wings


def flap(wings, t0, t1, period=0.14, lo=-50, hi=50):
    t, i = t0, 0
    while t <= t1 + 1e-6:
        for w, s in zip(wings, (-1, 1)):
            rot(w, [(t, (0, s * (hi if i % 2 else lo), 0))])
        t, i = t + period / 2, i + 1
