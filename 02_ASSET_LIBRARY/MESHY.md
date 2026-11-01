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

## Quy tắc khi sinh hình

Lumo và Tavi (rig Humanoid):
1. **A-pose:** tay dang chéo xuống khoảng 45°, có khe hở giữa tay và thân, hai chân tách nhau.
2. **Thấy rõ khớp:** cằm và cổ, vai, khuỷu tay, cổ tay, háng, đầu gối, cổ chân. Meshy đặt điểm đánh dấu xương đúng ở những chỗ này.
3. **Đầu to là rủi ro:** Meshy chỉ ghi rằng tỉ lệ càng gần người thì tay chân càng ít méo. Concept có đầu gần bằng nửa chiều cao, cần sinh thử Lumo trước để biết Meshy còn đặt khớp đúng không.
4. **Không đồ rộng, không cầm đồ.** Đồ ôm sát (mũ, gile) để liền được. Áo choàng, túi, bảo bối là model riêng.
5. **Không cho Meshy tạo phần chĩa xa khỏi thân** (đuôi). Meshy sẽ gắn nó vào xương chân, nhấc chân là đuôi méo theo.

Mọi nhân vật:
- **Mặt:** Meshy vẽ mắt miệng lên texture, không cử động được. Giữ mặt đơn giản để làm vị trí tham chiếu. Trong Blender tô lại vùng mặt bằng màu da rồi làm face rig: mắt, mí, đồng tử, lông mày là các bộ phận rời gắn vào xương đầu; miệng là shape key bám trên bề mặt mõm; tất cả điều khiển bằng thanh trượt (custom property + driver) trên rig.
- **Trong suốt, phát sáng:** Meshy chỉ ra màu đặc. Thân thạch của Piko, ánh sáng của Nori, tinh thể của Tavi làm lại bằng shader trong Blender.

## Các bước trên web

1. **Ảnh đầu vào** cho **Image to 3D**: một đối tượng, nền trơn, chỉ gồm phần Meshy làm (bảng dưới). Chưa có ảnh đạt thì dùng **Text to 3D** với prompt bên dưới.
2. Lumo, Tavi: đặt **Pose = A-Pose**. Mọi nhân vật: bật **Symmetry**. Texture **2048** là đủ (phim 1080p; 4096 nặng cho EEVEE trên Vega 11).
3. Sinh 4 bản, chọn bản tách rõ tay khỏi thân, chân khỏi nhau, rồi mới chạy Texture/Refine.
4. **Remesh:** Quad, khoảng 20–50k mặt (máy Vega 11 chỉ nên dùng dưới 50k).
5. Lumo, Tavi: **Rig → Humanoid**, kiểm tra điểm đánh dấu ở 7 khớp. Sai thì bấm **Re-rig** rồi kéo lại. Chọn animation (idle, walk, run, jump, surprised, laugh, think…), không có sẵn thì thử Text to Motion.
6. **Tải về:** FBX, skeleton template **Mixamo** (mặc định), kèm animation. Lưu vào `Characters/<Tên>/source/<tên>_meshy_v01.fbx`.

**Đạo cụ** không cần rig.

### Ảnh đầu vào hiện có

| Asset | File trong `concept/` | Dùng được chưa | Cần sửa trước khi đưa vào Meshy |
|---|---|---|---|
| Lumo | `lumo_apose.png` | ❌ | Bỏ áo choàng và túi đeo chéo (làm riêng) |
| Tavi | `tavi_apose.png` | ❌ | Bỏ ba lô, túi đeo, ống, cuộn giấy và đuôi (làm riêng). Mũ, kính, gile ôm sát giữ lại |
| Nori | `nori_ref.png` | ❌ | Bỏ 4 cánh và 2 râu (làm trong Blender) |
| Piko | `piko_ref.png` | ✅ | — |
| Wonder Compass | `wonder_compass_ref.png` | ✅ | Kim la bàn phải quay được: làm kim riêng trong Blender, mặt kính làm bằng shader |
| Inventor Pack | `inventor_pack_ref.png` | ✅ | Ống tinh thể phát sáng làm bằng shader |
| Story Lens | `story_lens_ref.png` | ✅ | Hình trong mặt kính thay theo từng manh mối: làm bằng shader, không để Meshy vẽ cố định |
| Pocket of Wonders | `pocket_of_wonders_ref.png` | ⚠️ | Đồ thò ra miệng túi sẽ dính liền vào túi. Piko cần rút từng món ra (thìa, vịt, ô), nên tốt hơn là túi rỗng, các món làm riêng |

