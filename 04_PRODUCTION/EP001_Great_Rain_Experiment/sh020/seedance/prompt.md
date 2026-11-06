# EP001 sh020 — prompt Seedance

Cảnh 1 tập 01, đoạn 2 (28.8–55.0 giây của cảnh, S7–S14). Sinh trên Higgsfield, Seedance 2.5, video-to-video, 16:9, 1080p, 26.2 giây. Quy trình: `04_PRODUCTION/SEEDANCE.md`. Mốc giây = mốc trong `timing.py` của previz 2D trừ `OFFSET` 28.8 (`build_shot.py`); đổi timing previz thì sửa prompt theo.

Tải lên đúng thứ tự số. Thư mục gom sẵn: `renders/seedance_upload/` (không lên git; mất thì chép lại theo bảng, video render bằng `run.ps1 ref`).

| Số | File tải lên | Nguồn |
|---|---|---|
| `@Video 1` | `video1_previz.mp4` | `renders/sh020_ref.mp4` |
| `@Image 1` | `image1_lumo.png` | `02_ASSET_LIBRARY/Characters/Lumo/concept/lumo_hero.png` (tạm: ảnh tham chiếu Lumo chưa chốt) |
| `@Image 2` | `image2_tavi.png` | `02_ASSET_LIBRARY/Characters/Tavi/concept/tavi_hero.png` |
| `@Image 3` | `image3_nori.png` | `02_ASSET_LIBRARY/Characters/Nori/concept/nori_hero.png` |
| `@Image 4` | `image4_piko.png` | `02_ASSET_LIBRARY/Characters/Piko/concept/piko_pouch_ref.png` |
| `@Image 5` | `image5_valley.png` | `02_ASSET_LIBRARY/Environments/Cloud_Valley/concept/cloud_valley_dry_hero.png` |
| `@Image 6` | `image6_wonder_compass.png` | `02_ASSET_LIBRARY/Props/Wonder_Compass/concept/wonder_compass_ref.png` |
| `@Image 7` | `image7_valley_critters.png` | `02_ASSET_LIBRARY/Characters/Valley_Critters/concept/valley_critters_ref.png` |
| `@Image 8` | `image8_inventor_pack.png` | `02_ASSET_LIBRARY/Props/Inventor_Pack/concept/inventor_pack_ref.png` |

- Áo choàng Lumo đang để theo ảnh tham chiếu (chưa chốt dài tới gối như concept hay ngắn tới hông như bản 3D trong Character Bible).
- AUDIO đang để tiếng động như `TEST_First_Rain` (có sinh tiếng động hay không: chưa chốt). Không muốn tiếng thì thay cả khối AUDIO bằng `No sound at all.`
- Thoại theo kịch bản, chỉ để khớp miệng (lồng tiếng ở hậu kỳ): LUMO "Có gì lạ kìa!" 0.1–1.3s · LUMO "Thìa thôi mà?" 12.6–13.8s · TAVI "Gom hơi nước, làm lạnh, sẽ có mưa!" 19.8–23.4s · TAVI "Lên đỉnh đồi, trên đó lạnh hơn!" 23.5–25.7s.

## Prompt

