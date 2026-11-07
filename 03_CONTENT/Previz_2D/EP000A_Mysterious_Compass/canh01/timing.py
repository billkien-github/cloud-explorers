"""Mốc thời gian và CC của Cảnh 1 tập 000A: Nhà thám hiểm nhỏ (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh.
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #1#."""
FPS, SECONDS = 24, 48.6
SHOTS = [
    ("S1", 0.0, 3.4),     # toàn rừng mây: đảo lơ lửng, thác đổ xuống biển mây, bướm qua tán cây; Lumo bước vào khung
    ("S2", 3.4, 5.2),     # cận bản đồ (Lumo nhìn xuống): rương lộn ngược, mũi tên chỉ lên, về phía trước
    ("S3", 5.2, 8.75),    # Lumo dựng tai, chìa bản đồ, bụi gai ngay phía trước; câu hô lần 1; bước tới, vấp hòn đá, ngã vào bụi: SỘT
    ("S4", 8.75, 10.4),   # toàn hơn: mặt cắm trong bụi gai, vách đá cao chắn lối phía sau; lùi ra
    ("S5", 10.4, 13.4),   # cận: quả gai trên chóp mũi, lắc đầu, gai văng; nhìn bụi gai, nhìn bản đồ
    ("S6", 13.4, 15.3),   # cận bản đồ: xoay nửa vòng, rương đứng thẳng, mũi tên chỉ xuống (về phía Lumo)
    ("S7", 15.3, 18.3),   # "À… phía trước là phía sau.", quay ngoắt lại
    ("S8", 18.3, 21.9),   # toàn: con đường rừng rộng mở trước mặt Lumo, Lumo nhảy cẫng lên; tên phim
    ("S9", 21.9, 24.25),  # cận chú chim trên cành: nghiêng đầu, vỗ bụng cười (hai tiếng CHÍP đầu)
    ("S10", 24.25, 31.1), # Lumo và chú chim: CHÍP thứ ba, Lumo cụp tai ngượng, rồi ưỡn ngực, cất bản đồ, chống chế; chim bay đi
    ("S11", 31.1, 34.1),  # Lumo lại rút bản đồ, cắm mặt vào, sải bước nhanh ra khỏi khung
    ("S12", 34.1, 39.1),  # đường rẽ, Lumo đi thẳng, hụt chân ở mép dốc lá khô, trượt xuống, rơi vào đống lá
    ("S13", 39.1, 43.5),  # ngẩng lên khỏi đống lá, chiếc lá giữa trán, lắc đầu, nhặt bản đồ
    ("S14", 43.5, 48.6),  # bướm đậu phiến đá rêu trước mặt Lumo; máy lùi ra: phế tích cổ, ánh vàng le lói
]

# --- rừng mây, bụi gai
LUMO_WALK_IN = (1.4, 5.5)       # Lumo bước vào khung, cắm mặt vào bản đồ, sải bước tự tin, dừng trước bụi gai
LUMO_POSE = (5.5, 5.9)          # dựng thẳng hai tai, chìa bản đồ thẳng ra trước ngang ngực
LUMO_LINE1 = (6.4, 8.3)         # LUMO: Kho báu cổ đại… ngay phía trước!
LUMO_STEP = (8.1, 8.42)         # vừa hô dứt câu vừa sải một bước tự tin, mũi chân vướng hòn đá
TRIP = 8.42                     # vấp hòn đá, chúi người ngã tới
SOT = 8.6                       # ngã cắm mặt vào bụi gai: SỘT!
BACK_OUT = (10.0, 10.35)        # lùi ra, quả gai dính trên chóp mũi
BURR_LOOK = (10.5, 11.2)        # nhìn quả gai trên mũi
HEAD_SHAKE = (11.4, 11.9)       # lắc đầu
BURR_FLY = 11.65                # quả gai văng ra
LOOK_BUSH = (12.35, 12.75)      # nhìn bụi gai
LOOK_MAP = (12.85, 13.25)       # nhìn bản đồ
MAP_TURN = (13.7, 14.3)         # xoay bản đồ nửa vòng
LUMO_LINE2 = (15.5, 17.6)       # LUMO: À… phía trước là phía sau.
LOOK_BEHIND = 16.4              # mắt liếc ra sau lưng ở chữ "phía sau"
LUMO_TURN = (17.8, 17.95)       # quay ngoắt lại
TITLE = (18.7, 21.5)            # tên phim
LUMO_HOP = (19.6, 20.3)         # thấy đường rừng, Lumo nhảy cẫng lên một cái

# --- chú chim
BIRD_TILT = (22.1, 22.5)        # chú chim nghiêng đầu nhìn Lumo
BIRD_LAUGH = (23.2, 25.1)       # lấy cánh vỗ bụng: CHÍP CHÍP CHÍP!
CHIRPS = (23.3, 23.9, 24.5)     # ba cú vỗ bụng, mỗi cú một tiếng CHÍP
LUMO_SHY = (24.3, 25.9)         # Lumo bị cười: cụp tai, mặt ngượng, liếc chú chim
LUMO_PUFF = (25.9, 26.4)        # Lumo ưỡn ngực, dựng thẳng tai
MAP_STOW = (26.5, 27.4)         # gấp bản đồ nhét vào túi da
LUMO_LINE3 = (27.5, 29.8)       # LUMO: Mình biết chứ! Đang kiểm tra bản đồ thôi!
BIRD_FLY = (30.0, 30.8)         # chú chim bay đi

