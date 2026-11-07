"""
Previz khối Cảnh 3 tập 000A (Khám phá đầu tiên) dẫn Seedance (04_PRODUCTION/SEEDANCE.md): phế tích (tường, mảng dây
leo, phù điêu đám mây, cửa thấp, thảm rêu), vòm đá (bệ đỡ trống, cánh cửa khắc mây), Lumo, Wonder Compass, hòn sỏi
dạng khối (pipeline/blocks.py), máy quay từng cú. Mọi mốc lấy từ timing.py của previz 2D (TIMING trong build_shot.py
của đoạn), không gõ lại số. Diễn theo previz 2D đã chốt: 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh03/.
Ba đoạn (Seedance 2.5, tối đa 30 giây) gọi build() với giây bắt đầu và độ dài của đoạn:
    sh050: 0–26.0 s    (S1–S6: đi dọc tường, la bàn sáng dần, kêu dày; vạch dây leo, phù điêu ánh lên; ấn, kéo; lấy
           đà đẩy, phù điêu xoay, ngã lăn ra thảm rêu, cửa thấp mở, phù điêu tắt; cú nhìn la bàn: mũi sao quay vào cửa)
    sh060: 26.0–49.2 s (S7–S10: "Mình tìm được rồi!", vào cửa thấp; vòm đá, bệ trống, cụp tai; ấn la bàn vào bệ, gõ
           bệ, chờ sỏi, thở phào, PLOP; nhìn bệ, nhìn la bàn; quay lưng về phía cánh cửa, liếc la bàn)
    sh070: 49.2–74.9 s (S11–S14: cận la bàn, cánh cửa ở hậu cảnh: xoay trái, xoay phải, xoay hai vòng; chóng mặt;
           bước về phía cánh cửa, cửa lấp lánh; "Khoan đã…", "Cậu dẫn tới… kỳ lạ!", cất la bàn, chạy tới đẩy cửa)
Diễn dựng cho cả cảnh để các đoạn nối liền; khung 1 của đoạn = giây bắt đầu (blocks.T0), chỉ dựng máy quay của các cú
trong đoạn.

Nối ngay cuối Cảnh 2 (canh02_blocks.py): Lumo đứng sát đầu tường (-8.715, 1.2) quay ba phần tư về máy, la bàn ở tay phía
máy, mũi sao chỉ tâm phù điêu (RELIEF) sau mảng dây leo. Bối cảnh chung: ruins_blocks.py (build_ruins, build_far_wall).
Phần riêng Cảnh 3 dựng ở đây, không đổi hình của phần chung: khối tường xa (Ruins_WallFar) dựng lại đúng cỡ nhưng có lỗ
cửa thấp (DOOR_X, vừa tầm Lumo, vòm trên) và cánh đá lấp kín lỗ; mảng dây leo (Vines) tách đúng từng sợi thành hai nửa
rủ từ thanh ngang để vạch ra; phù điêu đám mây trong hốc trên mặt tường (tâm RELIEF, xoay quanh trục vuông góc mặt
tường); thảm rêu dày dưới chân tường; lối tối sau cửa thấp.
Vòm đá dựng riêng ở X quanh VC = 40 (xa phế tích), trục dài theo Y như ảnh stone_vault_hero.png: cửa thấp vào ở đầu gần
(Y VY0, lệch phải), bệ đỡ trống PED ở giữa, cánh cửa đá khắc mây ở đầu xa (Y VY1), đối diện cửa thấp; trần vòm cuốn có
ô tròn sáng (khối phát sáng, trần kín nên không có luồng nắng), đèn vùng tản đều. Lumo đi vào xa máy ở cả hai phía cửa
(ngoài: vào tường, +Y; trong: từ cửa gần về phía bệ, +Y) nên hướng màn hình liền.
Bố trí để thấy mặt: ở tường Lumo đứng bên phải phù điêu, mặt chếch về phù điêu, máy ở phía trước bên trái; ở bệ Lumo
đứng bên phải bệ quay mặt về bệ (-X), máy phía trước bên trái. Mọi chỗ tay chạm (dây leo, phù điêu, mặt bệ, cánh cửa)
tính từ vai và chiều dài khối tay (stand_for): người đứng chỗ để vai cách điểm chạm đúng ARM.
La bàn như Cảnh 2 (vỏ vàng, kính xanh, mũi sao tám cánh, đầu chỉ vàng có viên đá xanh); mũi sao tính góc từng khung từ
ma trận thế giới của la bàn: phù điêu → lướt vào trong cửa thấp (NEEDLE_TO_DOOR) → cánh cửa khắc mây (từ lúc vào vòm,
cả la bàn nằm trên bệ). Kính sáng dần, nhấp nháy lúc kêu (cường độ phát sáng tối đa khoảng 3 để giữ màu); rung bằng
key vị trí nhỏ của la bàn trong tay. Cú S6 là cú nhìn của Lumo (máy ở chỗ mắt, đầu ẩn tới hết đuôi sh050).
Màu: Lumo cam (ô trắng = hướng mặt); bối cảnh xám; la bàn vàng, kính xanh; đường mây trên phù điêu, ánh lấp lánh và
khe sáng trên cánh cửa phát sáng vàng; ô trần, lối sáng sau cửa vào phát sáng nhạt.
"""
import math
import pathlib
import random
import sys
from types import SimpleNamespace

import bpy
from bpy_extras import anim_utils
from mathutils import Euler, Matrix, Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.path[:0] = [str(ROOT / "pipeline"), str(HERE)]
import blocks  # noqa: E402  blocks.T0 (giây đầu đoạn) đổi sau start()
from blocks import *  # noqa: E402,F403  khối, vật liệu, nhân vật dạng khối, keyframe theo giây, máy quay
from ruins_blocks import LOW_Z, RELIEF, VINES, WALL_TOP, WALL_Y, build_far_wall, build_ruins, ground_z  # noqa: E402

HOLD = 1 / 24                                                    # một khung: key ẩn và key hiện cách nhau ít hơn thì rơi vào cùng khung
CR = 0.08                                                        # bán kính vỏ la bàn (như Cảnh 2)
ARM = 0.29                                                       # khối tay Lumo, vai tới đầu bàn tay
SHOULDER = {"l": Vector((0.20, 0, 0.55)), "r": Vector((-0.20, 0, 0.55))}   # l: tay trái, phía +X cục bộ
START = Vector((-8.715, 1.2, LOW_Z))                             # chỗ đứng cuối Cảnh 2, sát đầu tường
START_YAW = -45
# --- phế tích (phần riêng Cảnh 3)
DOOR_X, DOOR_W, DOOR_H = -13.25, 0.7, 1.12                       # cửa thấp vừa tầm Lumo (previz 2D: ruins.py)
DOOR_IN = Vector((DOOR_X, 1.8, LOW_Z + 0.5))                     # trong cửa thấp: mũi sao chỉ vào đây sau NEEDLE_TO_DOOR
MOSS_TOP = LOW_Z + 0.03                                          # mặt thảm rêu
SIT = Vector((-12.62, -0.05, MOSS_TOP - 0.22))                   # ngồi bệt trên thảm rêu, giữa phù điêu và cửa thấp
SIT_YAW = -178                                                   # ngồi quay mặt vào tường: phù điêu bên phải, cửa thấp bên trái
# --- vòm đá
VC, VX0, VX1 = 40.0, 38.0, 42.0                                  # trục vòm, hai tường bên
VY0, VY1 = -2.6, 3.4                                             # tường đầu gần (cửa vào), tường đầu xa (cánh cửa khắc mây)
VH, VR = 1.2, 2.0                                                # chân vòm cuốn, bán kính vòm (đỉnh trần 3.2)
ENT_X, ENT_W, ENT_H = 40.9, 0.7, 1.12                            # cửa thấp vào ở tường đầu gần, lệch phải
PED = Vector((VC, 0.6, 0.0))                                     # bệ đỡ trống: trụ đá tròn
PED_R, PED_H = 0.2, 0.45                                         # rộng bằng vai Lumo, mặt bệ ngang ngực
CD_W, CD_H = 1.3, 1.7                                            # cánh cửa đá khắc mây (hai cánh, vòm trên)
CLOUD_DOOR = Vector((VC, VY1, 0.85))                             # tâm cánh cửa: mũi sao chỉ vào đây trong vòm


def facing(yaw):
    r = math.radians(yaw)
    return Vector((math.sin(r), -math.cos(r), 0.0))


def lateral(yaw):
    """Hướng +X cục bộ (phía tay trái l) của nhân vật quay yaw."""
    r = math.radians(yaw)
    return Vector((math.cos(r), math.sin(r), 0.0))


def rmat(lean, yaw, roll=0.0):
    return Euler([math.radians(a) for a in (lean, roll, yaw)], "XYZ").to_matrix()


def stand_for(points, yaw, lean, z, anchor):
    """Gốc nhân vật (cùng yaw, lean, cao z) lùi từ anchor ngược hướng mặt sao cho mỗi vai cách điểm chạm của tay đó
    đúng ARM (trung bình các tay): points = {"l"/"r": điểm thế giới}."""
    R = rmat(lean, yaw)
    f = facing(yaw)
    a = Vector((anchor.x, anchor.y, z))

    def err(d):
        root = a - f * d
        return sum((root + R @ SHOULDER[s] - Vector(p)).length for s, p in points.items()) / len(points) - ARM

    lo, hi = -0.3, 1.2
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if err(mid) < 0 else (lo, mid)
    return a - f * ((lo + hi) / 2)


def linear(ob):
    """Mọi key của ob nội suy LINEAR (máy di chuyển đều: để ease thì Seedance dồn chuyển động thành một cú vụt)."""
    ad = ob.animation_data
    if ad and ad.action:
        for fc in anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def star_profile(r_long, r_short, cx=0.0, cz=0.0):
    """Sao hoa gió: bốn cánh dài xen bốn cánh ngắn (đa giác x, z)."""
    pts = []
    for k in range(16):
        a = math.pi / 2 + math.pi * k / 8
        r = (r_long if k % 4 == 0 else r_short) if k % 2 == 0 else r_short * 0.38
        pts.append((cx + r * math.cos(a), cz + r * math.sin(a)))
    return pts


def disc(name, center, normal, r, depth, mat, col, parent=None):
    """Đĩa tròn (trụ dẹt) tâm center, pháp tuyến normal."""
    ob = add_obj(name, cyl_bm(r, depth, segs=28), mat, col, parent=parent, loc=center)
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = Vector(normal).to_track_quat("Z", "Y")
    return ob


def arch_profile(x0, x1, z0, h, n=12):
    """Lỗ cửa vòm: chữ nhật từ z0, nửa tròn trên, cao h (đa giác x, z theo chiều kim đồng hồ ngược)."""
    r = (x1 - x0) / 2
    cx, zs = (x0 + x1) / 2, z0 + h - r
    return [(x0, z0), (x1, z0)] + [(cx + r * math.cos(math.pi * k / n), zs + r * math.sin(math.pi * k / n)) for k in range(n + 1)]


