"""
EP000A post-credit (5 giây, gài EP000B): previz 2D cutout (03_CONTENT/PREVIZ_2D.md, bộ cutout pipeline/cutout.py).
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #6#. Mốc thời gian và CC: timing.py.
    pipeline/run.sh build -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene06
    pipeline/run.sh preview -Shot 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene06
    blender -b --factory-startup -P pipeline/cc.py -- <cảnh>/renders/scene06_preview.mp4 <cảnh>/timing.py <cảnh>/renders/scene06_preview_cc.mp4
Bố cục (junkyard_hero.png; X, mét; Z = 0 là chân hộp): hộp kim loại phủ bụi ở giữa, nắp hé thấy quai đeo; hai đống phế
liệu hai bên (bánh xe, bánh răng, ống, lò xo, thùng gỗ); sau bãi là biển mây, hòn đảo có đài thiên văn ở chân trời phía
trên bên phải hộp. Hòn đảo, đài thiên văn (dáng Hub_House ở previz 2D Cảnh 2 tập 01) và nhịp lóe dùng chung với Cảnh 5
(build_hub_island(), glow_flash() của cutout) để lần lóe này trùng nhịp lần lóe cuối của Cảnh 5.
"""
import math
import pathlib
import random
import sys

import bpy

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.dont_write_bytecode = True                                  # không để __pycache__ cạnh timing.py
sys.path[:0] = [str(HERE), str(ROOT / "pipeline")]
from cutout import *  # noqa: E402,F403  bộ cutout: keyframe, hình, máy quay
from timing import *  # noqa: E402,F403  FPS, SECONDS, SHOTS, mốc hành động, CC của cảnh

OUT_BLEND = HERE / f"{HERE.name}.blend"
start(FPS)
HOLD = 1.0 / FPS
random.seed(6)


GOLD = "#E8B33A"
RUST, RUST_D, RUST_L, BRASS, WOOD = "#A86A4A", "#8E5A3E", "#C07A55", "#C99A5A", "#B88B5A"
HORIZON = 0.82

# ================================================================ trời, mặt trời, biển mây
part("Sky", None, [(rect(-6, 2.2, 6, 8), "#A79BDB"), (rect(-6, 1.55, 6, 2.2), "#C7A3D6"), (rect(-6, 1.15, 6, 1.55), "#E8AAC6"),
                   (rect(-6, 0.95, 6, 1.15), "#F7BCA6"), (rect(-6, -3, 6, 0.95), "#FBD0A0")], 6.0)
part("Sun", None, [(ell(0.26, 0.26, -0.7, 0.95), "#FDDDA0"), (ell(0.17, 0.17, -0.7, 0.95), "#FEE9B8"),
                   (ell(0.11, 0.11, -0.7, 0.95), "#FFF6DA")], 5.9)
part("HighClouds", None, [(ell(rx, rz, cx, cz), col) for rx, rz, cx, cz, col in (
    (0.6, 0.05, -0.9, 1.75, "#F4B5BE"), (0.45, 0.04, 0.4, 1.95, "#F8C7B8"), (0.7, 0.05, 1.2, 1.6, "#F4B5BE"),
    (0.5, 0.18, 1.75, 1.05, "#F9DDE5"), (0.35, 0.14, 1.55, 1.12, "#FBE4E3"))], 5.8)


# ================================================================ hòn đảo và đài thiên văn: như Cảnh 5 (cùng dáng, cùng nhịp lóe)
island = node("Island", None, (0.45, HORIZON), 5.5)             # gốc ở chân đảo trên chân trời, thu nhỏ vì xa hơn ở Cảnh 5
island.scale = (0.45, 1.0, 0.45)
hub = build_hub_island(island, "Island_Shape")
part("IslandMist", island, [(ell(0.32, 0.045, -0.45, 0.07), "#FBE6EE"), (ell(0.28, 0.04, 0.5, 0.05), "#FBE6EE")], -0.1)
sea = [(rect(-6, -3, 6, HORIZON), "#EFC9DE")]
for i in range(26):
    x = -6 + 0.48 * i
    sea += [(ell(0.42, 0.09, x, HORIZON + 0.02 * (i % 3)), "#F4D3E3"), (ell(0.24, 0.05, x + 0.1, HORIZON + 0.05), "#FBE2E2"),
            (ell(0.45, 0.1, x + 0.2, HORIZON - 0.3), "#EAC1DA")]
