"""Mốc thời gian và CC của Cảnh 4 tập 000A: Cây cầu sập (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh.
Kịch bản: 03_CONTENT/Scripts/EP000A_mysterious_compass.fountain, cảnh #4#."""
FPS, SECONDS = 24, 84.8
SHOTS = [
    ("S1", 0.0, 3.6),     # cánh cửa đá khắc mây nhìn từ phía cầu: cửa mở hẳn, hình mây tắt dần; Lumo loạng choạng ra bậc cửa
    ("S2", 3.6, 9.0),     # toàn: cầu ván cổ qua khe núi, lưới dây leo phủ kín bên dưới, lối nhỏ nửa khuất sau bụi cây, bệ đá
    ("S3", 9.0, 12.6),    # Lumo ở bậc cửa: túi da rung, TÍT… TÍT…; rút la bàn ra
    ("S4", 12.6, 14.8),   # cận la bàn Lumo cầm (máy sau vai): mũi sao chỉ thẳng ngôi sao đá bên kia cầu
    ("S5", 14.8, 18.0),   # dựng tai, chìa la bàn; câu hô lần 2; lấy đà
    ("S6", 18.0, 25.4),   # lao lên cầu, CREAAAAK, cụp tai chờ sỏi, "Không sao…", mắt vẫn ngước mà bước tiếp
    ("S7", 25.4, 27.2),   # toàn hơn: CRACK, cả dãy ván rơi xuống lưới, nảy bập bềnh; khoảng trống dài; Lumo chới với
    ("S8", 27.2, 30.0),   # túm dây leo ở thành cầu sát cửa, ngã ngồi lùi về bậc cửa phủ rêu, đáp lên đuôi bông: PHỊCH
    ("S9", 30.0, 33.4),   # cận chú chim đáp xuống cột cầu, nhìn Lumo, vỗ bụng cười
    ("S10", 33.4, 36.4),  # Lumo ngồi và chú chim: "Được rồi! Một chiếc cầu… rất cũ!"; nhìn la bàn
    ("S11", 36.4, 38.6),  # cận la bàn qua khoảng trống: mũi sao vẫn chỉ ngôi sao đá bên kia
    ("S12", 38.6, 44.0),  # đứng dậy, nhìn khoảng trống, vách đá, bụi cây; vạch bụi cây: bậc đá hiện ra
    ("S13", 44.0, 45.8),  # cận chú chim trên cột cầu: thôi cười, nghiêng đầu
    ("S14", 45.8, 47.8),  # cận Lumo: "Nhìn kỹ trước đã."
    ("S15", 47.8, 50.4),  # cất la bàn, bám tay vịn dây leo, đi chậm lên bậc; chim bay theo xuống bậc đầu
    ("S16", 50.4, 52.8),  # cận bậc đá (chân Lumo ở mép khung): chim nhảy từng bậc, nhấc chân y như Lumo
    ("S17", 52.8, 56.6),  # toàn: men vách vòng qua đầu khe, lưới ngay dưới lối nhỏ; la bàn trong túi kêu dày dần
    ("S18", 56.6, 59.0),  # xuống từng bậc tới bãi đất, đi tới bệ đá, với tay
    ("S19", 59.0, 61.6), # cận mặt bệ nhìn từ trên: bàn tay ấn ngôi sao, lún xuống, CẠCH; phiến đá trượt mở, lộ bản đồ khắc
    ("S20", 61.6, 63.8),  # chú chim đậu lên mép bệ; Lumo rút bản đồ giấy
    ("S21", 63.8, 73.4),  # cận hai bản đồ (giấy đặt cạnh bản đồ khắc): giấy cầm ngược, không khớp; xoay lại: khớp; máy tới
                          # mép phải: đài thiên văn khắc và cùng chỗ đó trên giấy là mây trống; đài thiên văn lóe xanh ngọc rồi tắt
    ("S22", 73.4, 74.6),  # Lumo: ánh xanh đã tắt; chuyển bản đồ sang tay kia, rút la bàn
    ("S23", 74.6, 79.0),  # cận mặt bệ nhìn từ trên, la bàn trong tay Lumo: mũi sao rời ngôi sao đá, về đảo khắc, rồi chỉ
                          # ra chân trời (mép phải); dịu xuống le lói
    ("S24", 79.0, 82.4),  # Lumo nhìn ra chân trời biển mây: "Chưa từng có hòn đảo này trên bản đồ của mình!"
    ("S25", 82.4, 84.8),  # chú chim bay đi về phía chân trời, Lumo nhìn theo
]

