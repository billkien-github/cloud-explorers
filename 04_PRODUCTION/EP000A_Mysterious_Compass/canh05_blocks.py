"""
Previz khối Cảnh 5 tập 000A (Tiếng gọi) dẫn Seedance (04_PRODUCTION/SEEDANCE.md): bối cảnh đỉnh đồi hoàng hôn, Lumo, la
bàn, bản đồ, chiếc lá, gió, chú chim dạng khối (pipeline/blocks.py), hòn đảo có Wonder Hub ở chân trời, máy quay từng cú.
Mọi mốc lấy từ timing.py của previz 2D (TIMING trong build_shot.py của đoạn), không gõ lại số. Diễn theo previz 2D đã
chốt: 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh05/.
Ba đoạn (Seedance 2.5, tối đa 30 giây) gọi build() với giây bắt đầu và độ dài của đoạn:
    sh120: 0–26.0 s của cảnh (S1–S7: la bàn chỉ qua ngọn đồi, leo lên đỉnh, đặt bản đồ, nâng la bàn, gió, mây tách,
           hòn đảo hiện ra, lóe lần 1, "Một nơi chưa ai khám phá…", "Được rồi, bạn la bàn.")
    sh130: 26.0–41.2 s (S8–S11: câu hô lần 3, lao đi, quên bản đồ, chạy ngược lại, "Nhà thám hiểm Lumo…", xoay bản đồ,
           nhún vai, cất bản đồ)
    sh140: 41.2–58.5 s (S12–S18: mép dốc lá khô, chiếc lá trượt, lối mòn, gật đầu, chú chim, la bàn, đi xuống lối
           mòn, lóe lần 2, khung đen)
Diễn dựng cho cả cảnh để các đoạn nối liền; khung 1 của đoạn = giây bắt đầu (blocks.T0), chỉ dựng máy quay của các cú
trong đoạn.
Toạ độ (m), theo previz 2D: trục X như previz 2D, máy quay phần lớn ở phía -Y nhìn về +Y (biển mây). Mặt đỉnh đồi Z 0;
chân đồi là bãi cỏ Z -1.0, sườn cỏ thoải lên đỉnh ở X -3.3; mép bên kia X 1.6, dốc lá khô (Y -0.6…3.6) xuống thảm cỏ
Z -0.9 ở X 4.0; lối mòn thoai thoải ở phía -Y của dốc lá (Y khoảng -1.3…-2.0), xuống tới thảm cỏ ở X 6.6. Tảng đá giữa
đỉnh ở (-0.62, 0.3), mặt trên ngang hông Lumo. Mặt đất là một lưới độ cao ground_z(x, y), check_in_frame dùng cùng hàm.
Hòn đảo ở chân trời theo hướng ISLAND_YAW (đông bắc), cách 150 m: cùng hai tầng mây che, mặt trời, dải mây chân trời là
con của SkyRig, node này bám vị trí máy quay đang dùng ở từng khung (key từng khung, LINEAR), nên vật ở rất xa không trôi
khi máy lia và mũi sao luôn chỉ đúng hướng hòn đảo. Biển mây là mặt phẳng đứng yên ở Z -4.5.
Các cú nhìn của Lumo (S1, S5 la bàn; S10 bản đồ; S13 dốc lá và lối mòn): máy ở chỗ mắt, đầu Lumo ẩn trong các cú này;
riêng S10 ẩn cả hai tay, hai bàn tay khối là con của bản đồ nên xoay theo bản đồ.
Màu: Lumo cam, chú chim nâu (mỗi nhân vật một màu, ô trắng = hướng mặt); bối cảnh, đạo cụ xám; la bàn vỏ vàng, mặt xanh
lam, đầu chỉ vàng sáng dài; chiếc lá vàng nhạt; ánh lóe của đài thiên văn xanh ngọc, của la bàn vàng.
"""
import math
import pathlib
import sys

import bmesh
import bpy
from bpy_extras import anim_utils
from mathutils import Matrix, Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.path.insert(0, str(ROOT / "pipeline"))
from blocks import *  # noqa: E402,F403  khối, vật liệu, nhân vật dạng khối, keyframe theo giây, máy quay

HOLD = 1 / 24                                                    # một khung: key ẩn và key hiện cách nhau ít hơn thì rơi vào cùng khung
PULSE = ((0.0, 0.25), (0.1, 1.25), (0.3, 0.95), (0.5, 1.12), (0.85, 0.0))   # một nhịp lóe của Wonder Hub (như previz 2D)

# ================================================================ địa hình (profile theo X của previz 2D)
EDGE, LOW, MEADOW = 1.6, -0.9, -1.0
HILL_L = [(-6.6, -1.0), (-6.3, -0.99), (-6.0, -0.95), (-5.7, -0.86), (-4.1, -0.17), (-3.8, -0.06), (-3.55, -0.01), (-3.3, 0.0)]
SLOPE = [(EDGE, 0.0), (1.68, -0.01), (1.78, -0.035), (1.9, -0.08), (2.05, -0.15), (3.5, -0.8), (3.65, -0.86), (3.8, -0.89),
         (4.0, LOW)]                                             # dốc lá khô thoải khoảng 24°, y như con dốc ở Cảnh 1
PATH = [(0.8, 0.0), (1.3, 0.0), (2.0, -0.05), (3.0, -0.2), (4.2, -0.42), (5.4, -0.66), (6.6, LOW)]   # lối mòn khoảng 11°
LEAF_Y = (-0.6, 3.6)                                             # bề ngang dốc lá khô
ROCK_C, ROCK_R, ROCK_TOP = Vector((-0.62, 0.3)), (0.46, 0.36), 0.265
MAP_SPOT = Vector((-0.74, 0.12, ROCK_TOP + 0.006))               # chỗ tấm bản đồ nằm trên tảng đá (mép phía máy)
POS_FOOT, POS_TOP = (-6.3, -1.0), (-3.3, -0.6)
POS_A = (-1.15, -0.25)                                           # đứng trước tảng đá, nhìn qua tảng đá ra hòn đảo
POS_B = (-0.12, 0.02)                                            # bên phải tảng đá (chạy ngược vào, chụp bản đồ)
POS_EDGE, POS_BACK = (1.52, -0.3), (1.3, -0.3)
LEAF_AT = Vector((1.74, 0.05))                                   # chiếc lá nằm ở mép dốc, trượt tới chân dốc
LEAF_END = Vector((4.25, 0.05))
ISLAND_YAW, ISLAND_R, ISLAND_S = 125.0, 150.0, 1.5              # hướng hòn đảo (yaw như nhân vật: 90 = +X, 180 = +Y)
SUN_YAW = 170.0


def ydir(yaw):
    """Vector đơn vị nằm ngang theo hướng yaw (0 = -Y, 90 = +X)."""
    a = math.radians(yaw)
    return Vector((math.sin(a), -math.cos(a), 0.0))


D_ISL = ydir(ISLAND_YAW)
R_ISL = Vector((D_ISL.y, -D_ISL.x, 0.0))                         # bên phải khi nhìn về hòn đảo