part("CloudSea", None, sea, 5.2)
part("FarJunk", None, [([(-2.2, 0.3), (-2.2, 0.62), (-1.9, 0.7), (-1.6, 0.6), (-1.35, 0.66), (-1.1, 0.4), (-1.0, 0.3)], "#B98B7A"),
                       ([(1.6, 0.3), (1.75, 0.55), (2.0, 0.62), (2.3, 0.5), (2.3, 0.3)], "#B98B7A")], 3.0)

# ================================================================ nền bãi, phiến đá lát
part("Ground", None, [([(-6, -3), (6, -3), (6, 0.34), (2.0, 0.36), (0.6, 0.33), (-0.8, 0.35), (-6, 0.33)], "#9DBF5E")]
     + [(ell(rx, rz, cx, cz), "#B0CE6C") for rx, rz, cx, cz in ((0.4, 0.04, -0.3, 0.3), (0.35, 0.04, 0.9, 0.31))], 2.0)
slabs = []
for k, (cx, cz, w) in enumerate(((-1.05, -0.12, 0.42), (-0.55, -0.2, 0.38), (0.0, -0.14, 0.44), (0.55, -0.22, 0.4), (1.05, -0.1, 0.42),
                                 (-0.3, -0.32, 0.36), (0.3, -0.34, 0.4), (-1.3, 0.12, 0.3), (1.35, 0.1, 0.3))):
    slabs.append((rrect(w, 0.08, 0.025, cx, cz), "#C9B8A0" if k % 2 else "#BFAE95"))
part("Slabs", None, slabs, 1.9)


def gear(r, cx, cz, teeth=10, depth=0.2):
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        rr = r if i % 4 in (1, 2) else r * (1 - depth)
        pts.append((cx + rr * math.cos(a), cz + rr * math.sin(a)))
    return pts


def gear_shapes(r, cx, cz, col, teeth=10):
    return [(gear(r, cx, cz, teeth), col), (ell(0.45 * r, 0.45 * r, cx, cz), RUST_D), (ell(0.25 * r, 0.25 * r, cx, cz), col)]


def wheel_shapes(r, cx, cz, col):
    sp = [(band([(cx - 0.85 * r * math.cos(a), cz - 0.85 * r * math.sin(a)), (cx + 0.85 * r * math.cos(a), cz + 0.85 * r * math.sin(a))],
                0.06 * r), col) for a in (0.3, 0.3 + math.pi / 3, 0.3 + 2 * math.pi / 3)]
    return [(arc(0.92 * r, 0, 360, 0.16 * r, cx, cz, 36), col)] + sp + [(ell(0.2 * r, 0.2 * r, cx, cz), RUST_D)]


def spring_shapes(cx, cz, w, h, n, col):
    pts = [(cx + (w / 2 if i % 2 else -w / 2), cz + h * i / n) for i in range(n + 1)]
    return [(band(pts, 0.03), col)]


# --- đống phế liệu bên trái
part("JunkLeft", None, wheel_shapes(0.45, -1.3, 0.62, RUST) + spring_shapes(-1.75, 0.3, 0.2, 0.5, 8, RUST_L)
     + [(rrect(0.5, 0.36, 0.05, -1.65, 0.95), RUST_D), (ell(0.1, 0.06, -1.65, 1.15), RUST)]          # nồi hơi cũ
     + gear_shapes(0.24, -0.82, 0.42, BRASS) + [(rrect(0.42, 0.26, 0.04, -1.0, 0.2), "#B8AE9C"), (ell(0.18, 0.04, -1.0, 0.33), "#93B451")]
     + [(band(curve((-0.6, 0.26), (-0.55, 0.55), (-0.75, 0.62)), 0.08), RUST_L)], 1.2)
