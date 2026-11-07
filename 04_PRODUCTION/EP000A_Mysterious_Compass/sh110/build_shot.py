"""
Previz khối Cảnh 4 tập 000A, đoạn 4: 61.6–84.8 giây của cảnh, S20–S25 (chim đậu mép bệ, bản đồ giấy cầm ngược rồi xoay khớp, đài thiên văn khắc lóe xanh ngọc, la bàn rung, đầu chỉ rời ngôi sao về đảo khắc rồi ra chân trời, "Chưa từng có hòn đảo này trên bản đồ của mình!", chim bay đi).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh04_blocks.py; mốc
lấy từ TIMING trừ OFFSET; lý do chọn chỗ nối ở docstring canh04_blocks.py.
Diễn: Chú chim bay vòng qua sau lưng Lumo đậu mép bệ; Lumo rút bản đồ giấy ở miệng túi, cầm ngang ngực (cầm ngược), hạ xuống đặt cạnh bản đồ khắc. Cú nhìn từ trên: rương lộn ngược, không khớp; xoay nửa vòng như vô lăng (hai bàn tay đi theo): khớp; máy tới mép phải, lia từ đài thiên văn khắc xuống chỗ mây trống trên bản đồ giấy, lùi ra; đài thiên văn khắc lóe xanh ngọc. Túi da rung mạnh, Lumo giật mình nhìn túi, chuyển bản đồ sang tay xa, rút la bàn (sáng mạnh). Cú nhìn từ trên: đầu chỉ rời ngôi sao đá, quay về đảo khắc, rồi chỉ ra chân trời (góc trên phải); la bàn dịu xuống. Lumo quay ra chân trời (bên phải, phía máy), nói, giơ la bàn rồi giơ bản đồ; chú chim vỗ cánh bay về phía chân trời, Lumo nhìn theo.
Ảnh tham chiếu dự kiến: Lumo, bệ đá có ngôi sao và bản đồ khắc, bản đồ giấy cầm ngược (paper_map_upside_down.png) và đúng chiều (paper_map_ref.png; theo SEEDANCE.md, Prompt theo giây: cú xoay ngắn cần đọc chiều thì cân nhắc ghép ở hậu kỳ thay vì đưa hai ảnh hai chiều), Wonder Compass, chú chim, cầu ván cổ qua khe núi (bối cảnh): 6–7 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh110
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh110
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh110
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh04_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh04_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh04/timing.py"
OFFSET = 61.6
FPS, SECONDS = 24, 24  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 23.2  # đoạn trong cảnh; 84.8–85.6 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh04_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh110.blend", SEGMENT)