# ================================================================ phế tích: phần riêng Cảnh 3
def ruins_extra():
    """Lỗ cửa thấp trong tường xa, cánh đá, lối tối sau cửa, thảm rêu, phù điêu đám mây, dây leo tách hai nửa."""
    stone = bpy.data.materials["M_Stone"]
    dark = material("M_DoorDark", (0.1, 0.095, 0.09), 0.9)
    moss = material("M_MossCarpet", (0.3, 0.32, 0.28), 0.95)
    recess_m = material("M_ReliefRecess", (0.22, 0.21, 0.2), 0.9)
    relief_m = material("M_ReliefStone", (0.66, 0.65, 0.63), 0.8)
    glow_m = material("M_ReliefGlow", (1.0, 0.72, 0.15), 0.3, emit=((1.0, 0.62, 0.08), 3.0))
    day_m = material("M_DaylightPatch", (0.9, 0.86, 0.72), 0.8, emit=((1.0, 0.95, 0.8), 0.8))

    # tường xa dựng lại đúng khối cũ, có lỗ cửa thấp vòm trên
    old = bpy.data.objects["Ruins_WallFar"]
    vs = [old.matrix_world @ v.co for v in old.data.vertices]
    lo = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
    hi = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    bpy.data.objects.remove(old)
    x0, x1 = DOOR_X - DOOR_W / 2, DOOR_X + DOOR_W / 2
    r = DOOR_W / 2
    zs, ztop = LOW_Z + DOOR_H - r, LOW_Z + DOOR_H
    bm = box_bm((x0 - lo.x, hi.y - lo.y, hi.z - lo.z), ((lo.x + x0) / 2, (lo.y + hi.y) / 2, (lo.z + hi.z) / 2))
    bm = box_bm((hi.x - x1, hi.y - lo.y, hi.z - lo.z), ((x1 + hi.x) / 2, (lo.y + hi.y) / 2, (lo.z + hi.z) / 2), bm=bm)
    bm = box_bm((DOOR_W, hi.y - lo.y, hi.z - ztop), (DOOR_X, (lo.y + hi.y) / 2, (ztop + hi.z) / 2), bm=bm)
    n = 10
    left = [(x0, ztop), (x0, zs)] + [(DOOR_X + r * math.cos(math.pi - math.pi / 2 * k / n), zs + r * math.sin(math.pi - math.pi / 2 * k / n))
                                     for k in range(1, n + 1)]
    right = [(x1, ztop), (DOOR_X, ztop)] + [(DOOR_X + r * math.cos(math.pi / 2 - math.pi / 2 * k / n), zs + r * math.sin(math.pi / 2 - math.pi / 2 * k / n))
                                           for k in range(1, n + 1)]
    bm = prism(left, lo.y, hi.y, bm=bm)
    bm = prism(right, lo.y, hi.y, bm=bm)
    add_obj("Ruins_WallFar", bm, stone, "SET")
    # cánh đá lấp kín lỗ (bản lề mép trái, mở vào trong tường), lùi 1 cm sau mặt tường cho thấy đường viền
    door = empty("Door_Hinge", "SET", loc=(x0 + 0.005, WALL_Y[0] + 0.06, LOW_Z))
    add_obj("Door_Panel", prism([(x - x0 - 0.005, z - LOW_Z) for x, z in arch_profile(x0 + 0.005, x1 - 0.005, LOW_Z, DOOR_H - 0.005)],
                                -0.05, 0.05), stone, "SET", parent=door)
    # lối tối sau cửa: hai vách, vách cuối, mái; vệt nắng trên nền lối (hiện khi cửa mở)
    bm = box_bm((0.15, 1.2, DOOR_H + 0.1), (x0 - 0.075, hi.y + 0.6, LOW_Z + (DOOR_H + 0.1) / 2))
    bm = box_bm((0.15, 1.2, DOOR_H + 0.1), (x1 + 0.075, hi.y + 0.6, LOW_Z + (DOOR_H + 0.1) / 2), bm=bm)
    bm = box_bm((DOOR_W + 0.3, 0.12, DOOR_H + 0.1), (DOOR_X, hi.y + 1.26, LOW_Z + (DOOR_H + 0.1) / 2), bm=bm)
    bm = box_bm((DOOR_W + 0.3, 1.32, 0.1), (DOOR_X, hi.y + 0.6, LOW_Z + DOOR_H + 0.05), bm=bm)
    add_obj("Door_Passage", bm, dark, "SET")
    patch = add_obj("Door_DayPatch", box_bm((DOOR_W - 0.12, 0.9, 0.004)), day_m, "PROPS", loc=(DOOR_X, WALL_Y[0] + 0.55, LOW_Z + 0.004))
    # thảm rêu dày dưới chân tường, trước phù điêu và cửa thấp
    add_obj("MossCarpet", box_bm((3.3, 1.43, 0.03), (-12.35, 0.165, LOW_Z + 0.015)), moss, "SET")
    # phù điêu đám mây trong hốc trên mặt tường; đường mây phát sáng (ẩn tới RELIEF_ON)
    relief = empty("Relief", "SET", loc=RELIEF)
    rec = add_obj("Relief_Recess", cyl_bm(1.0, 0.012, axis="Y", segs=32), recess_m, "SET", loc=RELIEF + Vector((0, -0.006, 0)))
    rec.scale = (0.46, 1.0, 0.36)
    bm = None
    for cx, cz, rr in ((-0.2, -0.04, 0.17), (0.02, 0.07, 0.21), (0.22, -0.03, 0.16), (-0.33, -0.1, 0.1), (0.34, -0.1, 0.1)):
        bm = sphere_bm(rr, (cx, -0.02, cz), (1.0, 0.25, 0.85), bm=bm, segs=20)
    bm = box_bm((0.72, 0.05, 0.1), (0.0, -0.02, -0.17), bm=bm)
    add_obj("Relief_Cloud", bm, relief_m, "SET", parent=relief)
    glow = []
    for i, (cx, cz, rr) in enumerate(((-0.2, -0.03, 0.08), (0.04, 0.08, 0.1), (0.24, -0.02, 0.07))):
        bm = None
        for k in range(10):
            a = math.radians(90 + 30 * k)
            bm = box_bm((0.035, 0.012, 0.016), (0, 0, 0), bm=bm)
            bm.verts.ensure_lookup_table()
            for v in bm.verts[-8:]:
                v.co = Matrix.Rotation(-a, 3, "Y") @ v.co + Vector((cx + rr * math.cos(a), -0.072, cz + rr * math.sin(a) * 0.9))
        glow.append(add_obj(f"Relief_Glow{i}", bm, glow_m, "PROPS", parent=relief))
    glow.append(add_obj("Relief_GlowBar", box_bm((0.6, 0.012, 0.018), (0.0, -0.05, -0.17)), glow_m, "PROPS", parent=relief))
    # mảng dây leo: tách đúng từng sợi của build_far_wall() thành hai nửa, mỗi nửa xoay quanh đầu trên mép ngoài
    old = bpy.data.objects["Vines"]
    vmat = old.data.materials[0]
    vs = [v.co.copy() for v in old.data.vertices]
    assert len(vs) % 8 == 0, "Vines không còn là các khối hộp"
    boxes = []
    for i in range(0, len(vs), 8):
        g = vs[i:i + 8]
        boxes.append((Vector((min(v.x for v in g), min(v.y for v in g), min(v.z for v in g))),
                      Vector((max(v.x for v in g), max(v.y for v in g), max(v.z for v in g)))))
    bpy.data.objects.remove(old)
    mid = (VINES[0] + VINES[1]) / 2
    bm = None
    for a, b in boxes:
        if b.x - a.x > 0.5:                                         # thanh ngang trên đỉnh tường đứng yên
            bm = box_bm(b - a, (a + b) / 2, bm=bm)
    add_obj("Vines_Bar", bm, vmat, "SET")
    halves = []
    for name, px, sel in (("L", VINES[0], lambda c: c < mid), ("R", VINES[1], lambda c: c >= mid)):
        piv = empty("Vines_" + name, "SET", loc=(px, WALL_Y[0] - 0.08, WALL_TOP + 0.05))
        bm = None
        for a, b in boxes:
            c = (a + b) / 2
            if b.x - a.x <= 0.5 and sel(c.x):
                bm = box_bm(b - a, c - piv.location, bm=bm)
        add_obj("Vines_Strands" + name, bm, vmat, "SET", parent=piv)
        halves.append(piv)
    return SimpleNamespace(door=door, patch=patch, relief=relief, glow=glow, vines=halves)


