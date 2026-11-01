# Làm nhân vật và đạo cụ 3D bằng Meshy

Meshy sinh hình (và rig thân cho nhân vật 2 chân). Blender làm tiếp bằng code những phần Meshy không làm được: đồ rời, đuôi, cánh, mặt, shader. Hình dáng, màu, chiều cao: [`01_BRAND/Character_Bible/`](../01_BRAND/Character_Bible/README.md).

## Gói và nơi làm

- **Gói Pro** (527.000 đ/tháng, giá tra ngày 01/11/2026): 1.000 credit/tháng, tải không giới hạn, file riêng tư thuộc về mình, có Remesh, thư viện hơn 600 động tác. Gói Free không dùng được: không có Remesh, chỉ 20 động tác, file bị công khai theo CC BY 4.0.
- **Làm trên web Meshy:** xem và chọn bản trực tiếp, sửa điểm khớp bằng tay, rig miễn phí. Model nằm trong workspace của tài khoản.
- **Credit:** sinh hình thô 20, tô texture 10, Text to Motion 3. Rig và animation có sẵn trên web: miễn phí.
- **Meshy MCP** (`@meshy-ai/meshy-mcp-server`, cần gói Pro) chỉ nên dùng khi sản xuất hàng loạt. Qua MCP, rig và Remesh tốn 5 credit mỗi lần, model chỉ giữ 3 ngày trên server và không hiện trên web.

## Meshy rig được gì

| Loại rig | Dùng cho | Thư viện animation |
|---|---|---|
| **Humanoid** | Nhân vật 2 tay, 2 chân (Lumo, Tavi) | Hơn 600 động tác + Text to Motion |
| Quadruped | Thú 4 chân | Chỉ 1 động tác đi |
| Smart Rig | Sinh vật khác, robot, đồ vật | Không dùng được thư viện |

Meshy **không rig mặt** và **không rig phần thừa** (đuôi, cánh, râu).

## Phân việc cho từng nhân vật

| | Meshy | Blender (build script của nhân vật) |
|---|---|---|
| **Lumo** | Thân, rig Humanoid, animation | Áo choàng, túi đeo chéo, đuôi (làm riêng rồi gắn); xương tai; mặt |
| **Tavi** | Thân kèm mũ, kính, gile ôm sát; rig Humanoid; animation | Đuôi (làm riêng); gai tinh thể đi cứng theo ngực; mặt |
| **Nori** | Chỉ hình thân (không cánh, không râu) | Rig toàn bộ: thân tròn, tay nhỏ, 4 cánh trong suốt, 2 râu sao, bay lơ lửng; mặt |
| **Piko** | Chỉ hình thân | Rig toàn bộ: co giãn bằng shape keys, tay nhỏ, sừng nảy; mặt |

## Ảnh đầu vào chuẩn

Meshy dựng hình đúng theo ảnh: ảnh sai tư thế thì model và rig sai theo. Kiểm tra ảnh trước khi đưa vào Meshy.

Lumo và Tavi (rig Humanoid):
1. **A-pose hoặc T-pose, đối xứng:** tay **thẳng**. A-pose: tay dang chéo xuống khoảng 45°. T-pose: tay dang ngang tầm vai, song song mặt đất. Có khe hở rõ giữa tay và thân. Chân thẳng, bàn chân đặt phẳng, rộng bằng vai, mũi chân hướng thẳng ra trước.
   - A-pose: vai biến dạng đẹp hơn khi tay buông xuống (tư thế hay gặp nhất).
   - T-pose: tay tách xa thân nhất nên Meshy dễ đặt khớp vai, khuỷu, cổ tay; hợp với nhân vật bụng tròn tay ngắn như Lumo, Tavi.
   - Sinh thử cả hai cho Lumo, giữ bản nào qua `rig_qa.py` tốt hơn rồi dùng cùng tư thế đó cho Tavi.
