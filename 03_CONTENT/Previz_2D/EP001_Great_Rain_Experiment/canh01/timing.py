"""Mốc thời gian và CC của Cảnh 1 tập 01: Hook + Discovery (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh.
Kịch bản: 03_CONTENT/Scripts/EP001_great_rain_experiment.fountain, cảnh #1#."""
FPS, SECONDS = 24, 55.0
SHOTS = [
    ("S1", 0.0, 3.9),     # cận lá khô và giọt sương: lấp lánh, lăn… dừng… lăn… dừng; mắt Piko bám theo, bông hoa vươn lên chờ
    ("S2", 3.9, 9.6),     # Piko, bông hoa, chiếc lá: giọt lăn nốt tới đầu lá, trĩu xuống, Piko nảy lên đớp, hoa gục, Piko cười trừ
    ("S3", 9.6, 13.4),    # toàn cảnh thung lũng khô, tên phim, Nori bay ngang
    ("S4", 13.4, 19.8),   # Nori rọi mầm cây, sinh vật nhỏ thở dài, Lumo bật dậy
    ("S5", 19.8, 26.4),   # Lumo lao đi, vấp, treo trên vết nứt, Tavi kéo lại; la bàn rung, Piko quay sang
    ("S6", 26.4, 28.8),   # cận la bàn: ngôi sao quay loạn rồi chỉ về phía túi, miệng túi lóe ánh vàng
    ("S7", 28.8, 30.8),   # Lumo và Piko: "Có gì lạ kìa!"
    ("S8", 30.8, 35.55),  # Piko: lục túi, rút ra cái thìa, liếc hoa, đào; nhát thứ ba làm cán thìa gập
    ("S9", 35.55, 37.5),  # cận Piko và cái thìa cong: rung bần bật, giơ thìa lên nhìn, chớp mắt, đặt xuống đất
    ("S10", 37.5, 39.7),  # cận la bàn kề cái thìa: sao giật về thìa rồi quay lại chỉ túi
    ("S11", 39.7, 44.85),  # Lumo cúi cạnh thìa, đứng dậy: "Thìa thôi mà?", Tavi dậm thử đất cứng, ngước nhìn chiếc lá
    ("S12", 44.85, 47.7),  # theo mắt Tavi: cận chiếc lá còn ướt sương lấp lánh, lia lên dải mây bám đỉnh đồi
    ("S13", 47.7, 52.3),  # Tavi "à!", quay sang Lumo, minh hoạ cách làm mưa bằng tay
    ("S14", 52.3, 55.0),  # toàn: Tavi bước lên chỉ đỉnh đồi, cả nhóm ngước theo
]

# --- Hook
DEW_GLINT = (0.3, 5.4)          # giọt sương cuối cùng lấp lánh ở đầu chiếc lá khô, tới lúc rơi
PIKO_STARE = (0.8, 5.3)         # Piko và bông hoa ngửa lên chờ
DEW_ROLL = (1.6, 5.4)           # giọt sương lăn… dừng… lăn… dừng… lăn tới đầu lá, trĩu xuống
PIKO_JUMP = (5.3, 6.0)          # Piko nén người, nảy lên đớp
SLURP = 5.65                    # Piko đớp gọn giọt sương
FLOWER_DROOP = (6.3, 7.0)       # bông hoa gục xuống
PIKO_LICK = (7.0, 7.4)          # Piko liếm môi
PIKO_LOOK_FLOWER = (7.5, 8.1)   # Piko nhìn bông hoa
PIKO_GRIN = (8.1, 9.4)          # Piko co người cười trừ, gãi má, toát mồ hôi
PIKO_GRIN_GLANCE = (8.5, 9.0)   # giữa hai lần cười, mở mắt nhìn bông hoa gục
TITLE = (10.0, 13.0)            # tên phim
NORI_FLY_IN = (10.5, 13.6)      # Nori bay ngang khung khi tên phim đang hiện

