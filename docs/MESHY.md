# Làm nhân vật 3D bằng Meshy

Hình nhân vật sinh bằng Meshy, rồi Blender làm tiếp bằng code những phần Meshy không làm được (đuôi, cánh, mặt, shader). Hình dáng chuẩn của từng nhân vật: [`01_BRAND/Character_Bible/`](../01_BRAND/Character_Bible/README.md).

## 1. Gói và nơi làm

- **Gói Pro** (527.000 đ/tháng khi tra ngày 01/11/2026): 1.000 credit/tháng, tải không giới hạn, file riêng tư thuộc về mình, có Remesh, thư viện hơn 600 động tác. Gói Free không dùng được cho dự án: không có Remesh, chỉ 20 động tác, file bị công khai theo CC BY 4.0.
- **Thiết kế làm trên web Meshy:** xem và chọn bản trực tiếp, sửa điểm khớp bằng tay, rig miễn phí. Model nằm trong workspace của tài khoản.
- **Meshy MCP** (`@meshy-ai/meshy-mcp-server`, cần gói Pro) để dành cho lúc sản xuất hàng loạt (đạo cụ, sinh vật phụ, gắn nhiều animation). Qua MCP/API, rig và Remesh tốn 5 credit mỗi lần, model chỉ được giữ 3 ngày trên server và không hiện trên web, nên phải tải về ngay.
- **Credit:** sinh hình thô 20, tô texture 10, Text to Motion 3. Rig và animation có sẵn trên web: miễn phí.

## 2. Meshy rig được gì

| Loại rig | Dùng cho | Thư viện animation |
|---|---|---|
| **Humanoid** | Nhân vật 2 tay, 2 chân | Hơn 600 động tác + Text to Motion |
| Quadruped | Thú 4 chân | Chỉ 1 động tác đi |
| Smart Rig | Sinh vật khác, robot, đồ vật | Không dùng được thư viện |

Meshy **không rig mặt** và **không rig phần thừa** (đuôi, cánh, râu). Những phần đó làm trong Blender (`pipeline/rigging/`).

## 3. Phương án cho từng nhân vật (theo concept hiện tại)

| | Meshy làm | Blender làm (code) |
|---|---|---|
| **Lumo** | Thân, rig Humanoid, animation | Áo choàng, túi đeo chéo, đuôi (làm riêng rồi gắn); xương tai; mặt |
| **Tavi** | Thân (kèm mũ, kính, gile ôm sát), rig Humanoid, animation | Đuôi (làm riêng); gai tinh thể đi cứng theo ngực; mặt |
| **Nori** | Chỉ sinh hình thân (không cánh, không râu) | Rig bằng code: thân tròn, tay nhỏ, 4 cánh trong suốt, 2 râu sao, bay lơ lửng; mặt |
| **Piko** | Chỉ sinh hình thân | Rig bằng code: co giãn bằng shape keys, tay nhỏ, sừng nảy; mặt |

⚠️ Nori và Piko không có chân nên không dùng được rig Humanoid và thư viện animation. Hướng này **đang chờ chốt**, xem phần "Cần chốt" trong Character Bible.

## 4. Quy tắc khi sinh hình

Với nhân vật dùng rig Humanoid (Lumo, Tavi):
1. **Sinh ở A-pose:** tay dang chéo xuống khoảng 45°, có khe hở giữa tay và thân, hai chân tách nhau.
2. **Nhìn thấy rõ các khớp:** cằm và cổ, vai, khuỷu tay, cổ tay, háng, đầu gối, cổ chân. Meshy đặt điểm đánh dấu xương đúng ở những chỗ này.
3. **Đầu to nhưng không quá to:** Meshy chỉ ghi rằng tỉ lệ càng gần người thì tay chân càng ít méo. Concept có đầu gần bằng nửa chiều cao, cần sinh thử để biết Meshy còn đặt khớp đúng không.
4. **Không đồ rộng, không cầm đồ.** Đồ ôm sát (mũ, gile) để liền được. Áo choàng, túi, bảo bối là model riêng.
5. **Phần chĩa xa khỏi thân** (đuôi, cánh, râu) không cho Meshy tạo. Nếu để Meshy tạo, chúng bị gắn vào xương chân, xương tay, nhấc chân là đuôi méo theo.

Với mọi nhân vật:
- **Mặt:** Meshy vẽ mắt miệng lên texture nên không cử động được. Giữ mặt đơn giản để làm vị trí tham chiếu. Trong Blender tô lại vùng mặt bằng màu da rồi gắn face rig (`pipeline/rigging/face_rig.py`).
- **Trong suốt và phát sáng:** Meshy chỉ ra màu đặc. Thân thạch của Piko, ánh sáng của Nori, tinh thể của Tavi làm lại bằng shader trong Blender.

## 5. Các bước trên web