## Prompt Text to 3D

Prompt tiếng Anh, màu ghi bằng chữ (Meshy không đọc mã hex).

**Negative (dùng chung):**
```
realistic, photorealistic, sharp teeth, scary, horror, angry, holding objects, base, pedestal, multiple characters, text, logo, arms touching the body, crossed arms, hands on hips, legs together, sitting, crouching, kneeling, jumping
```

**LUMO** (không áo choàng, túi, đuôi) — Negative thêm: `cape, bag, tail`
```
Cute chibi fox character with a humanoid body, standing upright on two legs in A-pose, arms held out diagonally away from the body, legs slightly apart, big round head, very large pointed ears with pink inner ears, small white tuft of fur on top of the head, big shiny brown eyes, short muzzle with a small dark nose, visible chin and neck, orange fur with cream white belly, chest, muzzle and paws, short arms with visible elbows, small rounded paw hands, short legs with visible knees, big soft paw feet, no clothes, no cape, no bag, no tail. Soft stylized 3D, rounded shapes, soft fur look, pastel colors, kids animation style, full body, front view, symmetrical
```

**TAVI** (không đuôi) — Negative thêm: `tail, backpack`
```
Cute chibi little green reptile inventor with a humanoid body, standing upright on two short legs in A-pose, arms held out diagonally away from the body, legs apart, round head with big green eyes and a wide friendly smile, grass green skin with cream belly and cream muzzle, a row of glowing teal crystal spikes along the back lying close to the body, brown leather aviator cap with round goggles on the forehead, fitted beige vest with a brown belt, hands with four fingers, visible elbows and knees, no tail. Soft stylized 3D, rounded shapes, smooth matte clay surfaces, pastel colors, kids animation style, full body, front view, symmetrical
```

**NORI** (chỉ thân) — Negative thêm: `wings, antennae, legs`
```
Cute small round glowing light spirit, head and body merged into one soft round shape, lavender purple with a soft inner glow, big gentle violet eyes, small smile, rosy cheeks, two tiny arms, no legs, no wings, no antennae, front view. Soft stylized 3D, rounded shapes, smooth surfaces, pastel colors, kids animation style, symmetrical
```

**PIKO** (chỉ thân) — Negative thêm: `legs`
```
Cute bright aqua blue jelly slime creature, soft rounded blob body wider at the bottom, two dark blue rounded horns on top, very big shiny blue eyes, wide open happy mouth with a pink tongue, two small stubby arms, no legs, glossy jelly surface. Soft stylized 3D, rounded shapes, smooth glossy surfaces, pastel colors, kids animation style, front view, symmetrical
```

**Rain-O-Matic 3000** (máy tạo mưa tập 01, chưa có concept)
```
Cute cartoon rain-making machine, chunky rounded body made of riveted pastel metal panels, large glowing blue crystal core in a glass dome on top, small rain cloud nozzle, row of colorful dials and a slider for intensity, one big round red button labeled MAX POWER, short stubby legs, playful whimsical design. Soft stylized 3D, smooth surfaces, pastel colors, kids animation style
```

## Sau khi tải về

- Scale theo chiều cao trong Character Bible (Lumo 1.00 · Tavi 0.85 · Nori 0.70 · Piko 0.80).
- Rig Meshy dùng khung Mixamo, tên xương kiểu `mixamorig:Head`. Xương thêm vào (tai, đuôi) và bộ phận mặt gắn vào các xương này.
- Kiểm tra rig bằng `pipeline/rig_qa.py` trên các tư thế khó (giơ tay, bật nhảy, ngoái đầu, cúi). Đạt khi bad% dưới khoảng 2% và thể tích gần 1.0.

## Nguồn (tra ngày 01/11/2026)

[Pricing](https://www.meshy.ai/pricing) · [Credits guide](https://www.meshy.ai/tutorials/meshy-credits-guide) · [Rigging guide](https://docs.meshy.ai/en/webapp/guides/3d-model/rigging) · [Animate guide](https://docs.meshy.ai/en/webapp/guides/animate) · [MCP guide](https://www.meshy.ai/tutorials/meshy-mcp-guide) · [API asset retention](https://docs.meshy.ai/en/api/asset-retention)
