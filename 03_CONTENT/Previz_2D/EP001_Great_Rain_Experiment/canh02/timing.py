"""Mốc thời gian và CC của Cảnh 2 tập 01: Gadget Action, lắp máy (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh.
Kịch bản: 03_CONTENT/Scripts/EP001_great_rain_experiment.fountain, cảnh #2#."""
FPS, SECONDS = 24, 86.6
SHOTS = [
    ("S1", 0.0, 3.0),     # toàn đỉnh đồi trọc trên vườn mầm; cả nhóm tới, Tavi hạ Inventor Pack xuống đất
    ("S2", 3.0, 7.4),     # Tavi bật khoá, Inventor Pack bung đồ như hoa nở; một con ốc bay vèo lên trời, rơi trúng hộp ốc: TINH!
    ("S3", 7.4, 11.8),    # Tavi vặn ốc, gõ búa, nối ống đồng; lắp ngược một tấm, tháo ra, lắp lại
    ("S4", 11.8, 15.9),   # Tavi chìa tay xin cờ lê, Lumo dúi cái búa; Tavi lặng lẽ đặt búa xuống, nhặt cờ lê
    ("S5", 15.9, 18.4),   # Nori xếp ốc theo cỡ: to, vừa, nhỏ
    ("S6", 18.4, 24.4),   # Piko ngồi phịch lên hộp ốc, ốc dính lên thân; Nori rũ cánh; Tavi gỡ ốc PÓC PÓC PÓC, Nori xếp lại
    ("S7", 24.4, 26.9),   # toàn: máy đã thành hình, vòm kính nằm dưới đất có ổ bánh răng còn trống
    ("S8", 26.9, 30.9),   # Tavi lục hộp đồ, cau mày: "Thiếu đúng một bánh răng."
    ("S9", 30.9, 34.8),   # Piko thò tay vào túi "giúp", rút ra con vịt ngậm bánh răng vàng
    ("S10", 34.8, 41.3),  # cận vòm kính: Tavi kéo kính xuống soi bánh răng, mở cửa nhỏ, lắp vào: CẠCH, đóng cửa, đẩy kính lên
    ("S11", 41.3, 42.5),  # Lumo mải ngắm máy; la bàn rung khẽ trong túi da
    ("S12", 42.5, 44.3),  # cận la bàn ló khỏi túi da, ngôi sao xoay về vòm kính có bánh răng vàng (dựng riêng ở X = 60)
    ("S13", 44.3, 46.5),  # Piko ôm chặt con vịt: "Để dành!"
    ("S14", 46.5, 50.9),  # Lumo chộp cái móc, móc vội vào mép vòm, chạy vòng sang nắm đầu dây: "Để tớ kéo lên!"
    ("S15", 50.9, 56.2),  # Lumo chạy lùi, vòm vọt lên nghiêng hẳn, chao đảo trên nóc; "Khoan! Lệch rồi!"; thả dây: BỊCH
    ("S16", 56.2, 58.2),  # Nori đưa Story Lens lên mắt
    ("S17", 58.2, 60.4),  # cận mặt kính: hình cái bập bênh, cân bằng ở điểm giữa (dựng riêng ở X = 50)
    ("S18", 60.4, 63.8),  # Nori nhìn bập bênh, nhìn vòm kính, chỉ điểm giữa đỉnh vòm: "Chỗ này mới cân."
    ("S19", 63.8, 65.3),  # cận vòm kính: tay Tavi dời cái móc từ mép vòm tới giữa đỉnh vòm (dựng riêng ở X = 70)
    ("S20", 65.3, 69.0),  # toàn: Lumo kéo lại, vòm lên thẳng tắp, đáp xuống nóc máy: KHỚP!; Nori ngó xuống chân đồi
    ("S21", 69.0, 71.8),  # Wonder Hub dưới chân đồi, qua ô cửa tròn thấy cổng truyện đang khép, le lói sáng (dựng riêng ở X = 40)
    ("S22", 71.8, 73.4),  # toàn: Tavi trước máy chỉ núm; xa xa dưới chân đồi cổng truyện vẫn le lói
    ("S23", 73.4, 75.4),  # trung hông trái máy: Tavi chỉ cần gạt
    ("S24", 75.4, 79.2),  # Tavi chỉ nút đỏ to: "Còn nút đỏ là MAX POWER. Mưa to hết cỡ!"
    ("S25", 79.2, 82.0),  # nút đỏ bóng loáng; mắt Piko lấp lánh theo, tay Piko lần tới… khựng
    ("S26", 82.0, 84.0),  # Lumo, Tavi, Nori: "Không chạm nút đỏ!"
    ("S27", 84.0, 86.6),  # Piko rụt tay, giấu ra sau lưng, cười toe
]
END = {name: t1 for name, _, t1 in SHOTS}

