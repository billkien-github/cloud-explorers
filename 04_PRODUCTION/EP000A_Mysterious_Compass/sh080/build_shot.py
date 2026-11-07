"""
Previz khối Cảnh 4 tập 000A, đoạn 1: 0–14.8 giây của cảnh, S1–S4 (cửa đá mở hẳn, mây tắt dần, toàn cảnh cầu ván cổ và lưới dây leo, TÍT… TÍT… trong túi da, rút la bàn, cận la bàn chỉ ngôi sao đá).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh04_blocks.py; mốc
lấy từ TIMING trừ OFFSET; lý do chọn chỗ nối ở docstring canh04_blocks.py.
Diễn: Cửa đá mở hẳn ra phía máy, hình mây trên mặt trong cánh cửa và trên khung cửa tắt dần; Lumo hụt tay, loạng choạng ra bậc cửa phủ rêu, thấy cây cầu: dựng tai. Cảnh toàn: cầu ván qua khe núi, lưới dây leo phủ kín bên dưới, lối bậc đá men vách sau nửa khuất sau bụi cây, bệ đá bên kia; mắt Lumo đi dọc cây cầu sang bệ đá. Túi da rung hai lần, Lumo liếc xuống túi, rút la bàn ra ngang ngực. Cú nhìn qua vai: la bàn sáng le lói, đầu chỉ chỉ thẳng ngôi sao đá trên bệ bên kia khe.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), cầu ván cổ qua khe núi (vine_bridge_hero.png), Wonder Compass (wonder_compass_ref.png), bệ đá có ngôi sao (star_plinth_ref.png, lúc này phiến đá còn đóng, tả bằng chữ), vòm đá (stone_vault_hero.png, cho cửa đá khắc mây, nếu cần): 4–5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh080
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh080
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh080
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh04_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh04_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh04/timing.py"
OFFSET = 0
FPS, SECONDS = 24, 16  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 14.8  # đoạn trong cảnh; 14.8–16 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh04_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh080.blend", SEGMENT)
