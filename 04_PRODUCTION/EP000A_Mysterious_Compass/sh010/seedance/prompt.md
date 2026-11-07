# sh010: prompt Seedance

Đoạn 1 của Cảnh 1 tập 000A: 0–21.9 s của cảnh (S1–S8), sinh 23 giây bằng Seedance 2.5 (bản nháp 480p); 21.9–23 s là đuôi, lúc dựng cắt bỏ.

## Tham chiếu

| Số | File tải lên | Nguồn |
|---|---|---|
| `@Video1` | `video1_previz.mp4` | `renders/sh010_ref.mp4` |
| `@Image1` | `image1_lumo.png` | `02_ASSET_LIBRARY/Characters/Lumo/concept/lumo_turnaround.png` |
| `@Image2` | `image2_cloud_forest.png` | `02_ASSET_LIBRARY/Environments/Cloud_Forest/concept/cloud_forest_hero.png` |
| `@Image3` | `image3_paper_map_upside_down.png` | `02_ASSET_LIBRARY/Props/Paper_Map/concept/paper_map_upside_down.png` |
| `@Image4` | `image4_paper_map.png` | `02_ASSET_LIBRARY/Props/Paper_Map/concept/paper_map_ref.png` |
| `@Image5` | `image5_little_bird.png` | `02_ASSET_LIBRARY/Characters/Little_Bird/concept/little_bird_turnaround.png` |
| `@Image6` | `image6_butterflies.png` | `02_ASSET_LIBRARY/Characters/Glow_Butterflies/concept/glow_butterflies_ref.png` |

## Prompt