```text
# EP001 sh020 — THE SPOON AND THE CLOUDY HILLTOP (26.2s, video-to-video)

In a parched valley garden, Lumo's Wonder Compass points at Piko's little pouch. Piko pulls out a spoon and digs until the spoon bends; held right over the spoon, the compass star still swings back to the pouch. Tavi stamps on the rock-hard ground, notices the dew on a dry leaf and a thin cloud clinging to the hilltop, gets an idea, acts out how to make rain with both hands and points up the hill; everyone looks up. Sunny day in the Valley of Clouds. Video-to-video pass driven by @Video 1.

ACTIVE REFERENCES
@Video 1 = the Blender previz (26.2s, 629 frames, 24fps), frame-aligned: 8 shots with hard cuts at 2.0s, 6.75s, 8.7s, 10.9s, 16.05s, 18.9s and 23.5s. SOLE authority for the camera (position, path, framing, lens, cut timing) and for every character's position and motion. Block figures, color = identity: the ORANGE blocks with tall ears = Lumo (@Image 1); the small dark box on Lumo's hip = Lumo's brown leather crossbody bag. The GREEN blocks with a long tail and a brown pack = Tavi (@Image 2) wearing the Inventor Pack (@Image 8); the dark bar on Tavi's head = the goggles on Tavi's aviator cap. The floating LAVENDER sphere with wings and two antennae = Nori (@Image 3); the lavender cone under Nori's sphere = Nori's soft light trail, not a leg or a tail. The AQUA blob with two dark-blue horns = Piko (@Image 4); the dark ball on Piko's left hip with a thin strap = Piko's pouch, worn as in @Image 4. The small WHITE patch on each head marks where that character's face looks. The grey disc in Lumo's paw with a dark bar on its face = the Wonder Compass (@Image 6); the dark bar = its glowing star needle. The small grey stick with an oval end = a plain metal spoon. The dark rectangle with small grey cones = the stone-edged garden bed with thin drooping seedlings. The thin grey pole with a flat oval on top = the dry curled twig with one dry leaf. The grey stem with a small disc = the small wilted flower. The small pale blobs wearing a flat dark disc = the tiny valley creatures (@Image 7) under their dry leaf hats. The big grey dome on the right = the dry grassy hill; the white puffs on its top = the thin band of white cloud clinging to the summit. Dark lines on the ground = cracks in the dry earth. Small flat white puffs on the ground = little dust puffs. The glowing yellow ball at Piko's pouch = a gold glint from the pouch's mouth; the white twinkle at the leaf tip = dew sparkling. Every block becomes the real character or object its position implies. Do NOT take any material, color, texture or lighting from @Video 1. If the text and the video disagree about motion, the video wins.
@Image 1 = Lumo — defines design, proportions, colors, red cape and brown leather crossbody bag. Background, pose and lighting not inherited.
@Image 2 = Tavi — defines design, proportions, colors, glowing crystal spikes, aviator cap with goggles, vest, belt and the Inventor Pack on the back. Background, pose and lighting not inherited.
@Image 3 = Nori — defines design, soft glow, four wings, star antennae and light trail. Background, pose and lighting not inherited.
@Image 4 = Piko wearing the pouch — defines design, translucent jelly body, dark-blue horns, and how the pouch is worn: a thin gold cord looped over the root of Piko's right horn, down the back and diagonally under the mouth; the small purple velvet pouch with the cream cloud emblem at Piko's left hip, drawstring gathered. Background, pose and lighting not inherited.
@Image 5 = the Valley of Clouds in drought — defines the look of the location: pale cracked earth, dry yellow grass, smooth pale rocks, the stone-edged garden bed with drooping seedlings, the curled dry twig and leaf, the wilted flower, the dry grassy hill with its cloud band, floating islands and the cloud sea far away, warm sunlight. Layout follows @Video 1. Camera angle not inherited.
@Image 6 = the Wonder Compass — defines the gold case, the glass face and the glowing eight-point star needle. Paw-sized in Lumo's paw, no lanyard. No letters or numbers on its face.
@Image 7 = the tiny valley creatures — defines their design: small peach-beige bean-shaped bodies, each wearing a dry leaf as a hat. In this clip they only sit, droopy and sad: the one beside the garden bed keeps its dry leaf hat slid down over its eyes (second pose of @Image 7); the others sit as in the first pose.
@Image 8 = Tavi's Inventor Pack — defines only the backpack on Tavi's back: brown leather and tan canvas, a blueprint roll on top, glowing crystal tubes on the sides, a gold gear emblem. It stays closed on Tavi's back; nothing comes out of it in this clip.

STYLE
Soft stylized 3D animated film for young children: rounded soft shapes, pastel colors, warm gentle light, soft shadows. Every character keeps the materials of its reference image. Friendly and safe: nothing scary, no injuries, no realism, no live-action, no text, no logos, no watermarks. Original, no IP.

CHARACTERS
Lumo: small fox explorer, the tallest of the four; head almost half the body height; very short arms: the paws reach only to chin height, raised paws reach ear level at most; big ears that move with every emotion; fluffy tail, always showing below the cape hem, separate from the cape; red cape and brown crossbody bag.
Tavi: small green reptile inventor, about 85% of Lumo's height; short legs, long tail, glowing cyan crystal spikes along the back and tail as in @Image 2 (the blocks do not show them), aviator cap with goggles, the Inventor Pack (@Image 8) on the back.
Nori: small round light spirit, head and body one piece, about 70% of Lumo's height; NO legs: below the body only a soft glowing light trail; two antennae tipped with small yellow stars; tiny arms; always floating, never touches the ground; the four wings flutter all the time.
Piko: jelly blob, about 80% of Lumo's height; body shape exactly as in @Image 4, a soft dome wider at the base than at the top (the round previz block is only a stand-in); no legs, moves only by bouncing or sliding along the ground like jelly, squashing and stretching; tiny paws. A few tiny water droplets bounce around Piko's jelly body (Piko has just drunk the last dewdrop). Piko always wears the pouch at the left hip as in @Image 4: fist-sized, its drawstring mouth opens just enough for Piko's paw, nothing ever spills out.
Exactly four main characters, plus the tiny valley creatures where @Video 1 shows them (about one sixth of Lumo's height); never anyone else. Paws and hands always as in the references, never human anatomy.

CAMERA
Strictly follow the camera work of @Video 1, 1:1 and frame-aligned for all 26.2 seconds. Exactly 8 shots, hard cuts exactly at 2.0s, 6.75s, 8.7s, 10.9s, 16.05s, 18.9s and 23.5s; no added shots, no new angles. Shot 6 is one continuous take: a close-up of the dry leaf, then the camera pans right and slightly up to the cloud-topped hilltop, widening. The camera stays at the characters' eye level unless the video goes higher.

RULES
1. Exactly four characters at every moment (some may be outside the frame, as in @Video 1). Never a fifth. The only other living things are the tiny valley creatures (@Image 7) where @Video 1 shows them; they sit still, droopy and sad.
2. The Wonder Compass star needle points at Piko's pouch. Only while the compass is held over the spoon does the needle jerk toward the spoon, then it swings back to the pouch. The spoon itself never glows; the gold glint comes only from the pouch's mouth.
3. The spoon is an ordinary metal spoon. It bends on the third hit; it does not break. Piko only shivers like jelly; nobody gets hurt.
4. Tavi's two stamps raise only small dust puffs. The ground stays hard: no hole opens, no water comes out of the ground.
5. No rain and no rain cloud in this clip: clear sky, only the thin band of cloud clinging to the hilltop.
6. No speech sound: when a character talks, only the mouth moves.
7. No text, no letters, no numbers on the compass, the pouch or anywhere in frame.

TIMELINE
0–2.0s — SHOT 1 (camera per @Video 1: medium two-shot, eye level, static; Lumo on the left, Piko on the right, Nori floating above, Tavi at the left edge). Lumo holds the Wonder Compass out toward Piko, the glowing star needle pointing at Piko's pouch, and the pouch's mouth glints gold. 0.1–1.3s Lumo talks, mouth moving: eyes sparkling, ears up, tail wagging. At 0.7s Piko looks down at the pouch on the left hip. At 1.4s Piko pushes one paw into the pouch and starts rummaging. END 2.0s: Lumo upright again, the compass lowered to the chest; Piko's paw in the pouch.

2.0–6.75s — SHOT 2 (camera per @Video 1: medium shot of Piko, eye level, static; the twig with the dry leaf on the left, the wilted flower on the right, Lumo at the left edge, the bottom of Nori's round body and its light trail at the top left). Piko rummages, the pouch bouncing, until 2.7s. At 2.8s Piko pulls out a plain metal spoon and holds it up in front of the face. At 3.2s Piko looks at the spoon and blinks in surprise. At 3.7s Piko glances over at the wilted flower and holds the look. 4.1–4.4s Piko looks down at the ground, determined, and raises the spoon high by 4.8s. Piko digs: CLONK at 5.1s, CLONK at 5.7s, CLONK at 6.4s; each hit lands on the hard ground in front of Piko with a little dust puff while Piko's jelly body squashes. At 6.4s the spoon's handle bends back into a curve and Piko's whole jelly body starts to shiver. END 6.75s: Piko shivering, holding the bent spoon.

6.75–8.7s — SHOT 3 (camera per @Video 1: close-up of Piko and the bent spoon). Piko's jelly body keeps shivering until 7.4s while Piko lifts the bent spoon to eye level. 7.5–8.1s Piko's eyes swivel sideways to the bent spoon held at Piko's side; Piko stares at it and blinks twice, puzzled. 8.2–8.6s Piko leans forward and lays the bent spoon on the ground, away from the pouch. END 8.7s: the bent spoon lying on the ground.

8.7–10.9s — SHOT 4 (camera per @Video 1: close-up insert from above and in front: the bent spoon in the middle; Piko's pouch at the upper right). At 8.7s Piko bounces a little way back. 8.7–9.0s Lumo steps in: only Lumo's feet show at the upper left. 9.0–9.6s Lumo bends deep at the waist and the Wonder Compass comes into frame just above the spoon, its face tilted toward us, Lumo's bending body filling the upper left; the arm stays short, only the bending body brings the compass down. At 9.2s the glowing star needle jerks from the pouch down to the spoon and holds there until 9.6s. At 9.6s the needle swings back to Piko's pouch, wobbling until it settles. Once it settles, the pouch's mouth glints gold, twice. Until 10.9s the needle stays on the pouch. END 10.9s: the needle pointing at the pouch, the spoon ignored.

10.9–14.6s — SHOT 5 (camera per @Video 1: medium-wide, eye level, static; Tavi on the left, Lumo in the center, Piko on the right, Nori floating above, calm and attentive). 10.9–11.5s Tavi walks up to look at the bent spoon. 11.0–11.3s Lumo is still bent low over the spoon. 11.3–11.6s Lumo straightens up, eyes still on the spoon. 11.6–12.0s Lumo looks down at the compass. 12.1–12.35s Lumo tilts the head, ears tilting, and holds the puzzled tilt until 12.5s. 12.6–13.8s Lumo talks, puzzled, mouth moving, the compass held out in one paw. At 14.1s Piko blinks at Lumo. END 14.6s: Tavi looking down at the cracked ground.

14.6–16.05s — SHOT 5 continues, same camera. Tavi hops and stamps on the cracked ground: CLOK at 14.9s, CLOK at 15.3s, each with a small dust puff, the ground hard as rock. Lumo turns to watch Tavi; Nori drifts over to watch too. At 15.6s Tavi looks up at the dry leaf on the twig, still beaded with dew. END 16.05s: Tavi's face tilted up toward the leaf.

16.05–18.9s — SHOT 6 (camera per @Video 1: close-up of the dry curled leaf on the twig, one continuous take; Lumo's left side at the left edge, Nori at the upper left, Piko large in the lower right foreground). Tiny dew drops on the leaf twinkle in the sunlight; Piko looks up at the twinkling leaf, eyes sparkling, and gives one small bounce. 16.9–17.9s the camera pans right and slightly up from the leaf to the summit of the big hill on the right, widening, where a thin band of white cloud clings; Piko slides out to the lower left, only Piko's horn stays in the lower-left corner. Hold on the cloud-topped summit until 18.9s. END 18.9s: the hilltop and its thin cloud band.

18.9–23.5s — SHOT 7 (camera per @Video 1: medium two-shot, eye level; Tavi on the left facing right, Lumo on the right facing Tavi, Nori partly visible above, the edge of Piko at the right edge). At 18.9s, head still raised toward the hilltop, Tavi's eyes light up and the mouth pops open in an "aha". 19.15–19.35s Tavi snaps the head to Lumo with a little hop and one raised finger, held until 19.8s; Nori glides back, smiling softly. 19.8–23.4s Tavi talks, mouth moving, acting it out with both hands: 19.8–21.0s sweeps both arms back and gathers them in front of the belly, as if gathering mist; 21.0–22.2s crosses both arms over the chest, hugging the shoulders, and shivers as if cold, while Lumo does a quick whole-body shiver, ears flattening, paws staying low at the sides; 22.2–23.4s Tavi raises both hands high and wiggles the fingers while lowering them, like falling rain. Lumo nods at each step, ears up, eyes wide. END 23.5s: Tavi's hands at chest height, Lumo leaning in, fascinated.

23.5–26.2s — SHOT 8 (camera per @Video 1: wide, eye level, static; the group on the left, the hill with its thin cloud band on the right). 23.5–24.0s Tavi strides forward past Lumo toward the hill. 24.0–24.2s Tavi turns to the hill and raises one arm high, pointing at the summit, held to the end. 23.5–25.7s Tavi talks, mouth moving. At 24.2s Lumo, Piko and Nori follow Tavi's arm and look up at the hilltop. Hold to 26.2s. END 26.2s: Tavi pointing at the summit; Lumo and Nori look up at it in profile, Piko's face in three-quarter view.

AUDIO
No music, no dialogue, no voice. Sound effects: soft dry breeze. Timed accents: 1.4s rustle in the pouch; 2.8s small pop as the spoon comes out; 5.1s, 5.7s and 6.4s dull clonk on hard ground; 6.4s comic boing as the spoon bends; 9.2s quick compass tick; 9.6s whoosh, then a gold twinkle as the pouch glints; 14.9s and 15.3s dull knock; 16.05s soft dew sparkle; 18.9s bright aha ding.

HOLD
@Video 1 camera 1:1 for all 26.2 seconds; 8 shots, cuts at 2.0 / 6.75 / 8.7 / 10.9 / 16.05 / 18.9 / 23.5s. Exactly four characters; @Image 1–4 identities constant; Piko's pouch worn as in @Image 4; Tavi's Inventor Pack as in @Image 8; the compass as in @Image 6; the tiny valley creatures as in @Image 7. The star needle returns to Piko's pouch at 9.6s. No rain, no text, no logos, no watermarks, nothing scary.
```

## Take

- Chưa sinh.
