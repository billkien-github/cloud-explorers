"""
EP001 Cảnh 2 (Gadget Action: lắp máy): previz 2D cutout (03_CONTENT/PREVIZ_2D.md, bộ nhân vật pipeline/cutout.py).
Kịch bản: 03_CONTENT/Scripts/EP001_great_rain_experiment.fountain, cảnh #2#. Mốc thời gian và CC: timing.py; mọi
keyframe tính từ các mốc đó.
    .\\pipeline\\run.ps1 build -Shot 03_CONTENT\\Previz_2D\\EP001_Great_Rain_Experiment\\canh02
    .\\pipeline\\run.ps1 preview -Shot 03_CONTENT\\Previz_2D\\EP001_Great_Rain_Experiment\\canh02
    blender -b --factory-startup -P pipeline\\cc.py -- <cảnh>\\renders\\canh02_preview.mp4 <cảnh>\\timing.py <cảnh>\\renders\\canh02_preview_cc.mp4
Bố cục (X, mét): đỉnh đồi phẳng ở Z 0 tới X 3.5 rồi dốc xuống thung lũng (Z -0.6); vườn mầm và Wonder Hub nhỏ xa
dưới chân đồi ở X 3.96–4.82. Máy ở X 2.0: thân 1.5–2.5, nóc 1.125, ròng rọc ở đỉnh giá ba chân 1.85; mặt trước có đồng
hồ (Z 0.88) và núm NHẸ (Z 0.52) bên trái, cần gạt TẮT bên trái phía dưới (Z 0.22–0.36), tấm hình mây giữa thân dưới,
ống đồng ngang Z 0.52, nút đỏ bên phải ngang ngực Lumo (tâm Z 0.40). Vòm kính nằm dưới đất ở X 2.95. Inventor Pack mở
ở X 1.05, hộp ốc ở X 0.45. Cú cận dựng riêng: Wonder Hub ở X = 40, mặt kính Story Lens ở X = 50, la bàn ló khỏi túi
nhìn sang vòm kính ở X = 60, tay Tavi dời móc trên vòm kính ở X = 70.
"""
import math
import pathlib
import sys

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


def steps(t0, t1, step):
    return [t0 + i * step for i in range(int(round((t1 - t0) / step)) + 1)]


def mouth(p, t, k):
    for name, ob in p.mouths.items():
        show(ob, t, name == k)


def cut(p, t):
    """Giữ nguyên tư thế cũ tới sát điểm cắt t (không trôi dần qua các cú không có mặt), từ t đặt tư thế mới."""
    obs = [p.root, p.arm, p.brow, *(n for n, _, _ in p.pupils)]
    obs += [getattr(p, k) for k in ("arm_far", "head", "ear_near", "ear_far") if hasattr(p, k)]
    for ob in obs:
        for path in ("location", "rotation_euler", "scale"):
            key(ob, path, t - HOLD, tuple(getattr(ob, path)))


def enter(p, t, x, z=0.0):
    """Vào cú máy mới ở chỗ (x, z) (Nori đi theo đường bay nori_path); key của từng nhân vật viết theo thứ tự thời gian."""
    cut(p, t)
    ob = nori_path if p is nori else p.root
    at(ob, t - HOLD, ob.location.x, ob.location.z)
    at(ob, t, x, z)


def park(p, t):
    """Ra hẳn ngoài khung từ điểm cắt t, cho tới lần enter sau."""
    enter(p, t, -8.0, 1.0 if p is nori else 0.0)


def facing(p, t, d, turn=0.0):
    """Quay mặt (d = 1 phải, -1 trái); turn = 0 là đổi tức thì ở điểm cắt, > 0 là quay trong turn giây."""
    scl(p.root, t - (turn or HOLD), p.dir, 1)
    scl(p.root, t, d, 1)
    p.dir = d


def bob(ob, t0, t1, x, period=0.8, h=0.02, z=0.0):
    for i, t in enumerate(steps(t0, t1, period / 2)):
        at(ob, t, x, z + (h if i % 2 else 0.0))
    at(ob, t1, x, z)


def walk(ob, t0, t1, x0, x1, n=4, hop=0.04, z=0.0):
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        at(ob, t, x0 + (x1 - x0) * i / n, z + (hop if i % 2 else 0.0))


def flash(ob, t, size=1.0):
    show(ob, t, True)
    for dt, s in ((0.0, 0.2), (0.12, 1.4), (0.3, 0.7), (0.45, 1.1), (0.6, 0.0)):
        scl(ob, t + dt, s * size, s * size)
    show(ob, t + 0.6, False)


def twinkle(ob, t0, t1):
    show(ob, t0, True)
    for i, t in enumerate(steps(t0, t1, 0.15)):
        s = 0.3 if i == 0 else 1.3 if i % 2 else 0.8
        scl(ob, t, s, s)
    scl(ob, t1 + 0.1, 0.0, 0.0)
    show(ob, t1 + 0.1, False)


def puff(ob, t, big=1.0):
    show(ob, t, True)
    scl(ob, t, 0.5 * big, 0.5 * big)
    scl(ob, t + 0.25, 1.4 * big, 1.4 * big)
    show(ob, t + 0.28, False)


def hand(p, x, z, a, lean_deg=0.0, shoulder=(0.03, 0.46), arm=0.21):
    """Vị trí bàn tay trong thế giới khi root ở (x, z), tay xoay a độ, người nghiêng lean_deg (theo hướng p.dir)."""
    hx, hz = shoulder[0] - arm * math.sin(math.radians(a)), shoulder[1] - arm * math.cos(math.radians(a))
    L = math.radians(lean_deg)
    return (x + p.dir * (hx * math.cos(L) + hz * math.sin(L)), z - hx * math.sin(L) + hz * math.cos(L))


def ease(keys, t):
    """Nội suy mượt (smoothstep) giữa các key (t, giá trị…)."""
    if t <= keys[0][0]:
        return keys[0][1:]
    for k0, k1 in zip(keys, keys[1:]):
        if t <= k1[0]:
            u = (t - k0[0]) / (k1[0] - k0[0])
            u = u * u * (3 - 2 * u)
            return tuple(a + (b - a) * u for a, b in zip(k0[1:], k1[1:]))
    return keys[-1][1:]


def gear(r, cx=0.0, cz=0.0):
    """Bánh răng vàng lạ (8 răng, tâm sáng): chỉ dùng cho bánh răng này, không in lên đồ khác."""
    return [(star(r, cx, cz, 8, 0.72), "#E8B33A"), (ell(r * 0.55, r * 0.55, cx, cz), "#F6CF5A"), (ell(r * 0.22, r * 0.22, cx, cz), DARK)]


def segment(name, y, width, col):
    """Đoạn thẳng co giãn được (dây, cánh tay ở cú cận): gốc ở p0, dài 1 m dọc trục -Z trước khi scale."""
    n = node(name, None, (0.0, 0.0), y)
    part(name + "_Line", n, [(rrect(width, 1.0, width / 2, 0, -0.5), col)])
    return n


def seg_to(n, t, p0, p1):
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    at(n, t, *p0)
    ry(n, t, math.degrees(math.atan2(-dx, -dz)))
    scl(n, t, 1, max(0.01, math.hypot(dx, dz)))


def frame(w, h, th, cx, cz):
    """Khung chữ nhật rỗng (chỉ viền) để nhìn xuyên qua."""
    return [rrect(w, th, th / 2, cx, cz + h / 2), rrect(w, th, th / 2, cx, cz - h / 2),
            rrect(th, h, th / 2, cx - w / 2, cz), rrect(th, h, th / 2, cx + w / 2, cz)]


# ================================================================ bối cảnh: đỉnh đồi trọc trên thung lũng
GOLD, PURPLE, METAL, METAL_D, COPPER, ROPE = "#E8B33A", "#7B3FB5", "#B8C0C8", "#7E8790", "#C87533", "#8B6A3E"
FUR, CREAM, LEATHER, GREEN = "#FD8A2B", "#FEECCF", "#8A5A35", "#7EA258"
part("Sky", None, [([(-5, -3), (12, -3), (12, 6), (-5, 6)], "#CFE7F3")], 3.0)
part("FarHills", None, [([(2.8, -0.6), (4.6, 0.05), (6.2, -0.2), (8.5, 0.15), (12, -0.3), (12, -0.6)], "#BCD3B0")], 2.9)
part("Valley", None, [([(3.5, -3), (12, -3), (12, -0.6), (3.5, -0.6)], "#E3C893")], 2.6)
garden = [([(3.96, -0.65), (4.31, -0.65), (4.31, -0.6), (3.96, -0.6)], "#8A6446")]
for gx in (3.99, 4.06, 4.13, 4.2, 4.27):                 # vườn mầm dưới chân đồi: chỗ mưa sẽ rơi
    garden += [(rrect(0.012, 0.08, 0.006, gx, -0.56), "#8DAA55"), (turn(ell(0.028, 0.012, gx + 0.022, -0.52), 25, gx, -0.53), "#A9A84E"),
               (turn(ell(0.024, 0.011, gx - 0.02, -0.54), -30, gx, -0.54), "#A9A84E")]
part("ValleyGarden", None, garden, 2.55)
part("FarHub", None, [(rrect(0.44, 0.1, 0.03, 4.6, -0.55), "#EFE2C4"), (ell(0.2, 0.17, 4.6, -0.5, 0, 180), "#B9A6E8"),
                      (ell(0.055, 0.055, 4.6, -0.43), GOLD), (ell(0.042, 0.042, 4.6, -0.43), "#3A2C5A")], 2.5)
far_portal = part("FarPortal", None, [(ell(0.03, 0.03), "#D7B8FF"), (ell(0.016, 0.016), "#FFE9A8")], 2.49, (4.6, -0.43))
part("Plateau", None, [([(-5, -1.5), (-5, 0.02), (3.5, 0.02), (3.7, -0.08), (3.95, -0.6), (4.05, -1.5)], "#DCCBA6")], 2.0)
tufts = []
for gx in (-1.6, -0.9, -0.2, 0.25, 2.7, 3.2, 3.4):
    tufts += [([(gx - 0.03, 0.02), (gx + 0.03, 0.02), (gx + 0.005, 0.08)], "#C9A44C"),
              ([(gx + 0.01, 0.02), (gx + 0.05, 0.02), (gx + 0.06, 0.06)], "#C9A44C")]
part("Tufts", None, tufts + [(ell(0.07, 0.035, -1.2, 0.03), "#BFAE8C"), (ell(0.05, 0.03, 3.3, 0.02), "#BFAE8C")], 0.5)

# --- Inventor Pack mở trên đất (biểu tượng cờ lê), hộp ốc có ba ngăn, dụng cụ, linh kiện
pack = node("Pack", None, (1.05, 0.0), -0.1)
part("Pack_Body", pack, [(rrect(0.3, 0.24, 0.05, 0, 0.12), LEATHER), (rrect(0.22, 0.13, 0.03, 0, 0.09), "#D8A75A"),
                         (turn(rrect(0.016, 0.085, 0.006, 0, 0.085), 35, 0, 0.09), METAL_D), (arc(0.018, -60, 240, 0.01, 0.025, 0.125), METAL_D),
                         (rrect(0.05, 0.12, 0.012, -0.1, 0.12), "#7FE8F0"), (rrect(0.04, 0.03, 0.008, 0.13, 0.12), GOLD)])   # khoá ở mép phải
flap = node("Pack_Flap", pack, (-0.15, 0.24), -0.01)
part("Pack_FlapShape", flap, [(rrect(0.31, 0.06, 0.03, 0.15, 0.0), "#D8A75A"), (rrect(0.05, 0.08, 0.01, 0.15, -0.02), LEATHER)])
tray = node("Tray", None, (0.45, 0.0), 0.1)
part("Tray_Box", tray, [(rrect(0.4, 0.1, 0.02, 0, 0.05), "#9A7650"), (rrect(0.012, 0.08, 0.004, -0.065, 0.06), "#6E5236"),
                        (rrect(0.012, 0.08, 0.004, 0.065, 0.06), "#6E5236")], 0.0)
SCREW_ROWS = (((-0.15, 0.032), (-0.095, 0.032)), ((-0.035, 0.022), (0.0, 0.022), (0.035, 0.022)),
              ((0.095, 0.015), (0.125, 0.015), (0.155, 0.015)))      # ốc to, vừa, nhỏ


def screw(cx, cz, r):
    return [(rrect(r * 0.6, r * 1.6, r * 0.2, cx, cz - r * 0.8), METAL_D), (rrect(r * 2, r * 0.8, r * 0.3, cx, cz), METAL)]


