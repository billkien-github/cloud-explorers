"""
Nhịp của clip nhảy (dùng chung cho build_shot.py và build_audio.py để miệng mở đúng nốt nhạc).
Điệu nhảy kiểu "Baby Shark" (tay khép mở như hàm cá: baby = bàn tay, mommy = cẳng tay, daddy = cả cánh tay),
nhạc và giai điệu tự sáng tác.
"""
FPS, BPM = 24, 120
BEAT = FPS * 60 / BPM               # 12 khung một nhịp
BEATS = 32
FRAMES = int(BEATS * BEAT)          # 384 khung = 16 giây
SECTIONS = {"intro": (0, 4), "baby": (4, 12), "mommy": (12, 20), "daddy": (20, 28), "finale": (28, 32)}


def frame(beat):
    """Khung (bắt đầu từ 1) của một nhịp (số thực)."""
    return 1 + beat * BEAT


def section(beat):
    return next((name for name, (a, b) in SECTIONS.items() if a <= beat < b), "finale")


# câu nhạc 8 nhịp: (nhịp trong câu, độ dài nhịp, độ cao so với Đô) — ngũ cung Đô trưởng
PHRASE = [(0, 0.5, 7), (0.5, 0.5, 9), (1, 1, 12), (2, 0.5, 9), (2.5, 0.5, 7), (3, 1, 4),
          (4, 0.5, 7), (4.5, 0.5, 9), (5, 0.5, 12), (5.5, 0.5, 14), (6, 1.5, 12)]
OCTAVE = {"baby": 72, "mommy": 60, "daddy": 48}     # baby cao, daddy trầm
MELODY = [(a + b, d, OCTAVE[name] + n) for name in ("baby", "mommy", "daddy")
          for a in range(SECTIONS[name][0], SECTIONS[name][1], 8) for b, d, n in PHRASE]   # (nhịp, độ dài, MIDI)
SHOUTS = [(3, 0.75), (30, 2.0)]     # "hây!" cuối đoạn mở màn, "ta-da!" lúc kết (nhịp, độ dài)
BLINKS = [2.2, 9.1, 15.6, 22.4, 26.8]               # nhịp chớp mắt; nháy mắt phải ở nhịp 30.5
