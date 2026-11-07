"""
Previz khối Cảnh 3 tập 000A, đoạn 3: 49.2–74.9 giây của cảnh, S11–S14 (cận la bàn, cánh cửa khắc mây ở hậu cảnh: mũi sao chỉ ra sau lưng; xoay phắt trái, xoay phắt phải, xoay hai vòng, mũi sao không rời cánh cửa; chóng mặt, loạng choạng; bước về phía cánh cửa, la bàn sáng thêm, rung mạnh dần, TÍT… TÍT… TÍT TÍT TÍT!, mây trên cửa lấp lánh; "Khoan đã… cậu không dẫn tới kho báu.", mắt sáng lên, "Cậu dẫn tới những thứ… kỳ lạ!"; nhét la bàn vào túi da, chạy tới đẩy cánh cửa, hé khe sáng).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../canh03_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Lumo đứng cạnh bệ, mặt về máy, cánh cửa khắc mây sau lưng ở hậu cảnh; la bàn hai tay trước ngực, mũi sao chỉ ra sau lưng; liếc ra sau; xoay phắt sang trái quay mặt về cánh cửa (la bàn dời sang phía máy, mặt la bàn xoay về máy), xoay phắt sang phải quay lưng lại; xoay một vòng, dừng liếc la bàn, xoay thêm vòng nữa, tai lật phật; loạng choạng, người lắc qua lại, hai tai lắc lư; quay về phía cánh cửa, bước sáu bước tới trước cửa, la bàn sáng thêm từng bước; sáu đốm sáng vàng nhấp nháy trên mặt cánh cửa; quay ba phần tư về máy nói với la bàn; nhìn cánh cửa, tai dựng; nói tiếp, chìa la bàn về phía cánh cửa, nhún lên; nhét la bàn vào túi da bên hông phải; chạy ba bước tới, hai tay đẩy cánh cửa, hai cánh nhúc nhích rồi hé vào trong, khe sáng giữa hai cánh rộng dần.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), vòm đá (stone_vault_hero.png), Wonder Compass (wonder_compass_ref.png); cân nhắc mặt la bàn nhìn thẳng (wonder_compass_front.png, cho cú cận S11) và ảnh cận đầu Lumo: 3–5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh070
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh070
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh070
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh03_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh03_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh03/timing.py"
OFFSET = 49.2
FPS, SECONDS = 24, 27  # thời lượng sinh: Seedance nhận số nguyên giây (25.7 + đuôi 0.5, làm tròn lên)
SEGMENT = 25.7  # đoạn trong cảnh; 25.7–27 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

canh03_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh070.blend", SEGMENT)
