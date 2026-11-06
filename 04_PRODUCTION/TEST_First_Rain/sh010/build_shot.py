"""
TEST_First_Rain sh010 — previz 27 giây, 7 shot cắt trong một timeline: Cảnh 3 tập 01 "Cơn mưa đầu tiên" rút gọn
(beat sheet: 03_CONTENT/Scripts/EP001_great_rain_experiment.md). Đủ 4 nhân vật dạng khối, làm video dẫn cho Seedance
(quy trình: 04_PRODUCTION/SEEDANCE.md). Mốc thời gian ở đầu file là nguồn cho prompt theo giây.
    .\\pipeline\\run.ps1 build -Shot 04_PRODUCTION\\TEST_First_Rain\\sh010
    .\\pipeline\\run.ps1 ref -Shot 04_PRODUCTION\\TEST_First_Rain\\sh010       # 1920x1080, 24fps, MP4 dẫn cho Seedance
Prompt và danh sách file tải lên: seedance/prompt.md.
Lưu bản sao sau mỗi giai đoạn vào backups/: stage1_set, stage2_cast, stage3_action, stage4_cameras.
Màu khối = nhân vật: CAM = Lumo, XANH LÁ = Tavi, TÍM NHẠT = Nori, XANH NGỌC = Piko; ô TRẮNG trước đầu = hướng mặt.
Máy, bối cảnh, đất vườn xám; nút MAX POWER đỏ; mây trắng. Tỉ lệ khối Lumo đo từ lumo_rig.blend.
Toạ độ: máy ở gốc, mặt trước máy nhìn -Y (phía máy quay); núm NHẸ và đồng hồ ở hông trái (-X, chỗ Tavi), nút đỏ ở
hông phải (+X); vườn mầm bên phải. Hướng nhân vật (yaw): 0 = nhìn -Y, 90 = nhìn +X, 180 = nhìn +Y, 270 = nhìn -X.
"""
import math
import pathlib
import random
import sys

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.path.insert(0, str(ROOT / "pipeline"))
from blocks import *  # noqa: E402,F403  khối, vật liệu, 4 nhân vật dạng khối, keyframe theo giây, máy quay
OUT_BLEND = HERE / "sh010.blend"
BACKUPS = HERE / "backups"
FPS, SECONDS = 24, 27
FRAMES = FPS * SECONDS

# ---------------------------------------------------------------- shot: (tên, bắt đầu, kết thúc giây)
SHOTS = [("S1", 0.0, 5.0), ("S2", 5.0, 9.0), ("S3", 9.0, 14.5), ("S4", 14.5, 18.5),
         ("S5", 18.5, 23.0), ("S6", 23.0, 24.5), ("S7", 24.5, 27.0)]

# ---------------------------------------------------------------- mốc hành động (giây)
KNOB_TURN = 1.0           # Tavi vặn núm NHẸ, vòm kính sáng xanh
CLOUD_POOF = 3.0          # mây bé phụt ra từ vòi
LUMO_TURN = (3.6, 4.6)    # Lumo quay người theo đám mây
CLOUD_ON_HEAD = 5.5       # mây bé đậu trên đầu Lumo
NOSE_DROP = 7.0           # giọt nước trúng mũi, tai dựng
SHOUT_WATER = (7.5, 8.3)  # LUMO: "NƯỚC!", hai tay giơ
CLOUD_GONE = (8.5, 9.0)   # mây bé tan
RAIN_CLOUD = (9.0, 10.2)  # mây lớn lan ra phủ vườn, mưa lất phất
LUMO_TO_GARDEN = (9.3, 9.9)  # Lumo quay sang, bước hai bước về phía vườn đứng xem
PIKO_HOP = (9.0, 10.0)    # Piko nảy vào vườn
NORI_TWIRL = (9.5, 10.5)  # Nori xoay một vòng, sáng hơn
PIKO_BOWL = 11.0          # Piko xẹp thành cái bát hứng mưa
PIKO_GULP = 12.5          # SLURP, phồng lại
TAVI_GAUGE = 13.0         # Tavi xem đồng hồ, gật gù
PIKO_TO_EDGE = (13.6, 14.3)  # Piko nảy sang mép vườn gần máy, đứng nhìn
EARS_DROOP = 15.5         # Lumo thấy dải khô: tai cụp, nghiêng đầu
LOOK_BUTTON = 16.5        # Lumo quay đầu về nút đỏ
WALK = (18.5, 19.5)       # Lumo kiễng chân vòng sang hông phải máy
WHISPER = (19.5, 20.5)    # LUMO: "Thêm chút nữa thôi…", tay nhích tới
PAW_STOPS = 20.5          # tay dừng trước nút, ngập ngừng, rụt dần
GLINT = 20.8              # nút đỏ lóe, Piko bật nhảy
CLICK = 21.5              # Piko đáp lên lưng Lumo, tay Lumo ấn nút
TAVI_SHOUT = (22.0, 23.0) # TAVI: "Không chạm nút—!" (bước ra trước máy để thấy Lumo)
MACHINE_GO = 24.5         # máy rung, vòm lóe đỏ, VRRRM
CLOUD_SWELL = 25.0        # mây phình to, sẫm lại; cả bốn ngước lên

