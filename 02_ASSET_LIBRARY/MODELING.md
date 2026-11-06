# Làm nhân vật và đạo cụ 3D

Quy trình: **ChatGPT** sinh ảnh tham chiếu → **Blender** dựng lưới, rig, material theo ảnh bằng build script cạnh asset ([`README.md`](README.md)) → shot sinh hình cuối bằng **Seedance** ([`04_PRODUCTION/SEEDANCE.md`](../04_PRODUCTION/SEEDANCE.md)). Hình dáng, màu, chiều cao: [`01_BRAND/Character_Bible/`](../01_BRAND/Character_Bible/README.md).

## Bộ ảnh tham chiếu

Mỗi ảnh một góc nhìn, nền trơn. Ảnh nhìn sau đi cặp với ảnh nhìn trước cùng tên, thêm hậu tố `_back`. Mỗi nhân vật có:

- **Thân** (`<tên>_apose_body.png`, `<tên>_tpose_body.png`): chỉ phần dựng liền vào thân. Bỏ đồ rời và phần làm riêng (áo choàng, túi, ba lô, đuôi, cánh, râu, lá đội đầu); đồ ôm sát (mũ, kính, gile của Tavi) để liền. Dùng để dựng lưới thân và đặt xương.
- **Đủ đồ** (`<tên>_outfit.png`): ảnh thân A-pose mặc đủ đồ, giữ nguyên tư thế, cỡ và vị trí trong khung để chồng khớp lên ảnh thân. Dùng để dựng và đặt đồ rời. Không cần bản T-pose vì đồ rời dựng trên tư thế A.
- **Bộ phận làm riêng** (`<tên>_<bộ phận>_ref.png`): đuôi, cánh, áo choàng, túi.

Đạo cụ: ảnh nhìn thẳng trước, sau (`<tên>_front.png`, `<tên>_back.png`). Ảnh `<tên>_ref.png` nhìn 3/4 có sẵn chỉ để tham khảo thiết kế.

Ngoại lệ:
- Vật có hai mặt như nhau (bánh răng, thìa, móc) hoặc vật dài (thuyền, cầu ván): thay ảnh sau bằng ảnh nhìn ngang (`_side`) hoặc nhìn từ trên (`_top`).
- Thú bốn chân: ảnh trước, ngang, sau; không có A-pose, T-pose.
- Đạo cụ đổi hình trong phim có thêm ảnh trạng thái (`_frost`, `_bent`…).

### Hiện trạng

Ảnh nằm trong `concept/` của asset. ✅ có, ❌ chưa có. Ảnh thân cố ý không có đuôi và đồ rời; đuôi chỉ có ở ảnh đủ đồ và ảnh `_tail_ref`.

| Nhân vật | Thân A-pose (trước · sau) | Thân T-pose (trước · sau) | Đủ đồ (trước · sau) | Làm riêng |
|---|---|---|---|---|
| Lumo | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ | áo choàng ✅ `lumo_cape_ref.png`, túi ✅ `lumo_bag_ref.png`, đuôi ✅ `lumo_tail_ref.png` |
| Tavi | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ | đuôi ✅ `tavi_tail_ref.png` |
| Nori | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ | cánh ✅ `nori_wing_ref.png` |
| Piko | ✅ · ✅ | ✅ · ✅ | ✅ · ✅ `piko_pouch_ref.png` (nhìn 3/4), `piko_pouch_back_ref.png` | — |
| Sinh vật nhỏ (`Valley_Critters/`, tên file `valley_critter_…`) | ✅ · ✅ | ✅ · ✅ | — | lá đội đầu: theo `valley_critters_ref.png` ✅ |

| Đạo cụ | Trước · sau |
|---|---|
| Wonder Compass (Lumo) | ✅ · ✅ |
| Inventor Pack (Tavi) | ✅ · ✅ |
| Story Lens (Nori) | ✅ · ✅ |
| Pocket of Wonders (Piko) | ✅ · ✅ |

Tập 01 (danh sách asset: beat sheet `03_CONTENT/Scripts/EP001_great_rain_experiment.md`):

| Asset | Thư mục | Ảnh | Có |
|---|---|---|---|
| Rain-O-Matic 3000 | `Props/Rain_O_Matic/` | `rain_o_matic_front.png`, `rain_o_matic_back.png`, `rain_o_matic_frost.png` | ✅ |
| Nắp che nút đỏ | `Props/Rain_O_Matic/` | `button_cover_front.png`, `button_cover_side.png` | ✅ |
| Bánh răng vàng | `Props/Golden_Gear/` | `golden_gear_front.png`, `golden_gear_side.png`, `golden_gear_frost.png` | ✅ |
| Móc ròng rọc | `Props/Pulley_Hook/` | `pulley_hook_front.png`, `pulley_hook_side.png` | ✅ |
| Vịt cao su | `Props/Rubber_Duck/` | `rubber_duck_side.png`, `rubber_duck_front.png`, `rubber_duck_gear.png` | ✅ |
| Thìa | `Props/Spoon/` | `spoon_top.png`, `spoon_side.png`, `spoon_bent.png` | ✅ |
| Ô | `Props/Umbrella/` | `umbrella_open.png`, `umbrella_closed.png`, `umbrella_inverted.png` | ✅ |
| Hộp ốc | `Props/Screw_Box/` | `screw_box_front.png`, `screw_box_open.png` | ✅ |
| Cuộn dây của Noah | `Props/Noah_Rope/` | `noah_rope_ref.png` | ✅ |
| Con thuyền | `Environments/Noah_Story/` | `noah_ark_side.png`, `noah_ark_front.png` | ✅ |
| Cầu ván | `Environments/Noah_Story/` | `plank_bridge_side.png`, `plank_bridge_top.png` | ✅ |
| Đôi voi con | `Characters/Baby_Elephants/` | `baby_elephants_ref.png` (thiết kế cả đôi), `baby_elephant_front.png`, `baby_elephant_side.png`, `baby_elephant_back.png` | ✅ |
| Noah | `Characters/Noah/` | `noah_front.png`, `noah_side.png`, `noah_hand_front.png`, `noah_hand_back.png` | ✅ |
| Thú trên boong (thỏ, chim, hươu cao cổ) | `Characters/Ark_Animals/` | `ark_animals_ref.png` (thiết kế cả nhóm) | ✅ |

Không cần ảnh riêng: mây bé (hiệu ứng dựng trong Blender), chiếc lá khô (theo `Environments/Cloud_Valley/concept/cloud_valley_dry_hero.png`). Bối cảnh thế giới truyện và Wonder Hub là ảnh tham chiếu bối cảnh, prompt theo `04_PRODUCTION/SEEDANCE.md`.

Ảnh có bối cảnh: `<tên>_hero.png`.

## Chuẩn ảnh

