"""Mốc thời gian và CC của Cảnh 3 tập 000A: Khám phá đầu tiên (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh.
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #3# (phế tích) và #3A# (vòm đá)."""
FPS, SECONDS = 24, 74.9
SHOTS = [
    ("S1", 0.0, 3.4),     # toàn: đi dọc bức tường, la bàn trước ngực; mũi sao chỉ mảng dây leo phía trước
    ("S2", 3.4, 6.6),     # trung, máy theo: càng gần càng sáng, rung mạnh dần, TÍT… TÍT… TÍT TÍT TÍT!
    ("S3", 6.6, 10.2),    # trung: vạch dây leo, phù điêu đám mây, những đường mây ánh lên
    ("S4", 10.2, 15.4),   # trung: thử ấn, không có gì; thử kéo, không có gì
    ("S5", 15.4, 21.6),   # trung rộng: lấy đà đẩy, phù điêu xoay, ngã lăn ra thảm rêu; cửa thấp mở, phù điêu tắt
    ("S6", 21.6, 26.0),   # cận la bàn: dịu đi, rung khẽ, TÍT… TÍT…; mũi sao rời phù điêu, quay vào trong cửa thấp
    ("S7", 26.0, 29.4),   # trung: "Mình tìm được rồi!", bước vào cửa thấp
    ("S8", 29.4, 35.0),   # toàn vòm đá: ánh sáng tản đều, bệ đỡ trống, cánh cửa khắc mây cuối vòm; khựng lại, cụp tai
    ("S9", 35.0, 46.4),   # trung ở bệ: ấn la bàn vào hình khắc; gõ bệ, chờ sỏi, thở phào, PLOP; nhìn bệ, nhìn la bàn
    ("S10", 46.4, 49.2),  # trung rộng: đứng ở bệ quay lưng về phía cánh cửa khắc mây, liếc la bàn
    ("S11", 49.2, 56.4),  # cận la bàn, cánh cửa ở hậu cảnh: chỉ ra sau lưng; xoay trái, xoay phải, xoay hai vòng
    ("S12", 56.4, 59.4),  # trung: chóng mặt, loạng choạng, hai tai lắc lư
    ("S13", 59.4, 64.0),  # trung rộng: bước về phía cánh cửa, la bàn sáng thêm, rung mạnh dần; hình mây lấp lánh
    ("S14", 64.0, 74.9),  # trung ở cánh cửa: "Khoan đã…", mắt sáng lên, "Cậu dẫn tới…"; cất la bàn, chạy tới đẩy cửa
]

# --- dọc bức tường tới mảng dây leo
WALK_WALL = (0.4, 6.0)          # đi dọc bức tường, la bàn giữ trước ngực, chậm dần khi tới gần mảng dây leo
BEEPS_SPARSE = (1.2, 2.6)       # còn xa: TÍT… TÍT…
BEEPS_DENSE = (3.8, 6.2)        # tới gần: kêu dày dần, TÍT TÍT TÍT!
SWAP_FAR = 6.75                 # chuyền la bàn sang tay xa để vạch dây leo
PART_VINES = (7.0, 7.8)         # vạch dây leo: phù điêu hình đám mây
RELIEF_ON = 8.1                 # những đường mây trên phù điêu ánh lên
PRESS = (10.5, 11.3)            # thử ấn vào
PRESS_NOTHING = (11.4, 12.2)    # không có gì
PULL = (12.4, 13.6)             # thử kéo
PULL_NOTHING = (13.7, 14.6)     # không có gì
RUNUP = (15.6, 16.4)            # lùi lại lấy đà
PUSH = (16.5, 16.9)             # lao tới đẩy thật mạnh
RELIEF_TURN = (16.9, 17.25)     # phù điêu đột nhiên xoay nhẹ
TUMBLE = (17.0, 18.3)           # mất thăng bằng, ngã lăn ra thảm rêu dày
DOOR_OPEN = (18.9, 19.9)        # cửa thấp mở ra trong tường, ánh sáng ban ngày lọt vào
RELIEF_OFF = 19.7               # những đường mây trên phù điêu tắt
COMPASS_DIM = 21.9              # la bàn dịu đi, còn le lói, rung khẽ
BEEPS_INSERT = (22.3, 23.3, 24.6)   # kêu thưa: TÍT… TÍT…
NEEDLE_TO_DOOR = (23.5, 24.1)   # mũi sao rời phù điêu, quay vào phía trong cửa thấp
GET_UP = (26.0, 26.4)           # bật dậy khỏi thảm rêu
LUMO_LINE1 = (26.4, 27.7)       # LUMO: Mình tìm được rồi!
INTO_DOOR = (28.0, 29.3)        # bước vào cửa thấp

