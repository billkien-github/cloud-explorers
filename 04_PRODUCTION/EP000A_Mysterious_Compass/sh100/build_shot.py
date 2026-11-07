"""
Previz khối Cảnh 4 tập 000A, đoạn 3: 38.6–61.6 giây của cảnh, S12–S19 (nhìn kỹ, vạch bụi cây, "Nhìn kỹ trước đã.", cất la bàn, lối bậc đá, chim bắt chước bước chậm, toàn lối nhỏ trên lưới, tới bệ đá, ấn ngôi sao, CẠCH, phiến đá trượt lộ bản đồ khắc).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh04_blocks.py; mốc
lấy từ TIMING trừ OFFSET; lý do chọn chỗ nối ở docstring canh04_blocks.py.
Diễn: Lumo đứng dậy, nhìn khoảng trống, vách đá, bụi cây; tới sát bụi cây bên cạnh cửa, hai tay vạch ra: bậc đá rộng hiện ra; chú chim thôi cười, nghiêng đầu; cận Lumo nói. Lumo cất la bàn vào túi, tay xa bám tay vịn dây leo, lên từng bậc; chú chim bay xuống bậc đầu, nhảy từng bậc theo sau, nhón người như Lumo. Cảnh toàn: men gờ vách vòng qua đầu khe, lưới ngay dưới lối, túi da rung dày dần; xuống bãi đất tới bệ đá. Cú nhìn từ trên: tay xa ấn ngôi sao đá, ngôi sao lún xuống, phiến đá trên mặt bệ trượt sang lút vào trong bệ, lộ bản đồ khắc.
Ảnh tham chiếu dự kiến: Lumo, cầu ván cổ qua khe núi (cầu đã sập: tả bằng chữ), chú chim, bệ đá có ngôi sao và bản đồ khắc (star_plinth_ref.png): 4 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh100
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh100
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh100
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh04_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh04_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh04/timing.py"
OFFSET = 38.6
FPS, SECONDS = 24, 24  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 23.0  # đoạn trong cảnh; 61.6–62.6 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh04_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh100.blend", SEGMENT)
