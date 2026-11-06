"""Mốc thời gian và CC của Cảnh 5 tập 000A: Tiếng gọi (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh.
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #5#."""
FPS, SECONDS = 24, 58.5
SHOTS = [
    ("S1", 0.0, 2.4),     # cận la bàn trong tay Lumo, ngọn đồi chắn tầm nhìn: mũi sao chỉ qua đỉnh đồi, le lói
    ("S2", 2.4, 6.4),     # toàn chân đồi: Lumo hạ la bàn, ngẩng nhìn đỉnh đồi, leo lên sườn cỏ thoải
    ("S3", 6.4, 9.6),     # toàn đỉnh đồi: biển mây, tảng đá giữa đỉnh, mép bên kia dốc lá khô xuống thảm cỏ, lối mòn bên cạnh
    ("S4", 9.6, 12.8),    # trung: đặt bản đồ lên tảng đá, hai tay nâng la bàn ngang ngực, nhìn ra chân trời
    ("S5", 12.8, 14.6),   # cận la bàn, chân trời phía sau: mũi sao chỉ vào biển mây
    ("S6", 14.6, 21.8),   # trung toàn: gió thổi tạt, mây tách, hòn đảo dần hiện ra; đài thiên văn lóe, la bàn lóe theo
    ("S7", 21.8, 26.0),   # cận Lumo: "Một nơi chưa ai khám phá…", "Được rồi, bạn la bàn."
    ("S8", 26.0, 30.6),   # trung, đảo ở hậu cảnh: câu hô lần 3; cất la bàn, kéo dây túi, lao ra khỏi khung
    ("S9", 30.6, 35.6),   # cận tảng đá: bản đồ nằm lại một mình; Lumo chạy ngược vào, chụp bản đồ, câu chống chế
    ("S10", 35.6, 39.0),  # cận bản đồ (Lumo nhìn xuống): xoay, xoay nữa, xoay thêm vòng nữa
    ("S11", 39.0, 41.2),  # trung: nhún vai, gấp bản đồ nhét vào túi
    ("S12", 41.2, 45.2),  # toàn mép đồi, thấy cả sườn dốc xuống tới thảm cỏ: sải bước, nhấc chân, khựng lại; lá trượt; nhìn sang bên
    ("S13", 45.2, 46.4),  # góc nhìn của Lumo từ mép đồi: dốc lá khô bên trái, máy lia sang lối mòn thoai thoải bên phải
    ("S14", 46.4, 47.6),  # trung: Lumo gật đầu
    ("S15", 47.6, 50.4),  # cận chú chim đáp xuống tảng đá, nhìn theo Lumo, gật gù
    ("S16", 50.4, 53.8),  # trung ở mép đồi, đảo ở hậu cảnh: rút la bàn, nhìn mũi sao, ngẩng nhìn hòn đảo, cất la bàn
    ("S17", 53.8, 58.0),  # máy lia theo Lumo đi xuống lối mòn; hòn đảo lóe lần nữa, la bàn lóe qua mép nắp túi
    ("S18", 58.0, 58.5),  # CUT TO BLACK
]

# --- chân đồi, leo lên
NEEDLE_FAR = (0.0, 6.4)         # la bàn sáng le lói, mũi sao chỉ qua đỉnh đồi (không rung, không kêu: còn xa)
COMPASS_LOWER = (2.6, 2.9)      # hạ la bàn xuống ngang bụng
LOOK_HILL = (2.9, 3.3)          # ngẩng nhìn đỉnh đồi, dựng tai
CLIMB = (3.4, 5.4)              # leo lên sườn cỏ thoải, mắt nhìn phía trước
TOP_WALK = (5.4, 8.0)           # lên tới đỉnh, đi tới tảng đá giữa đỉnh đồi
VIEW_LOOK = (8.2, 9.4)          # dừng lại, nhìn ra biển mây

# --- đặt bản đồ, nâng la bàn
MAP_DOWN = (9.8, 10.5)          # đặt tấm bản đồ giấy lên tảng đá
COMPASS_UP = (10.7, 11.3)       # hai tay nâng la bàn lên ngang ngực
LOOK_HORIZON = 11.5             # nhìn theo mũi sao ra chân trời: chỉ có mây

