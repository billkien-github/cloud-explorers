"""
Previz khối Cảnh 1 tập 000A, đoạn 1: 0–21.9 giây của cảnh, S1–S8 (rừng mây, bản đồ cầm ngược, câu hô lần 1, vấp hòn đá ngã vào bụi gai, quả gai trên mũi, xoay bản đồ, "À… phía trước là phía sau.", quay ngoắt lại, đường rừng rộng mở).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene01_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Lumo đi trên đường rừng, cắm mặt vào bản đồ cầm ngược; cú nhìn của Lumo xuống bản đồ; dựng tai, chìa bản đồ, hô, vừa hô dứt câu vừa sải bước, vấp hòn đá, chúi người ngã, đầu lút vào bụi gai trước vách đá; kẹt, ngọ nguậy, giật ra, quả gai trên mũi, lắc đầu, nhìn bụi gai, nhìn bản đồ; cú nhìn: xoay bản đồ nửa vòng; liếc ra sau, quay ngoắt lại; cảnh toàn đường rừng, nhảy cẫng lên (tên phim thêm ở hậu kỳ). Chú chim đậu trên cành, bướm bay qua tán cây.
Ảnh tham chiếu: Lumo (lumo_turnaround.png), rừng mây (cloud_forest_hero.png), bản đồ cầm ngược (paper_map_upside_down.png; mặt đúng chiều sau cú xoay ghép ở hậu kỳ), chú chim (little_bird_turnaround.png), bướm phát sáng (glow_butterflies_ref.png), cận đầu Lumo (lumo_head_ref.png): 6 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh010
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh010
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh010
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene01_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene01_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene01/timing.py"
OFFSET = 0
FPS, SECONDS = 24, 23  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 21.9  # đoạn trong cảnh; 21.9–23 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene01_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh010.blend", SEGMENT)