Trong Blender, ảnh trước đặt làm ảnh nền (Reference) ở Front view, ảnh sau ở Back view, scale theo chiều cao trong Character Bible. Ảnh sai tư thế hoặc hai ảnh lệch cỡ thì model sai theo, nên soát từng ảnh trước khi dùng:

1. **Tư thế đối xứng, tay thẳng.** A-pose: tay dang chéo xuống khoảng 45°. T-pose: tay dang ngang tầm vai, song song mặt đất. Khe hở rõ giữa tay và thân. Nhân vật có chân: chân thẳng, bàn chân đặt phẳng, rộng bằng vai, mũi chân hướng ra trước, có khe hở giữa hai chân.
   - A-pose: vai biến dạng đẹp hơn khi tay buông xuống (tư thế hay gặp nhất). T-pose: tay xa thân nhất, dễ thấy vai, khuỷu, cổ tay; hợp với nhân vật bụng tròn tay ngắn như Lumo, Tavi.
   - Dựng lưới theo tư thế nào: thử với Lumo, giữ tư thế nào qua `pipeline/rig_qa.py` tốt hơn rồi dùng cho cả nhóm.
2. **Bàn tay úp:** lòng bàn tay hướng xuống đất, ngón duỗi thẳng và hơi tách nhau, ngón cái hướng ra trước. Dựng theo tay ngửa thì cổ tay ở tư thế nghỉ đã xoắn, animation trông gượng.
3. **Thấy rõ khớp** để đặt xương: cằm và cổ, vai, khuỷu, cổ tay, háng, đầu gối, cổ chân.
4. **Biểu cảm trung tính:** miệng khép, cười nhẹ, mắt mở nhìn thẳng. Biểu cảm do face rig làm.
5. **Máy quay:** chính diện, trực giao (không phối cảnh), ngang tầm ngực; thấy trọn từ chóp tai, sừng, râu tới bàn chân, chừa lề. Nhân vật khổ dọc 2:3, đạo cụ khổ vuông (Story Lens khổ dọc).
6. **Cặp trước, sau khớp nhau:** cùng cỡ, cùng vị trí trong khung. Lật ngang ảnh sau rồi chồng mờ 50% lên ảnh trước: viền ngoài phải gần trùng. ChatGPT có thể trả khổ khác ảnh gửi kèm (1122×1402 so với 1086×1448), nên so theo chiều cao nhân vật, không theo khung ảnh. Trong ảnh sau, bên phải của nhân vật nằm bên phải người xem.
7. **Nền, ánh sáng:** nền xám nhạt trơn, ánh sáng đều, không bóng đổ xuống đất, không chữ, chỉ một đối tượng.
8. **Trong suốt, phát sáng làm bằng shader** (thân thạch của Piko, ánh sáng của Nori, tinh thể của Tavi), ảnh chỉ cần rõ hình. Ảnh thân bỏ bọt trong thân và giọt nước quanh Piko, bỏ quầng sáng quanh Nori để thấy rõ viền.

## Prompt ChatGPT

- Mỗi chat là một khối có tiêu đề bên dưới. Gửi lần lượt từng prompt theo thứ tự, mỗi lần nhận **một ảnh**; ảnh sau và ảnh đủ đồ sinh trong cùng chat với ảnh trước để giữ đúng thiết kế.
- Đính kèm đúng file ghi ở mỗi bước, theo đúng thứ tự khi có nhiều file, kể cả khi ảnh đó đã có sẵn trong chat. Prompt tiếng Anh để GPT giữ đúng từng ý.
- Ảnh T-pose sửa từ ảnh A-pose đã duyệt và chỉ đổi tay. Ảnh sau T-pose sửa từ ảnh sau A-pose, đính kèm thêm ảnh trước T-pose để lấy dáng tay. Nếu để GPT tự vẽ lại T-pose từ đầu, thân hay bị lệch (Tavi từng mất gai hai bên thân, tay to ra và có tay áo).
- Claude làm giúp được qua Claude in Chrome, nhưng phải dùng Chrome trên máy Mac chứa repo: ảnh tải về nằm ở `~/Downloads` của Mac, Claude đổi tên và chuyển vào `concept/`. Chrome trên máy Windows tải về không sang được Mac. Ô chat của ChatGPT gửi tin khi gặp dấu xuống dòng, nên prompt được gõ thành một dòng.
- Lưu ảnh nhận về đúng tên ghi ở mỗi bước vào `concept/` của asset. Soát theo "Chuẩn ảnh" và Character Bible rồi mới gửi bước tiếp; chưa đạt thì nhắn sửa đúng điểm sai trong cùng chat.
- Ảnh sau lệch cỡ, lệch vị trí so với ảnh trước, nhắn: `Same back view, but match the exact size and position of the front image: same top of the head, same feet line, same width.`
- GPT ghép hai góc nhìn vào một ảnh, nhắn: `Only one view per image. Generate it again as a single view.`
- Ảnh sau của vật có trang trí lệch một bên (Story Lens): soát xem bố cục đã lật ngang chưa. GPT hay vẽ lại y như mặt trước; khi đó nhắn rõ chi tiết nào chuyển sang bên nào.
- ChatGPT đôi khi đưa hai bản và hỏi "Which image do you like more?": phải chọn một bản thì mới tải được. Nếu nút tải trong khung xem ảnh không ăn, tải bằng link tạo ngay trong trang (Claude làm được qua công cụ JavaScript của Claude in Chrome).

### Lumo: ảnh sau của thân