2. **Bàn tay úp:** lòng bàn tay **hướng xuống đất**, ngón tay duỗi thẳng và hơi tách nhau, ngón cái hướng ra trước. Ảnh có lòng bàn tay ngửa ra phía trước thì model sinh ra bị ngửa tay, rig Humanoid giữ nguyên tư thế sai đó nên animation trông gượng.
3. **Thấy rõ khớp:** cằm và cổ, vai, khuỷu tay, cổ tay, háng, đầu gối, cổ chân. Meshy đặt điểm đánh dấu xương đúng ở những chỗ này.
4. **Đầu to là rủi ro:** Meshy chỉ ghi rằng tỉ lệ càng gần người thì tay chân càng ít méo. Concept có đầu gần bằng nửa chiều cao, cần sinh thử Lumo trước để biết Meshy còn đặt khớp đúng không.
5. **Không đồ rộng, không cầm đồ.** Đồ ôm sát (mũ, gile) để liền được. Áo choàng, túi, bảo bối là model riêng (xem "Gắn đồ rời").
6. **Không có phần chĩa xa khỏi thân** (đuôi). Meshy sẽ gắn nó vào xương chân, nhấc chân là đuôi méo theo. Ảnh chính diện không thấy đuôi thì Meshy vẫn có thể tự thêm đuôi phía sau (đã gặp với Lumo): khi đó tách đuôi và gán lại trong Blender.

Mọi nhân vật:
- **Biểu cảm trung tính:** miệng khép, cười nhẹ, mắt mở nhìn thẳng. Miệng há (răng, lưỡi) tạo hốc lưới khó xử lý; biểu cảm do face rig làm.
- **Máy quay:** chính diện, ngang tầm ngực, không méo phối cảnh, thấy trọn từ đỉnh tai tới bàn chân, chừa lề.
- **Nền và ánh sáng:** nền xám nhạt trơn, ánh sáng đều, không bóng đổ xuống đất, không chữ, chỉ một nhân vật.
- **Mặt:** Meshy vẽ mắt miệng lên texture, không cử động được. Giữ mặt đơn giản để làm vị trí tham chiếu. Trong Blender tô lại vùng mặt bằng màu da rồi làm face rig: mắt, mí, đồng tử, lông mày là các bộ phận rời gắn vào xương đầu; miệng là shape key bám trên bề mặt mõm; tất cả điều khiển bằng thanh trượt (custom property + driver) trên rig.
- **Trong suốt, phát sáng:** Meshy chỉ ra màu đặc. Thân thạch của Piko, ánh sáng của Nori, tinh thể của Tavi làm lại bằng shader trong Blender.

## Các bước trên web

1. **Ảnh đầu vào** cho **Image to 3D**: một đối tượng, nền trơn, chỉ gồm phần Meshy làm (bảng dưới). Chưa có ảnh đạt thì dùng **Text to 3D** với prompt bên dưới.
2. Lumo, Tavi: đặt **Pose** khớp với ảnh (**A-Pose** hoặc **T-Pose**). Mọi nhân vật: bật **Symmetry**. Texture **2048** là đủ (phim 1080p; 4096 nặng cho EEVEE trên Vega 11).
3. Sinh 4 bản, chọn bản tách rõ tay khỏi thân, chân khỏi nhau, rồi mới chạy Texture/Refine.
4. **Remesh:** Quad, khoảng 20–50k mặt (máy Vega 11 chỉ nên dùng dưới 50k).
5. Lumo, Tavi: **Rig → Humanoid**, kiểm tra điểm đánh dấu ở 7 khớp. Sai thì bấm **Re-rig** rồi kéo lại. Chọn animation (idle, walk, run, jump, surprised, laugh, think…), không có sẵn thì thử Text to Motion.
6. **Tải về:** FBX, skeleton template **Mixamo** (mặc định), kèm animation. Mỗi animation là một FBX riêng có cả da (`..._Animation_<tên>_withSkin.fbx`), texture nhúng sẵn trong FBX và có thêm bản PNG đi kèm. Giải nén vào `Characters/<Tên>/source/<tên>_meshy_vNN/`, giữ nguyên tên file của Meshy.

**Đạo cụ** không cần rig.

### Ảnh đầu vào hiện có

