"""Mốc thời gian và CC của Cảnh 2 tập 000A: Ánh sáng lạ (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh.
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #2#."""
FPS, SECONDS = 24, 44.8
SHOTS = [
    ("S1", 0.0, 4.85),     # nối cuối Cảnh 1: Lumo chui ra khỏi đống lá, bướm bay đi, bước tới phiến đá, ngồi xổm nhấc lên
    ("S2", 4.85, 7.0),     # cận hốc dưới phiến đá: la bàn vàng; thò tay rút ra, phiến đá rơi về chỗ
    ("S3", 7.0, 13.9),    # trung cận: "Ồ! Kho báu!"; thổi bụi, bụi bay ngược vào mặt, hắt xì, lau kính bằng vạt áo choàng
    ("S4", 13.9, 19.4),   # cận la bàn và mặt Lumo: kính sáng le lói, ngôi sao rung rung, xoay phắt, TÍT… TÍT…; giật mình
    ("S5", 19.4, 23.0),   # cận la bàn, bức tường ở hậu cảnh: mũi sao chỉ về phía bức tường, chếch về mảng dây leo xa hơn
    ("S6", 23.0, 25.4),   # trung: bước vòng sang phía bên kia phiến đá, tới đầu tường
    ("S7", 25.4, 28.2),   # cận la bàn: Lumo quay lại, mũi sao xoay theo, vẫn chỉ về phía bức tường
    ("S8", 28.2, 34.0),   # trung: "Hừm… la bàn phải chỉ hướng Bắc chứ. Sao lại chỉ vào tường?"
    ("S9", 34.0, 40.0),   # trung cận ở đầu tường: quay vào tường, áp tai, gõ ba lần, hòn sỏi rơi trúng đầu, cụp tai
    ("S10", 40.0, 44.8),  # trung: "Mình nghĩ bức tường không thích bị làm phiền."; liếc la bàn
]

# --- chui ra khỏi đống lá, nhấc phiến đá
CLIMB_OUT = (0.5, 1.9)          # nhổm khỏi đống lá, bước ra, lá rơi khỏi người
BFLY_OFF = (1.3, 3.2)           # con bướm trên phiến đá rêu bay lên, qua phế tích
WALK_SLAB = (2.1, 3.3)          # bước tới phiến đá có ánh vàng
SQUAT = (3.4, 3.8)              # ngồi xổm trước phiến đá
SLAB_LIFT = (4.0, 4.8)          # nhấc phiến đá lên (bản lề ở mép sát tường), ánh vàng bung ra
COMPASS_SEE = 4.8               # thấy la bàn trong hốc: tròn mắt
GRAB = (6.0, 6.6)               # thò tay rút la bàn ra
SLAB_DROP = 6.85                # thả phiến đá rơi về chỗ cũ
STAND = (7.0, 7.4)              # đứng dậy, giữ la bàn ngang ngực
LUMO_LINE1 = (7.5, 8.6)         # LUMO: Ồ! Kho báu!
BLOW = (9.0, 9.7)               # cúi mõm thổi bụi: FOOOO!
DUST_BACK = (9.8, 10.2)         # bụi bay ngược vào mặt
SNEEZE = (10.9, 12.0)           # (nhăn mũi, tai giật lên) Hắt… xì!
SNEEZE_HIT = 11.55              # tiếng "xì!": đầu giật tới
WIPE = (12.4, 13.8)             # lau mặt kính bằng vạt áo choàng

# --- la bàn thức dậy
GLASS_GLOW = 14.1               # hết bụi, mặt kính lộ ra đang sáng le lói
NEEDLE_WOBBLE = (14.5, 16.0)    # ngôi sao trên mặt la bàn rung rung
NEEDLE_SNAP = (16.0, 16.3)      # xoay phắt một cái
BEEPS1 = (16.4, 17.3)           # kêu khẽ và thưa: TÍT… TÍT…
STARTLE = (16.5, 18.3)          # giật mình, la bàn tuột khỏi tay, chụp lại được
INSERT_BEEPS = (20.0, 21.3)     # cú cận: TÍT… TÍT…

