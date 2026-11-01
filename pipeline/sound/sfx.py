"""
Thư viện tổng hợp âm thanh hoạt hình bằng numpy (chạy bằng Python đi kèm Blender, đã có numpy).
Mỗi hàm trả về mảng mono float32 ở SR Hz. Track gom các tiếng vào một buffer stereo theo frame phim.
"""
import wave

import numpy as np

SR = 48000
rng = np.random.default_rng(7)


# ---------------------------------------------------------------- cơ bản
def t_of(dur):
    return np.arange(int(dur * SR)) / SR


def osc(freq, shape="sine"):
    """freq: số hoặc mảng tần số theo thời gian (Hz)."""
    phase = np.cumsum(np.broadcast_to(freq, np.shape(freq))) / SR
    if shape == "sine":
        return np.sin(2 * np.pi * phase)
    if shape == "saw":
        return 2 * (phase % 1.0) - 1
    if shape == "square":
        return np.sign(np.sin(2 * np.pi * phase))
    if shape == "tri":
        return 2 * np.abs(2 * (phase % 1.0) - 1) - 1
    raise ValueError(shape)


def glide(f0, f1, dur, curve="exp"):
    t = t_of(dur) / dur
    return f0 * (f1 / f0) ** t if curve == "exp" else f0 + (f1 - f0) * t


def white(n):
    return rng.standard_normal(n)