# ================================================================ vòm đá
def build_vault():
    """Vòm đá ở VC: nền, hai tường bên, hai tường đầu (lỗ cửa vào, lỗ cánh cửa khắc mây), trần vòm cuốn, ô trần sáng,
    lối vào có ánh ngày, bệ đỡ trống, cánh cửa khắc mây hai cánh, ánh lấp lánh, khe sáng, đèn vùng."""
    stone = material("M_VaultStone", (0.6, 0.59, 0.57), 0.85)
    stone_d = material("M_VaultStoneDark", (0.45, 0.44, 0.42), 0.85)
    ped_m = material("M_PedStone", (0.5, 0.49, 0.47), 0.8)
    moss = material("M_MossCarpet", (0.3, 0.32, 0.28), 0.95)
    dark = material("M_DoorDark", (0.1, 0.095, 0.09), 0.9)
    sky = material("M_VaultSky", (0.75, 0.86, 0.98), 0.5, emit=((0.8, 0.9, 1.0), 1.5))
    day = material("M_VaultDaylight", (1.0, 0.95, 0.85), 0.5, emit=((1.0, 0.95, 0.82), 2.0))
    day_floor = material("M_DaylightPatch", (0.9, 0.86, 0.72), 0.8, emit=((1.0, 0.95, 0.8), 0.8))
    spark = material("M_DoorSparkle", (1.0, 0.8, 0.2), 0.3, emit=((1.0, 0.72, 0.12), 3.0))
    crack_m = material("M_DoorCrack", (1.0, 0.92, 0.6), 0.3, emit=((1.0, 0.9, 0.55), 3.0))
    T = 0.3                                                          # bề dày tường

    def top(x):
        return VH + math.sqrt(max(VR * VR - (x - VC) ** 2, 0.0))

    def end_wall(name, y0, y1, hole):
        """Tường đầu kín tới trần vòm, có lỗ cửa vòm (tâm x, rộng, cao), dựng bằng các dải đứng."""
        hx, hw, hh = hole
        hr = hw / 2
        hzs = hh - hr
        xs = sorted({round(VX0 + 0.1 * k, 4) for k in range(int((VX1 - VX0) / 0.1) + 1)} |
                    {round(hx - hr + hw * k / 16, 4) for k in range(17)})
        bm = None
        for xa, xb in zip(xs, xs[1:]):
            inside = hx - hr - 1e-6 <= (xa + xb) / 2 <= hx + hr + 1e-6

            def bot(x):
                return hzs + math.sqrt(max(hr * hr - (x - hx) ** 2, 0.0)) if inside else 0.0
            bm = prism([(xa, bot(xa)), (xb, bot(xb)), (xb, top(xb)), (xa, top(xa))], y0, y1, bm=bm)
        return add_obj(name, bm, stone, "SET")

    add_obj("Vault_Floor", box_bm((VX1 - VX0 + 2 * T, VY1 - VY0 + 1.6 + T, 0.1), (VC, (VY0 - 1.6 + VY1 + T) / 2, -0.05)), stone_d, "SET")
    bm = box_bm((T, VY1 - VY0 + 2 * T, VH + 0.05), (VX0 - T / 2, (VY0 + VY1) / 2, (VH + 0.05) / 2))
    bm = box_bm((T, VY1 - VY0 + 2 * T, VH + 0.05), (VX1 + T / 2, (VY0 + VY1) / 2, (VH + 0.05) / 2), bm=bm)
    add_obj("Vault_SideWalls", bm, stone, "SET")
    bm = None
    N = 16
    for k in range(N):
        a0, a1 = math.pi * k / N, math.pi * (k + 1) / N
        bm = prism([(VC + VR * math.cos(a0), VH + VR * math.sin(a0)), (VC + VR * math.cos(a1), VH + VR * math.sin(a1)),
                    (VC + (VR + T) * math.cos(a1), VH + (VR + T) * math.sin(a1)), (VC + (VR + T) * math.cos(a0), VH + (VR + T) * math.sin(a0))],
                   VY0 - T, VY1 + T, bm=bm)
    add_obj("Vault_Ceiling", bm, stone, "SET")
    bm = None
    for y in (VY0 + 1.0, 0.6, 2.2):                                    # gân vòm
        for k in range(N):
            a0, a1 = math.pi * k / N, math.pi * (k + 1) / N
            bm = prism([(VC + VR * math.cos(a0), VH + VR * math.sin(a0)), (VC + VR * math.cos(a1), VH + VR * math.sin(a1)),
                        (VC + (VR - 0.08) * math.cos(a1), VH + (VR - 0.08) * math.sin(a1)),
                        (VC + (VR - 0.08) * math.cos(a0), VH + (VR - 0.08) * math.sin(a0))], y - 0.12, y + 0.12, bm=bm)
    add_obj("Vault_Ribs", bm, stone_d, "SET")
    end_wall("Vault_WallNear", VY0 - T, VY0, (ENT_X, ENT_W, ENT_H))
    end_wall("Vault_WallFar", VY1, VY1 + T, (VC, CD_W, CD_H))
    for i, (a, y) in enumerate(((90, 0.6), (40, 2.0), (140, 2.0))):  # ô cửa tròn trên trần: trời sáng dịu
        r = math.radians(a)
        n = Vector((-math.cos(r), 0, -math.sin(r)))
        disc(f"Vault_Skylight{i}", (VC + (VR - 0.01) * math.cos(r), y, VH + (VR - 0.01) * math.sin(r)), n, 0.38 if i == 0 else 0.28, 0.01, sky, "SET")
    # trang trí: mặt la bàn sao hoa gió trên hai tường bên, mây khắc ở chân tường, rêu trên nền
    for i, x in enumerate((VX0 + 0.012, VX1 - 0.012)):
        s = 1 if i == 0 else -1
        disc(f"Vault_Rose{i}", (x, 1.6, 0.85), (s, 0, 0), 0.36, 0.024, stone_d, "SET")
        ob = add_obj(f"Vault_RoseStar{i}", prism(star_profile(0.3, 0.14), -0.012, 0.012), stone, "SET", loc=(x + s * 0.02, 1.6, 0.85))
        ob.rotation_euler = (0, 0, math.radians(90))
        bm = None
        for dy, dz, rr in ((-0.18, 0.0, 0.12), (0.0, 0.06, 0.15), (0.17, 0.0, 0.11)):
            bm = sphere_bm(rr, (0, dy, dz), (0.3, 1.0, 0.8), bm=bm, segs=16)
        add_obj(f"Vault_Cloud{i}", bm, stone_d, "SET", loc=(x, -0.6, 0.35))
    bm = None
    for x, y, rx, ry in ((38.5, -1.6, 0.4, 0.3), (41.5, 1.4, 0.35, 0.5), (38.4, 2.8, 0.35, 0.4), (41.4, -0.6, 0.3, 0.25), (VC, PED.y, 0.32, 0.32)):
        bm = sphere_bm(1.0, (x, y, 0.0), (rx, ry, 0.03), bm=bm, segs=16)
    add_obj("Vault_Moss", bm, moss, "SET")
    # lối vào: hai vách, mái, vách cuối sáng ánh ngày; vệt sáng trên nền trong vòm
    bm = box_bm((0.15, 1.3, ENT_H + 0.2), (ENT_X - ENT_W / 2 - 0.075, VY0 - T - 0.65, (ENT_H + 0.2) / 2))
    bm = box_bm((0.15, 1.3, ENT_H + 0.2), (ENT_X + ENT_W / 2 + 0.075, VY0 - T - 0.65, (ENT_H + 0.2) / 2), bm=bm)
    bm = box_bm((ENT_W + 0.3, 1.3, 0.1), (ENT_X, VY0 - T - 0.65, ENT_H + 0.05), bm=bm)
    add_obj("Vault_EntPassage", bm, dark, "SET")
    add_obj("Vault_EntDay", box_bm((ENT_W + 0.1, 0.05, ENT_H + 0.1), (ENT_X, VY0 - T - 1.3, (ENT_H + 0.1) / 2)), day, "SET")
    add_obj("Vault_EntPatch", box_bm((ENT_W - 0.05, 0.9, 0.004), (ENT_X, VY0 + 0.45, 0.002)), day_floor, "SET")
    # bệ đỡ trống: trụ đá tròn ngang ngực Lumo, mặt khắc hình la bàn có hốc tròn ở giữa, quanh thân khắc mây và sao
    bm = cyl_bm(PED_R, PED_H - 0.04, (0, 0, (PED_H - 0.04) / 2), segs=32)
    bm = cyl_bm(PED_R + 0.02, 0.04, (0, 0, PED_H - 0.02), bm=bm, segs=32)
    bm = cyl_bm(PED_R + 0.035, 0.05, (0, 0, 0.025), bm=bm, segs=32)
    add_obj("Pedestal", bm, ped_m, "SET", loc=PED)
    add_obj("Pedestal_Recess", cyl_bm(CR * 1.12, 0.004, (0, 0, PED_H + 0.001), segs=32), dark, "SET", loc=PED)
    ob = add_obj("Pedestal_Star", prism(star_profile(0.2, 0.13), -0.004, 0.004), stone_d, "SET", loc=PED + Vector((0, 0, PED_H)))
    ob.rotation_euler = (math.radians(90), 0, 0)
    for k in range(4):                                               # mây và sao quanh thân
        a = math.radians(45 + 90 * k)
        d = Vector((math.cos(a), math.sin(a), 0))
        bm = None
        for du, dz, rr in ((-0.06, 0.0, 0.05), (0.0, 0.025, 0.06), (0.06, 0.0, 0.045)):
            p = d * PED_R + Vector((-d.y, d.x, 0)) * du + Vector((0, 0, 0.12 + dz))
            bm = sphere_bm(rr, tuple(p), (1, 1, 0.75), bm=bm, segs=12)
        add_obj(f"Pedestal_Cloud{k}", bm, stone_d, "SET", loc=PED)
        ob = add_obj(f"Pedestal_Rose{k}", prism(star_profile(0.07, 0.035), -0.006, 0.006), stone_d, "SET",
                     loc=PED + d * (PED_R + 0.003) + Vector((0, 0, 0.29)))
        ob.rotation_euler = (0, 0, a + math.pi / 2)
    # cánh cửa khắc mây: khung vòm, hai cánh bản lề mép ngoài, mây khắc nổi; sau cửa là ánh sáng (lộ qua khe khi đẩy)
    r = CD_W / 2
    zs = CD_H - r
    bm = None
    for k in range(12):
        a0, a1 = math.pi * k / 12, math.pi * (k + 1) / 12
        bm = prism([(VC + r * math.cos(a0), zs + r * math.sin(a0)), (VC + r * math.cos(a1), zs + r * math.sin(a1)),
                    (VC + (r + 0.12) * math.cos(a1), zs + (r + 0.12) * math.sin(a1)), (VC + (r + 0.12) * math.cos(a0), zs + (r + 0.12) * math.sin(a0))],
                   VY1 - 0.06, VY1, bm=bm)
    for s in (-1, 1):
        bm = box_bm((0.12, 0.06, zs), (VC + s * (r + 0.06), VY1 - 0.03, zs / 2), bm=bm)
    add_obj("CloudDoor_Frame", bm, stone_d, "SET")
    add_obj("CloudDoor_Beyond", box_bm((CD_W, 0.05, CD_H), (VC, VY1 + 0.35, CD_H / 2)), day, "SET")
    leaves = []
    for s in (-1, 1):                                                # s = -1: cánh trái (bản lề ở VC - r)
        piv = empty(f"CloudDoor_Hinge{s:+d}", "SET", loc=(VC + s * r, VY1 + 0.04, 0.0))
        w = r - 0.004                                               # khe giữa hai cánh
        half = [(0.0, 0.0), (w, 0.0)] + [(min(r + r * math.cos(a), w), zs + r * math.sin(a))
                                         for a in (math.pi / 2 + math.pi / 2 * k / 10 for k in range(11))]   # nửa trái, gốc ở bản lề
        if s > 0:
            half = [(-x, z) for x, z in reversed(half)]
        add_obj(f"CloudDoor_Leaf{s:+d}", prism(half, -0.04, 0.04), stone, "SET", parent=piv)
        bm = None
        for cx, cz, cw in ((-0.3, 1.25, 0.42), (0.28, 1.0, 0.44), (-0.28, 0.7, 0.44), (0.3, 0.42, 0.4), (-0.3, 0.2, 0.36)):
            if (cx > 0) != (s > 0):
                continue
            for du, dz, rr in ((-0.3, -0.02, 0.32), (0.0, 0.08, 0.42), (0.3, -0.02, 0.3)):
                bm = sphere_bm(cw * rr, (cx + cw * du * 0.8 - s * r, -0.05, cz + cw * dz), (1.0, 0.25, 0.75), bm=bm, segs=14)
        add_obj(f"CloudDoor_Clouds{s:+d}", bm, stone_d, "SET", parent=piv)
        leaves.append((piv, s))
    glints = []
    for i, (cx, cz) in enumerate(((-0.42, 1.38), (0.15, 1.1), (-0.12, 0.78), (0.42, 0.5), (-0.38, 0.28), (0.1, 1.5))):
        bm = box_bm((0.13, 0.008, 0.026))
        bm = box_bm((0.026, 0.008, 0.13), bm=bm)
        ob = add_obj(f"CloudDoor_Glint{i}", bm, spark, "PROPS", loc=(VC + cx, VY1 - 0.1, cz))
        ob.rotation_euler = (0, math.radians(20 * i), 0)
        glints.append(ob)
    crack = add_obj("CloudDoor_Crack", box_bm((0.02, 0.01, CD_H - 0.25)), crack_m, "PROPS", loc=(VC, VY1 - 0.055, (CD_H - 0.25) / 2 + 0.03))
    # ánh sáng tản đều: đèn vùng dưới trần (trần kín, không luồng nắng), đèn nhẹ ở hai đầu
    for name, loc, size, energy in (("Vault_Fill", (VC, 0.4, 2.7), (3.2, 5.6), 60.0), ("Vault_FillFar", (VC, 2.7, 2.2), (2.5, 1.0), 12.0)):
        lt = bpy.data.objects.new(name, bpy.data.lights.new(name, "AREA"))
        COLS["SET"].objects.link(lt)
        lt.data.shape, lt.data.size, lt.data.size_y, lt.data.energy = "RECTANGLE", size[0], size[1], energy
        lt.location = loc
    return SimpleNamespace(leaves=leaves, glints=glints, crack=crack)