# --- đống phế liệu bên phải (thấp dưới hòn đảo để không che đảo)
part("JunkRight", None, wheel_shapes(0.32, 1.42, 0.52, RUST) + gear_shapes(0.26, 1.62, 0.2, BRASS, 9)
     + [(rrect(0.34, 0.3, 0.04, 1.02, 0.26), RUST_D), (ell(0.17, 0.05, 1.02, 0.41), RUST),               # khúc ống đứng
        (band(curve((0.62, 0.22), (0.66, 0.48), (0.86, 0.5)), 0.09), RUST_L),                            # ống cong
        (rrect(0.46, 0.4, 0.03, 1.95, 0.38), WOOD), (band([(1.72, 0.25), (2.18, 0.25)], 0.025), "#9A7044"),
        (band([(1.72, 0.45), (2.18, 0.45)], 0.025), "#9A7044")], 1.2)
part("Vines", None, [(band(curve((-1.9, 1.1), (-1.6, 1.3), (-1.35, 1.12)), 0.025), "#6E9E3C")]
     + [(leaf_pts(x, z, 2.2, a), "#86B24C") for x, z, a in ((-1.75, 1.2, 30), (-1.5, 1.22, -20), (-1.38, 1.14, 40))]
     + [(ell(0.025, 0.025, x, z), col) for x, z, col in ((-0.55, 0.1, "#F7A8C8"), (-0.45, 0.06, WHITE), (0.62, 0.08, "#F7A8C8"),
                                                          (0.7, 0.04, WHITE), (-1.25, -0.02, WHITE))], 1.1)

# ================================================================ hộp kim loại phủ bụi, nắp hé, quai đeo bên trong
BOX_W = 0.9
part("Box_Shadow", None, [(ell(0.56, 0.05, 0.0, 0.0), "#7E9E48")], 0.9)
part("Box_Inside", None, [(rect(-0.43, 0.4, 0.43, 0.66), "#2A2522")], 0.53)
gap_glow = part("Box_GapGlow", None, [(rect(-0.42, 0.44, 0.42, 0.64), TEAL_L)], 0.52)
gap_dim = part("Box_GapDim", None, [(rect(-0.42, 0.44, 0.42, 0.64), "#2F5E5A")], 0.522)   # sau lóe: khe nắp còn le lói xanh
part("Box_Strap", None, [(band([(-0.34, 0.47), (-0.05, 0.5), (0.34, 0.52)], 0.035), "#8A4F2A"),
                         (rrect(0.075, 0.055, 0.01, 0.05, 0.5), GOLD), (rrect(0.04, 0.025, 0.006, 0.05, 0.5), "#5A3A20")], 0.515)
pack_halo = part("Pack_Halo", None, [(ell(0.53, 0.07), TEAL)]               # vệt sáng hẹp lọt ra hai đầu khe nắp, sau hộp
                 + [(band([(sx * 0.46, dz * 0.3), (sx * 0.64, dz)], 0.022), TEAL) for sx in (-1, 1) for dz in (-0.07, 0.0, 0.08)],
                 0.56, (0.0, 0.53))
rust = [(ell(rx, rz, cx, cz), col) for rx, rz, cx, cz, col in (
    (0.09, 0.05, -0.28, 0.12, RUST), (0.06, 0.04, 0.3, 0.3, RUST_L), (0.05, 0.08, 0.36, 0.1, RUST), (0.07, 0.03, -0.1, 0.36, RUST_L),
    (0.04, 0.05, -0.36, 0.33, RUST))]