rows = [part(f"Tray_Screws{i}", tray, [s for x, r in row for s in screw(x, 0.11 + r * 0.8, r)], -0.01) for i, row in enumerate(SCREW_ROWS)]
fly_screw = part("FlyScrew", None, screw(0, 0, 0.045), -0.15, (1.05, 0.2))
tinh = part("Tinh", None, [(star(0.07, 0, 0, 4, 0.3), "#FFF6B0")], -0.16, (0.45, 0.2))


def item(name, shapes):
    n = node(name, None, (1.05, 0.15), -0.12)
    part(name + "_Shape", n, shapes)
    return n


wrench_s = [(rrect(0.022, 0.16, 0.01, 0, 0), METAL), (arc(0.03, -40, 220, 0.016, 0, 0.09), METAL)]
hammer_s = [(rrect(0.022, 0.17, 0.01, 0, 0), "#8B6A3E"), (rrect(0.09, 0.04, 0.012, 0, 0.09), METAL_D)]
driver_s = [(rrect(0.03, 0.07, 0.012, 0, 0.04), "#D23C55"), (rrect(0.01, 0.09, 0.004, 0, -0.04), METAL)]
pipe_s = [(rrect(0.035, 0.2, 0.015, 0, 0), COPPER), (rrect(0.05, 0.03, 0.01, 0, 0.1), "#A85E25")]
items = {
    "wrench": item("It_Wrench", wrench_s), "hammer": item("It_Hammer", hammer_s), "driver": item("It_Driver", driver_s),
    "pipe1": item("It_Pipe1", pipe_s),
    "pipe2": item("It_Pipe2", [(rrect(0.035, 0.16, 0.015, 0, 0), COPPER), (rrect(0.05, 0.03, 0.01, 0, -0.08), "#A85E25")]),
    "plate1": item("It_Plate1", [(rrect(0.16, 0.12, 0.02, 0, 0), METAL), (ell(0.01, 0.01, -0.06, 0.04), METAL_D)]),
    "plate2": item("It_Plate2", [(rrect(0.13, 0.13, 0.02, 0, 0), "#E7D3B0"), (ell(0.01, 0.01, 0.05, -0.05), METAL_D)]),
}
BURST = {"pipe1": (155, 0.66, 70), "plate1": (128, 0.78, 0), "driver": (104, 0.92, 80), "pipe2": (80, 1.6, 95),
         "wrench": (58, 1.24, 90), "plate2": (36, 1.72, 0), "hammer": (18, 0.74, 90)}   # góc cánh hoa, chỗ rơi X, góc nằm
hammer_tavi = part("Hammer_Tavi", None, hammer_s, 0)            # gắn vào tay ở phần diễn
wrench_tavi = part("Wrench_Tavi", None, wrench_s, 0)
driver_tavi = part("Driver_Tavi", None, driver_s, 0)
pipe_tavi = part("Pipe_Tavi", None, [(turn(rrect(0.03, 0.17, 0.012, 0, 0), 90), COPPER)], 0)
hammer_lumo = part("Hammer_Lumo", None, hammer_s, 0)
wrench_ground = part("Wrench_Ground", None, [(turn(pts, 90), c) for pts, c in wrench_s], -0.12, (1.86, 0.035))
hammer_ground = part("Hammer_Ground", None, [(turn(pts, 90), c) for pts, c in hammer_s], -0.12, (1.79, 0.035))
koc = part("Koc", None, [(turn(rrect(0.012, 0.05, 0.005, 0, 0.06), a), "#FF9F1C") for a in (-50, 0, 50)], -0.45, (1.95, 0.36))

# --- máy làm mưa Rain-O-Matic (thân tròn ú cao quá đầu Lumo, bốn chân, giá ba chân có ròng rọc trên nóc)
machine = node("Machine", None, (2.0, 0.0), 0.3)
legs = part("M_Legs", machine, [(rrect(0.1, 0.22, 0.03, -0.2, 0.1), "#6E6E6E"), (rrect(0.1, 0.22, 0.03, 0.2, 0.1), "#6E6E6E")], 0.02)
legs_front = part("M_LegsFront", machine, [(rrect(0.12, 0.22, 0.04, -0.33, 0.1), "#8C8C8C"), (rrect(0.12, 0.22, 0.04, 0.33, 0.1), "#8C8C8C")],
                  -0.02)
body_low = part("M_BodyLow", machine, [(rrect(1.0, 0.5, 0.2, 0, 0.425), "#E7D3B0"), (rrect(1.0, 0.03, 0.01, 0, 0.6), "#C9B48E")], 0.0)
ribs = part("M_Ribs", machine, [(rrect(0.05, 0.5, 0.02, -0.4, 0.88), METAL_D), (rrect(0.05, 0.5, 0.02, 0.4, 0.88), METAL_D),
                                (band(curve((-0.4, 1.1), (0.0, 1.22), (0.4, 1.1)), 0.04), METAL_D)], 0.005)
rivets = [(ell(0.012, 0.012, x, z), "#B49C74") for x in (-0.42, -0.14, 0.14, 0.42) for z in (0.68, 1.02)]
body = part("M_Body", machine, [(rrect(1.0, 0.95, 0.28, 0, 0.65), "#E7D3B0"), (rrect(1.0, 0.03, 0.01, 0, 0.6), "#C9B48E"),
                                (rrect(1.0, 0.03, 0.01, 0, 0.75), "#C9B48E"), (rrect(0.62, 0.04, 0.015, 0, 1.135), METAL_D)] + rivets,
            -0.001)
PLATE = [(rrect(0.24, 0.2, 0.03, 0, 0), "#D4E3EC"), (ell(0.05, 0.03, -0.02, 0.04), WHITE), (ell(0.035, 0.03, 0.03, 0.05), WHITE),
         (ell(0.012, 0.018, -0.04, -0.03), "#4FB3E8"), (ell(0.012, 0.018, 0.0, -0.05), "#4FB3E8"),
         (ell(0.012, 0.018, 0.04, -0.03), "#4FB3E8")]                        # tấm có hình mây và ba giọt mưa: lắp ngược là thấy
PLATE_AT = (2.02, 0.3)                                          # giữa thân dưới, không che núm, cần gạt, nút đỏ
plate = part("M_Plate", None, PLATE, 0.27, PLATE_AT)
pipe_a = part("M_PipeA", None, [(rrect(0.17, 0.032, 0.012, 1.9, 0.52), COPPER), (rrect(0.03, 0.05, 0.01, 1.82, 0.52), "#A85E25")], 0.27)
pipe_b = part("M_PipeB", None, [(rrect(0.18, 0.032, 0.012, 2.07, 0.52), COPPER), (rrect(0.03, 0.05, 0.01, 1.985, 0.52), "#A85E25")], 0.27)
controls = node("M_Controls", machine, (0.0, 0.0), -0.01)
part("M_Knob", controls, [(ell(0.064, 0.064, -0.3, 0.52), "#4A4A4A"), (rrect(0.013, 0.055, 0.005, -0.3, 0.55), WHITE)])     # núm NHẸ
part("M_Gauge", controls, [(ell(0.085, 0.085, -0.27, 0.88), "#5A5A5A"), (ell(0.072, 0.072, -0.27, 0.88), "#F5F5F5"),
                           (arc(0.055, 45, 170, 0.016, -0.27, 0.88), "#7BC67B"), (arc(0.055, 10, 45, 0.016, -0.27, 0.88), "#E05050"),
                           (turn(rrect(0.008, 0.055, 0.003, -0.27, 0.905), 50, -0.27, 0.88), "#333333")])
part("M_Lever", controls, [(rrect(0.1, 0.05, 0.015, -0.34, 0.22), "#4A4A4A"),                                                 # cần gạt TẮT
                           (turn(rrect(0.022, 0.13, 0.008, -0.34, 0.28), -20, -0.34, 0.22), METAL_D), (ell(0.03, 0.03, -0.315, 0.335), "#2E86C1")])
part("M_Button", controls, [(ell(0.11, 0.11, 0.33, 0.4), "#5A5A5A"), (ell(0.09, 0.09, 0.33, 0.4), "#B71C1C"),
                            (ell(0.075, 0.075, 0.335, 0.405), "#E53935"), (ell(0.025, 0.02, 0.36, 0.44), "#FF9A9A")])     # ngang ngực Lumo
button_glint = part("M_ButtonGlint", controls, [(star(0.08, 0, 0, 4, 0.3), "#FFF6C8")], -0.02, (0.37, 0.46))
part("M_Nozzle", controls, [(rrect(0.08, 0.16, 0.02, 0.3, 1.2), METAL_D), (rrect(0.12, 0.04, 0.015, 0.3, 1.28), "#6E6E6E")], 0.012)
part("M_Tripod", controls, [(band([(-0.44, 1.1), (0.0, 1.85)], 0.035), "#9A7650"), (band([(0.44, 1.1), (0.0, 1.85)], 0.035), "#9A7650"),
                            (band([(0.0, 1.12), (0.0, 1.85)], 0.03), "#7A5A3A")], 0.04)
part("M_Pulley", controls, [(ell(0.07, 0.07, 0, 1.85), "#6E6E6E"), (ell(0.035, 0.035, 0, 1.85), METAL), (ell(0.012, 0.012, 0, 1.85), DARK)],
     -0.03)
PULLEY_R, PULLEY_L = (2.06, 1.85), (1.94, 1.85)


# --- vòm kính: kính tròn, lõi tinh thể xanh, ổ bánh răng (trống tới lúc lắp), cửa nhỏ chỉ có viền (nhìn xuyên thấy ổ),
# khoen móc ở mép và ở giữa đỉnh (điểm cân bằng)
def make_dome(name, loc, y, s=1.0):
    d = node(name, None, loc, y)
    d.scale = (s, 1.0, s)
    part(name + "_Base", d, [(rrect(0.62, 0.07, 0.025, 0, 0.035), METAL_D), (ell(0.025, 0.025, -0.27, 0.07), "#6E6E6E")], -0.004)
    part(name + "_Glass", d, [(ell(0.3, 0.3, 0, 0.065, 0, 180), "#BFE8F5"), (arc(0.22, 100, 150, 0.025, 0, 0.065), WHITE)], 0.0)
    part(name + "_Core", d, [([(0.05, 0.08), (0.1, 0.17), (0.05, 0.28), (0.0, 0.17)], "#3FA9F5"),
                             ([(0.05, 0.12), (0.075, 0.17), (0.05, 0.24)], "#9FE0FF"),
                             (arc(0.042, 0, 360, 0.012, -0.1, 0.14), "#6E6E6E")], -0.002)          # lõi tinh thể, ổ bánh răng
    part(name + "_TopLoop", d, [(arc(0.025, 0, 360, 0.012, 0, 0.385), "#6E6E6E")], -0.003)
    sock = part(name + "_SocketGear", d, gear(0.036, -0.1, 0.14), -0.003)
    hat = node(name + "_Hatch", d, (-0.1, 0.205), -0.006)
    part(name + "_HatchShape", hat, [(pts, "#5FA8C4") for pts in frame(0.12, 0.13, 0.012, 0, -0.065)]
         + [(ell(0.012, 0.012, 0.045, -0.065), "#6E6E6E")])
    spot = part(name + "_BalanceSpot", d, [(star(0.075, 0, 0, 4, 0.3), "#FFF27A")], -0.01, (0.0, 0.385))
    return d, sock, hat, spot


dome, socket_gear, hatch, balance_spot = make_dome("Dome", (2.95, 0.0), 0.25)
klop = part("Dome_Klop", dome, [(star(0.07, 0, 0, 4, 0.3), "#FFF6C8")], -0.012, (-0.1, 0.14))
H_RIM, H_TOP = (-0.27, 0.07), (0.0, 0.385)
dust = part("DomeDust", None, [(ell(0.1, 0.04), "#D9C8A2"), (ell(0.07, 0.03, 0.14, 0.02), "#D9C8A2"),
                               (ell(0.07, 0.03, -0.14, 0.02), "#D9C8A2")], -0.05, (2.95, 0.03))
khop = part("Khop", None, [(star(0.12, 0, 0, 8, 0.35), "#FFF27A")], 0.22, (2.0, 1.2))

# --- móc và hai đoạn dây ròng rọc (đoạn có móc bên phải, đầu dây bên trái), dây trước thân máy
HOOK_S = [(arc(0.035, 180, 360, 0.014, 0, 0.0), "#5A5A5A"), (rrect(0.014, 0.05, 0.006, 0.035, 0.025), "#5A5A5A")]
hook = node("Hook", None, (2.58, 0.9), 0.18)
part("Hook_Shape", hook, HOOK_S)
rope_r, rope_l = segment("RopeR", 0.2, 0.014, ROPE), segment("RopeL", 0.2, 0.014, ROPE)