def build(timing, offset, seconds, out_blend, segment=None):
    """seconds: độ dài video render (số nguyên giây Seedance nhận); segment: độ dài đoạn trong cảnh. Từ segment tới
    seconds chỉ giữ cú máy cuối (diễn vẫn chạy tiếp), lúc dựng cắt bỏ."""
    segment = seconds if segment is None else segment
    tm = load_timing(ROOT / timing)
    start(tm.FPS, seconds, offset)
    T_END = tm.SECONDS
    S = {n: (a, b) for n, a, b in tm.SHOTS}
    scene = bpy.context.scene
    rnd = random.Random(3)

    # ============================================================ bối cảnh
    W = build_ruins()
    build_far_wall()
    X = ruins_extra()
    V = build_vault()
    prop_dark = material("M_PropDark", (0.12, 0.12, 0.13), 0.6)
    pebble_m = material("M_Pebble", (0.22, 0.21, 0.2), 0.8)
    gold_m = material("M_Compass_Gold", (1.0, 0.68, 0.12), 0.35, emit=((1.0, 0.65, 0.1), 0.3))
    glass_m = material("M_Compass_Glass", (0.06, 0.22, 0.75), 0.15, emit=((0.25, 0.55, 1.0), 0.6))
    point_m = material("M_Compass_Pointer", (1.0, 0.85, 0.15), 0.3, emit=((1.0, 0.78, 0.1), 2.5))
    star_m = material("M_Compass_Star", (0.85, 0.93, 1.0), 0.4, emit=((0.85, 0.93, 1.0), 0.4))
    gem_m = material("M_Compass_Gem", (0.1, 0.8, 1.0), 0.2, emit=((0.1, 0.8, 1.0), 1.5))

    def build_compass(name, parent=None, loc=(0, 0, 0)):
        """Như Cảnh 2: mặt la bàn = mặt XY cục bộ, pháp tuyến +Z; quai ở +Y. Mũi sao quay quanh Z, đầu chỉ dọc +Y."""
        root = empty(name, "PROPS", parent=parent, loc=loc)
        add_obj(name + "_Case", cyl_bm(CR, 0.032, segs=32), gold_m, "PROPS", parent=root)
        add_obj(name + "_Bail", box_bm((0.034, 0.03, 0.02), (0, CR + 0.01, 0)), gold_m, "PROPS", parent=root)
        add_obj(name + "_Glass", cyl_bm(CR * 0.82, 0.004, (0, 0, 0.016), segs=32), glass_m, "PROPS", parent=root)
        needle = empty(name + "_Needle", "PROPS", parent=root, loc=(0, 0, 0.02))
        bm = box_bm((0.016, 0.046, 0.006), (0, 0.023, 0))           # đầu chỉ: thân dài…
        n = len(bm.verts)
        bm = box_bm((0.017, 0.017, 0.006), (0, 0, 0), bm=bm)        # …mũi hình thoi
        bm.verts.ensure_lookup_table()
        for v in bm.verts[n:]:
            v.co = Matrix.Rotation(math.radians(45), 3, "Z") @ v.co + Vector((0, 0.05, 0))
        add_obj(name + "_Pointer", bm, point_m, "PROPS", parent=needle)
        add_obj(name + "_Gem", sphere_bm(0.008, (0, 0.058, 0.0), (1, 1, 0.45), segs=8), gem_m, "PROPS", parent=needle)
        bm = cyl_bm(0.011, 0.007, segs=12)                          # tâm sao
        for k in range(1, 8):                                       # bảy cánh ngắn
            n = len(bm.verts)
            bm = box_bm((0.009, 0.026, 0.004), (0, 0.016, 0), bm=bm)
            bm.verts.ensure_lookup_table()
            for v in bm.verts[n:]:
                v.co = Matrix.Rotation(math.radians(45 * k), 3, "Z") @ v.co
        add_obj(name + "_Star", bm, star_m, "PROPS", parent=needle)
        return SimpleNamespace(root=root, needle=needle)

    # ============================================================ Lumo, la bàn, hòn sỏi, mảnh rêu
    L = build_lumo(tuple(START))
    lumo = Act(L, START.x, START.y, START_YAW)
    bag = add_obj("Lumo_Bag", box_bm((0.1, 0.06, 0.09)), prop_dark, "CAST", parent=L.root, loc=(-0.2, -0.1, 0.3))
    hold = empty("Lumo_CompassHold", "PROPS", parent=L.root)        # la bàn cầm tay: vị trí, góc trong khung gốc của Lumo
    comp = build_compass("Compass", hold)
    pcomp = build_compass("PedCompass", loc=(PED.x, PED.y, PED_H + 0.008))   # la bàn đặt khớp vào hốc mặt bệ
    pcomp.root.rotation_euler = (0, 0, math.radians(-90))
    pebble = add_obj("Pebble", sphere_bm(0.045, scale=(1.0, 0.9, 0.8), segs=12), pebble_m, "PROPS")
    moss_bits = [add_obj(f"MossBit{i}", box_bm((0.06, 0.04, 0.012)), bpy.data.materials["M_MossCarpet"], "PROPS") for i in range(6)]

    for ob in (pebble, *moss_bits, pcomp.root, X.patch, *X.glow, *V.glints, V.crack):
        key(ob, "scale", -1.0, Vector((0, 0, 0)))                   # ẩn bằng scale 0 tới lúc xuất hiện

    def show(ob, t, on, s=1.0):
        key(ob, "scale", t - HOLD, Vector((s, s, s)) if not on else Vector((0, 0, 0)))
        key(ob, "scale", t, Vector((s, s, s)) if on else Vector((0, 0, 0)))

    def head(t, pitch=0.0, yaw=0.0, roll=0.0):
        rot(L.head, [(t, (pitch, roll, yaw))])

    def ears(t, a, b=None):
        for ear, side in L.ears:
            rot(ear, [(t, (a if side > 0 or b is None else b, 0, 0))])

    def tail(t, up, side=0.0):
        rot(L.tail, [(t, (up, 0, side))])

    def squash(t, sx, sz):
        key(L.root, "scale", t, Vector((sx, sx, sz)))

    def legs(t, a):
        for leg in L.legs:
            rot(leg, [(t, (a, 0, 0))])

    def pose(t, lean=None, yaw=None, roll=None):
        """lumo.pose, hướng chọn vòng gần nhất với hướng trước đó (không xoay vòng dài)."""
        if yaw is not None:
            yaw += 360 * round((lumo.yaw - yaw) / 360)
        lumo.pose(t, lean, yaw, roll)

    def go(t, p):
        lumo.go(t, p.x, p.z, p.y)

    def rootm():
        """Ma trận gốc Lumo theo trạng thái vừa key (gọi ngay sau lumo.go/pose ở cùng giây)."""
        return Matrix.Translation((lumo.x, lumo.y, lumo.z)) @ rmat(lumo.lean, lumo.yaw, lumo.roll).to_4x4()

    def local(p):
        return rootm().inverted() @ Vector(p)

    prev = {}

    def arm_to(side, t, p):
        """Chĩa tay (l: tay trái, phía +X cục bộ; r: tay phải) về điểm p trong khung gốc của Lumo."""
        arm = L.arm_l if side == "l" else L.arm_r
        d = (Vector(p) - SHOULDER[side]).normalized()
        e = Vector((0, 0, -1)).rotation_difference(d).to_euler("XYZ", prev.get(side, Euler()))
        prev[side] = e
        rot(arm, [(t, tuple(math.degrees(a) for a in e))])

    def touch(side, t, p):
        arm_to(side, t, local(p))

    def arms_down(t, a=6, sides="lr"):
        for side in sides:
            prev[side] = Euler((math.radians(a), 0, 0))
            rot(L.arm_l if side == "l" else L.arm_r, [(t, (a, 0, 0))])

    def grip(t, c, tilt=37, yaw=0.0, roll=0.0, hands="lr"):
        """La bàn ở c (khung gốc Lumo), mặt nghiêng tilt độ (0: ngửa, 90: dựng đứng quay ra trước); tay trong hands bám
        mép vỏ hai bên (tay đi theo la bàn)."""
        key(hold, "location", t, Vector(c))
        rot(hold, [(t, (tilt, roll, yaw))])
        m = Matrix.Translation(c) @ Euler([math.radians(a) for a in (tilt, roll, yaw)], "XYZ").to_matrix().to_4x4()
        for side in hands:
            arm_to(side, t, m @ Vector(((1 if side == "l" else -1) * (CR + 0.012), 0, 0)))

    CHEST = (0.0, -0.26, 0.45)                                      # la bàn ngang ngực, mặt ngửa chếch về trước
    ONE = (0.13, -0.25, 0.43)                                       # một tay phía máy cầm (như cuối Cảnh 2)
    HIP_R = (-0.27, -0.06, 0.29)                                    # tay xa, để bên hông
    LOOK_C = (0.0, -0.28, 0.64)                                     # cú nhìn: giơ la bàn trước mắt, mặt quay về mắt

    glass_e = bsdf_in(glass_m, "Emission Strength")

    def glass(t, v):
        glass_e.default_value = v
        glass_e.keyframe_insert("default_value", frame=fr(t))

    def beep(t, base, peak):
        glass(t - 0.05, base)
        glass(t, peak)
        glass(t + 0.16, base)

    def jitter(ob, t0, t1, amp, period):
        t = t0
        while t < t1:
            key(ob, "location", t, Vector(((rnd.random() - 0.5) * 2 * amp, (rnd.random() - 0.5) * 2 * amp, (rnd.random() - 0.5) * 2 * amp)))
            t += period
        key(ob, "location", t1, Vector((0, 0, 0)))

    # ============================================================ S1–S2: đi dọc bức tường, càng gần càng sáng, rung, kêu dày
    w0, w1 = tm.WALK_WALL
    sw = tm.SWAP_FAR
    v0, v1 = tm.PART_VINES
    PART_YAW, PART_LEAN = -112, 6
    VINE_HAND = Vector((-11.64, WALL_Y[0] - 0.17, -0.56))           # tay chạm nửa phải mảng dây leo, ngang vai (người đứng bên phải phù điêu)
    PART = stand_for({"l": VINE_HAND}, PART_YAW, PART_LEAN, LOW_Z, VINE_HAND)
    lumo.go(0.0, START.x, START.z, START.y)
    pose(0.0, lean=0, yaw=START_YAW, roll=0)
    head(0.0, 18, 0)
    ears(0.0, 8)
    tail(0.0, 25)
    grip(0.0, ONE, tilt=45, hands="l")
    arms_down(0.0, 6, "r")
    path = [(START.x, START.y), (-8.45, 0.92), (-8.45, 0.5), (-8.8, 0.12), (-9.8, 0.08), (-10.45, 0.3), (-11.0, 0.42), (PART.x, PART.y)]
    dist = [0.0]
    for a, b in zip(path, path[1:]):
        dist.append(dist[-1] + math.dist(a, b))
    for k, (x, y) in enumerate(path):
        t = w0 + (w1 - w0) * (dist[k] / dist[-1]) ** 0.85             # bước ngắn dần khi tới gần
        lumo.go(t, x, LOW_Z, y)
        if k:
            pose(t, lean=4, yaw=yaw_to(path[k - 1], (x, y)) if k < len(path) - 1 else PART_YAW)
        grip(t, CHEST)
    pose(w0, lean=0, yaw=START_YAW)
    grip(w0, CHEST)
    steps(L.legs, w0, w1, 12, 22)
    pose(w1, lean=0)
    wag(L.tail, w0, w1, 0.55, 18, base=(30, 0, 0))
    head(w0, 16, 0)                                                 # nhìn la bàn…
    head(w0 + 1.6, 2, 0)                                            # …ngẩng nhìn theo mũi sao về phía trước
    head(w0 + 2.6, 16, 0)
    head(tm.BEEPS_DENSE[0], 0, 0)
    ears(tm.BEEPS_DENSE[0], 18)
    head(tm.BEEPS_DENSE[0] + 1.2, 16, 0)
    ears(tm.BEEPS_DENSE[0] + 1.2, 10)
    head(w1, 2, 0)
    glass(0.0, 0.5)
    for t in tm.BEEPS_SPARSE:
        beep(t, 0.6, 1.4)
    dense = [tm.BEEPS_DENSE[0] + d for d in (0.0, 0.55, 1.0, 1.35, 1.65, 1.88, 2.08, 2.25, 2.4)]
    for i, t in enumerate(dense):                                   # sáng dần, kêu dày dần
        b = 0.8 + 0.8 * i / (len(dense) - 1)
        beep(t, b, b + 1.2)
    VIB1, VIB2 = tm.BEEPS_DENSE[0] - 0.8, tm.BEEPS_DENSE[0] + 1.0    # các nấc rung mạnh dần khi tới gần
    jitter(comp.root, 0.0, VIB1, 0.002, 0.07)
    jitter(comp.root, VIB1, VIB2, 0.004, 0.06)
    jitter(comp.root, VIB2, sw, 0.007, 0.05)

    # ============================================================ S3: chuyền la bàn sang tay xa, vạch dây leo, phù điêu ánh lên
    go(sw - 0.3, PART)
    pose(sw - 0.3, lean=0, yaw=PART_YAW)
    grip(sw - 0.3, CHEST)
    grip(sw, (-0.12, -0.2, 0.4), tilt=60)
    grip(sw + 0.25, HIP_R, tilt=80, yaw=-70, hands="r")            # la bàn ở tay xa, bên hông
    arms_down(sw + 0.25, -20, "l")
    pose(v0, lean=PART_LEAN)
    touch("l", v0, VINE_HAND)                                       # tay phía máy chạm giữa mảng dây leo…
    grip(v0, HIP_R, tilt=80, yaw=-70, hands="r")
    head(v0, 4, 0)
    ears(v0, 14)
    pose(v0 + 0.35, lean=PART_LEAN)
    touch("l", v0 + 0.35, VINE_HAND + Vector((0.08, -0.03, 0.02)))
    pose(v1, lean=2)
    touch("l", v1, Vector((-11.3, WALL_Y[0] - 0.35, -0.5)))          # …gạt sang bên
    for piv, a, sx in ((X.vines[0], 12, 0.3), (X.vines[1], -38, 0.45)):   # hai nửa dây leo dạt ra hai bên, không che cửa thấp
        rot(piv, [(v0 + 0.1, (0, 0, 0)), (v1, (0, a, 0)), (v1 + 0.25, (0, a * 0.9, 0))])
        keys(piv, "scale", [(v0 + 0.1, Vector((1, 1, 1))), (v1, Vector((sx, 1, 1)))])
    ro = tm.RELIEF_ON
    for ob in X.glow:                                               # các đường mây ánh lên
        show(ob, ro, True)
    squash(ro, 1, 1)
    squash(ro + 0.12, 0.96, 1.05)
    squash(ro + 0.3, 1, 1)
    ears(ro + 0.05, 24)
    ears(ro + 0.3, 12)
    head(ro + 0.1, -2, 0)
    arms_down(ro + 0.4, -10, "l")
    for t in (sw + 0.4 + 0.32 * k for k in range(int((tm.DOOR_OPEN[0] - sw - 0.4) / 0.32) + 1)):   # sát phù điêu: sáng mạnh, kêu dày
        beep(t, 1.6, 2.8)
    jitter(comp.root, sw + 0.3, tm.TUMBLE[0], 0.007, 0.05)

    # ============================================================ S4: thử ấn, thử kéo
    p0, p1 = tm.PRESS
    PRESS_P = Vector((-11.72, RELIEF.y - 0.08, RELIEF.z + 0.04))    # mặt phù điêu, nửa phải, ngang ngực
    REL_YAW = -122
    PR = stand_for({"l": PRESS_P}, REL_YAW, 6, LOW_Z, PRESS_P)
    go(p0 - 0.3, PART)
    pose(p0 - 0.3, lean=0, yaw=PART_YAW)
    go(p0, PR + facing(REL_YAW) * -0.04)
    pose(p0, lean=0, yaw=REL_YAW)
    touch("l", p0, PRESS_P + Vector((0.05, -0.08, 0.02)))
    go(p0 + 0.25, PR)
    pose(p0 + 0.25, lean=6)
    touch("l", p0 + 0.25, PRESS_P)                                  # ấn vào
    go(p0 + 0.45, PR + facing(REL_YAW) * -0.03)
    pose(p0 + 0.45, lean=3)
    touch("l", p0 + 0.45, PRESS_P + Vector((0.01, -0.03, 0)))
    go(p0 + 0.6, PR)
    pose(p0 + 0.6, lean=6)
    touch("l", p0 + 0.6, PRESS_P)                                   # ấn thêm lần nữa
    go(p1, PR)
    pose(p1, lean=6)
    touch("l", p1, PRESS_P)
    head(p0, 4, 0)
    n0, n1 = tm.PRESS_NOTHING
    pose(n0 + 0.1, lean=0)
    arms_down(n0 + 0.1, -8, "l")
    ears(n0, -8)
    squash(n0 + 0.2, 1, 1)
    squash(n0 + 0.32, 0.98, 1.04)                                   # nhún vai
    squash(n0 + 0.5, 1, 1)
    head(n0 + 0.3, 10, 25, -10)                                     # ngó quanh: không có gì
    head(n1, 2, 0)
    k0, k1 = tm.PULL
    PULL_P = Vector((-11.6, RELIEF.y - 0.06, RELIEF.z - 0.02))      # bám mép phải phù điêu
    pulls = [(k0, -2)] + [(t, -14 if i % 2 else -6) for i, t in enumerate(k0 + 0.3 + 0.25 * j for j in range(int((k1 - k0 - 0.3) / 0.25) + 1))]
    go(k0 - 0.2, PR)
    pose(k0 - 0.2, lean=0)
    for t, ln in pulls:                                             # kéo giật giật: tay vẫn bám mép phù điêu, người ngả ra
        go(t, stand_for({"l": PULL_P}, REL_YAW + 8, ln, LOW_Z, PULL_P))
        pose(t, lean=ln, yaw=REL_YAW + 8)
        touch("l", t, PULL_P)
    ears(k0 + 0.1, -22)
    head(k0 + 0.1, 0, 0)
    m0, m1 = tm.PULL_NOTHING
    go(m0, PR + facing(REL_YAW) * -0.12)
    pose(m0, lean=0, yaw=REL_YAW)
    arms_down(m0, -10, "l")
    ears(m0, -18)
    head(m0 + 0.2, 6, 0, 14)                                        # nghiêng đầu nhìn phù điêu

    # ============================================================ S5: lấy đà đẩy, phù điêu xoay, ngã lăn ra thảm rêu, cửa thấp mở
    u0, u1 = tm.RUNUP
    RUN = PR + facing(REL_YAW) * -0.6                               # lùi lại hai bước
    go(u0, PR + facing(REL_YAW) * -0.12)
    go(u0 + 0.4, PR + facing(REL_YAW) * -0.36 + Vector((0, 0, 0.03)))
    go(u1, RUN)
    steps(L.legs, u0, u1, 2, 20)
    head(u0, 0, 0)
    ears(u0, -32)                                                   # tai ép ra sau, quyết tâm
    squash(u1 - 0.1, 1, 1)
    squash(u1, 1.07, 0.9)                                           # khom người lấy đà
    pose(u1, lean=12)
    arms_down(u1, -25, "l")
    pu0, pu1 = tm.PUSH
    PUSH_P = Vector((-11.74, RELIEF.y - 0.08, RELIEF.z))
    PU = stand_for({"l": PUSH_P}, REL_YAW, 14, LOW_Z, PUSH_P)
    squash(pu0, 0.96, 1.04)
    go(pu0, RUN)
    go(pu0 + 0.2, (RUN + PU) / 2 + Vector((0, 0, 0.05)))
    go(pu1, PU)
    pose(pu1, lean=14)
    steps(L.legs, pu0, pu1, 2, 30)
    arms_down(pu0 + 0.15, -90, "l")
    touch("l", pu1, PUSH_P)
    squash(pu1, 1, 1)
    rt0, rt1 = tm.RELIEF_TURN                                       # phù điêu đột nhiên xoay nhẹ (quanh trục vuông góc mặt tường)
    rot(X.relief, [(rt0, (0, 0, 0)), (rt1, (0, 25, 0)), (rt1 + 0.08, (0, 22, 0)), (rt1 + 0.16, (0, 25, 0))])
    # mất thăng bằng, chúi sang trái theo phù điêu, lộn một vòng trên thảm rêu, ngồi bệt
    tm0, tm1 = tm.TUMBLE
    ROLL_YAW = yaw_to((PU.x, PU.y), (SIT.x, SIT.y))
    H_C = 0.42                                                      # tâm người cao 0.42 trên gốc: lộn quanh tâm
    ears(tm0 + 0.05, 26)
    pose(tm0 + 0.05, lean=14)
    go(tm0 + 0.05, PU)
    c0 = PU + facing(ROLL_YAW) * 0.25 + Vector((0, 0, H_C - 0.04))
    c1 = Vector((SIT.x, SIT.y, MOSS_TOP + 0.32))
    for k in range(14):
        u = k / 13
        t = tm0 + 0.2 + (tm1 - 0.25 - tm0 - 0.2) * u
        ln = 42 + 318 * u
        c = c0.lerp(c1, u) + Vector((0, 0, 0.06 * math.sin(math.pi * u)))
        up = rmat(ln, ROLL_YAW) @ Vector((0, 0, 1))
        go(t, c - up * H_C)
        lumo.pose(t, ln, ROLL_YAW, 0)
    arms_down(tm0 + 0.2, -150, "l")
    legs(tm0 + 0.2, -40)
    legs(tm1 - 0.3, -60)
    head(tm0 + 0.3, 20, 0)
    t, i = tm0 + 0.3, 0
    while t < tm1 - 0.25:                                           # tai lật phật khi lộn
        ears(t, -60 if i % 2 else 10)
        t, i = t + 0.14, i + 1
    go(tm1 - 0.1, SIT + Vector((0, 0, 0.05)))
    lumo.pose(tm1 - 0.1, 360 - 18, ROLL_YAW, 0)
    go(tm1, SIT)                                                    # ngồi phịch xuống thảm rêu: PHỊCH
    lumo.pose(tm1, 360 - 10, ROLL_YAW, 0)
    legs(tm1, -82)                                                  # hai chân duỗi ra trước
    squash(tm1 - HOLD, 1, 1)
    squash(tm1, 1.1, 0.88)
    squash(tm1 + 0.2, 0.97, 1.03)
    squash(tm1 + 0.4, 1, 1)
    arms_down(tm1, -30, "l")
    ears(tm1, -40)
    ears(tm1 + 0.3, -10)
    head(tm1, 6, 0)
    lumo.pose(tm1 + 0.6, 350, ROLL_YAW, 0)                          # cùng tư thế, góc nghiêng về -10 (350 = -10)
    lumo.pose(tm1 + 0.6 + HOLD, -10, ROLL_YAW, 0)
    for i, ob in enumerate(moss_bits):                              # rêu tung lên
        pa = Vector((SIT.x - 0.1 + 0.05 * i, SIT.y + 0.1 - 0.04 * i, MOSS_TOP + 0.02))
        pb = Vector((SIT.x - 0.5 + 0.18 * i, SIT.y - 0.25 + 0.1 * (i % 3), MOSS_TOP + 0.01))
        show(ob, tm1, True)
        for k in range(5):
            u = k / 4
            key(ob, "location", tm1 + 0.6 * u, pa.lerp(pb, u) + Vector((0, 0, 0.22 * math.sin(math.pi * u))))
            rot(ob, [(tm1 + 0.6 * u, (200 * u, 0, 90 * u))])
        show(ob, tm1 + 1.0, False)
    # cửa thấp mở ra (cánh đá xoay vào trong), ánh sáng ban ngày lọt vào; phù điêu tắt; Lumo quay vào tường nhìn cửa
    d0, d1 = tm.DOOR_OPEN
    rot(X.door, [(d0, (0, 0, 0)), (d0 + 0.15, (0, 0, 2)), (d0 + 0.3, (0, 0, 0)), (d1, (0, 0, 85))])
    show(X.patch, d0 + 0.35, True)
    key(X.patch, "scale", d1, Vector((1, 1, 1)))
    head(d0 + 0.1, -4, -55)                                         # quay phắt đầu về phía cửa
    ears(d0 + 0.1, 22)
    squash(d0 + 0.1, 0.96, 1.05)
    squash(d0 + 0.3, 1, 1)
    for ob in X.glow:
        show(ob, tm.RELIEF_OFF, False)
    lumo.pose(d1 + 0.2, -10, ROLL_YAW, 0)
    pose(tm.RELIEF_OFF + 0.6, lean=-8, yaw=-140)                    # xoay người trên thảm rêu, mặt vào tường
    head(tm.RELIEF_OFF + 0.6, 0, -25)
    pose(S["S6"][0] - 0.2, lean=-6, yaw=SIT_YAW)
    head(S["S6"][0] - 0.2, 4, 0)
    ears(d1 + 0.3, 12)

    # ============================================================ S6: cú nhìn la bàn: dịu đi, rung khẽ, mũi sao quay vào cửa thấp
    i0, i1 = S["S6"]
    grip(tm1, HIP_R, tilt=80, yaw=-70, hands="r")
    grip(tm.RELIEF_OFF + 0.6, (-0.05, -0.27, 0.45), tilt=30)       # đưa la bàn lên, hai tay
    grip(i0 - 0.2, LOOK_C, tilt=-48)
    beep(i0, 2.4, 2.8)
    glass(tm.COMPASS_DIM, 2.0)
    glass(tm.COMPASS_DIM + 0.5, 0.5)                                # dịu đi, còn le lói
    for t in tm.BEEPS_INSERT:
        beep(t, 0.5, 1.2)
    jitter(comp.root, tm.TUMBLE[0], tm.COMPASS_DIM + 0.4, 0.006, 0.05)
    jitter(comp.root, tm.COMPASS_DIM + 0.4, i1, 0.002, 0.07)        # rung khẽ
    nt0, nt1 = tm.NEEDLE_TO_DOOR
    ears(nt1 + 0.1, 20)
    ears(nt1 + 0.4, 10)

    # ============================================================ S7: "Mình tìm được rồi!", bước vào cửa thấp
    c7 = S["S7"][0]
    g0, g1 = tm.GET_UP
    LINE_YAW = -80
    go(g0, SIT)
    pose(g0, lean=-6, yaw=SIT_YAW)
    legs(g0, -82)
    squash(g0, 1.06, 0.92)
    go(g0 + 0.2, Vector((SIT.x, SIT.y, LOW_Z + 0.12)))              # bật dậy
    pose(g0 + 0.2, lean=6, yaw=-120)
    legs(g0 + 0.2, -20)
    squash(g0 + 0.2, 0.95, 1.06)
    go(g1, Vector((SIT.x, SIT.y, LOW_Z)))
    pose(g1, lean=0, yaw=LINE_YAW)
    legs(g1, 0)
    squash(g1, 1, 1)
    grip(g0, LOOK_C, tilt=-48)
    grip(g1, CHEST)
    head(g0, 4, 0)
    head(g1, 6, 0)
    ears(g0 + 0.15, 22)
    ears(g1, 10)
    o0, o1 = tm.LUMO_LINE1
    grip(o0, CHEST)
    grip(o0 + 0.3, (0.0, -0.3, 0.52), tilt=50)                      # chìa la bàn ra trước, ngang ngực
    squash(o0 + 0.1, 1.06, 0.92)                                    # lấy đà
    squash(o0 + 0.25, 0.94, 1.08)
    go(o0 + 0.1, Vector((SIT.x, SIT.y, LOW_Z)))
    go(o0 + 0.45, Vector((SIT.x, SIT.y, LOW_Z + 0.26)))             # nhảy cẫng
    go(o0 + 0.8, Vector((SIT.x, SIT.y, LOW_Z)))
    squash(o0 + 0.8, 1.06, 0.93)
    squash(o0 + 1.0, 1, 1)
    legs(o0 + 0.45, -15)
    legs(o0 + 0.8, 0)
    ears(o0 + 0.4, 28)
    ears(o0 + 0.9, 12)
    head(o0, -6, 0)
    head(o1, 8, 0)
    grip(o1 + 0.1, CHEST)
    wag(L.tail, g1, tm.INTO_DOOR[1], 0.3, 25, base=(40, 0, 0))
    e0, e1 = tm.INTO_DOOR
    into = [(e0, SIT.x, SIT.y), (e0 + 0.45, -12.98, 0.33), (e0 + 0.85, DOOR_X, 0.75), (e1, DOOR_X, 1.55)]
    for k, (t, x, y) in enumerate(into):
        lumo.go(t, x, LOW_Z, y)
        if k:
            pose(t, lean=6, yaw=yaw_to(into[k - 1][1:], (x, y)))
        grip(t, CHEST)
    pose(e0, lean=0, yaw=LINE_YAW)
    steps(L.legs, e0, e1, 4, 25)
    squash(e0 + 0.6, 1, 1)
    squash(e0 + 0.85, 0.97, 0.94)                                   # khom vào cửa thấp
    head(e0, 4, 0)
    glass(c7, 0.6)
    for t in (c7 + 0.6, c7 + 1.7, c7 + 2.8):
        beep(t, 0.6, 1.4)
    jitter(comp.root, i1, S["S8"][0], 0.002, 0.07)

    # ============================================================ S8: vào vòm đá, bệ đỡ trống, khựng lại, cụp tai
    c8 = S["S8"][0]
    PRESS_LEAN, PED_YAW = 22, -90
    top_c = Vector((PED.x, PED.y, PED_H + 0.008))
    lat = lateral(PED_YAW) * (CR + 0.012)
    STAND = stand_for({"l": top_c + lat, "r": top_c - lat}, PED_YAW, PRESS_LEAN, 0.0, top_c)   # đứng bên phải bệ, vừa tầm tay
    go(c8 - HOLD, Vector((DOOR_X, 1.55, LOW_Z)))
    squash(c8 - HOLD, 0.97, 0.94)
    squash(c8, 1, 1)
    en0, en1 = tm.ENTER_VAULT
    vpath = [(c8, ENT_X, VY0 - 0.9), (en0, ENT_X, VY0 - 0.75), (en0 + 0.6, ENT_X, VY0 + 0.1), (en0 + 1.3, 40.75, -1.0),
             (en0 + 1.9, STAND.x + 0.12, STAND.y - 0.45), (en1, STAND.x, STAND.y)]
    for k, (t, x, y) in enumerate(vpath):
        lumo.go(t, x, 0.0, y)
        if k == 0:
            lumo.pose(c8 - HOLD, 0, -180, 0)
            lumo.pose(t, 0, -180, 0)
        elif k < len(vpath) - 1:
            pose(t, lean=4, yaw=yaw_to(vpath[k - 1][1:], (x, y)))
        grip(t, CHEST)
    pose(en1, lean=0, yaw=PED_YAW)
    steps(L.legs, en0 + 0.1, en1, 6, 22)
    head(c8, 2, 0)
    head(en0 + 0.8, -12, 30)                                        # ngước nhìn quanh vòm
    head(en0 + 1.5, 10, 0)                                          # nhìn bệ đỡ
    ears(en0 + 0.5, 16)
    wag(L.tail, en0, en1, 0.4, 22, base=(35, 0, 0))
    se = tm.SEE_EMPTY
    head(se, 26, 0)                                                 # nhìn bệ trống, khựng lại
    squash(se - 0.1, 1, 1)
    squash(se + 0.08, 0.97, 1.03)
    squash(se + 0.25, 1, 1)
    ed = tm.EARS_DOWN1
    ears(ed - 0.05, 10)
    ears(ed + 0.25, -62)                                            # cụp tai
    squash(ed, 1, 1)
    squash(ed + 0.25, 1.04, 0.94)                                   # thân xệ xuống
    tail(ed + 0.25, -20)
    grip(ed, CHEST)
    grip(ed + 0.25, (0.0, -0.22, 0.38), tilt=45)
    head(ed + 0.25, 22, 0)
    for t in (en0 + 0.4, en0 + 1.6):
        beep(t, 0.6, 1.4)
    jitter(comp.root, c8, tm.PED_PRESS[0], 0.002, 0.07)

    # ============================================================ S9: ấn la bàn vào bệ; gõ bệ, chờ sỏi, thở phào, PLOP; nhìn bệ, nhìn la bàn
    pp0, pp1 = tm.PED_PRESS
    squash(pp0, 1, 1)
    ears(pp0 - 0.2, -55)
    ears(pp0 + 0.3, -18)
    pose(pp0, lean=0)
    grip(pp0, (0.0, -0.22, 0.38), tilt=45)
    pose(pp0 + 0.35, lean=PRESS_LEAN)
    grip(pp0 + 0.35, local(top_c + Vector((0, 0, 0.04))), tilt=-PRESS_LEAN, yaw=0)   # đưa la bàn xuống, nằm ngang trên hốc
    pose(pp0 + 0.45, lean=PRESS_LEAN)
    grip(pp0 + 0.45, local(top_c), tilt=-PRESS_LEAN, yaw=0)
    show(comp.root, pp0 + 0.45, False)                              # la bàn khớp vào hốc mặt bệ
    show(pcomp.root, pp0 + 0.45, True)
    head(pp0 + 0.35, 24, 0)
    for t, dz in ((pp0 + 0.6, -0.012), (pp0 + 0.75, 0.0), (pp1, 0.0)):   # ấn khớp vào
        pose(t, lean=PRESS_LEAN + (3 if dz else 0))
        for side, s in (("l", 1), ("r", -1)):
            touch(side, t, top_c + lat * s + Vector((0, 0, dz)))
    no0, no1 = tm.PED_NOTHING
    pose(no0 + 0.1, lean=6)
    arms_down(no0 + 0.15, -10)
    head(no0, 0, 30)                                                # chờ, nhìn quanh: không có gì
    head(no0 + 0.45, -8, -25)
    head(no1, 20, 0)
    squash(no0 + 0.3, 1, 1)
    squash(no0 + 0.42, 0.98, 1.04)
    squash(no0 + 0.6, 1, 1)
    # gõ lên mặt bệ: TOK. TOK. TOK. (tay phía máy, mép bệ gần Lumo)
    bpy.context.scene.frame_set(fr(no1))
    sh_l = rootm() @ SHOULDER["l"]
    tgt = min((abs((sh_l - p).length - ARM), tuple(p)) for p in
              (Vector((PED.x + u, PED.y - 0.08, PED_H + 0.01)) for u in [k * 0.01 for k in range(-5, 21)]))[1]
    KNOCK_P = Vector(tgt)
    pose(tm.PED_KNOCKS[0] - 0.3, lean=6)
    for k in tm.PED_KNOCKS:
        touch("l", k - 0.18, KNOCK_P + Vector((0.03, -0.02, 0.14)))   # vung tay lên rồi gõ xuống
        touch("l", k, KNOCK_P)
        touch("l", k + 0.12, KNOCK_P + Vector((0.01, 0, 0.05)))
        head(k, 22, 0)
    ears(tm.PED_KNOCKS[0], -10)
    # cụp tai, ngước nhìn trần, chờ hòn sỏi
    wp0, wp1 = tm.WAIT_PEBBLE
    arms_down(wp0, 6, "l")
    pose(wp0, lean=0)
    ears(wp0, -10)
    ears(wp0 + 0.2, -55)
    head(wp0 + 0.25, -28, 0)                                        # ngước nhìn trần
    squash(wp0, 1, 1)
    squash(wp0 + 0.2, 1.03, 0.96)                                   # rụt cổ chờ
    head(wp0 + 1.2, -28, 18)
    head(wp1 - 0.2, -28, -8)
    s0, s1 = tm.RELIEF_SIGH                                         # không có gì: thở phào, hai tai dựng lên
    squash(s0, 1.03, 0.96)
    squash(s0 + 0.3, 0.97, 1.03)
    squash(s1, 1, 1)
    head(s0 + 0.2, 4, 0)
    ears(s0 + 0.15, -20)
    ears(s1, 16)
    head(s1, 0, 0)
    # PLOP! hòn sỏi rơi từ trần trúng đỉnh đầu (đo đỉnh đầu thật ở khung PLOP), nảy ra, lăn trên nền
    pl = tm.PLOP
    pr0, pr1 = tm.PLOP_REACT
    head(pl - HOLD, 0, 0)
    head(pl + 0.08, 12, 0)
    squash(pl, 1, 1)
    squash(pl + 0.08, 1.07, 0.9)
    squash(pl + 0.28, 1, 1)
    bpy.context.scene.frame_set(fr(pl))
    topp = L.head.matrix_world @ Vector((0, -0.02, 0.33))
    ceil_z = VH + math.sqrt(VR * VR - (topp.x - VC) ** 2) - 0.05
    fall = math.sqrt(2 * (ceil_z - topp.z) / 9.8)
    for k in range(6):
        u = k / 5
        key(pebble, "location", pl - fall * (1 - u), Vector((topp.x, topp.y, ceil_z - (ceil_z - topp.z) * u * u)))
    for t, d in ((pl + 0.08, (0, 0, 0.01)), (pl + 0.25, (0.18, -0.1, 0.16)), (pl + 0.5, (0.36, -0.22, -topp.z + 0.04)),
                 (pl + 0.65, (0.42, -0.26, -topp.z + 0.1)), (pl + 0.8, (0.47, -0.29, -topp.z + 0.04)), (pl + 1.2, (0.6, -0.36, -topp.z + 0.04))):
        key(pebble, "location", t, topp + Vector(d))
    rot(pebble, [(pl - fall, (0, 0, 0)), (pl + 1.2, (0, 600, 0))])
    show(pebble, pl - fall, True)
    show(pebble, pl + 1.6, False)
    ears(pl - HOLD, 16)
    ears(pl + 0.05, 30)
    ears(pl + 0.25, -55)                                            # cụp tai, nhắm tịt mắt
    tail(pl + 0.25, -15)
    head(pr1, 8, 0)
    # nhấc la bàn lên, nhìn bệ trống, rồi nhìn la bàn trong tay, nghiêng đầu
    l0, l1 = tm.LIFT_COMPASS
    pose(l0 - 0.25, lean=0)
    pose(l0, lean=PRESS_LEAN)
    for side, s in (("l", 1), ("r", -1)):
        touch(side, l0, top_c + lat * s)
    grip(l0, local(top_c), tilt=-PRESS_LEAN, yaw=0, hands="")
    show(pcomp.root, l0 + 0.05, False)
    show(comp.root, l0 + 0.05, True)
    head(l0, 24, 0)
    pose(l1, lean=0)
    grip(l1, CHEST)
    head(tm.LOOK_PED, 28, 15)                                       # nhìn bệ trống
    head(tm.LOOK_COMPASS, 18, 0)                                    # nhìn la bàn trong tay
    head(tm.HEAD_TILT, 16, 0, -16)                                  # nghiêng đầu
    ears(tm.HEAD_TILT, -8, -22)
    grip(tm.HEAD_TILT, CHEST)
    jitter(comp.root, l1, tm.TO_DOOR[0], 0.002, 0.07)

    # ============================================================ S10: quay lưng về phía cánh cửa, liếc la bàn
    ta0, ta1 = tm.TURN_AWAY
    STAND2 = Vector((PED.x + 0.5, PED.y - 0.15, 0.0))               # bước ra khỏi bệ, có chỗ để xoay
    AWAY = yaw_to((CLOUD_DOOR.x, CLOUD_DOOR.y), (2 * STAND2.x - CLOUD_DOOR.x, 2 * STAND2.y - CLOUD_DOOR.y))
    go(ta0, STAND)
    pose(ta0, lean=0, yaw=PED_YAW)
    go((ta0 + ta1) / 2, (STAND + STAND2) / 2 + Vector((0, 0, 0.04)))
    go(ta1, STAND2)
    pose(ta1, lean=0, yaw=AWAY)
    grip(ta1, CHEST)
    head(ta1, 4, 0)
    ears(ta1, 2)
    tail(ta1, 15)
    gl = tm.GLANCE
    head(gl, 20, 0)                                                 # liếc la bàn
    ears(gl + 0.2, -6)
    for t in (ta1 + 0.3, gl + 0.5):
        beep(t, 0.6, 1.4)

    # ============================================================ S11: cận la bàn, cánh cửa ở hậu cảnh: xoay trái, xoay phải, hai vòng
    c11, e11 = S["S11"]
    ddir = (Vector((CLOUD_DOOR.x, CLOUD_DOOR.y, 0)) - Vector((STAND2.x, STAND2.y, 0))).normalized()
    cdir = Matrix.Rotation(math.radians(35), 3, "Z") @ -ddir         # máy chếch 35° khỏi trục Lumo–cánh cửa, về phía +X, thấp ngang
    COMP11 = STAND2 + facing(AWAY) * 0.26 + Vector((0, 0, 0.45))     # la bàn: thấy la bàn ở cả hai hướng xoay, cánh cửa vẫn trong khung
    CAM11 = COMP11 + cdir * 0.65 + Vector((0, 0, 0.15))

    def toward_cam(t, yaw):
        """Lumo quay lưng về máy S11: một tay giơ la bàn ra bên phía máy, ngang vai, mặt la bàn xoay về máy (để trước
        ngực thì thân và tay che kín)."""
        cl = rmat(0, yaw).inverted() @ (CAM11 - STAND2)
        sx = 1 if cl.x > 0 else -1
        grip(t, (sx * 0.33, -0.08, 0.58), tilt=80, yaw=sx * 125, hands="l" if sx > 0 else "r")
        arms_down(t, 6, "r" if sx > 0 else "l")

    grip(c11, CHEST)
    head(c11, 18, 0)
    head(c11 + 0.6, 6, 70)                                          # liếc ra sau lưng theo mũi sao
    head(tm.SPIN_LEFT - 0.3, 18, 0)
    for t in (c11 + 0.5, c11 + 1.4):
        beep(t, 0.6, 1.4)
    sl, sr = tm.SPIN_LEFT, tm.SPIN_RIGHT
    lumo.pose(sl, 0, AWAY, 0)
    grip(sl, CHEST)
    lumo.pose(sl + 0.12, 0, AWAY + 195, 0)                          # xoay phắt sang trái, quay mặt về cánh cửa
    lumo.pose(sl + 0.22, 0, AWAY + 180, 0)
    toward_cam(sl + 0.2, AWAY + 180)
    head(sl + 0.12, 18, 0)
    ears(sl, 26)
    ears(sl + 0.25, 8)
    lumo.pose(sr, 0, AWAY + 180, 0)
    toward_cam(sr, AWAY + 180)
    lumo.pose(sr + 0.12, 0, AWAY - 15, 0)                           # xoay phắt sang phải, quay lưng lại
    lumo.pose(sr + 0.22, 0, AWAY, 0)
    grip(sr + 0.2, CHEST)
    ears(sr, 26)
    ears(sr + 0.25, 8)
    sp0, sp1 = tm.SPINS
    yaw = AWAY
    for g0 in (sp0, sp0 + 1.05):                                    # một vòng, ngừng nhìn la bàn, thêm vòng nữa
        lumo.pose(g0, 0, yaw, 0)
        grip(g0, CHEST)
        for q in range(1, 5):
            lumo.pose(g0 + 0.125 * q, 0, yaw + 90 * q, 0)
        yaw += 360
        grip(g0 + 0.5, CHEST)
        lumo.go(g0, STAND2.x, 0.0, STAND2.y)
        lumo.go(g0 + 0.25, STAND2.x, 0.05, STAND2.y)
        lumo.go(g0 + 0.5, STAND2.x, 0.0, STAND2.y)
        t, i = g0, 0
        while t < g0 + 0.5:
            ears(t, -40 if i % 2 else 30)
            t, i = t + 0.1, i + 1
        ears(g0 + 0.55, 10)
    head(sp0 + 0.55, 20, 0)                                         # giữa hai vòng: liếc la bàn, mũi sao vẫn chỉ cửa
    lumo.pose(sp1, 0, yaw, 0)
    for t in (sp0 + 0.6, sp1 - 0.2):
        beep(t, 0.6, 1.4)

    # ============================================================ S12: chóng mặt, loạng choạng, hai tai lắc lư
    dz0, dz1 = tm.DIZZY
    t, i = dz0, 0
    while t < dz1:
        lumo.pose(t, 8 if i % 2 else -6, yaw + (10 if i % 2 else -10), 9 if i % 2 else -9)
        lumo.go(t, STAND2.x + (0.05 if i % 2 else -0.05), 0.0, STAND2.y + (0.02 if i % 2 else -0.02))
        ears(t, -35, 25) if i % 2 else ears(t, 25, -35)
        head(t, 10, 14 if i % 2 else -14, -12 if i % 2 else 12)
        t, i = t + 0.3, i + 1
    lumo.pose(dz1 + 0.2, 0, yaw, 0)
    lumo.go(dz1 + 0.2, STAND2.x, 0.0, STAND2.y)
    head(dz1 + 0.2, 6, 0)
    ears(dz1 + 0.2, 6)
    grip(dz1 + 0.2, CHEST)

    # ============================================================ S13: bước về phía cánh cửa, sáng thêm, rung mạnh dần; mây lấp lánh
    td0, td1 = tm.TO_DOOR
    DOOR_STOP = Vector((VC + 0.25, VY1 - 1.05, 0.0))               # dừng cách cửa vài bước để còn chạy tới
    DOOR_YAW = yaw_to((DOOR_STOP.x, DOOR_STOP.y), (CLOUD_DOOR.x, CLOUD_DOOR.y))
    pose(td0, lean=0, yaw=DOOR_YAW)
    head(td0, 12, 0)
    xs = [STAND2.lerp(DOOR_STOP, k / 6) for k in range(7)]
    for k, p in enumerate(xs):
        t = td0 + 0.15 + (td1 - td0 - 0.15) * k / 6
        lumo.go(t, p.x, 0.03 if k % 2 else 0.0, p.y)                # mỗi bước một nhịp
        grip(t, CHEST)
    steps(L.legs, td0 + 0.15, td1, 6, 22)
    wag(L.tail, td0, td1, 0.45, 20, base=(32, 0, 0))
    bd0, bd1 = tm.BEEPS_DOOR_DENSE
    beeps = [tm.BEEPS_DOOR[0], tm.BEEPS_DOOR[0] + 0.9] + [bd0 + (bd1 - bd0) * u for u in (0.0, 0.3, 0.52, 0.7, 0.85, 1.0)]
    for i, t in enumerate(beeps):
        b = 0.6 + 1.1 * i / (len(beeps) - 1)
        beep(t, b, b + 1.2)
    jitter(comp.root, td0, tm.BEEPS_DOOR[1], 0.003, 0.06)
    jitter(comp.root, tm.BEEPS_DOOR[1], tm.STOW[0], 0.007, 0.05)
    ds = tm.DOOR_SPARKLE
    for i, ob in enumerate(V.glints):                               # những hình mây trên cánh cửa lấp lánh
        t = ds + 0.12 * i
        show(ob, t, True, 0.5)
        k = 0
        while t < T_END + 1:
            key(ob, "scale", t, Vector((1.3, 1.3, 1.3)) if k % 2 else Vector((0.5, 0.5, 0.5)))
            t, k = t + 0.25 + 0.03 * i, k + 1
    head(ds, -4, 0)
    ears(ds, 20)

    # ============================================================ S14: "Khoan đã…", mắt sáng lên, "Cậu dẫn tới…", cất la bàn, đẩy cửa
    k0, k1 = tm.LUMO_LINE2
    TALK_YAW = DOOR_YAW + 40                                        # nói với la bàn, ba phần tư về máy
    pose(k0 - 0.3, lean=0, yaw=DOOR_YAW)
    pose(k0, lean=0, yaw=TALK_YAW)
    grip(k0, (0.0, -0.28, 0.5), tilt=45)
    head(k0, 20, 0)                                                 # nhìn la bàn
    head(k0 + 0.8, 18, 0, 8)                                        # "Khoan đã…"
    ears(k0 + 1.1, -12)                                             # "…cậu không dẫn tới kho báu."
    head(k1, 18, 0, -6)
    eo0, eo1 = tm.EYES_SHINE
    pose(eo0, yaw=DOOR_YAW + 15)
    head(eo0, -10, -10)                                             # nhìn cánh cửa lấp lánh
    ears(eo0 + 0.3, 22)
    squash(eo0 + 0.3, 1, 1)
    squash(eo0 + 0.45, 0.97, 1.04)
    squash(eo0 + 0.65, 1, 1)
    q0, q1 = tm.LUMO_LINE3
    pose(q0, yaw=TALK_YAW)
    head(q0, 18, 0)
    head(q0 + 1.7, -6, -15)
    grip(q0 + 1.6, (0.0, -0.28, 0.5), tilt=45)
    grip(q0 + 1.8, (0.0, -0.32, 0.56), tilt=60)                     # chìa la bàn về phía cánh cửa, ngang ngực
    pose(q0 + 1.8, yaw=DOOR_YAW + 10)
    lumo.go(q0 + 1.9, DOOR_STOP.x, 0.0, DOOR_STOP.y)
    lumo.go(q0 + 2.1, DOOR_STOP.x, 0.07, DOOR_STOP.y)
    lumo.go(q1, DOOR_STOP.x, 0.0, DOOR_STOP.y)
    ears(q1, 16)
    wag(L.tail, q0, tm.STOW[0], 0.3, 25, base=(45, 0, 0))
    st0, st1 = tm.STOW                                              # nhét la bàn vào túi da bên hông phải
    BAG_TOP = (-0.2, -0.1, 0.36)
    grip(st0, (0.0, -0.28, 0.5), tilt=45)
    grip(st0 + 0.3, (-0.2, -0.16, 0.46), tilt=90, yaw=90, hands="r")
    arms_down(st0 + 0.3, 6, "l")
    grip(st1 - 0.15, BAG_TOP, tilt=90, yaw=90, hands="r")
    key(comp.root, "scale", st0 + 0.3, Vector((1, 1, 1)))
    key(comp.root, "scale", st1 - 0.1, Vector((0, 0, 0)))           # lút vào túi
    head(st0, 26, 20)
    head(st1, 6, 0)
    rp0, rp1 = tm.RUN_PUSH
    RUN_END = rp0 + 0.7
    dc = Vector((CLOUD_DOOR.x, VY1 - 0.04, 0.62))
    PUSH_D = stand_for({"l": dc + lateral(180) * 0.15, "r": dc - lateral(180) * 0.15}, 180, 16, 0.0, dc)
    pose(rp0, lean=10, yaw=180)
    lumo.go(rp0, DOOR_STOP.x, 0.0, DOOR_STOP.y)
    for k in range(1, 4):                                           # chạy ba bước
        p = DOOR_STOP.lerp(PUSH_D, k / 3)
        lumo.go(rp0 + 0.7 * k / 3, p.x, 0.06 if k < 3 else 0.0, p.y)
    steps(L.legs, rp0, RUN_END, 3, 35)
    ears(rp0, -25)
    head(rp0, 0, 0)
    arms_down(rp0 + 0.2, -40)
    pose(RUN_END, lean=16, yaw=180)
    for side, s in (("l", 1), ("r", -1)):
        touch(side, RUN_END, dc + lateral(180) * 0.15 * s)
        touch(side, T_END + 1, dc + lateral(180) * 0.15 * s)
    pose(T_END + 1, lean=16, yaw=180)
    lumo.go(T_END + 1, PUSH_D.x, 0.0, PUSH_D.y)
    for piv, s in V.leaves:                                         # cánh cửa nhúc nhích dưới tay, hé vào trong
        rot(piv, [(RUN_END, (0, 0, 0)), (RUN_END + 0.12, (0, 0, -s * 1.5)), (RUN_END + 0.2, (0, 0, 0)), (T_END + 1, (0, 0, -s * 6))])
    show(V.crack, RUN_END + 0.1, True)                              # cánh cửa hé một khe sáng
    key(V.crack, "scale", T_END + 1, Vector((3.0, 1, 1)))

    # ============================================================ mũi sao: phù điêu → cửa thấp → cánh cửa khắc mây
    f_last = scene.frame_end

    def secs(f):
        return (f - 1 + round(blocks.T0 * blocks.FPS)) / blocks.FPS

    def door_glide(t):
        u = ss((t - nt0) / (nt1 - nt0))
        return RELIEF.lerp(DOOR_IN, u)

    def target(t):
        if t < nt0:
            return RELIEF
        if t < S["S8"][0]:
            return door_glide(t)
        return CLOUD_DOOR

    def buzz(t):
        amp = (1.0 if t < VIB1 else 2.0 if t < VIB2 else 3.5 if t < tm.TUMBLE[0] else 3.0 if t < tm.COMPASS_DIM else 1.0
               if t < tm.BEEPS_DOOR[1] else 2.5)
        return amp * math.sin(t * 2 * math.pi * 7.0)

    def aim(c):
        prev_a = None
        for f in range(1, f_last + 1):
            scene.frame_set(f)
            mw = c.root.matrix_world
            if mw.to_scale().length < 1e-3:
                continue
            t = secs(f)
            p = mw.inverted() @ target(t)
            a = math.degrees(math.atan2(-p.x, p.y))
            if prev_a is not None:
                a -= 360 * round((a - prev_a) / 360)
            prev_a = a
            c.needle.rotation_euler = (0, 0, math.radians(a + buzz(t)))
            c.needle.keyframe_insert("rotation_euler", frame=f)

    aim(comp)
    aim(pcomp)

    # ============================================================ cú nhìn của Lumo (S6): đầu ẩn, máy ở chỗ mắt
    end_t = offset + segment
    if offset - 1e-6 <= i0 < end_t - 1e-6:
        hide_to = i1 if i1 < end_t - 1e-6 else offset + seconds + 1   # cú cuối của đoạn: ẩn luôn qua phần đuôi
        key(L.head, "scale", i0 - HOLD, Vector((1, 1, 1)))
        key(L.head, "scale", i0, Vector((0, 0, 0)))
        key(L.head, "scale", hide_to - HOLD, Vector((0, 0, 0)))
        key(L.head, "scale", hide_to, Vector((1, 1, 1)))
    scene.frame_set(fr(i0 + 0.2))
    eye6 = L.root.matrix_world @ Vector((0, -0.04, 0.86))
    mid6 = Vector(((RELIEF.x + DOOR_X) / 2, WALL_Y[0], -0.75))
    look6 = eye6 + (comp.root.matrix_world.translation - eye6).normalized() * 0.5 + (mid6 - eye6).normalized() * 0.5

    # ============================================================ máy quay (một máy mỗi cú; chỉ dựng các cú trong đoạn)
    d11 = [(p - CAM11).normalized() for p in (COMP11 + Vector((0, 0, 0.08)), CLOUD_DOOR)]
    look11 = CAM11 + (d11[0] * 0.6 + d11[1] * 0.4).normalized()      # giữa la bàn và cánh cửa, nghiêng về la bàn
    def lp(t):
        scene.frame_set(fr(t))
        p = L.root.matrix_world.translation
        return Vector((p.x, p.y, LOW_Z))

    CAMS = {   # (giây, vị trí máy, điểm nhìn, tiêu cự mm)
        "S1": [(S["S1"][0], (-9.75, -3.3, -0.5), (-10.2, 0.7, -0.85), 26),                 # toàn: tường, dây leo phía trước, Lumo ở đầu tường
               (S["S1"][1], (-10.3, -3.3, -0.5), (-10.75, 0.7, -0.85), 26)],               # lia đều theo Lumo
        "S2": [(t, tuple(lp(t) + Vector((-1.35, -1.35, 0.75))), tuple(lp(t) + Vector((-0.3, 0.05, 0.45))), 28)   # trung, máy theo: chéo phía trước bên trái
               for t in (S["S2"][0], w1, S["S2"][1])],
        "S3": [(S["S3"][0], (-12.95, -0.7, -0.5), (-11.8, 0.7, -0.78), 24)],                # trung: dây leo, phù điêu, Lumo bên phải
        "S4": [(S["S4"][0], (-12.7, -1.05, -0.62), (-11.65, 0.65, -0.78), 28)],             # trung: ấn, kéo
        "S5": [(S["S5"][0], (-13.95, -1.25, -0.6), (-12.5, 0.65, -0.92), 25)],              # trung rộng: phù điêu, thảm rêu, cửa thấp
        "S6": [(S["S6"][0], tuple(eye6), tuple(look6), 17)],                                # cú nhìn: la bàn trước mắt, phù điêu và cửa thấp
        "S7": [(S["S7"][0], (-14.05, -1.45, -0.55), (-12.95, 0.45, -0.78), 24)],             # trung: nhảy cẫng, vào cửa thấp
        "S8": [(S["S8"][0], (39.0, -2.45, 1.5), (40.25, 2.2, 0.55), 18),                     # toàn vòm: bệ, cánh cửa khắc mây cuối vòm
               (tm.VAULT_PUSH, (39.0, -2.45, 1.5), (40.25, 2.2, 0.55), 18),
               (tm.SEE_EMPTY + 0.4, (39.75, -1.05, 1.1), (40.3, 0.9, 0.5), 22)],           # đẩy vào bệ
        "S9": [(S["S9"][0], (38.75, -0.75, 0.85), (40.25, 0.55, 0.55), 26)],                 # trung ở bệ, phía trước bên trái
        "S10": [(S["S10"][0], (39.35, -1.8, 0.95), (40.25, 1.5, 0.6), 22)],                # trung rộng: Lumo quay lưng về cánh cửa
        "S11": [(S["S11"][0], tuple(CAM11), tuple(look11), 22)],                          # cận la bàn, cánh cửa sau lưng
        "S12": [(S["S12"][0], (40.15, -1.0, 0.8), (40.5, 0.45, 0.6), 30)],                  # trung: chóng mặt
        "S13": [(S["S13"][0], (38.3, 0.15, 0.9), (40.3, 1.95, 0.6), 24)],                   # trung rộng từ bên trái: bước về phía cánh cửa
        "S14": [(S["S14"][0], (38.55, 1.85, 0.85), (40.15, 2.85, 0.62), 26)],                 # trung ở cánh cửa
    }
    shots = [(n, a, b) for n, a, b in tm.SHOTS if a < end_t - 1e-6 and b > offset + 1e-6]
    cams = cameras(shots, {n: CAMS[n] for n, _, _ in shots})
    for n, cam in cams.items():                                     # máy di chuyển đều: nội suy LINEAR
        linear(cam)
        linear(bpy.data.objects[f"Aim_{n}"])
    H = Vector((0, 0, 0.2))
    must = {n: [(L.head, H)] for n in ("S1", "S2", "S3", "S4", "S5", "S9", "S10", "S12", "S13", "S14")}
    must.update({"S6": [(comp.root, Vector())], "S11": [(comp.root, Vector())]})
    extra = [("S7", L.head, S["S7"][0], tm.INTO_DOOR[0] + 0.8), ("S8", L.head, tm.ENTER_VAULT[0] + 1.3, S["S8"][1]),
             ("S5", X.door, tm.DOOR_OPEN[0], S["S5"][1]), ("S9", pebble, tm.PLOP, tm.PLOP + 0.3),
             ("S3", X.relief, tm.PART_VINES[1], S["S3"][1]), ("S13", V.glints[0], tm.DOOR_SPARKLE, S["S13"][1])]
    check_in_frame(shots, cams, must, extra, ground=lambda p: ground_z(p.x))
    stills = [round((a + b) / 2, 2) for _, a, b in shots]
    stills += [t for t in (0.3, tm.BEEPS_DENSE[0] + 1.0, tm.PART_VINES[1], tm.RELIEF_ON + 0.4, tm.PRESS[0] + 0.3,
                           tm.PULL[0] + 0.6, tm.RUNUP[1], tm.PUSH[1], tm.TUMBLE[0] + 0.6, tm.TUMBLE[1] + 0.2, tm.DOOR_OPEN[1],
                           tm.NEEDLE_TO_DOOR[0] - 0.3, tm.NEEDLE_TO_DOOR[1] + 0.3, tm.LUMO_LINE1[0] + 0.45, tm.INTO_DOOR[0] + 0.9,
                           tm.ENTER_VAULT[0] + 1.0, tm.EARS_DOWN1 + 0.5, tm.PED_PRESS[0] + 0.6, tm.PED_KNOCKS[1],
                           tm.WAIT_PEBBLE[0] + 0.8, tm.PLOP, tm.LIFT_COMPASS[1] + 0.2, tm.GLANCE, tm.SPIN_LEFT + 0.5,
                           tm.SPIN_RIGHT + 0.5, tm.SPINS[0] + 0.25, tm.DIZZY[0] + 1.0, tm.DOOR_SPARKLE + 0.5,
                           tm.LUMO_LINE2[0] + 1.0, tm.EYES_SHINE[0] + 0.4, tm.STOW[0] + 0.5, tm.RUN_PUSH[0] + 0.8)
               if offset <= t < end_t]
    finish(out_blend, sorted(set(stills)))
