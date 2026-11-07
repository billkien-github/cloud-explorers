"""
Previz khối Cảnh 4 tập 000A, đoạn 3: 38.6–61.6 giây của cảnh, S12–S19 (nhìn kỹ, vạch bụi cây, "Nhìn kỹ trước đã.", cất la bàn, lối bậc đá, chim bắt chước bước chậm, toàn lối nhỏ trên lưới, tới bệ đá, ấn ngôi sao, CẠCH, phiến đá trượt lộ bản đồ khắc).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene04_blocks.py; mốc
lấy từ TIMING trừ OFFSET; lý do chọn chỗ nối ở docstring scene04_blocks.py.
Diễn: Lumo đứng dậy, quay cả thân nhìn khoảng trống, vách đá, bụi cây (máy sau vai trái); tới sát bụi cây bên cạnh cửa (bụi trùm kín năm bậc lên), hai tay vạch: hai nửa dạt sang phải, trái màn hình, bậc đá rộng có tay vịn hiện ra, giữ hình 1.4 giây; cận chú chim từ phía Lumo, nền là trời và lưới: còn cười một nhịp rồi thôi, nghiêng đầu; cận Lumo nói. Lumo cất la bàn vào túi, tay xa bám tay vịn dây leo, lên từng bậc, hai chân bước so le (máy sau lưng chếch trái); chú chim bay xuống bậc đầu, nhảy từng bậc theo sau, nhón người như Lumo. Toàn từ trên cao trước mặt chếch phía khe, máy lùi theo: Lumo đi về phía máy, tay trái bám tay vịn (bên phải màn hình), chim nhảy theo sau, men gờ vách vòng qua đầu khe, lưới ngay dưới lối, túi da rung dày dần; xuống bãi đất tới bệ đá. Cú nhìn từ trên: tay xa ấn ngôi sao đá, ngôi sao lún xuống, phiến đá trên mặt bệ trượt sang lút vào trong bệ, lộ bản đồ khắc.
Ảnh tham chiếu dự kiến: Lumo, cầu ván cổ qua khe núi (cầu đã sập: tả bằng chữ), chú chim, bệ đá có ngôi sao và bản đồ khắc (star_plinth_ref.png): 4 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh100
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh100
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh100
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene04_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene04_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene04/timing.py"
OFFSET = 38.6
FPS, SECONDS = 24, 24  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 23.0  # đoạn trong cảnh; 61.6–62.6 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene04_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh100.blend", SEGMENT)