# --- cú cận: mặt kính Story Lens (X = 50) với hình cái bập bênh
part("Lens_BG", None, [([(49.0, -0.6), (51.0, -0.6), (51.0, 0.6), (49.0, 0.6)], "#E6DAF7")], 1.0)
part("Lens_Big", None, [(rrect(0.12, 0.5, 0.05, 50.0, -0.6), PURPLE), (ell(0.4, 0.4, 50.0, 0.02), GOLD), (ell(0.36, 0.36, 50.0, 0.02), "#CDB6FF"),
                        (star(0.06, 50.0, 0.43, 4, 0.5), "#B98BF0"), (ell(0.05, 0.05, 50.32, 0.27), WHITE)], 0.5)
seesaw = node("Lens_Seesaw", None, (50.0, -0.08), 0.46)
part("Lens_Fulcrum", seesaw, [([(-0.07, -0.12), (0.07, -0.12), (0.0, 0.0)], "#7B5CC2")], 0.004)
plank = node("Lens_Plank", seesaw, (0.0, 0.0), 0.0)
part("Lens_PlankShape", plank, [(rrect(0.5, 0.03, 0.012, 0, 0.015), "#5A3E9A"), (rrect(0.06, 0.06, 0.015, -0.21, 0.06), "#5A3E9A"),
                                (rrect(0.06, 0.06, 0.015, 0.21, 0.06), "#5A3E9A")])
lens_dot = part("Lens_Dot", seesaw, [(star(0.05, 0, 0, 4, 0.3), "#FFF27A")], -0.01, (0.0, 0.02))

# --- cú cận: Wonder Hub dưới chân đồi (X = 40), cổng truyện đang khép, le lói qua ô cửa tròn
part("Hub_Sky", None, [([(38.0, -1.0), (42.0, -1.0), (42.0, 1.2), (38.0, 1.2)], "#CFE7F3")], 1.0)
part("Hub_Hills", None, [([(38.0, -0.3), (39.0, 0.15), (40.4, -0.05), (41.5, 0.25), (42.0, -0.3)], "#BCD3B0")], 0.97)
part("Hub_Ground", None, [([(38.0, -1.0), (42.0, -1.0), (42.0, -0.32), (38.0, -0.32)], "#E3C893")], 0.95)
part("Hub_House", None, [(rrect(1.4, 0.3, 0.06, 40.1, -0.2), "#EFE2C4"), (ell(0.66, 0.55, 40.1, -0.05, 0, 180), "#B9A6E8"),
                         (arc(0.66, 0, 180, 0.03, 40.1, -0.05), GOLD), (rrect(0.24, 0.3, 0.1, 40.65, -0.2), "#C9B48E"),
                         (ell(0.24, 0.24, 40.1, 0.08), GOLD), (ell(0.2, 0.2, 40.1, 0.08), "#2E2347")], 0.9)
portal = node("Hub_Portal", None, (40.1, 0.08), 0.88)
part("Hub_PortalShape", portal, [(arc(0.15, 0, 360, 0.04), "#C59BFF"), (arc(0.11, 0, 360, 0.02), "#FFE9A8"), (ell(0.09, 0.09), "#5C3F9E")])
part("Hub_Foreground", None, [([(38.6, 1.2), (38.6, -0.2), (38.85, 0.05), (39.0, 0.6), (39.2, 1.2)], "#C9B794")], 0.5)   # mép đồi phía trước

# --- cú cận: la bàn ló khỏi túi da của Lumo, ngôi sao xoay về vòm kính có bánh răng vàng (X = 60)
part("Peek_BG", None, [([(59.0, -0.6), (61.0, -0.6), (61.0, 0.6), (59.0, 0.6)], "#CFE7F3"),
                       ([(59.0, -0.6), (61.0, -0.6), (61.0, -0.3), (59.0, -0.3)], "#DCCBA6")], 1.0)
part("Peek_Lumo", None, [(ell(0.62, 0.62, 59.35, 0.12), FUR), (ell(0.34, 0.42, 59.56, 0.06), CREAM),
                         (band([(59.0, 0.62), (59.8, -0.12)], 0.05), LEATHER)], 0.9)                # thân Lumo, quai túi chéo
part("Peek_Bag", None, [(rrect(0.4, 0.3, 0.06, 59.75, -0.18), LEATHER), (rrect(0.4, 0.05, 0.02, 59.75, -0.04), "#6E4527"),
                        (ell(0.06, 0.035, 59.73, -0.18), WHITE), (ell(0.045, 0.03, 59.79, -0.17), WHITE)], 0.8)   # túi da có hình mây
peek_big = node("Peek_Compass", None, (59.75, -0.12), 0.85)     # sau mặt túi: ló dần lên
part("Peek_CompassShape", peek_big, [(ell(0.17, 0.17), "#E5B53A"), (ell(0.135, 0.135), "#5BC3E8")])
peek_big_star = node("Peek_Star", peek_big, (0.0, 0.0), -0.005)
part("Peek_StarShape", peek_big_star, [(star(0.1, 0, 0, 8, 0.4), "#FFF6C8"), ([(0, 0.13), (0.02, 0.0), (0, -0.02), (-0.02, 0.0)], "#FF6B4A"),
                                       (ell(0.02, 0.02), WHITE)])
peek_tit = part("Peek_Tit", None, [(turn(rrect(0.02, 0.08, 0.008, 0.0, 0.25), a), "#FF9F1C") for a in (-45, 0, 45)], 0.7, (59.75, 0.0))
small_dome, _, _, small_spot = make_dome("PeekDome", (60.5, -0.32), 0.92, 0.8)   # bánh răng đã lắp, thấy qua cửa nhỏ
peek_dome_glint = part("PeekDome_Glint", None, [(star(0.07, 0, 0, 4, 0.3), "#FFF6C8")], 0.9, (60.42, -0.21))

# --- cú cận: tay Tavi dời cái móc từ mép vòm tới giữa đỉnh vòm (X = 70), vòm phóng to 1.9 lần
part("Big_BG", None, [([(69.0, -0.6), (71.0, -0.6), (71.0, 0.6), (69.0, 0.6)], "#CFE7F3"),
                      ([(69.0, -0.6), (71.0, -0.6), (71.0, -0.33), (69.0, -0.33)], "#DCCBA6")], 1.0)
BIG_S, BIG_AT = 1.9, (70.05, -0.35)
big_dome, _, _, big_spot = make_dome("BigDome", BIG_AT, 0.9, BIG_S)
big_hook = node("BigHook", None, (69.5, -0.2), 0.8)
part("BigHook_Shape", big_hook, [(pts, c) for pts, c in ((turn([(x * BIG_S, z * BIG_S) for x, z in p], 0), c) for p, c in HOOK_S)])
big_rope = segment("BigRope", 0.82, 0.026, ROPE)
big_arm = segment("BigArm", 0.75, 0.1, GREEN)                    # tay Tavi thò vào từ góc trên bên trái
big_hand = part("BigHand", None, [(ell(0.065, 0.06), GREEN)], 0.74)
BIG_RIM = (BIG_AT[0] + H_RIM[0] * BIG_S, BIG_AT[1] + H_RIM[1] * BIG_S)
BIG_TOP = (BIG_AT[0] + H_TOP[0] * BIG_S, BIG_AT[1] + H_TOP[1] * BIG_S)

# ================================================================ nhân vật và đồ cầm tay
tavi = build_tavi(-1.0, -0.40)
lumo = build_lumo(-1.4, -0.32)
piko = build_piko(-1.7, -0.28)
nori = build_nori(0.0, 0.0, -0.2)
nori_path = node("Nori_Path", None, (-1.0, 1.25), -0.2)
nori.root.parent, nori.root.location = nori_path, (0.0, 0.0, 0.0)

for ob, p, z in ((hammer_tavi, tavi, -0.2), (wrench_tavi, tavi, -0.2), (driver_tavi, tavi, -0.2), (pipe_tavi, tavi, -0.2),
                 (hammer_lumo, lumo, -0.22)):
    ob.parent, ob.location = p.arm, (0.0, -0.006, z)
duck_s = [(ell(0.065, 0.042, 0, 0), "#FFD84D"), (ell(0.034, 0.034, 0.05, 0.045), "#FFD84D"),
          ([(0.075, 0.05), (0.11, 0.04), (0.075, 0.03)], "#FF9A2E"), (ell(0.007, 0.007, 0.06, 0.055), DARK),
          (arc(0.03, 200, 330, 0.01, -0.01, 0.02), "#F2B92E")]
duck = part("Duck", piko.arm, duck_s, -0.006, (0.03, -0.1))
duck_gear = part("Duck_Gear", duck, gear(0.028, 0.125, 0.04), -0.002)
gear_glint = part("Duck_GearGlint", duck, [(star(0.06, 0, 0, 4, 0.3), "#FFF6C8")], -0.004, (0.13, 0.06))
duck_hug = part("DuckHug", piko.root, duck_s, -0.04, (0.17, 0.2))   # ôm vào bụng
tavi_gear = part("Tavi_Gear", tavi.arm, gear(0.036), -0.008, (0.0, -0.22))
STUCK = ((-0.24, 0.3), (-0.2, 0.48), (-0.16, 0.15))             # ba con ốc dính sau lưng Piko
stuck = [part(f"Piko_Screw{i}", piko.root, screw(0, 0, 0.026), -0.032, xz) for i, xz in enumerate(STUCK)]
poc = part("Poc", None, [(star(0.05, 0, 0, 5, 0.4), "#FFF6C8")], -0.45, (0.0, 0.3))
pop_fly = part("PopFly", None, screw(0, 0, 0.026), -0.46, (0.0, 0.3))
sparkle = [part(f"Piko_EyeStar{i}", piko.head, [(star(0.03, 0, 0, 4, 0.3), WHITE)], -0.03, (0.1 + dx, 0.44 + dz))
           for i, (dx, dz) in enumerate(((0.02, 0.03), (-0.02, -0.025)))]
peek = part("Lumo_CompassPeek", lumo.bag, [(ell(0.045, 0.045), "#E5B53A"), (ell(0.034, 0.034), "#5BC3E8")], 0.002, (0.1, 0.2))
tit = part("Lumo_Tit", lumo.root, [(turn(rrect(0.012, 0.05, 0.005, 0.0, 0.08), a), "#FF9F1C") for a in (-50, 0, 50)], -0.03, (0.1, 0.25))
lens = node("Nori_Lens", nori.root, (0.13, -0.2), -0.03)
part("Nori_LensShape", lens, [(rrect(0.022, 0.08, 0.01, 0, -0.08), PURPLE), (ell(0.065, 0.065), GOLD), (ell(0.052, 0.052), "#CDB6FF"),
                              (arc(0.04, 110, 160, 0.01), WHITE)])

# ================================================================ ẩn hiện mặc định
for ob in (*items.values(), hammer_tavi, wrench_tavi, driver_tavi, pipe_tavi, hammer_lumo, wrench_ground, hammer_ground, koc, fly_screw,
           tinh, legs, legs_front, body_low, ribs, body, plate, pipe_a, pipe_b, controls, dome, hook, rope_r, rope_l, duck, duck_hug,
           tavi_gear, *stuck, poc, pop_fly, *sparkle, peek, tit, lens, klop, dust, khop, gear_glint, lens_dot, pack, tray, *rows, peek_tit,
           peek_dome_glint, big_spot, small_spot):
    show(ob, 0.0, False)

# ================================================================ montage: lên đỉnh đồi, mở Inventor Pack
show(tavi.pack, 0.0, True)
show(tavi.pack, PACK_DOWN, False)                                # hạ ba lô xuống đất
for ob in (pack, tray, *rows):
    show(ob, PACK_DOWN, True)
