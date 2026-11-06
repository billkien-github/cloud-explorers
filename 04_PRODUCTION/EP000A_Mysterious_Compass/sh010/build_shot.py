"""
Previz khối Cảnh 1 tập 000A, đoạn 1: 0–13.4 giây của cảnh, S1–S5 (rừng mây, bản đồ cầm ngược, câu hô lần 1, SỘT, quả gai trên mũi).
Video dẫn cho Seedance (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh01_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Lumo đi trên đường rừng, cắm mặt vào bản đồ cầm ngược; cú nhìn của Lumo xuống bản đồ; dựng tai, chìa bản đồ ngang ngực, hô; bước thêm, mõm lút vào bụi gai trước vách đá; lùi ra, quả gai trên mũi, lắc đầu, nhìn bụi gai, nhìn bản đồ. Chú chim đậu trên cành từ đầu, bướm bay qua tán cây.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), rừng mây (cloud_forest_hero.png: đường rừng, bụi gai quả ké, vách đá, đảo lơ lửng), bản đồ giấy (paper_map_ref.png), chú chim (little_bird_turnaround.png), bướm phát sáng (glow_butterflies_ref.png): 5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh010
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh010
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh010
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh01_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh01_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh01/timing.py"
OFFSET = 0
FPS, SECONDS = 24, 14  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 13.4  # đoạn trong cảnh; 13.4–14 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh01_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh010.blend", SEGMENT)
