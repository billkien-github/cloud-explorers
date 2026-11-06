"""
Previz khối Cảnh 1 tập 000A, đoạn 3: 21.9–34.1 giây của cảnh, S9–S11 (chú chim cười, Lumo ngượng rồi chống chế, chim bay đi, lại cắm mặt vào bản đồ).
Video dẫn cho Seedance (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh01_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Cận chú chim nghiêng đầu, lấy cánh vỗ bụng cười; Lumo cụp tai ngượng, ưỡn ngực, cất bản đồ vào túi, chống chế; chim bay đi; Lumo rút bản đồ, cắm mặt vào, sải bước ra khỏi khung.
Ảnh tham chiếu dự kiến: Lumo, rừng mây, chú chim, bản đồ giấy, bướm phát sáng: 5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh030
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh030
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh030
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh01_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh01_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh01/timing.py"
OFFSET = 21.9
FPS, SECONDS = 24, 13  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 12.2  # đoạn trong cảnh; 12.2–13 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh01_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh030.blend", SEGMENT)
