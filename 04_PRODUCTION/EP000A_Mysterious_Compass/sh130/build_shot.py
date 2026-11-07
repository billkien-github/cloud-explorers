"""
Previz khối Cảnh 5 tập 000A, đoạn 2: 26.0–41.2 giây của cảnh, S8–S11 (câu hô lần 3, cất la bàn, kéo dây túi, lao đi,
bản đồ nằm lại một mình, chạy ngược lại chụp bản đồ, "Nhà thám hiểm Lumo không bao giờ quên bản đồ!", xoay bản đồ ba
lần, nhún vai, cất bản đồ vào túi).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene05_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: trung, hòn đảo ở hậu cảnh: Lumo cụp tai lấy đà, dựng thẳng tai, một tay chìa la bàn ra trước ngang ngực, hô, đẩy la
bàn tới ở "ngay phía trước"; cất la bàn vào túi da, kéo dây túi, lấy đà lao ra khỏi khung bên phải; cận sát mặt tảng đá: bản đồ
nằm lại một mình, mép phập phồng trong gió nhẹ; Lumo chạy ngược vào từ bên phải, khựng lại, chồm tới chụp bản đồ, gấp nhỏ
cầm bên hông, quay về phía máy ưỡn ngực nói; quay về phía mép đồi, mở bản đồ; cú nhìn bản đồ: hai bàn tay giữ hai cạnh
bên, bản đồ xoay từng nấc 60°, trong mỗi nấc hai tay quay theo bản đồ, giữa các nấc bản đồ đứng yên và tay nhích về chỗ cũ
(đổi tay cầm): xoay (một nấc), xoay nữa (một nấc), xoay thêm vòng nữa (ba nấc liền, hai lần đổi tay); trung: nhún vai, xòe
tay, cụp tai, gấp bản đồ nhét vào túi.
Ảnh tham chiếu dự kiến: Lumo, đỉnh đồi hoàng hôn, hòn đảo có Wonder Hub, Wonder Compass, bản đồ giấy: 5 ảnh (như sh120).
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh130
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh130
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh130
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene05_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene05_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene05/timing.py"
OFFSET = 26.0
FPS, SECONDS = 24, 16  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 15.2  # đoạn trong cảnh; 15.2–16 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene05_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh130.blend", SEGMENT)
