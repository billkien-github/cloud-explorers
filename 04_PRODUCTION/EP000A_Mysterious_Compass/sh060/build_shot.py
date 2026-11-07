"""
Previz khối Cảnh 3 tập 000A, đoạn 2: 26.0–49.2 giây của cảnh, S7–S10 ("Mình tìm được rồi!", bước vào cửa thấp; vòm đá, bệ đỡ trống, cánh cửa khắc mây cuối vòm, khựng lại, cụp tai; ấn la bàn vào hình khắc trên bệ, gõ bệ TOK TOK TOK, chờ sỏi, thở phào, PLOP; nhấc la bàn, nhìn bệ, nhìn la bàn, nghiêng đầu; quay lưng về phía cánh cửa, liếc la bàn).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh03_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Lumo bật dậy khỏi thảm rêu, quay ba phần tư về máy, chìa la bàn ra trước, nhảy cẫng ở câu nói; bước vào cửa thấp, khom người; vòm đá (cửa thấp ở đầu gần, sau máy; bệ đỡ trống ở giữa; cánh cửa đá khắc mây ở đầu xa), Lumo đi từ cửa vào tới bên phải bệ, máy đẩy vào bệ; nhìn bệ trống, khựng lại, cụp tai, thân xệ xuống; chồm qua bệ đặt la bàn nằm ngang khớp vào hốc mặt bệ, ấn hai lần; nhìn quanh; gõ ba lần lên mép mặt bệ bằng tay phía máy; cụp tai, rụt cổ, ngước nhìn trần chờ; thở phào, dựng tai; hòn sỏi rơi từ trần trúng đỉnh đầu, nảy ra, lăn trên nền; nhấc la bàn lên ngang ngực, nhìn bệ, nhìn la bàn, nghiêng đầu; bước ra khỏi bệ, quay lưng về phía cánh cửa khắc mây (mặt về máy), liếc la bàn.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), phế tích cổ (ancient_ruins_hero.png, cho cú S7), vòm đá (stone_vault_hero.png: trần vòm, ô trần, bệ, cánh cửa khắc mây), Wonder Compass (wonder_compass_ref.png); cân nhắc ảnh cận đầu Lumo: 4–5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh060
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh060
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh060
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh03_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh03_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh03/timing.py"
OFFSET = 26.0
FPS, SECONDS = 24, 24  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 23.2  # đoạn trong cảnh; 23.2–24 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh03_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh060.blend", SEGMENT)