# --- dốc lá khô
MAP_OUT = (31.3, 31.8)          # lại rút bản đồ ra, cắm mặt vào đó
STRIDE = (32.0, 35.5)           # sải bước thật nhanh (qua điểm cắt S11 → S12), bỏ qua chỗ đường rẽ
EDGE = 35.5                     # bước hụt ra mép sườn dốc
WHOOSH = (35.5, 35.85)          # hụt chân, bản đồ tuột tay: WHOOSH!
SLIDE = (35.85, 37.45)          # trượt một mạch xuống dốc lá khô: RUSTLE!
POOF = 37.45                    # rơi vào đống lá trên nền rêu: POOF!
MAP_DRIFT = (35.55, 38.4)       # tấm bản đồ chao lượn rồi rơi xuống mép đống lá
LUMO_POP = 39.3                 # ngẩng đầu khỏi đống lá, chiếc lá dính giữa trán
HEAD_SHAKE2 = (40.5, 41.0)      # lắc mạnh đầu
LEAF_FALL = (40.75, 41.5)       # chiếc lá rơi ra sau, xuống lưng đống lá
MAP_PICK = (41.7, 42.2)         # nhặt tấm bản đồ rơi cạnh đó
MAP_STOW2 = (42.3, 42.9)        # nhét vào túi da

# --- phế tích
BFLY_LAND = (43.7, 44.4)        # bướm phát sáng đậu xuống phiến đá rêu ngay trước mặt Lumo
CAM_REVEAL = (45.1, 46.5)       # máy lùi ra: phía sau con bướm là phế tích cổ
GOLD_GLOW = (45.6, SECONDS)     # giữa những phiến đá, ánh vàng le lói (hiện từ đây, khi máy đang lùi ra)
LUMO_WONDER = 46.3              # Lumo tròn mắt, dựng tai nhìn ánh vàng

# Mỗi dòng hiện từ lúc việc xảy ra, khoảng 20 ký tự mỗi giây trở xuống
CC = [
    (0.2, 1.9, "[rừng mây, thác đổ xuống biển mây]"),
    (1.9, 3.4, "[Lumo cắm mặt vào bản đồ]"),
    (3.4, 5.2, "[rương lộn ngược, mũi tên chỉ lên]"),
    (5.2, LUMO_LINE1[0], "[dựng tai, chìa bản đồ]"),
    (LUMO_LINE1[0], LUMO_LINE1[1], "LUMO: Kho báu cổ đại… ngay phía trước!"),
    (TRIP, SOT + 0.8, "[vấp đá: SỘT!]"),
    (SOT + 0.8, BACK_OUT[1] + 0.1, "[vách đá chắn lối]"),
    (BACK_OUT[1] + 0.1, HEAD_SHAKE[0], "[gai dính chóp mũi]"),
    (HEAD_SHAKE[0], LOOK_BUSH[0], "[lắc đầu: gai văng]"),
    (LOOK_BUSH[0], MAP_TURN[0], "[nhìn bụi gai, nhìn bản đồ]"),
    (MAP_TURN[0], 15.3, "[xoay bản đồ: mũi tên chỉ xuống]"),
    (LUMO_LINE2[0], LUMO_LINE2[1], "LUMO: À… phía trước là phía sau."),
    (LUMO_TURN[0], LUMO_TURN[0] + 0.9, "[quay ngoắt lại]"),
    (TITLE[0], TITLE[0] + 1.7, "[con đường rừng rộng mở]"),
    (BIRD_TILT[0] - 0.1, BIRD_LAUGH[0], "[chú chim nghiêng đầu]"),
    (BIRD_LAUGH[0], BIRD_LAUGH[1] + 0.1, "[chim vỗ bụng: CHÍP CHÍP CHÍP!]"),
    (BIRD_LAUGH[1] + 0.1, LUMO_PUFF[0], "[Lumo cụp tai]"),
    (LUMO_PUFF[0], LUMO_LINE3[0], "[ưỡn ngực, cất bản đồ vào túi]"),
    (LUMO_LINE3[0], LUMO_LINE3[1], "LUMO: Mình biết chứ! Đang kiểm tra bản đồ thôi!"),
    (BIRD_FLY[0], BIRD_FLY[1] + 0.3, "[chú chim bay đi]"),
    (MAP_OUT[0], MAP_OUT[0] + 2.0, "[lại cắm mặt vào bản đồ, sải bước]"),
    (EDGE, EDGE + 0.95, "[hụt chân: WHOOSH!]"),
    (EDGE + 0.95, POOF, "[trượt dốc: RUSTLE!]"),
    (POOF, POOF + 1.25, "[rơi vào đống lá: POOF!]"),
    (LUMO_POP, HEAD_SHAKE2[0], "[lá dính giữa trán]"),
    (HEAD_SHAKE2[0], HEAD_SHAKE2[0] + 1.1, "[lắc đầu, lá rơi]"),
    (MAP_PICK[0], MAP_PICK[0] + 1.4, "[nhặt bản đồ, nhét vào túi]"),
    (BFLY_LAND[0], BFLY_LAND[0] + 1.8, "[bướm phát sáng đậu xuống phiến đá]"),
    (GOLD_GLOW[0], GOLD_GLOW[0] + 2.0, "[phế tích cổ, ánh vàng le lói]"),
]