Đính kèm `Characters/Lumo/concept/lumo_apose_body.png`, lưu `lumo_apose_body_back.png`:
```
The attached image is the approved FRONT view of Lumo, a cute chibi fox character from a soft stylized 3D animated film for young children. Create the BACK view of exactly the same character as one separate image.
- Seen from directly behind, orthographic, no perspective distortion, camera at chest height.
- Exactly the same A-pose (arms straight, about 45 degrees down, palms facing down), same proportions and head size, same size and position in the frame, same canvas: the ear tips and the feet at the same height as in the front image.
- Seen from behind, Lumo's right arm is on the viewer's right.
- The very large ears keep exactly the same shape, size and outward spread as in the front view. Their backs are orange fur with a cream-white upper third (the tips); the pink is only on the inside. The white tuft on top of the head, the back of the head, the neck, the back and the backs of the arms and legs are orange fur. Cream paws and cream feet.
- NO tail: the lower back and bottom are smooth orange fur. No cape, no bag, no clothes.
- Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `lumo_apose_body_back.png`, `lumo_tpose_body.png`; lưu `lumo_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the arms, rotating each whole arm at the shoulder up to point straight out horizontally, parallel to the ground, exactly like the arms in Image 2 (seen from behind). Everything else stays identical to Image 1: head, ears, body, size and position in the frame. The arms keep the same thickness and length.
```

### Lumo: đủ đồ

Đính kèm theo thứ tự `lumo_apose_body.png`, `lumo_cape_ref.png`, `lumo_bag_ref.png`; lưu `lumo_outfit.png`:
```
Image 1 is Lumo's approved front view (body only), from a soft stylized 3D animated film for young children. Image 2 is Lumo's red cape, Image 3 is Lumo's brown shoulder bag. Create ONE new image: Image 1 exactly as it is (same pose, proportions, face, size and position in the frame, same canvas), now wearing the cape and the bag, with the tail.
- Cape from Image 2: red, round gold clasp at the front of the neck, gold cloud pattern along the lower edge. It is LONG: it reaches the knees. It hangs behind the arms; the arms, chest and belly stay visible.
- Bag from Image 3 with its gold cloud buckle, resting on the front of the belly on Lumo's right side (the viewer's left). The strap runs diagonally from the bag up over Lumo's LEFT shoulder (the viewer's right).
- Tail: a big fluffy fox tail, orange with a cream-white tip. It comes out of the lower back through a vertical slit in the middle of the back of the cape and curves out to Lumo's left side (the viewer's right), so part of it shows next to the leg.
- Mouth closed with a gentle smile, eyes looking straight at the camera, as in Image 1.
- Orthographic front view, no perspective distortion. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Lưu `lumo_outfit_back.png`:
```
Now create the BACK view of this outfit image as one separate image: seen from directly behind, orthographic, same pose, same size and position in the frame, same canvas. Seen from behind, Lumo's right side is on the viewer's right.
- The red cape covers the back from the neck down to the knees, with the gold cloud pattern along its lower edge as in Image 2, and no other emblem.
- The bag strap crosses the back diagonally from Lumo's left shoulder (the viewer's left) down to the right hip (the viewer's right), where only the edge of the bag shows.
- The fluffy tail comes out through a vertical slit in the middle of the back of the cape, at the lower back, with its cream-white tip.
- Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Lưu `lumo_tail_ref.png`:
```
From this image, show only Lumo's tail as a separate object: side view, isolated, full length from the root to the tip, same fur, colors and size. No character. Plain flat light-gray background, soft even lighting, no text.
```

### Tavi: thân

Đính kèm `Characters/Tavi/concept/tavi_outfit.png` (ảnh gốc cũ đã xoá; ảnh thân đã sinh xong, bước này chỉ để gen lại), lưu `tavi_apose_body.png`:
```
Edit this image of Tavi, a cute chibi reptile inventor from a soft stylized 3D animated film for young children. Create ONE image in a symmetrical A-pose: arms straight, angled about 45 degrees down from the shoulders. Keep the design, head size, proportions, colors, crystal spikes, leather aviator cap and goggles exactly the same, and apply all of these:
1. Remove the backpack with its blueprint roll and crystal tubes, the belt pouch, the glass tube on the belt and the wrist cuffs. Keep only the fitted beige vest and a simple brown belt.
2. Remove the tail completely. Keep the crystal spikes on the back of the head and along the spine, close to the body.
3. Clear gap between the arms and the body, and between the arms and the crystal spikes.
4. Hands: palms facing down toward the ground (not toward the camera), four fingers straight and slightly apart, thumbs pointing forward.
5. Legs straight, feet flat on the ground, shoulder-width apart, toes pointing forward, clear gap between the legs.
6. Mouth closed with a gentle smile, eyes open looking straight at the camera.
7. Orthographic front view at chest height, no perspective distortion, whole body visible from the top of the spikes to the feet with some margin, centered. Portrait 2:3.
8. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm `tavi_apose_body.png`, lưu `tavi_tpose_body.png`:
```
Use the attached approved A-pose as the base and edit ONLY the arms: rotate each whole arm at the shoulder joint up to a straight T-pose, horizontal at shoulder height, parallel to the ground, palms facing down. Everything else stays identical to the attached image: head, face, cap, goggles, the crystal spikes (including those along both sides of the torso), vest, belt, belly, legs, feet, size and position in the frame. The arms keep exactly the same thickness, length and plain green color: no sleeves, no shoulder pads. One separate image, plain flat light-gray background, no ground shadow, no text.
```
Đính kèm `tavi_apose_body.png`, lưu `tavi_apose_body_back.png`:
```
The attached image is the approved A-pose FRONT view of Tavi. Create its BACK view as one separate image: seen from directly behind, orthographic, exactly the same pose, proportions, size and position in the frame, same canvas. Seen from behind, Tavi's right arm is on the viewer's right.
- The glowing teal crystal crest is wide: a central row of spikes from the top of the head down the spine, plus smaller spikes angled outward on both sides of the back, so that they stick out past both sides of the torso at the same places and sizes as in the front view. Biggest on the head and shoulders, smaller toward the lower back.
- The back of the leather aviator cap and the goggle strap around the back of the head.
- The back of the fitted beige vest and the simple brown belt. No backpack, no pouches.
- NO tail: the lower back and bottom are smooth green skin.
- Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `tavi_apose_body_back.png`, `tavi_tpose_body.png`; lưu `tavi_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the arms, rotating each whole arm at the shoulder up to a straight T-pose exactly like the arms in Image 2 (seen from behind). Everything else stays identical to Image 1: the wide crystal crest with the side spikes, cap, vest, belt, legs, size and position in the frame. Arms the same thickness and plain green. No tail, no backpack.
```

### Tavi: đủ đồ

Đính kèm theo thứ tự `tavi_apose_body.png`, `Props/Inventor_Pack/concept/inventor_pack_ref.png`; lưu `tavi_outfit.png`:
```
Image 1 is Tavi's approved front view (body only), from a soft stylized 3D animated film for young children. Image 2 is Tavi's backpack, the Inventor Pack. Create ONE new image: Image 1 exactly as it is (same pose, proportions, face, size and position in the frame, same canvas), now with the full outfit and the tail:
- A brown leather belt pouch with a gold cloud emblem on Tavi's right hip (the viewer's left), a small glowing glass tube hanging from the belt on Tavi's left hip (the viewer's right), brown leather wrist cuffs.
- The Inventor Pack from Image 2 worn on the back: two shoulder straps over the front of the shoulders, the blueprint roll on top and the glowing crystal tubes peeking out at the sides.
- Tail: green with a cream underside and small teal crystal spikes along its top, coming out from the lower back and curving out to Tavi's right side (the viewer's left), so part of it shows next to the leg.
- Hands palms down, mouth closed with a gentle smile, as in Image 1.
- Orthographic front view, no perspective distortion. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `tavi_outfit.png`, `tavi_apose_body_back.png`, `Props/Inventor_Pack/concept/inventor_pack_ref.png`; lưu `tavi_outfit_back.png`:
```
Image 1 is Tavi's approved outfit FRONT view. Image 2 is Tavi's approved BACK view without the outfit. Image 3 is the Inventor Pack. Create the BACK view of the outfit as one separate image: seen from directly behind, orthographic, same pose as Image 1 and Image 2, same size and position in the frame, same canvas. Seen from behind, Tavi's right side is on the viewer's right. Use Image 2 as the base (same head, cap, goggle strap, crystal crest, arms, legs) and add:
- The Inventor Pack worn on the middle of the back: we see its outer face as in Image 3 (gear emblem, buckles, blueprint roll on top, glowing crystal tubes on both sides). It hangs below the big crystal spikes of the head and shoulders; the spikes do not pass through the pack; the side spikes still peek out past both sides of the torso.
- The brown leather wrist cuffs, the belt with its pouch and glass tube seen from behind.
- The tail comes out from the lower back below the pack, green with a cream underside and small teal crystal spikes along its top, curving to Tavi's right side (the viewer's right).
- Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Lưu `tavi_tail_ref.png`:
```
From these outfit images, show only Tavi's tail as a separate object: side view, isolated, full length from the root to the tip, green with a cream underside and its small teal crystal spikes along the top, same colors and size. No character. Plain flat light-gray background, soft even lighting, no text.
```

### Nori: thân

Đính kèm `Characters/Nori/concept/nori_outfit.png` (ảnh gốc cũ đã xoá; ảnh thân đã sinh xong, bước này chỉ để gen lại), lưu `nori_apose_body.png`:
```
Edit this image of Nori, a small glowing light spirit from a soft stylized 3D animated film for young children. Create ONE image. Keep the round lavender body (head and body are one round shape), face, eyes, rosy cheeks and tiny arms exactly the same, and change only the following:
1. Remove all four wings completely.
2. Remove both antennae and their stars completely.
3. Remove the golden light trail under the body; the bottom of the body is smoothly round, no feet.
4. The tiny arms are held straight out from the body, angled about 45 degrees down, with a clear gap between the arms and the body, palms facing down.
5. Mouth closed with a gentle smile, eyes open looking straight at the camera.
6. Orthographic front view, no perspective distortion, Nori centered with some margin. Portrait 2:3.
7. Plain flat light-gray background, soft even lighting, no glow halo around the body, no ground shadow, no text.
```
Đính kèm `nori_apose_body.png`, lưu `nori_tpose_body.png`:
```
Use the attached approved image as the base and edit ONLY the tiny arms: rotate each arm at the shoulder up to point straight out horizontally, parallel to the ground. Everything else stays identical: body, face, size and position in the frame. The arms keep the same size and shape. One separate image, plain flat light-gray background, no glow halo, no text.
```
Đính kèm `nori_apose_body.png`, lưu `nori_apose_body_back.png`:
```
Create the BACK view of the attached approved front image as one separate image: seen from directly behind, orthographic, same pose, same size and position in the frame, same canvas. Seen from behind, Nori's right arm is on the viewer's right. The back is one smooth round lavender surface: no face, no wings, no antennae, no feet. Plain flat light-gray background, soft even lighting, no glow halo, no ground shadow, no text.
```
Đính kèm theo thứ tự `nori_apose_body_back.png`, `nori_tpose_body.png`; lưu `nori_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the tiny arms, rotating them up to point straight out horizontally exactly like the arms in Image 2 (seen from behind). Everything else stays identical to Image 1.
```

### Nori: đủ đồ

Đính kèm theo thứ tự `nori_apose_body.png`, `nori_wing_ref.png`; lưu `nori_outfit.png`:
```
Image 1 is Nori's approved front view (body only), from a soft stylized 3D animated film for young children. Image 2 shows Nori's right upper and lower wings. Create ONE new image: Image 1 exactly as it is (same pose, face, size and position in the frame, same canvas), now with:
- Four transparent wings like those in Image 2, mirrored for the left side (two bigger upper wings, two smaller lower wings), attached to the back of the body and spreading out to both sides.
- Two thin lavender antennae on top of the head, curving outward, each ending in a small glowing pale-yellow star.
- No feet: under the round body, a short soft trail of golden light that fades out, in place of legs.
- A gentle glow, but the body outline stays sharp and easy to read.
- Orthographic front view, no perspective distortion. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `nori_outfit.png`, `nori_apose_body_back.png`; lưu `nori_outfit_back.png`:
```
Image 1 is Nori's approved outfit FRONT view. Image 2 is Nori's approved BACK view without wings and antennae. Create the BACK view of the outfit as one separate image: use Image 2 as the base (same round body, arms, size and position in the frame, same canvas) and add the same four transparent wings, the two antennae with glowing stars and the golden light trail as in Image 1, all seen from directly behind. Seen from behind, Nori's right side is on the viewer's right. Show clearly where the four wings join the upper back and where the antennae rise from the top of the head. No face. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm `nori_outfit.png`, lưu `nori_wing_ref.png`:
```
From the attached image, show only Nori's two right wings (one upper, one lower) as separate objects, laid out flat and seen straight on, isolated, with their vein pattern and color gradient clearly visible. No character. Plain flat light-gray background, soft even lighting, no text.
```

### Piko: thân

Đính kèm `Characters/Piko/concept/piko_pouch_ref.png` (ảnh gốc cũ đã xoá; ảnh thân đã sinh xong, bước này chỉ để gen lại), lưu `piko_apose_body.png`:
```
Edit this image of Piko, a jelly creature from a soft stylized 3D animated film for young children. Create ONE image. Keep the body shape, the glossy aqua jelly look, the two dark-blue horns, eyes, cheeks and proportions exactly the same, and change only the following:
0. Remove the pouch and its gold cord completely.
1. Mouth closed with a playful smile, no teeth or tongue visible, eyes open looking straight at the camera.
2. The two stubby arms held out from the body, angled about 45 degrees down, with a clear gap between the arms and the body.
3. No bubbles inside the body and no water drops around it.
4. No legs: the wide rounded bottom rests on the ground.
5. Orthographic front view, no perspective distortion, Piko centered with some margin, from the horn tips to the bottom. Portrait 2:3.
6. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm `piko_apose_body.png`, lưu `piko_tpose_body.png`:
```
Use the attached approved image as the base and edit ONLY the stubby arms: rotate each arm at the shoulder up to point straight out horizontally, parallel to the ground. Everything else stays identical: body, horns, face, size and position in the frame. The arms keep the same size and shape. One separate image, plain flat light-gray background, no text.
```
Đính kèm `piko_apose_body.png`, lưu `piko_apose_body_back.png`:
```
Create the BACK view of the attached approved front image as one separate image: seen from directly behind, orthographic, same pose, same size and position in the frame, same canvas. Seen from behind, Piko's right arm is on the viewer's right. The two dark-blue horns seen from behind; the back is one smooth glossy aqua jelly surface with no face, no bubbles, no pouch, no cord. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `piko_apose_body_back.png`, `piko_tpose_body.png`; lưu `piko_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the stubby arms, rotating them up to point straight out horizontally exactly like the arms in Image 2 (seen from behind). Everything else stays identical to Image 1.
```

### Sinh vật nhỏ của thung lũng: thân

Đính kèm `Characters/Valley_Critters/concept/valley_critters_ref.png`, lưu `valley_critter_apose_body.png`:
```
The attached sheet shows the tiny creatures of the Valley of Clouds, background characters of a soft stylized 3D animated film for young children. Create ONE image of one creature with exactly the same design (pale peach-beige bean-shaped body, lighter belly, dot eyes, rosy cheeks, tiny stubby arms and feet) in a neutral reference pose:
1. Standing upright, symmetrical, arms straight out from the body angled about 45 degrees down, clear gap between the arms and the body; feet flat on the ground, slightly apart, clear gap between them.
2. No leaf on the head: the top of the head is visible.
3. Mouth closed with a small smile, eyes looking straight at the camera.
4. Orthographic front view, no perspective distortion, centered with some margin. Portrait 2:3.
5. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm `valley_critter_apose_body.png`, lưu `valley_critter_tpose_body.png`:
```
Use the attached approved image as the base and edit ONLY the arms: rotate each arm at the shoulder up to point straight out horizontally, parallel to the ground. Everything else stays identical: body, face, feet, size and position in the frame. The arms keep the same size and shape. One separate image, plain flat light-gray background, no text.
```
Đính kèm `valley_critter_apose_body.png`, lưu `valley_critter_apose_body_back.png`:
```
Create the BACK view of the attached approved front image as one separate image: seen from directly behind, orthographic, same pose, same size and position in the frame, same canvas. Seen from behind, the creature's right arm is on the viewer's right. A smooth peach-beige back, no face, no leaf, no tail, no wings. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
Đính kèm theo thứ tự `valley_critter_apose_body_back.png`, `valley_critter_tpose_body.png`; lưu `valley_critter_tpose_body_back.png`:
```
Image 1 is the approved A-pose BACK view, Image 2 the approved T-pose FRONT view. Create the T-pose BACK view as one separate image: use Image 1 as the base and edit ONLY the arms, rotating them up to point straight out horizontally exactly like the arms in Image 2 (seen from behind). Everything else stays identical to Image 1.
```

### Đạo cụ

Mỗi đạo cụ một chat: đính kèm `<tên>_ref.png` của nó trong `Props/<Tên>/concept/`, gửi prompt trước (lưu `<tên>_front.png`), rồi prompt sau (lưu `<tên>_back.png`).

**Wonder Compass**
```
The attached image is the Wonder Compass, a magic prop from a soft stylized 3D animated film for young children. Create ONE image of exactly the same object seen straight from the front, orthographic, no perspective: the round gold case with the ring on top, the blue sky dial with white clouds and the glowing eight-pointed star needle, the blue diamond gems and the cream cloud ornament at the bottom of the case. Same design, colors and materials. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the BACK view of the same object as one separate image: seen straight from behind, orthographic, same size and position in the frame. The back of the case is closed, smooth gold metal with a small engraved cloud swirl in the middle; the ring on top, the side gems and the cloud ornament seen from behind. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Inventor Pack**
```
The attached image is the Inventor Pack, Tavi's backpack in a soft stylized 3D animated film for young children. Create ONE image of exactly the same backpack seen straight from the front (the outer side that faces away from the wearer), orthographic, no perspective: blueprint roll and handle on top, flap with buckles, front pocket with the gold gear emblem, glowing crystal tubes on both sides, tool pocket with the wrench. Same design, colors and materials. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the BACK view of the same backpack as one separate image: seen straight from behind, the side that rests against the wearer's back, orthographic, same size and position in the frame. A padded brown leather back panel with two padded shoulder straps and their gold buckles; the blueprint roll, the handle and the crystal tubes seen from behind. No gear emblem on this side. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Story Lens** (hình trong mặt kính thay theo từng manh mối, làm bằng shader, nên ảnh để kính trống)
```
The attached image is the Story Lens, a magic prop from a soft stylized 3D animated film for young children. Create ONE image of exactly the same object seen straight from the front, orthographic, no perspective, handle pointing straight down: round gold frame with white cloud ornaments, lilac crystal gems, the butterfly and crystal on top, purple handle with gold cloud details and a crystal at its end. The glass is clear with a soft lavender shimmer and NO picture inside. Same design, colors and materials. Centered with some margin, portrait 2:3. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the BACK view of the same object as one separate image: seen straight from behind, orthographic, same size and position in the frame. The back of the gold frame, the butterfly, gems and cloud ornaments seen from behind, the handle from behind; the glass is clear with NO picture. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Pocket of Wonders** (Piko rút từng món ra, các món làm riêng, nên túi trống và thắt miệng như lúc đeo)
```
The attached image is the Pocket of Wonders, Piko's magic pouch in a soft stylized 3D animated film for young children. Create ONE image of exactly the same pouch seen straight from the front, orthographic, no perspective, as Piko wears it: purple velvet, its mouth gathered shut by the gold rope bow with the round blue gem, gold tassels on both sides, the cream cloud emblem with gold outline, the gold trim at the bottom. Nothing sticks out of the pouch: no bottle, crystal, mushroom, map, compass, feather, stars or sparkles. Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the BACK view of the same pouch as one separate image: seen straight from behind, orthographic, same size and position in the frame. Same purple velvet, the gold rope and tassels seen from behind, the gold trim at the bottom; plain velvet with no cloud emblem on this side. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

### Đạo cụ tập 01

- Mỗi món một chat, lưu ảnh vào `concept/` của thư mục ghi ở bảng "Hiện trạng".
- Làm máy Rain-O-Matic trước, vì nắp che nút và móc ròng rọc đính kèm ảnh máy. Làm bánh răng trước con vịt, vì ảnh vịt ngậm bánh răng đính kèm ảnh bánh răng.
- `cloud_explorers_character_sheet.png` (trong `01_BRAND/Character_Bible/`) chỉ để lấy phong cách và cỡ so với nhân vật. Cỡ đạo cụ lấy theo previz 2D tập 01.

**Rain-O-Matic 3000.** Đính kèm `cloud_explorers_character_sheet.png`, lưu lần lượt `rain_o_matic_front.png`, `rain_o_matic_back.png`, `rain_o_matic_frost.png`. Mặt trước theo bố cục previz Cảnh 2 (`03_CONTENT/Previz_2D/EP001_Great_Rain_Experiment/canh02/build_shot.py`). Bánh răng, móc, dây ròng rọc làm riêng.
```
The attached sheet shows the characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design the Rain-O-Matic 3000, a cute cartoon rain-making machine built by Tavi the inventor. ONE image, seen straight from the front, orthographic, no perspective, no characters.
- Chunky rounded body of riveted pastel metal panels on four short stubby legs; the body is a little taller than Lumo the fox.
- On top of the body: a round glass dome with a small hatch door that is only a thin metal frame; inside the dome, a glowing blue crystal core with one empty gear socket. A short chimney nozzle on the top right of the body (no clouds in this image).
- A wooden tripod stands on top of the body over the dome, with a small pulley wheel at its peak (no rope, no hook). The peak is almost twice Lumo's height.
- Front face, left half: a round gauge with tick marks and a needle at the top, a round knob below it, and a small pull lever near the bottom. Right half: one big round shiny red push button at Lumo's chest height. A horizontal copper pipe across the middle and a small cloud-shaped plate in the lower center.
- It runs on the crystal core: no electric wires, no plugs, no sparks.
- No text, no letters, no numbers anywhere. Playful, handmade, whimsical.
- Centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the BACK view of the same machine as one separate image: seen straight from behind, orthographic, same size and position in the frame. Exactly the same colors and materials as the front (teal and cream riveted panels, gold rivets and trim, wooden tripod), no purple or lavender anywhere. The four legs, the glass dome with the crystal core, the tripod with its pulley and the chimney nozzle seen from behind (the nozzle is now on the left); no gauge, knob, lever, button or cloud plate on this side. No text. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same machine from the same front view, as one separate image, same size and position in the frame, same teal and cream colors, in its overcooled state:
- The glass dome is covered with thick white frost and puffs of cold mist; through the frost, the golden gear in the socket glows bright gold.
- The small hatch door is frozen and has popped slightly open.
- The pulley rope hangs from the pulley, frozen stiff and white with ice.
- The gauge needle is pushed past the last tick mark and frozen, with frost on the gauge glass; the knob is turned all the way.
- Small icicles along the edge of the dome and the top of the body; the rest of the machine is wet with cold dew.
- Still cute and funny, never scary. No text. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Nắp che nút đỏ** (Cảnh 7). Đính kèm `rain_o_matic_front.png`, lưu `button_cover_front.png` (lắp trên máy), rồi `button_cover_side.png` (riêng cái nắp).
```
The attached image is the Rain-O-Matic 3000 from a soft stylized 3D animated film for young children. Tavi the inventor has built an over-the-top safety cover for its big red button. Create ONE image of the same machine, same front view, same size and position in the frame, with the cover fitted over the red button:
- A clear dome-shaped cover, about ten times bigger than the button, so the red button still shows through it.
- A sturdy hinged frame, a chunky coiled spring, a big latch with a lock, and a small round warning light on top, lit warm orange.
- Same pastel riveted metal and brass as the machine; handmade and a little silly.
- No text, no letters, no numbers. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now only the cover, removed from the machine and isolated, as one separate image, orthographic, no perspective. Keep the parts where they are on the machine: hinge on the dome's left edge, coiled spring on its right edge, lock at the bottom front, warning light on top. Show the cover seen exactly from the spring side (as if walking to the right of the front view and looking at it from there): the front of the cover, with the latch and lock sticking out, faces the viewer's left; the coiled spring faces the viewer, in the middle; the hinge is on the far side and hidden; the dome shows its full depth. Same design, colors and scale. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Bánh răng vàng** (rơi ra từ Chronicle Engine trong Wonder Hub, đài thiên văn cổ: `03_CONTENT/README.md`). Đính kèm `cloud_explorers_character_sheet.png`, lưu `golden_gear_front.png`, `golden_gear_side.png`, `golden_gear_frost.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design a mysterious golden gear that came from an ancient machine inside an old observatory. ONE image, the gear seen straight from the front, orthographic, no perspective, isolated.
- Warm polished gold, eight chunky rounded teeth, a lighter gold inner disc and a softly glowing pale-gold center hub.
- A faint engraved pattern of tiny stars and orbits on the inner disc, like an old astronomer's instrument.
- Small: it fits in a rubber duck's beak and in the palm of Tavi's hand.
- No text, no letters, no numbers. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same gear seen edge-on from the side, orthographic, same scale, as one separate image: the thickness of the gear, the teeth and the center hub are clear. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same gear from the same front view, as one separate image, covered with white frost and tiny ice crystals; the gold still glows faintly through the frost and a few small ice beads bounce off it. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Móc ròng rọc.** Đính kèm `rain_o_matic_front.png`, lưu `pulley_hook_front.png`, `pulley_hook_side.png`. Móc phải nhỏ đủ để thả lọt qua cửa nhỏ trên vòm kính (Cảnh 6).
```
The attached image is the Rain-O-Matic 3000 with its pulley tripod, from a soft stylized 3D animated film for young children. Design its pulley hook as ONE separate object: a chunky cartoon metal hook in dark gray with a rounded blunt tip, an eye ring at the top with a short piece of pale rope tied to it. About the size of Lumo the fox's paw, small enough to drop through a small hatch in the glass dome. Seen straight from the front, orthographic, no perspective, isolated, only the hook (no machine). Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same hook seen straight from the side, rotated 90 degrees, orthographic, same scale, as one separate image: the thickness of the hook, the eye ring seen edge-on and the rope knot are clear. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Vịt cao su.** Đính kèm `cloud_explorers_character_sheet.png`, lưu `rubber_duck_side.png`, `rubber_duck_front.png`. Ảnh thứ ba đính kèm thêm `Props/Golden_Gear/concept/golden_gear_front.png`, lưu `rubber_duck_gear.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design a classic rubber duck toy that Piko the jelly creature pulls out of a magic pouch and keeps as a favorite. ONE image, the duck seen straight from the side facing right, orthographic, no perspective, isolated.
- Bright yellow soft rubber, an orange beak with a small gap between its upper and lower halves (it can hold a small gear), small dark dot eyes, a little upturned tail, a round chubby body with a flat bottom so it floats upright.
- Small: about one sixth of Piko's height, so Piko can hug it with both stubby arms.
- No text, no logos. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same duck seen straight from the front, orthographic, same scale, as one separate image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same duck in a three-quarter view as one separate image, holding the attached golden gear in its beak by the edge of the gear, upright between the upper and lower halves of the beak; the gear glints. Same duck design, colors and proportions. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Thìa** (Cảnh 1). Đính kèm `cloud_explorers_character_sheet.png`, lưu `spoon_top.png`, `spoon_side.png`, `spoon_bent.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design an ordinary but cute metal spoon that Piko the jelly creature pulls out of a magic pouch. ONE image, the spoon seen straight from above, orthographic, no perspective, isolated, bowl at the top and handle pointing down.
- Polished silver-gray metal with soft rounded edges, an oval bowl, a slightly chunky handle with a rounded end. No engraving.
- About a quarter of Piko's height.
- No text, no logos. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same spoon seen straight from the side, orthographic, same scale, as one separate image: the curve of the bowl and the thickness of the handle are clear. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same spoon after digging very hard ground, side view, same scale, as one separate image: the handle is bent into a U shape in the middle, and the bowl has a little dry dirt on it. Funny, not broken. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Ô** (Cảnh 7). Đính kèm `cloud_explorers_character_sheet.png`, lưu `umbrella_open.png`, `umbrella_closed.png`, `umbrella_inverted.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design a small umbrella that Piko the jelly creature pulls out of a magic pouch. ONE image: the umbrella open, seen straight from the side, orthographic, no perspective, isolated.
- A round canopy of eight panels in soft pastel pink with small white polka dots, rounded tips, a short wooden shaft and a curved wooden handle.
- Sized for Piko: the open canopy is a little wider than Piko's body.
- No text, no logos. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same umbrella closed and folded, seen straight from the side, same scale, as one separate image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same umbrella blown inside out by the wind, as one separate image, same scale: the canopy flipped upward like a bowl and full of clear rain water to the brim, the handle pointing down, seen from the side and slightly above so the water surface shows. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Hộp ốc** (Nori xếp ốc theo cỡ ở Cảnh 2; cuối Cảnh 6 bánh răng được cất vào đây, Tavi đóng nắp). Đính kèm `cloud_explorers_character_sheet.png`, lưu `screw_box_front.png`, `screw_box_open.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design the screw box of Tavi the inventor: a small wooden box with a hinged lid. ONE image: the box closed, seen straight from the front, orthographic, no perspective, isolated.
- Warm honey-brown wood with rounded edges, brass corner caps, a brass hinge at the back and a simple brass latch at the front.
- About half as wide as Tavi is tall.
- No text, no letters, no numbers. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same box with the lid open, seen from the front and a little above, as one separate image: inside, three compartments from left to right hold big, medium and small chunky cartoon screws with round heads, neatly sorted by size. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Cuộn dây của Noah** (Cảnh 5–6: dắt đôi voi, rồi buộc móc ròng rọc vào đầu dây để rút bánh răng; độ dài dây chỉnh trong Blender). Đính kèm `cloud_explorers_character_sheet.png`, lưu `noah_rope_ref.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design a small coil of thick natural rope that kind old Noah drops from his big wooden boat. ONE image, seen straight from the front, orthographic, isolated: a neat round coil of golden-tan twisted hemp rope, with one loose end hanging down. Small enough for Lumo the fox to hold in front of the belly with both paws. No text. Plain flat light-gray background, soft even lighting, no ground shadow.
```

**Con thuyền.** Đính kèm `01_BRAND/Brand_Guideline/world_key_art.png`, lưu `noah_ark_side.png`, `noah_ark_front.png`. Thú trên boong không nằm trong ảnh này.
```
The attached image is a style reference only (soft stylized 3D animated film for young children). Design Noah's giant wooden boat for a storybook world. ONE image: the whole boat seen straight from the side, orthographic, no perspective, isolated, floating level; no water, no characters, no animals.
- A huge, gentle, rounded wooden ark, as tall as a small hill: a long chunky hull of warm honey-brown planks with soft rounded edges, a simple wooden house with a pitched roof on the deck, small round windows along the house, a wooden railing around the deck with one opening for a plank ramp. No ramp in this image (the ramp is a separate object); below the opening, show the hull planks.
- Handmade and cozy, never scary. No flags, no symbols, no text.
- Wide 16:9. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same boat (without a ramp) seen straight from the front (the bow), orthographic, same scale, as one separate image. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Cầu ván** (bắc từ mỏm đồi lên mạn thuyền; Nori để một chấm sáng trên từng nẹp, Lumo bước lên từng chấm). Đính kèm `world_key_art.png`, lưu `plank_bridge_side.png`, `plank_bridge_top.png`.
```
The attached image is a style reference only (soft stylized 3D animated film for young children). Design a long wooden plank ramp for walking animals up into a big wooden boat. ONE image, the ramp lying flat and seen straight from the side, orthographic, no perspective, isolated (it is tilted into place later in 3D).
- Two or three wide weathered planks side by side, eight evenly spaced wooden cleats nailed across the top, rope lashings at both ends, soft rounded edges, warm wood.
- Wide enough for a baby elephant to walk on.
- No text. Wide 16:9. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same ramp seen straight from above, orthographic, same scale, as one separate image, with the eight cleats clearly visible. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

### Nhân vật phụ tập 01

**Đôi voi con** (có diễn: nắm dây và vạt áo choàng bằng vòi, bắt chước nhịp bước của Lumo). Đính kèm `cloud_explorers_character_sheet.png`, lưu `baby_elephants_ref.png`, rồi `baby_elephant_front.png`, `baby_elephant_side.png`, `baby_elephant_back.png`. Voi thứ hai dựng từ model voi thứ nhất, đổi cỡ, tai, chỏm lông theo ảnh thiết kế.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design TWO baby elephants, side characters from a storybook world who want to climb into a big wooden boat to play with their animal friends.
- Cute and round: big heads, short legs, walking on four legs, short trunks that can hold a rope, big soft ears, tiny tails.
- Each about as tall as Lumo the fox; the second one a little smaller.
- Soft warm stone-gray skin with pale pink inner ears. The first one has a small tuft of hair on top of the head; the second one has rounder ears and rosy cheeks, so the two are easy to tell apart. No orange, green, lavender or aqua.
- Shy, sweet expressions, mouths closed with small smiles.
A design sheet: the two elephants side by side in a three-quarter view, standing on four legs. Plain flat light-gray background, soft even lighting. No text, no labels, no logos, no watermark.
```
```
Now only the first (bigger) elephant, as one separate image, in a neutral reference pose: standing on all four legs, legs straight and slightly apart, feet flat, trunk hanging straight down and relaxed, ears relaxed, mouth closed with a small smile, no rope. Seen straight from the front, orthographic, no perspective, centered with some margin, square 1:1. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same elephant in the same neutral pose seen straight from its left side, facing the viewer's left, orthographic, no perspective, same scale, as one separate image: head in a true side profile like the body, trunk hanging straight down, tiny tail hanging down, no rope. The ears stand out sideways as in the front view, so the left ear is seen from behind and edge-on: its gray outer back, foreshortened, with only a thin pink rim, not the pink inner side. Square 1:1, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the same elephant in the same pose seen straight from behind, orthographic, same size and position in the frame as the front view, square 1:1, as one separate image: the gray backs of the two ears standing out sideways exactly as in the front view, the tuft of hair on top of the head, the back, the four legs and the tiny tail hanging down. No rope. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Noah** (trong phim chỉ thấy dáng ngược sáng trong nắng vàng ấm trên boong và bàn tay, không thấy rõ mặt: kịch bản tập 01, Cảnh 5). Đính kèm `cloud_explorers_character_sheet.png`, lưu `noah_front.png`, `noah_side.png`, `noah_hand_front.png`, `noah_hand_back.png`.
```
The attached sheet shows the style of a soft stylized 3D animated film for young children; use it for style only. Design kind old Noah from a storybook world, as a shape reference for a character who is only ever seen as a warm backlit silhouette on his boat. ONE image, full body, standing upright and calm, arms relaxed and slightly away from the body, seen straight from the front, orthographic, no perspective.
- Tall and gentle, about two and a half times Lumo's height, broad shoulders, a long simple robe with a rope belt, a hooded cloak, a long soft white beard and long white hair.
- The face is very simple and calm, mostly hidden by the beard and the soft shadow of the hood, with no detailed features.
- Soft rounded stylized shapes, warm earthy colors (sand, brown, cream). No symbols, no text.
- Portrait 2:3, centered with some margin. Plain flat light-gray background, soft even lighting, no ground shadow.
```
```
Now the same figure in the same calm standing pose seen straight from his left side, facing the viewer's left, orthographic, same scale, as one separate image: the outline of the hood, beard, cloak and robe is clear, arms relaxed down at his sides, same sandals. Portrait 2:3. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now only Noah's right hand and forearm in its cream sleeve, isolated, as one separate image, seen from the palm side with the fingers pointing up: a large, kind, weathered hand in the same style and skin tone, fingers relaxed and slightly open, thumb clearly visible. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```
```
Now the very same hand and sleeve turned around, seen from the back of the hand, as one separate image: knuckles and fingernails face the viewer, fingers pointing up in the same spread, so the thumb is now on the opposite side of the image. Same size and position. Plain flat light-gray background, soft even lighting, no ground shadow, no text.
```

**Thú trên boong** (nhân vật nền Cảnh 5: vẫy gọi đôi voi, reo khi đôi voi lên tới boong). Đính kèm `cloud_explorers_character_sheet.png`, lưu `ark_animals_ref.png`. Chỉ dựng phần thấy trên mạn thuyền.
```
The attached sheet shows the four main characters of a soft stylized 3D animated film for young children; use it for style and scale only. Design the background animals that wave from the deck of Noah's big wooden boat in a storybook world: one rabbit, two small birds and one giraffe whose long neck pops up above the railing.
- Cute, round and simple, so they never compete with the main characters.
- Soft pastel colors that are not orange, green, lavender or aqua; happy expressions with closed-mouth smiles.
A design sheet: each animal in a three-quarter view, waving. Plain flat light-gray background, soft even lighting. No text, no labels, no logos, no watermark.
```

## Dựng trong Blender

Mỗi asset một build script dựng lưới, xương, face rig, material ra `<tên>_rig.blend` (`README.md`).

| | Thân (rig) | Làm riêng rồi gắn |
|---|---|---|
| **Lumo** | Thân 2 chân; xương tai; mặt | Áo choàng, túi đeo chéo, đuôi |
| **Tavi** | Thân 2 chân liền mũ, kính, gile ôm sát; gai tinh thể đi cứng theo ngực; mặt | Đuôi, Inventor Pack |
| **Nori** | Thân tròn, tay nhỏ, bay lơ lửng; mặt | 4 cánh trong suốt, 2 râu sao, vệt sáng thay chân |
| **Piko** | Thân co giãn bằng shape keys, tay nhỏ, sừng nảy; mặt | Pocket of Wonders: dây quàng gốc sừng phải, túi đung đưa theo cú nảy |
| **Sinh vật nhỏ** | Thân, tay chân ngắn | Lá khô đội đầu (trượt xuống che mắt, `valley_critters_ref.png`) |
| **Đôi voi con** | Thân 4 chân, vòi nắm được dây, tai; mặt. Voi thứ hai là bản đổi cỡ, tai, chỏm lông của voi thứ nhất | — |
| **Noah** | Chỉ dáng người và bàn tay; không rig mặt | — |

- **Mặt:** mắt, mí, đồng tử, lông mày là bộ phận rời gắn vào xương đầu; miệng là shape key bám trên bề mặt mõm; tất cả điều khiển bằng thanh trượt (custom property + driver) trên rig.
- **Lưới, texture:** quad, mỗi nhân vật dưới khoảng 50k mặt; texture 2048 là đủ (phim 1080p; 4096 nặng cho EEVEE trên Vega 11).
- Scale theo chiều cao trong Character Bible.
- Soát **bàn tay úp, ngón không dính nhau, miệng khép** trước khi rig.
- Kiểm tra rig bằng `pipeline/rig_qa.py` (ngưỡng đạt trong `pipeline/README.md`) trên các tư thế khó: giơ tay, bật nhảy, ngoái đầu, cúi.

### Gắn đồ rời (áo choàng, túi của Lumo; ba lô của Tavi)

Làm sau khi rig thân đã đạt kiểm tra.

| | Áo choàng | Túi đeo chéo / ba lô |
|---|---|---|
| Dựng | Theo `lumo_cape_ref.png`, đặt theo `lumo_outfit.png` và `lumo_outfit_back.png`. Lỗ cổ ôm mặt cắt vai; từ khuy trở xuống vạt áo rủ ra sau cánh tay (áo bọc kín quanh người thì tay đưa ra trước là áo phồng và nhăn) | Túi theo `lumo_bag_ref.png`: thân túi đặt trước bụng, lệch phải, đi cứng theo xương hông; dây dựng bằng code, vòng elip chéo từ hông phải qua vai trái, bám mặt da. Ba lô theo `inventor_pack_front.png`, `inventor_pack_back.png`, đặt theo `tavi_outfit_back.png` |
| Đi theo người | Chép trọng số da từ thân (Data Transfer), chỉ giữ ảnh hưởng của hông, lưng, ngực, cổ, vai; cánh tay 20%, đùi 30%; đầu, tai, đuôi, cẳng tay, cẳng chân không kéo áo | Dây: như áo choàng |

- **Áo choàng của Lumo dài tới gối** như concept. Đuôi mọc ở độ cao 0.2–0.3 m, thấp hơn mép áo, nên giữa lưng áo phải có khe xẻ cho đuôi thò ra. Chân bước dễ xuyên vạt áo, nên áo bắt buộc có xương vạt áo và va chạm với chân.
- **Kiểm tra:** đếm số đỉnh áo, dây lún vào người ở từng tư thế; giơ tay và chạy là hai tư thế dễ lún nhất.
- **Chưa có:** xương vạt áo (để áo bay khi chạy và tránh chân), khe đuôi, va chạm với chân, túi lắc theo bước. Mô phỏng vải (Cloth) chỉ dùng cho vài cận cảnh cần "wow" (áo quật trong bão): chậm, phải tính lại từng shot, dễ xuyên người.