# --- gió, mây tách, hòn đảo hiện ra, lóe lần 1
GUST = (14.9, 16.6)             # một cơn gió thổi tạt từ phía chân trời: tai, áo choàng, cỏ rạp
CLOUD_PART = (15.6, 19.0)       # các tầng mây phía xa tách ra, hòn đảo dần hiện ra
LUMO_LEAN = (16.8, 17.4)        # Lumo mở mắt, chồm tới nhìn
HUB_FLASH1 = 19.8               # đài thiên văn lóe sáng xanh ngọc; đúng nhịp đó la bàn lóe theo
LUMO_REACT = (20.0, 20.6)       # tai bật dựng, mắt tròn

# --- hai câu thoại, câu hô lần 3
LUMO_LINE1 = (22.1, 24.4)       # LUMO (nhỏ giọng): Một nơi chưa ai khám phá…
LOOK_COMPASS = 24.3             # cúi nhìn la bàn trong tay
LUMO_LINE2 = (24.5, 25.9)       # LUMO: Được rồi, bạn la bàn.
LUMO_POSE = (26.15, 26.6)       # dựng thẳng hai tai, chìa la bàn thẳng ra trước ngang ngực
LUMO_LINE3 = (26.8, 28.7)       # LUMO: Điều kỳ lạ… ngay phía trước!
COMPASS_STOW = (28.9, 29.35)    # cất la bàn vào túi da
STRAP_TUG = (29.4, 29.75)       # kéo dây túi cho ngay
DASH = (29.85, 30.45)           # quay người lao đi, ra khỏi khung bên phải

# --- quên bản đồ
MAP_ALONE = (30.6, 31.9)        # máy đứng yên trên tảng đá: tấm bản đồ nằm lại một mình
LUMO_BACK = (31.9, 32.4)        # Lumo chạy ngược vào khung, khựng lại cạnh tảng đá
MAP_GRAB = (32.4, 32.75)        # chụp lấy tấm bản đồ
LUMO_LINE4 = (33.0, 35.6)       # LUMO: Nhà thám hiểm Lumo không bao giờ quên bản đồ!
TURN_EDGE = (35.35, 35.55)      # quay về phía mép đồi, mở bản đồ
MAP_SPINS = ((36.0, 36.35), (36.75, 37.05), (37.5, 38.3))   # xoay; xoay nữa; xoay thêm vòng nữa: rương lộn lên lộn xuống
SHRUG = (39.2, 39.8)            # nhún vai
MAP_STOW = (40.0, 40.8)         # gấp bản đồ nhét vào túi

# --- mép dốc lá khô
STRIDE = (41.3, 42.5)           # sải bước nhanh ra mép đồi bên kia
LEG_LIFT = (42.5, 42.8)         # nhấc chân định lao xuống
FREEZE = (42.8, 43.6)           # khựng lại, chân còn nhấc
LEAF_SLIDE = (43.6, 44.3)       # một làn gió nhẹ, chiếc lá khô trượt vèo xuống dốc: WHOOSH!
LEG_BACK = (44.4, 44.7)         # rụt chân về, lùi một bước; mắt vẫn nhìn chiếc lá ở chân dốc
LOOK_PATH = (45.05, 45.2)       # nhìn sang bên: lối mòn thoai thoải
PATH_PAN = (45.35, 45.95)       # máy lia theo ánh mắt từ chiếc lá ở chân dốc sang lối mòn
LUMO_NOD = (46.55, 47.35)       # gật đầu

# --- chú chim, la bàn, lối mòn
BIRD_LAND = (47.7, 48.4)        # chú chim nhỏ đáp xuống tảng đá
BIRD_NOD = (49.0, 50.1)         # nhìn theo Lumo, gật gù
COMPASS_OUT = (50.6, 51.1)      # rút la bàn ra, nhìn mũi sao
LOOK_ISLAND = (51.7, 52.4)      # ngẩng lên nhìn hòn đảo
COMPASS_AWAY = (52.9, 53.5)     # cất la bàn
WALK_DOWN = (53.9, 58.0)        # đi xuống theo lối mòn, mắt nhìn phía trước
HUB_FLASH2 = 56.3               # hòn đảo lóe xanh ngọc lần nữa; qua mép nắp túi da, la bàn lóe theo (cùng nhịp post-credit)