# --- cánh cửa, toàn cảnh
DOOR_OPEN = (0.0, 0.7)          # cánh cửa đang hé (Lumo vừa đẩy ở cuối Cảnh 3) mở hẳn ra
LUMO_STUMBLE = (0.25, 1.3)      # hụt tay, loạng choạng bước ra bậc cửa phủ rêu
CLOUDS_FADE = (1.0, 2.4)        # hình mây trên cửa tắt dần
LUMO_WOW = 2.5                  # thấy cây cầu: tròn mắt, dựng tai
LOOK_ACROSS = (5.0, 6.8)        # mắt đi dọc cây cầu sang bệ đá bên kia

# --- la bàn trong túi, câu hô lần 2
BEEPS_BAG = (9.4, 10.2)         # TÍT… TÍT…: túi da rung khẽ
COMPASS_OUT = (10.9, 11.5)      # rút la bàn: sáng le lói, rung khẽ
POSE = (14.9, 15.3)             # dựng thẳng hai tai, chìa la bàn thẳng ra trước ngang ngực
LINE_AHEAD = (16.2, 17.5)       # LUMO: Ngay phía trước!
RUSH = (17.6, 18.55)            # lấy đà, lao lên cầu, mắt dán vào bệ đá (qua điểm cắt S5 → S6)

# --- cầu sập
CREAK = 18.65                   # tấm ván bật lên: CREAAAAK; Lumo khựng lại
WAIT_PEBBLE = (19.2, 21.0)      # cụp tai, ngước nhìn trời, chờ hòn sỏi
NO_PEBBLE = 21.15               # không có sỏi: thở phào
LINE_OLD = (22.0, 24.3)         # LUMO: Không sao. Một chiếc cầu hơi cũ thôi.
STEP_ON = (24.5, 25.5)          # mắt vẫn ngước nhìn trời, bước thêm một bước
CRACK = 25.55                   # tấm ván trước mũi chân gãy: CRACK!
PLANKS_FALL = (25.6, 27.0)      # cả dãy ván phía trước rơi lả tả xuống lưới, nảy bập bềnh
FLAIL = (25.65, 27.3)           # chới với ở mép khoảng trống
GRAB = (27.4, 28.0)             # túm sợi dây leo ở thành cầu sát cửa (tay gần), giữ chặt
PHICH = 28.6                    # buông dây, ngã ngồi lùi về bậc cửa phủ rêu, đáp lên đuôi bông: PHỊCH!

# --- chú chim, "rất cũ"
BIRD_LAND = (30.05, 30.75)      # chú chim lúc sáng đáp xuống cột cầu
BIRD_LOOK = 30.9                # nghiêng đầu nhìn Lumo
BIRD_LAUGH = (31.4, 33.0)       # lấy cánh vỗ bụng: CHÍP CHÍP CHÍP!
CHIRPS = (31.5, 32.1, 32.7)     # ba cú vỗ bụng, mỗi cú một tiếng CHÍP
LINE_VERY_OLD = (33.6, 35.8)    # LUMO: Được rồi! Một chiếc cầu… rất cũ!
LOOK_COMPASS = 36.0             # nâng la bàn lên nhìn

