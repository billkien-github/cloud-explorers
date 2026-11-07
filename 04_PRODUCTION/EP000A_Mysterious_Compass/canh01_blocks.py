"""
Previz khối Cảnh 1 tập 000A (Nhà thám hiểm nhỏ) dẫn Seedance (04_PRODUCTION/SEEDANCE.md): bối cảnh, đạo cụ, Lumo và
chú chim dạng khối (pipeline/blocks.py), máy quay từng cú. Mọi mốc lấy từ timing.py của previz 2D (TIMING trong
build_shot.py của đoạn), không gõ lại số. Diễn theo previz 2D đã chốt: 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh01/.
Hai đoạn (Seedance 2.5, tối đa 30 giây) gọi build() với giây bắt đầu và độ dài của đoạn:
    sh010: 0–21.9 s của cảnh (S1–S8: rừng mây, bản đồ cầm ngược, câu hô lần 1, vấp hòn đá ngã vào bụi gai, quả gai
           trên mũi, xoay bản đồ, "À… phía trước là phía sau.", quay ngoắt lại, đường rừng)
    sh020: 21.9–48.6 s (S9–S14: chú chim cười, Lumo chống chế, chim bay đi, dốc lá khô, đống lá, bướm, phế tích, ánh vàng)
Diễn dựng cho cả cảnh để các đoạn nối liền; khung 1 của đoạn = giây bắt đầu (blocks.T0), chỉ dựng máy quay của các cú
trong đoạn. Tên phim không dựng (thêm ở hậu kỳ; chữ lọt vào video dẫn sẽ lọt vào take).
Toạ độ (m): đất (mặt đường rừng) ở Z 0, máy quay phía -Y nhìn về +Y, trục X theo previz 2D: Lumo đi ra từ lối rẽ trong rừng (-2.62, Y 2.8), rẽ phải, dừng 1.68
trước bụi gai (2.5), vách đá từ 2.75; chú chim trên cành ngay trên đường (1.3, -0.15, cao 1.2), trước mặt Lumo khi Lumo
quay lại; đường rẽ vào rừng (về +Y) ở -3.5…-2.6. Dốc lá khô, đống lá, phiến đá rêu, phiến đá có ánh vàng (ẩn tới
GOLD_GLOW), tường phế tích dùng chung với Cảnh 2: ruins_blocks.py. Hướng nhìn phải 62°, trái -62°: quay giữa hai hướng
luôn đi qua mặt trước.
Hai cú cận bản đồ (S2, S6) là cú nhìn của Lumo: máy đặt ở chỗ mắt, đầu Lumo ẩn trong hai cú này.
Màu: Lumo cam, chú chim nâu (mỗi nhân vật một màu, ô trắng = hướng mặt); bối cảnh, đạo cụ xám; bướm, ánh vàng phát sáng.
"""
import math
import pathlib
import sys

import bmesh
import bpy
from mathutils import Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.path[:0] = [str(ROOT / "pipeline"), str(HERE)]
from blocks import *  # noqa: E402,F403  khối, vật liệu, nhân vật dạng khối, keyframe theo giây, máy quay
from ruins_blocks import LOW_Z, PILE_AT, STONE_TOP, bfly, build_ruins, flap, ground_z  # noqa: E402

RIGHT, LEFT = 62, -62
HOLD = 1 / 24                                                    # một khung: key ẩn và key hiện cách nhau ít hơn thì rơi vào cùng khung
BIRD_AT = Vector((1.3, -0.15, 1.2))


def tri_bm(w, h, th, center=(0, 0, 0), bm=None):
    """Tam giác dẹt (đầu mũi tên) nằm trong mặt XY, mũi chỉ về +Y, dày th."""
    bm = bm or bmesh.new()
    cx, cy, cz = center
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx, cy + h / 2)]
    a = [bm.verts.new((x, y, cz - th / 2)) for x, y in pts]
    b = [bm.verts.new((x, y, cz + th / 2)) for x, y in pts]
    bm.faces.new(list(reversed(a)))
    bm.faces.new(b)
    for i in range(3):
        bm.faces.new((a[i], a[(i + 1) % 3], b[(i + 1) % 3], b[i]))
    return bm


