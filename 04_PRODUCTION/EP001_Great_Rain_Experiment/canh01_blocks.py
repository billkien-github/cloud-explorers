"""
Previz khối Cảnh 1 tập 01 (Hook + Discovery) dẫn Seedance (04_PRODUCTION/SEEDANCE.md): bối cảnh, đạo cụ, diễn của bốn
nhân vật dạng khối (pipeline/blocks.py) và máy quay từng cú. Mọi mốc lấy từ timing.py của previz 2D (TIMING trong
build_shot.py của đoạn), không gõ lại số. Hai đoạn gọi build() với giây bắt đầu và độ dài của đoạn:
    sh010: 0–28.8 s của cảnh (S1–S6: giọt sương, Piko đớp, tên phim, Nori rọi mầm, Lumo vấp, la bàn chỉ túi Piko)
    sh020: 28.8–55.0 s (S7–S14: cái thìa cong, "Thìa thôi mà?", lá ướt sương, mây đỉnh đồi, Tavi giảng, chỉ đỉnh đồi)
Diễn dựng cho cả cảnh để hai đoạn nối liền; khung 1 của đoạn = giây bắt đầu (blocks.T0), chỉ dựng máy quay của các cú
trong đoạn.
Toạ độ (m): đất ở Z 0, máy quay đặt phía -Y nhìn về +Y, trục X theo previz 2D: Tavi 1.05, Lumo 1.6, vết nứt Lumo vấp
2.28, vườn mầm 2.35–4.7, mầm gầy nhom 2.45, sinh vật thở dài 2.66, cành lá khô 2.79 (đầu lá thấp ở phía +X, ngay trước
mặt Piko), Piko 3.42, bông hoa 3.85 phía trước bên phải Piko; đồi xa bên phải, đỉnh (8.0, 1.5) cao 2.4 để nhân vật nhìn
lên đồi vẫn nghiêng mặt về máy quay. Hướng nhìn phải 62°, trái -62°: quay giữa hai hướng luôn đi qua mặt trước.
Vị trí cái thìa trên đất, bụi đào, chỗ Lumo cúi kề la bàn, vệt sáng của Nori đặt theo vị trí tay thật sau khi diễn xong.
La bàn nghiêng mặt về phía máy quay, mũi sao tính theo vị trí thật của túi Piko và cái thìa chiếu lên mặt la bàn.
Màu: nhân vật theo blocks.py; bối cảnh, đạo cụ xám; giọt sương, ánh lóe, vệt sáng của Nori phát sáng.
"""
import importlib.util
import math
import pathlib
import sys

import bpy
from mathutils import Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.path.insert(0, str(ROOT / "pipeline"))
from blocks import *  # noqa: E402,F403  khối, vật liệu, 4 nhân vật dạng khối, keyframe theo giây, máy quay

HILLTOP = Vector((8.0, 1.5, 2.4))
PIKO_AT = Vector((3.42, 0.28, 0.0))
LEAF_AT = Vector((2.95, 0.12, 0.875))
LEAF_TIP = Vector((3.116, 0.1, 0.84))
FLOWER_AT = Vector((3.85, -0.3, 0.0))
TAVI_Y = -0.28
RIGHT, LEFT = 62, -62
HOLD = 1 / 24                                                    # một khung: key ẩn và key hiện cách nhau ít hơn thì rơi vào cùng khung
COMPASS_FACE = Vector((0.25, -1.0, 0.5)).normalized()           # mặt la bàn hướng về phía máy quay, hơi ngửa


def load_timing(timing):
    spec = importlib.util.spec_from_file_location("canh01_timing", ROOT / timing)
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    return tm


def yaw_to(src, dst):
    """Hướng (yaw) để nhìn từ src tới dst: 0 = -Y, 90 = +X."""
    return math.degrees(math.atan2(dst[0] - src[0], -(dst[1] - src[1])))


def near(a, ref):
    """Góc a cộng trừ 360 cho gần ref nhất, để nội suy không quay vòng."""
    return a + 360 * round((ref - a) / 360)


class Act:
    """Giữ (nghiêng, lăn, hướng) và vị trí của gốc nhân vật để mỗi key ghi đủ ba trục. Gọi theo thứ tự thời gian."""

    def __init__(self, rig, x, y, yaw):
        self.r, self.x, self.y, self.yaw, self.lean, self.roll = rig, x, y, yaw, 0.0, 0.0

    def pose(self, t, lean=None, yaw=None, roll=None):
        self.lean = self.lean if lean is None else lean
        self.yaw = self.yaw if yaw is None else yaw
        self.roll = self.roll if roll is None else roll
        rot(self.r.root, [(t, (self.lean, self.roll, self.yaw))])

    def go(self, t, x=None, y=None, z=0.0):
        self.x = self.x if x is None else x
        self.y = self.y if y is None else y
        key(self.r.root, "location", t, Vector((self.x, self.y, z)))


def head(r, t, pitch=0.0, roll=0.0, yaw=0.0):
    rot(r.head, [(t, (pitch, roll, yaw))])


def flash(ob, t, size=1.0, dur=0.6):
    key(ob, "scale", t - HOLD, Vector((0, 0, 0)))
    for u, s in ((0.0, 0.2), (0.2, 1.4), (0.5, 0.7), (0.75, 1.1), (1.0, 0.0)):
        key(ob, "scale", t + u * dur, Vector((s * size,) * 3))


def twinkle(ob, t0, t1, size=1.0):
    key(ob, "scale", t0 - HOLD, Vector((0, 0, 0)))
    t, i = t0, 0
    while t < t1:
        key(ob, "scale", t, Vector(((1.3 if i % 2 else 0.8) * size,) * 3))
        t, i = t + 0.15, i + 1
    key(ob, "scale", t1 + 0.1, Vector((0, 0, 0)))


def at(t):
    bpy.context.scene.frame_set(fr(t))