# --- montage lắp máy
ARRIVE = (0.2, 2.2)             # cả nhóm lên tới đỉnh đồi; Lumo chạy ra mép đồi nhìn xuống vườn mầm
PACK_DOWN = 2.4                 # Tavi hạ Inventor Pack xuống đất
TAVI_OPEN = 3.1                 # Tavi cúi xuống bật khoá ba lô
PACK_OPEN = (3.4, 4.5)          # nắp bật, dụng cụ, ống đồng, tấm kim loại bung ra như hoa nở
SCREW_UP = (4.9, 5.4)           # một con ốc bắn vèo lên trời
SCREW_IN = 6.1                  # con ốc rơi đúng vào hộp ốc: TINH!
TAVI_SCREW = (7.5, 8.1)         # Tavi vặn ốc
HAMMER = (8.2, 8.8)             # gõ búa: CỐC CỐC
PIPE = (8.9, 9.4)               # nối ống đồng
PLATE_WRONG = (9.5, 11.7)       # lắp ngược một tấm, nghiêng đầu, tháo ra, lật lại, lắp lại
TAVI_ASK = (12.0, 12.8)         # Tavi mắt vẫn nhìn máy, chìa tay ra sau xin cờ lê
LUMO_HAMMER = (12.8, 13.4)      # Lumo hăm hở dúi cái búa vào tay Tavi
TAVI_SWAP = (13.6, 15.7)        # Tavi nhìn cái búa, mặt tỉnh bơ, lặng lẽ đặt xuống, nhặt cờ lê, làm tiếp
NORI_SORT = (16.0, 18.2)        # Nori xếp ốc gọn gàng: hàng to, hàng vừa, hàng nhỏ
PIKO_SIT = (18.5, 19.3)         # Piko nảy tới, ngồi phịch lên hộp ốc
PIKO_UP = (19.8, 20.4)          # Piko đứng dậy: ốc dính lốm đốm ngoài thân thạch
NORI_DROOP = (20.4, 21.8)       # Nori nhìn hộp ốc trống trơn, cánh rũ xuống
POPS = (22.1, 22.7, 23.3)       # Tavi gỡ từng con ốc khỏi Piko: PÓC. PÓC. PÓC. Mỗi con bay sang tay Nori
NORI_RESORT = (22.1, 24.2)      # Nori lặng lẽ xếp lại từ đầu
MACHINE_DONE = (24.5, 26.7)     # máy thành hình: thân tròn ú, bốn chân, núm, đồng hồ, nút đỏ, cần gạt, vòi, giá ba chân có ròng rọc

# --- bánh răng
TAVI_RUMMAGE = (27.1, 28.5)     # Tavi lục hộp đồ. Lục nữa. Cau mày.
TAVI_MISS = (28.7, 30.3)        # TAVI: Thiếu đúng một bánh răng.
PIKO_HELP = (31.1, 32.3)        # Piko thò tay vào túi "giúp", lục lọi
DUCK_OUT = 32.4                 # rút ra một con vịt cao su
TAVI_PUZZLE = (32.5, 33.0)      # Tavi ngơ ngác nhìn con vịt
GEAR_GLINT = (33.0, 33.6)       # mỏ vịt ngậm bánh răng vàng lấp lánh; Tavi mừng rỡ
TAVI_TAKE = (33.9, 34.5)        # Tavi gỡ bánh răng khỏi mỏ vịt
GOGGLES_DOWN = (35.0, 35.4)     # Tavi kéo kính bảo hộ xuống
INSPECT = (35.5, 36.8)          # soi bánh răng, xoay xoay, gật gù
HATCH_OPEN = (36.9, 37.3)       # mở cửa nhỏ trên vòm kính
GEAR_IN = (37.7, 38.4)          # lắp bánh răng vào ổ cạnh lõi tinh thể
CLICK = 38.4                    # vừa khít: CẠCH
HATCH_CLOSE = (39.5, 39.9)      # đóng cửa
GOGGLES_UP = (40.2, 40.6)       # đẩy kính lên lại
COMPASS_PEEK = (41.5, 44.1)     # la bàn rung khẽ: TÍT, ló khỏi miệng túi da; Lumo mải ngắm máy
STAR_TURN = (42.7, 43.4)        # ngôi sao xoay về vòm kính
DOME_GLINT = 43.5               # bánh răng vàng trong vòm lóe sáng
PIKO_HUG = (44.4, 44.9)         # Piko ôm chặt con vịt vào lòng
PIKO_LINE = (45.0, 46.0)        # PIKO: Để dành!

