"""
Previz khối Cảnh 5 tập 000A, đoạn 3: 41.2–58.5 giây của cảnh, S12–S18 (sải bước ra mép dốc lá khô, nhấc chân, khựng
lại, chiếc lá trượt vèo, nhìn sang lối mòn, gật đầu, chú chim đáp xuống tảng đá gật gù, rút la bàn nhìn mũi sao, ngẩng
nhìn hòn đảo, đi xuống lối mòn, hòn đảo lóe lần nữa, la bàn lóe qua mép nắp túi, khung đen).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh05_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: toàn mép đồi thấy cả sườn dốc xuống tới thảm cỏ: Lumo sải bước ra mép, nhấc chân phải định lao xuống, khựng lại
ngả người ra sau, chân còn treo; một làn gió nhẹ, chiếc lá vàng trượt vèo xuống tới chân dốc; Lumo rụt chân lùi một bước,
quay đầu sang lối mòn; cú nhìn của Lumo từ mép đồi: dốc lá khô bên trái, chiếc lá ở chân dốc, máy lia sang lối mòn bên
phải; trung: gật đầu; cận chú chim bay vào đáp xuống tảng đá, nhìn theo Lumo, gật gù; trung ở mép đồi, đảo ở hậu cảnh:
rút la bàn từ miệng túi, nhìn mũi sao, ngẩng nhìn hòn đảo, cất la bàn; máy đi theo Lumo xuống lối mòn, hòn đảo lóe xanh
ngọc, túi da lóe vàng cùng nhịp, tai khẽ dựng; khung đen.
Ảnh tham chiếu dự kiến: Lumo, đỉnh đồi hoàng hôn, hòn đảo có Wonder Hub, Wonder Compass, chú chim
(little_bird_turnaround.png): 5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh140
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh140
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh140
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh05_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh05_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh05/timing.py"
OFFSET = 41.2
FPS, SECONDS = 24, 18  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 17.3  # đoạn trong cảnh; 17.3–18 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh05_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh140.blend", SEGMENT)
