"""
EP001 Cảnh 1 (Hook + Discovery): previz 2D cutout (03_CONTENT/PREVIZ_2D.md, bộ nhân vật pipeline/cutout.py).
Kịch bản: 03_CONTENT/Scripts/EP001_great_rain_experiment.fountain, cảnh #1#. Mốc thời gian và CC: timing.py; mọi
keyframe tính từ các mốc đó (cộng trừ vài phần mười giây cho nhịp lấy đà, giữ tư thế).
    .\\pipeline\\run.ps1 build -Shot 03_CONTENT\\Previz_2D\\EP001_Great_Rain_Experiment\\scene01
    .\\pipeline\\run.ps1 preview -Shot 03_CONTENT\\Previz_2D\\EP001_Great_Rain_Experiment\\scene01
    blender -b --factory-startup -P pipeline\\cc.py -- <cảnh>\\renders\\scene01_preview.mp4 <cảnh>\\timing.py <cảnh>\\renders\\scene01_preview_cc.mp4
Bố cục (X, mét): Tavi 1.05 và Lumo 1.6 co người ủ rũ; vết nứt Lumo vấp ở 2.2–2.36; vườn mầm 2.35–4.7 dưới chân đồi
(đỉnh đồi ở X 4.2, cao 1.95): mầm gầy nhom 2.45, sinh vật nhỏ 2.66, chỗ đặt thìa 2.95, cành lá khô 3.3, Piko 3.42 ngay
dưới đầu lá, bông hoa 4.05. Hai cú cận đạo cụ dựng riêng, phóng to: la bàn (S6) ở X = 20, la bàn kề cái thìa (S10) ở X = 30. Cú cận chiếc lá (S12)
quay ngay trong bối cảnh thật rồi lia lên đỉnh đồi.
"""
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


def steps(t0, t1, step):
    return [t0 + i * step for i in range(int(round((t1 - t0) / step)) + 1)]


def mouth(p, t, k):
    for name, ob in p.mouths.items():
        show(ob, t, name == k)


def bob(ob, t0, t1, x, period=0.8, h=0.02):
    """Nảy nhẹ tại chỗ (Piko không chân)."""
    for i, t in enumerate(steps(t0, t1, period / 2)):
        at(ob, t, x, h if i % 2 else 0.0)
    at(ob, t1, x, 0.0)


def critter(cx, col):
    """Sinh vật nhỏ ủ rũ: thân tròn, mắt nhắm buồn."""
    return [(ell(0.08, 0.065, cx, 0.065), col),
            (arc(0.014, 200, 340, 0.007, cx - 0.02, 0.085), DARK), (arc(0.014, 200, 340, 0.007, cx + 0.03, 0.085), DARK),
            (arc(0.014, 25, 155, 0.006, cx + 0.005, 0.035), DARK)]


def leaf_hat(cx):
    return [(rrect(0.012, 0.16, 0.006, cx + 0.06, 0.08), "#8B6A3E"), (turn(ell(0.12, 0.035, cx + 0.02, 0.17), 10, cx, 0.17), LEAF_DRY)]


# ================================================================ bối cảnh: thung lũng khô, đồi, vườn mầm
SOIL, CRACK, GRASS, LEAF_DRY, GREEN = "#8A6446", "#8A6A45", "#C9A44C", "#A0703C", "#6DA34D"
PURPLE, GOLD = "#7B3FB5", "#E8B33A"                             # màu túi Pocket of Wonders
part("Sky", None, [([(-4, -1.5), (9, -1.5), (9, 6), (-4, 6)], "#CFE7F3")], 3.0)
part("Hill", None, [([(1.9, 0.0), (2.9, 0.75), (3.6, 1.6), (4.2, 1.95), (4.85, 1.72), (5.8, 0.95), (7.2, 0.3),
                      (9.0, 0.05), (9.0, 0.0)], "#DCCBA6")], 2.6)                    # đồi trọc, đỉnh ngay trên vườn mầm
part("Ground", None, [([(-4, -1.5), (9, -1.5), (9, 0.02), (-4, 0.02)], "#E3C893")], 2.0)
cracks = []
for cx, cz, ang in ((-1.3, -0.15, 10), (-0.7, -0.45, -14), (0.2, -0.12, 6), (0.9, -0.6, -8), (1.5, -0.16, 12),
                    (2.0, -0.35, -10), (2.75, -0.14, 8), (3.6, -0.5, -6), (4.4, -0.2, 10), (5.2, -0.4, -12)):
    for k in range(3):                                          # vết nứt gấp khúc
        cracks.append((turn(rrect(0.22, 0.014, 0.006, cx + 0.19 * k, cz), ang if k % 2 else -ang, cx + 0.19 * k, cz), CRACK))
part("Cracks", None, cracks, 1.9)
part("TripCrack", None, [([(2.2, 0.022), (2.36, 0.022), (2.31, -0.16), (2.27, -0.06)], "#5E4630"),   # vết nứt Lumo vấp
                         (turn(rrect(0.18, 0.016, 0.007, 2.2, -0.12), 25, 2.28, -0.08), "#5E4630")], 0.45)
part("Garden", None, [([(2.35, -0.05), (4.7, -0.05), (4.7, 0.03), (2.35, 0.03)], SOIL)], 0.6)
grass = []
for gx in (-1.4, -1.05, -0.6, 0.0, 0.4, 0.75, 1.3, 2.05, 4.85, 5.2, 5.5):  # cỏ úa vàng
    grass += [([(gx - 0.03, 0.02), (gx + 0.03, 0.02), (gx + 0.005, 0.09)], GRASS),
              ([(gx + 0.01, 0.02), (gx + 0.05, 0.02), (gx + 0.06, 0.07)], GRASS)]
part("Grass", None, grass, 0.5)
sprouts = []
for j, sx in enumerate((3.2, 3.65, 4.3, 4.55)):                 # mầm cây nghiêng ngả, lá rũ xuống
    shapes = [(rrect(0.012, 0.1, 0.005, sx, 0.05), "#8DAA55"),
              (turn(ell(0.032, 0.01, sx + 0.03, 0.09), -55, sx, 0.1), "#A9A84E"),
              (turn(ell(0.026, 0.009, sx - 0.024, 0.065), 60, sx, 0.07), "#A9A84E")]
    sprouts += [(turn(pts, 14 if j % 2 else -10, sx, 0.0), col) for pts, col in shapes]
sprouts += [(turn(rrect(0.01, 0.15, 0.005, 2.45, 0.075), -8, 2.45, 0.0), "#8DAA55"),   # mầm gầy nhom Nori rọi sáng
            (turn(ell(0.03, 0.009, 2.485, 0.13), -60, 2.46, 0.14), "#A9A84E")]
part("Sprouts", None, sprouts, 0.55)
sprout_glow = part("SproutGlow", None, [(ell(0.08, 0.09, 2.45, 0.1), "#FFF1A8")], 0.57)
light = part("NoriLight", None, [([(2.65, 0.5), (2.71, 0.51), (2.53, 0.05), (2.37, 0.05)], "#FFF2B8")], 0.58)
part("Critters", None, leaf_hat(-1.2) + critter(-1.2, "#F7C8A0") + leaf_hat(-0.65) + critter(-0.65, "#BFD9F2")
     + leaf_hat(5.1) + critter(5.1, "#F2B8D0"), 0.4)                         # sinh vật nhỏ ủ rũ dưới lá khô
sigh_body = part("Critter_Sigh", None, critter(0.0, "#C6E2A0"), 0.41, (2.66, 0.0))   # bạn trong vườn, thở dài ở S4
sigh_leaf = node("Critter_SighLeaf", None, (2.66, 0.0), 0.405)
part("Critter_SighLeafShape", sigh_leaf, leaf_hat(0.0))

# cành khô, chiếc lá cong queo, giọt sương cuối cùng
part("Twig", None, [([(3.27, 0.0), (3.3, 0.0), (3.35, 0.5), (3.38, 0.88), (3.355, 0.89), (3.325, 0.5)], "#8B6A3E")], 0.35)
part("DryLeaf", None, [(turn(ell(0.12, 0.04, 3.47, 0.875), -15, 3.47, 0.875), LEAF_DRY),
                       (turn(rrect(0.2, 0.006, 0.003, 3.47, 0.875), -15, 3.47, 0.875), "#7A5530"),
                       (arc(0.026, -50, 210, 0.014, 3.605, 0.858), LEAF_DRY),          # đầu lá xoăn
                       (arc(0.02, 110, 290, 0.01, 3.4, 0.925), "#8E6A3A")], 0.34)       # mép lá quăn
dew = node("Dew", None, (3.40, 0.959), 0.3)
part("Dew_Body", dew, [(ell(0.045, 0.057), "#E2F7FF"), (ell(0.015, 0.018, -0.013, 0.02), WHITE)])
dew_glint = part("Dew_Glint", dew, [(star(0.07, 0, 0, 4, 0.3), WHITE)], -0.005, (0.035, 0.045))
leaf_glint = part("Leaf_Glint", None, [(star(0.04, 0, 0, 4, 0.3), WHITE)], 0.32, (3.585, 0.88))   # chỗ lá còn ướt sương
wet = [part(f"Leaf_Wet{i}", None, [(band([p0, p1], 0.007), "#E6CFA8")], 0.33)   # vệt ẩm giọt sương để lại khi lăn qua
       for i, (p0, p1) in enumerate((((3.40, 0.92), (3.45, 0.906)), ((3.45, 0.906), (3.51, 0.89)), ((3.51, 0.89), (3.575, 0.875))))]
