"""
Tạo âm thanh cho shot 02 bằng tổng hợp (không dùng file ngoài -> không vướng bản quyền).
Chạy bằng Python đi kèm Blender (có numpy):
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\5.2\\python\\bin\\python.exe" build_audio.py
Ra: audio/shot02_mix.wav (bản trộn) + audio/stem_*.wav (từng nhóm, để chỉnh mức trong Blender nếu muốn).
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "pipeline", "sound"))
sys.path.insert(0, HERE)
import sfx  # noqa: E402
from sfx import SR, Track, curve  # noqa: E402
from timing import (BOP, FLASHES, FRAMES, PIKO_HOPS, PIKO_INFLATE, PIKO_SHAKE, PRESS, RAIN_HEAVY,  # noqa: E402
                    RAIN_LIGHT, STEAM_PERIOD_L1, STORM0, STORM1)

OUT = os.path.join(HERE, "audio")
os.makedirs(OUT, exist_ok=True)
rnd = np.random.default_rng(42)
stems = {k: Track(FRAMES) for k in ("amb", "machine", "piko", "fx")}
N = stems["amb"].n


def lvl(points):
    return curve(points, N)


# ---------------------------------------------------------------- nền: gió, ve sầu, mưa
amb = stems["amb"]
amb.bed(sfx.wind(N), lvl([(1, 0.10), (STORM0, 0.12), (STORM1, 0.34), (FRAMES, 0.3)]))
# ve sầu kêu trong nắng... và im bặt ngay khi máy kêu BEEP (nhịp hài)
amb.bed(sfx.cicadas(N), lvl([(1, 0.09), (PRESS, 0.09), (PRESS + 5, 0.0)]), pan=0.2)
density = lvl([(1, 0), (RAIN_LIGHT, 0), (RAIN_LIGHT + 20, 0.25), (RAIN_HEAVY, 0.55), (RAIN_HEAVY + 40, 1.0),
               (FRAMES, 1.0)])
amb.bed(sfx.rain(N, density), density * 0.5)
# mây tí hon nhỏ giọt tưới hoa (Level 1)
for f in np.sort(rnd.uniform(1, PRESS + 30, 55)):
    amb.add(sfx.plink(rnd.uniform(2200, 3200)), f, 0.045, pan=-0.25)

# ---------------------------------------------------------------- máy Rain-O-Matic
mac = stems["machine"]
mac.bed(sfx.machine_hum(N), lvl([(1, 0.2), (PRESS, 0.2), (PRESS + 8, 0.0)]))
mac.bed(sfx.machine_rumble(N), lvl([(1, 0), (PRESS + 2, 0), (PRESS + 14, 0.5), (STORM1, 0.38), (FRAMES, 0.3)]))
mac.bed(sfx.steam_hiss(N), lvl([(1, 0), (PRESS + 6, 0), (PRESS + 14, 0.32), (600, 0.24), (660, 0.1), (FRAMES, 0.1)]))
for f0 in range(-40, PRESS, STEAM_PERIOD_L1):       # mỗi làn hơi Level 1 một tiếng "phù"
    if f0 >= 1:
        mac.add(sfx.puff(), f0, 0.1)
for k in range(30):                                  # nút đỏ nhấp nháy "bíp" theo nhịp sáng
    f = round(3.74 + 14.96 * k)
    if 97 <= f < PRESS - 2:
        mac.add(sfx.beep(2100, 0.04), f, 0.07, pan=0.15)
mac.add(sfx.click(), PRESS - 1, 0.5, pan=0.15)
mac.add(sfx.beep(1046, 0.12, 0.3), PRESS + 1, 0.55)
mac.add(sfx.beep(1568, 0.24, 0.3), PRESS + 4, 0.55)
mac.add(sfx.powerup(1.4), PRESS + 2, 0.4)
mac.add(sfx.siren(1.6), PRESS + 3, 0.28)

# ---------------------------------------------------------------- Piko
pk = stems["piko"]
for i, (up, down) in enumerate(PIKO_HOPS):
    big = down == 292
    pk.add(sfx.boing(240 + 25 * (i % 3), 0.45), up, 0.32, pan=0.1)
    pk.add(sfx.squish(0.45, 1.3) if big else sfx.bloop(), down, 0.5 if big else 0.32, pan=0.1)
pk.add(sfx.stretch(1.6), 110, 0.18, pan=0.1)                  # rướn người về phía nút
pk.add(sfx.wobble(0.9), PIKO_SHAKE[0], 0.3, pan=0.1)          # lắc đầu "không được"
pk.add(sfx.stretch(0.35, 320, 220), 298, 0.25)                # thân thạch bị ép vào nút
pk.add(sfx.inflate(), PIKO_INFLATE, 0.45, pan=0.2)            # phồng người vì sốc
for f in range(614, BOP - 2, 6):                              # há miệng hứng mưa: lộp độp
    pk.add(sfx.plink(rnd.uniform(1700, 2400), 0.06), f + int(rnd.integers(0, 3)), 0.09)

# ---------------------------------------------------------------- hiệu ứng: sinh vật, sấm, hoa, BOP
fx = stems["fx"]
for f, pan in ((318, -0.5), (322, 0.5), (330, -0.3), (336, 0.45)):   # 4 sinh vật lắc đầu "No"
    fx.add(sfx.squeak(rnd.uniform(1300, 1700), rnd.uniform(900, 1100)), f, 0.12, pan=pan)
for k, f in enumerate(FLASHES):
    fx.add(sfx.thunder(4.0, seed=k + 1), f, 0.75 + 0.1 * k, pan=(-0.3, 0.35)[k])
for f in np.sort(rnd.uniform(548, 625, 9)):                          # hoa ngẩng đầu: lấp lánh
    fx.add(sfx.bell(float(rnd.choice([1568, 1760, 2093, 2349, 2637]))), f, 0.05, pan=float(rnd.uniform(-0.6, 0.6)))
fx.add(sfx.big_drop(), BOP, 0.7)
fx.add(sfx.squish(0.5, 1.5), BOP + 1, 0.5)
fx.add(sfx.deflate(0.9), BOP + 4, 0.32)
fx.add(sfx.sad_trombone(), BOP + 12, 0.3)

# ---------------------------------------------------------------- xuất
length = int(FRAMES / 24 * SR)
for name, tr in stems.items():
    sfx.write_wav(os.path.join(OUT, f"stem_{name}.wav"), np.clip(tr.buf[:length], -1, 1))
mix = sum(tr.buf for tr in stems.values())[:length]
sfx.write_wav(os.path.join(OUT, "shot02_mix.wav"), sfx.master(mix))
peak = {k: round(float(np.abs(v.buf).max()), 2) for k, v in stems.items()}
print("AUDIO", os.path.join(OUT, "shot02_mix.wav"), f"{length / SR:.2f}s", "stem peaks:", peak)
