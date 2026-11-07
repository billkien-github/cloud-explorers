# sh020: prompt Seedance

Đoạn 2 của Cảnh 1 tập 000A: 21.9–48.6 s của cảnh (S9–S14), sinh 28 giây bằng Seedance 2.5 (bản nháp 480p); 26.7–28 s là đuôi, lúc dựng cắt bỏ.

## Tham chiếu

| Số | File tải lên | Nguồn |
|---|---|---|
| `@Video1` | `video1_previz.mp4` | `renders/sh020_ref.mp4` |
| `@Image1` | `image1_lumo.png` | `02_ASSET_LIBRARY/Characters/Lumo/concept/lumo_turnaround.png` |
| `@Image2` | `image2_cloud_forest.png` | `02_ASSET_LIBRARY/Environments/Cloud_Forest/concept/cloud_forest_hero.png` |
| `@Image3` | `image3_paper_map.png` | `02_ASSET_LIBRARY/Props/Paper_Map/concept/paper_map_ref.png` |
| `@Image4` | `image4_little_bird.png` | `02_ASSET_LIBRARY/Characters/Little_Bird/concept/little_bird_turnaround.png` |
| `@Image5` | `image5_butterflies.png` | `02_ASSET_LIBRARY/Characters/Glow_Butterflies/concept/glow_butterflies_ref.png` |
| `@Image6` | `image6_ancient_ruins.png` | `02_ASSET_LIBRARY/Environments/Ancient_Ruins/concept/ancient_ruins_hero.png` |
| `@Image7` | `image7_lumo_head.png` | `02_ASSET_LIBRARY/Characters/Lumo/concept/lumo_head_ref.png` |

## Prompt