mist = node("HillMist", None, (4.18, 1.93), 2.55)               # dải mây mỏng vắt ngang đỉnh đồi: trên cao lạnh hơn
part("HillMistShape", mist, [(ell(0.34, 0.05), "#F4F8FB"), (ell(0.2, 0.045, -0.22, 0.04), "#F4F8FB"),
                             (ell(0.22, 0.04, 0.24, 0.035), "#F4F8FB")])

# bông hoa nhỏ nhìn nghiêng: ngửa lên chờ giọt sương, rồi gục xuống
flower = node("Flower", None, (4.05, 0.0), 0.2)
part("Flower_StemLow", flower, [(rrect(0.014, 0.26, 0.007, 0, 0.13), GREEN), (turn(ell(0.045, 0.014, 0.035, 0.1), 25, 0, 0.1), GREEN)])
flower_top = node("Flower_Top", flower, (0.0, 0.26), -0.003)
part("Flower_StemHigh", flower_top, [(rrect(0.013, 0.1, 0.006, 0, 0.05), GREEN)])
flower_head = node("Flower_Head", flower_top, (0.0, 0.1), -0.003)
part("Flower_Bloom", flower_head, [([(-0.022, 0.0), (0.022, 0.0), (0.0, -0.03)], "#5E9A40")]
     + [(turn(ell(0.014, 0.045, 0, 0.045), a), "#F7A1C4") for a in (-55, -28, 0, 28, 55)]
     + [(ell(0.04, 0.014, 0, 0.012), "#FFD54F")])

title = [text("Title1", "CLOUD EXPLORERS", 0.42, (2.0, 2.5), "#FC6640"),
         text("Title2", "CƠN MƯA ĐẦU TIÊN", 0.26, (2.0, 2.05), "#7B3FB5")]

# --- S6: cận la bàn trong hai tay Lumo (X = 20); túi tím ở mép phải, đúng hướng mũi sao
NEEDLE_TO_BAG = 112                                             # hướng từ la bàn trong tay Lumo tới túi Piko (độ, 0 = lên)
part("Compass_BG", None, [([(18.9, -0.6), (21.1, -0.6), (21.1, 0.6), (18.9, 0.6)], "#E9D3A6")], 1.0)
part("Compass_PikoBody", None, [(ell(0.42, 0.75, 21.02, 0.05), "#44DAFC"), (ell(0.08, 0.06, 20.82, 0.45), "#E8FBFF")], 0.95)
part("Compass_BagHint", None, [(turn(rrect(0.014, 0.5, 0.007, 20.5, 0.13), -30, 20.5, -0.12), GOLD),   # túi đeo chéo
                               (ell(0.085, 0.085, 20.5, -0.2), PURPLE), (rrect(0.075, 0.024, 0.01, 20.5, -0.12), GOLD),
                               (ell(0.033, 0.02, 20.5, -0.21), "#F6EBD9")], 0.9)
hint_glint = part("Compass_BagGlint", None, [(star(0.05, 0, 0, 4, 0.3), "#FFE14D")], 0.85, (20.5, -0.1))   # ánh vàng ở miệng túi
part("Compass_Case", None, [(ell(0.06, 0.06, 20, 0.4), "#C99A2E"), (ell(0.035, 0.035, 20, 0.4), "#E9D3A6"),
                            (ell(0.37, 0.37, 20, 0), "#C99A2E"), (ell(0.34, 0.34, 20, 0), "#E5B53A"),
                            (ell(0.28, 0.28, 20, 0), "#5BC3E8"), (ell(0.09, 0.05, 19.86, -0.2), WHITE),
                            (ell(0.07, 0.045, 19.97, -0.21), WHITE)], 0.0)
compass_star = node("Compass_Star", None, (20.0, 0.0), -0.01)
part("Compass_StarShape", compass_star, [(star(0.22, 0, 0, 8, 0.4), "#FFF6C8"),
                                         ([(0, 0.26), (0.035, 0.0), (0, -0.04), (-0.035, 0.0)], "#FF6B4A"),   # mũi sao
                                         (ell(0.04, 0.04), WHITE)])
part("Compass_Paws", None, [(rrect(0.28, 0.34, 0.12, 19.6, -0.5), "#FD8A2B"), (rrect(0.26, 0.34, 0.11, 20.28, -0.53), "#FD8A2B"),
                            (ell(0.17, 0.12, 19.68, -0.3), "#FEECCF"), (ell(0.15, 0.11, 20.22, -0.33), "#FEECCF")], -0.05)   # tay ngắn, mập

# --- S10: cận la bàn kề cái thìa cong (X = 30, phóng to): thìa nằm trên đất ngay dưới la bàn, túi ở bên phải trên thân Piko
BENT = [(rrect(0.018, 0.08, 0.009, 0.02, -0.12), "#C9D1DA"),                                         # thìa cán gập chữ U
        (turn(rrect(0.018, 0.07, 0.009, 0.02, -0.195), 130, 0.02, -0.16), "#C9D1DA"),
        (turn(ell(0.032, 0.042, 0.02, -0.25), 130, 0.02, -0.16), "#C9D1DA")]
ZOOM = 2.4
part("Test_BG", None, [([(29.0, -0.6), (31.0, -0.6), (31.0, 0.6), (29.0, 0.6)], "#E9D3A6")], 1.0)
part("Test_Ground", None, [([(29.0, -0.6), (31.0, -0.6), (31.0, -0.19), (29.0, -0.19)], SOIL)], 0.95)
part("Test_PikoBody", None, [(ell(0.6, 0.85, 31.15, 0.2), "#44DAFC")], 0.9)                   # thân thạch Piko ở mép phải
test_spoon = part("Test_Spoon", None, [(turn(pts, 90, 0.02, -0.16), col) for pts, col in BENT], 0.45,
                  (29.98 - ZOOM * 0.02, -0.17 + ZOOM * 0.16))                                   # cán nằm trên đất, lòng thìa vểnh lên
scl(test_spoon, 0.0, ZOOM, ZOOM)
test_bag = node("Test_Bag", None, (30.5, 0.12), 0.5)
part("Test_BagShape", test_bag, [(turn(rrect(0.02, 0.5, 0.01, 0, 0.25), -30), GOLD), (ell(0.08, 0.035, 0, 0.0), PURPLE),
                                 (ell(0.12, 0.12, 0, -0.14), PURPLE), (rrect(0.11, 0.035, 0.015, 0, -0.025), GOLD),
                                 (ell(0.055, 0.032, 0, -0.15), "#F6EBD9")])
test_glint = part("Test_BagGlint", test_bag, [(star(0.07, 0, 0, 4, 0.3), "#FFE14D")], -0.02, (0.0, 0.02))
test_c = node("Test_Compass", None, (29.6, 0.34), 0.2)
part("Test_CompassCase", test_c, [(ell(0.22, 0.22), "#C99A2E"), (ell(0.2, 0.2), "#E5B53A"), (ell(0.165, 0.165), "#5BC3E8"),
                                  (ell(0.05, 0.03, -0.06, -0.11), WHITE), (ell(0.04, 0.026, 0.0, -0.12), WHITE)])
test_star = node("Test_CompassStar", test_c, (0.0, 0.0), -0.01)
part("Test_CompassStarShape", test_star, [(star(0.13, 0, 0, 8, 0.4), "#FFF6C8"),
                                          ([(0, 0.155), (0.022, 0.0), (0, -0.025), (-0.022, 0.0)], "#FF6B4A"), (ell(0.025, 0.025), WHITE)])
part("Test_Paws", test_c, [(turn(rrect(0.17, 0.5, 0.085, -0.387, 0.197), 45, -0.387, 0.197), "#FD8A2B"),   # tay vào từ phía
                           (turn(rrect(0.16, 0.5, 0.08, -0.205, 0.417), 30, -0.205, 0.417), "#E07722"),    # trên bên trái,
                           (ell(0.1, 0.085, -0.21, 0.02), "#FEECCF"), (ell(0.095, 0.08, -0.08, 0.2), "#FEECCF")], -0.03)   # không che thìa

# ================================================================ nhân vật
tavi = build_tavi(1.05, -0.40)                                 # trước Lumo: tay chụp quai túi nổi trên lưng Lumo
lumo = build_lumo(1.6, -0.32)
piko = build_piko(3.42, -0.28)
nori = build_nori(0.0, 0.0, -0.2)
nori_path = node("Nori_Path", None, (6.6, 1.5), -0.2)          # đường bay; root nảy nhẹ quanh nó
nori.root.parent, nori.root.location = nori_path, (0.0, 0.0, 0.0)

compass = part("Lumo_Compass", lumo.arm, [(ell(0.062, 0.062, 0, -0.23), "#E5B53A"), (ell(0.048, 0.048, 0, -0.23), "#5BC3E8")], -0.005)
needle = node("Lumo_CompassNeedle", compass, (0.0, -0.23), -0.002)
part("Lumo_CompassStar", needle, [(star(0.034, 0, 0, 8, 0.4), "#FFF6C8"), ([(0, 0.054), (0.011, 0.0), (0, -0.01), (-0.011, 0.0)], "#FF6B4A")])
buzz = part("Lumo_Buzz", lumo.root, [(turn(rrect(0.016, 0.07, 0.007, 0.0, 0.13), a), "#FF9F1C") for a in (-60, -20, 20, 60)],
            -0.03, (0.1, 0.2))
