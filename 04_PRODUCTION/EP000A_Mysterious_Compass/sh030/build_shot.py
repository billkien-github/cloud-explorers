"""
Previz khối Cảnh 2 tập 000A, đoạn 1: 0–23.0 giây của cảnh, S1–S5 (chui khỏi đống lá, nhấc phiến đá, la bàn trong hốc, "Ồ! Kho báu!", thổi bụi, hắt xì, lau kính, mũi sao rung rồi xoay phắt, TÍT… TÍT…, suýt đánh rơi, cận la bàn có bức tường ở hậu cảnh).
Video dẫn cho Seedance 2.5 (04_PRODUCTION/SEEDANCE.md). Bối cảnh, diễn, máy quay dùng chung trong ../scene02_blocks.py; mốc
lấy từ TIMING trừ OFFSET.
Diễn: nối ngay cuối Cảnh 1: Lumo nhổm lên lấy đà, bật ra khỏi đống lá, lá rơi khỏi người; con bướm trên phiến đá rêu bay lên qua phế tích; Lumo bước lên đầu bậc đá, ngồi xổm (gối gập, hai chân dạng hai bên phiến đá) chồm tới phiến đá có ánh vàng, nhấc mép phiến đá lên (ánh vàng bung ra); cận hốc: la bàn vàng sáng nằm trong hốc, tay rút ra, phiến đá rơi về chỗ; đứng dậy giữ la bàn ngang ngực, hô, nhón người giơ la bàn; cúi mõm thổi bụi, bụi bay ngược vào mặt, hắt xì; lau kính bằng vạt áo choàng; cận la bàn và mặt Lumo: kính sáng le lói, mũi sao rung rung, xoay phắt, TÍT… TÍT…, giật mình bật lùi, nhảy dựng, tai dựng thẳng, la bàn tung lên, chụp lại; cú nhìn của Lumo dựng riêng: la bàn và hai tay trước máy ở nửa dưới khung, bức tường nhìn chéo, mảng dây leo ở nửa trên khung, mũi sao chỉ lên mảng dây leo.
Ảnh tham chiếu dự kiến: Lumo (lumo_turnaround.png), phế tích cổ (ancient_ruins_hero.png), Wonder Compass (wonder_compass_ref.png), bướm phát sáng (glow_butterflies_ref.png); cân nhắc mặt la bàn nhìn thẳng (wonder_compass_front.png, cho mũi sao ở cú cận) và ảnh cận đầu Lumo (chỏm lông): 4–6 ảnh.
    pipeline/run.sh build -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh030
    pipeline/run.sh preview -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh030
    pipeline/run.sh ref -Shot 04_PRODUCTION/EP000A_Mysterious_Compass/sh030
"""
import pathlib
import sys

sys.dont_write_bytecode = True  # không để __pycache__ cạnh scene02_blocks.py, timing.py, pipeline/
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import scene02_blocks  # noqa: E402

TIMING = "03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene02/timing.py"
OFFSET = 0
FPS, SECONDS = 24, 24  # thời lượng sinh: Seedance nhận số nguyên giây
SEGMENT = 23.0  # đoạn trong cảnh; 23.0–24 s chỉ giữ cú máy cuối, lúc dựng cắt bỏ

scene02_blocks.build(TIMING, OFFSET, SECONDS, HERE / "sh030.blend", SEGMENT)