def build(timing, offset, seconds, out_blend, segment=None):
    """seconds: độ dài video render (số nguyên giây Seedance nhận); segment: độ dài đoạn trong cảnh. Từ segment tới
    seconds chỉ giữ cú máy cuối (diễn vẫn chạy tiếp), lúc dựng cắt bỏ."""
    segment = seconds if segment is None else segment
    tm = load_timing(timing)
    start(tm.FPS, seconds, offset)
    T_END = tm.SECONDS

    # ============================================================ bối cảnh: thung lũng khô, vườn mầm, cành lá, bông hoa, đồi
    grey = material("M_Ground", (0.42, 0.41, 0.39), 0.9)
    crack_m = material("M_Crack", (0.12, 0.11, 0.10), 0.95)
    soil = material("M_Soil", (0.20, 0.19, 0.18), 0.95)
    sprout_m = material("M_Sprout", (0.30, 0.30, 0.30), 0.8)
    hill_m = material("M_Hill", (0.36, 0.35, 0.33), 0.9)
    prop = material("M_Prop", (0.62, 0.62, 0.64), 0.5)
    compass_m = material("M_Compass", (0.42, 0.40, 0.36), 0.5)
    prop_dark = material("M_PropDark", (0.22, 0.22, 0.24), 0.5)
    leaf_m = material("M_Leaf", (0.35, 0.32, 0.29), 0.8)
    critter_m = material("M_Critter", (0.70, 0.70, 0.70), 0.7)
    dew_m = material("M_Dew", (0.75, 0.9, 1.0), 0.05, emit=((0.75, 0.9, 1.0), 2.0))
    glint_m = material("M_Glint", (1.0, 1.0, 1.0), 0.3, emit=((1.0, 1.0, 1.0), 3.0))
    gold_m = material("M_GoldGlint", (1.0, 0.85, 0.2), 0.3, emit=((1.0, 0.8, 0.2), 3.0))
    light_m = material("M_NoriLight", (1.0, 0.95, 0.6), 0.5, emit=((1.0, 0.92, 0.55), 1.2))
    mist_m = material("M_Mist", (0.97, 0.97, 1.0), 0.9, emit=((1.0, 1.0, 1.0), 0.3))

    add_obj("Ground", sphere_bm(40.0, (0, 0, -0.8), (1, 1, 0.02), segs=64), grey, "SET")
    add_obj("Hill", sphere_bm(1.0, (HILLTOP.x, HILLTOP.y, 0.0), (3.0, 2.5, HILLTOP.z), segs=48), hill_m, "SET")
    bm = None
    for cx, cy in ((-1.3, 0.3), (-0.6, -0.5), (0.3, 0.5), (0.9, -0.7), (1.5, 0.6), (2.7, -0.75), (3.7, -0.8), (4.9, -0.5)):
        bm = box_bm((0.5, 0.025, 0.012), (cx, cy, 0.0), bm=bm)
    add_obj("Cracks", bm, crack_m, "SET")
    add_obj("TripCrack", box_bm((0.16, 0.8, 0.03), (2.28, -0.1, 0.0)), crack_m, "SET")      # vết nứt Lumo vấp
    add_obj("Garden_Soil", box_bm((2.35, 0.9, 0.06), (3.525, 0.1, 0.0)), soil, "SET")
    bm = None
    for sx, sy in ((3.65, 0.5), (4.3, -0.2), (4.55, 0.35), (2.75, 0.45), (3.95, 0.45), (2.55, 0.3)):
        bm = cyl_bm(0.035, 0.12, (sx, sy, 0.08), bm=bm, cone_top=0.0)
    add_obj("Sprouts", bm, sprout_m, "SET")
    add_obj("Sprout_Thin", cyl_bm(0.025, 0.18, (0, 0, 0.09), cone_top=0.0), sprout_m, "SET",
            loc=(2.45, -0.15, 0.03)).rotation_euler = (0, math.radians(-8), 0)
    glow = add_obj("Sprout_Glow", sphere_bm(0.11), light_m, "PROPS", loc=(2.45, -0.15, 0.12))
    light_cone = add_obj("Nori_LightCone", cyl_bm(0.07, 1.0, (0, 0, -0.5), cone_top=0.015), light_m, "PROPS")

    def critter(name, x, y):
        body = add_obj(name, sphere_bm(0.08, (0, 0, 0.065), (1, 1, 0.8)), critter_m, "SET", loc=(x, y, 0))
        hat = add_obj(name + "_LeafHat", cyl_bm(0.12, 0.012), leaf_m, "SET", parent=body, loc=(0, 0, 0.17))
        hat.rotation_euler = (math.radians(10), 0, 0)
        return body, hat

    for i, (x, y) in enumerate(((-1.2, 0.4), (-0.65, 0.7), (5.1, -0.45))):
        critter(f"Critter_{i}", x, y)
    sigh_body, sigh_hat = critter("Critter_Sigh", 2.66, -0.1)

    add_obj("Twig", cyl_bm(0.013, 0.9, (0, 0, 0.45)), leaf_m, "SET", loc=(LEAF_AT.x - 0.16, LEAF_AT.y, 0.0))
    leaf = add_obj("Leaf", sphere_bm(1.0, scale=(0.17, 0.085, 0.018)), leaf_m, "SET", loc=LEAF_AT)
    leaf.rotation_euler = (math.radians(25), math.radians(12), 0)   # mặt lá ngửa về máy quay; đầu lá (+X) thấp, chĩa về mặt Piko
    dew = add_obj("Dew", sphere_bm(0.035), dew_m, "PROPS", loc=(2.86, 0.1, 0.942))
    leaf_glint = add_obj("Leaf_Glint", sphere_bm(0.025, segs=12), glint_m, "PROPS", loc=LEAF_TIP + Vector((0, -0.04, 0.04)))
    flower = empty("Flower", "SET", loc=FLOWER_AT)
    add_obj("Flower_StemLow", cyl_bm(0.012, 0.26, (0, 0, 0.13)), sprout_m, "SET", parent=flower)
    flower_top = empty("Flower_Top", "SET", parent=flower, loc=(0, 0, 0.26))
    add_obj("Flower_StemHigh", cyl_bm(0.011, 0.1, (0, 0, 0.05)), sprout_m, "SET", parent=flower_top)
    flower_head = empty("Flower_Head", "SET", parent=flower_top, loc=(0, 0, 0.1))
    add_obj("Flower_Bloom", cyl_bm(0.06, 0.03, (0, 0, 0.02), cone_top=0.03), prop, "SET", parent=flower_head)
    bm = None                                                       # dải mây mỏng: các cụm bám sát mặt đồi quanh đỉnh
    for dx, dy, r in ((-1.1, -0.7, 0.45), (-0.35, -1.0, 0.5), (0.45, -0.95, 0.5), (1.15, -0.55, 0.45), (-0.2, -0.2, 0.55),
                      (0.55, 0.2, 0.5)):
        z = HILLTOP.z * math.sqrt(max(0.0, 1 - (dx / 3.0) ** 2 - (dy / 2.5) ** 2))
        bm = sphere_bm(r, (dx, dy, z - HILLTOP.z + r * 0.15), (1.6, 1.0, 0.45), bm=bm)
    mist = add_obj("HillMist", bm, mist_m, "SET", loc=HILLTOP)

    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    COLS["SET"].objects.link(sun)
    sun.data.energy, sun.data.angle = 3.5, math.radians(4)
    sun.rotation_euler = (math.radians(50), 0, math.radians(25))
    world = bpy.data.worlds.new("Sky")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.50, 0.66, 0.92, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9

    # ============================================================ nhân vật và đồ cầm tay
    lumo_r, tavi_r, piko_r = build_lumo((1.6, 0.0, 0)), build_tavi((1.05, TAVI_Y, 0)), build_piko(PIKO_AT)
    nori_r = build_nori((10.0, -0.2, 1.8))
    lumo, tavi, piko = Act(lumo_r, 1.6, 0.0, RIGHT), Act(tavi_r, 1.05, TAVI_Y, RIGHT), Act(piko_r, PIKO_AT.x, PIKO_AT.y, LEFT)
    bsdf_in(cast_materials()["star"], "Emission Strength").default_value = 0.8

    add_obj("Lumo_Bag", box_bm((0.1, 0.06, 0.09)), prop_dark, "CAST", parent=lumo_r.root, loc=(-0.2, -0.1, 0.3))
    compass = add_obj("Lumo_Compass", cyl_bm(0.08, 0.025), compass_m, "PROPS", parent=lumo_r.arm_r, loc=(0.04, -0.04, -0.31))
    needle = add_obj("Lumo_CompassNeedle", box_bm((0.022, 0.11, 0.01), (0, -0.04, 0)), prop_dark, "PROPS", parent=compass,
                     loc=(0, 0, 0.017))
    piko_bag = add_obj("Piko_Bag", sphere_bm(0.06, (0, 0, -0.04), (1, 1, 1.1)), prop_dark, "CAST", parent=piko_r.squash,
                       loc=(0.33, -0.12, 0.24))                     # hông trái, ngang tầm tay
    add_obj("Piko_BagStrap", box_bm((0.02, 0.02, 0.68), (0, 0, 0.34)), prop_dark, "CAST", parent=piko_r.squash,
            loc=(0.33, -0.12, 0.24)).rotation_euler = (math.radians(-10), math.radians(-43), 0)   # chéo lên gốc sừng phải
    bag_glint = add_obj("Piko_BagGlint", sphere_bm(0.035, segs=12), gold_m, "PROPS", parent=piko_bag, loc=(0, -0.04, 0.03))
    spoon_arm = piko_r.arms[1]                                      # tay trái Piko: phía máy quay khi Piko nhìn sang trái
    grip = bpy.data.objects["Piko_Arm_+1"]                          # tay cầm thìa: hạt đậu dẹt bọc quanh đầu cán (nắm tay
    me = bpy.data.meshes.new("Piko_PawGrip")                        # bằng thạch), không phải quả cầu có que xuyên qua
    bm = sphere_bm(0.065, (0, 0, -0.06), (1.0, 0.8, 1.35), segs=16)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(cast_materials()["piko"])
    grip.data = me
    spoon = empty("Piko_Spoon", "PROPS", parent=spoon_arm, loc=(0, -0.01, -0.11))
    spoon.rotation_euler = (math.radians(-15), 0, 0)                # cán ló ra đáy nắm tay, hơi chúi về trước
    add_obj("Piko_SpoonHandle", box_bm((0.022, 0.022, 0.18), (0, 0, -0.09)), prop, "PROPS", parent=spoon)
    spoon_bowl = empty("Piko_SpoonBowlPivot", "PROPS", parent=spoon, loc=(0, 0, -0.18))
    add_obj("Piko_SpoonBowl", sphere_bm(0.045, (0, 0, -0.05), (0.8, 0.4, 1.2)), prop, "PROPS", parent=spoon_bowl)
    spoon_ground = add_obj("Spoon_Ground", box_bm((0.18, 0.022, 0.022), (-0.09, 0, 0)), prop, "PROPS")   # gốc ở chỗ gập
    ground_fold = empty("Spoon_GroundFold", "PROPS", parent=spoon_ground)
    ground_fold.rotation_euler = (0, math.radians(-125), 0)        # lòng thìa gập ngược lên trên cán, như thìa trong tay
    add_obj("Spoon_GroundBowl", sphere_bm(0.045, (0.05, 0, 0), (1.2, 0.8, 0.4)), prop, "PROPS", parent=ground_fold)
    dust = add_obj("DigDust", sphere_bm(0.05, scale=(1.6, 1.0, 0.6)), prop, "PROPS")
    knock_dust = add_obj("KnockDust", sphere_bm(0.05, scale=(1.6, 1.0, 0.6)), prop, "PROPS", loc=(1.62, TAVI_Y - 0.12, 0.03))
    buzz = add_obj("Lumo_Buzz", sphere_bm(0.03, segs=10), gold_m, "PROPS", parent=lumo_r.root, loc=(-0.2, -0.15, 0.4))
    for ob in (compass, spoon, spoon_ground, dust, knock_dust, glow, light_cone, bag_glint, leaf_glint, buzz):
        key(ob, "scale", -1.0, Vector((0, 0, 0)))                   # ẩn bằng scale 0 tới lúc xuất hiện

    # ============================================================ giọt sương, bông hoa, sinh vật thở dài, mây đỉnh đồi
    r0, r1 = tm.DEW_ROLL
    for dt, x, z in ((0.0, 2.86, 0.942), (0.6, 2.93, 0.927), (1.2, 2.93, 0.927), (1.7, 3.01, 0.910), (2.2, 3.01, 0.910),
                     (2.7, 3.10, 0.891)):                          # lăn… dừng… lăn… dừng… lăn tới đầu lá
        key(dew, "location", r0 + dt, Vector((x, 0.1, z)))
    key(dew, "location", tm.SLURP - 0.05, Vector((3.10, 0.1, 0.891)))
    keys(dew, "scale", [(tm.PIKO_JUMP[0] - 0.3, Vector((1, 1, 1))), (tm.PIKO_JUMP[0], Vector((0.9, 0.9, 1.35)))])   # trĩu
    key(dew, "location", tm.SLURP, Vector((3.11, 0.09, 0.85)))      # vào miệng Piko
    key(dew, "scale", tm.SLURP, Vector((0.9, 0.9, 1.35)))
    key(dew, "scale", tm.SLURP + HOLD, Vector((0, 0, 0)))
    d0, d1 = tm.FLOWER_DROOP
    rot(flower_top, [(0.0, (0, -14, 0)), (d0, (0, -14, 0)), (d0 + 0.4, (0, 100, 0)), (d1, (0, 92, 0))])
    rot(flower_head, [(0.0, (0, -30, 0)), (r0 + 0.6, (0, -30, 0)), (r0 + 0.9, (0, -44, 0)), (r0 + 1.3, (0, -30, 0)),
                      (r0 + 1.7, (0, -30, 0)), (r0 + 2.0, (0, -44, 0)), (r0 + 2.4, (0, -30, 0)), (d0, (0, -30, 0)),
                      (d0 + 0.4, (0, 45, 0)), (d1, (0, 40, 0))])    # vươn theo giọt sương, rồi gục
    c0, c1 = tm.CRITTER_SIGH
    keys(sigh_body, "scale", [(c0, Vector((1, 1, 1))), (c0 + 0.3, Vector((1.15, 1.15, 0.78))), (c0 + 0.8, Vector((1.05, 1.05, 0.9)))])
    rot(sigh_hat, [(c0 + 0.3, (10, 0, 0)), (c1, (-35, 0, 0))])
    keys(sigh_hat, "location", [(c0 + 0.3, Vector((0, 0, 0.17))), (c1, Vector((0, -0.05, 0.11)))])   # lá trễ xuống che mắt
    keys(mist, "location", [(0.0, HILLTOP + Vector((-0.12, 0, 0))), (T_END, HILLTOP + Vector((0.12, 0, 0)))])   # trôi chậm

    # ============================================================ PIKO
    sq = piko_r.squash
    piko.pose(0.0, lean=-12, yaw=LEFT)                              # ngửa lên nhìn giọt sương
    j0, j1 = tm.PIKO_JUMP
    for k in range(int((j0 - 0.4) / 0.7) + 1):                       # thở khi chờ
        key(sq, "scale", k * 0.7, Vector((1.03, 1.03, 0.97)) if k % 2 else Vector((1, 1, 1)))
    for dt in (0.6, 1.7):                                           # mỗi lần giọt dừng: ngửa thêm
        piko.pose(r0 + dt, lean=-12)
        piko.pose(r0 + dt + 0.25, lean=-18)
        piko.pose(r0 + dt + 0.6, lean=-12)
    piko.pose(j0, lean=-12)
    keys(sq, "scale", [(j0 - 0.1, Vector((1, 1, 1))), (j0 + 0.12, Vector((1.2, 1.2, 0.78))),     # nén người
                       (j0 + 0.22, Vector((0.88, 0.88, 1.15))), (tm.SLURP + 0.15, Vector((1, 1, 1))),
                       (j1 - 0.03, Vector((1.15, 1.15, 0.85))), (j1 + 0.15, Vector((1, 1, 1)))])   # bẹp khi đáp
    piko.go(j0 + 0.15)
    piko.go(tm.SLURP, z=0.40)                                       # bật lên đớp gọn
    piko.go(j1 - 0.05)
    piko.pose(j1, lean=0)
    fl_yaw = yaw_to(PIKO_AT, FLOWER_AT)
    piko.pose(tm.PIKO_LOOK_FLOWER[0])
    piko.pose(tm.PIKO_LOOK_FLOWER[0] + 0.35, lean=10, yaw=fl_yaw)   # nhìn xuống bông hoa gục
    g0, g1 = tm.PIKO_GRIN
    keys(sq, "scale", [(g0, Vector((1, 1, 1))), (g0 + 0.2, Vector((1.1, 1.1, 0.86))), (g1, Vector((1.1, 1.1, 0.86))),
                       (g1 + 0.3, Vector((1, 1, 1)))])               # co người cười trừ
    rot(piko_r.arms[0], [(0.0, (6, 0, 0)), (g0, (6, 0, 0)), (g0 + 0.25, (-150, 0, 0)), (g1, (-150, 0, 0)), (g1 + 0.3, (6, 0, 0))])
    piko.pose(g1, lean=10)
    piko.pose(g1 + 0.4, lean=0, yaw=RIGHT)
    t = tm.SHOTS[2][1]
    while t < tm.PIKO_TURN - 0.6:                                   # nảy nhẹ tại chỗ
        piko.go(t)
        piko.go(t + 0.3, z=0.025)
        t += 0.6
    piko.go(tm.PIKO_TURN - 0.4)
    piko.pose(tm.PIKO_TURN - 0.15)
    piko.pose(tm.PIKO_TURN + 0.2, yaw=LEFT)                         # nghe TÍT, quay sang phía Lumo
    piko.pose(tm.PIKO_CHECK)
    piko.pose(tm.PIKO_CHECK + 0.2, lean=12)                         # ngó xuống cái túi của mình
    u0, u1 = tm.PIKO_RUMMAGE
    rot(spoon_arm, [(0.0, (6, 0, 0)), (u0, (6, 0, 0)), (u0 + 0.25, (-25, 0, 25))])
    for k in range(int((u1 - 0.1 - u0 - 0.35) / 0.12) + 1):
        rot(spoon_arm, [(u0 + 0.35 + 0.12 * k, (-15 if k % 2 else -35, 0, 25))])   # lục lọi trong túi
    rot(piko_bag, [(u0, (0, 0, 0)), (u0 + 0.2, (14, 0, 0)), (u0 + 0.5, (-14, 0, 0)), (u0 + 0.8, (14, 0, 0)), (u1, (0, 0, 0))])
    keys(spoon, "scale", [(tm.SPOON_OUT - HOLD, Vector((0, 0, 0))), (tm.SPOON_OUT, Vector((1, 1, 1)))])
    rot(spoon_arm, [(tm.SPOON_OUT + 0.2, (-100, 0, 45))])           # giơ cái thìa chếch ra bên hông, không chĩa vào mặt
    piko.pose(tm.SPOON_OUT + 0.2, lean=0)
    k0, k1 = tm.PIKO_LOOK
    piko.pose(k0, lean=4)
    piko.pose(tm.PIKO_GLANCE_FLOWER[0], yaw=fl_yaw)                 # liếc bông hoa gục
    piko.pose(tm.PIKO_GLANCE_FLOWER[1])
    piko.pose(tm.PIKO_LOOK_GROUND[1], lean=14, yaw=LEFT)            # nhìn đất
    rot(spoon_arm, [(tm.PIKO_GLANCE_FLOWER[1], (-100, 0, 45)), (k1, (-165, 30, 0))])   # giơ thìa lên cạnh đầu
    for i, h in enumerate(tm.DIG):                                  # CỘP. CỘP. CỘP!
        if i:
            rot(spoon_arm, [(h - 0.3, (-175 if i == 2 else -165, 30, 0))])   # giơ lên cạnh đầu, xa mặt
        rot(spoon_arm, [(h, (-45, 0, 0))])                          # lòng thìa bổ xuống đất phía trước
        flash(dust, h, 1.2, 0.3)
        if i < 2:
            keys(sq, "scale", [(h - 0.02, Vector((1, 1, 1))), (h + 0.06, Vector((1.07, 1.07, 0.93))), (h + 0.18, Vector((1, 1, 1)))])
    rot(spoon_bowl, [(tm.DIG[2] - 0.02, (0, 0, 0)), (tm.DIG[2] + 0.05, (125, 0, 0))])   # cán thìa cong vòng
    s0, s1 = tm.PIKO_SHAKE
    for k in range(int((s1 - 0.05 - s0) / 0.05) + 1):               # rung bần bật
        key(sq, "scale", s0 + 0.02 + 0.05 * k, Vector((1.06, 1.06, 0.94)) if k % 2 else Vector((0.95, 0.95, 1.05)))
    key(sq, "scale", s1, Vector((1, 1, 1)))
    rot(spoon_arm, [(tm.DIG[2] + 0.1, (-40, 0, 0)), (tm.DIG[2] + 0.5, (-92, 0, 20))])   # giơ thìa cong ra trước ngang thân, thấp hơn mặt: chỗ gập lộ ngang khung
    piko.pose(s1 + 0.1, lean=6)
    piko.pose(tm.PIKO_BLINK[0] + 0.1, lean=0)
    q0, q1 = tm.PIKO_SET_SPOON                                      # với ra xa, đặt cái thìa cong xuống đất
    rot(spoon_arm, [(q0, (-92, 0, 20)), (q1 - 0.1, (-65, 0, 0)), (q1, (-65, 0, 0))])
    piko.pose(q0, lean=0)
    piko.pose(q1 - 0.1, lean=28)
    piko.pose(q1, lean=28)
    keys(spoon, "scale", [(q1 - 0.1, Vector((1, 1, 1))), (q1 - 0.1 + HOLD, Vector((0, 0, 0)))])
    keys(spoon_ground, "scale", [(q1 - 0.1, Vector((0, 0, 0))), (q1 - 0.1 + HOLD, Vector((1, 1, 1)))])
    rot(spoon_arm, [(q1 + 0.25, (6, 0, 0))])
    piko.pose(q1 + 0.3, lean=0)
    piko.go(q1 + 0.1)                                               # nảy lùi ra, để cái thìa nằm xa cái túi
    piko.go(q1 + 0.3, PIKO_AT.x + 0.11, PIKO_AT.y + 0.04, z=0.06)
    piko.go(q1 + 0.5, PIKO_AT.x + 0.22, PIKO_AT.y + 0.08)
    lf = tm.TAVI_LOOK_LEAF[0] + 0.5                                 # chiếc lá lấp lánh: Piko ngước lên, nảy một cái
    piko.pose(lf, lean=-16)
    piko.go(lf + 0.1)
    piko.go(lf + 0.25, z=0.07)
    piko.go(lf + 0.4)
    piko.pose(tm.TAVI_LOOK_UP[1], lean=0)
    gl = tm.GROUP_LOOK                                              # cả nhóm ngước theo tay Tavi về đỉnh đồi
    piko.pose(gl + 0.1)
    piko.pose(gl + 0.5, lean=-16, yaw=yaw_to((piko.x, piko.y), HILLTOP))

    # ============================================================ LUMO
    L = lumo_r
    lumo.pose(0.0, lean=10)                                         # co người ủ rũ
    key(L.root, "scale", 0.0, Vector((1.03, 1.03, 0.94)))
    head(L, 0.0, 18)
    for ear, side in L.ears:
        rot(ear, [(0.0, (0, side * 65, 0))])
    rot(L.tail, [(0.0, (-30, 0, 0))])
    for a in (L.arm_l, L.arm_r):
        rot(a, [(0.0, (-6, 0, 0))])
    sp0, sp1 = tm.LUMO_SPRING                                       # bật dậy
    lumo.pose(sp0, lean=10)
    lumo.pose(sp0 + 0.3, lean=0)
    head(L, sp0, 18)
    head(L, sp0 + 0.32, 0)
    keys(L.root, "scale", [(sp0, Vector((1.03, 1.03, 0.94))), (sp0 + 0.12, Vector((1.05, 1.05, 0.9))),
                           (sp0 + 0.3, Vector((0.97, 0.97, 1.04))), (sp1, Vector((1, 1, 1)))])
    lumo.go(sp0)
    lumo.go(sp0 + 0.3, z=0.1)
    lumo.go(sp1 + 0.05)
    for ear, side in L.ears:
        rot(ear, [(sp0, (0, side * 65, 0)), (sp0 + 0.32, (0, side * 10, 0))])
    rot(L.tail, [(sp0, (-30, 0, 0))])
    wag(L.tail, sp0 + 0.3, tm.LUMO_DASH[0], 0.4, 20, (20, 0, 0))
    rot(L.arm_r, [(tm.LUMO_LINE[0] - 0.1, (-6, 0, 0)), (tm.LUMO_LINE[0] + 0.1, (-95, 0, 0)), (tm.LUMO_LINE[1] - 0.1, (-95, 0, 0))])
    dsh0, dsh1 = tm.LUMO_DASH                                       # lao đi: một bước, hai bước, tới vết nứt
    rot(L.arm_r, [(dsh0, (-40, 0, 0))])
    lumo.pose(dsh0, lean=0)
    lumo.go(dsh0, 1.6)
    lumo.pose(dsh0 + 0.2, lean=12)
    for i, x in enumerate((1.75, 1.88, 2.0, 2.1)):
        t = dsh0 + (dsh1 - dsh0) * (i + 1) / 4
        lumo.go(t, x, z=0.05 if i % 2 == 0 else 0.0)
        rot(L.arm_r, [(t, (-60 if i % 2 == 0 else 20, 0, 0))])
        rot(L.arm_l, [(t, (20 if i % 2 == 0 else -60, 0, 0))])
    steps(L.legs, dsh0, dsh1, 4, 30)
    trip = tm.LUMO_TRIP                                             # vấp vết nứt, chúi người, treo chúi trên khe
    lumo.pose(trip, lean=12)
    lumo.pose(trip + 0.15, lean=25)
    lumo.go(trip + 0.15, 2.13)
    da0, da1 = tm.LUMO_DANGLE
    for k in range(int((da1 - 0.05 - trip - 0.1) / 0.16) + 1):      # tay chới với
        t = trip + 0.1 + 0.16 * k
        rot(L.arm_r, [(t, (-95 if k % 2 else -20, 0, 0))])
        rot(L.arm_l, [(t, (-20 if k % 2 else -95, 0, 0))])
    lumo.pose(tm.LUMO_STUMBLE[1], lean=32)
    lumo.go(tm.LUMO_STUMBLE[1], 2.16)
    lumo.pose(da0 + 0.2, lean=42)
    lumo.pose(da1, lean=42)
    lumo.go(da1, 2.17)
    head(L, trip + 0.1, 15)
    for ear, side in L.ears:
        rot(ear, [(trip + 0.1, (0, side * 35, 0))])
    rot(L.tail, [(trip, (20, 0, 0)), (trip + 0.2, (55, 0, 0))])     # đuôi vung lên
    p0, p1 = tm.LUMO_PULLED                                         # bị kéo đứng lại
    lumo.pose(p0 + 0.2, lean=-8)
    lumo.go(p0 + 0.25, 2.1)
    lumo.pose(p1, lean=0)
    for a in (L.arm_l, L.arm_r):
        rot(a, [(p0 + 0.25, (-6, 0, 0))])
    rot(L.tail, [(p0 + 0.25, (20, 0, 0))])
    for ear, side in L.ears:
        rot(ear, [(p0 + 0.25, (0, side * 15, 0)), (tm.TAVI_LINE[0] + 0.2, (0, side * 60, 0))])   # ngượng: tai cụp
    head(L, tm.TAVI_LINE[0], 0)
    head(L, tm.TAVI_LINE[0] + 0.3, 18)                              # nhìn xuống vết nứt
    keys(L.root, "scale", [(tm.TAVI_LINE[0] + 0.3, Vector((1, 1, 1))), (tm.TAVI_LINE[0] + 0.5, Vector((1.04, 1.04, 0.95))),
                           (tm.TAVI_LINE[0] + 0.8, Vector((1, 1, 1)))])   # nhún vai
    b0, b1 = tm.COMPASS_BUZZ                                        # la bàn rung trong túi da: TÍT TÍT TÍT
    head(L, b0 + 0.2, 26, 0, -25)                                   # cúi nhìn túi da bên hông phải
    for ear, side in L.ears:
        rot(ear, [(b0 + 0.05, (0, side * 10, 0))])
    for t in (b0 + 0.05, b0 + 0.45, b0 + 0.85):
        flash(buzz, t, 1.0, 0.25)
    o0, o1 = tm.COMPASS_OUT                                         # rút la bàn, cầm hai tay trước ngực
    rot(L.arm_r, [(o0, (-6, 0, 0)), (o0 + 0.15, (-25, 0, 0)), (o1 - 0.05, (-70, 0, 0))])
    rot(L.arm_l, [(o1 - 0.2, (-6, 0, 0)), (o1 - 0.05, (-70, -15, 0))])
    keys(compass, "scale", [(o0 + 0.2 - HOLD, Vector((0, 0, 0))), (o0 + 0.2, Vector((1, 1, 1)))])
    head(L, o1 - 0.05, 22)
    e0, e1 = tm.LUMO_LINE2                                          # "Có gì lạ kìa!": chìa la bàn về phía Piko
    rot(L.arm_r, [(e0 - 0.05, (-70, 0, 0)), (e0 + 0.15, (-95, 0, 0)), (e1 + 0.1, (-95, 0, 0)), (e1 + 0.4, (-70, 0, 0))])
    rot(L.arm_l, [(e1 + 0.1, (-70, -15, 0)), (e1 + 0.4, (-6, 0, 0))])
    head(L, e0, 22)
    head(L, e0 + 0.2, 0)
    lumo.pose(e0, lean=0)
    lumo.pose(e0 + 0.2, lean=6)
    lumo.pose(e1 + 0.4, lean=0)
    w0, w1 = tm.STAR_STILL                                          # bước tới, cúi xuống kề la bàn sát cái thìa
    x0, x1 = tm.LUMO_TEST
    lumo_test_at = Vector((2.62, 0.02, 0.0))                        # chỉnh lại theo chỗ cái thìa ở dưới (test_spot)

    def test_spot(p):
        key(L.root, "location", w0 + 0.15, Vector(((2.1 + p.x) / 2, p.y / 2, 0.04)))
        key(L.root, "location", x0, Vector((p.x, p.y, 0)))
        key(L.root, "location", tm.TAVI_KNOCK[0] + 0.1, Vector((p.x, p.y, 0)))

    lumo.go(w0, 2.1)
    test_spot(lumo_test_at)
    steps(L.legs, w0, x0, 2, 25)
    lumo.pose(x0, lean=0)
    lumo.pose(x0 + 0.3, lean=38)
    keys(L.root, "scale", [(x0, Vector((1, 1, 1))), (x0 + 0.3, Vector((1.03, 1.03, 0.9)))])
    rot(L.arm_r, [(x0, (-70, 0, 0)), (x0 + 0.3, (-92, 0, 0))])      # cùng với cúi 38°: la bàn trước ngực, sát mặt đất
    head(L, x0 + 0.3, 14)
    # LUMO_PUZZLE: đứng dậy, nhìn thìa, nhìn la bàn, nghiêng đầu
    lumo.pose(tm.LUMO_STAND[0], lean=38)
    lumo.pose(tm.LUMO_STAND[1], lean=0)
    keys(L.root, "scale", [(tm.LUMO_STAND[0], Vector((1.03, 1.03, 0.9))), (tm.LUMO_STAND[1], Vector((1, 1, 1)))])
    rot(L.arm_r, [(tm.LUMO_STAND[0], (-92, 0, 0)), (tm.LUMO_STAND[1], (-60, 0, 0))])
    head(L, tm.LUMO_STAND[0], 14)
    head(L, tm.LUMO_STAND[1], 12)
    head(L, tm.LUMO_LOOK_COMPASS[1], 24)                            # nhìn la bàn
    head(L, tm.LUMO_TILT[0], 24)
    head(L, tm.LUMO_TILT[1], 0, 18, 0)                              # nghiêng đầu
    for ear, side in L.ears:
        rot(ear, [(tm.LUMO_TILT[0], (0, side * 10, 0)), (tm.LUMO_TILT[1], (0, side * 35, 0))])
    kn0, kn1 = tm.TAVI_KNOCK                                        # Tavi dậm đất: Lumo quay sang nhìn
    lumo.pose(kn0 + 0.1)
    lumo.pose(kn0 + 0.35, yaw=LEFT)
    lumo.go(kn0 + 0.45, 2.25, 0.0)
    steps(L.legs, kn0 + 0.1, kn0 + 0.45, 2, 25)
    head(L, kn0 + 0.35, 10)
    rot(L.arm_r, [(kn0 + 0.1, (-60, 0, 0)), (kn0 + 0.4, (-15, 0, 0))])
    for ear, side in L.ears:
        rot(ear, [(kn0 + 0.3, (0, side * 12, 0))])
    head(L, tm.TAVI_LOOK_UP[1], -15)
    head(L, tm.TAVI_GATHER[0], 0)
    i0, i1 = tm.TAVI_IDEA                                           # Tavi "à!": Lumo giật mình rồi chồm tới nghe
    lumo.pose(i0 + 0.3, lean=0)
    lumo.pose(i0 + 0.5, lean=-4)
    lumo.pose(i1, lean=6)
    for n0 in (tm.TAVI_GATHER[0], tm.TAVI_SHIVER[0], tm.TAVI_RAIN[0]):   # gật đầu theo từng bước
        head(L, n0 + 0.2, 0)
        head(L, n0 + 0.4, 12)
        head(L, n0 + 0.6, 0)
    sh0 = tm.TAVI_SHIVER[0]                                         # "làm lạnh,": Lumo rùng mình theo
    for k in range(8):
        lumo.pose(sh0 + 0.3 + 0.07 * k, roll=10 if k % 2 else -10)
    lumo.pose(sh0 + 0.95, roll=0)
    for ear, side in L.ears:                                        # tai cụp khi rùng mình
        rot(ear, [(sh0 + 0.2, (0, side * 12, 0)), (sh0 + 0.35, (0, side * 60, 0)), (sh0 + 0.95, (0, side * 60, 0)),
                  (sh0 + 1.15, (0, side * 12, 0))])
    pt0, pt1 = tm.TAVI_POINT
    lumo.pose(pt0, lean=0)
    lumo.go(pt0 + 0.1, 2.25)
    lumo.go(pt0 + 0.35, 2.12)                                       # lùi lại nhường chỗ cho Tavi
    steps(L.legs, pt0 + 0.1, pt0 + 0.35, 1, 20)
    lumo.pose(gl)
    lumo.pose(gl + 0.25, yaw=yaw_to((2.12, 0.0), HILLTOP))          # quay theo tay Tavi, sau khi Tavi đã chỉ
    head(L, gl + 0.25, 0)
    head(L, gl + 0.45, -26)
    lumo.pose(gl + 0.55, lean=-4)
    wag(L.tail, p1, T_END, 0.5, 14, (20, 0, 0))

    # ============================================================ TAVI
    T = tavi_r
    tavi.pose(0.0, lean=6)
    head(T, 0.0, 14)
    for a in (T.arm_l, T.arm_r):
        rot(a, [(0.0, (-6, 0, 0))])
    wag(T.tail, 0.0, T_END, 2.0, 8, (-12, 0, 0))
    head(T, dsh0, 14)
    head(T, dsh0 + 0.15, 0)
    tavi.go(dsh0, 1.05)
    tavi.go(dsh0 + 0.35, 1.25, z=0.04)                              # bước theo Lumo
    tavi.go(trip, 1.4)
    steps(T.legs, dsh0, trip, 3, 20)
    lg0, lg1 = tm.TAVI_LUNGE                                        # lao tới chụp quai túi da của Lumo
    tavi.pose(lg0, lean=8)
    tavi.pose(lg0 + 0.15, lean=20)
    tavi.go(lg0 + 0.2, 1.65, z=0.05)
    tavi.go(lg1, 1.82)
    tavi.pose(lg1, lean=25)
    rot(T.arm_r, [(lg0, (-6, 0, 0)), (lg1 - 0.05, (-105, 0, 0)), (da1, (-105, 0, 0))])
    tavi.go(da1, 1.86)                                              # giữ chặt, bị kéo theo một chút
    tavi.pose(da1, lean=25)
    tavi.pose(p0 + 0.2, lean=-12)                                   # kéo lại
    tavi.go(p0 + 0.25, 1.65)
    rot(T.arm_r, [(p0 + 0.25, (-75, 0, 0)), (p1, (-6, 0, 0))])
    tavi.pose(p1, lean=0)
    head(T, tm.TAVI_LINE[0] + 0.1, 10)
    rot(T.arm_r, [(tm.TAVI_LINE[0], (-6, 0, 0)), (tm.TAVI_LINE[0] + 0.2, (-45, 0, 0)), (tm.TAVI_LINE[1], (-45, 0, 0)),
                  (tm.TAVI_LINE[1] + 0.2, (-6, 0, 0))])             # chỉ xuống vết nứt
    st0, st1 = tm.TAVI_STEP_BACK                                    # lùi ra chỗ trống
    tavi.go(st0, 1.65)
    tavi.go(st0 + 0.3, 1.47, z=0.03)
    tavi.go(st1, 1.3)
    steps(T.legs, st0, st1, 2, 20)
    head(T, st0, 0)
    n0, n1 = tm.TAVI_STEP_IN                                        # bước lại xem cái thìa cong
    tavi.go(n0, 1.3)
    tavi.go(n0 + 0.3, 1.43, z=0.03)
    tavi.go(n1, 1.55)
    steps(T.legs, n0, n1, 2, 20)
    head(T, n1, 14)
    head(T, kn0, 0)
    head(T, kn0 + 0.15, 18)                                         # nhìn xuống mặt đất nứt
    for t in tm.TAVI_STAMPS:                                # CỘC. CỘC.
        tavi.go(t - 0.3)
        tavi.go(t - 0.15, z=0.13)
        tavi.go(t)
        keys(T.root, "scale", [(t - 0.3, Vector((1, 1, 1))), (t, Vector((1.1, 1.1, 0.88))), (t + 0.15, Vector((1, 1, 1)))])
        flash(knock_dust, t, 2.0, 0.25)
    tv = (1.55, TAVI_Y)
    v0 = tm.TAVI_LOOK_LEAF[0]                                       # ngước nhìn chiếc lá còn ướt sương
    head(T, v0, 18)
    head(T, v0 + 0.3, -12, 0, yaw_to(tv, LEAF_TIP) - RIGHT)
    lu0, lu1 = tm.TAVI_LOOK_UP                                      # ngẩng dần lên đỉnh đồi
    head(T, lu0, -12, 0, yaw_to(tv, LEAF_TIP) - RIGHT)
    head(T, lu1, -30, 0, yaw_to(tv, HILLTOP) - RIGHT)
    head(T, tm.TAVI_SNAP[0], -30, 0, yaw_to(tv, HILLTOP) - RIGHT)
    head(T, tm.TAVI_SNAP[1], 0)                                 # "à!": quay phắt sang Lumo
    tavi.go(i0 + 0.3)
    tavi.go(tm.TAVI_SNAP[1], z=0.06)
    tavi.go(i0 + 0.6)
    keys(T.root, "scale", [(i0 + 0.3, Vector((1.05, 1.05, 0.93))), (tm.TAVI_SNAP[1], Vector((0.96, 0.96, 1.06))),
                           (i0 + 0.6, Vector((1, 1, 1)))])
    rot(T.arm_r, [(i0 + 0.3, (-6, 0, 0)), (tm.TAVI_SNAP[1], (-120, 0, 0)), (i1, (-120, 0, 0))])  # giơ một ngón tay
    tavi.pose(i1, lean=6)
    a0, a1 = tm.TAVI_GATHER                                         # "Gom hơi nước,": vung tay ra sau rồi vun về trước bụng
    for arm, s in ((T.arm_r, 1), (T.arm_l, -1)):
        rot(arm, [(a0, (-120 if s > 0 else -6, 0, 0)), (a0 + 0.25, (35, 0, 0)), (a0 + 0.6, (-80, 0, s * 25)),
                  (a1 - 0.1, (-70, 0, s * 30))])
    tavi.pose(a0 + 0.25, lean=-4)
    tavi.pose(a0 + 0.6, lean=8)
    h0, h1 = tm.TAVI_SHIVER                                         # "làm lạnh,": hai tay áp lên ngực, rùng mình
    for arm, s in ((T.arm_r, 1), (T.arm_l, -1)):
        rot(arm, [(h0 + 0.15, (-65, 0, s * 55)), (h1, (-65, 0, s * 55)), (h1 + 0.15, (-6, 0, 0))])
    head(T, h0 + 0.15, 12)
    head(T, h1 + 0.1, 0)
    tavi.pose(h0, lean=0)
    for k in range(int((h1 - 0.25 - h0) / 0.07)):
        tavi.pose(h0 + 0.15 + 0.07 * k, roll=6 if k % 2 else -6)
    tavi.pose(h1, roll=0)
    f0, f1 = tm.TAVI_RAIN                                           # "sẽ có mưa!": giơ hai tay rồi rung ngón hạ dần
    for arm, s in ((T.arm_r, 1), (T.arm_l, -1)):
        rot(arm, [(f0 + 0.15, (-165, 0, s * 10))])   # hai tay giơ qua đầu
        for k in range(int((f1 - 0.35 - f0) / 0.1) + 1):
            rot(arm, [(f0 + 0.25 + 0.1 * k, (-165 + 10 * k + (8 if (k + (s > 0)) % 2 else -8), 0, s * 10))])
    head(T, f1 - 0.2, 14)
    tavi.go(pt0, 1.55)                                              # bước lên trước Lumo, chỉ dốc lên đỉnh đồi
    tavi.go(pt0 + 0.25, 2.15, TAVI_Y - 0.25, z=0.04)
    tavi.go(tm.TAVI_STRIDE[1], 3.05, TAVI_Y - 0.05)
    steps(T.legs, pt0, tm.TAVI_STRIDE[1], 3, 25)
    tavi.pose(tm.TAVI_STRIDE[1])
    tavi.pose(pt0 + 0.7, lean=-8, yaw=yaw_to((3.05, TAVI_Y - 0.05), HILLTOP))
    rot(T.arm_l, [(tm.TAVI_STRIDE[1], (-6, 0, 0))])
    rot(T.arm_r, [(tm.TAVI_STRIDE[1], (-6, 0, 0)), (pt0 + 0.7, (-160, 0, 0)), (T_END, (-160, 0, 0))])
    head(T, tm.TAVI_STRIDE[1], 0)
    head(T, pt0 + 0.7, -32)

    # ============================================================ NORI: bay ngang khi tên phim còn hiện, rọi mầm cây, bay xem
    N = nori_r
    f0, f1 = tm.NORI_FLY_IN
    path = [(0.0, (10.0, -0.2, 1.8)), (f0, (10.0, -0.2, 1.8)), (f0 + (f1 - f0) * 0.4, (5.6, -0.2, 1.9)),
            (f0 + (f1 - f0) * 0.75, (3.8, -0.2, 1.5)), (f1, (2.78, -0.2, 0.7)), (tm.NORI_LIGHT[1], (2.78, -0.2, 0.7)),
            (tm.NORI_LIGHT[1] + 0.8, (2.7, 0.45, 1.15)), (tm.SPOON_OUT, (2.7, 0.45, 1.15)),
            (tm.SPOON_OUT + 0.5, (2.75, 0.5, 1.4)), (w1, (2.75, 0.5, 1.4)), (w1 + 0.4, (2.75, 0.45, 1.2)),
            (kn0, (2.75, 0.45, 1.2)), (kn0 + 0.6, (2.3, 0.45, 1.2)), (i0, (2.3, 0.45, 1.2)), (i0 + 0.6, (2.8, 0.45, 1.25)),
            (gl - 0.3, (2.8, 0.45, 1.25)), (gl + 0.4, (2.0, 0.45, 1.35))]
    for t, p in path:
        key(N.root, "location", t, Vector(p))
    yaw_n = [(0.0, LEFT), (tm.NORI_LIGHT[0] - 0.1, LEFT), (sp0 + 0.3, LEFT - 20), (tm.PIKO_TURN, LEFT), (gl - 0.1, LEFT),
             (gl + 0.3, yaw_to((2.0, 0.45), HILLTOP))]
    pitch_n = [(0.0, 0), (tm.NORI_LIGHT[0] - 0.1, 0), (tm.NORI_LIGHT[0] + 0.1, 20), (tm.NORI_LIGHT[1], 20),
               (tm.NORI_LIGHT[1] + 0.3, 0), (trip, 0), (trip + 0.1, 15), (p1, 15), (p1 + 0.3, 0), (gl + 0.3, 0), (gl + 0.6, -15)]

    def lerp_keys(ks, t):
        for (ta, va), (tb, vb) in zip(ks, ks[1:]):
            if ta <= t <= tb:
                return va + (vb - va) * ss((t - ta) / max(1e-6, tb - ta))
        return ks[-1][1] if t > ks[-1][0] else ks[0][1]

    for t in sorted({t for t, _ in yaw_n} | {t for t, _ in pitch_n}):
        rot(N.root, [(t, (lerp_keys(pitch_n, t), 0, lerp_keys(yaw_n, t)))])
    for w, sx, sz in N.wings:
        wag(w, 0.0, T_END, 0.5, 18, (0, 0, sx * (25 if sz > 0 else -15)))
    nl0, nl1 = tm.NORI_LIGHT                                        # rọi sáng mầm cây gầy nhom
    rot(N.arms[1], [(0.0, (0, 0, 0)), (nl0 - 0.1, (0, 0, 0)), (nl0 + 0.1, (-70, 0, 0)), (nl1, (-70, 0, 0)), (nl1 + 0.2, (0, 0, 0))])
    for ob in (light_cone, glow):
        keys(ob, "scale", [(nl0 - HOLD, Vector((0, 0, 0))), (nl0, Vector((1, 1, 1))), (nl1, Vector((1, 1, 1))),
                           (nl1 + HOLD, Vector((0, 0, 0)))])

    # ============================================================ ánh lóe: túi Piko mỗi lần la bàn chỉ vào; lá ướt sương
    for t in (tm.STAR_SPIN[1] + 0.35, e0 + 0.3, x1 + 0.4):
        flash(bag_glint, t, 1.3)
    twinkle(leaf_glint, tm.TAVI_LOOK_LEAF[0] + 0.5, tm.TAVI_LOOK_UP[0] + 0.3)

    # ============================================================ đặt theo vị trí thật sau khi diễn xong
    at(q1 - 0.1)                                                    # cái thìa nằm đúng chỗ Piko buông tay
    p = spoon_bowl.matrix_world.translation
    spoon_ground.location = (p.x, p.y, 0.02)
    spoon_ground.rotation_euler = (0, 0, math.radians(LEFT - 90))
    at(tm.DIG[0])
    p = spoon_bowl.matrix_world.translation
    dust.location = (p.x, p.y, 0.03)
    at(x0 + 0.3)                                                    # dời chỗ Lumo cúi để la bàn ở ngay trên cái thìa
    want = spoon_ground.location + Vector((0.0, -0.05, 0.2))
    got = compass.matrix_world.translation
    test_spot(lumo_test_at + Vector((want.x - got.x, want.y - got.y, 0)))
    at(nl0 + 1.0)                                                   # vệt sáng từ tay Nori xuống mầm cây
    src = N.arms[1].matrix_world @ Vector((0, 0, -0.08))
    d = glow.location - src
    light_cone.location = src
    light_cone.rotation_mode = "QUATERNION"
    light_cone.rotation_quaternion = Vector((0, 0, -1)).rotation_difference(d.normalized())
    for t in (nl0, nl1):
        key(light_cone, "scale", t, Vector((1, 1, d.length)))

    # la bàn: mặt luôn nghiêng về phía máy quay dù tay Lumo cử động (key mỗi 4 khung từ lúc rút ra)
    face_q = COMPASS_FACE.to_track_quat("Z", "Y")
    for f in range(fr(o0 + 0.15), fr(T_END) + 1, 4):
        bpy.context.scene.frame_set(f)
        local = compass.parent.matrix_world.to_quaternion().inverted() @ face_q
        compass.rotation_euler = local.to_euler("XYZ", compass.rotation_euler)
        compass.keyframe_insert("rotation_euler", frame=f)

    def needle_to(t, target):
        """Góc mũi sao (độ, quanh trục mặt la bàn) chỉ về target chiếu lên mặt la bàn; 0 = chỉ xuống mép dưới."""
        at(t)
        m = compass.matrix_world
        v = m.to_quaternion().inverted() @ (target() - m.translation)
        return math.degrees(math.atan2(v.x, -v.y))

    bag = lambda: piko_bag.matrix_world.translation.copy()           # noqa: E731
    spoon_at = lambda: spoon_ground.matrix_world.translation.copy()  # noqa: E731
    ss0, ss1 = tm.STAR_SPIN                                         # quay loạn rồi chỉ về túi Piko
    end = 720 + needle_to(ss1, bag)
    nk = [(0.0, 15.0), (ss0, 15.0)]
    for k in range(1, int((ss1 - ss0) / 0.1) + 1):
        u = (0.1 * k) / (ss1 - ss0)
        nk.append((ss0 + 0.1 * k, 15 + (end - 15) * (1 - (1 - u) ** 2.5)))
    nk += [(ss1, end), (ss1 + 0.1, end + 8), (ss1 + 0.2, end - 4), (ss1 + 0.3, end)]

    def track(t0, t1, target):
        t = t0
        while t < t1 - 1e-6:
            nk.append((t, near(needle_to(t, target), nk[-1][1])))
            t += 0.25

    track(ss1 + 0.55, x0 + 0.05, bag)                               # vẫn chỉ túi khi Lumo bước tới
    nk.append((tm.NEEDLE_TO_SPOON, near(needle_to(tm.NEEDLE_TO_SPOON, spoon_at), nk[-1][1])))  # kề thìa: giật về thìa…
    nk.append((x1, near(needle_to(x1, spoon_at), nk[-1][1])))
    back = near(needle_to(x1 + 0.15, bag), nk[-1][1])               # …rồi quay lại chỉ túi
    nk += [(x1 + 0.15, back + 8), (x1 + 0.27, back - 4), (x1 + 0.39, back)]
    track(x1 + 0.6, T_END + 0.01, bag)
    rot(needle, [(t, (0, 0, a)) for t, a in nk])

    # ============================================================ máy quay (một máy mỗi cú; chỉ dựng các cú trong đoạn)
    S = {n: (a, b) for n, a, b in tm.SHOTS}
    at(ss1 + 0.3)
    cp, bp = compass.matrix_world.translation.copy(), bag()
    nrm = compass.matrix_world.to_quaternion() @ Vector((0, 0, 1))
    at(x1 - 0.1)
    ct, sp = compass.matrix_world.translation.copy(), spoon_at()
    CAMS = {   # (giây, vị trí máy, điểm nhìn, tiêu cự mm)
        "S1": [(S["S1"][0], (3.3, -1.45, 0.8), (3.25, 0.0, 0.7), 30)],                      # cận lá, giọt sương, mắt Piko, hoa
        "S2": [(S["S2"][0], (3.5, -2.9, 0.75), (3.5, 0.1, 0.5), 35)],                      # Piko, bông hoa, chiếc lá
        "S3": [(S["S3"][0], (3.2, -7.0, 1.4), (4.2, 1.0, 1.1), 28),                         # toàn thung lũng khô, Nori bay ngang
               (S["S3"][1], (3.35, -6.8, 1.4), (4.2, 1.0, 1.1), 28)],
        "S4": [(S["S4"][0], (2.1, -2.9, 0.8), (2.2, 0.0, 0.5), 38)],                        # Nori rọi mầm, Lumo bật dậy
        "S5": [(S["S5"][0], (2.2, -3.6, 0.8), (2.25, 0.0, 0.48), 35)],                      # Lumo lao đi, vấp, Tavi kéo lại
        "S6": [(S["S6"][0], tuple(cp + nrm * 0.45 + Vector((-0.3, 0, 0.05))), tuple(cp + (bp - cp) * 0.3), 35)],   # cận la bàn
        "S7": [(S["S7"][0], (2.75, -2.8, 0.75), (2.8, 0.05, 0.5), 35)],                     # Lumo và Piko: "Có gì lạ kìa!"
        "S8": [(S["S8"][0], (3.25, -2.2, 0.6), (3.3, 0.1, 0.38), 38)],                      # Piko lục túi, đào
        "S9": [(S["S9"][0], (3.15, -1.35, 0.6), (3.25, 0.1, 0.45), 40)],                    # cận Piko và cái thìa cong
        "S10": [(S["S10"][0], tuple(ct + nrm * 0.55 + Vector((0.12, 0, 0.12))), tuple(ct * 0.5 + sp * 0.25 + bp * 0.25), 30)],
        "S11": [(S["S11"][0], (2.3, -3.5, 0.8), (2.4, 0.0, 0.5), 35)],                      # Lumo, Piko, Tavi; Tavi dậm đất
        "S12": [(S["S12"][0], (2.55, -1.5, 0.8), tuple(LEAF_AT), 45),                       # theo mắt Tavi: cận lá…
                (tm.TAVI_LOOK_UP[0], (2.55, -1.5, 0.8), tuple(LEAF_AT), 45),
                (tm.TAVI_LOOK_UP[1], (2.55, -1.5, 0.8), tuple(HILLTOP + Vector((0, 0, -0.3))), 32)],   # …lia lên mây đỉnh đồi
        "S13": [(S["S13"][0], (1.95, -2.6, 0.72), (2.0, -0.1, 0.55), 38)],                  # Tavi "à!", giảng bằng tay
        "S14": [(S["S14"][0], (3.2, -5.4, 1.1), (4.6, 0.6, 1.15), 24)],                     # toàn: chỉ đỉnh đồi, cả nhóm ngước
    }
    end_t = offset + segment
    shots = [(n, a, b) for n, a, b in tm.SHOTS if a < end_t - 1e-6 and b > offset + 1e-6]
    cams = cameras(shots, {n: CAMS[n] for n, _, _ in shots})
    H, P = Vector((0, 0, 0.2)), Vector((0, 0, 0.4))
    must = {"S1": [(dew, Vector()), (leaf, Vector()), (flower_head, Vector())], "S2": [(piko_r.root, P), (flower_head, Vector())],
            "S3": [(lumo_r.head, H), (tavi_r.head, H), (piko_r.root, P)],
            "S4": [(lumo_r.head, H), (glow, Vector())], "S5": [(lumo_r.head, H), (tavi_r.head, H)],
            "S6": [(compass, Vector()), (piko_bag, Vector())], "S7": [(lumo_r.head, H), (piko_r.root, P)],
            "S8": [(piko_r.root, P)], "S9": [(piko_r.root, P)], "S10": [(spoon_ground, Vector())],
            "S11": [(lumo_r.head, H), (tavi_r.head, H), (piko_r.root, P)], "S13": [(tavi_r.head, H), (lumo_r.head, H)],
            "S14": [(lumo_r.head, H), (tavi_r.head, H), (piko_r.root, P), (N.root, Vector())]}
    extra = [("S3", N.root, f0 + 0.7, f1), ("S10", compass, tm.NEEDLE_TO_SPOON, S["S10"][1]),  # Lumo bước vào khung rồi mới cúi
             ("S12", leaf, S["S12"][0], tm.TAVI_LOOK_UP[0])]
    check_in_frame(shots, cams, must, extra)
    print("PREVIZ_POS thìa", tuple(round(v, 2) for v in sp), "la bàn kề thìa", tuple(round(v, 2) for v in ct),
          "túi Piko", tuple(round(v, 2) for v in bp))
    stills = [round((a + b) / 2, 2) for _, a, b in shots]
    stills += [t for t in (tm.SLURP, da0 + 0.5, ss1 + 0.5, tm.DIG[2] + 0.3, x1 - 0.1, gl + 1.0) if offset <= t < end_t]
    finish(out_blend, sorted(stills))