spoon = part("Piko_Spoon", piko.arm, [(rrect(0.018, 0.13, 0.009, 0.02, -0.145), "#C9D1DA"), (ell(0.032, 0.042, 0.02, -0.25), "#C9D1DA"),
                                      (ell(0.018, 0.026, 0.024, -0.245), "#E6ECF2")], -0.004)
spoon_bent = part("Piko_SpoonBent", piko.arm, BENT, -0.004)
spoon_ground = part("SpoonOnGround", None, [(turn(pts, 90, 0.02, -0.16), col) for pts, col in BENT], -0.3, (2.93, 0.2))  # nằm trên đất
dust = part("Dust", None, [(ell(0.05, 0.03), "#D9C08F"), (ell(0.035, 0.025, 0.08, 0.02), "#D9C08F"),
                           (ell(0.03, 0.02, -0.07, 0.02), "#D9C08F")], -0.45, (3.0, 0.04))
bag_glint = part("Piko_BagGlint", piko.bag, [(star(0.035, 0, 0, 4, 0.3), "#FFE14D")], -0.01, (0.0, 0.015))   # ánh vàng ở miệng túi
idea = part("Tavi_Idea", tavi.head, [(star(0.05), "#FFE14D")], -0.03, (0.12, 0.52))
sweat = part("Piko_Sweat", piko.root, [([(0.0, 0.05), (-0.021, 0.0), (0.021, 0.0)], "#E4F8FF"),
                                       (ell(0.023, 0.025, 0.0, -0.004), "#E4F8FF")], -0.03, (0.22, 0.58))   # giọt mồ hôi
knock_dust = part("KnockDust", None, [(ell(0.04, 0.025), "#D9C08F"), (ell(0.03, 0.02, 0.06, 0.015), "#D9C08F"),
                                      (ell(0.025, 0.018, -0.05, 0.015), "#D9C08F")], -0.45, (1.62, 0.03))


def ears(t, near, far=None):
    ry(lumo.ear_near, t, near)
    ry(lumo.ear_far, t, near - 4 if far is None else far)


def flash(ob, t):
    """Lóe sáng một cái: hiện, bung to, thu lại, tắt."""
    show(ob, t, True)
    for dt, s in ((0.0, 0.2), (0.12, 1.4), (0.3, 0.7), (0.45, 1.1), (0.6, 0.0)):
        scl(ob, t + dt, s, s)
    show(ob, t + 0.6, False)


def twinkle(ob, t0, t1):
    """Lấp lánh liên tục trong một quãng: hiện, nhấp nháy to nhỏ, tắt."""
    show(ob, t0, True)
    for i, t in enumerate(steps(t0, t1, 0.15)):
        s = 0.3 if i == 0 else 1.4 if i % 2 else 0.8
        scl(ob, t, s, s)
    scl(ob, t1 + 0.1, 0.0, 0.0)
    show(ob, t1 + 0.1, False)


def aim(t, arm_deg, extra=0, target=NEEDLE_TO_BAG):
    """Mũi sao la bàn trong tay Lumo chỉ về túi Piko, bù góc tay đang cầm."""
    ry(needle, t, target - arm_deg + extra)


for ob in (compass, buzz, spoon, spoon_bent, spoon_ground, dust, knock_dust, idea, light, sprout_glow, *title,
           hint_glint, test_glint, bag_glint, leaf_glint, sweat):
    show(ob, 0.0, False)

# ================================================================ Hook: giọt sương cuối cùng
glint_keys = [(0.0, 0.0)] + [(t, 1.0 if i % 2 == 0 else 0.55) for i, t in enumerate(steps(DEW_GLINT[0], DEW_GLINT[1], 0.6))]
for t, s in glint_keys + [(DEW_GLINT[1] + 0.1, 0.0)]:
    scl(dew_glint, t, s, s)
r0, r1 = DEW_ROLL
ROLL = ((0.0, 3.40, 0.959), (0.6, 3.45, 0.945), (1.2, 3.45, 0.945), (1.7, 3.51, 0.929), (2.2, 3.51, 0.929), (2.7, 3.575, 0.914))
for dt, x, z in ROLL:                                           # lăn… dừng… lăn… dừng… lăn tới đầu lá
    at(dew, r0 + dt, x, z)
for ob, dt in zip(wet, (0.3, 1.45, 2.45)):                       # để lại vệt ẩm phía sau
    show(ob, 0.0, False)
    show(ob, r0 + dt, True)
scl(dew, r0 + 2.7, 1, 1)
scl(dew, PIKO_JUMP[0], 0.9, 1.25)                               # trĩu xuống ở đầu lá
at(dew, r1 - 0.02, 3.575, 0.914)
key(dew, "location", r1, (3.575, -0.35, 0.914))                 # lúc rơi lên lớp trước Piko: thấy rơi vào miệng
at(dew, SLURP, 3.58, 0.71)
show(dew, 0.0, True)
show(dew, SLURP + 0.02, False)                                  # ẩn cả giọt và ánh lấp lánh

ry(flower, 0.0, -4)
ry(flower_top, 0.0, -12)
ry(flower_head, 0.0, -30)                                       # ngửa về phía giọt sương
d0, d1 = FLOWER_DROOP
ry(flower, d0, -4)
ry(flower_top, d0, -12)
ry(flower_head, d0, -30)
scl(flower_head, d0, 1, 1)
ry(flower_top, d0 + 0.4, 105)                                   # gập ngang thân, đầu hoa rủ xuống
ry(flower_head, d0 + 0.4, 45)
ry(flower_top, d1, 95)
ry(flower_head, d1, 40)
ry(flower, d1, 8)
scl(flower_head, d1, 0.65, 1)                                   # cánh hoa cụp lại

# --- Piko: chờ, nhìn theo giọt sương, nảy lên đớp, liếm môi, nhìn bông hoa, cười trừ
show(piko.drops, 0.0, False)                                    # giọt nước quanh người hiện sau cú húp
show(piko.drops, SLURP + 0.1, True)
at(piko.root, 0.0, 3.42, 0)
face(piko, 0.0, "eager")
lean(piko, 0.0, -12)                                            # ngửa lên nhìn chằm chằm
look(piko, 0.0, -0.3, 1.0)
for dt, dx in ((0.0, -0.3), (0.6, -0.05), (1.2, -0.05), (1.7, 0.25), (2.2, 0.25), (2.7, 0.6)):   # mắt bám theo giọt sương
    look(piko, r0 + dt, dx, 1.0)
for dt in (0.6, 1.7):                                           # mỗi lần giọt dừng: ngửa thêm, há miệng sẵn; lăn tiếp thì ngậm
    lean(piko, r0 + dt, -12)
    lean(piko, r0 + dt + 0.25, -17)
    mouth(piko, r0 + dt + 0.2, "open")
    mouth(piko, r0 + dt + 0.6, "smile")
    lean(piko, r0 + dt + 0.6, -12)
    ry(flower_head, r0 + dt, -30)                               # bông hoa vươn lên chờ
    ry(flower_head, r0 + dt + 0.3, -42)
    ry(flower_head, r0 + dt + 0.7, -30)
for i, t in enumerate(steps(0.0, PIKO_JUMP[0] - 0.1, 0.7)):     # thở khi chờ
    scl(piko.root, t, 1.03 if i % 2 else 1.0, 0.97 if i % 2 else 1.0)
ry(piko.arm, 0.0, 6)
lean(piko, PIKO_JUMP[0], -12)
scl(piko.root, PIKO_JUMP[0] - 0.1, 1, 1)
scl(piko.root, PIKO_JUMP[0] + 0.08, 1.18, 0.8)                 # nén người
at(piko.root, PIKO_JUMP[0] + 0.12, 3.42, 0)
mouth(piko, PIKO_JUMP[0] + 0.12, "open")
scl(piko.root, PIKO_JUMP[0] + 0.18, 0.88, 1.15)                # giãn khi bật
lean(piko, PIKO_JUMP[0] + 0.12, -4)
at(piko.root, SLURP, 3.42, 0.40)
mouth(piko, SLURP + 0.02, "closed")                             # đớp gọn
face(piko, SLURP + 0.1, "happy")
scl(piko.root, SLURP + 0.15, 1, 1)
at(piko.root, PIKO_JUMP[1] - 0.05, 3.42, 0)
scl(piko.root, PIKO_JUMP[1] - 0.03, 1.15, 0.85)                # bẹp khi đáp
scl(piko.root, PIKO_JUMP[1] + 0.15, 1, 1)
lean(piko, PIKO_JUMP[1], 0)
l0, l1 = PIKO_LICK
for t, k in ((l0, "open"), (l0 + 0.15, "smile"), (l0 + 0.28, "open"), (l1, "smile")):   # liếm môi
    mouth(piko, t, k)