def pink(n):
    X = np.fft.rfft(white(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    X[1:] /= np.sqrt(f[1:])
    X[0] = 0
    y = np.fft.irfft(X, n)
    return y / (np.abs(y).max() + 1e-9)


def brown(n):
    y = np.cumsum(white(n))
    y = highpass(y, 20)
    return y / (np.abs(y).max() + 1e-9)


def band(x, lo=None, hi=None, slope=4):
    """Lọc bằng FFT (mềm, không méo pha). lo/hi theo Hz, None = bỏ qua."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR) + 1e-6
    m = np.ones_like(f)
    if lo:
        m *= 1 / (1 + (lo / f) ** slope)
    if hi:
        m *= 1 / (1 + (f / hi) ** slope)
    return np.fft.irfft(X * m, n)


def lowpass(x, hi, slope=4):
    return band(x, None, hi, slope)


def highpass(x, lo, slope=4):
    return band(x, lo, None, slope)


def onepole_sweep(x, cut):
    """Lọc thông thấp một cực với tần số cắt thay đổi theo thời gian (dùng cho tiếng ngắn)."""
    a = 1 - np.exp(-2 * np.pi * np.asarray(cut) / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def env(dur, attack=0.005, decay=None, release=0.02):
    """Bao biên: lên trong attack, giữ, tắt dần release. decay=tau -> tắt kiểu mũ."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(attack, 1e-4))
    if decay:
        e *= np.exp(-t / decay)
    rel = int(release * SR)
    if rel and n > rel:
        e[-rel:] *= np.linspace(1, 0, rel)
    return e


def norm(x, peak=1.0):
    return x * (peak / (np.abs(x).max() + 1e-9))


def curve(points, n):
    """Đường cong mức âm theo frame: points=[(frame, giá trị)] -> mảng theo sample."""
    fr, vals = zip(*points)
    ts = (np.asarray(fr, float) - 1) / 24.0
    return np.interp(np.arange(n) / SR, ts, vals)


def smooth_random(n, every=1.5, lo=0.4, hi=1.0, seed=0):
    r = np.random.default_rng(seed)
    k = int(n / SR / every) + 3
    pts = r.uniform(lo, hi, k)
    xs = np.arange(k) * every
    return np.interp(np.arange(n) / SR, xs, pts)


# ---------------------------------------------------------------- tiếng hoạt hình
def boing(f0=260, dur=0.5, wobble=14):
    t = t_of(dur)
    f = f0 * (1 + 0.45 * np.exp(-t * 7) * np.sin(2 * np.pi * wobble * t)) * (1 + 0.25 * t)
    y = osc(f) + 0.3 * osc(f * 2)
    return norm(y * env(dur, 0.004, 0.18))


def bloop(f0=190, f1=85, dur=0.22):
    y = osc(glide(f0, f1, dur)) * env(dur, 0.003, 0.08)
    thump = lowpass(white(len(y)), 400) * env(dur, 0.001, 0.03)
    return norm(y + 0.5 * norm(thump))


def squish(dur=0.4, size=1.0):
    n = int(dur * SR)
    wet = band(white(n), 250 / size, 1600 / size) * env(dur, 0.01, 0.12)
    low = osc(glide(140 / size, 60 / size, dur)) * env(dur, 0.005, 0.1)
    return norm(norm(wet) * 0.6 + low)


def wobble(dur=0.7, f=150, rate=11):
    t = t_of(dur)
    y = osc(f * (1 + 0.08 * np.sin(2 * np.pi * rate * t))) * (0.55 + 0.45 * np.sin(2 * np.pi * rate * t))
    return norm(y * env(dur, 0.02, None, 0.15))


def stretch(dur=1.6, f0=280, f1=470):
    """Tiếng cao su căng ra (Piko rướn người)."""
    t = t_of(dur)
    f = glide(f0, f1, dur) * (1 + 0.015 * np.sin(2 * np.pi * 7 * t))
    y = osc(f, "tri") * np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.25)
    return norm(lowpass(y, 1800))


def inflate(dur=0.4):
    t = t_of(dur)
    f = glide(210, 560, dur) * (1 + 0.03 * np.sin(2 * np.pi * 18 * t))
    air = band(white(len(t)), 600, 3000) * 0.25
    return norm((osc(f) + 0.3 * osc(f * 1.5) + air) * env(dur, 0.01, None, 0.08))


def deflate(dur=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    cut = 3200 * (300 / 3200) ** (t / dur)
    y = onepole_sweep(white(n), cut) * (0.6 + 0.4 * np.sin(2 * np.pi * 34 * t))
    return norm(y * env(dur, 0.01, None, 0.2))


def beep(f=1800, dur=0.05, harm=0.0):
    t = t_of(dur)
    y = osc(np.full(len(t), f)) + harm * osc(np.full(len(t), f * 3))
    return norm(y * env(dur, 0.002, None, 0.01))


def click(dur=0.015):
    return norm(highpass(white(int(dur * SR)), 2500) * env(dur, 0.0005, 0.003))


def puff(dur=0.32, lo=700, hi=3200):
    return norm(band(white(int(dur * SR)), lo, hi) * env(dur, 0.012, 0.09))


def powerup(dur=1.4):
    f = glide(110, 900, dur)
    y = lowpass(osc(f, "saw"), 2500) + 0.3 * band(white(len(f)), 1500, 6000) * np.linspace(0, 1, len(f))
    return norm(y * env(dur, 0.05, None, 0.05))


def siren(dur=1.5, lo=620, hi=930, rate=2.2):
    t = t_of(dur)
    f = lo + (hi - lo) * (0.5 + 0.5 * np.sin(2 * np.pi * rate * t - np.pi / 2))
    y = osc(f) + 0.25 * osc(f * 3)
    return norm(y * env(dur, 0.02, None, 0.1))


def squeak(f0=1500, f1=1050, dur=0.11):
    return norm(osc(glide(f0, f1, dur)) * env(dur, 0.004, None, 0.03))


def plink(f=2600, dur=0.07):
    return norm(osc(glide(f * 0.8, f * 1.3, dur)) * env(dur, 0.001, 0.015))


def bell(f=1800, dur=0.9):
    t = t_of(dur)
    y = osc(np.full(len(t), f)) + 0.4 * osc(np.full(len(t), f * 2.76)) + 0.2 * osc(np.full(len(t), f * 5.4))
    return norm(y * env(dur, 0.002, 0.25))


def big_drop():
    """Giọt nước to rơi 'BOP': bong bóng cộng hưởng vút lên + tiếng thịch trầm."""
    d = 0.32
    y = osc(glide(380, 1500, d)) * env(d, 0.002, 0.07)
    thud = osc(glide(110, 50, d)) * env(d, 0.002, 0.09)
    return norm(y + 0.9 * thud)


def thunder(dur=4.0, seed=1):
    n = int(dur * SR)
    r = np.random.default_rng(seed)
    t = np.arange(n) / SR
    crack = highpass(r.standard_normal(n), 1200) * np.exp(-t / 0.07)
    rumble = lowpass(brown(n), 170) * np.minimum(1, t / 0.08) * np.exp(-t / 1.4)
    rumble *= smooth_random(n, 0.18, 0.3, 1.0, seed)
    return norm(0.55 * norm(crack) + norm(rumble))


def sad_trombone(note_dur=0.42, last=1.25):
    """Bốn nốt đi xuống 'wah wah wah waaah' (kèn đồng giả bằng saw + lọc + rung)."""
    notes = [293.66, 277.18, 261.63, 246.94]
    out = []
    for k, f in enumerate(notes):
        d = last if k == 3 else note_dur
        t = t_of(d)
        vib = 1 + (0.012 if k < 3 else 0.03 * np.minimum(1, t / 0.35)) * np.sin(2 * np.pi * 5.5 * t)
        y = lowpass(osc(f * vib, "saw") + 0.5 * osc(f * vib * 0.5, "saw"), 1400)
        e = np.minimum(1, t / 0.04) * np.minimum(1, (d - t) / 0.08)
        if k == 3:
            e *= np.linspace(1, 0.35, len(t))
        out.append(y * e)
    return norm(np.concatenate(out))


# ---------------------------------------------------------------- nền dài
def wind(n, seed=3):
    y = band(brown(n), 60, 750)
    return norm(y * smooth_random(n, 1.7, 0.35, 1.0, seed))


def cicadas(n):
    t = np.arange(n) / SR
    buzz = band(white(n), 3600, 6800) * (0.5 + 0.5 * np.sin(2 * np.pi * 31 * t)) ** 4
    phrase = 0.55 + 0.45 * np.sin(2 * np.pi * 0.23 * t)
    return norm(buzz * phrase)


def machine_hum(n):
    t = np.arange(n) / SR
    y = osc(np.full(n, 98.0)) + 0.4 * osc(np.full(n, 196.0)) + 0.6 * norm(band(white(n), 140, 420))
    return norm(y * (0.85 + 0.15 * np.sin(2 * np.pi * 1.6 * t)))


def machine_rumble(n):
    t = np.arange(n) / SR
    motor = lowpass(osc(np.full(n, 55.0) * (1 + 0.02 * np.sin(2 * np.pi * 3 * t)), "saw"), 320)
    rattle = band(white(n), 90, 520) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t))
    whine = osc(880 * (1 + 0.01 * np.sin(2 * np.pi * 5 * t))) * 0.12
    return norm(norm(motor) + 0.8 * norm(rattle) + whine)


