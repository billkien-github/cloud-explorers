"""
Previz khối Cảnh 5 tập 000A, đoạn 1: 0–26.0 giây của cảnh, S1–S7 (la bàn chỉ qua ngọn đồi, leo lên đỉnh, biển mây, đặt
bản đồ lên tảng đá, nâng la bàn, gió thổi tạt, mây tách, hòn đảo có đài thiên văn hiện ra, lóe xanh ngọc, la bàn lóe
theo, "Một nơi chưa ai khám phá…", "Được rồi, bạn la bàn.").
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene05_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: cú nhìn của Lumo xuống la bàn trong tay, mũi sao chỉ qua sườn đồi; cảnh toàn chân đồi, Lumo hạ la bàn, ngẩng nhìn,
leo lên sườn cỏ thoải; cảnh toàn đỉnh đồi (tảng đá, mép dốc lá khô, lối mòn, biển mây); đặt bản đồ lên tảng đá, hai tay
nâng la bàn, nhìn ra chân trời; cú nhìn: mũi sao chỉ vào tầng mây ở chân trời; gió thổi tạt (tai, áo choàng, cỏ rạp, vệt
gió), hai tầng mây tách, hòn đảo hiện dần, đài thiên văn lóe xanh ngọc, la bàn lóe xanh ngọc cùng nhịp, tai bật dựng; cận
Lumo nói hai câu, cúi nhìn la bàn, gật nhẹ.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), đỉnh đồi hoàng hôn (sunset_hill_hero.png), hòn đảo có Wonder Hub
(wonder_hub_island_hero.png), Wonder Compass (wonder_compass_front.png), bản đồ giấy (paper_map_ref.png): 5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh120
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh120
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh120
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene05_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene05_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene05/timing.py"
OFFSET = 0
FPS, SECONDS = 24, 27  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 26.0  # đoạn trong cảnh; 26.0–27 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene05_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh120.blend", SEGMENT)