face(piko, PIKO_LOOK_FLOWER[0], "neutral")                      # mở mắt nhìn xuống bông hoa
look(piko, PIKO_LOOK_FLOWER[0], 0.9, -0.9)
lean(piko, PIKO_LOOK_FLOWER[0], 0)
lean(piko, PIKO_LOOK_FLOWER[0] + 0.25, 10)
gr0, gr1 = PIKO_GRIN                                            # co người cười trừ, gãi má, liếc bông hoa
face(piko, gr0, "grin")
scl(piko.root, gr0, 1, 1)
scl(piko.root, gr0 + 0.2, 1.1, 0.85)
show(sweat, gr0 + 0.15, True)
at(sweat, gr0 + 0.15, 0.22, 0.6)
at(sweat, gr1, 0.235, 0.52)                                      # giọt mồ hôi trượt xuống
show(sweat, gr1 + 0.25, False)
ry(piko.arm, gr0, 6)
ry(piko.arm, gr0 + 0.2, -150)
loop(piko.arm, gr0 + 0.3, gr1 - 0.1, 0.2, -140, -156)
face(piko, PIKO_GRIN_GLANCE[0], "neutral")
look(piko, PIKO_GRIN_GLANCE[0], 0.9, -0.9)
face(piko, PIKO_GRIN_GLANCE[1], "grin")
scl(piko.root, gr1, 1.1, 0.85)
scl(piko.root, gr1 + 0.3, 1, 1)
ry(piko.arm, gr1 + 0.3, 6)
lean(piko, gr1, 10)
lean(piko, gr1 + 0.4, 0)
look(piko, gr1, 0.0, 0.0)
face(piko, SHOT["S3"][0] + 0.2, "neutral")
bob(piko.root, SHOT["S3"][0], PIKO_TURN - 0.4, 3.42, 0.9, 0.035)
for t in (TITLE[1] + 0.6, NORI_LINE[0] + 0.6, TAVI_LINE[0], COMPASS_BUZZ[0] + 1.5):
    blink(piko, t)
loop(piko.bag, 0.0, PIKO_JUMP[0], 1.4, -4, 4)
loop(piko.bag, PIKO_JUMP[0], FLOWER_DROOP[0] - 0.1, 0.3, -14, 10)   # lắc theo cú nảy, dừng trước khi hoa gục
loop(piko.bag, FLOWER_DROOP[0], PIKO_RUMMAGE[0] - 0.1, 1.4, -4, 4)

# --- sinh vật nhỏ trong vườn thở dài, chiếc lá trên đầu trễ xuống che mắt (không rơi ra ngoài)
c0, c1 = CRITTER_SIGH
scl(sigh_body, c0, 1, 1)
scl(sigh_body, c0 + 0.3, 1.12, 0.8)
scl(sigh_body, c0 + 0.8, 1.05, 0.9)
ry(sigh_leaf, c0 + 0.3, 0)
at(sigh_leaf, c0 + 0.3, 2.66, 0.0)
ry(sigh_leaf, c1, 8)
at(sigh_leaf, c1, 2.66, -0.07)

# ================================================================ Discovery
# --- Tavi: ủ rũ, đi theo Lumo, lao tới chụp quai túi, nhắc vết nứt, nghĩ ra cách làm mưa
loop(tavi.tail, 0.0, SECONDS, 2.0, -4, 4)
at(tavi.root, 0.0, 1.05, 0)
face(tavi, 0.0, "sad")
lean(tavi, 0.0, 6)
ry(tavi.head, 0.0, 14)
ry(tavi.arm, 0.0, 6)
ry(tavi.arm_far, 0.0, -6)
for t in (TITLE[0] + 2.5, NORI_LINE[0] + 1.0):
    blink(tavi, t)
dash0 = LUMO_DASH[0]
ry(tavi.head, dash0, 14)
ry(tavi.head, dash0 + 0.15, 0)
face(tavi, dash0 + 0.1, "worried")
at(tavi.root, dash0, 1.05, 0)
at(tavi.root, dash0 + 0.35, 1.25, 0.04)                         # bước theo Lumo
at(tavi.root, LUMO_TRIP, 1.4, 0)
lean(tavi, dash0, 6)
lean(tavi, dash0 + 0.3, 8)
g0, g1 = TAVI_LUNGE                                             # Lumo vấp rồi Tavi mới lao tới
face(tavi, g0 + 0.02, "shock", 18)
at(tavi.root, g0, 1.4, 0)
at(tavi.root, g0 + 0.2, 1.7, 0.05)
at(tavi.root, g1, 1.92, 0)                                      # đứng sau Lumo, không che thân Lumo
lean(tavi, g0, 8)
lean(tavi, g0 + 0.15, 20)
lean(tavi, g1, 25)
ry(tavi.arm, g0, 6)
ry(tavi.arm, g1 - 0.05, -110)                                   # tay chạm quai túi sau vai Lumo
at(tavi.root, LUMO_DANGLE[1], 1.97, 0)                          # giữ chặt quai túi, bị kéo theo một chút
lean(tavi, LUMO_DANGLE[1], 25)
ry(tavi.arm, LUMO_DANGLE[1], -110)
p0, p1 = LUMO_PULLED
lean(tavi, p0 + 0.2, -12)                                        # kéo lại
at(tavi.root, p0 + 0.25, 1.72, 0)
ry(tavi.arm, p0 + 0.25, -75)
lean(tavi, p1, 0)
ry(tavi.arm, p1, 6)
face(tavi, TAVI_LINE[0] - 0.05, "worried")
ry(tavi.head, TAVI_LINE[0] + 0.1, 10)
ry(tavi.arm, TAVI_LINE[0], 6)
ry(tavi.arm, TAVI_LINE[0] + 0.2, -40)                          # chỉ xuống vết nứt
talk(tavi, TAVI_LINE[0], TAVI_LINE[1])
ry(tavi.arm, TAVI_LINE[1], -40)
ry(tavi.arm, TAVI_LINE[1] + 0.2, 6)
s0, s1 = TAVI_STEP_BACK                                         # lùi ra khỏi khung hai người Lumo và Piko
at(tavi.root, s0, 1.72, 0)
at(tavi.root, s0 + 0.3, 1.5, 0.03)
at(tavi.root, s1, 1.3, 0)
face(tavi, s0, "neutral")
ry(tavi.head, s0, 0)
face(tavi, DIG[2] + 0.02, "shock")
face(tavi, PIKO_BLINK[0] + 0.1, "neutral")
# bước lại xem cái thìa cong, dậm thử mặt đất nứt (đất cứng, đào không ra nước), rồi ngẩng dần lên tới đỉnh đồi
n0, n1 = TAVI_STEP_IN
at(tavi.root, n0, 1.3, 0)
at(tavi.root, n0 + 0.3, 1.43, 0.03)
at(tavi.root, n1, 1.55, 0)
look(tavi, n1, 0.8, -0.8)                                       # nhìn cái thìa cong
k0, k1 = TAVI_KNOCK
face(tavi, k0, "puzzled", 14)
ry(tavi.head, k0, 0)
ry(tavi.head, k0 + 0.15, 18)                                    # nhìn xuống mặt đất nứt
look(tavi, k0 + 0.15, 0.6, -1.0)
for t in TAVI_STAMPS:                                           # CỘC. CỘC.
    at(tavi.root, t - 0.3, 1.55, 0)
    scl(tavi.root, t - 0.3, 1, 1)
    at(tavi.root, t - 0.15, 1.55, 0.13)
    at(tavi.root, t, 1.55, 0)
    scl(tavi.root, t, 1.1, 0.88)                                 # bẹp người khi chạm đất
    scl(tavi.root, t + 0.15, 1, 1)
    show(knock_dust, t, True)
    show(knock_dust, t + 0.25, False)
    scl(knock_dust, t, 1.0, 1.0)
    scl(knock_dust, t + 0.25, 2.4, 2.4)
