"""
Previz khối Cảnh 1 tập 000A, đoạn 2: 21.9–48.6 giây của cảnh, S9–S14 (chú chim cười, Lumo ngượng rồi chống chế, chim bay đi, lại cắm mặt vào bản đồ, hụt chân ở mép dốc lá khô, trượt, đống lá, chiếc lá trên trán, bướm, phế tích, ánh vàng).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene01_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Cận chú chim nghiêng đầu, lấy cánh vỗ bụng cười; Lumo cụp tai ngượng, ưỡn ngực, cất bản đồ vào túi, chống chế; chim bay đi; Lumo rút bản đồ, cắm mặt vào, sải bước ra khỏi khung, đi thẳng qua chỗ đường rẽ, hụt chân ở mép dốc lá khô thoải, bản đồ tuột tay, ngồi bệt trượt xuống, lút vào đống lá trên nền rêu; ngẩng lên, chiếc lá giữa trán, lắc đầu, nhặt bản đồ nhét vào túi; bướm phát sáng đậu xuống phiến đá rêu trước mặt; máy lùi ra: phế tích cổ, ánh vàng le lói giữa những phiến đá.
Ảnh tham chiếu: Lumo, rừng mây, bản đồ đúng chiều, chú chim, bướm phát sáng, phế tích cổ (ancient_ruins_hero.png), cận đầu Lumo (lumo_head_ref.png): 7 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh020
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh020
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh020
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene01_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene01_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene01/timing.py"
OFFSET = 21.9
FPS, SECONDS = 24, 28  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 26.7  # đoạn trong cảnh; 26.7–28 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene01_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh020.blend", SEGMENT)