corners = [(rrect(0.11, 0.11, 0.02, x, z), BRASS) for x in (-0.41, 0.41) for z in (0.055, 0.405)]
rivets = [(ell(0.012, 0.012, x, z), "#E0BE6A") for x in (-0.41, 0.41) for z in (0.035, 0.075, 0.385, 0.425)]
part("Box_Body", None, [(rrect(BOX_W, 0.46, 0.03, 0.0, 0.23), "#8C9CA4"), (rrect(0.8, 0.36, 0.03, 0.0, 0.23), "#97A7AE")] + rust
     + corners + rivets + [(rrect(0.15, 0.12, 0.02, 0.0, 0.33), BRASS), (ell(0.015, 0.02, 0.0, 0.34), DARK),
                           (ell(0.16, 0.025, 0.12, 0.44), "#C9C4B9"), (ell(0.12, 0.02, -0.24, 0.43), "#C9C4B9"),   # bụi
                           (ell(0.08, 0.02, 0.2, 0.08), "#C9C4B9")], 0.5)
lid = node("Box_Lid", None, (-0.46, 0.475), 0.45)                 # bản lề trái, nắp hé: đầu phải nhấc cao hơn
part("Box_LidShape", lid, [(rrect(0.94, 0.13, 0.03, 0.47, 0.13), "#8C9CA4"), (ell(0.47, 0.07, 0.47, 0.19, 0, 180), "#97A7AE"),
                           (rrect(0.11, 0.12, 0.02, 0.06, 0.12), BRASS), (rrect(0.11, 0.12, 0.02, 0.88, 0.12), BRASS),
                           (arc(0.11, 0, 180, 0.035, 0.47, 0.25), BRASS), (rrect(0.05, 0.05, 0.01, 0.36, 0.25), BRASS),
                           (rrect(0.05, 0.05, 0.01, 0.58, 0.25), BRASS), (ell(0.18, 0.025, 0.3, 0.2), "#C9C4B9"),
                           (ell(0.06, 0.04, 0.7, 0.12), RUST_L)])
lid.rotation_euler = (0.0, math.radians(-3.5), 0.0)
part("FG_Gear", None, gear_shapes(0.42, -1.75, -0.45, BRASS, 12) + [(ell(0.06, 0.05, -1.2, -0.38), "#F7A8C8")], -0.5)
motes = [part(f"Mote{i}", None, [(ell(0.008, 0.008), "#FFF4DC")], 0.3) for i in range(5)]


# ================================================================ diễn: bụi bay, máy đẩy vào, lóe cùng nhịp
for ob in (hub.flash, hub.tint, gap_glow, gap_dim, pack_halo):
    show(ob, 0.0, False)
glow_flash(hub.flash, HUB_FLASH, lit=hub.tint)                  # hòn đảo lóe xanh ngọc
glow_flash(pack_halo, PACK_FLASH, lit=gap_glow)                 # cùng nhịp đó, Inventor Pack trong hộp lóe qua khe nắp
show(gap_dim, PACK_FLASH + 0.7, True)                          # le lói tới hết cảnh
for i, ob in enumerate(motes):                                  # bụi lơ lửng trong nắng chiều
    x0, z0 = -0.5 + 0.25 * i, 0.15 + 0.12 * (i % 3)
    at(ob, 0.0, x0, z0)
    at(ob, SECONDS, x0 + 0.08 * (1 if i % 2 else -1), z0 + 0.25)

CAMS = {"S1": (0.08, 0.66, 3.7)}                                # tâm X, tâm Z, bề ngang khung (m); đáy khung chừa cho CC
cameras(SHOTS, CAMS)
cam = bpy.data.objects["Cam_S1"]
for t, (cx, cz, w) in ((PUSH[0], CAMS["S1"]), (PUSH[1] - HOLD, (0.08, 0.54, 2.9))):   # máy đẩy chậm vào chiếc hộp
    key(cam, "location", t, (cx, -10.0, cz))
    key(cam.data, "ortho_scale", t, w)
finish(SECONDS, OUT_BLEND, (0.5, 2.0, 2.7, 2.9, 3.2, 4.5))