ry(flap, 0.0, 0)
ry(flap, PACK_OPEN[0], 0)
ry(flap, PACK_OPEN[0] + 0.25, -175)                             # nắp bật ngửa hẳn ra sau
b0 = PACK_OPEN[0] + 0.2
for k, (ang, gx, rot) in BURST.items():                         # bung ra như cánh hoa rồi rơi xuống quanh ba lô
    ob = items[k]
    a = math.radians(ang)
    px, pz = 1.05 + 0.36 * math.cos(a), 0.34 + 0.3 * math.sin(a)
    show(ob, b0, True)
    at(ob, b0, 1.05, 0.18)
    scl(ob, b0, 0.2, 0.2)
    ry(ob, b0, 0)
    at(ob, b0 + 0.35, px, pz)
    scl(ob, b0 + 0.35, 1, 1)
    ry(ob, b0 + 0.35, 90 - ang)
    at(ob, PACK_OPEN[1] + 0.2, px, pz + 0.03)
    ry(ob, PACK_OPEN[1] + 0.2, 90 - ang)
    at(ob, PACK_OPEN[1] + 0.6, gx, 0.04)
    ry(ob, PACK_OPEN[1] + 0.6, rot)
    show(ob, SHOT["S3"][0], False)                              # linh kiện đã lắp vào máy, dụng cụ đã cất
show(fly_screw, SCREW_UP[0], True)                              # con ốc bay vèo lên trời rồi rơi trúng hộp ốc
at(fly_screw, SCREW_UP[0], 1.05, 0.2)
at(fly_screw, SCREW_UP[1], 0.95, 1.4)
at(fly_screw, SCREW_IN - 0.45, 0.55, 1.3)
at(fly_screw, SCREW_IN, 0.45, 0.16)
for i, t in enumerate(steps(SCREW_UP[0], SCREW_IN, 0.1)):
    ry(fly_screw, t, 70 * i)
show(fly_screw, SCREW_IN + 0.05, False)
flash(tinh, SCREW_IN, 1.2)

# --- máy thành hình dần qua các cú montage
for ob in (legs, legs_front, body_low, ribs, pipe_a, wrench_ground):
    show(ob, SHOT["S3"][0], True)
show(ribs, SHOT["S4"][0], False)
show(body, SHOT["S4"][0], True)
show(plate, PLATE_WRONG[0], True)
for ob in (controls, dome, hook, rope_r, rope_l):
    show(ob, SHOT["S7"][0], True)
for ob in (button_glint, socket_gear, balance_spot, klop):      # mảnh con chỉ hiện lúc cần
    show(ob, SHOT["S7"][0], False)

# --- tấm lắp ngược: lắp vào, Tavi nghiêng đầu, tháo ra, lật lại, lắp lại
w0, w1 = PLATE_WRONG
ry(plate, w0, 180)
at(plate, w0, *PLATE_AT)
at(plate, w0 + 1.0, *PLATE_AT)
ry(plate, w0 + 1.0, 180)
at(plate, w0 + 1.15, PLATE_AT[0] - 0.09, PLATE_AT[1] - 0.03)   # tháo ra cầm trên tay
ry(plate, w0 + 1.35, 180)
ry(plate, w0 + 1.6, 0)                                          # lật lại
at(plate, w0 + 1.6, PLATE_AT[0] - 0.09, PLATE_AT[1] - 0.03)
at(plate, w0 + 1.8, *PLATE_AT)                                  # lắp lại
ry(plate, w0 + 1.8, 0)

# ================================================================ Tavi
loop(tavi.tail, 0.0, SECONDS, 1.8, -4, 4)
face(tavi, 0.0, "eager")
ry(tavi.arm, 0.0, 6)
ry(tavi.arm_far, 0.0, -6)
lean(tavi, 0.0, 0)
walk(tavi.root, ARRIVE[0], ARRIVE[1], -1.0, 1.35, 6)
lean(tavi, PACK_DOWN - 0.2, 0)
lean(tavi, PACK_DOWN, 14)                                       # hạ ba lô
lean(tavi, PACK_DOWN + 0.3, 0)
# S2: cúi bật khoá ba lô, ba lô bung đồ; mắt theo con ốc lên trời rồi xuống hộp
enter(tavi, SHOT["S2"][0], 1.42)
facing(tavi, SHOT["S2"][0], -1)
lean(tavi, SHOT["S2"][0], 16)
look(tavi, SHOT["S2"][0], 1.0, -0.8)
lean(tavi, TAVI_OPEN, 25)
ry(tavi.arm, TAVI_OPEN - 0.1, 6)
ry(tavi.arm, TAVI_OPEN + 0.1, -40)                              # bật khoá
ry(tavi.arm, PACK_OPEN[0] + 0.15, 6)
lean(tavi, PACK_OPEN[0] + 0.2, 10)
face(tavi, PACK_OPEN[0] + 0.25, "eager")
look(tavi, SCREW_UP[0] + 0.1, 0.4, 1.0)
lean(tavi, SCREW_UP[0], 10)
lean(tavi, SCREW_UP[0] + 0.3, 0)
ry(tavi.head, SCREW_UP[0], 0)
ry(tavi.head, SCREW_UP[0] + 0.3, -22)
ry(tavi.head, SCREW_IN - 0.4, -22)
ry(tavi.head, SCREW_IN, 12)
look(tavi, SCREW_IN - 0.3, 1.0, -1.0)
face(tavi, SCREW_IN + 0.05, "happy")
# S3: vặn ốc, gõ búa, nối ống đồng, lắp ngược một tấm
enter(tavi, SHOT["S3"][0], 1.68)
facing(tavi, SHOT["S3"][0], 1)
lean(tavi, SHOT["S3"][0], 0)
ry(tavi.head, SHOT["S3"][0], 0)
look(tavi, SHOT["S3"][0], 0.9, -0.2)
face(tavi, SHOT["S3"][0], "eager")
show(driver_tavi, TAVI_SCREW[0] - 0.05, True)
show(driver_tavi, TAVI_SCREW[1] + 0.05, False)
ry(tavi.arm, TAVI_SCREW[0], -95)
loop(tavi.arm, TAVI_SCREW[0] + 0.1, TAVI_SCREW[1], 0.15, -88, -102)
show(hammer_tavi, HAMMER[0] - 0.05, True)
show(hammer_tavi, HAMMER[1] + 0.05, False)
for t in (HAMMER[0] + 0.2, HAMMER[0] + 0.45):                   # CỐC. CỐC.
    ry(tavi.arm, t - 0.15, -150)
    ry(tavi.arm, t, -95)
    flash(koc, t, 0.8)
ry(tavi.arm, HAMMER[1], -95)
show(pipe_tavi, PIPE[0] - 0.05, True)                           # nối ống đồng
ry(tavi.arm, PIPE[0], -95)
ry(tavi.arm, PIPE[0] + 0.25, -122)
look(tavi, PIPE[0], 0.9, 0.3)
show(pipe_tavi, PIPE[0] + 0.35, False)
show(pipe_b, PIPE[0] + 0.35, True)
ry(tavi.arm, PIPE[1], -95)
w0, w1 = PLATE_WRONG
ry(tavi.arm, w0 - 0.05, -95)                                    # đặt tấm vào
ry(tavi.arm, w0 + 0.25, 6)
look(tavi, w0, 0.9, -0.3)
ry(tavi.head, w0 + 0.3, 0)
ry(tavi.head, w0 + 0.55, 16)                                    # nghiêng đầu nhìn tấm lắp ngược
face(tavi, w0 + 0.5, "puzzled", 16)
blink(tavi, w0 + 0.75)
ry(tavi.arm, w0 + 0.95, -95)                                    # tháo ra, lật lại, lắp lại
ry(tavi.arm, w0 + 1.15, -82)
ry(tavi.arm, w0 + 1.8, -95)
ry(tavi.head, w0 + 1.2, 6)
ry(tavi.head, w0 + 1.9, 0)
face(tavi, w0 + 1.85, "happy")
ry(tavi.arm, w1, 6)
# S4: chìa tay ra sau xin cờ lê, nhận cái búa; tỉnh bơ đặt búa xuống, nhặt cờ lê
ry(tavi.arm, TAVI_ASK[0] - 0.2, -95)
loop(tavi.arm, SHOT["S4"][0], TAVI_ASK[0] - 0.1, 0.15, -88, -102)
face(tavi, SHOT["S4"][0], "eager")
look(tavi, SHOT["S4"][0], 0.9, -0.1)
ry(tavi.arm, TAVI_ASK[0] + 0.15, 45)                            # mắt vẫn nhìn máy, tay chìa ra sau
show(hammer_tavi, LUMO_HAMMER[1] - 0.1, True)
s0, s1 = TAVI_SWAP
ry(tavi.arm, s0, 45)
ry(tavi.arm, s0 + 0.25, -75)                                    # đưa cái búa ra trước mặt
ry(tavi.head, s0, 0)
ry(tavi.head, s0 + 0.25, 14)
look(tavi, s0 + 0.25, 0.6, -0.7)
face(tavi, s0 + 0.2, "neutral", 14)                             # mặt tỉnh bơ, nhìn cái búa một lúc
blink(tavi, s0 + 0.6)
ry(tavi.arm, s0 + 1.0, -75)
lean(tavi, s0 + 1.0, 0)
lean(tavi, s0 + 1.2, 22)                                        # cúi đặt búa xuống đất
ry(tavi.arm, s0 + 1.2, -20)
show(hammer_tavi, s0 + 1.25, False)
show(hammer_ground, s0 + 1.25, True)
show(wrench_ground, s0 + 1.45, False)                           # nhặt cờ lê
show(wrench_tavi, s0 + 1.45, True)
look(tavi, s0 + 1.2, 0.8, -1.0)
lean(tavi, s0 + 1.5, 22)
lean(tavi, s0 + 1.75, 0)
ry(tavi.arm, s0 + 1.5, -20)
ry(tavi.arm, s0 + 1.75, -95)
ry(tavi.head, s0 + 1.75, 0)
look(tavi, s0 + 1.75, 0.9, -0.1)
loop(tavi.arm, s0 + 1.8, SHOT["S4"][1], 0.15, -88, -102)
show(wrench_tavi, SHOT["S4"][1], False)
park(tavi, SHOT["S5"][0])
# S6: gỡ ốc khỏi Piko
enter(tavi, SHOT["S6"][0], -0.36)
ry(tavi.arm, SHOT["S6"][0], 6)
face(tavi, SHOT["S6"][0], "neutral")
look(tavi, SHOT["S6"][0], 0.9, -0.2)
for t, a in zip(POPS, (-82, -115, -60)):                        # PÓC. PÓC. PÓC.
    ry(tavi.arm, t - 0.3, a)
    ry(tavi.arm, t, a)
    ry(tavi.arm, t + 0.12, a + 25)
