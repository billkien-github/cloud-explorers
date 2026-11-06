"""
TEST_Cutout canh01: thử bộ nhân vật cutout 2D (pipeline/cutout.py, 03_CONTENT/PREVIZ_2D.md) trên khoảnh khắc Cảnh 3
tập 01 (beat sheet: 03_CONTENT/Scripts/EP001_great_rain_experiment.md). Lumo vội với tay về nút đỏ, khựng lại; Piko bị
nút lấp lánh hút mắt, nhảy lên lưng Lumo, tay Lumo đè xuống nút. Mốc thời gian và CC: timing.py.
    .\\pipeline\\run.ps1 build -Shot 03_CONTENT\\Previz_2D\\TEST_Cutout\\canh01
    .\\pipeline\\run.ps1 preview -Shot 03_CONTENT\\Previz_2D\\TEST_Cutout\\canh01
    blender -b --factory-startup -P pipeline\\cc.py -- <cảnh>\\renders\\canh01_preview.mp4 <cảnh>\\timing.py <cảnh>\\renders\\canh01_preview_cc.mp4
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.dont_write_bytecode = True                                  # không để __pycache__ cạnh timing.py
sys.path[:0] = [str(HERE), str(ROOT / "pipeline")]
from cutout import *  # noqa: E402,F403  bộ cutout: keyframe, hình, mặt, nhân vật, máy quay
from timing import *  # noqa: E402,F403  FPS, SECONDS, SHOTS, mốc hành động, CC của cảnh

OUT_BLEND = HERE / f"{HERE.name}.blend"
start(FPS)


# ================================================================ bối cảnh: đỉnh đồi, máy, vườn mầm, mây
part("Sky", None, [([(-4, -1), (8, -1), (8, 6), (-4, 6)], "#BFE4F7")], 3.0)
part("Ground", None, [([(-4, -1), (8, -1), (8, 0.02), (-4, 0.02)], "#E9D9B6")], 2.0)
part("Garden", None, [([(1.45, -0.05), (3.2, -0.05), (3.2, 0.03), (1.45, 0.03)], "#6B4A33"),
                      ([(3.2, -0.05), (3.65, -0.05), (3.65, 0.03), (3.2, 0.03)], "#C2A27A")], 0.6)   # dải khô ở mép phải
sprouts = []
for i in range(9):
    sx = 1.55 + i * 0.18
    sprouts += [(rrect(0.012, 0.09, 0.005, sx, 0.07), "#5FA544"), (ell(0.03, 0.015, sx - 0.025, 0.11), "#6DBB4E"),
                (ell(0.03, 0.015, sx + 0.025, 0.12), "#6DBB4E")]
sprouts += [([(3.42, 0.02), (3.44, 0.02), (3.47, 0.07), (3.52, 0.05), (3.52, 0.06), (3.46, 0.09)], "#8B6A3E")]  # mầm héo
part("Sprouts", None, sprouts, 0.55)

machine = node("Machine", None, (0.0, 0.0), 0.3)
part("Machine_Body", machine, [(rrect(0.08, 0.14, 0.02, -0.3, 0.07), "#6E6E6E"), (rrect(0.08, 0.14, 0.02, 0.3, 0.07), "#6E6E6E"),
                               (rrect(0.9, 1.0, 0.08, 0, 0.62), "#D9C6AA"), (rrect(0.9, 0.08, 0.02, 0, 0.3), "#BFA98A"),
                               (ell(0.33, 0.28, 0, 1.12, 0, 180), "#A8E0F2"),
                               ([(0, 1.18), (0.07, 1.27), (0, 1.36), (-0.07, 1.27)], "#4FB3E8"),
                               (rrect(0.1, 0.16, 0.02, 0, 1.46), "#9A9A9A")])
part("Machine_Knob", machine, [(ell(0.06, 0.06), "#4A4A4A"), (rrect(0.012, 0.05, 0.005, 0, 0.02), WHITE)], -0.02, (-0.33, 0.48))
part("Machine_Gauge", machine, [(ell(0.1, 0.1), "#F5F5F5"), (arc(0.075, 45, 170, 0.02), "#7BC67B"), (arc(0.075, 10, 45, 0.02), "#E05050")],
     -0.02, (-0.28, 0.84))
needle = part("Machine_Needle", machine, [(rrect(0.01, 0.08, 0.004, 0, 0.04), "#333333")], -0.03, (-0.28, 0.84))
part("Machine_Button", machine, [(ell(0.075, 0.075), "#B71C1C"), (ell(0.06, 0.06, 0.005, 0.005), "#E53935"),
                                 (ell(0.02, 0.02, 0.02, 0.03), "#FF9A9A")], -0.02, (0.45, 0.5))   # ngang ngực Lumo
glint = part("Machine_Glint", machine, [(star(0.07), "#FFF27A")], -0.04, (0.49, 0.57))

cloud = part("Cloud", None, [(ell(0.32, 0.16), WHITE), (ell(0.2, 0.15, -0.25, 0.05), WHITE), (ell(0.22, 0.17, 0.22, 0.06), WHITE),
                             (ell(0.18, 0.15, 0.0, 0.14), WHITE)], 1.0, (2.45, 1.75), unique="CloudMat")
part("Rain", cloud, [(rrect(0.008, 0.07, 0.003, rx, rz), "#7FC4E8")
                     for rx, rz in ((-0.3, -0.3), (-0.15, -0.5), (0.0, -0.35), (0.15, -0.6), (0.3, -0.4), (-0.22, -0.8),
                                    (0.08, -0.85), (0.25, -0.95))], 0.05)

tavi = build_tavi(-0.82, -0.3)
lumo = build_lumo(1.12, -0.32)
piko = build_piko(1.95, -0.28)                                 # sau Lumo: khi đáp lên lưng vẫn thấy mặt Lumo
nori = build_nori(2.6, 1.05, -0.2)
tavi.dir, lumo.dir, piko.dir, nori.dir = 1, 1, -1, -1

# ================================================================ diễn
for p in (lumo, tavi, nori, piko):
    face(p, 0.0, "neutral")
    ry(p.arm, 0.0, 6)
    lean(p, 0.0, 0)

# --- Tavi: nhìn đồng hồ, giật mình, bước ra, hô muộn một nhịp
ry(tavi.arm_far, 0.0, -6)
loop(tavi.tail, 0.0, SECONDS, 1.6, -4, 4)
ry(tavi.head, 0.3, -18)                                       # ngước nhìn đồng hồ
for t in (2.0, 4.3):
    blink(tavi, t)
ry(tavi.head, MAX_POWER[0], -18)
face(tavi, MAX_POWER[0] + 0.05, "shock")
ry(tavi.head, MAX_POWER[0] + 0.2, 0)
at(tavi.root, TAVI_STEP[0], -0.82, 0)                         # bước ra đứng trước thân máy
at(tavi.root, TAVI_STEP[0] + 0.15, -0.6, 0.04)
at(tavi.root, TAVI_STEP[1], -0.3, 0)
for arm, rest, up in ((tavi.arm, 6, -95), (tavi.arm_far, -6, -150)):   # tay gần chỉ về Lumo, tay xa giơ cao
    ry(arm, TAVI_STEP[1], rest)
    ry(arm, TAVI_SHOUT[0] + 0.1, up)
    ry(arm, TAVI_SHOUT[1], up)
    ry(arm, TAVI_SHOUT[1] + 0.4, rest)
lean(tavi, TAVI_STEP[1], 0)
lean(tavi, TAVI_SHOUT[0] + 0.1, 6)
lean(tavi, TAVI_SHOUT[1] + 0.4, 0)
face(tavi, TAVI_SHOUT[0], "shout")
face(tavi, TAVI_SHOUT[1] + 0.2, "worried")
ry(tavi.head, CLOUD_SWELL[0], 0)
face(tavi, CLOUD_SWELL[0] + 0.2, "shock")
ry(tavi.head, CLOUD_SWELL[0] + 0.5, -22)

# --- Nori: lơ lửng trên vườn, giảng về mưa, bị MAX POWER cắt ngang
scl(nori.root, 0.0, -1, 1)
for i in range(int(SECONDS) + 1):
    at(nori.root, i, 2.6, 1.05 + (0.03 if i % 2 else -0.03))
for w in nori.wings:
    loop(w, 0.0, SECONDS, 0.24, -14, 14)
for a in nori.antennae:
    loop(a, 0.0, SECONDS, 1.4, -6, 6)
talk(nori, NORI_TALK[0], NORI_TALK[1])
ry(nori.arm, NORI_TALK[0], 6)
ry(nori.arm, NORI_TALK[0] + 0.4, -60)                          # tay nhỏ minh hoạ khi giảng
ry(nori.arm, NORI_TALK[1], -60)
face(nori, NORI_TALK[1] + 0.05, "shock")
ry(nori.arm, NORI_TALK[1] + 0.3, 10)
lean(nori, CLOUD_SWELL[0], 0)
lean(nori, CLOUD_SWELL[0] + 0.5, -14)                          # ngửa lên nhìn mây

# --- Lumo: nhìn dải khô, vội với tay, khựng lại, bị đè xuống nút, nhận ra
scl(lumo.root, 0.0, 1, 1)
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, 0.0, -4)
ry(lumo.arm_far, 0.0, -6)
loop(lumo.tail, 0.0, LUMO_REACH[0], 0.5, 6, 20)
ry(lumo.head, LUMO_LOOK_DRY[0], 0)
ry(lumo.head, LUMO_LOOK_DRY[0] + 0.3, 12)                      # nhìn xuống dải khô
face(lumo, LUMO_LOOK_DRY[0] + 0.2, "sad")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, LUMO_LOOK_DRY[0] + 0.4, -32)
scl(lumo.root, LUMO_TURN, 1, 1)
scl(lumo.root, LUMO_TURN + 0.15, -1, 1)                        # quay sang trái, về phía nút
lumo.dir = -1
ry(lumo.head, LUMO_TURN, 0)
face(lumo, LUMO_TURN + 0.1, "eager")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, LUMO_TURN + 0.1, 4)
at(lumo.root, LUMO_REACH[0], 1.12, 0)                          # vội: bước nhanh, nhún
at(lumo.root, LUMO_REACH[0] + 0.15, 1.02, 0.04)
at(lumo.root, LUMO_REACH[1] - 0.2, 0.9, 0)
lean(lumo, LUMO_REACH[0], 0)
lean(lumo, LUMO_REACH[1] - 0.2, 4)                             # chồm tới
ry(lumo.arm, LUMO_REACH[0], 6)
ry(lumo.arm, LUMO_REACH[1] - 0.15, -92)                        # vươn tay, còn cách nút vài phân
ry(lumo.arm_far, LUMO_REACH[1] - 0.15, -40)
talk(lumo, LUMO_REACH[0], LUMO_REACH[1] + 0.2, "smile")
ry(lumo.tail, LUMO_REACH[0] + 0.3, 24)
# khựng lại: mặt lo, tai cụp hẳn ra sau, người ngả lại, tay lơ lửng
face(lumo, LUMO_FREEZE[0], "worried")
for e, deg in ((lumo.ear_near, -72), (lumo.ear_far, -78)):
    ry(e, LUMO_FREEZE[0], 4)
    ry(e, LUMO_FREEZE[0] + 0.15, deg)
lean(lumo, LUMO_FREEZE[0], 4)
lean(lumo, LUMO_FREEZE[0] + 0.25, -3)
ry(lumo.head, LUMO_FREEZE[0] + 0.25, -8)
ry(lumo.arm, LUMO_FREEZE[0], -92)
ry(lumo.arm, LUMO_PULL[0], -90)
ry(lumo.tail, LUMO_FREEZE[0] + 0.2, -28)                       # đuôi cụp
# bắt đầu rụt tay
ry(lumo.arm, LUMO_PULL[1] - 0.05, -55)
at(lumo.root, LUMO_PULL[0], 0.9, 0)
at(lumo.root, LUMO_PULL[1] - 0.05, 0.94, 0)
# Piko đáp lên lưng: chúi tới, tay đè xuống nút
at(lumo.root, CLICK, 0.94, 0)
at(lumo.root, CLICK + 0.1, 0.8, 0)
lean(lumo, CLICK, -3)
lean(lumo, CLICK + 0.1, 12)
ry(lumo.arm, CLICK, -55)
ry(lumo.arm, CLICK + 0.08, -100)
face(lumo, CLICK, "shock")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, CLICK, -72)
    ry(e, CLICK + 0.1, 8)                                      # tai bật dựng vì giật mình
lean(lumo, MAX_POWER[1], 9)
ry(lumo.arm, LUMO_REALIZE[0], -100)
# nhận ra: nhìn tay mình trên nút, tai cụp
ry(lumo.head, LUMO_REALIZE[0], -8)
ry(lumo.head, LUMO_REALIZE[0] + 0.3, 22)
face(lumo, LUMO_REALIZE[0] + 0.2, "sad")
for e in (lumo.ear_near, lumo.ear_far):
    ry(e, LUMO_REALIZE[0], 8)
    ry(e, LUMO_REALIZE[0] + 0.4, -48)
ry(lumo.head, CLOUD_SWELL[0], 22)
ry(lumo.head, CLOUD_SWELL[0] + 0.4, -25)                       # ngước lên mây
face(lumo, CLOUD_SWELL[0] + 0.2, "shock")

# --- Piko: nút lấp lánh hút mắt, nén người, bật nhảy, đáp lên lưng Lumo
scl(piko.root, 0.0, -1, 1)
for i in range(7):                                             # nảy nhẹ tại chỗ
    t = i * 0.6
    at(piko.root, t, 1.95, 0)
    at(piko.root, t + 0.3, 1.95, 0.035)
at(piko.root, GLINT, 1.95, 0)
face(piko, GLINT + 0.05, "eager")
lean(piko, GLINT + 0.2, 8)                                     # chồm về phía nút
scl(piko.root, PIKO_CROUCH[0], -1, 1)
scl(piko.root, PIKO_CROUCH[1] - 0.05, -1.25, 0.72)             # nén
at(piko.root, PIKO_JUMP[0], 1.95, 0)
scl(piko.root, PIKO_JUMP[0] + 0.1, -0.85, 1.2)                 # giãn khi bật
at(piko.root, PIKO_JUMP[0] + 0.35, 1.5, 0.62)
lean(piko, PIKO_JUMP[0] + 0.35, -10)
at(piko.root, CLICK, 1.2, 0.3)                                 # đáp vào lưng Lumo, ở lớp sau
scl(piko.root, CLICK, -1, 1)
scl(piko.root, CLICK + 0.06, -1.22, 0.8)                       # bẹp khi đáp
at(piko.root, CLICK + 0.1, 1.1, 0.26)
scl(piko.root, CLICK + 0.25, -1, 1)
lean(piko, CLICK + 0.1, 0)
face(piko, CLICK + 0.1, "happy")
ry(piko.arm, CLICK + 0.1, -60)
face(piko, CLOUD_SWELL[0] + 0.2, "shock")
lean(piko, CLOUD_SWELL[0] + 0.4, -12)

# --- máy: kim chỉ NHẸ, lấp lánh, rung khi MAX POWER; mây phồng, sẫm lại
ry(needle, 0.0, -35)
ry(needle, MAX_POWER[0], -35)
ry(needle, MAX_POWER[0] + 0.25, 78)
for t0, t1, amp in ((MAX_POWER[0], MAX_POWER[1], 0.02), (CLOUD_SWELL[0], CLOUD_SWELL[1], 0.012)):
    t, flip = t0, False
    while t < t1:
        at(machine, t, amp if flip else -amp, 0)
        ry(needle, t, 74 if flip else 82)
        t, flip = t + 0.08, not flip
    at(machine, t1, 0.0, 0)
scl(glint, 0.0, 0, 0)
for t, s in ((GLINT - 0.05, 0), (GLINT + 0.1, 1.0), (GLINT + 0.3, 0.55), (GLINT + 0.5, 1.0), (PIKO_JUMP[0], 0)):
    scl(glint, t, s, s)
cm = MATS["CloudMat"]
for t, s, x, col in ((0.0, 1.0, 2.45, (1, 1, 1)), (MAX_POWER[0], 1.0, 2.45, (1, 1, 1)), (MAX_POWER[1], 1.15, 2.4, (0.85, 0.87, 0.9)),
                     (CLOUD_SWELL[0], 1.15, 2.4, (0.85, 0.87, 0.9)), (CLOUD_SWELL[1], 1.9, 1.7, (0.27, 0.29, 0.33))):
    scl(cloud, t, s, s)
    at(cloud, t, x, 1.75 + 0.1 * (s - 1))
    key(cm, "diffuse_color", t, (*col, 1.0))

# ================================================================ máy quay, render
CAMS = {"S1": (1.25, 1.1, 5.0), "S2": (1.12, 0.6, 2.5), "S3": (1.2, 1.25, 5.4)}   # tâm X, tâm Z, bề ngang khung (m)
cameras(SHOTS, CAMS)
finish(SECONDS, OUT_BLEND, (1.5, 2.9, 3.4, 4.2, 5.1, 5.65, 6.9, 8.4, 10.6))