# --- nhìn kỹ, lối nhỏ
STAND_UP = (38.7, 39.2)         # đứng dậy
LOOK_GAP = (39.3, 39.9)         # nhìn khoảng trống dài trước mặt
LOOK_WALL = (40.0, 40.6)        # nhìn vách đá
LOOK_BUSH = (40.7, 41.3)        # nhìn bụi cây bên cạnh cửa
TO_BUSH = (41.4, 41.9)          # bước tới bụi cây
PART_BUSH = (42.0, 42.6)        # vạch bụi cây: những bậc đá rộng hiện ra, giữ hình tới hết S12
BIRD_STOP = 44.6                # chú chim còn khúc khích nửa giây đầu S13 rồi thôi cười, nghiêng đầu
LINE_LOOK = (46.0, 47.4)        # LUMO: Nhìn kỹ trước đã.
STOW_COMPASS = (48.0, 48.6)     # cất la bàn vào túi da
GRAB_RAIL = (48.7, 49.0)        # bám tay vịn dây leo
CLIMB = (49.1, 52.6)            # đi chậm từng bậc lên lối nhỏ (5 bậc, mỗi bậc 0.7 s)
BIRD_FOLLOW = 50.0              # chú chim bay từ cột cầu xuống bậc đầu, rồi nhảy từng bậc theo sau, bắt chước bước chậm
PATH_WALK = (52.8, 56.5)        # đi chậm dọc gờ vách, vòng qua đầu khe, xuống bậc (lược nửa đầu gờ)
BEEPS_PATH = (54.4, 55.3, 56.0, 56.6, 57.0, 57.3, 57.55, 57.75, 57.95)   # la bàn trong túi kêu mỗi lúc một dày
ARRIVE = (56.6, 58.4)           # bước xuống hai bậc cuối, từng bước đi tới trước bệ đá (không lao)

# --- bệ đá, bản đồ khắc
PRESS_STAR = (58.5, 59.25)      # với tay ấn ngôi sao đá
CACH = 59.25                    # ngôi sao lún xuống: CẠCH!
SLAB_SLIDE = (59.9, 60.8)       # phiến đá trên mặt bệ trượt mở, lộ bản đồ khắc
BIRD_PERCH = (61.7, 62.2)       # chú chim đậu lên mép bệ
MAP_OUT = (62.5, 63.2)          # rút tấm bản đồ giấy ra, cầm ngang ngực (lại cầm ngược)
MAP_TURN = (65.8, 66.4)         # xoay nửa vòng: khớp
CAM_EDGE = (66.9, 67.9)         # máy tới gần mép phải hai bản đồ
CAM_PAN = (67.9, 71.6)          # lia từ đài thiên văn khắc tới khung có cả đài khắc và góc mây trống trên bản đồ giấy, giữ
OBS_FLASH = (71.8, 73.1)        # đài thiên văn khắc lóe xanh ngọc rồi tắt (trọn trong S21)
BEEPS_FLASH = (71.85, 72.1, 72.35)   # cùng lúc, la bàn trong túi rung: TÍT TÍT TÍT
COMPASS_OUT2 = (73.95, 74.45)     # rút la bàn ra (vẫn sáng mạnh)
NEEDLE_ISLAND = (75.3, 76.1)    # mũi sao rời ngôi sao đá, quay về hòn đảo khắc ở rìa bản đồ
NEEDLE_HORIZON = (76.8, 77.6)   # rồi chỉ thẳng ra chân trời
DIM = (77.8, 78.4)              # la bàn dịu xuống, chỉ còn sáng le lói
LINE_ISLAND = (79.3, 82.0)      # LUMO: Chưa từng có hòn đảo này trên bản đồ của mình!
BIRD_FLY = (82.6, 84.0)         # chú chim vỗ cánh bay đi