ry(tavi.arm, POPS[2] + 0.4, 6)
face(tavi, POPS[2] + 0.3, "happy")
# S7: ngắm cái máy vừa xong
enter(tavi, SHOT["S7"][0], 1.25)
ry(tavi.head, SHOT["S7"][0], -14)
look(tavi, SHOT["S7"][0], 0.6, 0.8)
face(tavi, SHOT["S7"][0], "happy")
# S8: lục hộp đồ, cau mày, "Thiếu đúng một bánh răng."
enter(tavi, SHOT["S8"][0], 1.32)
facing(tavi, SHOT["S8"][0], -1)
ry(tavi.head, SHOT["S8"][0], 14)
look(tavi, SHOT["S8"][0], 0.8, -0.9)
face(tavi, SHOT["S8"][0], "eager", 30)
lean(tavi, SHOT["S8"][0], 24)
r0, r1 = TAVI_RUMMAGE
ry(tavi.arm, r0, -45)
loop(tavi.arm, r0 + 0.1, r1, 0.2, -35, -65)                     # lục. lục nữa.
lean(tavi, r0 + 0.7, 30)
lean(tavi, r1, 24)
face(tavi, r1 - 0.2, "worried", 30)                             # cau mày
lean(tavi, TAVI_MISS[0], 8)
ry(tavi.head, TAVI_MISS[0], 6)
ry(tavi.arm, TAVI_MISS[0], 6)
look(tavi, TAVI_MISS[0], 0.5, 0.0)
face(tavi, TAVI_MISS[0], "worried", 14)
talk(tavi, TAVI_MISS[0], TAVI_MISS[1], "frown")
lean(tavi, TAVI_MISS[1], 0)
# S9: ngơ ngác nhìn con vịt, rồi thấy bánh răng vàng: mừng rỡ nhảy cẫng, gỡ bánh răng
ry(tavi.head, PIKO_HELP[0], 6)
look(tavi, PIKO_HELP[0], 0.8, -0.4)
face(tavi, TAVI_PUZZLE[0], "puzzled", 6)
ry(tavi.head, TAVI_PUZZLE[0] + 0.15, 14)                        # nghiêng đầu nhìn con vịt
blink(tavi, TAVI_PUZZLE[0] + 0.3)
face(tavi, GEAR_GLINT[0] + 0.15, "eager")
ry(tavi.head, GEAR_GLINT[0] + 0.15, 0)
look(tavi, GEAR_GLINT[0] + 0.15, 0.9, -0.2)
at(tavi.root, GEAR_GLINT[0] + 0.15, 1.32, 0)
at(tavi.root, GEAR_GLINT[0] + 0.3, 1.32, 0.08)                  # nhảy cẫng
at(tavi.root, GEAR_GLINT[0] + 0.45, 1.32, 0)
ry(tavi.arm, TAVI_TAKE[0], 6)
ry(tavi.arm, TAVI_TAKE[0] + 0.25, -92)                          # gỡ bánh răng khỏi mỏ vịt
show(tavi_gear, TAVI_TAKE[0] + 0.3, True)
ry(tavi.arm, TAVI_TAKE[1], -100)
# S10: kéo kính xuống, soi bánh răng, mở cửa nhỏ, lắp vào, CẠCH, đóng cửa, đẩy kính lên
enter(tavi, SHOT["S10"][0], 2.55)
facing(tavi, SHOT["S10"][0], 1)
lean(tavi, SHOT["S10"][0], 0)
ry(tavi.head, SHOT["S10"][0], 0)
ry(tavi.arm, SHOT["S10"][0], -95)
look(tavi, SHOT["S10"][0], 0.8, -0.3)
face(tavi, SHOT["S10"][0], "eager")
g0, g1 = GOGGLES_DOWN
DOWN = (tavi.GOGGLES_DOWN[0], -0.02, tavi.GOGGLES_DOWN[1])
show(tavi.goggle_lens, 0.0, True)
key(tavi.goggles, "location", g0, (0.0, -0.02, 0.0))
ry(tavi.arm_far, g0 - 0.1, -6)
ry(tavi.arm_far, g0 + 0.15, -150)                               # tay kia kéo kính xuống
key(tavi.goggles, "location", g1, DOWN)
show(tavi.goggle_lens, g1, False)                               # chỉ còn vành kính: vẫn thấy mắt
ry(tavi.arm_far, g1 + 0.1, -6)
i0, i1 = INSPECT
ry(tavi.head, i0, 18)                                           # cúi soi bánh răng trên tay
look(tavi, i0, 1.0, -0.6)
face(tavi, i0, "puzzled", 18)
ry(tavi_gear, i0 + 0.2, 0)
ry(tavi_gear, i0 + 0.8, 140)                                    # xoay xoay
for t, a in ((i0 + 1.0, 18), (i0 + 1.12, 30), (i0 + 1.24, 18), (i0 + 1.36, 30)):   # gật gù
    ry(tavi.head, t, a)
face(tavi, i0 + 1.0, "happy", 18)
h0, h1 = HATCH_OPEN
lean(tavi, h0, 0)
lean(tavi, h0 + 0.3, 15)                                        # cúi vừa phải: mõm ở trên, không che cửa nhỏ
ry(tavi.head, h0 + 0.3, 6)
ry(tavi.arm, h0 + 0.3, -45)
ry(hatch, h0 + 0.2, 0)
ry(hatch, h1, -115)                                             # mở cửa nhỏ, giữ mở một nhịp
look(tavi, h0 + 0.2, 1.0, -0.8)
face(tavi, h0 + 0.2, "eager", 21)
at(tavi.root, GEAR_IN[0], 2.55, 0)
at(tavi.root, GEAR_IN[0] + 0.3, 2.64, 0)
ry(tavi.arm, GEAR_IN[0] + 0.3, -42)
ry(tavi.arm, CLICK - 0.1, -40)
show(tavi_gear, CLICK, False)
show(socket_gear, CLICK, True)                                  # vừa khít: CẠCH
flash(klop, CLICK)
face(tavi, CLICK + 0.05, "happy", 21)
for t, a in ((CLICK + 0.3, 6), (CLICK + 0.45, 16), (CLICK + 0.6, 6)):
    ry(tavi.head, t, a)
ry(tavi.arm, HATCH_CLOSE[0], -48)
ry(hatch, HATCH_CLOSE[0], -115)
ry(hatch, HATCH_CLOSE[1], 0)                                    # đóng cửa
ry(tavi.arm, HATCH_CLOSE[1] + 0.1, 6)
lean(tavi, HATCH_CLOSE[1] + 0.1, 15)
lean(tavi, GOGGLES_UP[0], 0)
at(tavi.root, GOGGLES_UP[0], 2.6, 0)
ry(tavi.head, GOGGLES_UP[0], 6)
ry(tavi.head, GOGGLES_UP[1], 0)
ry(tavi.arm_far, GOGGLES_UP[0] - 0.1, -6)
ry(tavi.arm_far, GOGGLES_UP[0] + 0.15, -150)                    # đẩy kính lên lại
key(tavi.goggles, "location", GOGGLES_UP[0], DOWN)
key(tavi.goggles, "location", GOGGLES_UP[1], (0.0, -0.02, 0.0))
show(tavi.goggle_lens, GOGGLES_UP[0] + 0.2, True)
ry(tavi.arm_far, GOGGLES_UP[1] + 0.1, -6)
face(tavi, GOGGLES_UP[1], "happy")
look(tavi, GOGGLES_UP[1], 0.8, 0.1)
park(tavi, SHOT["S11"][0])
# S14–S15: đứng bên phải vòm xem Lumo; vòm lệch: "Khoan! Lệch rồi!"
enter(tavi, SHOT["S14"][0], 3.35)
facing(tavi, SHOT["S14"][0], -1)
ry(tavi.arm, SHOT["S14"][0], 6)
ry(tavi.head, SHOT["S14"][0], 0)
face(tavi, SHOT["S14"][0], "neutral")
look(tavi, SHOT["S14"][0], 0.8, 0.0)
face(tavi, DOME_UP[0] + 0.2, "shock")
look(tavi, DOME_UP[0] + 0.2, 0.4, 1.0)
ry(tavi.head, DOME_UP[0] + 0.2, -16)
ry(tavi.head, TAVI_STOP[0] - 0.1, 0)
look(tavi, TAVI_STOP[0], 0.9, 0.2)                              # quay sang Lumo
for arm, a, rest in ((tavi.arm, -100, 6), (tavi.arm_far, -95, -6)):   # hai tay chìa ra: khoan!
    ry(arm, TAVI_STOP[0], rest)
    ry(arm, TAVI_STOP[0] + 0.2, a)
    ry(arm, TAVI_STOP[1], a)
    ry(arm, TAVI_STOP[1] + 0.3, rest)
face(tavi, TAVI_STOP[0] + 0.05, "shout")
talk(tavi, TAVI_STOP[0], TAVI_STOP[1], "frown")
face(tavi, TAVI_STOP[1] + 0.05, "worried")
look(tavi, DROP[0], 0.6, -0.4)
face(tavi, DROP[1], "shock")
park(tavi, SHOT["S16"][0])
# S20: đứng bên phải xem vòm lên thẳng
enter(tavi, SHOT["S20"][0], 3.35)
ry(tavi.head, SHOT["S20"][0], -12)
look(tavi, SHOT["S20"][0], 0.5, 0.9)
face(tavi, SHOT["S20"][0], "eager")
face(tavi, FIT, "happy")
# S22–S26: giới thiệu núm, cần gạt, nút đỏ; hô "Không chạm nút đỏ!"
enter(tavi, SHOT["S22"][0], 2.05)
ry(tavi.head, SHOT["S22"][0], 0)
look(tavi, SHOT["S22"][0], 0.8, 0.1)
face(tavi, SHOT["S22"][0], "eager")
ry(tavi.arm, KNOB_POINT - 0.2, 6)
ry(tavi.arm, KNOB_POINT, -100)                                  # núm này: tay chỉ ngang dưới mõm, mắt ngước nhìn núm
ry(tavi.head, KNOB_POINT, -10)
look(tavi, KNOB_POINT, 1.0, 0.5)
ry(tavi.arm, LEVER_POINT - 0.2, -100)
ry(tavi.arm, LEVER_POINT, -70)                                  # cần này (chếch xuống)
ry(tavi.head, LEVER_POINT - 0.2, -10)
ry(tavi.head, LEVER_POINT, 12)
look(tavi, LEVER_POINT, 1.0, -0.6)
face(tavi, LEVER_POINT, "eager", 12)
talk(tavi, TAVI_INTRO[0], TAVI_INTRO[1], "smile")
ry(tavi.arm, TAVI_INTRO[1] + 0.2, -70)
ry(tavi.arm, TAVI_INTRO[1] + 0.4, 6)
ry(tavi.head, TAVI_INTRO[1] + 0.4, 0)
enter(tavi, SHOT["S24"][0], 2.05)
facing(tavi, SHOT["S24"][0], 1)
face(tavi, SHOT["S24"][0], "eager")
ry(tavi.arm, BUTTON_POINT - 0.1, 6)
ry(tavi.arm, BUTTON_POINT + 0.1, -95)                           # nút đỏ to
ry(tavi.head, BUTTON_POINT + 0.1, -10)
look(tavi, BUTTON_POINT, 1.0, 0.1)
flash(button_glint, BUTTON_POINT + 0.15)
talk(tavi, TAVI_MAX[0], TAVI_MAX[1], "smile")
r0, r1 = RAIN_GESTURE                                           # "Mưa to hết cỡ!": giơ hai tay, mười ngón rơi mạnh xuống
key(tavi.arm_far, "location", r0 - HOLD, (-0.01, 0.02, 0.36))
key(tavi.arm_far, "location", r0, (0.0, -0.035, 0.36))           # tay xa lên lớp trước
ry(tavi.arm, r0, -95)
ry(tavi.arm_far, r0, -6)
ry(tavi.arm, r0 + 0.15, -112)
ry(tavi.arm_far, r0 + 0.15, -118)
ry(tavi.head, r0 + 0.15, -14)
face(tavi, r0, "shout")
for i, t in enumerate(steps(r0 + 0.25, r1 - 0.1, 0.1)):
    a = -112 + 7 * i
    ry(tavi.arm, t, a + (8 if i % 2 else -8))
    ry(tavi.arm_far, t, a - 6 + (-8 if i % 2 else 8))
scl(tavi.root, r1 - 0.25, 1, 1)
scl(tavi.root, r1 - 0.1, 1.05, 0.94)                            # nhún theo
scl(tavi.root, r1 + 0.05, 1, 1)
ry(tavi.arm, r1 + 0.1, -50)
ry(tavi.arm_far, r1 + 0.1, -55)
ry(tavi.arm, r1 + 0.35, 6)
ry(tavi.arm_far, r1 + 0.35, -6)
ry(tavi.head, r1 + 0.1, 0)
key(tavi.arm_far, "location", r1 + 0.35, (0.0, -0.035, 0.36))
key(tavi.arm_far, "location", r1 + 0.35 + HOLD, (-0.01, 0.02, 0.36))
face(tavi, TAVI_MAX[1] + 0.2, "happy")
facing(tavi, TAVI_MAX[1] + 0.5, -1, 0.15)                       # quay sang Lumo, Nori: không thấy Piko
look(tavi, TAVI_MAX[1] + 0.6, 0.8, 0.1)
facing(tavi, SHOUT[0], 1, 0.12)
ry(tavi.arm, SHOUT[0], 6)
ry(tavi.arm, SHOUT[0] + 0.15, -100)                             # một tay chìa ra: dừng!
face(tavi, SHOUT[0], "shout")
talk(tavi, SHOUT[0], SHOUT[1], "frown")
ry(tavi.arm, SHOUT[1] + 0.2, -100)
ry(tavi.arm, SHOUT[1] + 0.5, 6)
face(tavi, SHOUT[1] + 0.3, "neutral")
park(tavi, SHOT["S27"][0])

