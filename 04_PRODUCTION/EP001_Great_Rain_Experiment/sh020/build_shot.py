"""
Previz khối Cảnh 1 tập 01, đoạn 2: 28.8–55.0 giây của cảnh, S7–S14 ("Có gì lạ kìa!", cái thìa cong, la bàn kề thìa vẫn
chỉ túi, "Thìa thôi mà?", lá ướt sương, mây đỉnh đồi, Tavi giảng cách làm mưa, chỉ đỉnh đồi). Video dẫn cho Seedance
(04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung với sh010 trong ../canh01_blocks.py; mốc lấy từ TIMING
trừ OFFSET.
    .\\pipeline\\run.ps1 build -Shot 04_PRODUCTION\\EP001_Great_Rain_Experiment\\sh020
    .\\pipeline\\run.ps1 ref -Shot 04_PRODUCTION\\EP001_Great_Rain_Experiment\\sh020
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh01_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh01_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/canh01/timing.py"
OFFSET = 28.8
FPS, SECONDS = 24, 27  # thời lượng sinh: Seedance trên BytePlus ModelArk nhận số nguyên giây
SEGMENT = 26.2  # đoạn trong cảnh; 26.2–27 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh01_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh020.blend", SEGMENT)
