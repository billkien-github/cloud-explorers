"""Mốc thời gian và CC của post-credit tập 000A (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh.
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #6# (POST-CREDIT, 5 giây)."""
FPS, SECONDS = 24, 5.0
SHOTS = [
    ("S1", 0.0, 5.0),     # bãi phế liệu lúc hoàng hôn, máy đẩy chậm vào hộp kim loại; hòn đảo xa xa sau đống phế liệu
]

PUSH = (0.0, 5.0)               # máy đẩy chậm vào chiếc hộp
HUB_FLASH = 2.6                 # hòn đảo lóe xanh ngọc: cùng nhịp lóe với lần lóe cuối của Cảnh 5 (HUB_FLASH2 ở scene05)
PACK_FLASH = HUB_FLASH          # cùng nhịp đó, Inventor Pack trong hộp lóe xanh ngọc qua khe nắp

# Mỗi dòng hiện từ lúc việc xảy ra, khoảng 20 ký tự mỗi giây trở xuống
CC = [
    (0.2, 2.5, "[bãi phế liệu: hộp kim loại phủ bụi, nắp hé]"),
    (HUB_FLASH, SECONDS, "[hòn đảo lóe xanh ngọc, ba lô trong hộp lóe theo]"),
]