def build(timing, offset, seconds, out_blend, segment=None):
    """seconds: độ dài video render (số nguyên giây Seedance nhận); segment: độ dài đoạn trong cảnh. Từ segment tới
    seconds chỉ giữ cú máy cuối (diễn vẫn chạy tiếp), lúc dựng cắt bỏ."""
    segment = seconds if segment is None else segment
    tm = load_timing(ROOT / timing)
    start(tm.FPS, seconds, offset)
    T_END = tm.SECONDS
    S = {n: (a, b) for n, a, b in tm.SHOTS}

    # ============================================================ bối cảnh
    W = build_ruins()                                               # rừng mây, dốc lá khô, phế tích: ../ruins_blocks.py
    glow, pile = W.glow, W.pile
    moss_m, litter_m, trunk_m, canopy_m = W.mats.moss, W.mats.litter, W.mats.trunk, W.mats.canopy
    path_m = material("M_Path", (0.75, 0.73, 0.68), 0.9)
    cliff_m = material("M_Cliff", (0.5, 0.49, 0.47), 0.9)
    bush_m = material("M_Bush", (0.3, 0.31, 0.3), 0.9)
    prop = material("M_Prop", (0.78, 0.78, 0.78), 0.6)
    prop_dark = material("M_PropDark", (0.12, 0.12, 0.13), 0.6)
    bird_m = material("M_Bird_Brown", (0.32, 0.15, 0.06), 0.6)

    add_obj("Path", box_bm((6.25, 0.9, 0.02), (-0.425, 0.0, 0.0)), path_m, "SET")               # đường rừng X -3.55…2.7
    fork = add_obj("PathFork", box_bm((0.8, 6.0, 0.02), (0, 3.0, 0.0)), path_m, "SET", loc=(-3.05, 0.4, 0.002))
    fork.rotation_euler = (0, 0, math.radians(-12))                 # đường rẽ vào rừng; mép dốc ở thẳng phía trước
    # cây có cành chú chim đậu: cành vươn ra ngay trên đường, trước mặt Lumo lúc Lumo quay lại
    rod("BirdTree_Trunk", (0.55, 0.85, -0.1), (0.6, 0.85, 1.8), 0.11, trunk_m, "SET")
    add_obj("BirdTree_Canopy", sphere_bm(0.8, (0.6, 0.85, 2.2), (1.3, 1.0, 0.6)), canopy_m, "SET")
    branch_end = BIRD_AT + Vector((0.32, -0.12, 0.0))
    rod("Branch", (0.6, 0.8, 1.1), branch_end - Vector((0, 0, 0.03)), 0.03, trunk_m, "SET", cone_top=0.018)
    add_obj("Branch_Leaves", sphere_bm(0.1, branch_end, (1.3, 1.0, 0.7)), canopy_m, "SET")
    # vách đá cao chắn ngang lối, bụi gai trước chân vách
    add_obj("Cliff", box_bm((4.5, 6.6, 4.5), (5.0, 2.7, 2.25)), cliff_m, "SET")                # mặt trước ở Y -0.6
    bm = None
    for cx, cy, cz, r in ((2.9, 0.1, 0.6, 0.5), (2.95, 1.0, 1.6, 0.6), (3.0, 0.4, 2.8, 0.7), (2.85, 1.8, 0.4, 0.45)):
        bm = sphere_bm(r, (cx, cy, cz), bm=bm, segs=16)
    add_obj("Cliff_Boulders", bm, cliff_m, "SET")
    bm = None
    for cx, cy, cz, r in ((2.5, 0.0, 0.38, 0.42), (2.32, 0.05, 0.5, 0.3), (2.62, -0.1, 0.62, 0.28), (2.45, 0.1, 0.75, 0.22)):
        bm = sphere_bm(r, (cx, cy, cz), bm=bm, segs=16)
    bush = add_obj("Bush", bm, bush_m, "SET")
    add_obj("TripStone", sphere_bm(0.1, (1.8, -0.02, 0.0), scale=(1.0, 0.9, 0.6), segs=12), moss_m, "SET")   # hòn đá Lumo vấp: sẫm, đủ to để thấy trên mặt đường sáng

    # ============================================================ Lumo, đồ cầm tay, chú chim, bướm
    L = build_lumo((-3.8, 0.0, 0.0))
    lumo = Act(L, -3.8, 0.0, RIGHT)
    add_obj("Lumo_Bag", box_bm((0.1, 0.06, 0.09)), prop_dark, "CAST", parent=L.root, loc=(-0.2, -0.1, 0.3))
    map_hold = empty("Lumo_MapHold", "PROPS", parent=L.root)       # tấm bản đồ trước ngực, hai tay cầm
    map_spin = empty("Lumo_MapSpin", "PROPS", parent=map_hold)     # quay quanh pháp tuyến: 0 đúng chiều, 180 cầm ngược

    def map_shapes(parent, tag):
        """Bản đồ to cỡ đầu Lumo; mũi tên và rương sẫm. Đúng chiều: mũi tên chỉ về +Y (phía người cầm, tức chỉ xuống
        trên tấm bản đồ), rương ở mép +Y."""
        add_obj(f"Map{tag}_Sheet", box_bm((0.36, 0.3, 0.008)), prop, "PROPS", parent=parent)
        bm = box_bm((0.04, 0.08, 0.01), (0, -0.03, 0.006))           # thân mũi tên
        bm = tri_bm(0.1, 0.07, 0.01, (0, 0.045, 0.006), bm=bm)      # đầu mũi tên chỉ về +Y
        bm = box_bm((0.09, 0.05, 0.014), (0, 0.115, 0.008), bm=bm)  # rương
        bm = cyl_bm(0.026, 0.09, (0, 0.09, 0.03), axis="X", bm=bm, segs=12)    # nắp vòm, ở phía mũi tên (trên rương); nằm trọn
        # trước mặt giấy: ló ra mặt sau thì ở cú nhìn lưng bản đồ thành vệt sẫm trên tấm trắng, Seedance vẽ thành tấm thẻ
        add_obj(f"Map{tag}_Marks", bm, prop_dark, "PROPS", parent=parent)

    map_shapes(map_spin, "")
    map_fly = empty("MapFly", "PROPS")
    map_shapes(map_fly, "Fly")
    burr = add_obj("Lumo_Burr", sphere_bm(0.035, segs=10), bush_m, "PROPS", parent=L.head, loc=(0, -0.27, 0.12))
    burr_fly = add_obj("BurrFly", sphere_bm(0.035, segs=10), bush_m, "PROPS")
    head_leaf = add_obj("Lumo_Leaf", sphere_bm(0.09, scale=(1.0, 0.15, 0.6)), litter_m, "PROPS", parent=L.head,
                        loc=(0, -0.19, 0.25))                       # chiếc lá dính giữa trán, áp lên mặt trước đầu
    leaf_fall = add_obj("LeafFall", sphere_bm(0.09, scale=(1.0, 0.45, 0.12)), litter_m, "PROPS")
    bits = [add_obj(f"Leaf{i}", box_bm((0.07, 0.04, 0.01)), litter_m, "PROPS") for i in range(12)]
    bush_bits = [add_obj(f"BushLeaf{i}", box_bm((0.08, 0.05, 0.01)), bush_m, "PROPS") for i in range(4)]

    B = Rig()                                                       # chú chim nhỏ cỡ nắm tay Lumo
    B.root = empty("BIRD", "CAST", loc=BIRD_AT)
    add_obj("Bird_Body", sphere_bm(0.042, (0, 0, 0.045), (1.0, 1.1, 0.95)), bird_m, "CAST", parent=B.root)
    B.neck = empty("Bird_Neck", "CAST", parent=B.root, loc=(0, -0.01, 0.095))
    B.head = add_obj("Bird_Head", sphere_bm(0.032, (0, 0, 0.0)), bird_m, "CAST", parent=B.neck)
    face_marker("Bird_Face", B.head, 0.03, 0.02, -0.03, 0.0)
    add_obj("Bird_Tuft", box_bm((0.012, 0.025, 0.03), (0, 0.01, 0.04)), bird_m, "CAST", parent=B.head)
    add_obj("Bird_Tail", box_bm((0.02, 0.05, 0.04), (0, 0.06, 0.07)), bird_m, "CAST", parent=B.root)
    B.wing = add_obj("Bird_Wing", box_bm((0.012, 0.05, 0.03), (0, 0.015, -0.02)), bird_m, "CAST", parent=B.root,
                     loc=(-0.045, 0.0, 0.065))                      # cánh phía máy quay: vỗ bụng, vỗ bay
    B.wing_far = add_obj("Bird_WingFar", box_bm((0.012, 0.05, 0.03), (0, 0.015, -0.02)), bird_m, "CAST", parent=B.root,
                         loc=(0.045, 0.0, 0.065))

    bflies = [bfly(f"Butterfly{i}") for i in range(4)]
    for root, _ in bflies[:3]:
        root.scale = (1.5, 1.5, 1.5)

    for ob in (burr, burr_fly, head_leaf, leaf_fall, map_fly, *bits, *bush_bits):
        key(ob, "scale", -1.0, Vector((0, 0, 0)))                   # ẩn bằng scale 0 tới lúc xuất hiện

    def show(ob, t, on):
        key(ob, "scale", t - HOLD, Vector((1, 1, 1)) if not on else Vector((0, 0, 0)))
        key(ob, "scale", t, Vector((1, 1, 1)) if on else Vector((0, 0, 0)))

    def head(t, pitch=0.0, yaw=0.0, roll=0.0):
        rot(L.head, [(t, (pitch, roll, yaw))])

    def ears(t, a):
        for ear, side in L.ears:
            rot(ear, [(t, (a, 0, 0))])

    def arms(t, a, b=None):
        rot(L.arm_r, [(t, (a, 0, 0))])                              # tay phải: phía máy quay khi Lumo quay sang phải
        rot(L.arm_l, [(t, (a if b is None else b, 0, 0))])

    def tail(t, up, side=0.0):
        rot(L.tail, [(t, (up, 0, side))])

    def squash(t, sx, sz):
        key(L.root, "scale", t, Vector((sx, sx, sz)))

    READ = ((0, -0.3, 0.47), (-55, 0, 0))                           # bản đồ sát mặt khi đọc (cắm mặt vào)
    CHEST = ((0, -0.31, 0.42), (-72, 0, 0))                         # chìa thẳng ra trước, ngang ngực, sát bàn tay
    PUSH = ((0, -0.34, 0.43), (-75, 0, 0))
    BELLY = ((0, -0.3, 0.36), (-35, 0, 0))
    RAISE = ((0, -0.26, 0.72), (-85, 0, 0))                         # giơ lên, thấp hơn tai
    BAG = Vector((-0.2, -0.16, 0.3))                                # túi da ở hông
    BAG_TOP = BAG + Vector((0, -0.03, 0.1))                         # miệng túi: bản đồ ló ra, chui vào ở đây, túi giữ nguyên

    def hold(t, pose, arm=None):
        loc, r = pose
        key(map_hold, "location", t, Vector(loc))
        rot(map_hold, [(t, r)])
        a = {READ: -55, CHEST: -78, PUSH: -86, BELLY: -35, RAISE: -140}[pose] if arm is None else arm
        arms(t, a)

    def map_flip(t, deg):
        rot(map_spin, [(t, (0, 0, deg))])

    # bàn tay đi theo bản đồ khi xoay (cú nhìn S6): chỉ xoay bản đồ còn tay đứng yên thì take cho tay buông, bản đồ lơ lửng
    turn_paws = [add_obj(f"Lumo_TurnPaw{s:+d}", box_bm((0.07, 0.06, 0.05), (s * 0.17, -0.07, 0.02)), cast_materials()["lumo"],
                         "CAST", parent=map_spin) for s in (-1, 1)]
    for ob in turn_paws:
        key(ob, "scale", -1.0, Vector((0, 0, 0)))
        if S["S6"][0] >= offset - 1e-6 and S["S6"][0] < offset + segment:
            key(ob, "scale", S["S6"][0] - HOLD, Vector((0, 0, 0)))
            key(ob, "scale", S["S6"][0], Vector((1, 1, 1)))
            key(ob, "scale", S["S6"][1] - HOLD, Vector((1, 1, 1)))
            key(ob, "scale", S["S6"][1], Vector((0, 0, 0)))

    # ============================================================ Lumo: rừng mây, bụi gai
    w0, w1 = tm.LUMO_WALK_IN
    lumo.go(0.0, -2.62, 0.0, 2.8)                                   # trên lối rẽ, khuất sau hàng cây
    lumo.pose(0.0, lean=-3, yaw=10)                                 # ưỡn ngực, sải bước tự tin, đi ra phía đường chính
    head(0.0, 22)                                                   # cắm mặt vào bản đồ
    ears(0.0, -30)
    tail(0.0, 30)
    hold(0.0, READ)
    map_flip(0.0, 180)                                              # cầm ngược: mũi tên chỉ ra trước, rương lộn ngược
    key(L.head, "scale", 0.0, Vector((1, 1, 1)))
    for i, (t, x, y) in enumerate(((0.35, -2.7, 2.35), (0.7, -2.78, 1.9), (1.05, -2.86, 1.4), (w0, -2.95, 0.9), (w0 + 0.35, -3.0, 0.45),
                                   (w0 + 0.7, -2.85, 0.1), (w0 + 1.0, -2.55, 0.0))):
        lumo.go(t, x, 0.04 if i % 2 == 0 else 0.0, y)
    lumo.pose(w0 + 0.6, yaw=10)
    lumo.pose(w0 + 1.0, yaw=RIGHT)                                  # rẽ phải, về phía bụi gai
    for i, x in enumerate((-2.0, -1.4)):
        lumo.go(w0 + 1.0 + (S["S2"][0] - w0 - 1.0) * (i + 1) / 2, x, 0.04 if i % 2 == 0 else 0.0)
    for i in range(6):
        lumo.go(S["S2"][0] + (S["S3"][0] - S["S2"][0]) * (i + 1) / 6, -1.4 + 2.7 * (i + 1) / 6, 0.04 if i % 2 == 0 else 0.0)
    lumo.go(S["S3"][0] + 0.15, 1.52, 0.03)
    STOP_X, SOT_X = 1.5, 1.96                                        # dừng cách bụi gai một bước, hòn đá ở giữa; SOT_X: đầu lút hẳn
                                                                    # vào bụi gai (mép bụi ở khoảng 2.05)
    lumo.go(w1, STOP_X)
    steps(L.legs, 0.0, w1, 20, 28)
    wag(L.tail, 0.0, w1, 0.5, 18, base=(30, 0, 0))
    for i, t in enumerate([0.3 * k for k in range(int((w1 - 0.2) / 0.3) + 1)]):
        head(t, 22 if i % 2 else 17)                                # đầu nhún theo bước
    # dựng thẳng hai tai, chìa bản đồ thẳng ra trước ngang ngực
    p0, p1 = tm.LUMO_POSE
    ears(p0, -30)
    ears(p0 + 0.15, 14)
    ears(p1, 0)
    hold(p0, READ)
    hold(p0 + 0.25, CHEST)
    head(p0, 20)
    head(p0 + 0.2, -6)
    head(p1, 2)
    lumo.pose(p0, lean=-3)
    lumo.pose(p0 + 0.25, lean=-6)
    squash(p0, 1, 1)
    squash(p0 + 0.12, 1.08, 0.92)
    squash(p0 + 0.25, 0.95, 1.06)
    squash(p1, 1, 1)
    tail(p1, 30)
    wag(L.tail, p1, tm.LUMO_STEP[0], 0.6, 12, base=(32, 0, 0))
    # "Kho báu cổ đại… ngay phía trước!"
    l0, l1 = tm.LUMO_LINE1
    hold(l0 + 0.9, CHEST)
    hold(l0 + 1.1, PUSH)                                            # đẩy bản đồ tới thêm ở "ngay phía trước"
    lumo.pose(l0 + 0.9, lean=-6)
    lumo.pose(l0 + 1.15, lean=2)
    head(l0 + 0.9, 2)
    head(l0 + 1.15, -8)
    # vừa hô dứt câu vừa sải một bước tự tin (ưỡn ngực, hếch cằm, không nhìn đường), mũi chân vướng hòn đá, chúi người
    # ngã tới, đầu lút vào bụi gai, người còn trôi tới thêm rồi nén lại, giữ. SỘT! Ngả cứng cả người quanh bàn chân trông
    # như tấm ván đổ: cần đà, cú vấp làm nguyên nhân, quán tính và độ nảy.
    s0, trip = tm.LUMO_STEP[0], tm.TRIP
    lumo.go(s0, STOP_X)
    lumo.go(s0 + 0.16, STOP_X + 0.08, 0.05)                         # sải bước, nhổm lên
    lumo.go(trip, STOP_X + 0.14, 0.02)                              # chân trước vướng hòn đá
    lumo.go(tm.SOT, SOT_X - 0.04)
    lumo.go(tm.SOT + 0.1, SOT_X)                                    # quán tính: người còn trôi tới sau lúc chạm
    lumo.pose(s0, lean=-6)                                          # ưỡn ngực tự hào
    lumo.pose(trip, lean=2)
    lumo.pose(trip + 0.08, lean=14)                                 # vấp: chúi người tới
    lumo.pose(tm.SOT, lean=20)
    lumo.pose(tm.SOT + 0.1, lean=26)
    lumo.pose(tm.SOT + 0.25, lean=22)                               # nảy lại chút rồi giữ
    head(s0, -12)                                                   # hếch cằm, không nhìn phía trước
    head(trip, -14)                                                 # giật mình khi vấp
    head(tm.SOT, 4)
    head(tm.SOT + 0.1, 12)                                          # đầu chúi vào lá
    ears(trip, 20)                                                  # vấp: tai dựng ngược
    ears(tm.SOT + 0.05, -40)
    tail(trip, 50)
    tail(tm.SOT + 0.05, 55)                                         # đuôi dựng đứng
    squash(tm.SOT, 1, 1)
    squash(tm.SOT + 0.08, 1.08, 0.92)                               # nén lại khi va
    squash(tm.SOT + 0.2, 0.97, 1.03)
    squash(tm.SOT + 0.3, 1, 1)
    hold(trip, PUSH)
    hold(trip + 0.06, RAISE)                                        # hai tay hất lên theo cú vấp (thấp hơn tai)
    hold(tm.SOT + 0.15, BELLY)                                      # tay buông xuống, bản đồ thõng thấp
    for k in range(8):                                              # bụi gai rung
        key(bush, "location", tm.SOT + 0.05 * k, Vector((0.012 if k % 2 else -0.012, 0, 0)))
    key(bush, "location", tm.SOT + 0.4, Vector((0, 0, 0)))
    for i, ob in enumerate(bush_bits):                              # vài chiếc lá bụi gai bật ra
        p0v, p1v = Vector((2.15, -0.15, 0.75 + 0.05 * i)), Vector((1.8 + 0.2 * i, -0.4 - 0.1 * i, 0.01))
        show(ob, tm.SOT, True)
        for k in range(5):
            u = k / 4
            key(ob, "location", tm.SOT + (0.9 + 0.1 * i) * u, p0v.lerp(p1v, u) + Vector((0, 0, 0.3 * math.sin(math.pi * u))))
            rot(ob, [(tm.SOT + (0.9 + 0.1 * i) * u, (0, 220 * u, 90 * u))])
        show(ob, tm.SOT + 1.2 + 0.1 * i, False)
    for i, t in enumerate([tm.SOT + 0.3 + 0.3 * k for k in range(int((tm.BACK_OUT[0] - 0.1 - tm.SOT - 0.3) / 0.3) + 1)]):
        lumo.pose(t, lean=26 if i % 2 else 17, roll=8 if i % 2 else -8)  # kẹt trong bụi gai, ngọ nguậy cả người, đầu vẫn trong lá
        ears(t, -50 if i % 2 else -10)
    wag(L.tail, tm.SOT + 0.2, tm.BACK_OUT[0], 0.25, 30, base=(48, 0, 0))
    lumo.pose(tm.BACK_OUT[0], roll=0)
    # lùi ra, quả gai dính trên chóp mũi
    b0, b1 = tm.BACK_OUT
    lumo.go(b0, SOT_X)
    lumo.go(b0 + 0.18, 1.73, 0.03)
    lumo.go(b1, 1.7)
    lumo.pose(b0, lean=20)
    lumo.pose(b0 + 0.18, lean=-8)
    lumo.pose(b1, lean=0)
    show(burr, b0 + 0.05, True)
    head(b1, 6)
    ears(b0 + 0.18, 6)
    tail(b1, 22)
    hold(b1, CHEST)
    head(tm.BURR_LOOK[0], 16)                                       # nhìn quả gai trên mũi
    # lắc đầu, quả gai văng ra
    h0, h1 = tm.HEAD_SHAKE
    t, i = h0, 0
    while t < h1 - 0.05:
        head(t, 6, 24 if i % 2 else -24)
        ears(t, 20 if i % 2 else -45)
        t, i = t + 0.06, i + 1
    head(h1, 0)
    ears(h1, -5)
    bpy.context.scene.frame_set(fr(tm.BURR_FLY))
    bp = burr.matrix_world.translation.copy()
    show(burr, tm.BURR_FLY, False)
    show(burr_fly, tm.BURR_FLY, True)
    for k in range(5):
        u = k / 4
        key(burr_fly, "location", tm.BURR_FLY + 0.8 * u,               # bay đủ lâu để đọc ra
            bp.lerp(Vector((2.2, -0.35, 0.03)), u) + Vector((0, 0, 0.3 * math.sin(math.pi * u))))
    # nhìn bụi gai, nhìn bản đồ
    head(tm.LOOK_BUSH[0], 0)
    head(tm.LOOK_BUSH[0] + 0.15, -14)                               # ngẩng nhìn ngọn bụi gai, vách đá
    head(tm.LOOK_BUSH[1], -14)
    head(tm.LOOK_MAP[0], 0)
    head(tm.LOOK_MAP[1], 22)
    hold(tm.LOOK_MAP[0], CHEST)
    hold(tm.LOOK_MAP[1], READ)                                      # kéo bản đồ lại gần mặt
    # xoay bản đồ nửa vòng: rương đứng thẳng, mũi tên chỉ về phía Lumo (ra sau lưng)
    t0, t1 = tm.MAP_TURN
    map_flip(t0, 180)
    map_flip(t1, 360)
    # "À… phía trước là phía sau."
    a0, a1 = tm.LUMO_LINE2
    ears(a0, -5)
    ears(a0 + 0.15, 12)
    ears(a0 + 0.3, 5)
    head(a0 + 0.5, 22)
    head(a0 + 0.8, 8)
    head(tm.LOOK_BEHIND, 8)
    lumo.pose(tm.LOOK_BEHIND, yaw=RIGHT)
    lumo.pose(tm.LOOK_BEHIND + 0.25, yaw=20)                       # xoay người theo, mặt nghiêng hẳn về con đường bên trái
    head(tm.LOOK_BEHIND + 0.25, 4, -90)                             # liếc ra sau lưng, về con đường bên trái khung
    head(a1, 4, -90)
    tail(a0, 22)
    # quay ngoắt lại: con đường rừng rộng mở
    q0, q1 = tm.LUMO_TURN
    ears(q0, 5)
    ears(q0 + 0.08, -25)
    ears(q1 + 0.15, 10)
    ears(q1 + 0.3, 2)
    lumo.pose(q0, lean=0, yaw=20)
    lumo.pose(q1, lean=6, yaw=LEFT)
    lumo.pose(q1 + 0.25, lean=0)
    head(q0, 4, -90)
    head(q1, 2, 0)
    tail(q0, 22, 0)
    tail(q1, 10, 30)
    tail(q1 + 0.2, 30, 0)
    hold(q1 + 0.2, CHEST)
    hold(q1 + 0.5, BELLY)                                           # hạ bản đồ xuống ngang bụng
    wag(L.tail, q1 + 0.3, tm.BIRD_LAUGH[0], 0.6, 16, base=(30, 0, 0))
    j0, j1 = tm.LUMO_HOP                                            # nhảy cẫng lên một cái
    lumo.go(j0, 1.7)
    squash(j0, 1, 1)
    squash(j0 + 0.12, 1.1, 0.88)
    lumo.go(j0 + 0.12, 1.7)
    squash(j0 + 0.25, 0.92, 1.1)
    lumo.go(j0 + 0.3, 1.7, 0.38)
    lumo.go(j0 + 0.45, 1.7, 0.4)                                    # giữ ở đỉnh cú nhảy
    lumo.go(j1 - 0.08, 1.7)
    squash(j1 - 0.08, 1.1, 0.9)
    squash(j1 + 0.1, 1, 1)
    ears(j0, 2)
    ears(j0 + 0.2, 18)
    ears(j1 + 0.15, 4)
    hold(j0, BELLY)
    hold(j0 + 0.25, RAISE)                                          # giơ bản đồ (không quá ngang tai)
    hold(j1 + 0.25, BELLY)
    head(j0 + 0.2, -12)
    head(j1 + 0.2, 0)

    # ============================================================ chú chim: đậu trên cành xem từ đầu, cười, bay đi
    BY = yaw_to(BIRD_AT, (1.7, 0.0))                                # nhìn Lumo
    rot(B.root, [(0.0, (0, 0, BY - 40))])
    rot(B.head, [(0.0, (0, 0, 0)), (4.0, (0, 0, 20)), (7.0, (0, 0, 0)), (tm.SOT, (0, 0, 0)), (tm.SOT + 0.1, (-20, 0, 0)),
                 (tm.SOT + 0.5, (8, 0, 25)), (14.0, (0, 0, 10)), (18.0, (0, 0, 0))])   # ngó theo Lumo; giật mình lúc SỘT
    rot(B.root, [(tm.LUMO_TURN[1], (0, 0, BY - 40)), (tm.LUMO_TURN[1] + 0.4, (0, 0, BY - 60))])
    rot(B.neck, [(0.0, (0, 0, 0)), (tm.LUMO_TURN[1], (0, 0, 0)), (tm.LUMO_TURN[1] + 0.4, (0, 0, 60))])   # đầu ngoảnh về Lumo
    rot(B.head, [(tm.BIRD_TILT[0], (0, 0, 0)), (tm.BIRD_TILT[1], (0, 28, 0))])   # nghiêng đầu nhìn Lumo
    rot(B.wing, [(0.0, (0, 0, 0)), (tm.BIRD_LAUGH[0] - 0.2, (0, 0, 0))])
    for c in tm.CHIRPS:                                             # lấy cánh vỗ bụng: CHÍP CHÍP CHÍP!
        rot(B.wing, [(c - 0.18, (-30, 0, 0)), (c, (-95, 0, -35)), (c + 0.1, (-60, 0, -20)), (c + 0.2, (-95, 0, -35)),
                     (c + 0.3, (-30, 0, 0))])
        key(B.root, "location", c - 0.1, BIRD_AT)
        key(B.root, "location", c + 0.05, BIRD_AT + Vector((0, 0, 0.03)))
        key(B.root, "location", c + 0.25, BIRD_AT)
        rot(B.head, [(c, (-20, 0, 0)), (c + 0.3, (6, 10, 0))])        # ngửa đầu cười
    rot(B.wing, [(tm.BIRD_LAUGH[1] + 0.2, (0, 0, 0))])
    for c in (tm.LUMO_PUFF[0] + 0.1, tm.LUMO_LINE3[1] - 0.6):        # còn khúc khích khi Lumo chống chế
        rot(B.wing, [(c, (0, 0, 0)), (c + 0.12, (-90, 0, -30)), (c + 0.3, (0, 0, 0))])
    rot(B.head, [(tm.LUMO_LINE3[0], (0, 20, 0)), (tm.LUMO_LINE3[0] + 0.4, (-10, -10, 0)), (tm.LUMO_LINE3[1] - 0.8, (0, 22, 0))])
    f0, f1 = tm.BIRD_FLY                                            # nhún lấy đà, vỗ cánh bay lên về phía rừng
    key(B.root, "location", f0, BIRD_AT)
    keys(B.root, "scale", [(f0, Vector((1, 1, 1))), (f0 + 0.1, Vector((1.12, 1.12, 0.85))), (f0 + 0.2, Vector((1, 1, 1)))])
    for t, d in ((f0 + 0.18, (0, 0, 0.02)), (f0 + 0.35, (-0.25, 0.2, 0.25)), (f0 + 0.55, (-0.75, 0.6, 0.55)),
                 (f1, (-1.6, 1.4, 1.1)), (f1 + 0.1, (-6.0, 6.0, 6.0))):
        key(B.root, "location", t, BIRD_AT + Vector(d))
    rot(B.root, [(f0 + 0.15, (0, 0, BY - 60)), (f0 + 0.3, (0, 0, 220))])
    rot(B.neck, [(f0 + 0.15, (0, 0, 60)), (f0 + 0.3, (0, 0, 0))])
    t, i = f0 + 0.15, 0
    while t < f1:
        rot(B.wing, [(t, (0, 0, -70 if i % 2 else 10))])
        rot(B.wing_far, [(t, (0, 0, 70 if i % 2 else -10))])
        t, i = t + 0.06, i + 1

    # ============================================================ Lumo: bị cười, ngượng, chống chế
    head(tm.BIRD_LAUGH[0] + 0.2, 0)
    head(tm.BIRD_LAUGH[0] + 0.5, -22, -8)                           # nghe CHÍP, ngước nhìn chú chim
    y0, y1 = tm.LUMO_SHY                                            # cụp tai, rụt vai, liếc đi chỗ khác rồi liếc lại chim
    head(y0, -22, -8)
    ears(y0, 2)
    ears(y0 + 0.35, -55)
    head(y0 + 0.35, 10, 30)
    squash(y0 + 0.1, 1, 1)
    squash(y0 + 0.35, 1.05, 0.94)
    head(y1 - 0.5, 10, 30)
    head(y1 - 0.2, -18, -8)
    squash(y1 - 0.1, 1.05, 0.94)
    tail(y0, 20)
    tail(y0 + 0.4, -10)                                             # đuôi rủ
    u0, u1 = tm.LUMO_PUFF                                           # ưỡn ngực, dựng thẳng tai, hếch cằm
    lumo.pose(u0, lean=0)
    lumo.pose(u1, lean=-10, yaw=-15)                                # ưỡn ngực về phía máy
    squash(u0 + 0.15, 1, 1)
    squash(u1, 0.98, 1.04)
    ears(u0, -55)
    ears(u0 + 0.2, 12)
    ears(u1, 0)
    head(u0, -18, -8)
    head(u1, -14, -54)                                              # hếch cằm, vẫn nhìn chim
    tail(u0, -10)
    tail(u1, 38)
    m0, m1 = tm.MAP_STOW                                            # gấp bản đồ nhét vào túi da
    hold(m0, BELLY)
    keys(map_hold, "scale", [(m0, Vector((1, 1, 1))), (m0 + 0.35, Vector((0.5, 0.5, 0.5))), (m0 + 0.6, Vector((0.3, 0.3, 0.3)))])
    key(map_hold, "location", m0 + 0.65, BAG_TOP)                   # tới miệng túi ở hông
    rot(L.arm_r, [(m0 + 0.65, (-25, 0, 0))])
    rot(L.arm_l, [(m0 + 0.35, (-6, 0, 0))])
    keys(map_hold, "scale", [(m0 + 0.7 - HOLD, Vector((0.3, 0.3, 0.3))), (m0 + 0.7, Vector((0, 0, 0)))])
    rot(L.arm_r, [(m1, (6, 0, 0))])
    head(m0, 14, -10)                                               # liếc xuống túi
    head(m1, -14, -54)
    e0, e1 = tm.LUMO_LINE3                                          # "Mình biết chứ! Đang kiểm tra bản đồ thôi!"
    for t, a in ((e0, -14), (e0 + 0.25, -4), (e0 + 0.5, -16), (e0 + 1.0, -14)):
        head(t, a, -54)                                             # gật mạnh một cái ở "Mình biết chứ!"
    rot(L.arm_r, [(e0 + 1.4, (6, 0, 0)), (e0 + 1.6, (-25, 0, 0)), (e0 + 1.75, (-10, 0, 0)), (e0 + 1.9, (-25, 0, 0)), (e1, (6, 0, 0))])
    lumo.pose(e1, lean=-10)
    wag(L.tail, u1 + 0.1, e1, 0.5, 16, base=(34, 0, 0))
    head(f0 + 0.1, -22, -54)                                        # nhìn chim bay đi
    head(f1, -38, -75)
    lumo.pose(f0, lean=-10)
    lumo.pose(f1, lean=0)
    ears(f1, -10)

    # ============================================================ Lumo: lại rút bản đồ, sải bước, hụt chân, trượt dốc
    o0, o1 = tm.MAP_OUT
    head(o0, -38, -75)
    head(o1, 22, 0)                                                 # cắm mặt vào bản đồ
    rot(L.arm_r, [(o0, (6, 0, 0)), (o0 + 0.15, (-25, 0, 0))])
    key(map_hold, "location", o0 + 0.18, BAG_TOP)                   # ló ra ở miệng túi (túi giữ nguyên), kéo lên, mở bản đồ;
                                                                    # phóng bản đồ ngay trong khối túi thì Seedance biến túi thành bản đồ
    keys(map_hold, "scale", [(o0 + 0.18 - HOLD, Vector((0, 0, 0))), (o0 + 0.18, Vector((0.3, 0.3, 0.3))), (o1, Vector((1, 1, 1)))])
    hold(o1, READ)
    ears(o1, -30)
    lumo.pose(o1 - 0.1, yaw=-15)
    lumo.pose(o1, lean=-3, yaw=LEFT)
    st0, st1 = tm.STRIDE
    cut = S["S12"][0]
    for i in range(9):                                              # sải bước thật nhanh ra khỏi khung
        lumo.go(st0 + (cut - HOLD - st0) * i / 8, 1.7 + (-1.3 - 1.7) * i / 8, 0.05 if i % 2 else 0.0)
    for i in range(7):                                              # vào cú S12 từ mép phải
        lumo.go(cut + (st1 - cut) * i / 6, -1.75 + (-3.92 + 1.75) * i / 6, 0.05 if i % 2 else 0.0)
    steps(L.legs, st0, st1, 16, 32)
    wag(L.tail, o1, st1, 0.4, 18, base=(28, 0, 0))
    x0, ed = -3.92, tm.EDGE                                         # hụt chân: WHOOSH! bản đồ tuột tay
    lumo.pose(ed, lean=-3)
    lumo.pose(ed + 0.12, lean=18)                                   # chúi về trước, chân hụt
    lumo.pose(ed + 0.24, lean=10)                                   # chới với ở mép một nhịp rồi mới ngã ngồi
    lumo.go(ed + 0.12, x0 - 0.18, -0.03)
    head(ed + 0.12, 10)
    ears(ed + 0.05, 25)
    hold(ed, READ)
    rot(L.arm_r, [(ed + 0.06, (-140, 0, 0))])                       # hai tay hất lên (không quá ngang tai)
    rot(L.arm_l, [(ed + 0.06, (-140, 0, 0))])
    bpy.context.scene.frame_set(fr(ed + 0.06))
    mp = map_hold.matrix_world.translation.copy()
    keys(map_hold, "scale", [(ed + 0.06 - HOLD, Vector((1, 1, 1))), (ed + 0.06, Vector((0, 0, 0)))])
    show(map_fly, ed + 0.06, True)
    for t, p, r in ((ed + 0.06, mp, (-60, 0, 0)), (ed + 0.4, mp + Vector((-0.4, -0.1, 0.4)), (20, 40, 60)),
                    (ed + 0.9, Vector((-5.1, -0.3, 0.6)), (-30, 80, 100)), (ed + 1.5, Vector((-5.9, -0.3, 0.2)), (40, 140, 160)),
                    (ed + 2.1, Vector((-6.7, -0.35, -0.4)), (-20, 200, 200)), (ed + 2.5, Vector((-7.3, -0.4, -0.75)), (30, 250, 240)),
                    (tm.MAP_DRIFT[1], Vector((-7.78, -0.3, -1.08)), (-30, 360, 270))):   # chao lượn, rơi xuống mép đống lá
        key(map_fly, "location", t, p)
        rot(map_fly, [(t, r)])
    lumo.pose(tm.WHOOSH[1] - 0.1, lean=-35)
    lumo.go(tm.WHOOSH[1] - 0.1, -4.25, -0.08)
    sl0, sl1 = tm.SLIDE                                             # trượt một mạch xuống dốc, ngồi bệt, chân trước: RUSTLE!
    END_X = -6.95
    k = 0
    t = sl0
    while t <= sl1 - 0.25 + 1e-6:
        u = min(1.0, (t - sl0) / (sl1 - 0.25 - sl0)) ** 1.3
        x = -4.45 + (END_X + 4.45) * u
        lumo.go(t, x, ground_z(x) + 0.12 + (0.02 if k % 2 else 0.0))
        lumo.pose(t, lean=-55 + (4 if k % 2 else -4))
        t, k = t + 0.1, k + 1
    wag(L.arm_r, sl0, sl1 - 0.1, 0.16, 25, base=(-120, 0, 0), axis=0)   # tay chới với
    wag(L.arm_l, sl0 + 0.08, sl1 - 0.1, 0.16, 25, base=(-120, 0, 0), axis=0)
    for ear, side in L.ears:                                        # tai bay ngược ra sau
        wag(ear, sl0, sl1 - 0.1, 0.14, 15, base=(-55, 0, 0), axis=0)
    wag(L.tail, ed, sl1, 0.12, 15, base=(45, 0, 0), axis=0)
    head(sl0, -10)
    for kk, ob in enumerate(bits[8:]):                              # lá khô tung lên dọc đường trượt
        ts = sl0 + 0.2 + 0.3 * kk
        x = -4.45 + (END_X + 4.45) * min(1.0, (ts - sl0) / (sl1 - 0.25 - sl0)) ** 1.3
        pa, pb = Vector((x + 0.1, -0.2, ground_z(x) + 0.05)), Vector((x + 0.4, -0.4, ground_z(x + 0.4) + 0.02))
        show(ob, ts, True)
        for q in range(5):
            u = q / 4
            key(ob, "location", ts + 0.6 * u, pa.lerp(pb, u) + Vector((0, 0, 0.3 * math.sin(math.pi * u))))
            rot(ob, [(ts + 0.6 * u, (0, 260 * u, 90 * u))])
        show(ob, ts + 0.9, False)
    lumo.go(sl1 - 0.12, -7.15, LOW_Z + 0.12)                        # rơi vào đống lá: POOF!
    lumo.pose(sl1 - 0.12, lean=-50)
    lumo.go(tm.POOF, PILE_AT.x, LOW_Z - 0.75)                       # lút mất trong đống lá
    lumo.pose(tm.POOF, lean=-15)
    rot(L.arm_r, [(tm.POOF + 0.2, (6, 0, 0))])
    rot(L.arm_l, [(tm.POOF + 0.2, (6, 0, 0))])
    ears(tm.POOF + 0.2, -10)
    keys(pile, "scale", [(tm.POOF - 0.05, Vector((1, 1, 1))), (tm.POOF + 0.05, Vector((1.18, 1.18, 0.82))),
                         (tm.POOF + 0.25, Vector((0.94, 0.94, 1.1))), (tm.POOF + 0.45, Vector((1, 1, 1)))])
    for kk, ob in enumerate(bits[:8]):                              # lá tung tóe
        a = math.radians(20 + 20 * kk)
        pa = PILE_AT + Vector((0.2 * math.cos(a), -0.2, 0.35))
        pb = PILE_AT + Vector((0.8 * math.cos(a), -0.3 - 0.1 * (kk % 3), 0.02))
        t0b = tm.POOF + 0.02 * kk
        show(ob, t0b, True)
        for q in range(5):
            u = q / 4
            key(ob, "location", t0b + (1.0 + 0.05 * kk) * u, pa.lerp(pb, u) + Vector((0, 0, 0.5 * math.sin(math.pi * u))))
            rot(ob, [(t0b + (1.0 + 0.05 * kk) * u, (0, 300 * u, 120 * u))])
        show(ob, t0b + 1.3 + 0.05 * kk, False)
    show(head_leaf, tm.POOF, True)

    # ============================================================ Lumo: ngẩng lên khỏi đống lá, lắc đầu, nhặt bản đồ
    POP_Z = LOW_Z - 0.16
    pp = tm.LUMO_POP
    lumo.go(pp - 0.05, PILE_AT.x, LOW_Z - 0.75)
    lumo.go(pp + 0.12, PILE_AT.x, POP_Z + 0.05)
    lumo.go(pp + 0.25, PILE_AT.x, POP_Z)
    lumo.pose(pp, lean=-10)
    lumo.pose(pp + 0.25, lean=0)
    ears(pp, -40)
    ears(pp + 0.15, 15)                                             # tai bật lên
    ears(pp + 0.35, 4)
    head(pp + 0.25, 0)
    head(pp + 0.75, -15)                                            # ngước mắt nhìn chiếc lá trên trán
    k0, k1 = tm.HEAD_SHAKE2
    head(k0, -15)
    t, i = k0, 0
    while t < k1 - 0.05:
        head(t, 0, 26 if i % 2 else -26)
        ears(t, 25 if i % 2 else -50)
        t, i = t + 0.05, i + 1
    head(k1, 0)
    ears(k1, 2)
    bpy.context.scene.frame_set(fr(tm.LEAF_FALL[0]))
    lp = head_leaf.matrix_world.translation.copy()
    show(head_leaf, tm.LEAF_FALL[0], False)
    show(leaf_fall, tm.LEAF_FALL[0], True)
    for t, p, r in ((tm.LEAF_FALL[0], lp, (0, 0, 0)), (tm.LEAF_FALL[0] + 0.25, lp + Vector((0.12, 0.05, 0.04)), (30, 0, 40)),
                    (tm.LEAF_FALL[0] + 0.5, lp + Vector((0.28, 0.1, -0.12)), (-20, 0, 80)),
                    (tm.LEAF_FALL[1], PILE_AT + Vector((0.32, 0.05, 0.36)), (15, 0, 110))):
        key(leaf_fall, "location", t, p)                            # chao ra sau lưng, nằm trên lưng đống lá
        rot(leaf_fall, [(t, r)])
    head(k1 + 0.3, 18)                                              # thấy tấm bản đồ rơi cạnh đó
    n0, n1 = tm.MAP_PICK
    PICK_Z, PICK_LEAN = LOW_Z - 0.03, 30
    lumo.go(n0, PILE_AT.x, POP_Z)
    lumo.go(n0 + 0.2, PILE_AT.x, PICK_Z)
    lumo.pose(n0, lean=0)
    lumo.pose(n0 + 0.25, lean=PICK_LEAN)
    rot(L.arm_l, [(n0, (6, 0, 0)), (n0 + 0.3, (-55, 0, -25))])      # tay phía máy quay vươn qua mặt đống lá
    show(map_fly, n0 + 0.32, False)
    key(map_hold, "location", n0 + 0.32 - HOLD, Vector((0.12, -0.3, 0.3)))
    key(map_hold, "scale", n0 + 0.32 - HOLD, Vector((0, 0, 0)))
    key(map_hold, "location", n0 + 0.32, Vector((0.12, -0.36, 0.32)))
    key(map_hold, "scale", n0 + 0.32, Vector((0.8, 0.8, 0.8)))      # nhặt lên
    head(n0 + 0.25, 12)
    v0, v1 = tm.MAP_STOW2
    lumo.pose(v0, lean=PICK_LEAN)
    lumo.pose(v0 + 0.25, lean=0)
    lumo.go(v0, PILE_AT.x, PICK_Z)
    lumo.go(v0 + 0.25, PILE_AT.x, POP_Z)
    rot(L.arm_l, [(v0, (-55, 0, -25)), (v0 + 0.3, (-15, 0, 0)), (v1, (6, 0, 0))])   # nhét vào túi da (lút trong đống lá)
    keys(map_hold, "scale", [(v0, Vector((0.8, 0.8, 0.8))), (v0 + 0.25, Vector((0.3, 0.3, 0.3))), (v0 + 0.3, Vector((0, 0, 0)))])
    key(map_hold, "location", v0 + 0.3, BAG)
    head(v1, 0)

    # ============================================================ bướm, phế tích, ánh vàng
    def drift(root, wings, t0, t1, cx, cy, cz, ax, az, speed=0.35, phase=0.0, dt=0.4):
        t = t0
        while t <= t1 + 1e-6:
            u = (t + phase) * speed
            key(root, "location", t, Vector((cx + ax * math.sin(u), cy, cz + az * math.sin(2 * u))))
            rot(root, [(t, (0, 0, 90 if math.cos(u) >= 0 else -90))])
            t += dt
        flap(wings, t0, t1)

    drift(*bflies[0], 0.0, T_END, -0.4, -3.5, 2.4, 1.6, 0.35, 0.3)       # bay qua trước máy cú toàn mở đầu
    drift(*bflies[1], 0.0, T_END, -1.9, 1.6, 1.35, 0.6, 0.2, 0.5, 2.0)
    drift(*bflies[2], 0.0, T_END, -0.6, 0.6, 0.8, 1.6, 0.18, 0.25, 4.0)
    for root, _ in bflies[:3]:                                      # từ S12 chỉ còn con bướm dẫn mắt
        key(root, "scale", S["S12"][0] - HOLD, Vector((1.5, 1.5, 1.5)))
        key(root, "scale", S["S12"][0], Vector((0, 0, 0)))
    hero, hero_w = bflies[3]
    hero.scale = (1.6, 1.6, 1.6)                                    # con bướm dẫn mắt: to hơn một chút để đọc được ở S14
    l0b, l1b = tm.BFLY_LAND
    drift(hero, [], 0.0, l0b - 0.4, -8.6, 0.3, 0.1, 0.5, 0.18, 0.4, 1.0)
    for t, p in ((l0b - 0.2, (-8.45, -0.15, -0.7)), (l0b + 0.25, (-8.25, -0.15, -0.78)), (l0b + 0.5, (-8.1, -0.13, -0.92)),
                 (l1b, tuple(STONE_TOP))):
        key(hero, "location", t, Vector(p))
    rot(hero, [(l0b - 0.2, (0, 0, 90)), (l1b, (0, 0, 60))])        # đậu trên phiến đá rêu, đầu hướng về Lumo
    key(hero, "location", T_END, STONE_TOP)
    flap(hero_w, 0.0, l1b)
    flap(hero_w, l1b, T_END, 0.9, 20, 55)                           # đậu: cánh hé mở về phía máy, khép mở chậm
    head(l0b, -10)                                                  # nhìn con bướm bay vào, đậu ngay trước mặt
    head(l1b, 14)
    head(tm.CAM_REVEAL[0], 14)
    head(tm.CAM_REVEAL[0] + 0.4, 2, -10)                            # nhìn qua con bướm, về phía phế tích
    wo = tm.LUMO_WONDER
    ears(wo - 0.05, -20)
    ears(wo + 0.12, 30)                                             # tai bật dựng
    ears(wo + 0.3, 16)
    lumo.go(wo - 0.05, PILE_AT.x, POP_Z)
    lumo.go(wo + 0.25, PILE_AT.x, POP_Z + 0.22)                    # nhổm hẳn lên khỏi đống lá (tới ngực): đủ to cho cú toàn
    head(wo + 0.25, -6, -30)                                        # quay đầu về phía ánh vàng
    key(glow, "scale", 0.0, Vector((0, 0, 0)))                     # la bàn dưới phiến đá: ẩn tới GOLD_GLOW (máy đang lùi ra),
    key(glow, "scale", tm.GOLD_GLOW[0] - HOLD, Vector((0, 0, 0)))  # nếu không đốm vàng lộ ở mép khung S13, đầu S14
    t, i = tm.GOLD_GLOW[0], 0
    while t < T_END:
        key(glow, "scale", t, Vector((1.2, 1.2, 1.0)) if i % 2 else Vector((0.9, 0.9, 1.0)))
        t, i = t + 0.6, i + 1

    # ============================================================ hai cú nhìn của Lumo (S2, S6): đầu ẩn, máy ở chỗ mắt
    for n in ("S2", "S6"):
        a, b = S[n]
        if not (offset - 1e-6 <= a < offset + segment - 1e-6):
            continue
        key(L.head, "scale", a - HOLD, Vector((1, 1, 1)))
        key(L.head, "scale", a, Vector((0, 0, 0)))
        key(L.head, "scale", b - HOLD, Vector((0, 0, 0)))
        key(L.head, "scale", b, Vector((1, 1, 1)))

    def pov(n, dt=0.3):
        a, b = S[n]
        out, t = [], a
        while t <= b + 1e-6:
            bpy.context.scene.frame_set(fr(t))
            eye = L.root.matrix_world @ Vector((0, -0.04, 0.86))
            tgt = map_hold.matrix_world.translation.copy()
            out.append((t, tuple(eye), tuple(tgt), 22))
            t += dt
        return out

    # ============================================================ máy quay (một máy mỗi cú; chỉ dựng các cú trong đoạn)
    CAMS = {   # (giây, vị trí máy, điểm nhìn, tiêu cự mm)
        "S1": [(S["S1"][0], (0.2, -8.0, 1.5), (0.0, 6.0, 8.0), 26),                         # toàn: đảo lơ lửng, thác, bướm…
               (tm.LUMO_WALK_IN[0] - 0.2, (0.2, -8.0, 1.5), (0.0, 6.0, 8.0), 26),
               (tm.LUMO_WALK_IN[0] + 0.9, (0.2, -8.0, 1.5), (0.3, 2.0, 1.7), 26)],          # …hạ xuống: Lumo ra từ lối rẽ
        "S2": pov("S2"),                                                                    # bản đồ cầm ngược, Lumo nhìn xuống
        "S3": [(S["S3"][0], (1.85, -2.7, 0.75), (2.0, 0.0, 0.52), 30)],                     # Lumo, bản đồ, bụi gai; rộng hơn cần: Seedance hay cắt chặt cú trung
        "S4": [(S["S4"][0], (2.4, -4.3, 1.15), (2.5, 0.0, 1.0), 35)],                       # mặt trong bụi gai, vách đá cao
        "S5": [(S["S5"][0], (1.95, -1.75, 0.78), (1.95, 0.0, 0.72), 35)],                   # cận: quả gai trên mũi
        "S6": pov("S6", 0.5),                                                               # xoay bản đồ nửa vòng
        "S7": [(S["S7"][0], (1.1, -3.6, 1.0), (1.3, 0.0, 0.6), 26)],                       # rộng hơn S5: thấy con đường sau lưng
        "S8": [(S["S8"][0], (0.5, -4.5, 1.4), (-0.5, 1.5, 0.5), 26)],                       # con đường rừng rộng mở trước mặt Lumo
        "S9": [(S["S9"][0], (1.65, -0.9, 1.28), tuple(BIRD_AT + Vector((0, 0, 0.07))), 50)],   # cận chú chim cười, thấy bụng
        "S10": [(S["S10"][0], (1.5, -2.4, 0.85), (1.5, 0.0, 0.76), 35)],                     # Lumo ngượng, chống chế, chim bay
        "S11": [(S["S11"][0], (1.0, -3.6, 0.6), (1.0, 0.0, 0.5), 32)],                      # rộng hơn S10 hẳn: sải bước ra khỏi khung
        "S12": [(S["S12"][0], (-4.9, -6.6, 1.1), (-4.95, 0.0, -0.35), 35)],                 # đường rẽ, mép dốc, trượt, đống lá
        "S13": [(S["S13"][0], (-7.25, -2.7, -0.62), (-7.25, 0.0, -0.82), 35)],              # lá trên trán, nhặt bản đồ
        "S14": [(S["S14"][0], (-7.62, -1.95, -0.78), (-7.62, 0.0, -0.76), 35),              # cận hơn S13 hẳn: đá rêu có bướm bên trái,
                (tm.CAM_REVEAL[0], (-7.62, -1.95, -0.78), (-7.62, 0.0, -0.76), 35),         # đầu, tai Lumo bên phải, phiến đá vàng ngoài khung…
                (tm.CAM_REVEAL[1], (-8.3, -4.4, -0.35), (-8.4, 0.5, -0.65), 35)],           # …máy lùi ra: phế tích, ánh vàng
    }
    end_t = offset + segment
    shots = [(n, a, b) for n, a, b in tm.SHOTS if a < end_t - 1e-6 and b > offset + 1e-6]
    cams = cameras(shots, {n: CAMS[n] for n, _, _ in shots})
    H = Vector((0, 0, 0.2))
    must = {"S1": [], "S3": [(L.head, H), (bush, Vector((2.3, 0, 0.5)))], "S4": [(L.root, Vector((0, 0, 0.5)))],
            "S5": [(L.head, H)], "S7": [(L.head, H)], "S8": [(L.root, Vector((0, 0, 0.5)))], "S9": [(B.head, Vector())],
            "S10": [(L.head, H), (B.head, Vector())], "S12": [(pile, Vector())], "S13": [(pile, Vector())],
            "S14": [(hero, Vector()), (L.head, Vector((0, 0, 0.5)))]}   # chóp tai
    extra = [("S1", L.root, tm.LUMO_WALK_IN[0] + 1.0, S["S1"][1]), ("S14", L.head, S["S14"][0], S["S14"][1]), ("S11", L.head, S["S11"][0], tm.STRIDE[0] + 1.0),
             ("S12", L.head, S["S12"][0] + 0.3, tm.POOF), ("S13", L.head, tm.LUMO_POP + 0.3, S["S13"][1]),
             ("S14", glow, tm.CAM_REVEAL[1], S["S14"][1])]
    check_in_frame(shots, cams, must, extra, ground=lambda p: ground_z(p.x))
    stills = [round((a + b) / 2, 2) for _, a, b in shots]
    stills += [t for t in (tm.SOT + 0.2, tm.HEAD_SHAKE[0] + 0.2, tm.MAP_TURN[0] + 0.3, tm.LUMO_HOP[0] + 0.35, tm.CHIRPS[1],
                           tm.LUMO_SHY[0] + 0.6, tm.EDGE + 0.15, tm.SLIDE[0] + 0.6, tm.LUMO_POP + 0.5, tm.MAP_PICK[0] + 0.35,
                           tm.BFLY_LAND[1] + 0.2, tm.CAM_REVEAL[1] + 0.5) if offset <= t < end_t]
    finish(out_blend, sorted(set(stills)))