# ================================================================ Lumo
loop(lumo.tail, 0.0, SECONDS, 0.5, 6, 22)
face(lumo, 0.0, "eager")
ry(lumo.arm, 0.0, 6)
ry(lumo.arm_far, 0.0, -6)
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, 0.0, 6)
walk(lumo.root, ARRIVE[0], ARRIVE[1] - 0.2, -1.4, 3.05, 8, 0.06)   # chạy ra tận mép đồi
lean(lumo, ARRIVE[1] - 0.2, 0)
lean(lumo, ARRIVE[1], 18)                                       # nhìn xuống vườn mầm
ry(lumo.head, ARRIVE[1], 14)
look(lumo, ARRIVE[1], 0.8, -0.9)
face(lumo, ARRIVE[1], "eager", 32)
park(lumo, SHOT["S2"][0])
# S4: hăm hở đưa đồ, dúi nhầm cái búa
enter(lumo, SHOT["S4"][0], 1.3)
lean(lumo, SHOT["S4"][0], 0)
ry(lumo.head, SHOT["S4"][0], 0)
look(lumo, SHOT["S4"][0], 0.8, -0.2)
face(lumo, SHOT["S4"][0], "eager")
show(hammer_lumo, SHOT["S4"][0], True)
ry(lumo.arm, SHOT["S4"][0], -20)
at(lumo.root, LUMO_HAMMER[0], 1.3, 0)
at(lumo.root, LUMO_HAMMER[0] + 0.15, 1.34, 0.05)
at(lumo.root, LUMO_HAMMER[0] + 0.3, 1.38, 0)
ry(lumo.arm, LUMO_HAMMER[0], -20)
ry(lumo.arm, LUMO_HAMMER[0] + 0.3, -45)                         # dúi cái búa vào tay Tavi
show(hammer_lumo, LUMO_HAMMER[1] - 0.1, False)
ry(lumo.arm, LUMO_HAMMER[1] + 0.2, 6)
face(lumo, LUMO_HAMMER[1] + 0.2, "happy")                       # hớn hở, không biết mình đưa nhầm
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, LUMO_HAMMER[1] + 0.2, 16)
face(lumo, TAVI_SWAP[0] + 0.6, "eager")
ry(lumo.head, TAVI_SWAP[0] + 0.8, -8)                           # nghiêng đầu nhìn Tavi
park(lumo, SHOT["S5"][0])
# S7: ngắm máy
enter(lumo, SHOT["S7"][0], 0.8)
ry(lumo.head, SHOT["S7"][0], -16)
look(lumo, SHOT["S7"][0], 0.7, 0.8)
face(lumo, SHOT["S7"][0], "happy")
park(lumo, SHOT["S8"][0])
# S11: mải ngắm máy, không biết la bàn rung trong túi
enter(lumo, SHOT["S11"][0], 1.15)
ry(lumo.head, SHOT["S11"][0], -22)
look(lumo, SHOT["S11"][0], 0.6, 1.0)
face(lumo, SHOT["S11"][0], "happy", -22)
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, SHOT["S11"][0], 12)
c0, c1 = COMPASS_PEEK
show(peek, c0, True)
key(peek, "location", c0, (0.1, 0.002, 0.2))
key(peek, "location", c0 + 0.3, (0.11, 0.002, 0.27))            # ló khỏi miệng túi
flash(tit, c0, 0.8)                                             # TÍT
show(peek, SHOT["S11"][1], False)
park(lumo, SHOT["S13"][0])
# S14: chộp móc, móc vội vào mép vòm, chạy vòng nắm đầu dây
enter(lumo, SHOT["S14"][0], 2.45)
ry(lumo.head, SHOT["S14"][0], 0)
look(lumo, SHOT["S14"][0], 0.6, 0.9)
face(lumo, SHOT["S14"][0], "eager")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, SHOT["S14"][0], 12)
k0, k1 = HOOK_GRAB
scl(lumo.root, k0, 1, 1)
scl(lumo.root, k0 + 0.12, 1.05, 0.9)                            # nhún lấy đà
at(lumo.root, k0 + 0.12, 2.45, 0)
scl(lumo.root, k0 + 0.25, 0.97, 1.04)
at(lumo.root, k0 + 0.3, 2.45, 0.25)                              # nhảy chộp cái móc
ry(lumo.arm, k0 + 0.1, 6)
ry(lumo.arm, k0 + 0.3, -150)
at(lumo.root, k1 - 0.05, 2.45, 0)
scl(lumo.root, k1, 1, 1)
ry(lumo.arm, k1 - 0.05, -120)
o0, o1 = HOOK_ON
lean(lumo, o0, 0)
at(lumo.root, o0, 2.45, 0)
at(lumo.root, o0 + 0.2, 2.35, 0.03)                              # lùi một bước
at(lumo.root, o0 + 0.4, 2.35, 0)
lean(lumo, o0 + 0.4, 45)                                        # chồm xuống móc vào mép vòm
ry(lumo.arm, o0, -120)
ry(lumo.arm, o0 + 0.4, -40)
ry(lumo.head, o0, 0)
ry(lumo.head, o0 + 0.4, -30)
look(lumo, o0 + 0.1, -0.8, 1.0)                                 # mắt còn ngước nhìn nóc máy
lean(lumo, o1, 45)
lean(lumo, o1 + 0.15, 0)
ry(lumo.head, o1 + 0.15, 0)
ry(lumo.arm, o1 + 0.15, 6)
q0, q1 = LUMO_TO_ROPE
facing(lumo, q0 + 0.15, -1, 0.12)
walk(lumo.root, q0 + 0.15, q0 + 0.55, 2.35, 1.25, 4, 0.05)
facing(lumo, q0 + 0.68, 1, 0.12)
look(lumo, q0 + 0.6, 0.4, 0.3)
for arm, rest in ((lumo.arm, 6), (lumo.arm_far, -6)):           # nắm dây bằng hai tay ngang ngực
    ry(arm, q0 + 0.55, rest)
    ry(arm, q1 - 0.05, -80)
talk(lumo, LUMO_LINE[0], LUMO_LINE[1], "smile")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, LUMO_LINE[0], 16)
# S15: chạy lùi phăng phăng; Tavi hô khoan; thả dây; nhìn vòm rồi nhìn Tavi
RUN = [(LUMO_RUN[0], 1.25), (LUMO_RUN[1], 0.35)]
lean(lumo, LUMO_RUN[0], 0)
lean(lumo, LUMO_RUN[0] + 0.2, -12)                              # ngả người kéo
face(lumo, LUMO_RUN[0], "squint")
run_xz = []
for i, t in enumerate(steps(LUMO_RUN[0], LUMO_RUN[1], 0.1)):
    x, z = ease(RUN, t)[0], 0.04 if i % 2 else 0.0
    at(lumo.root, t, x, z)
    run_xz.append((t, x, z))
face(lumo, TAVI_STOP[0] + 0.1, "shock")
look(lumo, TAVI_STOP[0] + 0.1, 0.8, 0.2)
lean(lumo, DROP[0], -12)
for arm, rest in ((lumo.arm, 6), (lumo.arm_far, -6)):           # thả dây
    ry(arm, DROP[0], -80)
    ry(arm, DROP[0] + 0.15, rest)
lean(lumo, DROP[0] + 0.2, 0)
face(lumo, DROP[1], "sheepish")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, DROP[1], -50)
look(lumo, DROP[1] + 0.2, 0.8, -0.2)                            # nhìn cái vòm…
look(lumo, DROP[1] + 0.7, 0.8, 0.1)                             # …rồi nhìn Tavi
park(lumo, SHOT["S16"][0])
# S20: kéo lại, vòm lên thẳng tắp, KHỚP
enter(lumo, SHOT["S20"][0], 1.25)
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, SHOT["S20"][0], 12)
for arm in (lumo.arm, lumo.arm_far):
    ry(arm, SHOT["S20"][0], -80)
face(lumo, SHOT["S20"][0], "eager")
look(lumo, SHOT["S20"][0], 0.6, 0.6)
lean(lumo, LIFT2[0], 0)
lean(lumo, LIFT2[0] + 0.2, -10)
RUN2 = [(LIFT2[0], 1.25), (LIFT2[0] + 1.6, 0.75)]
for i, t in enumerate(steps(LIFT2[0], LIFT2[0] + 1.6, 0.1)):
    at(lumo.root, t, ease(RUN2, t)[0], 0.035 if i % 2 else 0.0)
lean(lumo, FIT, -10)
lean(lumo, FIT + 0.2, 0)
face(lumo, FIT + 0.05, "happy")
at(lumo.root, FIT + 0.1, 0.75, 0)
at(lumo.root, FIT + 0.3, 0.75, 0.1)                             # nhảy cẫng
at(lumo.root, FIT + 0.5, 0.75, 0)
# S22–S26: nghe giới thiệu, hô "Không chạm nút đỏ!"
enter(lumo, SHOT["S22"][0], 1.3)
for arm, rest in ((lumo.arm, 6), (lumo.arm_far, -6)):
    ry(arm, SHOT["S22"][0], rest)
look(lumo, SHOT["S22"][0], 0.8, 0.0)
face(lumo, SHOT["S22"][0], "eager")
face(lumo, SHOUT[0], "shout")
ry(lumo.arm, SHOUT[0], 6)
ry(lumo.arm, SHOUT[0] + 0.15, -95)                              # một tay chìa ra: dừng!
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, SHOUT[0], 16)
talk(lumo, SHOUT[0], SHOUT[1], "frown")
ry(lumo.arm, SHOUT[1] + 0.3, 6)
face(lumo, SHOUT[1] + 0.3, "eager")
park(lumo, SHOT["S27"][0])

# ================================================================ Piko
face(piko, 0.0, "eager")
ry(piko.arm, 0.0, 6)
for i, t in enumerate(steps(ARRIVE[0], ARRIVE[1], 0.25)):       # nảy theo cả nhóm lên đỉnh đồi
    at(piko.root, t, -1.7 + (0.15 + 1.7) * (t - ARRIVE[0]) / (ARRIVE[1] - ARRIVE[0]), 0.06 if i % 2 else 0.0)
loop(piko.bag, 0.0, SECONDS, 1.2, -6, 6)
park(piko, SHOT["S2"][0])
# S6: ngồi phịch lên hộp ốc, ốc dính lên thân, Tavi gỡ từng con
enter(piko, SHOT["S6"][0], -0.55)
p0, p1 = PIKO_SIT
at(piko.root, p0, -0.55, 0)
at(piko.root, p0 + 0.2, -0.2, 0.12)
at(piko.root, p0 + 0.4, 0.15, 0.0)
at(piko.root, p0 + 0.55, 0.42, 0.16)
at(piko.root, p0 + 0.6, 0.45, 0.0)                              # ngồi phịch
scl(piko.root, p0 + 0.55, 1, 1)
scl(piko.root, p0 + 0.65, 1.25, 0.72)
scl(piko.root, p1 + 0.2, 1.12, 0.86)
for ob in rows:
    show(ob, p0 + 0.6, False)                                   # ốc dính hết lên người Piko
face(piko, p0 + 0.65, "happy")
u0, u1 = PIKO_UP
scl(piko.root, u0, 1.12, 0.86)
scl(piko.root, u0 + 0.2, 1, 1)
at(piko.root, u0, 0.45, 0)
at(piko.root, u0 + 0.3, 0.26, 0.08)
at(piko.root, u1, 0.08, 0)
for ob in stuck:
    show(ob, u0 + 0.05, True)
face(piko, u1, "puzzled")
look(piko, u1, -0.6, -0.4)
for t, ob in zip(POPS, stuck):                                  # PÓC: rung một cái mỗi lần gỡ
    show(ob, t, False)
    at(poc, t, 0.08 + ob.location.x - 0.03, ob.location.z)
    flash(poc, t, 0.8)
    scl(piko.root, t, 1, 1)
    scl(piko.root, t + 0.08, 1.06, 0.94)
    scl(piko.root, t + 0.2, 1, 1)
    mouth(piko, t, "o")
    mouth(piko, t + 0.25, "closed")