v0, v1 = TAVI_LOOK_LEAF                                         # nhìn chiếc lá còn ướt sương: hơi nước gặp lạnh thành giọt
ry(tavi.head, v0, 18)
ry(tavi.head, v0 + 0.3, -10)                                    # ngước lên chiếc lá rồi mới cắt sang cú cận chiếc lá
look(tavi, v0, 0.6, -1.0)
look(tavi, v0 + 0.3, 1.0, 0.7)
u0, u1 = TAVI_LOOK_UP                                           # ngẩng dần lên đỉnh đồi (máy lia thay mắt Tavi)
ry(tavi.head, u0, -10)
ry(tavi.head, u1, -24)
look(tavi, u0, 1.0, 0.7)
look(tavi, u1, 0.6, 1.0)
lean(tavi, u0, 0)
lean(tavi, u1, -5)
i0, i1 = TAVI_IDEA                                              # "à!": mắt sáng lên, quay phắt sang Lumo, nhún bật, giơ ngón tay
ry(tavi.head, TAVI_SNAP[0], -24)
face(tavi, i0 + 0.15, "eager")
show(idea, i0 + 0.15, True)
scl(idea, i0 + 0.15, 0.3, 0.3)
scl(idea, i0 + 0.3, 1.5, 1.5)                                    # ngôi sao bung to rồi thu lại
scl(idea, TAVI_SNAP[1], 1.0, 1.0)
show(idea, TAVI_GATHER[0] + 0.2, False)
ry(tavi.head, TAVI_SNAP[1], 0)                                  # quay sang nhìn Lumo
look(tavi, TAVI_SNAP[1], 1.0, 0.0)
at(tavi.root, i0 + 0.3, 1.55, 0)
at(tavi.root, TAVI_SNAP[1], 1.55, 0.06)
at(tavi.root, i0 + 0.6, 1.55, 0)
scl(tavi.root, i0 + 0.3, 1.05, 0.93)                            # nhún lấy đà rồi bật
scl(tavi.root, TAVI_SNAP[1], 0.96, 1.06)
scl(tavi.root, i0 + 0.6, 1, 1)
ry(tavi.arm, i0 + 0.3, 6)
ry(tavi.arm, TAVI_SNAP[1], -108)                                # giơ một ngón tay ra trước (dưới mõm): "à!"
ry(tavi.arm, i1, -108)
lean(tavi, TAVI_SNAP[1], 0)
lean(tavi, i1, 6)                                               # chồm về phía Lumo
key(tavi.arm_far, "location", i1 - 0.1, (-0.01, 0.02, 0.36))
key(tavi.arm_far, "location", i1, (0.0, -0.035, 0.36))         # tay xa lên lớp trước: thấy đủ hai tay khi minh hoạ
# "Gom hơi nước,": lấy đà vung hai tay ra sau, rồi vun mạnh về trước bụng, giữ hai tay khum lại
a0, a1 = TAVI_GATHER
ry(tavi.arm_far, a0, -6)
ry(tavi.arm, a0 + 0.25, 30)
ry(tavi.arm_far, a0 + 0.25, 40)
lean(tavi, a0, 6)
lean(tavi, a0 + 0.25, -4)
ry(tavi.arm, a0 + 0.6, -85)
ry(tavi.arm_far, a0 + 0.6, -75)
lean(tavi, a0 + 0.6, 8)
ry(tavi.arm, a1 - 0.1, -70)
ry(tavi.arm_far, a1 - 0.1, -65)
face(tavi, a0 - 0.02, "eager")
talk(tavi, a0, a1 - 0.05, "smile")
# "làm lạnh,": hai bàn tay áp lên ngực (cẳng tay gập lại), rụt cổ, nhắm tịt mắt, rung bần bật
b0, b1 = TAVI_SHIVER
ry(tavi.arm, b0 + 0.15, -70)
ry(tavi.arm_far, b0 + 0.15, -65)
scl(tavi.arm, b0, 1, 1)
scl(tavi.arm_far, b0, 1, 1)
scl(tavi.arm, b0 + 0.15, 1, 0.55)
scl(tavi.arm_far, b0 + 0.15, 1, 0.55)
scl(tavi.arm, b1, 1, 0.55)
scl(tavi.arm_far, b1, 1, 0.55)
scl(tavi.arm, b1 + 0.15, 1, 1)
scl(tavi.arm_far, b1 + 0.15, 1, 1)
ry(tavi.head, b0, 0)
ry(tavi.head, b0 + 0.15, 12)
ry(tavi.head, b1 - 0.05, 12)
ry(tavi.head, b1 + 0.1, 0)
lean(tavi, b0, 0)
scl(tavi.root, b0, 1, 1)
scl(tavi.root, b0 + 0.15, 1.04, 0.95)
loop(tavi.root, b0 + 0.15, b1 - 0.1, 0.07, -6, 6)
scl(tavi.root, b1 - 0.05, 1, 1)
lean(tavi, b1, 0)
face(tavi, b0 + 0.02, "squint")
talk(tavi, b0, b1 - 0.05, "frown")
# "sẽ có mưa!": giơ hai tay chếch ra trước (dưới mõm) rồi rung các ngón tay hạ dần xuống đất
c0, c1 = TAVI_RAIN
ry(tavi.arm, c0 + 0.15, -105)
ry(tavi.arm_far, c0 + 0.15, -110)
for i, t in enumerate(steps(c0 + 0.25, c1 - 0.1, 0.1)):
    a = -105 + 5 * i                                            # hạ tới khoảng -60, tay không lọt xuống dải CC
    ry(tavi.arm, t, a + (10 if i % 2 else -10))
    ry(tavi.arm_far, t, a + (-10 if i % 2 else 10))
face(tavi, c0 + 0.02, "eager")
look(tavi, c0 + 0.2, 1.0, 0.3)
look(tavi, c1 - 0.2, 0.7, -0.9)                                 # mắt nhìn theo tay hạ xuống
scl(tavi.root, c1 - 0.3, 1, 1)
scl(tavi.root, c1 - 0.1, 1.04, 0.95)                            # người nhún theo
scl(tavi.root, c1 + 0.05, 1, 1)
talk(tavi, c0, c1 - 0.05, "smile")
# "Lên đỉnh đồi, trên đó lạnh hơn!": bước lên trước Lumo cho khoảng trời trống, rồi chỉ lên đỉnh đồi
t0, t1 = TAVI_POINT
key(tavi.arm_far, "location", t0, (0.0, -0.035, 0.36))
key(tavi.arm_far, "location", t0 + 0.1, (-0.01, 0.02, 0.36))
at(tavi.root, t0, 1.55, 0)
at(tavi.root, t0 + 0.25, 2.15, 0.04)
at(tavi.root, TAVI_STRIDE[1], 2.82, 0)                          # dừng phía trước Lumo, không chồng lên Lumo
ry(tavi.arm, TAVI_STRIDE[1], 6)
ry(tavi.arm, t0 + 0.7, -130)                                    # chỉ dốc lên đúng hướng đỉnh đồi, vươn dài tay,
scl(tavi.arm, TAVI_STRIDE[1], 1, 1)                             # ngửa đầu theo: bàn tay tách khỏi mõm
scl(tavi.arm, t0 + 0.7, 1, 1.3)
ry(tavi.arm_far, t0 + 0.15, 6)
ry(tavi.head, TAVI_STRIDE[1], 0)
ry(tavi.head, t0 + 0.7, -35)
look(tavi, t0 + 0.7, 0.7, 1.0)
lean(tavi, TAVI_STRIDE[1], 0)
lean(tavi, t0 + 0.7, -8)
face(tavi, t0 + 0.05, "shout")
talk(tavi, t0, t1, "smile")
ry(tavi.arm, SECONDS, -130)

# --- Nori: bay ngang khi tên phim còn hiện, rọi sáng mầm cây gầy nhom, nói một câu, rồi bay lên cao xem
nori.dir = -1
scl(nori.root, 0.0, -1, 1)
for i in range(int(SECONDS) + 1):
    at(nori.root, i, 0.0, 0.03 if i % 2 else -0.03)
for w, phase in zip(nori.wings, (0.06, 0.0)):                   # hai cặp cánh lệch pha
    loop(w, phase, SECONDS, 0.24, -14, 14)
for a in nori.antennae:
    loop(a, 0.0, SECONDS, 1.4, -6, 6)
f0, f1 = NORI_FLY_IN
at(nori_path, 0.0, 6.6, 1.5)
at(nori_path, f0, 6.6, 1.5)
at(nori_path, f0 + (f1 - f0) * 0.4, 4.8, 1.7)                  # lượn ngang khung toàn dưới tên phim
at(nori_path, f0 + (f1 - f0) * 0.75, 3.6, 1.45)                # bay qua cao hơn sừng Piko
at(nori_path, f1, 2.78, 0.66)
at(nori_path, NORI_LIGHT[1], 2.78, 0.66)
at(nori_path, NORI_LIGHT[1] + 0.8, 3.1, 1.0)                   # lên bên phải, trong khung S5, không che Lumo lúc vấp
at(nori_path, SPOON_OUT, 3.1, 1.0)
at(nori_path, SPOON_OUT + 0.5, 3.15, 1.34)                     # lên cao hơn nữa khi máy quay cận Piko
at(nori_path, STAR_STILL[1], 3.15, 1.34)
at(nori_path, STAR_STILL[1] + 0.4, 3.15, 1.12)
at(nori_path, TAVI_KNOCK[0], 3.15, 1.12)
at(nori_path, TAVI_KNOCK[0] + 0.6, 2.5, 1.15)                    # lại gần xem Tavi dậm đất, ra khỏi đường lia máy
at(nori_path, TAVI_IDEA[0], 2.5, 1.15)
at(nori_path, TAVI_IDEA[0] + 0.6, 3.15, 1.12)
at(nori_path, GROUP_LOOK - 0.3, 3.15, 1.12)
at(nori_path, GROUP_LOOK + 0.4, 2.0, 1.3)                      # dạt lên trên bên trái, ra khỏi đường tay Tavi chỉ
face(nori, 0.0, "sad")
look(nori, 0.0, 0.0, 0.0)
look(nori, NORI_LIGHT[0] - 0.1, 0.0, 0.0)
ry(nori.arm, NORI_LIGHT[0] - 0.1, 6)
ry(nori.arm, NORI_LIGHT[0] + 0.1, -60)                         # rọi xuống mầm cây
look(nori, NORI_LIGHT[0] + 0.1, 0.6, -1.0)
for ob in (light, sprout_glow):
    show(ob, NORI_LIGHT[0], True)
    show(ob, NORI_LIGHT[1], False)
