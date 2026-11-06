"""
Previz khối Cảnh 1 tập 000A, đoạn 2: 13.4–21.9 giây của cảnh, S6–S8 (xoay bản đồ, "À… phía trước là phía sau.", quay ngoắt lại, đường rừng rộng mở).
Video dẫn cho Seedance (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh01_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Cú nhìn của Lumo: xoay bản đồ nửa vòng, rương đứng thẳng, mũi tên chỉ về phía Lumo; Lumo hiểu ra, liếc ra sau lưng, quay ngoắt lại; cảnh toàn con đường rừng rộng mở, Lumo nhảy cẫng lên (tên phim thêm ở hậu kỳ, không có trong video dẫn).
Ảnh tham chiếu dự kiến: Lumo, rừng mây, bản đồ giấy, chú chim (nhỏ trên cành trong cảnh toàn), bướm phát sáng: 5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh020
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh020
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh020
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh01_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh01_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh01/timing.py"
OFFSET = 13.4
FPS, SECONDS = 24, 9  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 8.5  # đoạn trong cảnh; 8.5–9 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh01_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh020.blend", SEGMENT)