# ---------------------------------------------------------------- bố trí (m)
BUTTON = Vector((0.525, -0.15, 0.50))   # hông phải máy; thấp để tay Lumo (tới ngang cằm) với được
KNOB = Vector((-0.53, -0.15, 0.48))     # hông trái máy
GAUGE = Vector((-0.51, -0.15, 0.82))
NOZZLE_TOP = Vector((0.0, 0.0, 1.78))
LUMO_START, LUMO_WATCH = Vector((0.35, -1.40, 0)), Vector((0.60, -1.60, 0))   # chỗ xem mây / chỗ đứng xem vườn
LUMO_AT_BUTTON, PUSH = Vector((0.905, 0.05, 0)), 0.06    # vai trái Lumo thẳng hàng với nút; bị Piko đẩy 6 cm về -X
TAVI_POS, TAVI_STEP = Vector((-0.88, -0.20, 0)), Vector((-0.75, -0.75, 0))
PIKO_START, PIKO_GARDEN, PIKO_WAIT = Vector((1.00, -1.30, 0)), Vector((1.95, -0.65, 0)), Vector((1.75, -0.30, 0))
NORI_POS, NORI_END = Vector((2.40, -0.20, 1.00)), Vector((0.60, -1.00, 1.20))
GARDEN_X, GARDEN_Y, DRY_X = (1.4, 3.4), (-0.9, 1.1), (3.4, 3.8)   # vườn được tưới / dải khô ở mép phải

random.seed(3)


def save_stage(name):
    BACKUPS.mkdir(exist_ok=True)
    path = BACKUPS / f"sh010_{name}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(path), compress=True, copy=True)
    print("STAGE_SAVED", path)


# ---------------------------------------------------------------- dọn scene
scene = start(FPS, SECONDS, 0.0, ("SET", "MACHINE", "CAST", "CLOUDS", "CAMERAS"))


# ================================================================ GIAI ĐOẠN 1: đỉnh đồi, vườn mầm, máy, mây
m_ground = material("M_Ground", (0.42, 0.41, 0.39), 0.9)
m_soil = material("M_Soil", (0.12, 0.115, 0.11), 0.95)
m_dry = material("M_DrySoil", (0.62, 0.60, 0.56), 0.95)
m_sprout = material("M_Sprout", (0.30, 0.30, 0.30), 0.8)

add_obj("Hilltop", sphere_bm(30.0, (0, 0, -30.0 * 0.04), (1, 1, 0.04), segs=64), m_ground, "SET")
gx0, gx1 = GARDEN_X
gy0, gy1 = GARDEN_Y
add_obj("Garden_Soil", box_bm((gx1 - gx0, gy1 - gy0, 0.08), ((gx0 + gx1) / 2, (gy0 + gy1) / 2, 0.0)), m_soil, "SET")
add_obj("Garden_DryStrip", box_bm((DRY_X[1] - DRY_X[0], gy1 - gy0, 0.085), (sum(DRY_X) / 2, (gy0 + gy1) / 2, 0.0)),
        m_dry, "SET")
bm = bmesh.new()
x = gx0 + 0.15
while x < gx1:
    y = gy0 + 0.15
    while y < gy1:
        cyl_bm(0.04, 0.14, (x, y, 0.11), bm=bm, cone_top=0.0)
        y += 0.34
    x += 0.30
add_obj("Sprouts", bm, m_sprout, "SET")
for i, y in enumerate((-0.4, 0.5)):          # mầm héo ở dải khô
    s = add_obj(f"Sprout_Wilted_{i}", cyl_bm(0.04, 0.14, (0, 0, 0.07), cone_top=0.0), m_sprout, "SET",
                loc=(sum(DRY_X) / 2, y, 0.04))
    s.rotation_euler = (math.radians(65), 0, math.radians(30 + 90 * i))

sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
COLS["SET"].objects.link(sun)
sun.data.energy, sun.data.angle = 3.5, math.radians(4)
sun.rotation_euler = (math.radians(48), 0, math.radians(30))
world = bpy.data.worlds.new("Sky")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.50, 0.66, 0.92, 1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9