ry(nori.arm, NORI_LIGHT[1], -60)
ry(nori.arm, NORI_LIGHT[1] + 0.2, 6)
talk(nori, NORI_LINE[0], NORI_LINE[1], "frown")
face(nori, LUMO_SPRING[0] + 0.3, "eager")
look(nori, LUMO_SPRING[0] + 0.3, 0.8, -0.4)                    # nhìn Lumo
face(nori, LUMO_TRIP + 0.05, "worried")                          # lo cho Lumo vấp
look(nori, LUMO_TRIP + 0.05, 0.8, -0.9)
face(nori, LUMO_PULLED[1], "happy")                             # thở phào
look(nori, LUMO_PULLED[1], 0.8, -0.4)
face(nori, COMPASS_BUZZ[0] + 0.2, "eager")                      # tò mò tiếng TÍT
look(nori, LUMO_LINE2[0], 0.8, -0.6)
face(nori, DIG[2] + 0.02, "shock")
face(nori, PIKO_BLINK[0] + 0.1, "neutral")
look(nori, LUMO_PUZZLE[0], 0.3, -1.0)                           # nhìn cái thìa cong dưới đất
scl(nori.root, GROUP_LOOK - 0.1, -1, 1)                         # quay sang phải, ngước theo tay Tavi
scl(nori.root, GROUP_LOOK + 0.05, 1, 1)
nori.dir = 1
lean(nori, GROUP_LOOK + 0.05, 0)
lean(nori, GROUP_LOOK + 0.3, -10)
face(nori, GROUP_LOOK + 0.3, "eager")
look(nori, GROUP_LOOK + 0.3, 0.5, 1.0)

# --- Lumo: co người ủ rũ, bật dậy, lao đi, vấp, rút la bàn, thắc mắc, nghe Tavi
at(lumo.root, 0.0, 1.6, 0)
scl(lumo.root, 0.0, 1.03, 0.94)                                 # co người ủ rũ (cúi đầu, cụp tai, rủ đuôi là chính)
face(lumo, 0.0, "sad", 20)
lean(lumo, 0.0, 10)
ry(lumo.head, 0.0, 18)
ears(0.0, -65)
ry(lumo.arm, 0.0, 6)
ry(lumo.arm_far, 0.0, -6)
ry(lumo.tail, 0.0, -30)
for t in (TITLE[0] + 1.0, NORI_FLY_IN[0] + 2.0, NORI_LINE[0] + 0.6):
    blink(lumo, t)
# bật dậy
s0, s1 = LUMO_SPRING
scl(lumo.root, s0, 1.03, 0.94)
lean(lumo, s0, 10)
ry(lumo.head, s0, 18)
ears(s0, -65)
scl(lumo.root, s0 + 0.12, 1.05, 0.9)                            # lấy đà
scl(lumo.root, s0 + 0.3, 0.97, 1.04)
at(lumo.root, s0, 1.6, 0)
at(lumo.root, s0 + 0.3, 1.6, 0.1)
lean(lumo, s0 + 0.3, 0)
ry(lumo.head, s0 + 0.32, 0)
ears(s0 + 0.32, 10)
face(lumo, s0 + 0.25, "eager")
scl(lumo.root, s1, 1, 1)
at(lumo.root, s1 + 0.05, 1.6, 0)
ry(lumo.tail, s0, -30)
loop(lumo.tail, s0 + 0.3, LUMO_DASH[0], 0.4, 8, 24)
# "Đi tìm nước cho vườn!": đấm tay ra trước ngang ngực
ry(lumo.arm, LUMO_LINE[0] - 0.1, 6)
ry(lumo.arm, LUMO_LINE[0] + 0.1, -95)
ry(lumo.arm, LUMO_LINE[1] - 0.1, -95)
ears(LUMO_LINE[0] + 0.1, 15)
talk(lumo, LUMO_LINE[0], LUMO_LINE[1], "smile")
# lao đi: một bước, hai bước, tới vết nứt
d0, d1 = LUMO_DASH
at(lumo.root, d0, 1.6, 0)
ry(lumo.arm, d0, -40)
ry(lumo.arm_far, d0, -6)
for i, x in enumerate((1.75, 1.88, 2.0, 2.1)):
    t = d0 + (d1 - d0) * (i + 1) / 4
    at(lumo.root, t, x, 0.05 if i % 2 == 0 else 0.0)
    ry(lumo.arm, t, -60 if i % 2 == 0 else 20)
    ry(lumo.arm_far, t, 20 if i % 2 == 0 else -60)
lean(lumo, d0, 0)
lean(lumo, d0 + 0.2, 12)
lean(lumo, LUMO_TRIP, 12)
# vấp vết nứt, chúi người, tay chới với (không quá ngang ngực), rồi treo chúi trên vết nứt nhờ quai túi
face(lumo, LUMO_TRIP + 0.05, "shock", 26)
look(lumo, LUMO_TRIP + 0.05, 0.6, -1.0)
ears(LUMO_TRIP + 0.1, 30)
lean(lumo, LUMO_TRIP + 0.15, 25)
at(lumo.root, LUMO_TRIP + 0.15, 2.13, 0)                        # mũi chân kẹt mép vết nứt
loop(lumo.arm, LUMO_TRIP + 0.1, LUMO_DANGLE[1] - 0.05, 0.16, -95, -20)
loop(lumo.arm_far, LUMO_TRIP + 0.1, LUMO_DANGLE[1] - 0.05, 0.16, -20, -95)
lean(lumo, LUMO_STUMBLE[1], 32)
at(lumo.root, LUMO_STUMBLE[1], 2.16, 0)
lean(lumo, LUMO_DANGLE[0] + 0.2, 42)                            # chúi sâu, lơ lửng trên vết nứt
lean(lumo, LUMO_DANGLE[1], 42)
at(lumo.root, LUMO_DANGLE[1], 2.17, 0)
look(lumo, LUMO_DANGLE[0], 0.5, -1.0)
ry(lumo.tail, LUMO_TRIP, 12)
ry(lumo.tail, LUMO_TRIP + 0.2, 40)                              # đuôi vung lên
# bị kéo đứng lại
lean(lumo, p0 + 0.2, -8)
at(lumo.root, p0 + 0.25, 2.1, 0)
lean(lumo, p1, 0)
ry(lumo.arm, p0 + 0.25, 6)
ry(lumo.arm_far, p0 + 0.25, -6)
ry(lumo.tail, p0 + 0.25, 12)
ears(p0 + 0.25, 6)
face(lumo, p0 + 0.35, "happy")                                  # thở phào
look(lumo, p0 + 0.35, 0.0, 0.0)
ry(lumo.head, TAVI_LINE[0], 0)
ry(lumo.head, TAVI_LINE[0] + 0.3, 18)                          # nhìn xuống vết nứt
face(lumo, TAVI_LINE[0] + 0.2, "sheepish", 12)
ears(TAVI_LINE[0] + 0.2, -55)
scl(lumo.root, TAVI_LINE[0] + 0.3, 1, 1)
scl(lumo.root, TAVI_LINE[0] + 0.5, 1.04, 0.95)                  # nhún vai ngượng
scl(lumo.root, TAVI_LINE[0] + 0.8, 1, 1)
# la bàn rung trong túi da: TÍT TÍT TÍT
b0, b1 = COMPASS_BUZZ
face(lumo, b0 + 0.05, "shock", 18)
look(lumo, b0 + 0.05, -0.3, -0.9)
ears(b0 + 0.05, 10)
ry(lumo.head, b0 + 0.2, 24)
jitter(lumo.bag, b0, b1, 0.008, 0.05)
for t in (b0 + 0.05, b0 + 0.45, b0 + 0.85):
    show(buzz, t, True)
    show(buzz, t + 0.2, False)
o0, o1 = COMPASS_OUT                                            # rút la bàn, cầm hai tay trước ngực (như cận S6)
ry(lumo.arm, o0, 6)
ry(lumo.arm, o0 + 0.15, -15)
show(compass, o0 + 0.25, True)
ry(needle, o0 + 0.25, 0)
ry(needle, o1, 300)                                             # mũi sao quay loạn
ry(lumo.arm, o1 - 0.05, -70)
ry(lumo.arm_far, o1 - 0.2, -6)
ry(lumo.arm_far, o1 - 0.05, -70)
ry(lumo.head, o1 - 0.05, 20)
face(lumo, o1 - 0.1, "eager", 20)
look(lumo, o1 - 0.1, 0.3, -0.7)
ears(o1 - 0.1, 8)
aim(SHOT["S7"][0], -70)
# "Có gì lạ kìa!": chìa la bàn về phía Piko
e0, e1 = LUMO_LINE2
ry(lumo.arm, e0 - 0.05, -70)
ry(lumo.arm, e0 + 0.15, -95)
aim(e0 - 0.05, -70)
aim(e0 + 0.15, -95)
ry(lumo.head, e0, 20)
ry(lumo.head, e0 + 0.2, 0)
look(lumo, e0 + 0.2, 0.8, 0.0)
lean(lumo, e0, 0)
lean(lumo, e0 + 0.2, 6)
face(lumo, e0 + 0.2, "eager")                                   # ngẩng đầu: bỏ phần bù
talk(lumo, e0, e1, "smile")
ry(lumo.arm, e1 + 0.1, -95)
ry(lumo.arm, e1 + 0.4, -70)
ry(lumo.arm_far, e1 + 0.1, -70)
ry(lumo.arm_far, e1 + 0.4, -6)
aim(e1 + 0.1, -95)
aim(e1 + 0.4, -70)
lean(lumo, e1 + 0.4, 0)
face(lumo, PIKO_RUMMAGE[0] + 0.3, "neutral")
face(lumo, DIG[2] + 0.02, "shock")
ears(DIG[2] + 0.02, 12)
face(lumo, PIKO_BLINK[0] + 0.1, "neutral")
ears(PIKO_BLINK[0] + 0.1, 6)
# lúc máy ở cú cận, Lumo bước tới cúi xuống cạnh cái thìa, kề la bàn sát thìa (cú cận ở X = 30 kể rõ việc này);
# S11 mở ra với Lumo còn cúi cạnh thìa rồi đứng dậy
w0, w1 = STAR_STILL
x0, x1 = LUMO_TEST
at(lumo.root, w0, 2.1, 0)
at(lumo.root, w0 + 0.15, 2.32, 0.04)
at(lumo.root, x0, 2.55, 0)
ry(lumo.arm, w0, -70)
ry(lumo.arm_far, w0, -6)
lean(lumo, w0, 0)
scl(lumo.root, x0, 1, 1)
ry(lumo.head, x0, 0)
lean(lumo, x0 + 0.3, 38)                                        # chồm xuống sát mặt đất
scl(lumo.root, x0 + 0.3, 1.03, 0.9)
ry(lumo.arm, x0 + 0.3, -40)
ry(lumo.arm_far, x0 + 0.3, -40)
ry(lumo.head, x0 + 0.3, 14)
look(lumo, x0 + 0.3, 0.6, -0.8)
aim(w0, -70)
aim(x0 + 0.3, -40, -38, 85)
# nhìn thìa, nhìn la bàn, nghiêng đầu: "Thìa thôi mà?"
z0, z1 = LUMO_PUZZLE                                            # đứng dậy, nhìn thìa, nhìn la bàn
for ob, a in ((lumo.arm, -40), (lumo.arm_far, -40), (lumo.head, 14)):
    ry(ob, LUMO_STAND[0], a)
