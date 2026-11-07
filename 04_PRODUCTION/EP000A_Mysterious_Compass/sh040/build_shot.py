"""
Previz khối Cảnh 2 tập 000A, đoạn 2: 23.0–44.8 giây của cảnh, S6–S10 (đi vòng qua phiến đá tới đầu tường, quay lại, mũi sao xoay theo, "Hừm… la bàn phải chỉ hướng Bắc chứ. Sao lại chỉ vào tường?", áp tai, gõ ba lần, hòn sỏi rơi trúng đầu, "Mình nghĩ bức tường không thích bị làm phiền.", liếc la bàn).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh02_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Lumo cầm la bàn ngang ngực, bước xuống bậc đá, đi vòng qua đầu phiến đá ra sau, tới sát đầu tường; cận la bàn: quay ngoắt lại nhìn phía vừa đi, mũi sao xoay theo, vẫn chỉ về phía bức tường, la bàn kêu; Lumo nghiêng đầu "Hừm…", lắc lắc la bàn, nói, ngoái nhìn đầu tường sau lưng; quay mặt vào đầu tường, chuyền la bàn sang tay xa để bên hông, nghiêng đầu ép một bên tai vào mặt đầu tường, không có gì; gõ ba lần bằng tay phía máy; hòn sỏi lăn khỏi đá đỉnh tường, rơi trúng đỉnh đầu, nảy ra; cụp tai, ngước nhìn mép tường; quay ba phần tư về máy, la bàn về tay phía máy, chống chế, nhún vai; liếc xuống la bàn.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), phế tích cổ (ancient_ruins_hero.png), Wonder Compass (wonder_compass_ref.png); cân nhắc mặt la bàn nhìn thẳng (wonder_compass_front.png) và ảnh cận đầu Lumo: 3–5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh040
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh040
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh040
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh02_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh02_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh02/timing.py"
OFFSET = 23.0
FPS, SECONDS = 24, 23  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 21.8  # đoạn trong cảnh; 21.8–23 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh02_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh040.blend", SEGMENT)