# máy Rain-O-Matic (khối xám): thân, 4 chân, vòm kính, vòi; núm NHẸ + đồng hồ hông trái, nút MAX POWER hông phải
m_machine = material("M_Machine", (0.36, 0.36, 0.37), 0.55)
m_dark = material("M_MachineDark", (0.08, 0.08, 0.09), 0.5)
m_white = material("M_White", (0.85, 0.85, 0.85), 0.5)
m_dome = material("M_Dome", (0.10, 0.14, 0.22), 0.1, emit=((0.30, 0.60, 1.00), 0.0))
m_button = material("M_Button", (0.85, 0.02, 0.02), 0.35, emit=((1.0, 0.05, 0.02), 0.0))
machine = empty("MACHINE", "MACHINE")
bm = box_bm((1.0, 0.8, 1.06), (0, 0, 0.67))
for sx in (-1, 1):
    for sy in (-1, 1):
        cyl_bm(0.06, 0.14, (sx * 0.38, sy * 0.28, 0.07), bm=bm)
cyl_bm(0.07, 0.24, (0, 0, NOZZLE_TOP.z - 0.12), bm=bm, cone_top=0.10)
cyl_bm(0.10, 0.02, (0.505, BUTTON.y, BUTTON.z), axis="X", bm=bm)        # vành nút
add_obj("Machine_Body", bm, m_machine, "MACHINE", parent=machine)
dome = add_obj("Machine_Dome", sphere_bm(0.34, (0, 0, 1.20)), m_dome, "MACHINE", parent=machine)
knob = add_obj("Machine_Knob", box_bm((0.03, 0.03, 0.12), (-0.04, 0, 0.04), bm=cyl_bm(0.08, 0.06, axis="X")),
               m_dark, "MACHINE", parent=machine, loc=KNOB)
add_obj("Machine_Gauge", cyl_bm(0.10, 0.02, GAUGE, axis="X"), m_white, "MACHINE", parent=machine)
needle = add_obj("Machine_Needle", box_bm((0.01, 0.012, 0.08), (0, 0, 0.04)), m_dark, "MACHINE", parent=machine,
                 loc=GAUGE + Vector((-0.015, 0, 0)))
button = add_obj("Machine_Button", cyl_bm(0.07, 0.05, axis="X"), m_button, "MACHINE", parent=machine, loc=BUTTON)

m_cloud = material("M_Cloud", (0.92, 0.93, 0.95), 0.9)
m_cloud_small = material("M_CloudSmall", (0.92, 0.93, 0.95), 0.9)


def cloud_bm(blobs):
    bm = bmesh.new()
    for r, c in blobs:
        sphere_bm(r, c, (1, 1, 0.75), bm=bm, segs=20)
    return bm


cloud_small = add_obj("Cloud_Small", cloud_bm([(0.14, (0, 0, 0)), (0.11, (0.15, 0.02, -0.02)),
                                               (0.11, (-0.15, -0.02, -0.02)), (0.10, (0.03, 0.12, 0.0))]),
                      m_cloud_small, "CLOUDS")
cloud_rain = add_obj("Cloud_Rain", cloud_bm([(0.45, (0, 0, 0)), (0.38, (0.55, 0.2, -0.05)), (0.36, (-0.55, -0.2, -0.05)),
                                             (0.34, (0.2, -0.55, -0.02)), (0.34, (-0.25, 0.55, -0.02)),
                                             (0.30, (0.75, -0.35, -0.08)), (0.30, (-0.75, 0.35, -0.08))]),
                     m_cloud, "CLOUDS")
save_stage("stage1_set")

# ================================================================ GIAI ĐOẠN 2: bốn nhân vật dạng khối (pipeline/blocks.py)
lumo, tavi, nori, piko = build_lumo(LUMO_START), build_tavi(TAVI_POS), build_nori(NORI_POS), build_piko(PIKO_START)
m_nori, m_nori_star = cast_materials()["nori"], cast_materials()["star"]
save_stage("stage2_cast")


# ================================================================ GIAI ĐOẠN 3: diễn theo mốc
# ---- LUMO
L0, LB = LUMO_START, LUMO_AT_BUTTON
bob = [(0.0, L0)] + [(0.4 * i, L0 + Vector((0, 0, 0.03 if i % 2 else 0))) for i in range(1, 9)]
keys(lumo.root, "location", bob + [(LUMO_TO_GARDEN[0], L0), (LUMO_TO_GARDEN[1], LUMO_WATCH), (WALK[0], LUMO_WATCH),
                                   (WALK[0] + 0.5, Vector((1.05, -0.70, 0.02))),
                                   (WALK[1], LB + Vector((0, 0, 0.04))), (CLICK - 0.1, LB + Vector((0, 0, 0.04))),
                                   (CLICK + 0.05, LB + Vector((-PUSH, 0, 0.02)))])