```text
# sh020 — THE LITTLE EXPLORER, PART 2 (28s, video-to-video)

Cloud Forest, morning. A little bird on a branch laughs at Lumo the fox by patting its belly; Lumo is embarrassed, then puffs up, tucks the map away and insists on knowing the way; the bird flies off. Lumo pulls the map out again and strides away reading it, walks straight past a fork, steps off the edge of a gentle slope of dry leaves, slides down into a soft leaf pile and pops up with a leaf on the forehead; a glowing butterfly lands on a mossy stone and leads the eye to an ancient ruin with a faint golden glimmer. Video-to-video pass driven by @Video1.

ACTIVE REFERENCES
@Video1 = the Blender previz (28s, 672 frames, 24fps), frame-aligned. SOLE authority for the camera (path, framing, lens, timing), for the layout of every shot and for every character's position, facing and motion. ORANGE blocks = Lumo, BROWN blocks = the little bird; the WHITE square on a head = where that face looks. Gray blocks = trees, rocks, the burr bush, the slope, the leaf pile, stones and ruin walls. Small glowing peach blocks = butterflies; the small glowing block at the foot of the ruin wall = the golden glimmer. The pale flat panel in Lumo's paws = the parchment paper map; seen from behind it is plain parchment, never a white card. Every block becomes the real character or object its position implies. Do NOT take any material, color, texture or lighting from it. If the text and the video disagree about motion, the video wins.
@Image1 = Lumo turnaround sheet: left front view, right back view of ONE character. Defines design, proportions, colors, cape and bag. Layout, background and pose not inherited.
@Image2 = the Cloud Forest — defines look, materials, palette and warm morning light only: dirt path, giant leafy trees, mossy boulders, burr bushes with large heart-shaped leaves and soft round fuzzy burrs, the gentle slope of dry orange leaves and the leaf pile on moss. Its composition is NOT a view in this clip: the layout of every shot comes from @Video1. Camera angle not inherited.
@Image3 = Lumo's paper map, the right way up in this whole clip: treasure chest upright at the bottom, red arrow pointing down. Background not inherited.
@Image4 = little bird turnaround sheet: front and back of ONE bird. Defines design and colors. Layout, background and pose not inherited.
@Image5 = glowing butterfly design sheet: ONE butterfly drawn three times. Defines design and glow only; layout, pose, number and size not inherited.
@Image6 = the Ancient Ruins — defines the mossy stone walls with carved reliefs, vines, ferns, flat stone slabs on moss. Its composition is NOT a view in this clip: layout follows @Video1. Camera angle not inherited.
@Image7 = close-up of Lumo's head: defines the cream tuft of fur on top of the head (one tall curled cream swoosh), the ears, eyes and face markings exactly. Background not inherited.

STYLE
Soft stylized 3D animated film for young children: rounded soft shapes, pastel colors, warm gentle light, soft shadows. Every character keeps the materials of its reference image. Friendly and safe: nothing scary, no injuries, no realism, no live-action, no text, no logos, no watermarks. Original, no IP.

CHARACTERS
Lumo: young fox, 1.00 m tall. Very large ears (pink inside, orange to the tips), cream tuft on the head (one tall curled cream swoosh of fur exactly like @Image7), big brown eyes, cream muzzle, belly and paws, fluffy orange tail with a cream tip. Red knee-length cape with gold cloud trim and one round gold button; the tail comes out through a slit in the cape. Brown leather bag with a cloud emblem on ONE strap across the chest, never two. Big head, very short arms: paws touch the face no higher than the chin, never scratch the head or cover the eyes; raised arms reach ear level at most. Fur the same saturated orange as @Image1 in every shot and in every segment; cream cheeks as in @Image7.
Little bird: round, the size of Lumo's fist: the whole bird, head tuft and tail tuft included, is no taller than one quarter of Lumo's head height; chestnut-brown feathers, cream belly, rosy cheeks, head tuft, one curly tail tuft. Never speaks. Always perched on a thin tree branch until it flies away.
Glowing butterflies: tiny, the whole wingspan as wide as Lumo's nose, smaller than Lumo's eye; on the mossy stone it covers only a tiny spot of its top; pale peach-pink wings glowing softly. Never purple, gold or turquoise.
SIZES next to Lumo (1.00 m): the paper map is a little narrower than Lumo's head; the burr bush is the same bush as in the previous segment: a round leafy bush about as tall as Lumo with large heart-shaped light-green leaves and soft round fuzzy burrs the size of Lumo's nose, never thorns, spikes or needles; the leaf slope is gentle and only a little higher than Lumo from top to bottom; the leaf pile is waist-high to Lumo and a bit wider than Lumo; the mossy stone where the butterfly lands is knee-high; the ruin walls are about one and a half times Lumo's height; the golden glimmer is only a thin glowing line along the front edge of a flat slab, never a pool of light on top of it.

CAMERA
Strictly follow the camera work of @Video1, 1:1 and frame-aligned for all 28 seconds. Hard cuts exactly at 2.35s, 9.2s, 12.2s, 17.2s and 21.6s. Every shot exactly as framed in @Video1, never tighter, never wider: when @Video1 shows Lumo from ears to feet, the take shows Lumo from ears to feet. From 23.2s to 24.6s the camera pulls back as in @Video1, at one constant speed over the full 1.4 s, never a quick jump.

RULES
1. Exactly one Lumo; one little bird until it flies away at 8.9s; at most three butterflies until 12.2s, then exactly one tiny glowing butterfly; no other animals, no people.
2. The bird laughs only with its body: one wing pats its round belly; cheeky, never mean. It stays on its branch, small at the top left of the Lumo shots, until it flies away.
3. Lumo's embarrassment uses drooping ears, hunched shoulders and a shy glance; paws never above the chin.
4. The map is the right way up whenever it is seen, always parchment, and stays below Lumo's muzzle, never covering the face.
5. The slope is gentle and soft; Lumo slides on the back, feet first, never rolling over, never hurt, no rocks on the way.
6. The golden glimmer appears exactly at 23.7s and stays visible in every frame to the end: only a thin warm glowing line peeking out along the front edge of a flat stone slab, never a pool of light on the slab; its source stays hidden.
7. Ruin walls and stones stay where @Video1 puts them.
8. No text, letters or numbers anywhere, also not on the map or the ruin walls; the compass-rose carvings have no letters at their points.
9. The burr bush never has thorns, spikes or needles: soft heart-shaped leaves and round fuzzy burrs, the same bush as in the previous segment.
10. Lumo's bag stays on the hip with ONE strap across the chest the whole clip and never turns into the map.
11. Only natural sounds: no musical tones, no melody, no chord, no pad, no song, in any shot.

TIMELINE
0–2.35s — (camera per @Video1: close-up of the little bird on a thin branch above the path, belly toward camera) Continuing from the previous segment: Lumo, off-screen below, stands on the path facing left, delighted, the map at belly height the right way up. 0.2–0.6s the bird clearly tilts its head to one side, looking down-left at Lumo, and holds the tilt until 1.3s. The lower edge may show only Lumo's ear tips. 1.3–3.2s it laughs: one wing pats its round belly at 1.4s and 2.0s, eyes squeezed into happy curves, beak open. END 2.35s: bird mid-laugh.
2.35–5.5s — (camera per @Video1: Lumo from ears to feet facing left toward the path, the bird small on its branch at the top left) Lumo holds the map at belly height. At 2.6s the bird pats its belly a third time. 2.4–4.0s Lumo is embarrassed: ears droop back, shoulders hunch, a shy glance up at the bird. 4.0–4.5s Lumo puffs out the chest and pops both ears straight up; from now until 9.2s the ears stay up, chin high, a proud bluffing face. 4.6–5.5s Lumo folds the map in half twice and tucks it into the shoulder bag. END 5.5s: Lumo standing tall, map in the bag.
5.5–9.2s — (same camera) At 5.6s Lumo gives one firm nod; 5.6–7.9s Lumo talks: the mouth clearly opens and closes on every syllable, about 4 times per second, no spoken words; chest out, chin up, eyes half-closed, bluffing; the bird giggles once more, patting its belly. 8.1–8.9s the bird crouches, flaps and flies up and away to the left into the forest; Lumo's eyes follow it. END 9.2s: branch empty, Lumo alone.
9.2–12.2s — (camera per @Video1: wider, the path, the soft burr bush with round fuzzy burrs at right) 9.4–9.9s Lumo's paw lifts the bag flap and pulls the folded map up OUT of the bag, then unfolds it and reads it again, held just below the muzzle; the bag stays on the hip. From 10.1s Lumo strides off fast to the left, reading, and crosses the left edge of the frame by the cut. END 12.2s: the path is nearly empty.
12.2–15.55s — (camera per @Video1: wide and high over the path fork, the rounded edge of a gentle slope of dry leaves, a leaf pile on moss below) Lumo strides in fast from the top right, reading the map, straight past the fork, ears tilted back. At 13.6s Lumo steps off the edge; 13.6–13.95s Lumo is still upright at the edge, one foot over empty air, body tipping, eyes round, mouth a small O, both short arms up to ear level, and the map slips away (it flutters down 13.65–16.5s and lands at the pile's edge). At 13.95s, not before, Lumo sits down and slides down the slope on the back, feet first, a happy surprised "wheee" is fine, ears and tail streaming back, arms flailing, surprised and funny, never scared. At 15.55s Lumo plops into the leaf pile, leaves puffing up. END 15.55s: Lumo buried in the pile.
15.55–17.2s — (same camera) Leaves settle; only the pile and the map at its edge. END 17.2s: still.
17.2–21.6s — (camera per @Video1: medium on the leaf pile) At 17.4s Lumo's head pops out of the leaves, a dry leaf stuck mid-forehead, blinking, dazed. 18.6–19.1s Lumo shakes the head hard; 18.85–19.6s the leaf falls off behind onto the pile. 19.8–20.3s Lumo picks up the map beside the pile; 20.4–21.0s stuffs it into the shoulder bag. END 21.6s: Lumo sitting chest-deep in the pile.
21.6–23.2s — (camera per @Video1: closer, a mossy stone at left, Lumo's head and ears at right) 21.8–22.5s the glowing butterfly flutters down and lands on the mossy stone right in front of Lumo, wings slowly opening and closing. Lumo watches it, ears forward, curious. END 23.2s: butterfly resting.
23.2–24.4s — (camera per @Video1: pulls back at one constant speed until 24.6s) Behind the butterfly an ancient ruin appears, nearly swallowed by vines and moss: the ruin wall stands only on the LEFT half of the frame; on the right, behind Lumo and the pile, the same slope of dry orange leaves rises as in the previous shot; no wall and no big stone slab in the foreground. At 23.7s, not later, while the camera is still pulling back, a thin warm golden light appears under a flat stone slab at the foot of the wall on the left and stays visible in every frame to the end. END 24.4s: the light glows softly, Lumo still low in the pile.
24.4–26.7s — (camera per @Video1: holds from 24.6s; only natural sounds, no musical tones) At 24.4s, after the light has appeared, Lumo rises out of the leaves up to the chest, both ears popping straight up, eyes wide, turns the head to screen LEFT and looks at the golden light, and holds that pose. END 26.7s: Lumo gazing at the glimmer.
26.7–28s — (camera holds; this tail is cut in the edit) Same. END 28s: same.

AUDIO
No music, no songs, no spoken words; non-verbal character sounds (gasps, an "oh", giggles, a happy "wheee") are fine. The bird's chirps are sound effects. Sound effects: soft forest ambience, light breeze, paper rustling, quick footsteps. 5.6–7.9s no spoken words (the line is dubbed later). Timed accents: 1.4s chirp, 2.0s chirp, 2.6s chirp, 4.6s paper folding, 8.1s small wings fluttering, 9.4s paper rustle, 13.6s whoosh as the foot slips, 13.95s long rustle of sliding leaves, 15.55s soft poof into the pile, 17.4s leaves rustling as the head pops up, 23.7s a tiny, high, soft sparkle (not a low swell).

HOLD
@Video1 camera, framing and layout 1:1 for all 28 seconds, same cuts and pull-back. One Lumo; the bird only until it flies away; one tiny butterfly at the ruins. @Image1 identity constant: cream swoosh tuft exactly as @Image7, saturated orange fur, one bag strap that stays, knee-length cape. Soft burr bush, never thorns. Map right way up and always parchment. Lumo's mouth moves 5.6–7.9s. Lumo never hurt. Golden glimmer appears at 23.7s: a thin line under the slab's edge, source hidden. Ruin wall only on the left, leaf slope on the right. Bird and butterfly tiny next to Lumo's head. No text, no logos, no music, no songs, no spoken words.
```

