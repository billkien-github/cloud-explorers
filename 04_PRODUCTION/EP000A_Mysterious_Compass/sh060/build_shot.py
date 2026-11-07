"""
Previz khối Cảnh 3 tập 000A, đoạn 2: 29.4–46.4 giây của cảnh, S8–S9 (vòm đá, bệ đỡ trống, cánh cửa khắc mây cuối vòm, khựng lại, cụp tai; ấn la bàn vào hình khắc trên bệ, gõ bệ TOK TOK TOK, chờ sỏi, thở phào, PLOP; nhấc la bàn, nhìn bệ, nhìn la bàn, nghiêng đầu).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene03_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: vòm đá (cửa thấp ở đầu gần, sau máy; bệ đỡ trống ở giữa; cánh cửa đá khắc mây khép kín ở đầu xa), Lumo khom người qua cửa thấp, đi từ cửa vào tới bên phải bệ, máy đẩy vào bệ; nhìn bệ trống, khựng lại, cụp tai, thân xệ xuống; chồm qua bệ đặt la bàn nằm ngang khớp vào hốc mặt bệ, ấn hai lần; nhìn quanh; gõ ba lần lên mép mặt bệ bằng tay phía máy; cụp tai, rụt cổ, ngước nhìn trần chờ; thở phào, dựng tai; hòn sỏi sẫm rơi chậm từ trên xuống trúng đỉnh đầu, Lumo bẹp người, tai ép phẳng, hòn sỏi nảy ra, lăn trên nền; nhấc la bàn lên ngang ngực, nhìn bệ, nhìn la bàn, nghiêng đầu.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), vòm đá (stone_vault_hero.png: trần vòm, ô trần, bệ, cánh cửa khắc mây), Wonder Compass (wonder_compass_ref.png); cân nhắc ảnh cận đầu Lumo: 3–4 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh060
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh060
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh060
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene03_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene03_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene03/timing.py"
OFFSET = 29.4
FPS, SECONDS = 24, 18  # thời lượng sinh: Seedance nhận số nguyên giây (17.0 + đuôi 0.5, làm tròn lên)
SEGMENT = 17.0  # đoạn trong cảnh; 17.0–18 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene03_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh060.blend", SEGMENT)