# --- đi vòng, la bàn vẫn chỉ tường
AROUND = (23.2, 25.2)           # bước vòng sang phía bên kia phiến đá, tới đầu tường
TURN_BACK = (26.0, 26.7)        # quay lại nhìn phía vừa đi (đủ chậm để thấy mũi sao xoay theo), vẫn chỉ về phía bức tường
LUMO_LINE2 = (28.5, 33.2)       # LUMO: Hừm… la bàn phải chỉ hướng Bắc chứ. Sao lại chỉ vào tường?
LOOK_WALL = 31.3                # "Sao lại chỉ vào tường?": ngoái nhìn bức tường sau lưng

# --- áp tai, gõ, hòn sỏi
FACE_WALL = 34.2                # quay mặt vào đầu tường
EAR_PRESS = (34.6, 36.4)        # nghiêng đầu, ép một bên tai to sát vào mảng tường ngay cạnh; không có gì
KNOCKS = (36.9, 37.35, 37.8)    # gõ ba lần: TOK. TOK. TOK.
PEBBLE = (38.3, 38.7)           # hòn sỏi lăn khỏi mép tường, rơi trúng đầu, nảy ra
EARS_DROOP = 38.8               # cụp tai
LUMO_LINE3 = (40.4, 43.3)       # LUMO: Mình nghĩ bức tường không thích bị làm phiền.
GLANCE = 43.8                   # liếc la bàn: mũi sao vẫn chỉ dọc tường

# Mỗi dòng hiện từ lúc việc xảy ra, khoảng 20 ký tự mỗi giây trở xuống
CC = [
    (CLIMB_OUT[0], WALK_SLAB[1], "[Lumo chui ra khỏi đống lá]"),
    (SQUAT[0] + 0.1, 4.85, "[nhấc phiến đá có ánh vàng]"),
    (4.85, SLAB_DROP + 0.15, "[bên dưới là chiếc la bàn vàng]"),
    (LUMO_LINE1[0], LUMO_LINE1[1], "LUMO: Ồ! Kho báu!"),
    (BLOW[0] - 0.1, DUST_BACK[0], "[thổi bụi: FOOOO!]"),
    (DUST_BACK[0], SNEEZE[0] + 0.1, "[bụi bay ngược vào mặt]"),
    (SNEEZE[0] + 0.1, WIPE[0] + 0.5, "LUMO (nhăn mũi, tai giật lên): Hắt xì!"),
    (WIPE[0] + 0.5, GLASS_GLOW + 0.2, "[lau kính bằng áo choàng]"),
    (GLASS_GLOW + 0.2, NEEDLE_SNAP[0], "[kính sáng le lói, sao rung rung]"),
    (NEEDLE_SNAP[0], 18.9, "[xoay phắt: TÍT… TÍT… giật mình, suýt đánh rơi]"),
    (19.5, 23.0, "[mũi sao chỉ về phía bức tường, chếch về mảng dây leo]"),
    (AROUND[0], 25.4, "[bước vòng sang bên kia phiến đá]"),
    (TURN_BACK[0] + 0.1, 28.2, "[mũi sao xoay theo, vẫn chỉ về bức tường]"),
    (LUMO_LINE2[0], LUMO_LINE2[1], "LUMO: Hừm… la bàn phải chỉ hướng Bắc chứ. Sao lại chỉ vào tường?"),
    (EAR_PRESS[0], EAR_PRESS[1] + 0.2, "[áp tai vào tường: không có gì]"),
    (KNOCKS[0], PEBBLE[1], "[gõ: TOK. TOK. TOK.]"),
    (PEBBLE[1], LUMO_LINE3[0], "[hòn sỏi rơi trúng đầu, cụp tai]"),
    (LUMO_LINE3[0], LUMO_LINE3[1], "LUMO: Mình nghĩ bức tường không thích bị làm phiền."),
]