# --- Discovery
NORI_LIGHT = (13.8, 19.8)       # Nori rọi sáng lên một mầm cây gầy nhom
CRITTER_SIGH = (14.0, 15.1)     # sinh vật nhỏ trong vườn thở dài, chiếc lá trên đầu trễ xuống che mắt
NORI_LINE = (15.2, 17.2)        # NORI: Mầm cây sắp héo khô hết rồi.
LUMO_SPRING = (17.6, 18.1)      # Lumo bật dậy
LUMO_LINE = (18.3, 19.7)        # LUMO: Đi tìm nước cho vườn!
LUMO_DASH = (19.9, 20.7)        # Lumo lao đi: một bước, hai bước
LUMO_TRIP = 20.7                # vấp vết nứt
LUMO_STUMBLE = (20.7, 21.2)     # chúi người, tay chới với
TAVI_LUNGE = (20.75, 21.2)      # Tavi lao tới, chụp quai túi da của Lumo
LUMO_DANGLE = (21.2, 22.2)      # Lumo treo chúi trên vết nứt, mắt tròn nhìn xuống; Nori lo lắng nhìn theo
LUMO_PULLED = (22.2, 22.8)      # Tavi kéo Lumo đứng lại, Nori thở phào
TAVI_LINE = (22.9, 24.3)        # TAVI: Coi chừng vết nứt!
TAVI_STEP_BACK = (24.4, 25.0)   # Tavi lùi ra chỗ trống
COMPASS_BUZZ = (24.5, 25.8)     # la bàn rung trong túi da: TÍT TÍT TÍT
PIKO_TURN = 25.0                # Piko nghe tiếng TÍT, quay sang phía Lumo
COMPASS_OUT = (25.8, 26.4)      # Lumo rút la bàn ra, cầm hai tay
STAR_SPIN = (26.6, 27.7)        # ngôi sao quay loạn… rồi dừng, mũi sao chỉ về phía túi của Piko
LUMO_LINE2 = (28.9, 30.1)       # LUMO: Có gì lạ kìa!
PIKO_CHECK = 29.5               # Piko ngó xuống cái túi của mình
PIKO_RUMMAGE = (30.2, 31.5)     # Piko thò tay vào túi đeo chéo bên hông, lục lọi
SPOON_OUT = 31.6                # rút ra một chiếc thìa
PIKO_LOOK = (32.0, 33.6)        # nhìn thìa, liếc bông hoa gục, nhìn đất
PIKO_GLANCE_FLOWER = (32.5, 32.9)  # liếc bông hoa gục, giữ một nhịp
PIKO_LOOK_GROUND = (32.9, 33.2)    # cúi nhìn đất, quyết tâm
DIG = (33.9, 34.5, 35.2)        # CỘP. CỘP. CỘP! (nhát thứ ba làm cán thìa gập)
PIKO_SHAKE = (35.2, 36.2)       # cán thìa cong vòng, thân thạch rung bần bật, giơ thìa cong lên nhìn
PIKO_BLINK = (36.3, 36.9)       # nhìn cái thìa cong trước mắt, chớp mắt
PIKO_SET_SPOON = (37.0, 37.4)   # Piko đặt cái thìa cong xuống đất, xa cái túi
STAR_STILL = (37.5, 39.7)       # Lumo bước tới, cúi xuống cạnh cái thìa; ngôi sao la bàn vẫn chỉ vào túi của Piko
LUMO_TEST = (37.8, 38.4)        # Lumo hạ la bàn kề sát cái thìa: mũi sao giật về thìa, rồi quay lại chỉ túi
NEEDLE_TO_SPOON = 38.0           # mũi sao giật về cái thìa, giữ tới hết LUMO_TEST
TAVI_STEP_IN = (39.7, 40.3)     # Tavi bước lại gần xem cái thìa cong
LUMO_PUZZLE = (39.8, 41.3)      # Lumo đứng dậy, nhìn thìa, nhìn la bàn, nghiêng đầu
LUMO_STAND = (40.1, 40.4)         # Lumo đứng thẳng dậy, mắt còn trên cái thìa
LUMO_LOOK_COMPASS = (40.4, 40.8)  # cúi nhìn la bàn
LUMO_TILT = (40.9, 41.15)         # nghiêng đầu
LUMO_LINE3 = (41.4, 42.6)       # LUMO: Thìa thôi mà?
PIKO_BLINK2 = 42.9              # Piko chớp mắt nhìn Lumo
TAVI_KNOCK = (43.4, 44.4)       # Tavi dậm thử mặt đất nứt: CỘC CỘC, cứng như đá, đào không ra nước
TAVI_STAMPS = (43.7, 44.1)        # hai cú dậm chạm đất: CỘC, CỘC
TAVI_LOOK_LEAF = (44.4, 45.7)   # Tavi ngước nhìn chiếc lá còn ướt sương (hơi nước gặp lạnh thành giọt), lá lấp lánh
TAVI_LOOK_UP = (45.7, 46.7)     # máy lia theo mắt Tavi lên đỉnh đồi có dải mây mỏng bám (trên cao lạnh hơn), giữ trên mây
TAVI_IDEA = (47.7, 48.6)        # mắt Tavi sáng lên: "à!", quay phắt sang Lumo, nhún bật, giơ ngón tay
TAVI_SNAP = (47.95, 48.15)        # đầu còn ngước lên đồi, rồi quay phắt sang Lumo, nhún, giơ ngón tay
TAVI_GATHER = (48.6, 49.8)      # TAVI (chụm hai tay như gom): Gom hơi nước,
TAVI_SHIVER = (49.8, 51.0)      # (ôm vai, rùng mình) làm lạnh,
TAVI_RAIN = (51.0, 52.2)        # (rung mười ngón tay rơi xuống) sẽ có mưa!
TAVI_POINT = (52.3, 54.5)       # (chỉ lên đỉnh đồi) Lên đỉnh đồi, trên đó lạnh hơn!
TAVI_STRIDE = (52.3, 52.8)        # Tavi sải bước lên trước Lumo, rồi mới quay chỉ đỉnh đồi
GROUP_LOOK = 53.0               # cả nhóm ngước theo tay Tavi