| Asset | File trong `concept/` | Dùng được chưa | Cần sửa trước khi đưa vào Meshy |
|---|---|---|---|
| Lumo | `lumo_apose_meshy.png`, `lumo_tpose_meshy.png` | ✅ | — (đã bỏ áo choàng, túi; bàn tay úp; miệng khép; chân có khe hở) |
| Tavi | `tavi_apose.png` | ❌ | Bỏ ba lô, túi đeo, ống, cuộn giấy, đuôi; úp bàn tay. Mũ, kính, gile ôm sát giữ lại |
| Nori | `nori_ref.png` | ❌ | Bỏ 4 cánh, 2 râu, 2 mẩu chân |
| Piko | `piko_ref.png` | ❌ | Khép miệng (miệng há tạo hốc lưới, biểu cảm do face rig làm) |
| Wonder Compass | `wonder_compass_ref.png` | ✅ | Kim la bàn phải quay được: làm kim riêng trong Blender, mặt kính làm bằng shader |
| Inventor Pack | `inventor_pack_ref.png` | ✅ | Ống tinh thể phát sáng làm bằng shader |
| Story Lens | `story_lens_ref.png` | ✅ | Hình trong mặt kính thay theo từng manh mối: làm bằng shader, không để Meshy vẽ cố định |
| Pocket of Wonders | `pocket_of_wonders_ref.png` | ⚠️ | Đồ thò ra miệng túi sẽ dính liền vào túi. Piko cần rút từng món ra (thìa, vịt, ô), nên tốt hơn là túi rỗng, các món làm riêng |

### Prompt sửa ảnh bằng GPT

Tải ảnh gốc lên GPT kèm prompt. Ảnh nhận về lưu cạnh ảnh gốc, thêm hậu tố mô tả (`lumo_apose_meshy.png`, `lumo_tpose_meshy.png`), rồi soát lại theo "Ảnh đầu vào chuẩn" trước khi đưa vào Meshy. Prompt tiếng Anh để GPT giữ đúng từng ý.

**Lumo và Tavi:** một prompt ra 2 ảnh riêng, A-pose và T-pose. Nếu GPT ghép 2 tư thế vào một ảnh hoặc chỉ ra 1 ảnh, nhắn tiếp: `Now generate the T-pose version as a separate image, same rules.`

**Lumo** (từ `lumo_apose.png`, lưu `lumo_apose_meshy.png` và `lumo_tpose_meshy.png`):
```
Edit this image and create TWO SEPARATE IMAGES of the same character, one pose per image (not side by side in one image):
- Image 1: symmetrical A-pose, arms straight, angled about 45 degrees down from the shoulders.
- Image 2: symmetrical T-pose, arms straight, extended horizontally out to the sides at shoulder height, parallel to the ground.
In both images keep the character design, head size, proportions, colors, fur style, lighting and camera exactly the same, and apply all of these:
1. Remove the red cape and its gold clasp completely. Show the orange fur of the shoulders, arms and back where the cape was.
2. Remove the brown shoulder bag and its strap completely. No tail.
3. Clear gap between the arms and the body, and between the arms and the head.
4. Hands: palms facing down toward the ground (not toward the camera), fingers straight and slightly apart, thumbs pointing forward.
5. Legs straight, feet flat on the ground, shoulder-width apart, toes pointing forward, clear gap between the legs.
6. Neutral friendly face: mouth closed with a gentle smile, eyes open looking straight at the camera.
7. Front view at chest height, no perspective distortion, whole body visible from the ear tips to the feet with some margin.
8. Plain flat light gray background, soft even lighting, no ground shadow, no text.
```

**Tavi** (từ `tavi_apose.png`, lưu `tavi_apose_meshy.png` và `tavi_tpose_meshy.png`):
```
Edit this image and create TWO SEPARATE IMAGES of the same character, one pose per image (not side by side in one image):
- Image 1: symmetrical A-pose, arms straight, angled about 45 degrees down from the shoulders.
- Image 2: symmetrical T-pose, arms straight, extended horizontally out to the sides at shoulder height, parallel to the ground.
In both images keep the character design, head size, proportions, colors, crystal spikes, leather aviator cap and goggles exactly the same, and apply all of these:
1. Remove the backpack, the scrolls, the glass tubes, the belt pouches and the wrist cuffs. Keep only the fitted beige vest and a simple belt.
2. Remove the tail completely. Keep the crystal spikes along the back of the head and the spine, close to the body.
3. Clear gap between the arms and the body, and between the arms and the crystal spikes.
4. Hands: palms facing down toward the ground (not toward the camera), four fingers straight and slightly apart, thumbs pointing forward.
5. Legs straight, feet flat on the ground, shoulder-width apart, toes pointing forward, clear gap between the legs.
6. Neutral friendly face: mouth closed with a gentle smile, eyes open looking straight at the camera.
7. Front view at chest height, no perspective distortion, whole body visible with some margin.
8. Plain flat light gray background, soft even lighting, no ground shadow, no text.
```