rot(lumo.root, [(0.0, (0, 0, 180)), (LUMO_TURN[0], (0, 0, 180)), (LUMO_TURN[1], (0, 0, 0)),
                (LUMO_TO_GARDEN[0], (0, 0, 0)), (LUMO_TO_GARDEN[0] + 0.5, (0, 0, 90)), (14.5, (0, 0, 105)), (LOOK_BUTTON, (0, 0, 105)), (LOOK_BUTTON + 0.5, (0, 0, 140)),
                (WALK[0], (0, 0, 140)), (WALK[0] + 0.5, (0, 0, 200)), (WALK[1], (0, 0, 270)),
                (CLICK - 0.1, (0, 0, 270)), (CLICK, (8, 0, 270)), (CLICK + 0.3, (4, 0, 270))])
rot(lumo.head, [(0.0, (-20, 0, 0)), (CLOUD_POOF - 0.1, (-20, 0, 0)), (CLOUD_POOF + 0.2, (-35, 0, 0)),
                (4.0, (-30, 0, 0)), (5.0, (-35, 0, 0)), (CLOUD_ON_HEAD, (-45, 0, 0)), (6.0, (-50, 0, 0)),
                (NOSE_DROP - 0.05, (-50, 0, 0)), (NOSE_DROP + 0.1, (-15, 0, 0)), (SHOUT_WATER[0], (-25, 0, 0)),
                (SHOUT_WATER[1], (-20, 0, 0)), (9.0, (-5, 0, 0)), (9.8, (0, 0, 0)), (14.5, (0, 0, 10)),
                (EARS_DROOP, (5, 12, 10)), (LOOK_BUTTON - 0.1, (5, 12, 10)), (LOOK_BUTTON + 0.5, (12, 0, 42)),
                (WALK[0], (12, 0, 42)), (WALK[1], (8, 0, 0)), (CLICK - 0.1, (8, 0, 0)), (CLICK + 0.1, (-5, 0, 0)),
                (CLICK + 0.5, (0, 0, 0)), (MACHINE_GO, (0, 0, 0)), (CLOUD_SWELL, (-45, 0, 0))])
for ear, side in lumo.ears:
    e = lambda a: (0, side * a, 0)                       # noqa: E731 — nghiêng tai ra ngoài a độ
    rot(ear, [(0.0, e(20)), (NOSE_DROP, e(20)), (NOSE_DROP + 0.08, e(0)), (SHOUT_WATER[1], e(15)),
              (EARS_DROOP, e(65)), (LOOK_BUTTON - 0.1, e(65)), (LOOK_BUTTON + 0.5, e(30)), (PAW_STOPS, e(30)),
              (PAW_STOPS + 0.2, e(70)), (CLOUD_SWELL, e(75))])
# tay trái (phía máy quay) với nút
rot(lumo.arm_l, [(0.0, (-8, 0, 0)), (SHOUT_WATER[0] - 0.2, (-8, 0, 0)), (SHOUT_WATER[0], (-140, 20, 0)),
                 (SHOUT_WATER[1], (-140, 20, 0)), (8.8, (-8, 0, 0)), (WALK[1], (-8, 0, 0)),
                 (WHISPER[0] + 0.2, (-55, 0, 0)), (PAW_STOPS, (-80, 0, 0)), (CLICK - 0.15, (-72, 0, 0)),
                 (CLICK, (-86, 0, 0))])
rot(lumo.arm_r, [(0.0, (-8, 0, 0)), (SHOUT_WATER[0] - 0.2, (-8, 0, 0)), (SHOUT_WATER[0], (-140, -20, 0)),
                 (SHOUT_WATER[1], (-140, -20, 0)), (8.8, (-8, 0, 0)), (CLICK - 0.05, (-8, 0, 0)),
                 (CLICK + 0.15, (-40, 15, 0)), (CLICK + 0.6, (-25, 10, 0))])
steps(lumo.legs, LUMO_TURN[0], LUMO_TURN[1], 4, 15)
steps(lumo.legs, LUMO_TO_GARDEN[0], LUMO_TO_GARDEN[1], 3, 20)
steps(lumo.legs, WALK[0], WALK[1], 4)
wag(lumo.tail, 0.0, 5.0, 0.8, 25, (20, 0, 0))
wag(lumo.tail, SHOUT_WATER[1], 9.0, 0.3, 35, (25, 0, 0))
wag(lumo.tail, 9.0, 15.0, 1.2, 15, (20, 0, 0))
rot(lumo.tail, [(EARS_DROOP, (-15, 0, 0)), (CLICK - 0.05, (-15, 0, 0)), (CLICK + 0.1, (55, 0, 0))])

