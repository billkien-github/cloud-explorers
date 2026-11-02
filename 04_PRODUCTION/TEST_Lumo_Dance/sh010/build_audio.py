"""
Nhạc nền tự sáng tác cho clip nhảy: 120 BPM, trống + bass + giai điệu "đô đô" theo timing.py.
    "C:\\Program Files\\Blender Foundation\\Blender 5.2\\5.2\\python\\bin\\python.exe" build_audio.py
Ra audio/sh010_mix.wav; ghép vào video bằng .\\pipeline\\run.ps1 audio -Shot 04_PRODUCTION\\TEST_Lumo_Dance\\sh010
"""
import math
import pathlib
import sys
import wave

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from timing import BPM, BEATS, MELODY, SECTIONS, SHOUTS  # noqa: E402

SR = 48000
SPB = 60 / BPM                                  # giây mỗi nhịp
N = int((BEATS * SPB + 1.0) * SR)
rng = np.random.default_rng(12)
L, R = np.zeros(N), np.zeros(N)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def add(sig, beat, gain=1.0, pan=0.0):
    i = int(beat * SPB * SR)
    sig = sig[: max(0, N - i)]
    L[i:i + len(sig)] += sig * gain * math.sqrt((1 - pan) / 2)
    R[i:i + len(sig)] += sig * gain * math.sqrt((1 + pan) / 2)


def kick():
    t = tt(0.35)
    f = 45 + 95 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)


def noise(dur):
    return rng.uniform(-1, 1, int(dur * SR))


def hipass(x, k=2):
    for _ in range(k):
        x = np.diff(x, prepend=0.0)
    return x


def clap():
    t = tt(0.25)
    env = sum(np.exp(-np.maximum(t - d, 0) * 40) * (t >= d) for d in (0, 0.012, 0.024))
    return hipass(noise(0.25), 1) * env * 0.6


def hat(open_=False):
    t = tt(0.18)
    return hipass(noise(0.18), 2) * np.exp(-t * (18 if open_ else 70)) * 0.35


def tone(midi, dur, harmonics=7, vib=0.0):
    t = tt(dur)
    ph = 2 * np.pi * hz(midi) * (t + vib * np.sin(2 * np.pi * 5.5 * t) / (2 * np.pi * 5.5))
    sig = sum(np.sin(k * ph) / k for k in range(1, harmonics + 1, 2))      # sóng vuông mềm
    a = np.minimum(1, t / 0.01)
    rel = np.clip((dur - t) / 0.04, 0, 1)
    return sig * a * rel * np.exp(-t * 1.5)


def bass(midi, dur):
    t = tt(dur)
    ph = 2 * np.pi * hz(midi) * t
    return (np.sin(ph) + 0.12 * np.sin(3 * ph)) * np.minimum(1, t / 0.005) * np.exp(-t * 4)


def whoosh(dur):
    t = tt(dur)
    x = noise(dur)
    x = np.convolve(x, np.ones(12) / 12, mode="same")          # bớt chói
    return x * np.sin(np.pi * t / dur) ** 2 * 0.8


# trống: kick mỗi nhịp; clap nhịp 2, 4 và hi-hat móc từ đoạn "baby"
for b in range(BEATS):
    add(kick(), b, 0.9)
    if b >= SECTIONS["baby"][0]:
        if b % 2 == 1:
            add(clap(), b, 0.7)
        add(hat(), b, 0.5, pan=0.3)
        add(hat(open_=True), b + 0.5, 0.45, pan=0.3)
    else:
        add(hat(), b + 0.5, 0.4, pan=0.3)

# bass: Đô - La thứ - Fa - Son, mỗi hợp âm một ô nhịp, móc đơn đảo quãng tám
ROOTS = [36, 33, 29, 31]
for b2 in range(SECTIONS["baby"][0] * 2, SECTIONS["finale"][0] * 2):
    root = ROOTS[(b2 // 8) % 4]
    add(bass(root + (12 if b2 % 2 else 0), SPB / 2), b2 / 2, 0.55)

# giai điệu
for beat, dur, midi in MELODY:
    add(tone(midi, dur * SPB * 0.95, vib=0.004), beat, 0.22 if midi >= 72 else 0.26, pan=-0.15)

# điểm nhấn: "hây!" (nốt vút lên), xoay (gió), "ta-da" (hợp âm rải + lốc xoáy)
(hey_beat, _), (tada_beat, _) = SHOUTS
t = tt(0.3)
add(np.sin(2 * np.pi * np.cumsum(500 + 900 * t / 0.3) / SR) * np.exp(-t * 6), hey_beat, 0.25)
add(whoosh(2 * SPB), 28, 0.35)
for k, n in enumerate((60, 64, 67, 72)):
    add(tone(n, 1.5 - 0.1 * k, harmonics=5), tada_beat + 0.12 * k, 0.2)
t = tt(2.0)
add(hipass(noise(2.0), 1) * np.exp(-t * 2.5) * 0.35, tada_beat, 0.6)

mix = np.stack([L, R], axis=1)
mix = np.tanh(1.3 * mix / np.abs(mix).max()) / math.tanh(1.3) * 0.89
out = HERE / "audio" / "sh010_mix.wav"
out.parent.mkdir(exist_ok=True)
with wave.open(str(out), "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("AUDIO", out, round(N / SR, 2), "s")
