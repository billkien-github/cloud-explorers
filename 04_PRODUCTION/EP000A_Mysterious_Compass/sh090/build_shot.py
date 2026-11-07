"""
Previz khối Cảnh 4 tập 000A, đoạn 2: 14.8–38.6 giây của cảnh, S5–S11 ("Ngay phía trước!", lao lên cầu, CREAAAAK, chờ sỏi, "Không sao…", CRACK, cả dãy ván rơi xuống lưới, túm dây leo, PHỊCH, chim cười, "Một chiếc cầu… rất cũ!", cận la bàn vẫn chỉ ngôi sao đá).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene04_blocks.py; mốc
lấy từ TIMING trừ OFFSET; lý do chọn chỗ nối ở docstring scene04_blocks.py.
Diễn: Lumo dựng tai, chìa la bàn, hô, lấy đà lao lên cầu; tấm ván trước mặt bật lên, Lumo khựng lại, cụp tai ngước trời chờ sỏi, thở phào, nói, mắt vẫn ngước mà bước thêm một bước; tấm ván trước mũi chân gãy, cả dãy ván và mấy cột thành cầu rơi xuống lưới dây leo, lưới võng xuống nảy bập bềnh, dây thành cầu chùng giữa khe; Lumo chới với (la bàn sang tay xa), tay gần túm dây leo ở thành cầu sát cửa, rồi lùi về ngã ngồi trên đệm rêu, đuôi bẹp. Chú chim bay vào đậu đỉnh cột cầu sát cửa, vỗ bụng cười ba cái; Lumo cụp tai ngượng, xoè tay, nói, gật mạnh, nâng la bàn lên nhìn. Cú nhìn: đầu chỉ vẫn chỉ ngôi sao đá bên kia khoảng trống.
Ảnh tham chiếu dự kiến: Lumo, cầu ván cổ qua khe núi, Wonder Compass, chú chim (little_bird_turnaround.png), bệ đá có ngôi sao (nhỏ ở xa): 5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh090
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh090
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh090
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene04_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene04_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene04/timing.py"
OFFSET = 14.8
FPS, SECONDS = 24, 25  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 23.8  # đoạn trong cảnh; 38.6–39.8 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene04_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh090.blend", SEGMENT)