face(piko, POPS[2] + 0.3, "happy")
# S7: nảy nhẹ ngắm máy
enter(piko, SHOT["S7"][0], 0.2)
bob(piko.root, SHOT["S7"][0], SHOT["S7"][1], 0.2, 0.8, 0.03)
face(piko, SHOT["S7"][0], "eager")
look(piko, SHOT["S7"][0], 0.6, 0.6)
park(piko, SHOT["S8"][0])
# S9: thò tay vào túi "giúp", rút ra con vịt ngậm bánh răng vàng
enter(piko, SHOT["S9"][0], 0.65)
face(piko, SHOT["S9"][0], "eager")
look(piko, SHOT["S9"][0], 0.8, 0.2)
h0, h1 = PIKO_HELP
ry(piko.arm, h0, 6)
ry(piko.arm, h0 + 0.25, -27)                                    # thò tay xuống túi ở hông
loop(piko.arm, h0 + 0.35, h1, 0.22, -20, -34)                   # lục lọi
look(piko, h0 + 0.2, 0.9, -0.5)
lean(piko, h0 + 0.2, 8)
key(piko.arm, "location", DUCK_OUT - HOLD, (0.24, -0.029, 0.22))
key(piko.arm, "location", DUCK_OUT, (0.24, -0.035, 0.22))       # tay lên lớp trước túi
show(duck, DUCK_OUT, True)
show(gear_glint, DUCK_OUT, False)
ry(piko.arm, DUCK_OUT + 0.25, -115)                             # giơ con vịt lên
lean(piko, DUCK_OUT + 0.2, 0)
face(piko, DUCK_OUT + 0.1, "happy")
look(piko, DUCK_OUT + 0.2, 1.0, 0.3)
twinkle(gear_glint, GEAR_GLINT[0], GEAR_GLINT[1])
show(duck_gear, TAVI_TAKE[0] + 0.3, False)                      # Tavi gỡ bánh răng
face(piko, TAVI_TAKE[1], "eager")
park(piko, SHOT["S10"][0])
# S13: ôm chặt con vịt vào bụng: "Để dành!"
enter(piko, SHOT["S13"][0], 0.62)
show(duck, SHOT["S13"][0], False)
show(duck_hug, SHOT["S13"][0], True)
key(piko.arm, "location", SHOT["S13"][0], (0.24, -0.045, 0.22)) # tay trước con vịt
ry(piko.arm, SHOT["S13"][0], -40)
hg0, hg1 = PIKO_HUG
ry(piko.arm, hg0, -40)
ry(piko.arm, hg0 + 0.2, 35)                                     # quặp tay ôm vịt
scl(piko.root, hg0, 1, 1)
scl(piko.root, hg0 + 0.25, 1.08, 0.92)                          # thân bóp quanh con vịt
lean(piko, hg0, 0)
lean(piko, hg0 + 0.25, -8)                                      # hơi né đi
face(piko, hg0 + 0.1, "happy")
talk(piko, PIKO_LINE[0], PIKO_LINE[1], "smile")
scl(piko.root, PIKO_LINE[1], 1.08, 0.92)
park(piko, SHOT["S14"][0])
# S20: ôm vịt đứng xem vòm lên
enter(piko, SHOT["S20"][0], 0.22)
lean(piko, SHOT["S20"][0], 0)
scl(piko.root, SHOT["S20"][0], 1, 1)
bob(piko.root, SHOT["S20"][0], SHOT["S20"][1], 0.22, 0.8, 0.02)
face(piko, SHOT["S20"][0], "eager")
look(piko, SHOT["S20"][0], 0.6, 1.0)
face(piko, FIT + 0.1, "happy")
# S22–S27: nút đỏ lấp lánh, mắt lấp lánh, vươn người lần tay tới; cả nhóm hô; rụt tay, giấu ra sau, cười toe
enter(piko, SHOT["S22"][0], 3.3)
facing(piko, SHOT["S22"][0], -1)
show(duck_hug, SHOT["S22"][0], False)
ry(piko.arm, SHOT["S22"][0], 6)
key(piko.arm, "location", SHOT["S22"][0], (0.24, -0.029, 0.22))
face(piko, SHOT["S22"][0], "eager")
bob(piko.root, SHOT["S22"][0], PIKO_CREEP[0] - 0.1, 3.3, 0.9, 0.02)
look(piko, SHOT["S22"][0], 0.8, 0.2)
look(piko, BUTTON_POINT + 0.2, 1.0, 0.0)
e0, e1 = PIKO_EYES
for ob in sparkle:
    twinkle(ob, e0, e1)
face(piko, e0, "eager")
twinkle(button_glint, BUTTON_GLINT[0], BUTTON_GLINT[1])
w0, w1 = PIKO_CREEP
at(piko.root, w0, 3.3, 0)
at(piko.root, w1, 2.68, 0)                                      # trườn dần tới, sát thân máy
scl(piko.root, w0, -1, 1)
scl(piko.root, w1, -0.85, 1.4)                                  # thân thạch vươn cao
scl(piko.root, SHOUT[0], -0.85, 1.4)
ry(piko.arm, w0, 6)
ry(piko.arm, w1, -140)
scl(piko.arm, w0, 1, 1)
scl(piko.arm, w1, 1, 1.3)                                       # tay lần tới… sát mép nút, khựng lại
lean(piko, w0, 0)
lean(piko, w1, 6)
face(piko, SHOUT[0] + 0.05, "shock")                            # cả nhóm hô: khựng lại
look(piko, SHOUT[0] + 0.05, -0.6, 0.0)
x0, x1 = PIKO_HIDE
scl(piko.root, x0, -0.85, 1.4)
scl(piko.root, x0 + 0.25, -1.06, 0.92)
scl(piko.root, x0 + 0.45, -1, 1)
scl(piko.arm, x0, 1, 1.3)
scl(piko.arm, x0 + 0.25, 1, 1)
ry(piko.arm, x0, -140)
ry(piko.arm, x0 + 0.3, 60)                                      # giấu tay ra sau lưng
key(piko.arm, "location", x0 + 0.3 - HOLD, (0.24, -0.029, 0.22))
key(piko.arm, "location", x0 + 0.3, (0.24, 0.02, 0.22))
lean(piko, x0 + 0.3, 0)
g0 = PIKO_TOOTHY[0]
face(piko, g0, "happy")                                         # cười toe: miệng cười kéo rộng
scl(piko.mouths["smile"], 0.0, 1, 1)
scl(piko.mouths["smile"], g0, 1, 1)
scl(piko.mouths["smile"], g0 + 0.15, 1.8, 1.5)
look(piko, g0, 0.6, 0.0)
bob(piko.root, g0, SECONDS, 2.68, 0.6, 0.02)

# ================================================================ Nori
for i in range(int(SECONDS) + 1):
    at(nori.root, i, 0.0, 0.03 if i % 2 else -0.03)
for a in nori.antennae:
    loop(a, 0.0, SECONDS, 1.4, -6, 6)
d0, d1 = NORI_DROOP
for w, phase in zip(nori.wings, (0.06, 0.0)):                   # cánh vỗ; rũ xuống khi thấy hộp ốc trống trơn
    loop(w, phase, d0, 0.24, -14, 14)
    ry(w, d0 + 0.3, -80)                                        # cánh chúc xuống
    ry(w, d1, -80)
    loop(w, NORI_RESORT[0] + phase, SECONDS, 0.24, -14, 14)
face(nori, 0.0, "eager")
ry(nori.arm, 0.0, 6)
at(nori_path, 0.0, -1.0, 1.25)
at(nori_path, ARRIVE[0], -1.0, 1.25)
at(nori_path, ARRIVE[1] + 0.2, 0.6, 1.15)
park(nori, SHOT["S2"][0])
# S5: xếp ốc theo cỡ, tay chạm hộp mỗi hàng
enter(nori, SHOT["S5"][0], 0.74, 0.4)
facing(nori, SHOT["S5"][0], -1)
look(nori, SHOT["S5"][0], 0.6, -0.9)
face(nori, SHOT["S5"][0], "eager", 10)
lean(nori, SHOT["S5"][0], 10)
for ob in rows:
    show(ob, SHOT["S5"][0] - HOLD, False)
for ob, t in zip(rows, (NORI_SORT[0] + 0.3, NORI_SORT[0] + 1.0, NORI_SORT[0] + 1.7)):   # to, vừa, nhỏ
    ry(nori.arm, t - 0.25, 6)
    ry(nori.arm, t, -40)                                        # tay chạm xuống hộp
    show(ob, t, True)
    scl(ob, t, 1, 0.3)
    scl(ob, t + 0.12, 1, 1.3)                                   # hàng ốc nảy lên
    scl(ob, t + 0.25, 1, 1)
    ry(nori.arm, t + 0.2, 6)
face(nori, NORI_SORT[1], "happy")
# S6: tránh lên cao khi Piko nảy tới; rũ cánh; nhận từng con ốc Tavi gỡ ra, xếp lại
at(nori_path, PIKO_SIT[0], 0.74, 0.4)
at(nori_path, PIKO_SIT[0] + 0.4, 0.88, 0.62)                     # tránh lên cao khi Piko nảy tới
lean(nori, PIKO_SIT[0], 10)
lean(nori, PIKO_SIT[0] + 0.3, 0)
face(nori, PIKO_SIT[0] + 0.65, "shock")
look(nori, PIKO_SIT[0] + 0.65, 0.9, -0.3)
face(nori, d0, "sad")
look(nori, d0, 0.5, -0.9)
lean(nori, d0, 0)
lean(nori, d0 + 0.3, 12)
for a in nori.antennae:
    ry(a, d0 + 0.3, 20)
lean(nori, d1, 6)
at(nori_path, POPS[0] - 0.4, 0.88, 0.62)
at(nori_path, POPS[0] - 0.1, 0.74, 0.4)                          # xuống sát hộp ốc
face(nori, NORI_RESORT[0], "neutral")
look(nori, NORI_RESORT[0], 0.9, 0.1)
for ob, t, (sx, sz) in zip(rows, POPS, STUCK):                  # mỗi con ốc gỡ ra bay sang tay Nori rồi vào hộp
    show(pop_fly, t, True)
    at(pop_fly, t, 0.08 + sx, sz)
    at(pop_fly, t + 0.2, 0.35, 0.75)
    at(pop_fly, t + 0.38, 0.66, 0.22)
    show(pop_fly, t + 0.4, False)
    ry(nori.arm, t + 0.15, 6)
    ry(nori.arm, t + 0.38, -60)                                 # đón ốc
    ry(nori.arm, t + 0.5, -40)                                  # đặt vào hộp
    show(ob, t + 0.5, True)
    scl(ob, t + 0.5, 1, 0.3)
    scl(ob, t + 0.6, 1, 1.2)
    scl(ob, t + 0.7, 1, 1)
    look(nori, t + 0.05, 0.9, 0.1)
    look(nori, t + 0.45, 0.3, -1.0)
ry(nori.arm, NORI_RESORT[1], 6)
lean(nori, NORI_RESORT[1], 0)
# S7: ngắm máy
enter(nori, SHOT["S7"][0], 0.75, 1.15)
facing(nori, SHOT["S7"][0], 1)
face(nori, SHOT["S7"][0], "happy")
look(nori, SHOT["S7"][0], 0.8, -0.2)
park(nori, SHOT["S8"][0])
# S15: lơ lửng góc trên, nhăn mặt khi vòm chao đảo
enter(nori, SHOT["S15"][0], 1.0, 1.55)
face(nori, SHOT["S15"][0], "eager")
look(nori, SHOT["S15"][0], 0.8, -0.4)
face(nori, DOME_WOBBLE[0] + 0.2, "worried")
look(nori, DOME_WOBBLE[0] + 0.2, 0.9, -0.3)
face(nori, DROP[1], "shock")
# S16–S18: Story Lens: bập bênh, "Chỗ này mới cân."
enter(nori, SHOT["S16"][0], 1.45, 0.82)
face(nori, SHOT["S16"][0], "eager")
look(nori, SHOT["S16"][0], 0.8, 0.0)
l0, l1 = LENS_UP
show(lens, l0 - 0.05, True)
key(lens, "location", l0, (0.13, -0.03, -0.2))
key(lens, "location", l1, (0.1, -0.03, 0.04))                   # đưa mặt kính lên mắt
ry(nori.arm, l0, 6)
ry(nori.arm, l1, -150)
enter(nori, SHOT["S18"][0], 2.45, 0.8)
n0, n1 = NORI_COMPARE
key(lens, "location", n0 + 0.4, (0.1, -0.03, 0.04))
key(lens, "location", n0 + 0.7, (0.13, -0.03, -0.18))           # hạ kính, nhìn vòm kính
ry(nori.arm, n0 + 0.4, -150)
ry(nori.arm, n0 + 0.7, 6)
look(nori, n0, 0.6, 0.0)
look(nori, n0 + 0.7, 0.8, -0.8)
show(lens, NORI_POINT[0], False)
at(nori_path, NORI_POINT[0], 2.45, 0.8)
at(nori_path, NORI_POINT[1], 2.7, 0.68)                         # bay sát đỉnh vòm
ry(nori.arm, NORI_POINT[0], 6)
ry(nori.arm, NORI_POINT[1], -40)                                # chỉ xuống giữa đỉnh vòm
lean(nori, NORI_POINT[0], 0)
lean(nori, NORI_POINT[1], 18)
twinkle(balance_spot, NORI_POINT[1], HOOK_MOVE[1])
talk(nori, NORI_LINE[0], NORI_LINE[1], "smile")
ry(nori.arm, NORI_LINE[1] + 0.2, -40)
ry(nori.arm, NORI_LINE[1] + 0.4, 6)
lean(nori, NORI_LINE[1] + 0.4, 0)
# S20: bay cao xem vòm lên thẳng, rồi ngó xuống chân đồi (dẫn sang Wonder Hub)
enter(nori, SHOT["S20"][0], 3.45, 1.35)
facing(nori, SHOT["S20"][0], -1)
look(nori, SHOT["S20"][0], 0.8, -0.6)
face(nori, FIT, "happy")
facing(nori, NORI_LOOK_DOWN, 1, 0.15)
look(nori, NORI_LOOK_DOWN + 0.1, 0.8, -1.0)
lean(nori, NORI_LOOK_DOWN, 0)
lean(nori, NORI_LOOK_DOWN + 0.2, 14)
face(nori, NORI_LOOK_DOWN + 0.1, "eager", 14)
# S22–S26
enter(nori, SHOT["S22"][0], 1.06, 1.08)
lean(nori, SHOT["S22"][0], 0)
face(nori, SHOT["S22"][0], "eager")
look(nori, SHOT["S22"][0], 0.8, -0.3)
face(nori, SHOUT[0], "shout")
ry(nori.arm, SHOUT[0], 6)
ry(nori.arm, SHOUT[0] + 0.15, -80)
talk(nori, SHOUT[0], SHOUT[1], "frown")
ry(nori.arm, SHOUT[1] + 0.3, 6)
face(nori, SHOUT[1] + 0.3, "neutral")
park(nori, SHOT["S27"][0])

