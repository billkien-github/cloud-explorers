"""
Previz khối Cảnh 3 tập 000A, đoạn 3: 46.4–74.9 giây của cảnh, S10–S14 (quay lưng về phía cánh cửa khắc mây, liếc la bàn; cận la bàn, cánh cửa ở hậu cảnh: mũi sao chỉ ra sau lưng; xoay phắt trái, xoay phắt phải, xoay hai vòng, mũi sao không rời cánh cửa; chóng mặt, loạng choạng; bước về phía cánh cửa, la bàn sáng thêm, rung mạnh dần, TÍT… TÍT… TÍT TÍT TÍT!, mây trên cửa lấp lánh; "Khoan đã… cậu không dẫn tới kho báu.", mắt sáng lên, "Cậu dẫn tới những thứ… kỳ lạ!"; nhét la bàn vào túi da, chạy tới đẩy cánh cửa, hé khe sáng).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene03_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: Lumo bước ra khỏi bệ, quay lưng về phía cánh cửa khắc mây (mặt về máy), liếc la bàn; cận la bàn: một tay giơ la bàn ra bên hông phía máy, mặt la bàn quay về máy, cánh cửa ở nửa trên khung, mũi sao chỉ về cánh cửa; xoay phắt sang trái quay mặt về cánh cửa (đổi tay, la bàn vẫn ở bên phía máy), xoay phắt sang phải quay lưng lại; xoay một vòng, dừng giơ la bàn ra, xoay thêm vòng nữa, dừng giơ la bàn ra, tai lật phật; mỗi lần dừng mũi sao vẫn chỉ cánh cửa; loạng choạng, người lắc qua lại, hai tai lắc lư; quay về phía cánh cửa, bước sáu bước tới trước cửa, tay phía máy chìa la bàn ra bên hông, la bàn sáng thêm từng bước; sáu đốm sáng vàng nhấp nháy trên mặt cánh cửa; quay ba phần tư về máy nói với la bàn; nhìn cánh cửa, tai dựng; nói tiếp, chìa la bàn về phía cánh cửa, nhún lên; quay về phía máy, nhét la bàn xuống túi da bên hông phải; chạy ba bước tới, hai tay đẩy cánh cửa, hai cánh (trước đó khít nhau) nhúc nhích rồi hé vào trong, khe sáng giữa hai cánh rộng dần.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), vòm đá (stone_vault_hero.png), Wonder Compass (wonder_compass_ref.png); cân nhắc mặt la bàn nhìn thẳng (wonder_compass_front.png, cho cú cận S11) và ảnh cận đầu Lumo: 3–5 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh070
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh070
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh070
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene03_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene03_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene03/timing.py"
OFFSET = 46.4
FPS, SECONDS = 24, 29  # thời lượng sinh: Seedance nhận số nguyên giây (28.5 + đuôi 0.5)
SEGMENT = 28.5  # đoạn trong cảnh; 28.5–29 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene03_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh070.blend", SEGMENT)
