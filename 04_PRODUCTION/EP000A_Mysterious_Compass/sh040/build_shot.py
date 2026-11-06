"""
Previz khối Cảnh 1 tập 000A, đoạn 4: 34.1–48.6 giây của cảnh, S12–S14 (hụt chân ở mép dốc lá khô, trượt, đống lá, chiếc lá trên trán, bướm, phế tích, ánh vàng).
Video dẫn cho Seedance (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh01_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Lumo cắm mặt vào bản đồ đi thẳng qua chỗ đường rẽ, hụt chân ở mép dốc lá khô thoải, bản đồ tuột tay, ngồi bệt trượt xuống, lút vào đống lá trên nền rêu; ngẩng lên, chiếc lá giữa trán, lắc đầu, nhặt bản đồ nhét vào túi; bướm phát sáng đậu xuống phiến đá rêu trước mặt; máy lùi ra: phế tích cổ, ánh vàng le lói giữa những phiến đá.
Ảnh tham chiếu dự kiến: Lumo, rừng mây (dốc lá khô, đống lá), phế tích cổ (ancient_ruins_hero.png), bản đồ giấy, bướm phát sáng: 5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh040
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh040
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh040
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh01_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh01_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh01/timing.py"
OFFSET = 34.1
FPS, SECONDS = 24, 15  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 14.5  # đoạn trong cảnh; 14.5–15 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh01_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh040.blend", SEGMENT)