1. **Ảnh đầu vào:** ảnh hero trong `concept/` có nền, có đồ, không ở A-pose nên chưa dùng thẳng cho Image to 3D được. Cách chắc nhất là vẽ thêm một ảnh **chính diện, A-pose, nền trắng, không đồ rời** cho từng nhân vật (dùng ảnh hero làm tham chiếu), lưu vào `concept/<tên>_apose.png` rồi dùng **Image to 3D**. Chưa có ảnh đó thì dùng **Text to 3D** với prompt ở mục 6.
2. Đặt **Pose = A-Pose** (với Lumo, Tavi), bật **Symmetry**.
3. Sinh 4 bản. Chọn bản tách rõ tay khỏi thân, chân khỏi nhau, thấy rõ cổ, khuỷu, gối, rồi mới chạy Texture/Refine.
4. **Remesh:** Quad, khoảng 20–50k mặt (máy Vega 11 chỉ nên dùng dưới 50k).
5. **Rig → Humanoid** (Lumo, Tavi). Kiểm tra điểm đánh dấu ở cằm, vai, khuỷu, cổ tay, háng, gối, cổ chân. Sai thì bấm **Re-rig** rồi kéo lại.
6. **Animation:** chọn các loop cần (idle, walk, run, jump, surprised, laugh, think…). Không có sẵn thì thử Text to Motion.
7. **Tải về:** FBX, skeleton template **Mixamo** (mặc định), có kèm animation. Lưu vào `02_ASSET_LIBRARY/Characters/<Tên>/source/`, đặt tên có số phiên bản (`lumo_meshy_v01.fbx`).

**Đạo cụ** (4 bảo bối): ảnh concept trong `02_ASSET_LIBRARY/Props/<Tên>/concept/` là ảnh một vật ở giữa khung, dùng thẳng cho **Image to 3D** được. Đạo cụ không cần rig.

## 6. Prompt Text to 3D

Prompt tiếng Anh, màu ghi bằng chữ (Meshy không đọc mã hex, mã màu chỉnh lại trong Blender).

**Negative (dùng chung):**
```
realistic, photorealistic, sharp teeth, scary, horror, angry, holding objects, base, pedestal, multiple characters, text, logo, arms touching the body, crossed arms, hands on hips, legs together, sitting, crouching, kneeling, jumping
```

**LUMO** (Humanoid; không áo choàng, túi, đuôi)
```
Cute chibi fox character with a humanoid body, standing upright on two legs in A-pose, arms held out diagonally away from the body, legs slightly apart, big round head, very large pointed ears with pink inner ears, small white tuft of fur on top of the head, big shiny brown eyes, short muzzle with a small dark nose, visible chin and neck, peach orange fur with cream white belly, chest, muzzle and paws, short arms with visible elbows, small rounded paw hands, short legs with visible knees, big soft paw feet, no clothes, no cape, no bag, no tail. Soft stylized 3D, rounded shapes, soft fur look, pastel colors, kids animation style, full body, front view, symmetrical
```
Negative thêm: `cape, bag, tail`

**TAVI** (Humanoid; không đuôi)
```
Cute chibi little green reptile inventor with a humanoid body, standing upright on two short legs in A-pose, arms held out diagonally away from the body, legs apart, round head with big green eyes and a wide friendly smile, grass green skin with cream belly and cream muzzle, a row of teal crystal spikes along the back lying close to the body, brown leather aviator cap with round goggles on the forehead, fitted beige vest with a brown belt, hands with four fingers, visible elbows and knees, no tail. Soft stylized 3D, rounded shapes, smooth matte clay surfaces, pastel colors, kids animation style, full body, front view, symmetrical
```
Negative thêm: `tail, backpack`

**NORI** (chỉ thân; cánh và râu làm trong Blender)
```
Cute small round glowing light spirit, head and body merged into one soft round shape, lavender purple with a soft inner glow, big gentle violet eyes, small smile, rosy cheeks, two tiny arms, no legs, no wings, no antennae, front view. Soft stylized 3D, rounded shapes, smooth surfaces, pastel colors, kids animation style, symmetrical
```
Negative thêm: `wings, antennae, legs`

**PIKO** (chỉ thân)
```
Cute aqua blue jelly slime creature, soft rounded blob body wider at the bottom, two dark blue rounded horns on top, very big shiny blue eyes, wide open happy mouth with a pink tongue, two small stubby arms, no legs, glossy jelly surface. Soft stylized 3D, rounded shapes, smooth glossy surfaces, pastel colors, kids animation style, front view, symmetrical
```
Negative thêm: `legs`

**Rain-O-Matic 3000** (máy tạo mưa tập 01, chưa có concept)
```
Cute cartoon rain-making machine, chunky rounded body made of riveted pastel metal panels, large glowing blue crystal core in a glass dome on top, small rain cloud nozzle, row of colorful dials and a slider for intensity, one big round red button labeled MAX POWER, short stubby legs, playful whimsical design. Soft stylized 3D, smooth surfaces, pastel colors, kids animation style
```

## 7. Sau khi tải về

- Scale theo bảng chiều cao trong `docs/BRIEF.md`: Lumo 1.00 · Tavi 0.85 · Nori 0.70 · Piko 0.80.
- Rig Meshy dùng khung Mixamo, tên xương kiểu `mixamorig:Head`. Code thêm xương, sửa da (`skin.py`), face rig (`face_rig.py`) phải dùng tên này.
- Kiểm tra rig bằng `pipeline/rigging/rig_qa.py`: đặt các tư thế khó, đo % mặt lưới bị bóp hay giãn và thể tích. Đạt khi bad% dưới khoảng 2% và thể tích gần 1.0.

## Nguồn tra cứu (01/11/2026)

- [Meshy — Pricing](https://www.meshy.ai/pricing) · [Credits guide](https://www.meshy.ai/tutorials/meshy-credits-guide)
- [Meshy — Rigging guide](https://docs.meshy.ai/en/webapp/guides/3d-model/rigging) · [Animate guide](https://docs.meshy.ai/en/webapp/guides/animate)
- [Meshy — MCP guide](https://www.meshy.ai/tutorials/meshy-mcp-guide) · [meshy-mcp-server](https://github.com/meshy-dev/meshy-mcp-server) · [API asset retention](https://docs.meshy.ai/en/api/asset-retention)
