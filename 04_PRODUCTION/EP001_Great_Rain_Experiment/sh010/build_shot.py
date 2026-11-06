"""
Previz khối Cảnh 1 tập 01, đoạn 1: 0–28.8 giây của cảnh, S1–S6 (giọt sương cuối cùng, Piko đớp, tên phim, Nori rọi
mầm cây, Lumo vấp, la bàn chỉ về túi Piko). Video dẫn cho Seedance (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy
quay dùng chung với sh020 trong ../canh01_blocks.py; mốc lấy từ TIMING trừ OFFSET.
    .\\pipeline\\run.ps1 build -Shot 04_PRODUCTION\\EP001_Great_Rain_Experiment\\sh010
    .\\pipeline\\run.ps1 ref -Shot 04_PRODUCTION\\EP001_Great_Rain_Experiment\\sh010
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh01_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh01_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/canh01/timing.py"
OFFSET = 0.0
FPS, SECONDS = 24, 29  # thời lượng sinh: Seedance trên BytePlus ModelArk nhận số nguyên giây
SEGMENT = 28.8  # đoạn trong cảnh; 28.8–29 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh01_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh010.blend", SEGMENT)
