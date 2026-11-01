# The Wonderlings: Prompt cho Meshy (Text to 3D)

Dựa trên bảng nhân vật ở `BRIEF.md` mục 3. Cập nhật 01/11/2026: cả 4 nhân vật chuyển sang **dáng người** để dùng rig Humanoid và thư viện animation có sẵn của Meshy (lý do và quy tắc ở `BRIEF.md` mục 3.1).

Prompt viết bằng tiếng Anh vì Meshy hiểu tốt hơn. Màu ghi bằng chữ vì Meshy không đọc mã hex, mã hex chỉnh lại trong Blender sau.

## Cách dùng

1. **Gói tài khoản:** bản Free ra file CC BY 4.0 và công khai. Nhân vật chính nên sinh bằng gói trả phí để giữ quyền riêng (xem `ASSET_SOURCES.md` mục 4).
2. **Khi sinh hình:** đặt **Pose = A-Pose** (bắt buộc, rig Humanoid cần dáng này), bật **Symmetry**. Dán prompt nhân vật (đã kèm sẵn phần phong cách chung ở cuối), rồi dán phần Negative nếu có ô này.
3. Sinh mỗi nhân vật 4 bản. Chọn bản **tách rõ tay khỏi thân, chân khỏi nhau, thấy rõ cổ, khuỷu, gối** rồi mới chạy Texture/Refine. Bản đẹp mà tay dính thân thì bỏ.
4. **Remesh** trước khi rig: chọn Quad, khoảng 20–50k mặt. Meshy chỉ bắt giảm khi quá 300k mặt, nhưng lưới dày và không đều làm da bị xuyên khi cử động. Máy Vega 11 cũng chỉ nên dùng dưới 50k.
5. **Rig → Humanoid.** Kiểm tra các điểm đánh dấu ở cằm, vai, khuỷu, cổ tay, háng, gối, cổ chân đều nằm trong thân và đúng khớp. Sai thì bấm **Re-rig** rồi kéo lại.
6. **Animation:** chọn từ thư viện các loop mà `BRIEF.md` yêu cầu (idle, walk, run, jump, surprised, laugh, think…). Không có sẵn thì thử Text to Motion.
7. **Tải về:** FBX, skeleton template **Mixamo** (mặc định), có kèm animation. Đặt file vào `02_ASSET_LIBRARY/Characters/<Tên>/source/` để code Blender lấy.

Đạo cụ (bảo bối) luôn là **model riêng**, không gắn vào người, để còn tháo ra và animate.

**Negative (dùng chung):**
```
realistic, photorealistic, fur strands, detailed hair, sharp teeth, scary, horror, angry, clothing, cape, scarf, holding objects, base, pedestal, multiple characters, text, logo, arms touching the body, crossed arms, hands on hips, legs together, sitting, crouching, kneeling, jumping, flying pose, four legs, quadruped
```

---

## LUMO: Cloudling (cáo mây), cao 1.00

Đuôi mây **không** cho Meshy tạo: đuôi lớn chĩa ra sau sẽ bị gắn vào xương chân. Đuôi dựng bằng code trong Blender (đã có trong `lab/char_lumo/build_lumo.py`).

```
Cute cloud fox character with a humanoid body, standing upright on two legs in A-pose, arms held out diagonally away from the body, legs slightly apart, big round head about 40 percent of total height, very large pointed ears on top of the head, short muzzle with a visible chin and neck, slim rounded torso, arms reaching the hips with visible elbows and wrists, small rounded hands with short fingers, legs with visible knees and ankles, simple rounded paw feet, big round eyes, small simple smile, peach orange body with cream white belly, muzzle and ear tips, no tail. Soft stylized 3D, rounded shapes, smooth matte clay surfaces, pastel colors, kids animation style, full body, front view, symmetrical
```
Negative thêm: `tail`

## TAVI: Crystling (sinh vật tinh thể), cao 0.85

Gai tinh thể nên **thấp và ôm sát lưng** để không bị gắn vào xương tay. Kính bảo hộ để trên trán, đi theo đầu.

```
Cute crystal creature inventor with a humanoid body, standing upright on two legs in A-pose, arms held out diagonally away from the body, legs apart, sturdy compact build with broad shoulders and short strong legs with visible knees and ankles, big round head about 40 percent of total height, visible neck and chin, a row of short faceted crystal spikes along the upper back lying close to the body, round aviator goggles pushed up on the forehead, capable hands with four distinct fingers, big round eyes, focused clever expression, mint green body with darker teal crystals glowing softly. Soft stylized 3D, rounded shapes, smooth matte clay surfaces, pastel colors, kids animation style, full body, front view, symmetrical
```

## NORI: Lumina (tiên ánh sáng có cánh), cao 0.70