# Mỗi dòng hiện từ lúc việc xảy ra, khoảng 20 ký tự mỗi giây trở xuống
CC = [
    (0.1, 1.9, "[cánh cửa mở hẳn]"),
    (1.9, 3.6, "[hình mây trên cửa tắt dần]"),
    (3.8, 6.2, "[cầu ván cổ bắc qua khe núi]"),
    (6.2, 8.8, "[lưới dây leo đan kín dưới cầu]"),
    (BEEPS_BAG[0], COMPASS_OUT[0], "[trong túi da: TÍT… TÍT…]"),
    (COMPASS_OUT[0], 12.6, "[la bàn sáng le lói]"),
    (12.6, 14.8, "[mũi sao chỉ ngôi sao đá bên kia cầu]"),
    (POSE[0], LINE_AHEAD[0], "[dựng tai, chìa la bàn]"),
    (LINE_AHEAD[0], LINE_AHEAD[1], "LUMO: Ngay phía trước!"),
    (RUSH[0], CREAK, "[lao lên cầu]"),
    (CREAK, WAIT_PEBBLE[0] + 0.2, "[CREAAAAK]"),
    (WAIT_PEBBLE[0] + 0.2, NO_PEBBLE, "[cụp tai, ngước trời chờ sỏi]"),
    (NO_PEBBLE, LINE_OLD[0], "[không có sỏi]"),
    (LINE_OLD[0], LINE_OLD[1], "LUMO: Không sao. Một chiếc cầu hơi cũ thôi."),
    (STEP_ON[0] - 0.1, CRACK, "[vẫn ngước, bước tiếp]"),
    (CRACK, GRAB[0], "[CRACK! Cả dãy ván rơi xuống lưới]"),
    (GRAB[0], GRAB[1] + 0.4, "[túm dây leo]"),
    (PHICH, 30.0, "[đáp lên đuôi bông: PHỊCH!]"),
    (BIRD_LAND[0], BIRD_LAUGH[0], "[chú chim đáp xuống]"),
    (BIRD_LAUGH[0], BIRD_LAUGH[1] + 0.2, "[chim vỗ bụng: CHÍP CHÍP CHÍP!]"),
    (LINE_VERY_OLD[0], LINE_VERY_OLD[1], "LUMO: Được rồi! Một chiếc cầu… rất cũ!"),
    (36.4, 38.6, "[mũi sao vẫn chỉ ngôi sao đá]"),
    (LOOK_GAP[0], LOOK_BUSH[1], "[nhìn khoảng trống, vách đá, bụi cây]"),
    (PART_BUSH[0], 44.0, "[vạch bụi cây: lối bậc đá]"),
    (BIRD_STOP, 45.8, "[chim thôi cười]"),
    (LINE_LOOK[0], LINE_LOOK[1], "LUMO: Nhìn kỹ trước đã."),
    (STOW_COMPASS[0], CLIMB[0] + 0.1, "[cất la bàn, bám tay vịn]"),
    (CLIMB[0] + 0.1, 50.4, "[đi chậm từng bậc]"),
    (50.5, 52.8, "[chim bắt chước bước chậm]"),
    (52.9, BEEPS_PATH[0], "[men vách, vòng qua đầu khe]"),
    (BEEPS_PATH[0], BEEPS_PATH[3], "[trong túi da: TÍT… TÍT…]"),
    (BEEPS_PATH[3], PRESS_STAR[0], "[kêu dày dần: TÍT TÍT TÍT!]"),
    (PRESS_STAR[0], CACH, "[ấn ngôi sao]"),
    (CACH, SLAB_SLIDE[0], "[CẠCH!]"),
    (SLAB_SLIDE[0], 61.6, "[phiến đá trượt mở: bản đồ khắc]"),
    (BIRD_PERCH[0] - 0.05, MAP_OUT[0] + 0.4, "[chú chim đậu lên mép bệ]"),
    (MAP_OUT[0] + 0.4, 64.3, "[rút bản đồ giấy ra]"),
    (64.3, MAP_TURN[0] - 0.1, "[không khớp: rương lộn ngược]"),
    (MAP_TURN[0], MAP_TURN[0] + 1.4, "[xoay lại: khớp]"),
    (CAM_EDGE[1], CAM_PAN[0] + 1.8, "[rìa bản đồ khắc: đài thiên văn]"),
    (CAM_PAN[0] + 1.8, OBS_FLASH[0], "[bản đồ giấy: trống trơn]"),
    (OBS_FLASH[0], 73.4, "[đài khắc lóe: TÍT TÍT TÍT]"),
    (73.4, NEEDLE_ISLAND[0], "[rút la bàn ra]"),
    (NEEDLE_ISLAND[0], NEEDLE_HORIZON[0], "[mũi sao về đảo khắc]"),
    (NEEDLE_HORIZON[0], DIM[0] + 0.3, "[rồi chỉ ra chân trời]"),
    (DIM[0] + 0.3, 79.2, "[la bàn dịu, sáng le lói]"),
    (LINE_ISLAND[0], LINE_ISLAND[1], "LUMO: Chưa từng có hòn đảo này trên bản đồ của mình!"),
    (BIRD_FLY[0], BIRD_FLY[0] + 1.4, "[chú chim bay đi]"),
]