## Take

| Take | Model, giá | Kết quả |
|---|---|---|
| take01 | 2.5 bản nháp 480p, $3.45 | Không dùng (review đủ nhóm). Lỗi: bụi gai ở S10, S11 thành bụi gai nhọn (Chặn), túi da tan thành bản đồ lúc rút bản đồ (Chặn), chỏm lông Lumo thành nơ hồng, lông nhạt, miệng không mấp máy ở câu thoại, hụt chân dồn vào 3 khung, bướm quá to, ánh vàng trễ khoảng 1.5 s, Lumo không nhổm lên, có nhạc ở cú cuối. |
| take02 | 2.5 bản nháp 480p, $3.45, prompt và previz sửa theo review take01 | **Dùng tạm** (người dùng chấp nhận ngày 07/11/2026; lỗi còn lại sửa sau nếu cần). Review lại đủ nhóm: Đạt: bụi quả ké giống sh010, túi không biến hình, hụt chân, trượt, đống lá, bướm nhỏ, Lumo nhổm lên nhìn trái, an toàn. Nên sửa: chỏm lông thành nơ hồng (câu chữ không giữ được, cần ảnh cận đầu); má đỏ suốt S10; câu chống chế miệng chỉ mở một lần, mặt ngượng; ánh vàng trễ khoảng 1.4 s, Lumo nhìn trước khi có ánh vàng; Lumo không nhìn con bướm lúc nó đậu; còn nhạc ở 22.5–28 s, tiếng ù thay tiếng lấp lánh ở 23.7 s (thay ở hậu kỳ). |
