"""
Tiếng bước chân lạch bạch cho video vòng đi bộ (khớp frame chân chạm đất trong walk_cycle.py).
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\5.2\\python\\bin\\python.exe" walk_audio.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "pipeline", "sound"))
import sfx  # noqa: E402

FRAMES, CYCLE, STEP = 264, 18, 9
rnd = np.random.default_rng(3)


def pat():
    """Bước chân mềm của sinh vật nhỏ: tiếng 'pụp' trầm + chút tiếng sột soạt."""
    d = 0.12
    thump = sfx.osc(sfx.glide(rnd.uniform(200, 240), 110, d)) * sfx.env(d, 0.002, 0.03)
    brush = sfx.band(sfx.white(int(d * sfx.SR)), 500, 2500) * sfx.env(d, 0.001, 0.015)
    return sfx.norm(thump + 0.35 * sfx.norm(brush))


tr = sfx.Track(FRAMES)
for f in range(1, FRAMES + 1):
    t = (f - 1) % CYCLE
    if t == 0:
        tr.add(pat(), f, 0.5, pan=0.15)        # chân trái chạm đất
    elif t == STEP:
        tr.add(pat(), f, 0.5, pan=-0.15)       # chân phải
    if (f - 1) % STEP == 4:
        tr.add(sfx.boing(rnd.uniform(520, 600), 0.18, wobble=20), f, 0.05)   # đuôi/tai nảy nhẹ
length = int(FRAMES / 24 * sfx.SR)
out = os.path.join(HERE, "renders", "walk_steps.wav")
sfx.write_wav(out, sfx.master(tr.buf[:length], -3.0, 0.3))
print("AUDIO", out)
