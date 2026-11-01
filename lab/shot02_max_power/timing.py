"""
Mốc thời gian của shot 02 (frame @ 24fps). Dùng chung cho build_shot.py (hình) và build_audio.py (tiếng),
sửa ở đây thì cả hai cùng đổi.
"""
FPS, FRAMES = 24, 720

# shot: (frame bắt đầu, frame kết thúc)
SHOTS = {"S1": (1, 96), "S2": (97, 216), "S3": (217, 300), "S4": (301, 340),
         "S5": (341, 420), "S6": (421, 576), "S7": (577, 720)}
PRESS = 306                 # frame nút MAX POWER bị đè
STORM0, STORM1 = 380, 560   # trời chuyển từ nắng sang bão
RAIN_LIGHT, RAIN_HEAVY = 470, 520
WET0, WET1 = 480, 650
PERK0, PERK1 = 540, 640     # hoa ngẩng đầu
FLASHES = (528, 566)        # sấm chớp
BOP = 648                   # giọt mưa to trúng đầu Piko

# các nhịp diễn của Piko (khớp với animate_piko trong build_shot.py)
PIKO_HOPS = [(28, 40), (62, 74), (236, 252), (270, 292), (500, 514), (522, 536), (586, 598)]  # (cất cánh, đáp)
PIKO_SHAKE = (160, 182)     # lắc đầu "không được"
PIKO_INFLATE = 352          # phồng người vì sốc
STEAM_PERIOD_L1 = 14        # Level 1: một làn hơi mỗi 14 frame