**Nori** (từ `nori_ref.png`):
```
Edit this image. Keep the round glowing lavender body, face, eyes, cheeks and tiny arms exactly the same. Change only the following:
1. Remove all four wings completely.
2. Remove both antennae and their stars completely.
3. Remove the two small feet at the bottom; the bottom of the body is smoothly round.
4. Tiny arms held slightly away from the body, palms facing down.
5. Mouth closed with a gentle smile, eyes open looking straight at the camera.
6. Front view, no perspective distortion, plain flat light gray background, soft even lighting, no glow halo around the body, no text.
```

**Piko** (từ `piko_ref.png`):
```
Edit this image. Keep the aqua jelly body, horns, eyes, cheeks, bubbles and stubby arms exactly the same. Change only the face: mouth closed with a playful smile, no teeth or tongue visible, eyes open looking straight at the camera. Front view, no perspective distortion, plain flat light gray background, soft even lighting, no text.
```

**Pocket of Wonders** (từ `pocket_of_wonders_ref.png`):
```
Edit this image. Keep the purple velvet bag, gold rope, tassels, cloud emblem and gold trim exactly the same. Remove everything sticking out of the bag (bottle, crystal, mushroom, map, compass, feather, stars, sparkles). The bag is open at the top and empty inside, the opening is visible. Plain flat light gray background, soft even lighting, no text.
```

**Áo choàng và túi của Lumo** (ảnh tham chiếu để làm đồ rời, từ `lumo_apose.png`):
```
From this image, show only the red cape with its gold clasp, laid out flat and seen from the back, so the full shape and the gold cloud pattern along the edge are visible. No character. Plain flat light gray background, soft even lighting, no text.
```
```
From this image, show only the brown leather shoulder bag with its strap, front view, isolated. No character. Plain flat light gray background, soft even lighting, no text.
```
Lưu thành `lumo_cape_ref.png` và `lumo_bag_ref.png`.

## Prompt Text to 3D

Prompt tiếng Anh, màu ghi bằng chữ (Meshy không đọc mã hex).

**Negative (dùng chung):**
```
realistic, photorealistic, sharp teeth, open mouth, palms facing forward, scary, horror, angry, holding objects, base, pedestal, multiple characters, text, logo, arms touching the body, crossed arms, hands on hips, legs together, sitting, crouching, kneeling, jumping
```

**LUMO** (không áo choàng, túi, đuôi) — Negative thêm: `cape, bag, tail`
```
Cute chibi fox character with a humanoid body, standing upright on two legs in A-pose, straight arms held out diagonally away from the body, palms facing down, legs slightly apart, big round head, very large pointed ears with pink inner ears, small white tuft of fur on top of the head, big shiny brown eyes, closed mouth with a gentle smile, short muzzle with a small dark nose, visible chin and neck, orange fur with cream white belly, chest, muzzle and paws, short arms with visible elbows, small rounded paw hands, short legs with visible knees, big soft paw feet, no clothes, no cape, no bag, no tail. Soft stylized 3D, rounded shapes, soft fur look, pastel colors, kids animation style, full body, front view, symmetrical
```

**TAVI** (không đuôi) — Negative thêm: `tail, backpack`
```
Cute chibi little green reptile inventor with a humanoid body, standing upright on two short legs in A-pose, straight arms held out diagonally away from the body, palms facing down, legs apart, round head with big green eyes and a closed-mouth friendly smile, grass green skin with cream belly and cream muzzle, a row of glowing teal crystal spikes along the back lying close to the body, brown leather aviator cap with round goggles on the forehead, fitted beige vest with a brown belt, hands with four fingers, visible elbows and knees, no tail. Soft stylized 3D, rounded shapes, smooth matte clay surfaces, pastel colors, kids animation style, full body, front view, symmetrical
```

**NORI** (chỉ thân) — Negative thêm: `wings, antennae, legs`
```
Cute small round glowing light spirit, head and body merged into one soft round shape, lavender purple with a soft inner glow, big gentle violet eyes, small smile, rosy cheeks, two tiny arms, no legs, no wings, no antennae, front view. Soft stylized 3D, rounded shapes, smooth surfaces, pastel colors, kids animation style, symmetrical
```