Cánh và râu **không** cho Meshy tạo: cánh mỏng trong suốt và râu mảnh Meshy làm không được, lại bị gắn vào xương tay. Cả hai dựng bằng code trong Blender, cánh dùng shader trong suốt.

```
Cute small glowing light fairy creature with a humanoid body, standing upright on two legs in A-pose, thin arms held out diagonally away from the body, short slender legs slightly apart, small round soft torso, big round head about 45 percent of total height, visible chin and neck, visible elbows and knees, small hands and feet, big wise gentle eyes, soft smile, lavender purple body with a soft inner glow, no wings, no antennae. Soft stylized 3D, rounded shapes, smooth surfaces, pastel colors, kids animation style, full body, front view, symmetrical
```
Negative thêm: `wings, antennae, floating`

## PIKO: Bloop (người thạch kẹo dẻo), cao 0.80

Đầu và thân liền một khối giọt nước, nhưng **phải có ngấn cổ** dưới cằm để Meshy đặt được điểm cằm, và tay chân đủ dài để thấy khuỷu, gối. Co giãn làm bằng shape keys trong Blender.

```
Cute jelly gummy creature with a humanoid body, standing upright on two legs in A-pose, short chubby arms held out diagonally away from the body, short chubby legs apart with visible knees, head and body merged into one soft water droplet shape with a slight neck crease under the chin, two small rounded horns on top of the head, simple round hands and feet, very big shiny eyes, wide playful grin, mischievous excited expression, aqua blue glossy jelly body with lighter highlights. Soft stylized 3D, rounded shapes, smooth glossy surfaces, pastel colors, kids animation style, full body, front view, symmetrical
```

---

## Đạo cụ

Đạo cụ không cần rig nên không cần A-pose.

**Rain-O-Matic 3000** (máy tạo mưa, Tập 01):
```
Cute cartoon rain-making machine, chunky rounded body made of riveted pastel metal panels, large glowing blue crystal core in a glass dome on top, small rain cloud nozzle, row of colorful dials and a slider for intensity, one big round red button labeled MAX POWER, short stubby legs, playful whimsical design. Soft stylized 3D, smooth surfaces, pastel colors, kids animation style
```

**Wonder Compass** (Lumo):
```
Cute cartoon magic compass, round brass case with a glowing crystal needle, cloud-shaped decorations, chunky simple shapes. Soft stylized 3D, pastel colors, kids animation style
```

**Story Lens** (Nori):
```
Cute cartoon magic magnifying lens, round glowing glass with tiny stars inside, curly golden handle shaped like a feather, chunky simple shapes. Soft stylized 3D, pastel colors, kids animation style
```

---

## Sau khi tải về: phần Blender làm tiếp (bằng code)

| Việc | Lumo | Tavi | Nori | Piko |
|---|---|---|---|---|
| Scale theo bảng chiều cao | 1.00 | 0.85 | 0.70 | 0.80 |
| Thêm xương, chỉnh trọng số da | 2 chuỗi xương tai | Gai lưng đi cứng theo xương ngực | — | 2 sừng nảy nhẹ |
| Gắn phần dựng riêng | Đuôi mây + chuỗi xương đuôi | — | 4 cánh + 2 râu sao, có xương | — |
| Động tác riêng | Vẫy đuôi, tai nảy | — | Vỗ cánh, bay lơ lửng | Squash & stretch (shape keys) |
| Mặt | Tô lại mắt miệng vẽ sẵn bằng màu da, gắn face rig | như Lumo | như Lumo | như Lumo |
| Material | Màu pastel theo mã hex trong `BRIEF.md` | + tinh thể phát sáng | + thân phát sáng, cánh trong suốt | + thạch bóng, hơi trong |

- **Trong suốt và phát sáng:** Meshy chỉ ra màu đặc. Thân thạch của Piko, ánh sáng của Nori, tinh thể của Tavi đều làm lại bằng shader trong Blender.
- **Tên xương:** rig Mixamo đặt tên kiểu `mixamorig:Head`, khác rig Rigify của Lumo. Code thêm xương tai, đuôi và face rig sẽ được chỉnh lại theo tên này.
- Nếu Text to 3D ra chưa đúng ý, cách chắc hơn là vẽ concept 2D trước (front view, A-pose, nền trắng) rồi dùng **Image to 3D**, vẫn đặt Pose = A-Pose.

## Nguồn tra cứu (01/11/2026)

- [Meshy — Rigging guide](https://docs.meshy.ai/en/webapp/guides/3d-model/rigging): loại rig Humanoid / Quadruped / Smart Rig, A-pose, điểm đánh dấu khớp, Remesh, không rig mặt và xương tùy chỉnh
- [Meshy — Animate guide](https://docs.meshy.ai/en/webapp/guides/animate): hơn 600 động tác và Text to Motion chỉ dành cho Humanoid, skeleton Mixamo
- [Meshy — AI Auto Rigging](https://www.meshy.ai/features/ai-auto-rigging)