# ---- TAVI
keys(tavi.root, "location", [(0.0, TAVI_POS), (CLICK + 0.1, TAVI_POS), (CLICK + 0.45, TAVI_STEP)])
rot(tavi.root, [(0.0, (0, 0, 90)), (CLOUD_POOF + 0.2, (0, 0, 90)), (4.4, (0, 0, 46)), (9.0, (0, 0, 46)),
                (9.6, (0, 0, 90)), (CLICK + 0.1, (0, 0, 90)), (CLICK + 0.45, (0, 0, 117))])
rot(tavi.head, [(0.0, (-10, 0, 0)), (CLOUD_POOF + 0.2, (-35, 0, 0)), (4.4, (-25, 0, 0)), (9.0, (0, 0, 0)),
                (TAVI_GAUGE + 0.2, (-20, 0, 0)), (TAVI_GAUGE + 0.6, (-5, 0, 0)), (TAVI_GAUGE + 0.9, (-18, 0, 0)),
                (TAVI_GAUGE + 1.2, (-5, 0, 0)), (CLICK + 0.45, (0, 0, 0)), (MACHINE_GO, (0, 0, 0)),
                (CLOUD_SWELL, (-40, 0, 0))])
rot(tavi.arm_r, [(0.0, (-10, 0, 0)), (KNOB_TURN - 0.4, (-90, 0, 0)), (KNOB_TURN, (-90, 0, -40)),
                 (KNOB_TURN + 0.3, (-10, 0, 0)), (TAVI_SHOUT[0] - 0.3, (-10, 0, 0)), (TAVI_SHOUT[0], (-160, -15, 0)),
                 (MACHINE_GO, (-160, -15, 0)), (CLOUD_SWELL, (-120, -10, 0))])
rot(tavi.arm_l, [(0.0, (-10, 0, 0)), (TAVI_SHOUT[0] - 0.3, (-10, 0, 0)), (TAVI_SHOUT[0], (-35, 0, 0))])
steps(tavi.legs, 3.6, 4.4, 3, 15)
steps(tavi.legs, CLICK + 0.1, CLICK + 0.45, 3, 20)
wag(tavi.tail, 0.0, SECONDS, 2.0, 8, (-12, 0, 0))

# ---- PIKO: nảy tại chỗ, vào vườn, hoá cái bát, nuốt, sang mép vườn, bật nhảy đáp lên lưng Lumo
pk, sq = [], []
for i in range(5):
    t = 0.6 * i
    pk += [(t, PIKO_START), (t + 0.3, PIKO_START + Vector((0, 0, 0.18)))]
    sq += [(t, (1.15, 1.15, 0.85)), (t + 0.15, (0.92, 0.92, 1.12)), (t + 0.3, (1, 1, 1))]
back = LB + Vector((-PUSH + 0.15 + 0.27, 0, 0.30))                # lưng Lumo (quay -X) sau cú đẩy
pk += [(3.0, PIKO_START), (PIKO_HOP[0], PIKO_START),
       ((PIKO_HOP[0] + PIKO_HOP[1]) / 2, (PIKO_START + PIKO_GARDEN) / 2 + Vector((0, 0, 0.35))),
       (PIKO_HOP[1], PIKO_GARDEN), (PIKO_TO_EDGE[0], PIKO_GARDEN),
       (sum(PIKO_TO_EDGE) / 2, (PIKO_GARDEN + PIKO_WAIT) / 2 + Vector((0, 0, 0.25))), (PIKO_TO_EDGE[1], PIKO_WAIT),
       (GLINT, PIKO_WAIT), (GLINT + 0.35, (PIKO_WAIT + back) / 2 + Vector((0, 0, 0.55))),
       (CLICK, back), (CLICK + 0.25, back + Vector((0.02, 0, -0.02)))]
sq += [(3.0, (1, 1, 1)), (PIKO_HOP[0], (1, 1, 1)), (PIKO_HOP[0] + 0.1, (0.9, 0.9, 1.15)),
       (PIKO_HOP[1], (1.15, 1.15, 0.85)), (PIKO_HOP[1] + 0.2, (1, 1, 1)), (PIKO_BOWL - 0.2, (1, 1, 1)),
       (PIKO_BOWL + 0.1, (1.45, 1.45, 0.42)), (PIKO_GULP - 0.1, (1.45, 1.45, 0.42)), (PIKO_GULP, (0.85, 0.85, 1.3)),
       (PIKO_GULP + 0.2, (1.08, 1.08, 0.92)), (PIKO_GULP + 0.4, (1, 1, 1)), (PIKO_TO_EDGE[0], (1, 1, 1)),
       (PIKO_TO_EDGE[0] + 0.1, (0.9, 0.9, 1.15)), (PIKO_TO_EDGE[1], (1.15, 1.15, 0.85)),
       (PIKO_TO_EDGE[1] + 0.2, (1, 1, 1)), (GLINT - 0.2, (1, 1, 1)), (GLINT, (1.2, 1.2, 0.75)),
       (GLINT + 0.1, (0.85, 0.85, 1.25)), (GLINT + 0.35, (1, 1, 1)),
       (CLICK, (1.2, 0.8, 0.95)), (CLICK + 0.3, (1.05, 0.95, 1.0))]   # dẹt theo trục mặt (y cục bộ) khi đập vào lưng
