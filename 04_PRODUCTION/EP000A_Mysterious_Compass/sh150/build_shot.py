"""
Previz khối post-credit tập 000A (cảnh 6), một đoạn: 0–5 giây của cảnh, S1 (bãi phế liệu lúc hoàng hôn, hộp kim loại phủ bụi nắp hé; hòn đảo có Wonder Hub ở chân trời lóe xanh ngọc, cùng nhịp đó Inventor Pack trong hộp lóe qua khe nắp).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay trong ../canh06_blocks.py; mốc lấy từ
TIMING trừ OFFSET.
Diễn: không có nhân vật. Máy đẩy chậm, đều vào chiếc hộp suốt cú; ở HUB_FLASH đài thiên văn trên hòn đảo lóe một nhịp
(quầng tia xanh ngọc, mái vòm sáng 0.7 giây), cùng nhịp đó lòng hộp sáng bừng, quầng và tia xanh ngọc lọt ra khe nắp;
sau lóe khe nắp còn le lói xanh tới hết cảnh.
Ảnh tham chiếu: bãi phế liệu (junkyard_hero.png), hòn đảo có Wonder Hub (wonder_hub_island_hero.png), Inventor Pack (inventor_pack_ref.png): 3 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh150
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh150
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh150
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh canh06_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import canh06_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/canh06/timing.py"
OFFSET = 0
FPS, SECONDS = 24, 6  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 5.0  # đoạn trong cảnh; 5–6 s máy đẩy tiếp cùng tốc độ, lúc dựng cắt bỏ

canh06_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh150.blend", SEGMENT)