**PIKO** (chỉ thân) — Negative thêm: `legs`
```
Cute bright aqua blue jelly slime creature, soft rounded blob body wider at the bottom, two dark blue rounded horns on top, very big shiny blue eyes, closed mouth with a playful smile, two small stubby arms, no legs, glossy jelly surface. Soft stylized 3D, rounded shapes, smooth glossy surfaces, pastel colors, kids animation style, front view, symmetrical
```

**Rain-O-Matic 3000** (máy tạo mưa tập 01, chưa có concept)
```
Cute cartoon rain-making machine, chunky rounded body made of riveted pastel metal panels, large glowing blue crystal core in a glass dome on top, small rain cloud nozzle, row of colorful dials and a slider for intensity, one big round red button labeled MAX POWER, short stubby legs, playful whimsical design. Soft stylized 3D, smooth surfaces, pastel colors, kids animation style
```

## Sau khi tải về

- Scale theo chiều cao trong Character Bible (Lumo 1.00 · Tavi 0.85 · Nori 0.70 · Piko 0.80).
- Rig Meshy là khung Mixamo **24 xương, không có xương ngón tay** (bàn tay cử động một khối), tên xương kiểu `mixamorig:Head`. Xương thêm vào (tai, đuôi, ngón nếu cần) và bộ phận mặt gắn vào các xương này.
- Kiểm tra rig bằng `pipeline/rig_qa.py` trên các tư thế khó (giơ tay, bật nhảy, ngoái đầu, cúi). Đạt khi bad% dưới khoảng 2% và thể tích gần 1.0.
- Mở model trong Meshy hoặc Blender, soát **bàn tay úp, ngón không dính nhau, miệng khép** trước khi rig. Sai thì sửa ảnh rồi sinh lại, không rig tiếp.

## Gắn đồ rời (áo choàng, túi của Lumo; ba lô của Tavi)

Làm sau khi rig thân đã đạt `rig_qa.py`. Trình tự: thân → túi → áo choàng → chạy lại kiểm tra với tư thế đi, chạy, giơ tay, đo chỗ áo xuyên vào người.

| | Áo choàng | Túi đeo chéo / ba lô |
|---|---|---|
| Làm ra | Dựng bằng code trong Blender: tấm vải cong, lưới tứ giác đều để uốn mượt (lưới Meshy không đều). Hoa văn mây vàng đắp bằng texture theo `lumo_cape_ref.png` | Meshy Image to 3D từ ảnh riêng của món đồ (`lumo_bag_ref.png`), không rig |
| Khớp vào người | Đặt khít vai ở A-pose. Cổ áo và khuy vàng đi cứng theo xương ngực | Dây đeo là dải mỏng bám theo da thân (Surface Deform hoặc chép trọng số da từ thân), nên biến dạng theo ngực. Thân túi là vật cứng treo vào hông |
| Chuyển động | 3–4 đốt xương dọc lưng áo. Code tạo độ trễ: chạy thì áo bay ra sau, dừng thì đung đưa rồi rủ xuống. Chồng lên mọi animation lấy từ thư viện Meshy | Lắc nhẹ theo nhịp bước bằng code. Cảnh lấy đồ trong túi thì chuyển túi sang đi theo tay |

- **Mô phỏng vải (Cloth)** chỉ dùng cho vài cận cảnh cần "wow" (áo quật trong bão): chậm, phải tính lại từng shot, dễ xuyên người.
- **Áo choàng dài tới gối sẽ chạm chân khi bước.** Khi dựng áo: cho áo hơi xòe ra sau, hoặc ngắn bớt, hoặc thêm va chạm với chân.
- Đồ rời là object riêng nên bật tắt được theo cảnh (ví dụ Lumo không mặc áo choàng).

## Nguồn (tra ngày 01/11/2026)

[Pricing](https://www.meshy.ai/pricing) · [Credits guide](https://www.meshy.ai/tutorials/meshy-credits-guide) · [Rigging guide](https://docs.meshy.ai/en/webapp/guides/3d-model/rigging) · [Animate guide](https://docs.meshy.ai/en/webapp/guides/animate) · [MCP guide](https://www.meshy.ai/tutorials/meshy-mcp-guide) · [API asset retention](https://docs.meshy.ai/en/api/asset-retention)