# Mỗi dòng hiện từ lúc việc xảy ra, khoảng 20 ký tự mỗi giây trở xuống; dòng hành động nối liền dòng sau
CC = [
    (0.3, 2.8, "[giọt sương cuối cùng lấp lánh trên lá khô]"),
    (2.8, DEW_ROLL[1], "[Piko và bông hoa chờ; giọt sương lăn…]"),
    (SLURP, FLOWER_DROOP[0] + 0.3, "[Piko đớp: SLURP!]"),
    (FLOWER_DROOP[0] + 0.3, PIKO_LICK[1], "[hoa gục xuống]"),
    (PIKO_LICK[1], PIKO_GRIN[1], "[Piko liếm môi, nhìn hoa, cười trừ]"),
    (TITLE[0], TITLE[1], "[Thung lũng Mây khô nứt nẻ]"),
    (NORI_LIGHT[0], NORI_LINE[0], "[Nori rọi mầm cây gầy nhom]"),
    (NORI_LINE[0], NORI_LINE[1], "NORI: Mầm cây sắp héo khô hết rồi."),
    (LUMO_SPRING[0], LUMO_LINE[0], "[Lumo bật dậy]"),
    (LUMO_LINE[0], LUMO_LINE[1], "LUMO: Đi tìm nước cho vườn!"),
    (LUMO_DASH[0], LUMO_TRIP, "[Lumo lao đi…]"),
    (LUMO_TRIP, LUMO_DANGLE[1], "[…vấp vết nứt!]"),
    (LUMO_DANGLE[1], TAVI_LINE[0], "[Tavi kéo lại]"),
    (TAVI_LINE[0], TAVI_LINE[1], "TAVI: Coi chừng vết nứt!"),
    (COMPASS_BUZZ[0], COMPASS_OUT[0], "[la bàn rung: TÍT TÍT TÍT]"),
    (COMPASS_OUT[0], STAR_SPIN[0], "[rút la bàn ra]"),
    (STAR_SPIN[0], STAR_SPIN[1], "[ngôi sao quay loạn…]"),
    (STAR_SPIN[1], LUMO_LINE2[0], "[…chỉ về túi Piko]"),
    (LUMO_LINE2[0], LUMO_LINE2[1], "LUMO: Có gì lạ kìa!"),
    (PIKO_RUMMAGE[0], SPOON_OUT, "[Piko lục túi bên hông…]"),
    (SPOON_OUT, PIKO_LOOK[0] + 0.6, "[…ra một chiếc thìa]"),
    (PIKO_LOOK[0] + 0.6, DIG[0], "[Piko nhìn hoa, nhìn đất]"),
    (DIG[0], DIG[2] + 0.1, "[Piko đào: CỘP. CỘP. CỘP!]"),
    (DIG[2] + 0.1, PIKO_BLINK[0], "[thìa cong vòng!]"),
    (PIKO_BLINK[0], PIKO_SET_SPOON[1], "[Piko chớp mắt]"),
    (STAR_STILL[0] + 0.1, LUMO_TEST[1], "[kề cái thìa…]"),
    (LUMO_TEST[1], STAR_STILL[1], "[…sao vẫn chỉ túi Piko]"),
    (LUMO_PUZZLE[0], LUMO_LINE3[0], "[Lumo nhìn thìa, nhìn la bàn]"),
    (LUMO_LINE3[0], LUMO_LINE3[1], "LUMO: Thìa thôi mà?"),
    (TAVI_KNOCK[0] + 0.3, TAVI_KNOCK[1] + 0.3, "[đất cứng: CỘC CỘC]"),
    (TAVI_LOOK_LEAF[0] + 0.45, TAVI_LOOK_UP[0] + 0.3, "[lá còn ướt sương]"),
    (TAVI_LOOK_UP[0] + 0.5, TAVI_IDEA[0], "[mây bám đỉnh đồi]"),
    (TAVI_IDEA[0], TAVI_IDEA[1], "[mắt sáng lên]"),
    (TAVI_GATHER[0], TAVI_RAIN[1], "TAVI: Gom hơi nước, làm lạnh, sẽ có mưa!"),
    (TAVI_GATHER[0], TAVI_GATHER[1], "[chụm tay]"),
    (TAVI_SHIVER[0], TAVI_SHIVER[1], "[rùng mình]"),
    (TAVI_RAIN[0], TAVI_RAIN[1], "[tay rơi như mưa]"),
    (TAVI_POINT[0], TAVI_POINT[1], "TAVI: Lên đỉnh đồi, trên đó lạnh hơn!"),
    (TAVI_POINT[0] + 0.6, SECONDS, "[chỉ lên đỉnh đồi, cả nhóm ngước theo]"),
]