def steam_hiss(n):
    return norm(band(white(n), 1500, 7000) * smooth_random(n, 0.25, 0.6, 1.0, 11))


def rain(n, density_curve, seed=5):
    """Mưa = nền pink noise + hạt rơi lách tách (mật độ theo density_curve 0..1)."""
    r = np.random.default_rng(seed)
    bed = band(pink(n), 400, 9000)
    hits = np.zeros(n)
    p = density_curve * 220 / SR          # tối đa ~220 hạt/giây
    idx = np.nonzero(r.random(n) < p)[0]
    drop = plink(3000, 0.02)
    for i in idx:
        g = r.uniform(0.15, 1.0)
        seg = drop[: n - i]
        hits[i:i + len(seg)] += g * seg
    return norm(norm(bed) * 0.8 + 0.35 * norm(hits + 1e-9))


# ---------------------------------------------------------------- mixer
class Track:
    """Buffer stereo dài bằng shot; đặt tiếng theo frame phim."""

    def __init__(self, frames, fps=24):
        self.fps = fps
        self.n = int(frames / fps * SR) + SR
        self.buf = np.zeros((self.n, 2))

    def add(self, sound, frame, gain=1.0, pan=0.0):
        i = int((frame - 1) / self.fps * SR)
        if i >= self.n or i + len(sound) <= 0:
            return
        s = sound[max(0, -i):]
        i = max(0, i)
        s = s[: self.n - i]
        a = (pan + 1) * np.pi / 4      # pan đẳng công suất
        self.buf[i:i + len(s), 0] += s * gain * np.cos(a)
        self.buf[i:i + len(s), 1] += s * gain * np.sin(a)

    def bed(self, sound, level, pan=0.0):
        """Âm nền cả shot nhân với đường mức level (cùng độ dài buffer)."""
        a = (pan + 1) * np.pi / 4
        s = sound[: self.n] * level[: self.n]
        self.buf[: len(s), 0] += s * np.cos(a)
        self.buf[: len(s), 1] += s * np.sin(a)


def master(buf, peak_db=-1.0, fade_out=0.6):
    y = np.tanh(buf * 1.1) / np.tanh(1.1)          # nén mềm, tránh vỡ tiếng
    y = norm(y, 10 ** (peak_db / 20))
    k = int(fade_out * SR)
    y[-k:] *= np.linspace(1, 0, k)[:, None]
    return y


def write_wav(path, stereo):
    data = (np.clip(stereo, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())