keys(piko.root, "location", pk)
keys(piko.squash, "scale", sq)
rot(piko.root, [(0.0, (0, 0, 180)), (CLOUD_POOF, (0, 0, 180)), (4.4, (0, 0, 20)), (PIKO_HOP[0], (0, 0, 20)),
                (PIKO_HOP[1], (0, 0, 50)), (PIKO_TO_EDGE[0], (0, 0, 50)), (PIKO_TO_EDGE[1], (0, 0, -90)),
                (CLICK, (0, 0, -90)), (MACHINE_GO, (0, 0, -90)), (CLOUD_SWELL, (-20, 0, -90))])


# ---- NORI: lơ lửng nhấp nhô, quay theo mây, xoay một vòng khi mưa, bay ra trước nhóm lúc máy nổi điên
def nori_yaw(t):
    if t < CLOUD_POOF:
        return -90
    if t < 4.4:
        return -90 + 30 * ss((t - CLOUD_POOF) / 1.4)
    if t < RAIN_CLOUD[0]:
        return -60
    if t < NORI_TWIRL[0]:
        return -60 + 100 * ss((t - RAIN_CLOUD[0]) / (NORI_TWIRL[0] - RAIN_CLOUD[0]))
    if t < MACHINE_GO:
        return 40 + 360 * ss((t - NORI_TWIRL[0]) / (NORI_TWIRL[1] - NORI_TWIRL[0]))
    return 400 - 43 * ss((t - MACHINE_GO) / 1.0)                  # 357 = nhìn về máy quay S7


t = 0.0
while t <= SECONDS + 1e-6:
    base = NORI_POS.lerp(NORI_END, ss((t - MACHINE_GO) / 1.0)) if t > MACHINE_GO else NORI_POS
    key(nori.root, "location", t, base + Vector((0, 0, 0.05 * math.sin(2 * math.pi * t / 1.6))))
    rot(nori.root, [(t, (-30 * ss((t - CLOUD_SWELL) / 0.5), 0, nori_yaw(t)))])
    t += 0.2
for w, sx, sz in nori.wings:
    wag(w, 0.0, SECONDS, 0.5, 18, (0, 0, sx * (25 if sz > 0 else -15)))
keys(bsdf_in(m_nori, "Emission Strength"), "default_value",
     [(0.0, 0.3), (NORI_TWIRL[0], 0.3), (sum(NORI_TWIRL) / 2, 0.9), (NORI_TWIRL[1] + 1.0, 0.4)])
keys(bsdf_in(m_nori_star, "Emission Strength"), "default_value",
     [(0.0, 0.8), (CLOUD_SWELL, 0.8)] + [(CLOUD_SWELL + 0.2 * (i + 1), 0.0 if i % 2 == 0 else 3.0) for i in range(10)])

# ---- MÁY: núm, vòm kính, đồng hồ, nút đỏ, rung
rot(knob, [(0.0, (0, 0, 0)), (KNOB_TURN - 0.05, (0, 0, 0)), (KNOB_TURN + 0.15, (-70, 0, 0))])
rot(needle, [(0.0, (50, 0, 0)), (KNOB_TURN + 0.2, (50, 0, 0)), (KNOB_TURN + 1.0, (20, 0, 0)), (CLICK, (20, 0, 0)),
             (CLICK + 0.4, (-60, 0, 0))] + [(MACHINE_GO + 0.15 * i, (-70 + (8 if i % 2 else -8), 0, 0))
                                             for i in range(17)])
keys(bsdf_in(m_dome, "Emission Strength"), "default_value",
     [(0.0, 0.0), (KNOB_TURN, 0.0), (KNOB_TURN + 0.25, 1.5), (MACHINE_GO, 1.5)] +
     [(MACHINE_GO + 0.25 * (i + 1), 5.0 if i % 2 == 0 else 1.5) for i in range(10)])
keys(bsdf_in(m_dome, "Emission Color"), "default_value",
     [(0.0, (0.30, 0.60, 1.0, 1)), (MACHINE_GO, (0.30, 0.60, 1.0, 1)), (MACHINE_GO + 0.15, (1.0, 0.08, 0.04, 1))])