def line_z(pts, x):
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, z0), (x1, z1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


GROUND_LEAF = [(-16.0, MEADOW)] + HILL_L + SLOPE + [(16.0, LOW)]
GROUND_PATH = [(-16.0, MEADOW)] + HILL_L + PATH + [(16.0, LOW)]


def path_y(x):
    """Đường giữa lối mòn: tách khỏi đỉnh đồi ở X 0.6, men theo phía -Y của dốc lá."""
    if x <= 0.6:
        return -1.3
    if x <= 1.8:
        return -1.3 - 0.5 * (x - 0.6) / 1.2
    return -1.8 - 0.05 * (x - 1.8)


def ground_z(x, y):
    zl, zp = line_z(GROUND_LEAF, x), line_z(GROUND_PATH, x)
    w = ss((y + 1.45) / 0.85)                                    # Y -1.45…-0.6: bờ cỏ thoải nối vai đồi có lối mòn với dốc lá
    z = zp + (zl - zp) * w
    h = 1.0 if -4.5 <= y <= 3.5 else ss(1 - (-4.5 - y) / 2.5) if y < -4.5 else ss(1 - (y - 3.5) / 2.5)
    z = MEADOW + (z - MEADOW) * h                                # đồi thu về bãi cỏ ở hai bên theo Y
    dx, dy = max(0.0, -12.0 - x, x - 9.0), max(0.0, -11.0 - y, y - 6.5)
    return z - 6.0 * ss(math.hypot(dx, dy) / 4.0)               # mép hòn đảo nổi: chìm dưới biển mây


def tri_bm(w, h, th, center=(0, 0, 0), bm=None):
    """Tam giác dẹt (đầu mũi tên) nằm trong mặt XY, mũi chỉ về -Y, dày th."""
    bm = bm or bmesh.new()
    cx, cy, cz = center
    pts = [(cx - w / 2, cy + h / 2), (cx, cy - h / 2), (cx + w / 2, cy + h / 2)]
    a = [bm.verts.new((x, y, cz - th / 2)) for x, y in pts]
    b = [bm.verts.new((x, y, cz + th / 2)) for x, y in pts]
    bm.faces.new(list(reversed(a)))
    bm.faces.new(b)
    for i in range(3):
        bm.faces.new((a[i], a[(i + 1) % 3], b[(i + 1) % 3], b[i]))
    return bm


class GroundAct(Act):
    """Act của pipeline/blocks.py, Z mặc định bám mặt đất ground_z (đỉnh đồi, sườn dốc, lối mòn). Gọi theo thứ tự thời gian."""

    def go(self, t, x=None, y=None, hop=0.0, z=None):
        self.x = self.x if x is None else x
        self.y = self.y if y is None else y
        self.z = ground_z(self.x, self.y) + hop if z is None else z
        key(self.r.root, "location", t, Vector((self.x, self.y, self.z)))

    def walk(self, t0, t1, pts, hop=0.04):
        """Đi qua các điểm (x, y) đều nhau theo thời gian, nhún mỗi bước."""
        n = len(pts) - 1
        for i, (x, y) in enumerate(pts):
            self.go(t0 + (t1 - t0) * i / n, x, y, 0.0 if i in (0, n) else hop * (i % 2))


def fcurves(ob):
    """Các kênh keyframe của một object (action nhiều lớp của Blender 5.x); chưa có key thì trả về danh sách rỗng."""
    ad = ob.animation_data
    if not ad or not ad.action:
        return []
    return anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves


def set_linear(ob):
    for cv in fcurves(ob):
        for kp in cv.keyframe_points:
            kp.interpolation = "LINEAR"


def ease_gaps(obs, gap=0.6, lead=0.25):
    """Chống trôi giữa hai key thưa (như ease_gaps của pipeline/cutout.py): hai key cùng kênh cách nhau quá gap giây mà
    khác giá trị thì giữ giá trị cũ tới lead giây trước key sau, nên tư thế đứng yên rồi mới chuyển."""
    fps = bpy.context.scene.render.fps
    for ob in obs:
        for cv in fcurves(ob):
            pts = sorted((kp.co[0], kp.co[1]) for kp in cv.keyframe_points)
            for (f0, v0), (f1, v1) in zip(pts, pts[1:]):
                if f1 - f0 > gap * fps and abs(v1 - v0) > 1e-4:
                    cv.keyframe_points.insert(f1 - round(lead * fps), v0)
            cv.update()


def build(timing, offset, seconds, out_blend, segment=None):
    """seconds: độ dài video render (số nguyên giây Seedance nhận); segment: độ dài đoạn trong cảnh. Từ segment tới
    seconds chỉ giữ cú máy cuối (diễn vẫn chạy tiếp), lúc dựng cắt bỏ."""
    segment = seconds if segment is None else segment
    tm = load_timing(ROOT / timing)
    scene = start(tm.FPS, seconds, offset)
    T_END = tm.SECONDS
    S = {n: (a, b) for n, a, b in tm.SHOTS}
    end_t = offset + segment

    def in_seg(n):
        return offset - 1e-6 <= S[n][0] < end_t - 1e-6

    # ============================================================ vật liệu
    grass_m = material("M_Grass", (0.44, 0.45, 0.42), 0.9)
    litter_m = material("M_LeafLitter", (0.27, 0.25, 0.23), 0.95)
    path_m = material("M_Path", (0.62, 0.6, 0.56), 0.9)
    stone_m = material("M_Stone", (0.62, 0.61, 0.59), 0.8)
    bush_m = material("M_Bush", (0.31, 0.32, 0.3), 0.9)
    tuft_m = material("M_Tuft", (0.24, 0.26, 0.23), 0.9)
    sea_m = material("M_CloudSea", (0.88, 0.86, 0.9), 0.9, emit=((0.95, 0.9, 0.95), 0.5))
    bank_m = material("M_CloudBank", (0.92, 0.9, 0.93), 0.9, emit=((0.97, 0.93, 0.96), 0.6))
    sun_m = material("M_SunDisc", (1.0, 0.92, 0.7), 0.5, emit=((1.0, 0.9, 0.65), 3.0))
    isl_m = material("M_Island", (0.5, 0.49, 0.48), 0.9, emit=((0.6, 0.58, 0.62), 0.15))
    hill_m = material("M_IslandHill", (0.42, 0.43, 0.41), 0.9, emit=((0.5, 0.5, 0.52), 0.12))
    hub_m = material("M_HubBase", (0.84, 0.82, 0.78), 0.7, emit=((0.85, 0.83, 0.8), 0.2))
    dome_m = material("M_HubDome", (0.8, 0.78, 0.86), 0.5, emit=((0.82, 0.8, 0.88), 0.25))
    band_m = material("M_HubBand", (0.55, 0.47, 0.3), 0.5)
    window_m = material("M_HubWindow", (0.12, 0.12, 0.14), 0.5)
    teal_m = material("M_HubFlash", (0.2, 0.9, 0.8), 0.4, emit=((0.2, 0.9, 0.8), 1.25))   # sáng hơn 1.3 thì ra trắng (Standard)
    gold_m = material("M_CompassGold", (0.92, 0.62, 0.1), 0.35)
    face_m = material("M_CompassFace", (0.05, 0.2, 0.75), 0.3, emit=((0.25, 0.55, 1.0), 0.6))
    needle_m = material("M_CompassPointer", (1.0, 0.82, 0.2), 0.3, emit=((1.0, 0.8, 0.2), 0.5))
    arm_w_m = material("M_CompassStar", (0.9, 0.95, 1.0), 0.4)
    gem_m = material("M_CompassGem", (0.35, 0.85, 1.0), 0.2, emit=((0.35, 0.85, 1.0), 1.0))
    cflash_m = material("M_CompassFlash", (1.0, 0.78, 0.2), 0.4, emit=((1.0, 0.78, 0.2), 1.3))
    bright_m = material("M_CompassBright", (1.0, 0.95, 0.7), 0.4, emit=((1.0, 0.95, 0.7), 1.3))
    prop = material("M_Prop", (0.8, 0.8, 0.79), 0.6)
    prop_dark = material("M_PropDark", (0.12, 0.12, 0.13), 0.6)
    leaf_m = material("M_SlideLeaf", (1.0, 0.86, 0.35), 0.5)    # chiếc lá vàng sáng, nổi trên lớp lá sẫm
    wind_m = material("M_Wind", (0.55, 0.66, 0.85), 0.5)          # vệt gió xanh xám: trắng thì chìm vào biển mây
    bird_m = material("M_Bird_Brown", (0.32, 0.15, 0.06), 0.6)
    black_m = material("M_Black", (0.0, 0.0, 0.0), 1.0)
    bsdf_in(black_m, "Specular IOR Level").default_value = 0.0

    # ============================================================ mặt đất: lưới độ cao (cỏ, dốc lá, lối mòn)
    bm = bmesh.new()
    xs = [-16.0 + 0.1 * i for i in range(321)]
    ys = [-14.0 + 0.1 * j for j in range(221)]
    grid = [[bm.verts.new((x, y, ground_z(x, y))) for x in xs] for y in ys]
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            f = bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
            cx, cy = xs[i] + 0.05, ys[j] + 0.05
            if abs(cy - path_y(cx)) < 0.33 and 0.45 < cx < 6.9:
                f.material_index = 2
            elif EDGE + 0.02 < cx < 4.05 and LEAF_Y[0] < cy < LEAF_Y[1]:
                f.material_index = 1
            f.smooth = True
    ground = add_obj("Ground", bm, grass_m, "SET")
    ground.data.materials.append(litter_m)
    ground.data.materials.append(path_m)
    bm = bmesh.new()                                             # lá khô rải trên dốc (vân lá cho dễ đọc là lớp lá)
    for k in range(140):
        u, v = ((k * 0.618034) % 1.0), ((k * 0.381966 + 0.13 * (k % 7)) % 1.0)
        lx, ly = EDGE + 0.08 + u * (4.1 - EDGE - 0.08), LEAF_Y[0] + 0.1 + v * (LEAF_Y[1] - LEAF_Y[0] - 0.2)
        res = bmesh.ops.create_cube(bm, size=1.0)
        a = k * 2.4
        dz = (ground_z(lx + 0.05, ly) - ground_z(lx - 0.05, ly)) / 0.1
        for vv in res["verts"]:
            x, y, z = vv.co.x * 0.12, vv.co.y * 0.07, vv.co.z * 0.012
            x, y = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
            vv.co = Vector((lx + x, ly + y, ground_z(lx, ly) + 0.01 + z + dz * x))
    add_obj("SlopeLeafBits", bm, material("M_LeafBits", (0.38, 0.35, 0.31), 0.9), "SET")
    add_obj("CloudSea", box_bm((700.0, 700.0, 0.1), (0, 0, -4.5)), sea_m, "SET")
    bm = None
    for i in range(40):                                          # gợn mây gần trên biển mây (đứng yên)
        a = math.radians(i * 9.0)
        r = 22.0 + 9.0 * (i % 3)
        bm = sphere_bm(5.0 + 2.0 * (i % 2), (r * math.sin(a), -r * math.cos(a) + 2.0, -4.6), (1.6, 1.0, 0.25), bm=bm, segs=12)
    add_obj("CloudSea_Puffs", bm, sea_m, "SET")
    # tảng đá phẳng giữa đỉnh đồi, mặt trên ngang hông Lumo (sunset_hill_hero.png)
    rock = add_obj("Rock", cyl_bm(1.0, ROCK_TOP, (0, 0, ROCK_TOP / 2 - 0.02), segs=24), stone_m, "SET",
                   loc=(ROCK_C.x, ROCK_C.y, 0.0))
    rock.scale = (ROCK_R[0], ROCK_R[1], 1.0)
    rock.rotation_euler = (0, 0, math.radians(15))
    bm = None
    for cx, cy, r in ((-1.25, 0.55, 0.12), (0.05, 0.45, 0.09), (-0.35, 0.75, 0.07)):
        bm = sphere_bm(r, (cx, cy, 0.0), (1.2, 1.0, 0.7), bm=bm, segs=12)
    add_obj("Pebbles", bm, stone_m, "SET")
    bm = None
    for cx, cy, r in ((-7.4, -0.2, 0.35), (-7.1, -1.9, 0.28), (4.9, 2.6, 0.4), (6.2, 1.4, 0.3), (2.6, 4.0, 0.35), (-2.4, 3.4, 0.3)):
        bm = sphere_bm(r, (cx, cy, ground_z(cx, cy) + 0.15), (1.2, 1.0, 0.75), bm=bm, segs=14)
    add_obj("Bushes", bm, bush_m, "SET")
    tufts = []                                                   # cỏ quanh tảng đá rạp xuống khi gió thổi tạt
    for k, (gx, gy) in enumerate(((-1.6, -0.6), (-1.0, -0.75), (-0.2, -0.45), (0.3, -0.2), (-1.45, 0.25), (0.15, 0.75))):
        pv = empty(f"Tuft{k}", "SET", loc=(gx, gy, 0.0))
        bm = sphere_bm(0.05, (0, 0, 0.06), (0.7, 0.7, 1.4), segs=10)            # búi cỏ tròn (nón nhọn trông như gai)
        bm = sphere_bm(0.04, (0.05, 0.02, 0.045), (0.7, 0.7, 1.3), bm=bm, segs=10)
        add_obj(f"Tuft{k}_Blades", bm, tuft_m, "SET", parent=pv)
        tufts.append(pv)
    # khung đen cuối cảnh: hộp đen kín ở xa, máy S18 nằm trong hộp
    black = add_obj("BlackBox", box_bm((6.0, 6.0, 6.0)), black_m, "SET", loc=(90.0, 0.0, 5.0))
    key(black, "scale", -1.0, Vector((0, 0, 0)))                 # chỉ hiện ở S18: hộp đen lộ thành ô vuông đen ở chân trời
    key(black, "scale", S["S18"][0] - HOLD, Vector((0, 0, 0)))
    key(black, "scale", S["S18"][0], Vector((1, 1, 1)))

    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    COLS["SET"].objects.link(sun)
    sun.data.energy, sun.data.angle = 2.4, math.radians(4)
    sun.rotation_euler = (math.radians(32), 0, math.radians(25))    # cao, từ phía nam (phía máy quay): khối, dốc lá, bờ cỏ đều sáng
    fill = bpy.data.objects.new("Fill", bpy.data.lights.new("Fill", "SUN"))   # đèn phụ từ phía bắc, không bóng: bờ cỏ giữa
    COLS["SET"].objects.link(fill)                                         # lối mòn và dốc lá khuất nắng thì trông như rãnh sâu
    fill.data.energy, fill.data.use_shadow = 0.8, False
    fill.rotation_euler = (math.radians(-50), 0, math.radians(-20))
    world = bpy.data.worlds.new("Sky")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.66, 0.58, 0.8, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.85

    # ============================================================ trời xa: hòn đảo, hai tầng mây che, mặt trời, dải mây
    sky = empty("SkyRig", "SET")                                 # bám vị trí máy quay từng khung (key ở cuối build)
    isl = empty("Island", "SET", parent=sky, loc=D_ISL * ISLAND_R + Vector((0, 0, -3.0)))
    isl.rotation_euler = (0, 0, math.radians(ISLAND_YAW + 180))   # mặt trước (-Y cục bộ) quay về phía máy, +X cục bộ là bên phải
    isl.scale = (ISLAND_S,) * 3
    bm = cyl_bm(0.0, 12.0, (0, 0, -6.5), cone_top=16.0, segs=16)  # đảo nổi: nón chúc xuống
    bm = sphere_bm(16.0, (0, 0, -0.5), (1.0, 0.8, 0.12), bm=bm, segs=16)
    add_obj("Island_Base", bm, isl_m, "SET", parent=isl)
    add_obj("Island_Hill", sphere_bm(11.0, (4.0, 4.0, 0.0), (1.0, 0.9, 1.55), segs=20), hill_m, "SET", parent=isl)
    HUB = Vector((-5.0, -4.0, 0.0))                              # đài thiên văn ở chân đồi, phía trước bên trái
    add_obj("Hub_Base", cyl_bm(6.0, 3.4, HUB + Vector((0, 0, 1.7)), segs=24), hub_m, "SET", parent=isl)
    add_obj("Hub_Wing", box_bm((5.0, 4.0, 2.4), HUB + Vector((7.5, 0.5, 1.2))), hub_m, "SET", parent=isl)
    add_obj("Hub_Dome", sphere_bm(5.2, HUB + Vector((0, 0, 3.4)), segs=24), dome_m, "SET", parent=isl)
    add_obj("Hub_Band", cyl_bm(5.45, 0.7, HUB + Vector((0, 0, 3.75)), segs=24), band_m, "SET", parent=isl)
    win = add_obj("Hub_Window", cyl_bm(1.5, 0.4, axis="Y", segs=20), window_m, "SET", parent=isl,
                  loc=HUB + Vector((0, -5.2 * math.cos(math.radians(32)), 3.4 + 5.2 * math.sin(math.radians(32)))))
    win.rotation_euler = (math.radians(32), 0, 0)
    bm = None
    for cx, cy, cz, r in ((-12.0, -6.0, 0.2, 4.0), (10.0, -7.0, 0.0, 3.5), (-1.0, -9.0, -0.4, 3.0), (15.0, 2.0, 0.3, 3.5)):
        bm = sphere_bm(r, (cx, cy, cz), (1.8, 1.0, 0.45), bm=bm, segs=12)
    add_obj("Island_Mist", bm, bank_m, "SET", parent=isl)
    hub_flash = add_obj("Hub_Flash", sphere_bm(9.0, segs=24), teal_m, "SET", parent=isl, loc=HUB + Vector((0, 0, 4.0)))
    hub_tint = add_obj("Hub_FlashDome", sphere_bm(5.5, segs=24), teal_m, "SET", parent=isl, loc=HUB + Vector((0, 0, 3.4)))
    banks = []                                                   # hai tầng mây che hòn đảo, tách ra hai bên ở CLOUD_PART
    for side in (-1, 1):
        root = empty(f"CloudBank{'L' if side < 0 else 'R'}", "SET", parent=sky, loc=D_ISL * 115.0 + R_ISL * (side * 9.0))
        bm = None
        for k, (u, z, r) in enumerate(((0.0, 1.0, 13.0), (side * 9.0, 4.0, 11.0), (-side * 7.0, 9.0, 10.0), (side * 3.0, 15.0, 9.0),
                                       (-side * 2.0, 20.0, 7.0), (side * 12.0, 10.0, 8.0))):
            c = R_ISL * u + Vector((0, 0, z - 4.0))
            bm = sphere_bm(r, tuple(c), (1.25, 1.0, 0.85), bm=bm, segs=16)
        add_obj(f"CloudBank{'L' if side < 0 else 'R'}_Shape", bm, bank_m, "SET", parent=root)
        banks.append((root, side))
    bm = None
    for i in range(72):                                          # dải mây dày ở chân trời, quanh cả vòng
        a = math.radians(i * 5.0)
        bm = sphere_bm(22.0, (230.0 * math.sin(a), -230.0 * math.cos(a), -7.0 - 2.0 * (i % 2)), (1.0, 0.6, 0.38), bm=bm, segs=10)
    add_obj("HorizonClouds", bm, bank_m, "SET", parent=sky)
    add_obj("SunDisc", sphere_bm(10.0, segs=16), sun_m, "SET", parent=sky, loc=ydir(SUN_YAW) * 260.0 + Vector((0, 0, 6.0)))
    for ob in (hub_flash, hub_tint):
        key(ob, "scale", -1.0, Vector((0, 0, 0)))

    # ============================================================ Lumo, áo choàng, túi, dây túi
    L = build_lumo((POS_FOOT[0], POS_FOOT[1], ground_z(*POS_FOOT)))
    lumo = GroundAct(L, *POS_FOOT, 95)
    lm = cast_materials()["lumo"]
    cape = empty("Lumo_CapePivot", "CAST", parent=L.root, loc=(0, 0.15, 0.57))
    add_obj("Lumo_Cape", box_bm((0.3, 0.025, 0.27), (0, 0.012, -0.135)), lm, "CAST", parent=cape)
    bag = add_obj("Lumo_Bag", box_bm((0.1, 0.06, 0.09)), prop_dark, "CAST", parent=L.root, loc=(-0.2, -0.12, 0.3))
    p0s, p1s = Vector((-0.17, -0.165, 0.34)), Vector((0.13, -0.165, 0.58))   # dây túi chéo trước ngực, từ túi lên vai trái
    strap = add_obj("Lumo_Strap", cyl_bm(0.012, (p1s - p0s).length, segs=8), prop_dark, "CAST", parent=L.root, loc=(p0s + p1s) / 2)
    strap.rotation_mode = "QUATERNION"
    strap.rotation_quaternion = (p1s - p0s).to_track_quat("Z", "Y")
    bag_glow = add_obj("Lumo_BagGlow", box_bm((0.14, 0.09, 0.03), (0, 0, 0.055)), cflash_m, "CAST", parent=bag)
    key(bag_glow, "scale", -1.0, Vector((0, 0, 0)))              # ánh la bàn lọt qua mép nắp túi da (lóe lần 2)
    BAG = Vector((-0.2, -0.16, 0.3))
    BAG_TOP = BAG + Vector((0, -0.03, 0.1))                      # miệng túi: vật ló ra, chui vào ở đây, túi giữ nguyên

    def head(t, pitch=0.0, yaw=0.0, roll=0.0):
        rot(L.head, [(t, (pitch, roll, yaw))])

    def ears(t, a):
        for ear, _ in L.ears:
            rot(ear, [(t, (a, 0, 0))])

    def arms(t, r=None, l=None):
        """r, l: (x, y, z) độ hoặc một số (chỉ xoay X). Bỏ trống là để yên tay đó."""
        for arm, a in ((L.arm_r, r), (L.arm_l, l)):
            if a is None:
                continue
            a = (a, 0, 0) if isinstance(a, (int, float)) else a
            rot(arm, [(t, a)])

    def tail(t, up, side=0.0):
        rot(L.tail, [(t, (up, 0, side))])

    def capef(t, a):
        rot(cape, [(t, (a, 0, 0))])

    def squash(t, sx, sz):
        key(L.root, "scale", t, Vector((sx, sx, sz)))

    def show(ob, t, on, s=1.0):
        key(ob, "scale", t - HOLD, Vector((s, s, s)) if not on else Vector((0, 0, 0)))
        key(ob, "scale", t, Vector((s, s, s)) if on else Vector((0, 0, 0)))

    def pulse(ob, t, size=1.0):
        """Một nhịp lóe: hiện, co giãn theo PULSE, tắt."""
        key(ob, "scale", t - HOLD, Vector((0, 0, 0)))
        for dt, s in PULSE:
            key(ob, "scale", t + dt, Vector((s * size,) * 3))

    # ============================================================ la bàn (Wonder Compass) khối, to hơn cỡ thật một chút
    CR, CT = 0.085, 0.035                                        # bán kính vỏ, bề dày
    comp_hold = empty("Lumo_CompassHold", "PROPS", parent=L.root)
    comp = empty("Compass", "PROPS", parent=comp_hold)           # mặt kính là +Z cục bộ; mép xa (khoen, 0° của mũi sao) là -Y
    add_obj("Compass_Case", cyl_bm(CR, CT, segs=28), gold_m, "PROPS", parent=comp)
    add_obj("Compass_Ring", cyl_bm(0.022, 0.012, (0, -CR - 0.024, 0), axis="X", segs=14), gold_m, "PROPS", parent=comp)
    add_obj("Compass_Knob", box_bm((0.028, 0.02, 0.02), (0, -CR - 0.004, 0)), gold_m, "PROPS", parent=comp)
    add_obj("Compass_Face", cyl_bm(CR * 0.8, 0.004, (0, 0, CT / 2 + 0.001), segs=28), face_m, "PROPS", parent=comp)
    needle = empty("Compass_Needle", "PROPS", parent=comp, loc=(0, 0, CT / 2 + 0.006))
    bm = box_bm((0.016, 0.05, 0.006), (0, -0.025, 0))            # đầu chỉ: cánh vàng dài, đầu có viên đá xanh
    bm = tri_bm(0.026, 0.024, 0.006, (0, -0.06, 0), bm=bm)
    add_obj("Compass_Pointer", bm, needle_m, "PROPS", parent=needle)
    add_obj("Compass_PointerGem", sphere_bm(0.009, (0, -0.074, 0.002), segs=10), gem_m, "PROPS", parent=needle)
    bm = bmesh.new()
    for j in range(1, 8):                                        # bảy cánh ngắn trắng xanh
        a = math.radians(45 * j)
        res = bmesh.ops.create_cube(bm, size=1.0)
        for v in res["verts"]:
            x, y, z = v.co.x * 0.009, v.co.y * 0.034 - 0.017, v.co.z * 0.004
            v.co = Vector((x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a), z))
    bm = sphere_bm(0.012, (0, 0, 0.002), bm=bm, segs=10)
    add_obj("Compass_Star", bm, arm_w_m, "PROPS", parent=needle)
    comp_flash = add_obj("Compass_Flash", sphere_bm(0.15, segs=20), cflash_m, "PROPS", parent=comp, loc=(0, 0, -0.01))
    comp_bright = add_obj("Compass_Bright", cyl_bm(CR * 0.82, 0.006, (0, 0, CT / 2 + 0.003), segs=28), bright_m, "PROPS", parent=comp)
    for ob in (comp_flash, comp_bright):
        key(ob, "scale", -1.0, Vector((0, 0, 0)))
    tw = bsdf_in(face_m, "Emission Strength")                    # le lói: mặt kính sáng lên tắt xuống nhẹ suốt cảnh
    t, i = 0.0, 0
    while t <= T_END:
        tw.default_value = 0.9 if i % 2 else 0.3
        tw.keyframe_insert("default_value", frame=fr(t))
        t, i = t + 0.35, i + 1

    # tư thế cầm la bàn: (vị trí, góc của vỏ, tay phải, tay trái); vỏ nghiêng ngửa về phía mắt Lumo
    C_UP = ((-0.06, -0.36, 0.62), (-50, 0, 0), (-102, 0, 18), None)       # tay phải giơ la bàn trước mặt (S1)
    C_BELLY = ((-0.12, -0.3, 0.38), (-30, 0, 0), (-42, 0, 10), None)    # tay phải hạ la bàn ngang bụng
    C_CHEST = ((0.0, -0.34, 0.5), (-45, 0, 0), (-82, 0, 18), (-82, 0, -18))   # hai tay nâng ngang ngực
    C_ONE = ((-0.05, -0.36, 0.5), (-50, 0, 0), (-84, 0, 12), (6, 0, 0))     # một tay chìa thẳng ra trước, tay kia buông
    C_PUSH = ((-0.05, -0.4, 0.51), (-60, 0, 0), (-93, 0, 12), (6, 0, 0))    # đẩy tới ở "ngay phía trước"
    C_LOOK = ((-0.06, -0.33, 0.48), (-40, 0, 0), (-80, 0, 12), None)        # một tay, nhìn mũi sao (S16)

    def chold(t, pose, s=1.0):
        loc, r, ar, al = pose
        key(comp_hold, "location", t, Vector(loc))
        rot(comp_hold, [(t, r)])
        key(comp_hold, "scale", t, Vector((s, s, s)))
        arms(t, ar, al)

    # ============================================================ bản đồ giấy: chi tiết sẫm chỉ ở mặt trước
    def map_shapes(parent, tag):
        """Bản đồ to cỡ đầu Lumo. Mặt trước là +Z; đứng thẳng (ANG 0) rương ở mép -Y (mép xa người cầm, phía trên khi Lumo
        nhìn xuống), mũi tên chỉ về rương. Mũi tên, rương nằm trọn trên mặt trước: ló ra mặt sau thì ở cú nhìn lưng bản
        đồ thành vệt sẫm, Seedance vẽ thành tấm thẻ."""
        add_obj(f"Map{tag}_Sheet", box_bm((0.36, 0.3, 0.008)), prop, "PROPS", parent=parent)
        bm = box_bm((0.04, 0.08, 0.006), (0, 0.04, 0.007))      # thân mũi tên
        bm = tri_bm(0.1, 0.07, 0.006, (0, -0.035, 0.007), bm=bm)  # đầu mũi tên chỉ về -Y
        bm = box_bm((0.09, 0.05, 0.008), (0, -0.105, 0.008), bm=bm)   # rương
        bm = cyl_bm(0.024, 0.09, (0, -0.105, 0.016), axis="X", bm=bm, segs=12)   # nắp vòm (trên mặt giấy)
        for v in bm.verts:
            v.co.z = max(v.co.z, 0.0045)                         # không gì ló ra mặt sau tấm giấy
        add_obj(f"Map{tag}_Marks", bm, prop_dark, "PROPS", parent=parent)

    map_hold = empty("Lumo_MapHold", "PROPS", parent=L.root)
    map_spin = empty("Lumo_MapSpin", "PROPS", parent=map_hold)   # quay quanh pháp tuyến (xoay trong mặt phẳng tấm giấy)
    map_shapes(map_spin, "")
    map_rock = empty("MapOnRock", "PROPS", loc=MAP_SPOT)
    map_rock.rotation_euler = (0, 0, math.radians(yaw_to(POS_A, MAP_SPOT)))
    map_shapes(map_rock, "Rock")
    paws = [add_obj(f"Lumo_MapPaw{s:+d}", box_bm((0.07, 0.07, 0.05), (s * 0.19, 0.05, -0.012)), lm, "CAST",
                    parent=map_spin) for s in (-1, 1)]             # bàn tay ở cú nhìn S10: con của bản đồ, xoay theo bản đồ
    for ob in paws:
        key(ob, "scale", -1.0, Vector((0, 0, 0)))
    key(map_rock, "scale", -1.0, Vector((0, 0, 0)))
    M_SMALL = ((0.2, -0.13, 0.27), (-80, 0, 0), 0.5)               # gấp nhỏ trong tay trái, thõng bên hông
    M_CHEST = ((0.0, -0.3, 0.4), (-45, 0, 0), 1.0)                 # trước ngực, thấp hơn cằm: không che mặt
    M_READ = ((0.0, -0.3, 0.45), (-50, 0, 0), 1.0)                # mở ra trước ngực, nhìn xuống

    def mhold(t, pose, s=None):
        loc, r, sc = pose
        key(map_hold, "location", t, Vector(loc))
        rot(map_hold, [(t, r)])
        sc = sc if s is None else s
        key(map_hold, "scale", t, Vector((sc, sc, sc)))

    def mspin(t, deg):
        rot(map_spin, [(t, (0, 0, deg))])

    # ============================================================ chiếc lá trượt, gió
    slide_leaf = add_obj("SlideLeaf", sphere_bm(0.12, scale=(1.0, 0.55, 0.12), segs=14), leaf_m, "PROPS")   # to hơn cỡ thật cho đọc được
    streaks = [add_obj(f"Wind{i}", box_bm((0.02, 0.7, 0.02)), wind_m, "PROPS") for i in range(8)]
    gust_leaves = [add_obj(f"GustLeaf{i}", box_bm((0.08, 0.05, 0.01)), litter_m, "PROPS") for i in range(4)]
    for ob in (*streaks, *gust_leaves):
        key(ob, "scale", -1.0, Vector((0, 0, 0)))

    # ============================================================ chú chim nhỏ cỡ nắm tay Lumo (như Cảnh 1)
    BIRD_AT = Vector((-0.5, 0.38, ROCK_TOP - 0.005))
    B = Rig()
    B.root = empty("BIRD", "CAST", loc=BIRD_AT)
    add_obj("Bird_Body", sphere_bm(0.042, (0, 0, 0.045), (1.0, 1.1, 0.95)), bird_m, "CAST", parent=B.root)
    B.neck = empty("Bird_Neck", "CAST", parent=B.root, loc=(0, -0.01, 0.095))
    B.head = add_obj("Bird_Head", sphere_bm(0.032, (0, 0, 0.0)), bird_m, "CAST", parent=B.neck)
    face_marker("Bird_Face", B.head, 0.03, 0.02, -0.03, 0.0)
    add_obj("Bird_Tuft", box_bm((0.012, 0.025, 0.03), (0, 0.01, 0.04)), bird_m, "CAST", parent=B.head)
    add_obj("Bird_Tail", box_bm((0.02, 0.05, 0.04), (0, 0.06, 0.07)), bird_m, "CAST", parent=B.root)
    B.wing = add_obj("Bird_Wing", box_bm((0.012, 0.05, 0.03), (0, 0.015, -0.02)), bird_m, "CAST", parent=B.root,
                     loc=(-0.045, 0.0, 0.065))
    B.wing_far = add_obj("Bird_WingFar", box_bm((0.012, 0.05, 0.03), (0, 0.015, -0.02)), bird_m, "CAST", parent=B.root,
                         loc=(0.045, 0.0, 0.065))

    # ============================================================ S1–S3: la bàn chỉ qua ngọn đồi, leo lên đỉnh
    lumo.go(0.0, *POS_FOOT)
    lumo.pose(0.0, lean=0, yaw=95)
    squash(0.0, 1, 1)
    head(0.0, 14)
    ears(0.0, 4)
    tail(0.0, 25)
    capef(0.0, 0)
    chold(0.0, C_UP)
    mhold(0.0, M_SMALL)
    arms(0.0, l=(-20, 0, 0))
    key(L.head, "scale", 0.0, Vector((1, 1, 1)))
    key(L.arm_r, "scale", 0.0, Vector((1, 1, 1)))
    key(L.arm_l, "scale", 0.0, Vector((1, 1, 1)))
    wag(L.tail, 0.0, tm.CLIMB[0], 0.7, 12, base=(25, 0, 0))
    c0, c1 = tm.COMPASS_LOWER
    chold(c0, C_UP)
    chold(c1, C_BELLY)                                           # hạ la bàn xuống ngang bụng
    head(c1, 4)
    h0, h1 = tm.LOOK_HILL
    head(h0, 4)
    head(h0 + 0.2, -16)                                          # ngẩng nhìn đỉnh đồi, dựng tai
    head(h1, -12)
    ears(h0, 4)
    ears(h0 + 0.15, 18)
    ears(h1, 8)
    squash(h0, 1, 1)
    squash(h0 + 0.15, 1.04, 0.95)
    squash(h1, 1, 1)
    k0, k1 = tm.CLIMB                                            # leo lên sườn cỏ thoải, mắt nhìn phía trước
    pts = [(POS_FOOT[0] + (POS_TOP[0] - POS_FOOT[0]) * i / 8, POS_FOOT[1] + (POS_TOP[1] - POS_FOOT[1]) * i / 8) for i in range(9)]
    lumo.walk(k0, k1, pts, 0.05)
    steps(L.legs, k0, k1, 8, 30)
    lumo.pose(k0, lean=0, yaw=98)
    lumo.pose(k0 + 0.2, lean=10)                                 # chồm lên dốc
    lumo.pose(k1 - 0.1, lean=10)
    lumo.pose(k1 + 0.15, lean=0)
    head(k0, -10)
    head(k0 + 0.2, -4)
    wag(L.arm_l, k0, k1, 0.25, 22, base=(-20, 0, 0), axis=0)      # tay trái đánh theo bước, bản đồ gấp vẫn trong tay
    wag(L.tail, k0, tm.TOP_WALK[1], 0.4, 14, base=(32, 0, 0))
    w0, w1 = tm.TOP_WALK                                         # lên tới đỉnh, đi tới trước tảng đá
    pts = [(POS_TOP[0] + (POS_A[0] - POS_TOP[0]) * i / 8, POS_TOP[1] + (POS_A[1] - POS_TOP[1]) * i / 8) for i in range(9)]
    lumo.walk(w0, w1, pts, 0.035)
    steps(L.legs, w0, w1, 8, 22)
    lumo.pose(w1 - 0.6, yaw=99)
    lumo.pose(w1, yaw=120)                                       # quay về phía tảng đá, biển mây
    head(w0 + 0.1, 0)
    arms(w1, l=(-20, 0, 0))
    v0, v1 = tm.VIEW_LOOK                                        # dừng lại, nhìn ra biển mây
    head(v0, 0)
    head(v0 + 0.3, -10)
    ears(v0, 6)
    ears(v0 + 0.15, 18)
    ears(v0 + 0.35, 8)
    lumo.pose(v0, lean=0)
    lumo.pose(v0 + 0.3, lean=-4)
    head(v1, -10)
    wag(L.tail, w1, tm.MAP_DOWN[0], 0.6, 14, base=(28, 0, 0))

    # ============================================================ S4: đặt bản đồ lên tảng đá, hai tay nâng la bàn
    m0, m1 = tm.MAP_DOWN
    PUT_LEAN = 22
    lumo.pose(m0, lean=-4)
    lumo.pose(m0 + 0.3, lean=PUT_LEAN)
    head(m0, -10)
    head(m0 + 0.3, 26)                                           # nhìn chỗ đặt
    mhold(m0, M_SMALL)
    arms(m0, l=(-20, 0, 0))
    arms(m0 + 0.3, l=(-62, 0, -12))
    # lúc buông tay tấm bản đồ (đã mở) phải nằm đúng chỗ tấm bản đồ trên tảng đá: tính vị trí trong hệ của Lumo
    rel_t = m0 + 0.35
    scene.frame_set(fr(rel_t))
    w_map = Matrix.Translation(MAP_SPOT) @ map_rock.rotation_euler.to_matrix().to_4x4()
    loc_m = L.root.matrix_world.inverted() @ w_map
    pl, pr, _ = loc_m.decompose()
    key(map_hold, "location", rel_t - HOLD, pl)
    rot(map_hold, [(rel_t - HOLD, tuple(math.degrees(a) for a in pr.to_euler("XYZ")))])
    key(map_hold, "scale", rel_t - HOLD, Vector((1, 1, 1)))
    key(map_hold, "scale", rel_t, Vector((0, 0, 0)))             # buông tay: bản đồ nằm lại trên tảng đá
    show(map_rock, rel_t, True)
    lumo.pose(m1, lean=0)
    head(m1, 4)
    arms(m1, l=(-10, 0, 0))
    u0, u1 = tm.COMPASS_UP
    chold(u0, C_BELLY)
    arms(u0, l=(-10, 0, 0))
    chold(u1, C_CHEST)                                           # hai tay nâng la bàn ngang ngực
    head(u0 + 0.1, 24)
    head(u1, 18)
    ears(u0, 6)
    ears(u1, 14)
    head(tm.LOOK_HORIZON - 0.15, 18)
    head(tm.LOOK_HORIZON + 0.15, -4, 5)                          # nhìn theo mũi sao ra chân trời: chỉ có mây
    tail(u1, 30)

    # ============================================================ S6: gió thổi tạt, mây tách, hòn đảo dần hiện, lóe lần 1
    g0, g1 = tm.GUST
    A3 = Vector((POS_A[0], POS_A[1], 0.0))
    for i, ob in enumerate(streaks[:7]):                         # vệt gió lướt từ phía chân trời về phía Lumo
        ts = g0 + 0.18 * i
        side = (-1) ** i * (0.35 + 0.18 * (i % 3))
        z = 0.3 + 0.17 * ((i * 3) % 7)
        p0v = A3 + D_ISL * 3.2 + R_ISL * side + Vector((0, 0, z))
        p1v = A3 - D_ISL * 2.0 + R_ISL * side + Vector((0, 0, z + 0.06))
        rot(ob, [(ts, (0, 0, ISLAND_YAW))])
        key(ob, "location", ts, p0v)
        key(ob, "location", ts + 0.55, p1v)
        show(ob, ts, True)
        show(ob, ts + 0.56, False)
    for i, ob in enumerate(gust_leaves):
        ts = g0 + 0.25 + 0.3 * i
        side = (-1) ** i * (0.3 + 0.15 * i)
        show(ob, ts, True)
        for q in range(5):
            u = q / 4
            p = A3 + D_ISL * (2.6 - 4.6 * u) + R_ISL * side + Vector((0, 0, 0.5 + 0.12 * i + 0.25 * math.sin(math.pi * u)))
            key(ob, "location", ts + 0.9 * u, p)
            rot(ob, [(ts + 0.9 * u, (540 * u, 200 * u, 90 * u))])
        show(ob, ts + 0.92, False)
    for k, pv in enumerate(tufts):                               # cỏ rạp theo gió (ngả ra xa hòn đảo)
        rot(pv, [(g0 + 0.05 * k, (0, 0, ISLAND_YAW))])
        wag(pv, g0 + 0.15 + 0.03 * k, g1 - 0.1, 0.22, 10, base=(-28, 0, ISLAND_YAW), axis=0)
        rot(pv, [(g1 + 0.1, (0, 0, ISLAND_YAW))])
    MR_YAW = math.degrees(map_rock.rotation_euler.z)
    rot(map_rock, [(g0, (0, 0, MR_YAW))])
    for k in range(int((g1 - g0 - 0.3) / 0.12)):                 # mép bản đồ trên tảng đá phập phồng
        rot(map_rock, [(g0 + 0.1 + 0.12 * k, (5 if k % 2 else -3, 0, MR_YAW))])
    rot(map_rock, [(g1, (0, 0, MR_YAW))])
    head(g0, 18)
    head(g0 + 0.2, 10)                                           # nheo mắt, cúi đầu vào gió
    for ear, _ in L.ears:                                        # tai bị gió thổi ngả ra sau
        wag(ear, g0 + 0.05, g1 - 0.1, 0.16, 8, base=(-36, 0, 0), axis=0)
    ears(g1 + 0.05, 4)
    capef(g0, 0)
    wag(cape, g0 + 0.05, g1, 0.14, 10, base=(42, 0, 0), axis=0)   # áo choàng bay ngược ra sau
    capef(g1 + 0.2, 0)
    wag(L.tail, g0, g1, 0.14, 12, base=(55, 0, 0))
    lumo.pose(g0, lean=0)
    lumo.pose(g0 + 0.2, lean=6, yaw=110)                         # chồm vào gió; người xoay nhẹ về phía máy, mắt vẫn về hòn đảo
    p0, p1 = tm.CLOUD_PART                                       # hai tầng mây tách ra hai bên, hòn đảo hiện dần
    for root, side in banks:
        base = root.location.copy()
        key(root, "location", p0, base)
        key(root, "location", p0 + (p1 - p0) * 0.4, base + R_ISL * (side * 12.0) + Vector((0, 0, -1.0)))
        key(root, "location", p1, base + R_ISL * (side * 46.0) + Vector((0, 0, -4.0)))
    l0, l1 = tm.LUMO_LEAN
    head(l0, 10)
    head(l1, -6, 15)                                             # mở mắt, chồm tới nhìn hòn đảo
    lumo.pose(g1, lean=6)
    lumo.pose(l1, lean=10)
    ears(l0, 4)
    ears(l1, 14)
    wag(L.tail, g1 + 0.1, tm.LUMO_LINE1[0], 0.6, 12, base=(30, 0, 0))
    pulse(hub_flash, tm.HUB_FLASH1, 1.0)                         # đài thiên văn lóe xanh ngọc
    show(hub_tint, tm.HUB_FLASH1, True)
    show(hub_tint, tm.HUB_FLASH1 + 0.7, False)
    pulse(comp_flash, tm.HUB_FLASH1, 1.0)                        # đúng nhịp đó la bàn lóe theo (chỉ lóe, không rung)
    show(comp_bright, tm.HUB_FLASH1, True)
    show(comp_bright, tm.HUB_FLASH1 + 0.7, False)
    r0, r1 = tm.LUMO_REACT
    ears(r0, 14)
    ears(r0 + 0.12, 30)                                          # tai bật dựng
    ears(r1, 12)
    squash(r0, 1, 1)
    squash(r0 + 0.12, 0.96, 1.05)
    squash(r1, 1, 1)
    head(r0, -6, 15)
    head(r0 + 0.3, 24, 0)                                        # liếc xuống la bàn vừa lóe
    head(r1 + 0.1, 24, 0)
    head(r1 + 0.4, -6, 15)                                       # rồi lại nhìn hòn đảo
    lumo.pose(r1, lean=6)

    # ============================================================ S7: "Một nơi chưa ai khám phá…", "Được rồi, bạn la bàn."
    a0, a1 = tm.LUMO_LINE1
    head(a0, -6, 15)
    head(a0 + 1.0, -4, 15, 6)                                     # nghiêng đầu nhẹ, say mê
    head(a1, -8, 15, 0)
    lumo.pose(a0, lean=6)
    lumo.pose(a1, lean=2)
    b0, b1 = tm.LUMO_LINE2
    head(tm.LOOK_COMPASS, 26)                                    # cúi nhìn la bàn trong tay
    for t, a in ((b0, 26), (b0 + 0.3, 34), (b0 + 0.55, 24)):     # gật nhẹ ở "Được rồi"
        head(t, a)
    ears(b0, 8)
    ears(b1, 4)
    chold(b0, C_CHEST)
    chold(b1, C_CHEST)

    # ============================================================ S8: câu hô lần 3, cất la bàn, kéo dây túi, lao đi
    q0, q1 = tm.LUMO_POSE
    ears(q0, -30)                                                # tai cụp hẳn lấy đà
    ears(q0 + 0.15, 16)                                          # bật dựng thẳng hai tai
    ears(q1, 2)
    chold(q0, C_CHEST)
    chold(q0 + 0.25, C_ONE)                                      # chìa la bàn thẳng ra trước ngang ngực, tay kia buông
    head(q0, 24)
    head(q0 + 0.2, -8, 10)
    head(q1, -2, 10)
    lumo.pose(q0, lean=2, yaw=110)
    lumo.pose(q0 + 0.25, lean=-6, yaw=112)                       # xoay nhẹ về phía máy, mắt vẫn về hòn đảo
    squash(q0, 1, 1)
    squash(q0 + 0.12, 1.08, 0.92)
    squash(q0 + 0.25, 0.95, 1.06)
    squash(q1, 1, 1)
    s0, s1 = tm.LUMO_LINE3
    chold(s0 + 0.9, C_ONE)
    chold(s0 + 1.1, C_PUSH)                                      # đẩy la bàn tới thêm ở "ngay phía trước"
    lumo.pose(s0 + 0.9, lean=-6)
    lumo.pose(s0 + 1.15, lean=3)
    head(s0 + 0.9, -2, 10)
    head(s0 + 1.15, -10, 10)
    wag(L.tail, q1, s1, 0.4, 16, base=(36, 0, 0))
    t0, t1 = tm.COMPASS_STOW                                     # cất la bàn vào túi da (miệng túi ở hông phải)
    chold(t0, C_PUSH)
    head(t0 + 0.2, 26, -30)                                      # liếc xuống túi
    chold(t0 + 0.28, (tuple(BAG_TOP), (-10, 0, 0), (-25, 0, 0), (6, 0, 0)), 0.6)
    key(comp_hold, "scale", t0 + 0.32 - HOLD, Vector((0.6, 0.6, 0.6)))
    key(comp_hold, "scale", t0 + 0.32, Vector((0, 0, 0)))
    lumo.pose(t0, lean=3)
    lumo.pose(t1, lean=0)
    k0, k1 = tm.STRAP_TUG                                        # kéo dây túi cho ngay
    arms(k0, (-25, 0, 0))
    arms(k0 + 0.15, (-8, 0, -10))
    arms(k1, (-20, 0, 0))
    key(bag, "location", k0, Vector((-0.2, -0.12, 0.3)))
    key(bag, "location", k0 + 0.15, Vector((-0.2, -0.12, 0.27)))
    key(bag, "location", k1, Vector((-0.2, -0.12, 0.3)))
    squash(k0, 1, 1)
    squash(k0 + 0.15, 1.02, 0.97)
    squash(k1, 1, 1)
    head(k1, 0, 5)
    d0, d1 = tm.DASH                                             # quay người lao đi, ra khỏi khung bên phải
    head(d0, -6, 0)
    squash(d0, 1, 1)
    squash(d0 + 0.1, 1.07, 0.9)                                  # lấy đà
    squash(d0 + 0.2, 0.96, 1.04)
    squash(d0 + 0.3, 1, 1)
    lumo.pose(d0, lean=0, yaw=112)
    lumo.pose(d0 + 0.1, lean=-10, yaw=80)
    lumo.pose(d0 + 0.2, lean=18, yaw=58)                         # lao đi, ngang qua khung về bên phải
    ears(d0 + 0.1, 0)
    ears(d0 + 0.25, -32)
    tail(d0 + 0.2, 55)
    DASH_END = (1.35, -1.95)                                     # ngoài khung S8, bên phải
    pts = [(POS_A[0] + (DASH_END[0] - POS_A[0]) * i / 4, POS_A[1] + (DASH_END[1] - POS_A[1]) * i / 4) for i in range(5)]
    lumo.walk(d0 + 0.15, d1, pts, 0.06)
    steps(L.legs, d0 + 0.15, d1, 4, 36)
    wag(L.arm_r, d0 + 0.15, d1, 0.15, 30, base=(-20, 0, 0), axis=0)
    wag(L.arm_l, d0 + 0.2, d1, 0.15, 30, base=(-20, 0, 0), axis=0)

    # ============================================================ S9: bản đồ nằm lại một mình; Lumo chạy ngược vào, chụp lấy
    lumo.go(tm.MAP_ALONE[0], *DASH_END)
    lumo.pose(tm.MAP_ALONE[0], lean=0, yaw=58)
    BACK_IN = (1.35, 0.15)                                       # ngoài khung S9, bên phải
    lumo.go(tm.LUMO_BACK[0] - 0.1, *BACK_IN)
    lumo.pose(tm.LUMO_BACK[0] - 0.1, lean=16, yaw=-90)           # quay qua mặt trước (ngoài khung), mặt về tảng đá
    rot(map_rock, [(tm.MAP_ALONE[0], (0, 0, MR_YAW))])
    for i, t in enumerate([tm.MAP_ALONE[0] + 0.2 + 0.25 * k for k in range(5)]):   # gió nhẹ: mép bản đồ phập phồng
        rot(map_rock, [(t, (3 if i % 2 else -2, 0, MR_YAW))])
    rot(map_rock, [(tm.MAP_ALONE[1], (0, 0, MR_YAW))])
    n0, n1 = tm.LUMO_BACK
    pts = [(BACK_IN[0] + (POS_B[0] - BACK_IN[0]) * i / 3, BACK_IN[1] + (POS_B[1] - BACK_IN[1]) * i / 3) for i in range(4)]
    lumo.walk(n0, n1 - 0.08, pts, 0.06)
    lumo.go(n1, *POS_B)
    steps(L.legs, n0, n1 - 0.08, 3, 36)
    wag(L.arm_r, n0, n1 - 0.08, 0.15, 30, base=(-20, 0, 0), axis=0)
    wag(L.arm_l, n0 + 0.05, n1 - 0.08, 0.15, 30, base=(-20, 0, 0), axis=0)
    lumo.pose(n0, lean=16, yaw=-90)
    lumo.pose(n1 - 0.08, lean=16)
    lumo.pose(n1, lean=-12, yaw=-98)                             # khựng lại
    ears(n0, -32)
    ears(n1, 14)
    head(n0, 6, 0)
    arms(n1, (-30, 0, 0), (-30, 0, 0))
    gr0, gr1 = tm.MAP_GRAB
    GRAB_LEAN = 24
    lumo.pose(gr0, lean=-12)
    lumo.pose(gr0 + 0.15, lean=GRAB_LEAN)
    head(gr0, 24)
    arms(gr0, (-30, 0, 0), (-30, 0, 0))
    arms(gr0 + 0.15, (-60, 0, 14), (-60, 0, -14))
    grab_t = gr0 + 0.17                                          # chụp lấy tấm bản đồ: bản đồ trong tay ở đúng chỗ trên tảng đá
    scene.frame_set(fr(grab_t))
    loc_m = L.root.matrix_world.inverted() @ (Matrix.Translation(MAP_SPOT) @ map_rock.rotation_euler.to_matrix().to_4x4())
    pl, pr, _ = loc_m.decompose()
    show(map_rock, grab_t, False)
    key(map_hold, "location", grab_t - HOLD, pl)
    rot(map_hold, [(grab_t - HOLD, tuple(math.degrees(a) for a in pr.to_euler("XYZ")))])
    key(map_hold, "scale", grab_t - HOLD, Vector((0, 0, 0)))
    key(map_hold, "location", grab_t, pl)
    rot(map_hold, [(grab_t, tuple(math.degrees(a) for a in pr.to_euler("XYZ")))])
    key(map_hold, "scale", grab_t, Vector((1, 1, 1)))
    mspin(grab_t, 0)
    mhold(gr1, M_CHEST)
    lumo.pose(gr1, lean=0)
    arms(gr1, (-76, 0, 16), (-76, 0, -16))
    tail(n1, 30)
    e0, e1 = tm.LUMO_LINE4                                       # "Nhà thám hiểm Lumo không bao giờ quên bản đồ!"
    lumo.pose(e0 - 0.3, lean=0, yaw=-98)
    lumo.pose(e0, lean=-9, yaw=-25)                              # quay về phía máy, ưỡn ngực, hếch cằm
    squash(e0 - 0.2, 1, 1)
    squash(e0, 0.98, 1.04)
    ears(e0 - 0.2, 14)
    ears(e0, 0)
    head(e0 - 0.2, 10)
    head(e0, -14)
    mhold(e0, M_CHEST)                                           # bản đồ trước ngực, không che mặt
    for t, a in ((e0 + 1.3, -14), (e0 + 1.5, -4), (e0 + 1.7, -14)):
        head(t, a)
    wag(L.tail, e0, e1, 0.5, 16, base=(36, 0, 0))
    f0, f1 = tm.TURN_EDGE                                        # quay về phía mép đồi, mở bản đồ
    lumo.pose(f0, lean=-9, yaw=-25)
    lumo.pose(f1, lean=0, yaw=85)
    squash(f1, 1, 1)
    head(f0, -14)
    head(f1, 30)
    mhold(f0, M_CHEST)
    mhold(f1, M_READ)
    arms(f1, (-70, 0, 16), (-70, 0, -16))

    # ============================================================ S10: cú nhìn bản đồ: xoay, xoay nữa, xoay thêm vòng nữa
    ANG = [0, 180, 270, 630]                                     # rương: đứng thẳng, lộn ngược, nằm ngang, một vòng rồi lại ngang
    for (sa, sb), a, b in zip(tm.MAP_SPINS, ANG, ANG[1:]):
        mspin(sa, a)
        mspin(sb, b)
    for i, t in enumerate([S["S10"][0] + 0.4 * k for k in range(int((S["S10"][1] - S["S10"][0]) / 0.4) + 1)]):
        key(map_hold, "location", t, Vector((0.006 if i % 2 else -0.006, -0.3, 0.45 + (0.006 if i % 2 else -0.006))))   # tay hơi nhún
    head(S["S10"][1], 30)

    # ============================================================ S11: nhún vai, gấp bản đồ nhét vào túi
    h0, h1 = tm.SHRUG
    key(map_hold, "location", h0, Vector(M_READ[0]))
    squash(h0, 1, 1)
    squash(h0 + 0.15, 0.93, 1.09)                                # nhún vai
    squash(h1, 1, 1)
    arms(h0, (-70, 0, 16), (-70, 0, -16))
    arms(h0 + 0.15, (-30, 55, 0), (-60, 0, -8))                  # tay trái giữ bản đồ, tay phải (phía máy) xòe ra ngoài
    arms(h1 + 0.1, (-68, 0, 16), (-68, 0, -16))
    head(h0, 30)
    head(h0 + 0.15, 4, 0, 14)                                    # nghiêng đầu
    head(h1, 6, 0, 4)
    ears(h0, 4)
    ears(h0 + 0.15, -28)                                         # cụp tai
    ears(h1, -8)
    mhold(h0, M_READ)
    mhold(h0 + 0.15, ((0.13, -0.3, 0.4), (-45, 0, -12), 1.0))   # bản đồ theo tay trái (tay cầm vật phải đi theo vật)
    mhold(h1 + 0.1, M_READ)
    o0, o1 = tm.MAP_STOW
    mhold(o0, M_READ)
    head(o0, 26, -25)                                            # liếc xuống túi
    keys(map_hold, "scale", [(o0 + 0.35, Vector((0.5, 0.5, 0.5))), (o0 + 0.55, Vector((0.35, 0.35, 0.35)))])   # gấp lại
    key(map_hold, "location", o0 + 0.55, BAG_TOP)
    rot(map_hold, [(o0 + 0.55, (-80, 0, 0))])
    arms(o0 + 0.35, (-50, 0, 0), (-40, 0, -10))
    arms(o0 + 0.6, (-22, 0, 0), (-6, 0, 0))
    key(map_hold, "scale", o0 + 0.62 - HOLD, Vector((0.35, 0.35, 0.35)))
    key(map_hold, "scale", o0 + 0.62, Vector((0, 0, 0)))
    arms(o1, (-12, 0, 0), (-6, 0, 0))
    ears(o1, 4)
    head(o1, 0, 0)

    # ============================================================ S12–S14: sải bước ra mép, nhấc chân, khựng lại; chiếc lá; lối mòn
    st0, st1 = tm.STRIDE
    yw = yaw_to(POS_B, POS_EDGE)
    lumo.pose(st0, lean=0, yaw=85)
    lumo.pose(st0 + 0.15, lean=7, yaw=yw)
    pts = [(POS_B[0] + (POS_EDGE[0] - 0.02 - POS_B[0]) * i / 6, POS_B[1] + (POS_EDGE[1] - POS_B[1]) * i / 6) for i in range(7)]
    lumo.walk(st0, st1, pts, 0.04)
    steps(L.legs, st0, st1, 6, 30)
    wag(L.arm_r, st0, st1, 0.2, 25, base=(-12, 0, 0), axis=0)
    wag(L.arm_l, st0 + 0.05, st1, 0.2, 25, base=(-6, 0, 0), axis=0)
    wag(L.tail, st0, st1, 0.3, 14, base=(34, 0, 0))
    head(st0, -2)                                                # mắt nhìn phía trước, chưa nhìn xuống chân
    lf0, lf1 = tm.LEG_LIFT
    leg_n = L.legs[1]                                            # chân phải: phía máy quay khi Lumo quay sang phải
    rot(leg_n, [(lf0, (0, 0, 0)), (lf1, (-82, 0, 0))])           # nhấc chân định lao xuống
    rot(L.legs[0], [(lf0, (0, 0, 0)), (lf1, (6, 0, 0))])
    lumo.go(lf1, POS_EDGE[0] + 0.02, POS_EDGE[1], z=0.035)
    lumo.pose(lf1, lean=4)
    arms(lf0, (-12, 0, 0), (-6, 0, 0))
    arms(lf1, (-45, 0, 0), (-40, 0, 0))
    fz0, fz1 = tm.FREEZE                                         # khựng lại, người ngả ra sau, chân còn treo
    lumo.pose(fz0 + 0.1, lean=-10)
    rot(leg_n, [(fz0 + 0.1, (-76, 0, 0)), (fz1, (-78, 0, 0))])
    arms(fz0 + 0.1, (24, 0, 0), (28, 0, 0))
    head(fz0, -2)
    head(fz0 + 0.1, 34)                                          # nhìn xuống sườn dốc lá khô
    ears(fz0, 6)
    ears(fz0 + 0.1, 28)
    ears(fz1, 18)
    tail(fz0, 30)
    tail(fz0 + 0.1, 58)
    sl0, sl1 = tm.LEAF_SLIDE
    ob = streaks[7]                                              # một làn gió nhẹ ở mép dốc
    rot(ob, [(sl0 - 0.25, (0, 0, 90))])
    key(ob, "location", sl0 - 0.25, Vector((0.9, 0.35, 0.3)))
    key(ob, "location", sl0 + 0.1, Vector((2.6, 0.35, 0.05)))
    show(ob, sl0 - 0.25, True)
    show(ob, sl0 + 0.12, False)
    for k in range(9):                                           # chiếc lá trượt vèo xuống dốc tới thảm cỏ: WHOOSH!
        u = k / 8
        p = LEAF_AT.lerp(LEAF_END, u ** 1.15)
        key(slide_leaf, "location", sl0 + (sl1 - sl0) * u, Vector((p.x, p.y, ground_z(p.x, p.y) + 0.015)))
        ang = math.degrees(math.atan2(-(ground_z(p.x + 0.05, p.y) - ground_z(p.x - 0.05, p.y)), 0.1))
        rot(slide_leaf, [(sl0 + (sl1 - sl0) * u, (0, ang, 90 + (10 if k % 2 else -10)))])
    key(slide_leaf, "location", 0.0, Vector((LEAF_AT.x, LEAF_AT.y, ground_z(*LEAF_AT) + 0.015)))
    rot(slide_leaf, [(0.0, (0, 0, 90))])
    key(slide_leaf, "location", sl1 + 0.15, Vector((LEAF_END.x + 0.08, LEAF_END.y, LOW + 0.015)))
    rot(slide_leaf, [(sl1 + 0.15, (0, 0, 96))])
    head(sl0 + 0.15, 34, 4)                                      # mắt nhìn theo chiếc lá
    head(sl1, 28, 4)
    bk0, bk1 = tm.LEG_BACK                                       # rụt chân về, lùi một bước
    rot(leg_n, [(bk0, (-78, 0, 0)), (bk1, (0, 0, 0))])
    rot(L.legs[0], [(bk1, (0, 0, 0))])
    lumo.go(bk0, POS_EDGE[0] + 0.02, POS_EDGE[1], z=0.035)
    lumo.go(bk0 + 0.15, (POS_EDGE[0] + POS_BACK[0]) / 2, POS_EDGE[1], 0.04)
    lumo.go(bk1, *POS_BACK)
    lumo.pose(bk0, lean=-10)
    lumo.pose(bk1, lean=0)
    arms(bk0, (24, 0, 0), (28, 0, 0))
    arms(bk1, (-10, 0, 0), (-4, 0, 0))
    tail(bk1, 30)
    head(bk1, 28, 4)                                             # vẫn nhìn chiếc lá ở chân dốc
    ears(bk1, 6)
    pp0, pp1 = tm.LOOK_PATH                                      # nhìn sang bên: lối mòn (phía tay phải, về phía máy)
    head(pp0, 28, 4)
    head(pp1, 18, -45)
    ears(pp0, 6)
    ears(pp1, 18)
    lumo.pose(tm.PATH_PAN[1], yaw=yw)
    lumo.pose(tm.PATH_PAN[1] + 0.3, yaw=45)                      # cả người quay về lối mòn (trong cú nhìn S13)
    head(tm.PATH_PAN[1] + 0.3, 14, 0)
    nd0, nd1 = tm.LUMO_NOD
    for t, a in ((nd0, 10), (nd0 + 0.2, 26), (nd0 + 0.4, 8), (nd0 + 0.6, 26), (nd1, 8)):   # gật đầu
        head(t, a, 0)
    ears(nd1, 8)
    wag(L.tail, nd0, tm.WALK_DOWN[0], 0.6, 14, base=(28, 0, 0))

    # ============================================================ S15: chú chim đáp xuống tảng đá, nhìn theo Lumo, gật gù
    bl0, bl1 = tm.BIRD_LAND
    key(B.root, "scale", -1.0, Vector((0, 0, 0)))
    show(B.root, bl0 - 0.05, True)
    BY = yaw_to(BIRD_AT, POS_BACK)                               # nhìn theo Lumo ở mép đồi
    for t, d in ((bl0 - 0.05, (-0.95, -0.25, 0.75)), (bl0 + 0.25, (-0.6, -0.15, 0.42)), (bl0 + 0.5, (-0.25, -0.05, 0.16)),
                 (bl1, (0, 0, 0))):
        key(B.root, "location", t, BIRD_AT + Vector(d))
    rot(B.root, [(bl0 - 0.05, (0, 0, 60)), (bl1, (0, 0, BY))])
    t, i = bl0 - 0.05, 0
    while t < bl1 - 0.05:
        rot(B.wing, [(t, (0, 0, -70 if i % 2 else 10))])
        rot(B.wing_far, [(t, (0, 0, 70 if i % 2 else -10))])
        t, i = t + 0.06, i + 1
    rot(B.wing, [(bl1 + 0.05, (0, 0, 0))])
    rot(B.wing_far, [(bl1 + 0.05, (0, 0, 0))])
    keys(B.root, "scale", [(bl1, Vector((1.12, 1.12, 0.86))), (bl1 + 0.12, Vector((0.95, 0.95, 1.06))), (bl1 + 0.25, Vector((1, 1, 1)))])
    rot(B.head, [(bl1, (0, 0, 0)), (bl1 + 0.3, (-12, 0, 0))])     # ngẩng nhìn theo Lumo
    nb0, nb1 = tm.BIRD_NOD
    for t, a in ((nb0, -12), (nb0 + 0.25, 22), (nb0 + 0.5, -4), (nb0 + 0.75, 22), (nb1, 0)):   # gật gù chậm: tán thành
        rot(B.head, [(t, (a, 0, 0))])

    # ============================================================ S16: rút la bàn, nhìn mũi sao, ngẩng nhìn hòn đảo, cất la bàn
    lumo.pose(tm.BIRD_LAND[0], yaw=45)
    lumo.pose(tm.BIRD_NOD[0], yaw=108)                           # quay về phía hòn đảo (ngoài khung, trong cú chim)
    head(tm.BIRD_NOD[0], 0, 0)
    x0, x1 = tm.COMPASS_OUT                                      # la bàn ló ra ở miệng túi (túi giữ nguyên), kéo lên
    arms(x0, (-12, 0, 0), (-4, 0, 0))
    arms(x0 + 0.15, (-25, 0, 0))
    key(comp_hold, "scale", x0 + 0.17 - HOLD, Vector((0, 0, 0)))
    key(comp_hold, "location", x0 + 0.17, BAG_TOP)
    rot(comp_hold, [(x0 + 0.17, (-10, 0, 0))])
    key(comp_hold, "scale", x0 + 0.17, Vector((0.4, 0.4, 0.4)))
    chold(x1, C_LOOK)
    head(x0, 10, -20)
    head(x1, 28, 0)                                              # nhìn mũi sao
    li0, li1 = tm.LOOK_ISLAND
    head(li0, 28, 0)
    head(li1, -12, 12)                                           # ngẩng lên nhìn hòn đảo
    ears(li0, 6)
    ears(li0 + 0.2, 18)
    ears(li1, 8)
    y0, y1 = tm.COMPASS_AWAY                                     # cất la bàn
    chold(y0, C_LOOK)
    chold(y0 + 0.3, (tuple(BAG_TOP), (-10, 0, 0), (-25, 0, 0), (-4, 0, 0)), 0.6)
    key(comp_hold, "scale", y0 + 0.35 - HOLD, Vector((0.6, 0.6, 0.6)))
    key(comp_hold, "scale", y0 + 0.35, Vector((0, 0, 0)))
    arms(y1, (-10, 0, 0), (-4, 0, 0))
    head(y1, 0, 5)

    # ============================================================ S17: đi xuống theo lối mòn, mắt nhìn phía trước; lóe lần 2
    wd0, wd1 = tm.WALK_DOWN
    route = [POS_BACK, (1.62, -0.85), (1.95, -1.35), (2.4, -1.72), (2.9, -1.84), (3.35, path_y(3.35))]
    dist = [0.0]                                                 # chia đều theo quãng đường, 12 bước
    for (ax, ay), (bx, by) in zip(route, route[1:]):
        dist.append(dist[-1] + math.hypot(bx - ax, by - ay))
    pts = []
    for k in range(13):
        d = dist[-1] * k / 12
        j = max(i for i in range(len(dist) - 1) if dist[i] <= d + 1e-9) if d < dist[-1] else len(dist) - 2
        u = (d - dist[j]) / (dist[j + 1] - dist[j])
        pts.append((route[j][0] + (route[j + 1][0] - route[j][0]) * u, route[j][1] + (route[j + 1][1] - route[j][1]) * u))
    lumo.walk(wd0, wd1, pts, 0.03)
    steps(L.legs, wd0, wd1 - 0.05, 12, 20)
    lumo.pose(wd0, lean=0, yaw=108)
    lumo.pose(wd0 + 0.5, lean=4, yaw=yaw_to(route[0], route[2]))
    lumo.pose(wd0 + (wd1 - wd0) * 0.45, yaw=yaw_to(route[2], route[3]))
    lumo.pose(wd0 + (wd1 - wd0) * 0.7, yaw=yaw_to(route[3], route[5]))
    lumo.pose(wd1, lean=4)
    head(wd0, 0, 5)
    head(wd0 + 0.5, -2, 0)
    wag(L.arm_r, wd0, wd1, 0.68, 14, base=(4, 0, 0), axis=0)      # tay phải đánh ra sau, không che túi
    wag(L.arm_l, wd0 + 0.34, wd1, 0.68, 14, base=(-8, 0, 0), axis=0)
    pulse(hub_flash, tm.HUB_FLASH2, 1.0)                         # hòn đảo lóe xanh ngọc lần nữa
    show(hub_tint, tm.HUB_FLASH2, True)
    show(hub_tint, tm.HUB_FLASH2 + 0.7, False)
    pulse(bag_glow, tm.HUB_FLASH2, 1.0)                          # la bàn lóe theo qua mép nắp túi da
    ears(tm.HUB_FLASH2 + 0.1, 6)
    ears(tm.HUB_FLASH2 + 0.25, 16)                               # tai khẽ dựng, vẫn đi tiếp
    ears(tm.HUB_FLASH2 + 0.5, 8)

    # ============================================================ chống trôi giữa hai key thưa
    ease_gaps([L.root, L.head, *[e for e, _ in L.ears], L.arm_r, L.arm_l, L.tail, *L.legs, cape, comp_hold, map_hold, bag,
               B.root, B.head])

    # ============================================================ các cú nhìn của Lumo: đầu ẩn (S10 ẩn cả hai tay, hiện bàn tay theo bản đồ)
    def hide_in(obs, n, s=1.0):
        a, b = S[n]
        for ob in obs:
            key(ob, "scale", a - HOLD, Vector((s, s, s)))
            key(ob, "scale", a, Vector((0, 0, 0)))
            key(ob, "scale", b - HOLD, Vector((0, 0, 0)))
            key(ob, "scale", b, Vector((s, s, s)))

    for n in ("S1", "S5", "S10", "S13"):
        if in_seg(n):
            hide_in([L.head], n)
    if in_seg("S10"):
        hide_in([L.arm_r, L.arm_l], n="S10")
        for ob in paws:
            show(ob, S["S10"][0], True)
            show(ob, S["S10"][1], False)

    # ============================================================ máy quay (một máy mỗi cú; chỉ dựng các cú trong đoạn)
    def pov(n, eye, look, lens, dt=0.1, follow=None):
        """Cú nhìn: máy ở chỗ mắt (eye: điểm cục bộ của gốc Lumo), nhìn tới look (điểm cục bộ của gốc Lumo, hoặc hàm
        trả về điểm thế giới)."""
        a, b = S[n]
        out, t = [], a
        while t <= b + 1e-6:
            scene.frame_set(fr(t))
            mw = L.root.matrix_world
            e = mw @ Vector(eye)
            g = look() if callable(look) else mw @ Vector(look)
            out.append((t, tuple(e), tuple(g), lens))
            t += dt
        return out

    def around(p, los, dist, z, look_yaw=None, look_z=None, lens=30, t=None, n=None):
        """Máy nhìn tới p (x, y) theo hướng los (yaw của đường ngắm), cách dist, cao z; look_yaw: trục máy lệch khỏi
        đường ngắm (điểm nhìn cách 6 m theo hướng đó)."""
        c = Vector((p[0], p[1], 0.0)) - ydir(los) * dist
        c.z = z
        if look_yaw is None:
            tgt = Vector((p[0], p[1], look_z))
        else:
            tgt = c + ydir(look_yaw) * 6.0
            tgt.z = look_z
        return (S[n][0] if t is None else t, tuple(c), tuple(tgt), lens)

    def map_center():
        return map_hold.matrix_world.translation.copy()

    CAMS = {   # (giây, vị trí máy, điểm nhìn, tiêu cự mm)
        "S1": lambda: pov("S1", (0, 0.1, 0.84), (0, -1.6, 0.42), 22),                     # cú nhìn: la bàn trong tay, sườn đồi chắn
        "S2": lambda: [(S["S2"][0], (-5.4, -5.6, -0.3), (-4.4, 0.0, -0.25), 26)],         # toàn chân đồi: sườn cỏ thoải lên bên phải
        "S3": lambda: [(S["S3"][0], (-1.0, -7.0, 3.0), (0.6, 0.9, -0.4), 24)],          # toàn đỉnh đồi: tảng đá, mép dốc lá, lối mòn, biển mây
        "S4": lambda: [around(POS_A, 225, 2.2, 0.72, look_z=0.42, lens=30, n="S4")],      # trung: đặt bản đồ, nâng la bàn
        "S5": lambda: pov("S5", (0, 0.12, 0.74), (0, -3.0, 0.1), 22),                     # cú nhìn: la bàn, chân trời phía sau
        "S6": lambda: [around(POS_A, 165, 2.7, 0.95, look_yaw=144, look_z=0.55, lens=26, n="S6")],   # trung toàn: hòn đảo hiện ra
        "S7": lambda: [around(POS_A, 262, 1.8, 0.78, look_z=0.7, lens=40, n="S7")],       # cận Lumo, mặt 3/4 về máy
        "S8": lambda: [around(POS_A, 170, 2.2, 0.85, look_yaw=146, look_z=0.5, lens=24, n="S8")],    # trung, đảo ở hậu cảnh
        "S9": lambda: [(S["S9"][0], (-0.72, -2.05, 0.72), (-0.48, 0.3, 0.38), 32)],      # cận tảng đá: bản đồ một mình
        "S10": lambda: pov("S10", (0, -0.02, 0.86), map_center, 22, 0.2),                # cú nhìn bản đồ
        "S11": lambda: [around(POS_B, 228, 2.0, 0.8, look_z=0.48, lens=32, n="S11")],     # trung: nhún vai, cất bản đồ
        "S12": lambda: [(S["S12"][0], (3.6, -4.6, 0.75), (2.0, 0.4, -0.25), 28)],        # toàn từ chân dốc: Lumo ở mép, cả sườn dốc tới thảm cỏ
        "S13": lambda: [(S["S13"][0], (POS_BACK[0], POS_BACK[1] + 0.04, 0.86), (LEAF_END.x, LEAF_END.y + 0.1, LOW), 24),
                        (tm.PATH_PAN[0], (POS_BACK[0], POS_BACK[1] + 0.04, 0.86), (LEAF_END.x, LEAF_END.y + 0.1, LOW), 24),
                        (tm.PATH_PAN[1], (POS_BACK[0], POS_BACK[1] + 0.04, 0.86), (4.0, path_y(4.0) - 0.2, -0.3), 24)],   # lia sang lối mòn
        "S14": lambda: [around(POS_BACK, 228, 2.3, 0.75, look_z=0.52, lens=35, n="S14")],  # trung: gật đầu
        "S15": lambda: [(S["S15"][0], (-0.5, -0.95, 0.42), (-0.5, 0.38, 0.33), 40)],      # cận chú chim trên tảng đá
        "S16": lambda: [around(POS_BACK, 168, 2.2, 0.85, look_yaw=145, look_z=0.5, lens=26, n="S16")],   # trung, đảo ở hậu cảnh
        "S17": lambda: [around(POS_BACK, 165, 2.4, 0.9, look_yaw=150, look_z=0.3, lens=26, n="S17"),
                        around((3.35, path_y(3.35)), 165, 2.4, 0.55, look_yaw=150, look_z=-0.05, lens=26,
                               t=S["S17"][1], n="S17")],                                   # lia theo Lumo xuống lối mòn
        "S18": lambda: [(S["S18"][0], (90.0, 0.0, 5.0), (90.0, 5.0, 5.0), 30)],           # khung đen
    }
    shots = [(n, a, b) for n, a, b in tm.SHOTS if a < end_t - 1e-6 and b > offset + 1e-6]
    cams = cameras(shots, {n: CAMS[n]() for n, _, _ in shots})
    for cam in cams.values():                                    # máy di chuyển đều: nội suy LINEAR
        set_linear(cam)
        set_linear(cam.data)
        set_linear(cam.constraints[0].target)

    # ============================================================ SkyRig bám máy đang dùng từng khung (LINEAR)
    marks = sorted((m.frame, m.camera) for m in scene.timeline_markers)
    for f in range(1, scene.frame_end + 1):
        cam = [c for fm, c in marks if fm <= f]
        cam = cam[-1] if cam else marks[0][1]
        scene.frame_set(f)
        sky.location = cam.matrix_world.translation
        sky.keyframe_insert("location", frame=f)
    set_linear(sky)

    # ============================================================ mũi sao luôn chỉ về hòn đảo (key từng khung, sau mọi chuyển động)
    hub_dome = bpy.data.objects["Hub_Dome"]
    prev = None
    for f in range(1, scene.frame_end + 1):
        scene.frame_set(f)
        mw = comp.matrix_world
        if mw.to_3x3().determinant() < 1e-9:
            continue
        tgt = hub_dome.matrix_world @ (HUB + Vector((0, 0, 3.4)))
        d = mw.inverted() @ tgt
        phi = math.degrees(math.atan2(d.x, -d.y))
        if prev is not None:
            phi += 360 * round((prev - phi) / 360)
        prev = phi
        needle.rotation_euler = (0, 0, math.radians(phi))
        needle.keyframe_insert("rotation_euler", frame=f)
    set_linear(needle)

    # ============================================================ tự kiểm khung
    Hd = Vector((0, 0, 0.2))
    must = {"S2": [(L.root, Vector((0, 0, 0.5)))], "S3": [(rock, Vector())], "S4": [(L.head, Hd), (rock, Vector())],
            "S5": [(comp, Vector())], "S1": [(comp, Vector())], "S6": [(L.head, Hd)], "S7": [(L.head, Hd)],
            "S8": [(rock, Vector())], "S9": [(map_rock, Vector())], "S10": [(map_spin, Vector())], "S11": [(L.head, Hd)],
            "S12": [(L.head, Hd), (slide_leaf, Vector())], "S14": [(L.head, Hd)], "S15": [],
            "S16": [(L.head, Hd)], "S17": [(L.head, Hd)]}
    extra = [("S8", L.head, S["S8"][0], tm.DASH[0] + 0.2), ("S15", B.root, tm.BIRD_LAND[0] + 0.4, S["S15"][1]), ("S9", L.head, tm.LUMO_BACK[1], S["S9"][1]),
             ("S6", isl, tm.CLOUD_PART[1], S["S6"][1]), ("S8", isl, S["S8"][0], S["S8"][1]),
             ("S16", isl, S["S16"][0], S["S16"][1]), ("S17", isl, S["S17"][0], S["S17"][1])]
    check_in_frame(shots, cams, must, extra, ground=lambda p: ground_z(p.x, p.y))
    stills = [round((a + b) / 2, 2) for _, a, b in shots]
    stills += [t for t in (tm.MAP_DOWN[0] + 0.4, tm.HUB_FLASH1 + 0.12, tm.LUMO_POSE[1], tm.DASH[0] + 0.3, tm.MAP_GRAB[0] + 0.2,
                           tm.MAP_SPINS[0][1], tm.MAP_SPINS[2][0] + 0.4, tm.FREEZE[0] + 0.3, tm.LEAF_SLIDE[0] + 0.35,
                           tm.PATH_PAN[1], tm.BIRD_LAND[1], tm.LOOK_ISLAND[1], tm.HUB_FLASH2 + 0.12) if offset <= t < end_t]
    finish(out_blend, sorted(set(stills)))