lean(lumo, LUMO_STAND[0], 38)
scl(lumo.root, LUMO_STAND[0], 1.03, 0.9)
aim(LUMO_STAND[0], -40, -38, 85)
lean(lumo, LUMO_STAND[1], 0)
scl(lumo.root, LUMO_STAND[1], 1, 1)
ry(lumo.arm_far, LUMO_STAND[1], -6)
ry(lumo.head, LUMO_STAND[1], 10)
look(lumo, LUMO_STAND[1], 0.6, -0.8)                            # nhìn cái thìa cong dưới đất
ry(lumo.arm, LUMO_STAND[1], -60)
aim(LUMO_STAND[1], -60, 0, 120)
ry(lumo.arm, z0 + 0.8, -55)                                     # đưa la bàn lại gần mặt
aim(z0 + 0.8, -55, 0, 128)
ry(lumo.head, z0 + 0.8, 10)
ry(lumo.head, LUMO_LOOK_COMPASS[1], 24)
look(lumo, LUMO_LOOK_COMPASS[1], 0.3, -1.0)                     # nhìn la bàn
ry(lumo.head, LUMO_TILT[0], 24)
ry(lumo.head, LUMO_TILT[1], -14)                                # nghiêng đầu
ears(LUMO_TILT[0], 6)
ears(LUMO_TILT[1], -20, 12)
face(lumo, z1 - 0.2, "puzzled")
look(lumo, z1 - 0.2, 0.0, 0.0)
talk(lumo, LUMO_LINE3[0], LUMO_LINE3[1], "o")
# Tavi dậm đất: Lumo lùi lại một chút, quay sang nhìn Tavi, rồi nghe giảng, gật đầu theo từng bước
k0 = TAVI_KNOCK[0]
ry(lumo.head, k0, -14)
ears(k0, -20, 12)
at(lumo.root, k0 + 0.1, 2.55, 0)
at(lumo.root, k0 + 0.35, 2.25, 0)
scl(lumo.root, k0 + 0.1, 1, 1)
scl(lumo.root, k0 + 0.25, -1, 1)
lumo.dir = -1
ry(lumo.head, k0 + 0.25, 0)
ears(k0 + 0.3, 12)
face(lumo, k0 + 0.3, "eager")
look(lumo, k0 + 0.3, 0.6, -0.6)                                 # nhìn chân Tavi dậm đất
look(lumo, TAVI_LOOK_UP[1], 0.6, 0.8)                           # nhìn theo Tavi ngước lên
look(lumo, TAVI_GATHER[0], 0.8, 0.2)
for n0 in (TAVI_GATHER[0], TAVI_SHIVER[0], TAVI_RAIN[0]):
    ry(lumo.head, n0 + 0.2, 0)
    ry(lumo.head, n0 + 0.4, 12)
    ry(lumo.head, n0 + 0.6, 0)
ry(lumo.tail, LUMO_DASH[0] + 0.1, 12)
ry(lumo.tail, k0 + 0.2, 12)
loop(lumo.tail, k0 + 0.3, GROUP_LOOK, 0.5, 8, 24)
ears(TAVI_RAIN[0], 15)
i0, i1 = TAVI_IDEA                                              # Tavi "à!": Lumo giật mình rồi chồm tới nghe
face(lumo, i0 + 0.4, "shock")
ears(i0 + 0.4, 20)
lean(lumo, i0 + 0.3, 0)
lean(lumo, i0 + 0.5, -4)
lean(lumo, i1, 6)
face(lumo, i1, "eager")
b0, b1 = TAVI_SHIVER                                            # "làm lạnh,": Lumo nhắm tịt mắt rùng mình theo
face(lumo, b0 + 0.3, "squint")
scl(lumo.root, b0 + 0.3, -1.03, 0.97)
scl(lumo.root, b0 + 0.9, -1, 1)
face(lumo, b0 + 0.9, "eager")
lean(lumo, TAVI_POINT[0], 0)
at(lumo.root, TAVI_POINT[0] + 0.1, 2.25, 0)
at(lumo.root, TAVI_POINT[0] + 0.35, 2.12, 0)                    # lùi lại nhường chỗ cho Tavi bước lên
# cả nhóm ngước theo tay Tavi: Lumo quay lại, nhón người, như sắp lao đi
scl(lumo.root, GROUP_LOOK - 0.4, -1, 1)
scl(lumo.root, GROUP_LOOK - 0.25, 1, 1)
lumo.dir = 1
lean(lumo, GROUP_LOOK - 0.25, 0)
ry(lumo.head, GROUP_LOOK - 0.25, 0)
ry(lumo.head, GROUP_LOOK, -26)
ears(GROUP_LOOK, 12)
face(lumo, GROUP_LOOK - 0.1, "eager")
look(lumo, GROUP_LOOK - 0.1, 0.7, 1.0)
scl(lumo.root, GROUP_LOOK + 0.1, 1, 1.03)
scl(lumo.root, SECONDS, 1, 1.03)
lean(lumo, GROUP_LOOK + 0.1, -4)

# --- Piko: quay sang, lục túi, rút ra cái thìa, đào, thìa cong, đặt thìa xuống
lean(piko, PIKO_TURN - 0.15, 0)
scl(piko.root, PIKO_TURN - 0.15, 1, 1)
at(piko.root, PIKO_TURN - 0.15, 3.42, 0)
scl(piko.root, PIKO_TURN, -1, 1)
piko.dir = -1
lean(piko, PIKO_TURN, 0)
face(piko, PIKO_TURN + 0.1, "eager")
look(piko, PIKO_TURN - 0.1, 0.0, 0.0)
look(piko, PIKO_TURN + 0.1, 0.8, 0.2)                           # nghe TÍT, quay sang nhìn Lumo
look(piko, PIKO_CHECK - 0.1, 0.8, 0.2)
look(piko, PIKO_CHECK + 0.1, 0.5, -1.0)                         # ngó xuống cái túi của mình
blink(piko, PIKO_CHECK + 0.3)
u0, u1 = PIKO_RUMMAGE
ry(piko.arm, u0, 6)
scl(piko.arm, u0, 1, 1)
ry(piko.arm, u0 + 0.25, -27)                                    # thò tay xuống túi ở hông
scl(piko.arm, u0 + 0.25, 1, 1.15)
loop(piko.arm, u0 + 0.35, u1 - 0.1, 0.24, -20, -34)            # lục lọi
loop(piko.bag, u0, u1, 0.16, -16, 16)
lean(piko, u0 + 0.2, 8)
look(piko, u0 + 0.2, 0.9, -0.3)
key(piko.arm, "location", SPOON_OUT - 0.06, (0.24, -0.029, 0.22))
key(piko.arm, "location", SPOON_OUT - 0.05, (0.24, -0.035, 0.22))  # tay và thìa lên lớp trước túi
show(spoon, SPOON_OUT - 0.05, True)
ry(piko.arm, SPOON_OUT + 0.2, -70)                              # giơ cái thìa ra trước mặt
scl(piko.arm, SPOON_OUT + 0.2, 1, 1)
face(piko, SPOON_OUT + 0.1, "eager")
look(piko, SPOON_OUT + 0.2, 1.0, -0.3)
loop(piko.bag, SPOON_OUT, DIG[0] - 0.1, 1.0, -5, 5)
k0, k1 = PIKO_LOOK
lean(piko, k0, 4)                                               # nhìn thìa
look(piko, k0, 1.0, -0.3)
look(piko, PIKO_GLANCE_FLOWER[0], -1.0, -0.6)                   # liếc bông hoa gục phía sau
look(piko, PIKO_GLANCE_FLOWER[1], -1.0, -0.6)
lean(piko, PIKO_GLANCE_FLOWER[1], 4)
lean(piko, PIKO_LOOK_GROUND[1], 14)                             # nhìn đất
look(piko, PIKO_LOOK_GROUND[1], 0.6, -1.0)
ry(piko.arm, PIKO_GLANCE_FLOWER[1], -70)
ry(piko.arm, k1, -110)
lean(piko, k1, 8)
for i, h in enumerate(DIG):                                     # CỘP. CỘP. CỘP!
    if i:
        ry(piko.arm, h - 0.3, -145 if i == 2 else -110)
    ry(piko.arm, h, -35)                                        # mũi thìa chạm đất phía trước, xa cái túi
    show(dust, h, True)
    show(dust, h + 0.25, False)
    scl(dust, h, 0.5, 0.5)
    scl(dust, h + 0.24, 1.3, 1.3)
    if i < 2:
        scl(piko.root, h - 0.02, -1, 1)
        scl(piko.root, h + 0.06, -1.07, 0.93)
        scl(piko.root, h + 0.18, -1, 1)