keys(bsdf_in(m_button, "Emission Strength"), "default_value",
     [(0.0, 0.0), (GLINT - 0.1, 0.0), (GLINT + 0.05, 8.0), (GLINT + 0.3, 0.5), (CLICK + 0.1, 0.5)] +
     [(CLICK + 0.25 * (i + 1), 6.0 if i % 2 == 0 else 0.3) for i in range(int((SECONDS - CLICK) / 0.25))])
keys(button, "location", [(0.0, BUTTON), (CLICK - 0.05, BUTTON), (CLICK + 0.05, BUTTON + Vector((-0.025, 0, 0)))])
shake = [(MACHINE_GO - 0.05, Vector((0, 0, 0)))]
t = MACHINE_GO
while t < SECONDS:
    t += 2 / FPS
    shake.append((t, Vector((random.uniform(-0.015, 0.015), 0, random.uniform(0, 0.02)))))
keys(machine, "location", shake)

# ---- MÂY
over_head = LUMO_START + Vector((0, 0, 1.05))
keys(cloud_small, "location", [(CLOUD_POOF, NOZZLE_TOP), (CLOUD_POOF + 0.3, Vector((0.05, -0.2, 2.05))),
                               (4.2, Vector((0.25, -0.85, 1.8))), (5.0, over_head + Vector((0, 0.05, 0.25))),
                               (CLOUD_ON_HEAD, over_head), (CLOUD_GONE[0], over_head),
                               (CLOUD_GONE[1], over_head + Vector((0, 0, 0.2)))])
keys(cloud_small, "scale", [(0.0, (0, 0, 0)), (CLOUD_POOF - 0.05, (0, 0, 0)), (CLOUD_POOF, (0.3, 0.3, 0.3)),
                            (CLOUD_POOF + 0.3, (1, 1, 1)), (NOSE_DROP - 0.1, (1, 1, 1)), (NOSE_DROP, (1.1, 1.1, 0.9)),
                            (NOSE_DROP + 0.15, (1, 1, 1)), (CLOUD_GONE[0], (1, 1, 1)), (CLOUD_GONE[1], (0, 0, 0))])
rain_pos = Vector(((GARDEN_X[0] + GARDEN_X[1]) / 2, 0.1, 1.95))
keys(cloud_rain, "location", [(RAIN_CLOUD[0], NOZZLE_TOP + Vector((0, 0, 0.1))),
                              (RAIN_CLOUD[0] + 0.6, Vector((1.5, 0.0, 1.95))), (RAIN_CLOUD[1], rain_pos),
                              (MACHINE_GO, rain_pos + Vector((0.1, 0.05, 0))), (CLOUD_SWELL, Vector((0.6, -0.4, 2.3))),
                              (CLOUD_SWELL + 1.0, Vector((0.5, -0.4, 2.55)))])
keys(cloud_rain, "scale", [(0.0, (0, 0, 0)), (RAIN_CLOUD[0] - 0.05, (0, 0, 0)), (RAIN_CLOUD[0], (0.2, 0.2, 0.2)),
                           (RAIN_CLOUD[0] + 0.6, (0.7, 0.7, 0.7)), (RAIN_CLOUD[1], (1, 1, 1)), (MACHINE_GO, (1, 1, 1)),
                           (CLOUD_SWELL, (1.6, 1.6, 1.4)), (CLOUD_SWELL + 1.0, (2.0, 2.0, 1.7))])
keys(bsdf_in(m_cloud, "Base Color"), "default_value",
     [(0.0, (0.92, 0.93, 0.95, 1)), (MACHINE_GO + 0.3, (0.92, 0.93, 0.95, 1)), (CLOUD_SWELL + 1.0, (0.10, 0.10, 0.12, 1))])
save_stage("stage3_action")