# Mỗi dòng hiện từ lúc việc xảy ra, khoảng 20 ký tự mỗi giây trở xuống
CC = [
    (0.1, 2.4, "[la bàn le lói, chỉ qua ngọn đồi]"),
    (CLIMB[0], CLIMB[1] - 0.3, "[Lumo leo lên đồi]"),
    (6.5, 7.9, "[đỉnh đồi nhìn ra biển mây]"),
    (7.9, 9.6, "[mép bên kia: dốc lá khô, lối mòn]"),
    (MAP_DOWN[0], COMPASS_UP[0] + 0.3, "[đặt bản đồ lên tảng đá]"),
    (COMPASS_UP[0] + 0.3, 12.6, "[hai tay nâng la bàn]"),
    (12.8, 14.6, "[mũi sao chỉ về chân trời]"),
    (GUST[0], GUST[1], "[một cơn gió thổi tạt]"),
    (GUST[1], HUB_FLASH1 - 0.2, "[mây tách, hòn đảo dần hiện ra]"),
    (HUB_FLASH1, LUMO_LINE1[0], "[đài thiên văn lóe xanh ngọc, la bàn lóe theo]"),
    (LUMO_LINE1[0], LUMO_LINE1[1], "LUMO (nhỏ giọng): Một nơi chưa ai khám phá…"),
    (LUMO_LINE2[0], LUMO_LINE2[1], "LUMO: Được rồi, bạn la bàn."),
    (26.05, LUMO_LINE3[1], "[dựng tai, chìa la bàn]"),
    (LUMO_LINE3[0], LUMO_LINE3[1], "LUMO: Điều kỳ lạ… ngay phía trước!"),
    (COMPASS_STOW[0], 30.6, "[cất la bàn, kéo dây túi, lao đi]"),
    (MAP_ALONE[0], LUMO_BACK[0], "[bản đồ nằm lại một mình]"),
    (LUMO_BACK[0], 33.6, "[chạy ngược lại, chụp bản đồ]"),
    (LUMO_LINE4[0], LUMO_LINE4[1], "LUMO: Nhà thám hiểm Lumo không bao giờ quên bản đồ!"),
    (MAP_SPINS[0][0], MAP_SPINS[1][0], "[xoay]"),
    (MAP_SPINS[1][0], MAP_SPINS[2][0], "[xoay nữa]"),
    (MAP_SPINS[2][0], 38.9, "[xoay thêm vòng nữa]"),
    (SHRUG[0], 41.1, "[nhún vai, cất bản đồ vào túi]"),
    (STRIDE[0], LEG_LIFT[0], "[sải bước ra mép đồi]"),
    (LEG_LIFT[0], LEAF_SLIDE[0], "[nhấc chân… khựng lại]"),
    (LEAF_SLIDE[0], LOOK_PATH[0], "[chiếc lá trượt vèo: WHOOSH!]"),
    (LOOK_PATH[0], 46.4, "[nhìn sang lối mòn]"),
    (LUMO_NOD[0], 47.6, "[Lumo gật đầu]"),
    (BIRD_LAND[0], BIRD_NOD[0], "[chim đáp xuống tảng đá]"),
    (BIRD_NOD[0], 50.4, "[chim gật gù]"),
    (COMPASS_OUT[0], LOOK_ISLAND[1] + 0.1, "[nhìn mũi sao, ngẩng nhìn hòn đảo]"),
    (COMPASS_AWAY[0], 53.8, "[cất la bàn]"),
    (WALK_DOWN[0], 55.7, "[đi xuống theo lối mòn]"),
    (HUB_FLASH2, SHOTS[-1][1], "[hòn đảo lóe, la bàn lóe qua túi]"),   # tắt khi sang khung đen
]
