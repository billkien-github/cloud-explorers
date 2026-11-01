"""
Tiếng hiệu ứng cho đoạn chuyển cảm xúc (expressions.py: 9 biểu cảm x 24 frame, đổi ở frame 1 + 24*i).
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\5.2\\python\\bin\\python.exe" faces_audio.py
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "pipeline", "sound"))
import sfx  # noqa: E402

HOLD, N = 24, 9
tr = sfx.Track(HOLD * N)
start = [1 + HOLD * i for i in range(N)]
# 0 Bình thường, 1 Tò mò, 2 Bất ngờ, 3 Phấn khích, 4 Bối rối, 5 Ngượng ngùng, 6 Buồn, 7 Quyết tâm, 8 Vui
tr.add(sfx.stretch(0.45, 380, 620), start[1], 0.25)                                  # "hửm?" lên giọng
tr.add(sfx.boing(520, 0.35, wobble=24), start[2], 0.35)                                # giật mình
tr.add(sfx.squeak(1200, 1900, 0.15), start[3], 0.25)
for k, f in enumerate((1568, 2093, 2637)):                                             # lấp lánh vui sướng
    tr.add(sfx.bell(f, 0.7), start[3] + 3 + 3 * k, 0.08)
tr.add(sfx.wobble(0.6, 220, 9), start[4], 0.22)                                        # ngơ ngác
tr.add(sfx.squeak(1500, 800, 0.25), start[5], 0.18)                                    # ngượng, xẹp giọng
tr.add(sfx.sad_trombone(0.12, 0.5)[: int(0.9 * sfx.SR)], start[6], 0.18)              # buồn
tr.add(sfx.puff(0.25, 300, 1500), start[7], 0.3)                                       # "hừm!" quyết tâm
tr.add(sfx.bell(2093, 0.9), start[8] + 2, 0.12)                                        # vui
for i in (0, 1, 3, 4, 6, 7):                     # chớp mắt ở start+14, nhắm hẳn ở +2 (xem expressions.py)
    tr.add(sfx.plink(2600, 0.03), start[i] + 16, 0.025)
length = int(HOLD * N / 24 * sfx.SR)
out = os.path.join(HERE, "renders", "faces_sfx.wav")
sfx.write_wav(out, sfx.master(tr.buf[:length], -4.0, 0.3))
print("AUDIO", out, np.round(length / sfx.SR, 2), "s")
