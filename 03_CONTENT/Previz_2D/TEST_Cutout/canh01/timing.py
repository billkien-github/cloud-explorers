"""Mốc thời gian và CC của cảnh thử TEST_Cutout canh01 (quy ước: 03_CONTENT/PREVIZ_2D.md). Giây tính trong cảnh."""
FPS, SECONDS = 24, 11
SHOTS = [("S1", 0.0, 3.5), ("S2", 3.5, 6.3), ("S3", 6.3, 11.0)]   # toàn / trung Lumo với nút / toàn

NORI_TALK = (0.5, 5.5)       # Nori giảng về mưa, bị MAX POWER cắt ngang
LUMO_LOOK_DRY = (1.0, 2.0)   # Lumo nhìn dải đất còn khô, tai hơi cụp
LUMO_TURN = 2.2              # Lumo quay về phía nút đỏ, mắt sáng lên
LUMO_REACH = (2.6, 3.2)      # vội bước tới, vươn tay: "Thêm chút nữa thôi!"
LUMO_FREEZE = (3.6, 4.6)     # sực nhớ câu hô: khựng tay, mắt mở to, tai cụp, mặt lo
GLINT = 4.0                  # nút đỏ lấp lánh; Piko nhìn chằm chằm
PIKO_CROUCH = (4.4, 4.8)     # Piko nén người lấy đà
LUMO_PULL = (4.6, 5.4)       # Lumo bắt đầu rụt tay về
PIKO_JUMP = (4.8, 5.5)       # Piko bật nhảy về phía nút
CLICK = 5.5                  # Piko đáp lên lưng Lumo, Lumo chúi tới, tay đè xuống nút
MAX_POWER = (5.6, 6.6)       # máy rung, rít lên
TAVI_STEP = (6.0, 6.4)       # Tavi bước ra trước máy
TAVI_SHOUT = (6.4, 7.6)      # TAVI: "Không chạm nút đỏ!" (muộn một nhịp)
LUMO_REALIZE = (7.8, 9.0)    # Lumo nhìn tay mình trên nút, cụp tai
CLOUD_SWELL = (9.0, 11.0)    # mây phồng to, sẫm lại; cả nhóm ngước lên

CC = [
    (0.5, 3.0, "NORI: Mưa nhẹ thì đất thấm từ từ…"),
    (1.0, 2.0, "[Lumo nhìn dải đất còn khô]"),
    (2.6, 3.4, "LUMO: Thêm chút nữa thôi!"),
    (3.0, 5.5, "NORI: …rồi mầm cây sẽ—"),
    (3.6, 4.6, "[Lumo khựng tay, sực nhớ câu hô]"),
    (4.0, 4.8, "[nút đỏ lấp lánh, Piko nhìn chằm chằm]"),
    (4.8, 5.5, "[Piko bật nhảy: BOING]"),
    (5.5, 6.3, "[Piko đáp lên lưng Lumo, tay Lumo đè xuống nút: CẠCH]"),
    (5.6, 6.6, "[máy rung, rít lên: VRRRM]"),
    (6.4, 7.6, "TAVI: Không chạm nút đỏ!"),
    (7.8, 9.0, "[Lumo nhìn tay mình, cụp tai]"),
    (9.0, 11.0, "[mây phồng to, sẫm lại]"),
]