# --- vòm đá
ENTER_VAULT = (29.6, 32.0)      # bước qua cửa thấp vào vòm đá, tới bệ đỡ
VAULT_PUSH = 31.6               # máy từ toàn vòm (thấy cánh cửa khắc mây) đẩy vào bệ
SEE_EMPTY = 32.4                # nhìn bệ trống, khựng lại
EARS_DOWN1 = 32.9               # cụp tai
PED_PRESS = (35.3, 36.2)        # ấn la bàn khớp vào hình khắc trên bệ
PED_NOTHING = (36.3, 37.2)      # không có gì
PED_KNOCKS = (37.6, 38.0, 38.4)     # gõ lên bệ: TOK. TOK. TOK.
WAIT_PEBBLE = (38.8, 40.6)      # cụp tai, ngước nhìn trần, chờ hòn sỏi; không có gì
RELIEF_SIGH = (40.7, 41.4)      # thở phào, hai tai dựng lên
PLOP = 42.0                     # hòn sỏi rơi trúng đầu
PLOP_REACT = (42.05, 43.2)      # cụp tai, nhắm tịt mắt
LIFT_COMPASS = (43.6, 44.1)     # nhấc la bàn lên
LOOK_PED = 44.3                 # nhìn bệ trống
LOOK_COMPASS = 45.0             # nhìn la bàn trong tay
HEAD_TILT = 45.5                # nghiêng đầu
TURN_AWAY = (46.6, 46.8)        # đứng quay lưng về phía cánh cửa khắc mây
GLANCE = 47.4                   # liếc la bàn
SPIN_LEFT = 50.8                # xoay phắt sang trái
SPIN_RIGHT = 52.6               # xoay phắt sang phải
SPINS = (54.0, 55.8)            # xoay một vòng (hai lần lật), ngừng nhìn la bàn, rồi thêm vòng nữa
DIZZY = (56.5, 59.0)            # chóng mặt, loạng choạng, hai tai lắc lư
TO_DOOR = (59.8, 63.0)          # bước về phía cánh cửa: mỗi bước la bàn sáng thêm, rung mạnh dần
BEEPS_DOOR = (60.0, 61.8)       # mỗi bước: TÍT… TÍT…
BEEPS_DOOR_DENSE = (61.8, 63.6) # tới gần cửa: TÍT TÍT TÍT!
DOOR_SPARKLE = 61.6             # những hình mây trên cánh cửa lấp lánh
LUMO_LINE2 = (64.3, 67.4)       # LUMO: Khoan đã… cậu không dẫn tới kho báu.
EYES_SHINE = (67.8, 68.6)       # nhìn cánh cửa lấp lánh, mắt sáng lên
LUMO_LINE3 = (69.2, 72.2)       # LUMO: Cậu dẫn tới những thứ… kỳ lạ!
STOW = (72.6, 73.3)             # nhét la bàn vào túi da
RUN_PUSH = (73.4, 74.4)         # chạy tới đẩy cánh cửa khắc mây, cửa hé khe sáng