```text
# sh010 — THE LITTLE EXPLORER, PART 1 (23s, video-to-video)

Morning in the Cloud Forest. Lumo the fox marches along a forest path reading a paper map held upside down, proudly announces that the treasure is straight ahead, strides forward without looking, trips over a small stone and falls face-first into a bush of soft round burrs; a tall rock cliff blocks the way right behind it. Lumo backs out with one burr stuck on the nose, shakes it off, turns the map the right way round, realises that "ahead" was behind, whips around and sees a wide sunny forest path; Lumo hops for joy. Video-to-video pass driven by @Video1.

ACTIVE REFERENCES
@Video1 = the Blender previz (23s, 552 frames, 24fps), frame-aligned. SOLE authority for the camera (path, framing, lens, timing), for the layout of every shot and for every character's position, facing and motion. ORANGE blocks = Lumo, BROWN blocks = the little bird; the WHITE square on a head = where that face looks. Gray blocks = trees, rocks, the burr bush and the cliff; the tall gray wall at the right end of the path = the cliff; the small dark mound on the path between Lumo and the bush = the stone Lumo trips over. Small glowing peach blocks = butterflies. The pale flat panel in Lumo's paws = the parchment paper map; its dark marks are the drawn arrow and chest; seen from behind, the map is plain parchment, never a white card. Every block becomes the real character or object its position implies. Do NOT take any material, color, texture or lighting from it. If the text and the video disagree about motion, the video wins.
@Image1 = Lumo turnaround sheet: left front view, right back view of ONE character. Defines design, proportions, colors, cape and bag. Layout, background and pose not inherited.
@Image2 = the Cloud Forest — defines look, materials, palette and warm morning light only: dirt path, giant leafy trees, mossy boulders, burr bushes with round fuzzy burrs, floating islands with waterfalls above a sea of clouds. Its composition (boulders at the left, a path leading into the distance, a leaf slope at the right) is NOT a view in this clip: the layout of every shot comes from @Video1. Camera angle not inherited.
@Image3 = Lumo's paper map exactly as Lumo holds it from the start until 13.7s: already upside down — the treasure chest is upside down at the TOP edge and the big red arrow below it points UP. Background not inherited.
@Image4 = the same paper map the right way up, exactly as Lumo holds it from 14.3s to the end: the treasure chest upright at the bottom, the big red arrow pointing DOWN toward Lumo. Background not inherited.
@Image5 = little bird turnaround sheet: front and back of ONE bird. Defines design and colors. Layout, background and pose not inherited.
@Image6 = glowing butterfly design sheet: ONE butterfly drawn three times. Defines design and glow only; layout, pose and number not inherited.

STYLE
Soft stylized 3D animated film for young children: rounded soft shapes, pastel colors, warm gentle light, soft shadows. Every character keeps the materials of its reference image. Friendly and safe: nothing scary, no injuries, no realism, no live-action, no text, no logos, no watermarks. Original, no IP.

CHARACTERS
Lumo: young fox, 1.00 m tall. Very large ears (pink inside, orange to the tips), cream tuft on the head, big brown eyes, cream muzzle, belly and paws, fluffy orange tail with a cream tip. Red knee-length cape with gold cloud trim and one round gold button; the tail comes out through a slit in the cape. Brown leather bag with a cloud emblem on ONE strap across the chest, never two. Big head, very short arms: paws touch the face no higher than the chin, never scratch the head or cover the eyes; raised arms reach ear level at most.
Little bird: round, the size of Lumo's fist, about one tenth of Lumo's height, much smaller than Lumo's head; chestnut-brown feathers, cream belly, rosy cheeks, head tuft, one curly tail tuft. Never speaks. Always perched on a thin tree branch.
Glowing butterflies: the size of Lumo's finger, pale peach-pink wings glowing softly. Never purple, gold or turquoise.
SIZES next to Lumo (1.00 m): the paper map is as wide as Lumo's head; the burr bush is about as tall as Lumo and about as wide; each burr is a fuzzy ball the size of Lumo's nose; the stone is ankle-high, a low rounded rock about as long as Lumo's foot, half sunk in the path; the cliff is more than four times Lumo's height.

CAMERA
Strictly follow the camera work of @Video1, 1:1 and frame-aligned for all 23 seconds. Hard cuts exactly at 3.4s, 5.2s, 8.75s, 10.4s, 13.4s, 15.3s and 18.3s. Every shot exactly as framed in @Video1, never tighter, never wider: when @Video1 shows Lumo from ears to feet, the take shows Lumo from ears to feet. The opening shot first holds on the sky, then tilts down slowly and evenly, exactly as fast as @Video1. The shots 3.4–5.2s and 13.4–15.3s are Lumo's eye view: no head in frame; each lasts the full time between its two cuts.

RULES
1. Exactly one Lumo, one little bird, at most three butterflies; no other animals, no people.
2. The little bird sits on a thin tree branch, never on a treetop, a rock or the cliff, and only where @Video1 shows the brown block: in the opening shot it appears only after the camera has tilted down, tiny, on the branch over the path right of center; 5.2–8.75s at the top-left edge, partly cut (stay visible at that edge); 8.75–10.4s small on the same branch at the upper LEFT; in the later wide shots small on its branch where @Video1 shows it. Its head may turn; its body stays on the branch.
3. The map is upside down until Lumo turns it (13.7–14.3s), as in @Image3; after that it is the right way up, as in @Image4.
4. The map is always parchment, also seen from behind or small in a wide shot: never a white or blue card, never a gray square on its back.
5. The map stays below Lumo's muzzle and never covers the face.
6. The stone lies on the path exactly where @Video1 shows the dark mound, visible from 5.2s on, between Lumo and the bush.
7. The bush has soft fuzzy burrs like @Image2 that cling, never prick; Lumo is never hurt, never scratched. The trip and the fall are soft and funny.
8. The path ends at the burr bush: right behind the bush the tall mossy cliff closes the way; no path continues past the bush, no open sky behind it.
9. Lumo faces right toward the bush (three-quarter view) from the moment Lumo turns onto the main path until the whip-around at 17.8s; Lumo never looks into the camera.
10. No text, letters or numbers anywhere, also not on the map. The sky in the last wide shot stays calm and empty.

TIMELINE
0–3.4s — (camera per @Video1: wide; holds on the sky, then tilts down slowly to the forest path) Floating islands with small trees, waterfalls pouring into a sea of clouds, giant leafy trees; glowing butterflies drift over the treetops. At 1.4s Lumo walks out of a side path on the left, small in the distance, reading the map held just below the muzzle, ears tilted back and relaxed, bouncy confident stride. Lumo turns onto the main path and walks to the RIGHT across the frame, three-quarter view facing right, eyes always down on the map. The path runs from left to right toward the burr bush and the tall cliff at the right, as in @Video1. END 3.4s: Lumo walking right, reading.
3.4–5.2s — (camera per @Video1: Lumo's eye view looking down at the map, bobbing gently with each step) The bottom third of the frame is Lumo's own chest: cream belly, the edges of the red cape, the gold button and the bag strap. The map rests right against the chest; only the two cream paws show, at the map's lower corners; no long forearms reaching in from the frame corners, no ground under the map. The map is upside down as in @Image3: chest upside down at the top, big red arrow pointing straight up, toward the path ahead. END 5.2s: same view.
5.2–6.4s — (camera per @Video1: Lumo from ears to feet on the left, the stone on the path in front of Lumo's feet, the burr bush on the right, the foot of the tall mossy cliff at the right edge behind the bush) Lumo stops one step before the stone and the bush, three-quarter view facing right, ears still tilted back, eyes on the map. At 5.5s Lumo pops both ears straight up and pushes the map straight out toward the bush at chest height (until 5.9s): the top edge of the map stays below the chin, the whole muzzle visible; the bush peeks out right behind the map's edge. END 6.4s: Lumo proud, map held out.
6.4–8.1s — (same camera) Lumo talks, mouth moving, no spoken words: proud, eyes shining, ears straight up, map held out toward the bush, eyes on the map, not on the path or the stone. END 8.1s: still talking, chest out.
8.1–8.75s — (same camera) 8.1–8.3s Lumo finishes the line while starting ONE big confident stride forward, chin high, eyes closed with pride, not looking down. At 8.42s the front toe catches the stone: Lumo stumbles, eyes pop wide, mouth a small round O, both short arms fling up to ear level, the body pitches forward. At 8.6s, not before, Lumo falls face-first into the bush: the head sinks into the leaves up to the ears, the body keeps moving a little, squashes on impact and springs back slightly, tail shooting straight up, the map arm dropping low. A springy, natural cartoon trip-and-fall with weight and momentum, never a stiff tilt of the whole body. END 8.75s: head buried in the bush up to the ears, body bent forward over the stone.
8.75–10.4s — (camera per @Video1: wider; Lumo at the bush, the tall mossy cliff right behind it blocking the way, the bird small on the branch at the upper left) The dirt path ends at the bush. Lumo is stuck, head inside the leaves up to the ears the whole time, body bent forward: the whole body wiggles side to side, ears twitching, tail straight up and wagging fast; the parchment map hangs low in one paw. At 10.0s, not earlier, Lumo pulls back out (until 10.35s), one round fuzzy burr stuck on the nose tip, fur a little ruffled. END 10.4s: Lumo a step back from the bush.
10.4–11.4s — (camera per @Video1: close-up of Lumo, the bush at the right) 10.5–11.2s Lumo holds still and looks cross-eyed at the burr on the nose; the head does not move; the burr stays on the nose. END 11.4s: still cross-eyed.
11.4–12.35s — (same camera) 11.4–11.9s Lumo shakes the head side to side; at 11.65s the burr flies off to the right in a small arc and drops out of frame at the bottom right. Then Lumo holds still and blinks once. END 12.35s: head still, nose clean.
12.35–13.4s — (same camera) 12.35–12.75s a quick look up at the top of the bush; 12.85–13.25s a quick look down at the map, puzzled, frowning. The back of the map facing the camera is plain parchment. END 13.4s: frowning at the map.
13.4–15.3s — (camera per @Video1: Lumo's eye view down at the map again, chest and cape at the bottom, cream paws at the map's lower corners) The map starts upside down as in @Image3. 13.7–14.3s the paws turn the map half a turn: now it is the right way up as in @Image4, the chest upright at the bottom and the big red arrow pointing straight down, toward Lumo. END 15.3s: map the right way up.
15.3–17.8s — (camera per @Video1: Lumo from ears to feet before the burr bush, the path behind Lumo on the left) Lumo stands three-quarter facing right, map at chest height. 15.5–17.6s Lumo talks, mouth moving, no spoken words: a slow realisation, eyebrows rising. At 16.4s Lumo turns the head over the shoulder toward the path on the left, eyes widening. END 17.8s: Lumo about to turn.
17.8–18.3s — (same camera) 17.8–17.95s Lumo whips around to face left, cape and tail swinging. END 18.3s: Lumo facing left, toward the open path.
18.3–21.9s — (camera per @Video1: wide, a broad sunny path leading deep into the forest on the left, Lumo small at the right, the bird small on its branch) Giant trees arch over the path, soft light through the leaves. 18.7–21.5s a calm, open moment: nothing new enters the frame, the sky above the trees stays clear and empty. 19.6–20.3s Lumo hops up once with joy, lifting the map in both paws, never above the ears, both feet off the ground, then lands. END 21.9s: Lumo on the path, facing left, delighted.
21.9–23s — (camera holds; this tail is cut in the edit) Lumo stays happy on the path. END 23s: same.

AUDIO
No music, no songs, no spoken words; non-verbal character sounds (gasps, an "oh", giggles, a happy "wheee") are fine. Sound effects: soft forest ambience, light breeze, distant waterfall, footsteps on the dirt path, paper rustling. 6.4–8.3s and 15.5–17.6s no spoken words (the line is dubbed later). Timed accents: 5.5s crisp paper snap as the map is pushed out, 8.42s a light scuff as the toe catches the stone, 8.6s leafy crunch as the face hits the bush (the loudest sound of the clip), 11.65s a very soft tiny pop exactly as the burr leaves the nose, much quieter than the crunch, 13.7s paper rustle as the map turns, 17.8s quick whoosh of the spin and cape, 20.3s soft landing thump on the dirt path.

HOLD
@Video1 camera, framing and layout 1:1 for all 23 seconds, same cuts. One Lumo, one little bird on a branch, at most three butterflies. @Image1 identity constant: one bag strap, knee-length cape. Map upside down until 13.7s (@Image3), right way up after 14.3s (@Image4), always parchment. The stone causes the trip. The path ends at the bush, the cliff closes it. Lumo never hurt. No text, no logos, no music, no songs, no spoken words.
```