loop(piko.bag, DIG[0], PIKO_SHAKE[1], 0.2, -18, 18)
show(spoon, DIG[2], False)                                      # cán thìa cong vòng
show(spoon_bent, DIG[2], True)
face(piko, DIG[2] + 0.02, "shock")
for i, t in enumerate(steps(DIG[2] + 0.02, PIKO_SHAKE[1] - 0.05, 0.05)):   # rung bần bật
    scl(piko.root, t, -1.06 if i % 2 else -0.95, 0.94 if i % 2 else 1.05)
    at(piko.root, t, 3.42 + (0.012 if i % 2 else -0.012), 0)
scl(piko.root, PIKO_SHAKE[1], -1, 1)
at(piko.root, PIKO_SHAKE[1], 3.42, 0)
ry(piko.arm, DIG[2] + 0.1, -30)                                 # thìa cắm đất, cán gập
ry(piko.arm, DIG[2] + 0.5, -125)                                # giơ ngay thìa cong lên ngang mắt, giữa khung S9
look(piko, DIG[2] + 0.5, 1.0, 0.1)                              # trố mắt nhìn cái thìa cong
lean(piko, PIKO_SHAKE[1] + 0.1, 8)
lean(piko, PIKO_BLINK[0] + 0.1, 0)
face(piko, PIKO_BLINK[0] + 0.05, "puzzled")
look(piko, PIKO_BLINK[0] + 0.05, 1.0, 0.1)
blink(piko, PIKO_BLINK[0] + 0.25)
blink(piko, PIKO_BLINK[0] + 0.45)
q0, q1 = PIKO_SET_SPOON                                         # đặt cái thìa cong xuống đất, xa cái túi
ry(piko.arm, q0, -125)
ry(piko.arm, q1 - 0.1, -40)
lean(piko, q0, 0)
lean(piko, q1 - 0.1, 12)
show(spoon_bent, q1 - 0.05, False)
show(spoon_ground, q1 - 0.05, True)
ry(piko.arm, q1 + 0.2, 6)
key(piko.arm, "location", q1 + 0.2, (0.24, -0.035, 0.22))
key(piko.arm, "location", q1 + 0.21, (0.24, -0.029, 0.22))    # tay về lớp cũ
lean(piko, q1 + 0.3, 0)
look(piko, q1, 0.8, -1.0)
look(piko, PIKO_BLINK2 - 0.2, 1.0, 0.3)                         # nhìn Lumo, chớp mắt
blink(piko, PIKO_BLINK2)
look(piko, TAVI_KNOCK[0], 1.0, -0.2)                            # nhìn Tavi dậm đất
loop(piko.bag, PIKO_SHAKE[1] + 0.1, SECONDS, 1.4, -5, 5)
bob(piko.root, STAR_STILL[1], TAVI_LOOK_LEAF[0], 3.42, 0.9, 0.015)
lf = TAVI_LOOK_LEAF[0] + 0.5                                     # chiếc lá lấp lánh: Piko mê đồ lấp lánh, ngước lên, nảy một cái
face(piko, lf, "eager")
look(piko, lf, -0.3, 1.0)
at(piko.root, lf + 0.1, 3.42, 0.0)
at(piko.root, lf + 0.25, 3.42, 0.07)
at(piko.root, lf + 0.4, 3.42, 0.0)
look(piko, TAVI_LOOK_UP[1], 0.8, 0.3)
face(piko, TAVI_IDEA[0], "neutral")
bob(piko.root, TAVI_LOOK_UP[0], GROUP_LOOK - 0.1, 3.42, 0.9, 0.015)
scl(piko.root, GROUP_LOOK + 0.1, -1, 1)                         # quay sang phải, ngước theo tay Tavi
lean(piko, GROUP_LOOK + 0.1, 0)
scl(piko.root, GROUP_LOOK + 0.25, 1, 1)
piko.dir = 1
lean(piko, GROUP_LOOK + 0.25, 0)
lean(piko, GROUP_LOOK + 0.5, -16)
face(piko, GROUP_LOOK + 0.45, "eager")
look(piko, GROUP_LOOK + 0.45, 0.6, 1.0)

# --- S6 cận la bàn: ngôi sao quay loạn rồi dừng, mũi sao chỉ sang phải hơi chúc xuống, về túi của Piko
END = NEEDLE_TO_BAG + 360 * 2
ry(compass_star, 0.0, 15)
ry(compass_star, STAR_SPIN[0], 15)
for t in steps(STAR_SPIN[0] + 0.1, STAR_SPIN[1], 0.1):
    u = min(1.0, (t - STAR_SPIN[0]) / (STAR_SPIN[1] - STAR_SPIN[0]))
    ry(compass_star, t, 15 + (END - 15) * (1 - (1 - u) ** 2.5))
for dt, d in ((0.1, 8), (0.2, -4), (0.3, 0)):                  # khựng lại, rung nhẹ rồi đứng yên
    ry(compass_star, STAR_SPIN[1] + dt, END + d)

# --- S10 cận la bàn kề cái thìa: la bàn hạ xuống sát cái thìa, mũi sao giật về thìa một nhịp rồi quay phắt lại chỉ túi
at(test_c, w0, 29.6, 0.34)
at(test_c, x0, 29.6, 0.34)
at(test_c, x0 + 0.35, 29.62, 0.26)
ry(test_star, w0, 99)
ry(test_star, x0, 99)
ry(test_star, NEEDLE_TO_SPOON, 148)                             # mũi sao giật về phía cái thìa…
ry(test_star, x1, 148)
ry(test_star, x1 + 0.15, 92)                                    # …rồi quay phắt lại chỉ túi
ry(test_star, x1 + 0.27, 101)
ry(test_star, x1 + 0.39, 97)

# --- ánh vàng ở miệng túi mỗi lần la bàn chỉ vào túi; dải mây trên đỉnh đồi trôi rất chậm
flash(hint_glint, STAR_SPIN[1] + 0.35)
flash(bag_glint, LUMO_LINE2[0] + 0.3)
flash(test_glint, LUMO_TEST[1] + 0.2)
flash(test_glint, LUMO_TEST[1] + 0.85)
twinkle(leaf_glint, TAVI_LOOK_LEAF[0] + 0.5, TAVI_LOOK_UP[0] + 0.3)   # lá còn ướt sương lấp lánh trong cú cận chiếc lá
at(mist, 0.0, 4.18, 1.93)
at(mist, SECONDS, 4.28, 1.94)

# --- tên phim
for ob in title:
    show(ob, TITLE[0], True)
    show(ob, TITLE[1], False)

# ================================================================ máy quay, render
CAMS = {"S1": (3.58, 0.66, 1.75), "S2": (3.65, 0.55, 3.1), "S3": (2.0, 1.2, 7.4), "S4": (2.1, 0.46, 2.5),
        "S5": (1.97, 0.45, 2.9), "S6": (20.0, 0.0, 1.5), "S7": (2.85, 0.56, 2.5), "S8": (3.35, 0.32, 2.0),
        "S9": (3.05, 0.4, 1.0), "S10": (29.95, 0.08, 1.5), "S11": (2.6, 0.6, 3.0), "S12": (3.6, 0.72, 1.4),
        "S13": (1.9, 0.6, 2.3), "S14": (2.9, 0.82, 4.6)}                                # tâm X, tâm Z, bề ngang khung (m); đáy khung chừa cho CC
cameras(SHOTS, CAMS)
cam = bpy.data.objects["Cam_S12"]                               # S12: từ chiếc lá, máy lia theo mắt Tavi lên đỉnh đồi
for t, (cx, cz, w) in ((TAVI_LOOK_UP[0], CAMS["S12"]), (TAVI_LOOK_UP[1], (4.2, 1.72, 1.8))):
    key(cam, "location", t, (cx, -10.0, cz))
    key(cam.data, "ortho_scale", t, w)
finish(SECONDS, OUT_BLEND, (1.5, 2.6, 3.7, 4.6, 5.55, 6.9, 8.7, 11.6, 14.7, 16.0, 18.5, 20.9, 21.7, 22.5, 23.4, 25.1,
                            27.5, 29.4, 31.0, 32.1, 33.95, 35.25, 35.5, 35.8, 36.5, 37.2, 38.2, 38.8, 39.5, 40.0, 40.6,
                            42.0, 43.6, 44.6, 45.2, 46.3, 47.3, 48.2, 49.3, 50.4, 51.6, 53.5, 54.6))