# --- ròng rọc
HOOK_GRAB = (46.7, 47.3)        # Lumo nhún nhảy chộp cái móc ròng rọc
HOOK_ON = (47.5, 48.3)          # móc vội vào mép vòm kính, mắt còn nhìn lên nóc máy
LUMO_TO_ROPE = (48.4, 49.2)     # chạy vòng sang bên kia máy, nắm đầu dây bằng hai tay ngang ngực
LUMO_LINE = (49.3, 50.6)        # LUMO: Để tớ kéo lên!
LUMO_RUN = (51.0, 52.3)         # Lumo chạy lùi phăng phăng
DOME_UP = (51.1, 52.5)          # vòm kính vọt lên, nghiêng hẳn sang một bên
DOME_WOBBLE = (52.5, 54.4)      # chao đảo trên nóc máy
TAVI_STOP = (52.7, 54.1)        # TAVI: Khoan! Lệch rồi!
DROP = (54.5, 55.0)             # Lumo thả dây, vòm hạ xuống đất: BỊCH
LENS_UP = (56.4, 57.0)          # Nori đưa Story Lens lên mắt
LENS_IMAGE = (58.4, 59.0)       # trong mặt kính hiện hình cái bập bênh
LENS_BALANCE = 59.4             # bập bênh nằm thăng bằng, điểm tựa ở giữa sáng lên
NORI_COMPARE = (60.5, 61.6)     # Nori nhìn bập bênh, nhìn vòm kính
NORI_POINT = (61.6, 62.1)       # chỉ một điểm trên khung: giữa đỉnh vòm
NORI_LINE = (62.2, 63.6)        # NORI: Chỗ này mới cân.
HOOK_MOVE = (64.0, 65.0)        # Tavi dời cái móc tới đúng chỗ Nori chỉ
LIFT2 = (65.5, 67.5)            # Lumo kéo lại, vòm kính lên thẳng tắp
FIT = 67.7                      # đáp xuống nóc máy: KHỚP!
NORI_LOOK_DOWN = 68.4           # Nori ngó xuống chân đồi

# --- Wonder Hub, giới thiệu máy, nút đỏ
HUB_GLOW = (69.0, SECONDS)      # cổng truyện trong Wonder Hub đang khép, le lói sáng
KNOB_POINT = 72.0               # Tavi chỉ núm NHẸ
LEVER_POINT = 73.6              # Tavi chỉ cần gạt TẮT
TAVI_INTRO = (72.0, 74.8)       # TAVI: Núm này: mưa nhẹ. Cần này: tắt.
BUTTON_POINT = 75.6             # Tavi chỉ nút đỏ to
TAVI_MAX = (75.7, 78.6)         # TAVI: Còn nút đỏ là MAX POWER. Mưa to hết cỡ!
RAIN_GESTURE = (77.3, 78.6)     # "Mưa to hết cỡ!": giơ hai tay rồi rung mười ngón rơi mạnh xuống
BUTTON_GLINT = (79.4, 80.0)     # nút đỏ bóng loáng trong nắng
PIKO_EYES = (79.6, 81.9)        # mắt Piko lấp lánh theo
PIKO_CREEP = (79.8, 81.4)       # thân thạch vươn cao, tay Piko từ từ lần tới… khựng trước câu hô
SHOUT = (82.1, 83.9)            # LUMO, TAVI, NORI: Không chạm nút đỏ!
PIKO_HIDE = (84.1, 84.6)        # Piko rụt tay, giấu ra sau lưng
PIKO_TOOTHY = (84.6, 86.4)      # cười toe