# Mỗi dòng hiện từ lúc việc xảy ra, khoảng 20 ký tự mỗi giây trở xuống
CC = [
    (WALK_WALL[0], 2.4, "[đi dọc bức tường, la bàn trước ngực]"),
    (2.4, BEEPS_DENSE[0], "[la bàn sáng dần: TÍT… TÍT…]"),
    (BEEPS_DENSE[0], 6.4, "[càng gần càng rung: TÍT TÍT TÍT!]"),
    (PART_VINES[0], RELIEF_ON + 0.5, "[vạch dây leo: phù điêu đám mây]"),
    (RELIEF_ON + 0.5, 10.2, "[những đường mây ánh lên]"),
    (PRESS[0], PULL[0] - 0.1, "[thử ấn: không có gì]"),
    (PULL[0], PULL_NOTHING[1], "[thử kéo: không có gì]"),
    (RUNUP[0], RELIEF_TURN[0], "[lấy đà, đẩy thật mạnh]"),
    (RELIEF_TURN[0], DOOR_OPEN[0], "[phù điêu xoay, Lumo ngã lăn ra rêu]"),
    (DOOR_OPEN[0], RELIEF_OFF + 0.9, "[cửa thấp mở ra, ánh sáng lọt vào]"),
    (RELIEF_OFF + 0.9, 21.6, "[phù điêu tắt]"),
    (COMPASS_DIM, NEEDLE_TO_DOOR[0], "[la bàn dịu đi: TÍT… TÍT…]"),
    (NEEDLE_TO_DOOR[0], 25.9, "[mũi sao quay vào trong cửa thấp]"),
    (LUMO_LINE1[0], LUMO_LINE1[1], "LUMO: Mình tìm được rồi!"),
    (ENTER_VAULT[0], VAULT_PUSH, "[vòm đá, cánh cửa khắc mây cuối vòm]"),
    (VAULT_PUSH, SEE_EMPTY + 0.1, "[bệ đỡ trống]"),
    (SEE_EMPTY + 0.1, 34.9, "[khựng lại, cụp tai]"),
    (PED_PRESS[0], PED_KNOCKS[0] - 0.25, "[ấn la bàn vào hình khắc: không có gì]"),
    (PED_KNOCKS[0] - 0.25, WAIT_PEBBLE[0] - 0.1, "[gõ lên bệ: TOK. TOK. TOK.]"),
    (WAIT_PEBBLE[0] - 0.1, WAIT_PEBBLE[1], "[cụp tai, nhìn trần, chờ sỏi]"),
    (RELIEF_SIGH[0], PLOP - 0.05, "[thở phào, dựng tai]"),
    (PLOP, PLOP_REACT[1] + 0.2, "[PLOP! Sỏi rơi trúng đầu]"),
    (LIFT_COMPASS[0], 46.2, "[nhìn bệ trống, nhìn la bàn, nghiêng đầu]"),
    (TURN_AWAY[0], 48.8, "[quay lưng về phía cánh cửa, liếc la bàn]"),
    (49.3, SPIN_LEFT, "[mũi sao chỉ ra sau lưng]"),
    (SPIN_LEFT, SPIN_RIGHT - 0.1, "[xoay trái: mũi sao vẫn chỉ cửa]"),
    (SPIN_RIGHT, SPINS[0] - 0.1, "[xoay phải: vẫn chỉ cửa]"),
    (SPINS[0], 56.3, "[xoay hai vòng: không rời cánh cửa]"),
    (DIZZY[0] + 0.1, 58.6, "[chóng mặt, loạng choạng]"),
    (TO_DOOR[0], DOOR_SPARKLE, "[mỗi bước sáng thêm: TÍT… TÍT…]"),
    (DOOR_SPARKLE, 63.9, "[cửa lấp lánh: TÍT TÍT TÍT!]"),
    (LUMO_LINE2[0], LUMO_LINE2[1], "LUMO: Khoan đã… cậu không dẫn tới kho báu."),
    (EYES_SHINE[0], LUMO_LINE3[0] - 0.1, "[mắt sáng lên]"),
    (LUMO_LINE3[0], LUMO_LINE3[1], "LUMO: Cậu dẫn tới những thứ… kỳ lạ!"),
    (STOW[0], SECONDS, "[nhét la bàn vào túi, chạy tới đẩy cửa]"),
]