## Take

take01–06 thuộc cách chia cũ (đoạn 0–13.4 s, sinh 14 giây, gag cũ: Lumo tự bước vào bụi gai), giữ lại để so; từ take07 là đoạn 0–21.9 s hiện tại.

| Take | Model, giá | Kết quả |
|---|---|---|
| take01 | 2.0 mini, $1.27 | Không dùng. Bản đồ xuôi chiều (chép ảnh tham chiếu), bản đồ thành tấm thẻ trắng ở S4, S1 chép bố cục ảnh Rừng Mây, chim sai chỗ, S3 chặt hơn previz, thiếu nhịp dựng tai, bước thêm; S5 diễn sớm 0.3–0.6 s; pop của quả gai trễ 0.37 s. |
| take02 | 2.0 fast, $2.00 | Không dùng. Bản đồ xuôi chiều, S1 chép bố cục ảnh; chim ở S4 đúng chỗ. |
| take03 | 2.0, $2.61 | Không dùng. Bản đồ xuôi chiều, S1 chép bố cục ảnh; S3 đúng toàn thân, chim ở S4 đúng chỗ. |
| take04 | 2.5, $3.88 | Không dùng. Bản đồ ngược đúng, bố cục S1 đúng previz; S3, S5 chặt hơn previz; không thấy chim ở S4. |
| take05 | 2.0 fast, $2.00 | Không dùng. Ảnh bản đồ xoay sẵn: bản đồ ngược đúng, ngực ở cú nhìn xuống, chim, vách đá đúng; S1 vẫn chép bố cục ảnh, S3 vẫn chặt. |
| take06 | 2.0 fast, $2.00 | Không dùng. Cú đâm vào bụi có đà nhưng người dùng thấy vẫn gượng (đổi thành vấp đá ngã vào); S1 chép bố cục ảnh, S3 cắt ngang hông, S4 mất vách đá. |
| take07 | 2.5 bản nháp 480p, $2.83, prompt hiện tại | Chờ người dùng xem; chưa review đủ nhóm. So nhanh: bám previz ở mọi cú (S1 đường chạy ngang, Lumo đi sang phải; S3 toàn thân), bản đồ ngược rồi xuôi đúng, vấp đá ngã vào bụi gai, vách đá sau bụi, chim trên cành, điểm cắt lệch tối đa 1 khung. Lỗi thấy được: cú xoay bản đồ (khoảng 14 s) thành lật mặt, lộ mặt sau trơn như tấm thẻ trong khoảng nửa giây. |