# Mỗi dòng hiện từ lúc việc xảy ra, khoảng 20 ký tự mỗi giây trở xuống
CC = [
    (0.3, 2.9, "[đỉnh đồi trọc trên vườn mầm]"),
    (PACK_OPEN[0] - 0.2, SCREW_UP[0], "[Inventor Pack bung đồ như hoa nở]"),
    (SCREW_UP[0], SCREW_IN, "[con ốc bay vèo…]"),
    (SCREW_IN, END["S2"], "[…rơi trúng hộp ốc: TINH!]"),
    (TAVI_SCREW[0], HAMMER[0], "[Tavi vặn ốc]"),
    (HAMMER[0], PLATE_WRONG[0], "[CỐC CỐC; nối ống đồng]"),
    (PLATE_WRONG[0], END["S3"], "[lắp ngược một tấm, tháo ra, lắp lại]"),
    (TAVI_ASK[0] - 0.1, LUMO_HAMMER[0], "[Tavi xin cờ lê…]"),
    (LUMO_HAMMER[0], END["S4"], "[…Lumo dúi cái búa; Tavi lặng lẽ đổi lại]"),
    (NORI_SORT[0], END["S5"], "[Nori xếp ốc: to, vừa, nhỏ]"),
    (PIKO_SIT[0] + 0.5, PIKO_UP[1], "[Piko ngồi phịch lên hộp ốc]"),
    (PIKO_UP[1], POPS[0], "[ốc dính khắp Piko]"),
    (PIKO_UP[1], POPS[0], "[Nori rũ cánh]"),
    (POPS[0], END["S6"], "[Tavi gỡ ốc: PÓC. PÓC. PÓC.]"),
    (NORI_RESORT[0], END["S6"], "[Nori xếp lại]"),
    (MACHINE_DONE[0], END["S7"], "[máy làm mưa đã thành hình]"),
    (TAVI_RUMMAGE[0], TAVI_MISS[0], "[Tavi lục hộp đồ, cau mày]"),
    (TAVI_MISS[0], TAVI_MISS[1], "TAVI: Thiếu đúng một bánh răng."),
    (PIKO_HELP[0], DUCK_OUT, '[Piko lục túi "giúp"…]'),
    (DUCK_OUT, END["S9"], "[…ra con vịt cao su ngậm bánh răng vàng]"),
    (GOGGLES_DOWN[0], HATCH_OPEN[0], "[Tavi kéo kính xuống, soi bánh răng]"),
    (HATCH_OPEN[0], CLICK, "[mở cửa nhỏ vòm kính…]"),
    (CLICK, HATCH_CLOSE[0], "[…lắp vừa khít: CẠCH]"),
    (HATCH_CLOSE[0], END["S10"], "[đóng cửa, đẩy kính lên]"),
    (COMPASS_PEEK[0], STAR_TURN[0] + 0.2, "[la bàn rung: TÍT]"),
    (STAR_TURN[0] + 0.2, END["S12"], "[sao chỉ về vòm kính]"),
    (PIKO_HUG[0], PIKO_LINE[1], "[Piko ôm chặt con vịt]"),
    (PIKO_LINE[0], PIKO_LINE[1], "PIKO: Để dành!"),
    (HOOK_GRAB[0] - 0.1, LUMO_TO_ROPE[0], "[Lumo chộp móc, móc vội vào mép vòm]"),
    (LUMO_TO_ROPE[1] - 0.3, LUMO_LINE[1], "[nắm đầu dây]"),
    (LUMO_LINE[0], LUMO_LINE[1], "LUMO: Để tớ kéo lên!"),
    (DOME_UP[0], TAVI_STOP[0], "[vòm kính vọt lên, nghiêng hẳn]"),
    (TAVI_STOP[0], TAVI_STOP[1], "TAVI: Khoan! Lệch rồi!"),
    (DROP[0], END["S15"], "[Lumo thả dây; vòm hạ xuống: BỊCH]"),
    (LENS_UP[0], END["S16"], "[Nori đưa Story Lens lên mắt]"),
    (LENS_IMAGE[0] + 0.1, END["S17"], "[trong mặt kính: cái bập bênh]"),
    (NORI_COMPARE[0], NORI_LINE[0], "[nhìn bập bênh, nhìn vòm kính]"),
    (NORI_LINE[0], NORI_LINE[1], "NORI: Chỗ này mới cân."),
    (HOOK_MOVE[0], END["S19"], "[Tavi dời cái móc]"),
    (LIFT2[0], FIT, "[Lumo kéo lại: vòm lên thẳng tắp]"),
    (FIT, END["S20"], "[KHỚP!]"),
    (HUB_GLOW[0] + 0.1, END["S21"], "[chân đồi: Wonder Hub, cổng truyện le lói]"),
    (TAVI_INTRO[0], TAVI_INTRO[1], "TAVI: Núm này: mưa nhẹ. Cần này: tắt."),
    (TAVI_MAX[0], TAVI_MAX[1], "TAVI: Còn nút đỏ là MAX POWER. Mưa to hết cỡ!"),
    (BUTTON_GLINT[0], END["S25"], "[nút đỏ lấp lánh; tay Piko lần tới…]"),
    (SHOUT[0], SHOUT[1], "LUMO, TAVI, NORI: Không chạm nút đỏ!"),
    (PIKO_HIDE[0], SECONDS, "[Piko rụt tay, giấu sau lưng, cười toe]"),
]