# ================================================================ vòm kính, móc, hai đoạn dây
LIFT1 = [(DOME_UP[0], 2.95, 0.0, 0.0), (DOME_UP[0] + 0.2, 2.93, 0.12, 25), (DOME_UP[0] + 0.5, 2.88, 0.4, 45),
         (DOME_UP[0] + 0.9, 2.7, 0.85, 55), (DOME_UP[1], 2.45, 1.32, 62)]
WOBBLE = [(DOME_WOBBLE[0], 2.45, 1.32, 62), (DOME_WOBBLE[0] + 0.4, 2.42, 1.36, 46), (DOME_WOBBLE[0] + 0.8, 2.47, 1.33, 72),
          (DOME_WOBBLE[0] + 1.2, 2.43, 1.36, 50), (DOME_WOBBLE[0] + 1.6, 2.46, 1.34, 66), (DROP[0], 2.45, 1.35, 58)]
FALL = [(DROP[0], 2.45, 1.35, 58), (DROP[0] + 0.25, 2.75, 0.75, 30), (DROP[1], 2.95, 0.0, 0.0)]
LIFT2K = [(LIFT2[0], 2.95, 0.0, 0.0), (LIFT2[0] + 0.8, 2.95, 0.9, 3), (LIFT2[0] + 1.3, 2.6, 1.42, -4), (LIFT2[0] + 1.8, 2.05, 1.38, 2),
          (FIT, 2.0, 1.125, 0.0)]


def dome_point(x, z, th, pt):
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))
    return (x + pt[0] * c + pt[1] * s, z - pt[0] * s + pt[1] * c)


hook_keys, dome_keys = [], []                                   # (t, x, z) của móc; (t, x, z, góc) của vòm
dome_keys += [(0.0, 2.95, 0.0, 0.0), (DOME_UP[0], 2.95, 0.0, 0.0)]
hook_keys += [(SHOT["S7"][0], 2.58, 0.9), (k0 + 0.28, 2.58, 0.9)]
lumo.dir = 1
for t, a, zz in ((k0 + 0.3, -150, 0.25), (k1 - 0.05, -120, 0.0), (o0, -120, 0.0)):   # móc theo tay Lumo
    hook_keys.append((t, *hand(lumo, 2.45, zz, a)))
hook_keys.append((o0 + 0.4, *hand(lumo, 2.35, 0.0, -40, 45)))
hook_keys.append((o0 + 0.5, *dome_point(2.95, 0.0, 0.0, H_RIM)))
for keys in (LIFT1, WOBBLE, FALL):
    for t in steps(keys[0][0], keys[-1][0], 0.05):
        x, z, th = ease(keys, t)
        dome_keys.append((t, x, z, th))
        hook_keys.append((t, *dome_point(x, z, th, H_RIM)))
dome_keys += [(DROP[1] + 0.08, 2.95, 0.04, -3), (DROP[1] + 0.18, 2.95, 0.0, 0.0), (LIFT2[0], 2.95, 0.0, 0.0)]
hook_keys.append((HOOK_MOVE[0], *dome_point(2.95, 0.0, 0.0, H_RIM)))
hook_keys.append((HOOK_MOVE[0] + 0.5, 2.82, 0.42))              # dời móc (trong cú cận ở X = 70)
hook_keys.append((HOOK_MOVE[1], *dome_point(2.95, 0.0, 0.0, H_TOP)))
for t in steps(LIFT2K[0][0], LIFT2K[-1][0], 0.05):
    x, z, th = ease(LIFT2K, t)
    dome_keys.append((t, x, z, th))
    hook_keys.append((t, *dome_point(x, z, th, H_TOP)))
dome_keys.append((SECONDS, 2.0, 1.125, 0.0))
hook_keys.append((SECONDS, *dome_point(2.0, 1.125, 0.0, H_TOP)))
for t, x, z, th in dome_keys:
    at(dome, t, x, z)
    ry(dome, t, th)
for t, x, z in hook_keys:
    at(hook, t, x, z)
    seg_to(rope_r, t, PULLEY_R, (x, z + 0.03))
puff(dust, DROP[1], 1.0)                                        # BỊCH
scl(dome, DROP[1], 1, 1)
scl(dome, DROP[1] + 0.06, 1.06, 0.9)
scl(dome, DROP[1] + 0.2, 1, 1)
scl(dome, FIT, 1, 1)
scl(dome, FIT + 0.06, 1.05, 0.92)
scl(dome, FIT + 0.2, 1, 1)
flash(khop, FIT, 1.2)                                           # KHỚP!

# đầu dây bên trái: buông thõng ngoài mép thân máy, Lumo nắm và chạy lùi, thả ra, nắm lại
lumo.dir = 1
IDLE_END = (1.38, 0.5)
end_keys = [(SHOT["S7"][0], *IDLE_END), (q1 - 0.07, *IDLE_END)]
end_keys.append((q1 - 0.05, *hand(lumo, 1.25, 0.0, -80)))
end_keys.append((LUMO_RUN[0], *hand(lumo, 1.25, 0.0, -80)))
for t, x, z in run_xz:
    end_keys.append((t, *hand(lumo, x, z, -80, -12)))
end_keys.append((DROP[0], *hand(lumo, 0.35, 0.0, -80, -12)))
end_keys.append((DROP[1], 1.55, 1.25))                          # buông: đầu dây vụt lên
end_keys.append((SHOT["S20"][0] - HOLD, 1.55, 1.25))
end_keys.append((SHOT["S20"][0], *hand(lumo, 1.25, 0.0, -80)))
end_keys.append((LIFT2[0], *hand(lumo, 1.25, 0.0, -80)))
for i, t in enumerate(steps(LIFT2[0], LIFT2[0] + 1.6, 0.1)):
    end_keys.append((t, *hand(lumo, ease(RUN2, t)[0], 0.035 if i % 2 else 0.0, -80, -10)))
end_keys.append((SHOT["S22"][0] - HOLD, *hand(lumo, 0.75, 0.0, -80, -10)))
end_keys.append((SHOT["S22"][0], *IDLE_END))
end_keys.append((SECONDS, *IDLE_END))
for t, x, z in end_keys:
    seg_to(rope_l, t, PULLEY_L, (x, z))

# ================================================================ các cú cận dựng riêng
# S12: la bàn ló khỏi túi da, ngôi sao quay rồi chỉ về vòm kính có bánh răng vàng
t0, t1 = SHOT["S12"]
key(peek_big, "location", 0.0, (59.75, 0.85, -0.12))
key(peek_big, "location", t0, (59.75, 0.85, -0.04))
key(peek_big, "location", t0 + 0.35, (59.75, 0.85, 0.1))        # ló khỏi miệng túi
flash(peek_tit, t0, 1.0)                                        # TÍT
ry(peek_big_star, 0.0, 0)
ry(peek_big_star, t0, 0)
ry(peek_big_star, STAR_TURN[0], 220)                            # quay…
ry(peek_big_star, STAR_TURN[1], 112)                            # …rồi chỉ về vòm kính
ry(peek_big_star, STAR_TURN[1] + 0.12, 118)
ry(peek_big_star, STAR_TURN[1] + 0.24, 112)
flash(peek_dome_glint, DOME_GLINT, 1.2)
# S19: tay Tavi dời móc từ mép vòm tới giữa đỉnh vòm, điểm sáng nhấp nháy
m0, m1 = HOOK_MOVE
BIG_MID = (BIG_RIM[0] + 0.18, BIG_TOP[1] - 0.05)
HOOK_PATH = [(SHOT["S19"][0], *BIG_RIM), (m0, *BIG_RIM), (m0 + 0.5, *BIG_MID), (m1, *BIG_TOP), (SHOT["S19"][1], *BIG_TOP)]
SHOULDER, ROPE_TOP = (69.25, 0.62), (70.2, 0.62)
for t in steps(SHOT["S19"][0], SHOT["S19"][1], 0.05):
    hx, hz = ease(HOOK_PATH, t)
    at(big_hook, t, hx, hz)
    seg_to(big_rope, t, ROPE_TOP, (hx + 0.06, hz + 0.05))
    seg_to(big_arm, t, SHOULDER, (hx - 0.04, hz + 0.04))
    at(big_hand, t, hx - 0.04, hz + 0.04)
twinkle(big_spot, SHOT["S19"][0], SHOT["S19"][1])

# --- cổng truyện le lói; bập bênh trong mặt kính
for i, t in enumerate(steps(0.0, SECONDS, 0.35)):
    s = 1.0 if i % 2 else 0.75
    scl(far_portal, t, s, s)
for i, t in enumerate(steps(0.0, SECONDS, 0.3)):                # đang khép dần, le lói
    k = 1.0 - 0.3 * min(1.0, max(0.0, (t - HUB_GLOW[0]) / 3.0))
    s = k * (1.0 if i % 2 else 0.86)
    scl(portal, t, s, s)
ry(portal, 0.0, 0)
ry(portal, SECONDS, 720)
show(seesaw, 0.0, False)
show(seesaw, LENS_IMAGE[0], True)
show(lens_dot, LENS_IMAGE[0], False)
scl(seesaw, LENS_IMAGE[0], 0.2, 0.2)
scl(seesaw, LENS_IMAGE[1], 1, 1)
for t, a in ((LENS_IMAGE[0], 22), (LENS_IMAGE[1], 22), (LENS_IMAGE[1] + 0.2, -8), (LENS_BALANCE - 0.1, 4), (LENS_BALANCE, 0)):
    ry(plank, t, a)                                             # chao rồi nằm thăng bằng
twinkle(lens_dot, LENS_BALANCE, SHOT["S17"][1])

# ================================================================ máy quay, render
CAMS = {"S1": (1.75, 0.45, 6.4), "S2": (0.85, 0.38, 1.9), "S3": (1.95, 0.55, 2.1), "S4": (1.5, 0.38, 1.9),
        "S5": (0.55, 0.3, 1.6), "S6": (0.2, 0.36, 2.3), "S7": (2.0, 0.85, 3.8), "S8": (1.2, 0.36, 1.5),
        "S9": (0.98, 0.36, 1.6), "S10": (2.78, 0.36, 1.6), "S11": (1.3, 0.55, 1.8), "S12": (60.0, 0.0, 1.6),
        "S13": (0.62, 0.38, 1.2), "S14": (2.0, 0.43, 2.6), "S15": (1.75, 0.9, 3.8), "S16": (1.45, 0.78, 1.2),
        "S17": (50.0, 0.0, 1.7), "S18": (2.72, 0.5, 1.6), "S19": (70.0, 0.05, 1.6), "S20": (1.9, 0.9, 3.8),
        "S21": (40.0, 0.2, 2.6), "S22": (2.8, 0.2, 3.8), "S23": (1.85, 0.4, 1.3), "S24": (2.25, 0.45, 1.7),
        "S25": (2.55, 0.4, 1.4), "S26": (2.0, 0.6, 2.6), "S27": (2.8, 0.4, 1.2)}
cameras(SHOTS, CAMS)
finish(SECONDS, OUT_BLEND, [round((t0 + t1) / 2, 2) for _, t0, t1 in SHOTS] + [SCREW_IN, CLICK, DOME_WOBBLE[0] + 0.5, DROP[1], FIT,
                                                                             w1 - 0.1])
