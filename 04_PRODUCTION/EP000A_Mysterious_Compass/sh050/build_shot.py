"""
Previz khối Cảnh 3 tập 000A, đoạn 1: 0–29.4 giây của cảnh, S1–S7 (đi dọc bức tường, la bàn sáng dần, rung mạnh dần, TÍT… TÍT… TÍT TÍT TÍT!; vạch dây leo, phù điêu đám mây ánh lên; thử ấn, thử kéo; lấy đà đẩy, phù điêu xoay, ngã lăn ra thảm rêu, cửa thấp mở, phù điêu tắt; cú nhìn la bàn: dịu đi, mũi sao quay vào trong cửa thấp; "Mình tìm được rồi!", bước vào cửa thấp).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene03_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: nối ngay cuối Cảnh 2: Lumo đứng sát đầu tường, la bàn ở tay phía máy; đi vòng trước bậc đá rồi dọc bức tường về phía mảng dây leo, la bàn hai tay trước ngực, càng gần càng sáng, rung, kêu dày; chuyền la bàn sang tay xa để bên hông, tay phía máy vạch mảng dây leo (rủ kín tới chân tường), hai nửa dạt ra hai bên: phù điêu đám mây trong hốc tường, những đường mây ánh vàng; hai tay ấn hai lần, nhún vai; hai tay bám mép phải phù điêu kéo giật giật, ngả hẳn người ra sau, nghiêng đầu; lùi hai bước, khom lấy đà, lao tới đẩy; phù điêu xoay nhẹ, Lumo chúi sang trái, lộn một vòng trên thảm rêu, ngồi phịch, rêu tung lên; cánh đá bên trái phù điêu (trước đó phẳng với mặt tường) xoay vào trong tường, mở cửa thấp, vệt nắng lọt vào; đường mây tắt; Lumo xoay người trên thảm rêu nhìn vào tường, đưa la bàn lên trước mắt; cú nhìn: la bàn dịu đi, rung khẽ, mũi sao rời phù điêu, quay vào trong cửa thấp; Lumo bật dậy, chìa la bàn ra, nhảy cẫng ở câu nói; bước vào cửa thấp, khom người.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), phế tích cổ (ancient_ruins_hero.png: tường, mảng dây leo, phù điêu mây, thảm rêu), Wonder Compass (wonder_compass_ref.png); cân nhắc mặt la bàn nhìn thẳng (wonder_compass_front.png, cho cú nhìn S6) và ảnh cận đầu Lumo (chỏm lông): 3–5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh050
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh050
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh050
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene03_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene03_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene03/timing.py"
OFFSET = 0
FPS, SECONDS = 24, 30  # thời lượng sinh: Seedance nhận số nguyên giây (29.4 + đuôi 0.5, làm tròn lên)
SEGMENT = 29.4  # đoạn trong cảnh; 29.4–30 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene03_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh050.blend", SEGMENT)