# ================================================================ GIAI ĐOẠN 4: 7 máy quay, cắt bằng marker
# (giây, vị trí máy, điểm nhìn, tiêu cự mm); máy đặt thấp ngang tầm mắt nhân vật
CAMS = {
    "S1": [(0.0, (-0.40, -4.80, 0.85), (0.70, -0.30, 0.85), 24),                 # toàn, sau lưng nhóm, đẩy vào chậm
           (CLOUD_POOF, (-0.35, -4.40, 0.85), (0.60, -0.30, 1.00), 24),
           (5.0, (-0.30, -4.10, 0.90), (0.45, -0.80, 1.20), 24)],                # ngẩng theo mây bé
    "S2": [(5.0, (0.45, -3.20, 0.85), (0.35, -1.40, 0.92), 40),                  # cận trung Lumo chính diện
           (9.0, (0.43, -2.90, 0.85), (0.35, -1.40, 0.92), 40)],
    "S3": [(9.0, (4.60, -2.70, 1.40), (1.90, -0.20, 0.90), 24),                  # toàn nhìn ngang vườn, lia chậm
           (14.5, (4.30, -2.85, 1.40), (2.00, -0.35, 0.90), 24)],
    "S4": [(14.5, (1.30, -3.70, 0.90), (1.40, -0.80, 0.60), 28),                 # Lumo bên trái, dải khô bên phải
           (LOOK_BUTTON + 0.3, (1.30, -3.70, 0.90), (1.40, -0.80, 0.60), 28),
           (18.5, (1.55, -1.35, 0.70), (0.555, -0.15, 0.50), 40)],               # lia, đẩy theo ánh mắt tới nút đỏ
    "S5": [(18.5, (0.80, -2.60, 0.65), (0.50, -0.10, 0.55), 24),                 # trung rộng chính diện, máy đứng yên
           (23.0, (0.80, -2.60, 0.65), (0.50, -0.10, 0.55), 24)],
    "S6": [(23.0, (1.05, -0.85, 0.62), (0.56, -0.15, 0.50), 45),                 # đặc tả nút
           (24.5, (1.03, -0.83, 0.61), (0.56, -0.15, 0.50), 45)],
    "S7": [(24.5, (0.50, -2.80, 0.22), (0.35, -0.30, 1.35), 20),                 # toàn góc thấp, ngước lên
           (27.0, (0.50, -2.80, 0.22), (0.35, -0.30, 1.45), 20)],
}
cams = cameras(SHOTS, CAMS)

r = scene.render
r.engine = "BLENDER_EEVEE"
r.resolution_x, r.resolution_y = 1920, 1080
scene.eevee.taa_render_samples = 32
scene.view_settings.view_transform = "Standard"          # giữ màu khối nhân vật rực, dễ phân biệt
scene["stills"] = ",".join(str(fr(t)) for t in (0.5, 3.3, 4.8, 6.2, 7.7, 10.2, 11.6, 13.6, 15.6, 17.2, 18.4, 19.6,
                                                20.6, 21.7, 22.6, 23.6, 25.5, 26.9))

# ---------------------------------------------------------------- kiểm tra: ai phải thấy trong từng shot
HEAD = Vector((0, 0, 0.2))
ALL4 = [(lumo.head, HEAD), (tavi.head, HEAD), (piko.root, Vector((0, 0, 0.4))), (nori.root, Vector())]
MUST_SEE = {
    "S1": ALL4 + [(dome, Vector((0, 0, 1.2)))],
    "S2": [(lumo.head, HEAD)],
    "S3": [(tavi.head, HEAD), (piko.root, Vector((0, 0, 0.3))), (nori.root, Vector()), (machine, Vector((0, 0, 1.2)))],
    "S4": [(lumo.head, HEAD)],
    "S5": [(lumo.head, HEAD), (tavi.head, HEAD), (piko.root, Vector((0, 0, 0.4))), (button, Vector())],
    "S6": [(button, Vector())],
    "S7": ALL4 + [(dome, Vector((0, 0, 1.2)))],
}
EXTRA = [("S2", cloud_small, 5.6, 8.4), ("S3", cloud_rain, 10.3, 14.5), ("S4", button, 17.9, 18.5)]
problems = {}
for name, t0, t1 in SHOTS:
    cam = cams[name]
    for f in range(fr(t0), fr(t1)):
        scene.frame_set(f)
        t = (f - 1) / FPS
        checks = list(MUST_SEE[name])
        if name == "S4" and t > LOOK_BUTTON + 0.3:      # đang lia từ Lumo sang nút: chỉ kiểm nút ở cuối (EXTRA)
            checks = []
        checks += [(ob, Vector()) for s, ob, a, b in EXTRA if s == name and a <= t < b]
        for ob, local in checks:
            p = world_to_camera_view(scene, cam, ob.matrix_world @ local)
            if not (0.03 < p.x < 0.97 and 0.03 < p.y < 0.97 and p.z > 0.1):
                problems.setdefault(f"{name}: {ob.name} ra khỏi khung", []).append(f)
        if cam.matrix_world.translation.z < 0.1:
            problems.setdefault(f"{name}: máy dưới đất", []).append(f)
for label, fs in problems.items():
    print("PREVIZ_CHECK", label, f"{len(fs)} khung, từ {fs[0]} đến {fs[-1]}")
if not problems:
    print("PREVIZ_CHECK OK")

scene.frame_set(1)
save_stage("stage4_cameras")
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_BLEND), compress=True)
print("PREVIZ_SAVED", OUT_BLEND, FRAMES, "frames,", len(SHOTS), "shots")
