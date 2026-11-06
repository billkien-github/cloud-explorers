# EP001 sh010 — prompt Seedance

Cảnh 1 tập 01, đoạn 1 (0–28.8 giây của cảnh, S1–S6). Sinh trên Higgsfield, Seedance 2.5, video-to-video, 16:9, 1080p, 28.8 giây. Quy trình: `04_PRODUCTION/SEEDANCE.md`. Mốc giây = mốc trong `timing.py` của previz 2D (`OFFSET` 0, `build_shot.py`); đổi timing previz thì sửa prompt theo.

Tải lên đúng thứ tự số. Thư mục gom sẵn: `renders/seedance_upload/` (không lên git; mất thì chép lại theo bảng, video render bằng `run.ps1 ref`).

| Số | File tải lên | Nguồn |
|---|---|---|
| `@Video 1` | `video1_previz.mp4` | `renders/sh010_ref.mp4` |
| `@Image 1` | `image1_lumo.png` | `02_ASSET_LIBRARY/Characters/Lumo/concept/lumo_hero.png` (tạm: ảnh tham chiếu Lumo chưa chốt) |
| `@Image 2` | `image2_tavi.png` | `02_ASSET_LIBRARY/Characters/Tavi/concept/tavi_hero.png` |
| `@Image 3` | `image3_nori.png` | `02_ASSET_LIBRARY/Characters/Nori/concept/nori_hero.png` |
| `@Image 4` | `image4_piko.png` | `02_ASSET_LIBRARY/Characters/Piko/concept/piko_pouch_ref.png` |
| `@Image 5` | `image5_valley.png` | `02_ASSET_LIBRARY/Environments/Cloud_Valley/concept/cloud_valley_dry_hero.png` |
| `@Image 6` | `image6_wonder_compass.png` | `02_ASSET_LIBRARY/Props/Wonder_Compass/concept/wonder_compass_ref.png` |
| `@Image 7` | `image7_valley_critters.png` | `02_ASSET_LIBRARY/Characters/Valley_Critters/concept/valley_critters_ref.png` |
| `@Image 8` | `image8_inventor_pack.png` | `02_ASSET_LIBRARY/Props/Inventor_Pack/concept/inventor_pack_ref.png` |

- Tên phim (10.0–13.0s) chèn ở hậu kỳ; prompt dặn không vẽ chữ, giữ bầu trời trống.
- Giọt nước quanh Piko theo previz 2D: chưa có trước cú húp, hiện từ cú húp (chờ chốt trong Character Bible).
- Áo choàng Lumo đang để theo ảnh tham chiếu (chưa chốt dài tới gối như concept hay ngắn tới hông như bản 3D trong Character Bible).
- AUDIO đang để tiếng động như `sh020` (có sinh tiếng động hay không: chưa chốt). Không muốn tiếng thì thay cả khối AUDIO bằng `No sound at all.`
- Thoại theo kịch bản, chỉ để khớp miệng (lồng tiếng ở hậu kỳ): NORI "Mầm cây sắp héo khô hết rồi." 15.2–17.2s · LUMO "Đi tìm nước cho vườn!" 18.3–19.7s · TAVI "Coi chừng vết nứt!" 22.9–24.3s.

## Prompt

```text
# EP001 sh010 — THE LAST DEWDROP (28.8s, video-to-video)

In a parched valley garden, Piko waits under a dry leaf for the last dewdrop and slurps it in one gulp, and the little flower that was waiting for it droops. Nori shines a soft light on a thin seedling; Lumo springs up to find water, dashes off, trips over a narrow crack and is caught by Tavi. Then Lumo's Wonder Compass beeps in the bag; Lumo pulls it out and its star needle spins, then points at Piko's pouch. Sunny day in the Valley of Clouds. Video-to-video pass driven by @Video 1.

ACTIVE REFERENCES
@Video 1 = the Blender previz (28.8s, 691 frames, 24fps), frame-aligned: 6 shots with hard cuts at 3.9s, 9.6s, 13.4s, 19.8s and 26.4s. SOLE authority for the camera (position, path, framing, lens, cut timing) and for every character's position and motion. Block figures, color = identity: the ORANGE blocks with tall ears = Lumo (@Image 1); the small dark box on Lumo's hip = Lumo's brown leather crossbody bag. The GREEN blocks with a long tail and a brown pack = Tavi (@Image 2) wearing the Inventor Pack (@Image 8); the dark bar on Tavi's head = the goggles on Tavi's aviator cap. The floating LAVENDER sphere with wings and two antennae = Nori (@Image 3); the lavender cone under Nori's sphere = Nori's soft light trail, not a leg or a tail. The AQUA blob with two dark-blue horns = Piko (@Image 4); the dark ball on Piko's left hip with a thin strap = Piko's pouch, worn as in @Image 4; the small aqua blobs on Piko's sides = Piko's tiny bean-shaped jelly paws as in @Image 4, never bubbles. The small WHITE patch on each head marks where that character's face looks. The small glowing light-blue ball on the leaf = the last dewdrop. The thin grey pole with a flat oval on top = the dry curled twig with one dry leaf, standing exactly where @Video 1 places it. The grey stem with a small disc = the small flower: a pink flower head on a thin stem, as in @Image 5, never a seedling. The dark rectangle with small grey cones = the stone-edged garden bed with thin drooping seedlings. The big pale cone from Nori's paw down to a seedling = a soft beam of warm light; the glowing ball at its end = the lit thin seedling. The small pale blobs wearing a flat dark disc = the tiny valley creatures (@Image 7) under their dry leaf hats. The dark strip across the ground in front of the garden = the narrow, shallow crack Lumo trips on; dark lines elsewhere = cracks in the dry earth. The big grey dome on the right = the dry grassy hill; the white puffs on its top = the thin band of white cloud clinging to the summit. The small yellow glow at Lumo's bag = the compass beeping inside it. The grey disc in Lumo's paws with a dark bar on its face = the Wonder Compass (@Image 6); the dark bar = its glowing star needle. The glowing yellow ball at Piko's pouch = a gold glint from the pouch's mouth. Every block becomes the real character or object its position implies. Do NOT take any material, color, texture or lighting from @Video 1. If the text and the video disagree about motion, the video wins.
@Image 1 = Lumo — defines design, proportions, colors, red cape and brown leather crossbody bag. Background, pose and lighting not inherited.
@Image 2 = Tavi — defines design, proportions, colors, glowing crystal spikes, aviator cap with goggles, vest and belt. Background, pose and lighting not inherited.
@Image 3 = Nori — defines design, soft glow, four wings, star antennae and light trail. Background, pose and lighting not inherited.
@Image 4 = Piko wearing the pouch — defines design, translucent jelly body, dark-blue horns, and how the pouch is worn: a thin gold cord looped over the root of Piko's right horn, down the back and diagonally under the mouth; the small purple velvet pouch with the cream cloud emblem at Piko's left hip, drawstring gathered. Background, pose and lighting not inherited.
@Image 5 = the Valley of Clouds in drought — defines the look of the location: pale cracked earth, dry yellow grass, smooth pale rocks, the stone-edged garden bed with drooping seedlings, the curled dry twig and leaf, the small flower, the dry grassy hill with its cloud band, floating islands and the cloud sea far away, warm sunlight. Layout follows @Video 1. Camera angle not inherited.
@Image 6 = the Wonder Compass — defines the gold case, the glass face and the glowing eight-point star needle. Paw-sized in Lumo's paws, no lanyard. No letters or numbers on its face.
@Image 7 = the tiny valley creatures — defines their design: small peach-beige bean-shaped bodies, each wearing a dry leaf as a hat. In this clip they only sit, droopy and sad, as in the first pose of @Image 7; the one beside the thin seedling sighs as in the second pose.
@Image 8 = Tavi's Inventor Pack — defines only the backpack on Tavi's back: brown leather and tan canvas, a blueprint roll on top, glowing crystal tubes on the sides, a gold gear emblem. It stays closed on Tavi's back; nothing comes out of it in this clip.

STYLE
Soft stylized 3D animated film for young children: rounded soft shapes, pastel colors, warm gentle light, soft shadows. Every character keeps the materials of its reference image. Friendly and safe: nothing scary, no injuries, no realism, no live-action, no text, no logos, no watermarks. Original, no IP.

CHARACTERS
Lumo: small fox explorer, the tallest of the four; head almost half the body height; very short arms: the paws reach only to chin height, raised paws reach ear level at most; big ears that move with every emotion; fluffy tail, always showing below the cape hem, separate from the cape; red cape and brown crossbody bag.
Tavi: small green reptile inventor, about 85% of Lumo's height; short legs, long tail, glowing cyan crystal spikes along the back and tail as in @Image 2 (the blocks do not show them), aviator cap with goggles, the Inventor Pack (@Image 8) on the back.
Nori: small round light spirit, head and body one piece, about 70% of Lumo's height; NO legs: below the body only a soft glowing light trail; two antennae tipped with small yellow stars; tiny arms; always floating, never touches the ground; the four wings flutter all the time.
Piko: jelly blob, about 80% of Lumo's height; body shape exactly as in @Image 4, a soft dome wider at the base than at the top (the round previz block is only a stand-in); no legs, moves only by bouncing or sliding along the ground like jelly, squashing and stretching; tiny paws. Piko always wears the pouch at the left hip as in @Image 4, drawstring gathered, nothing spills out: the gold cord is ONE strand across the front, diagonally from under the mouth to the pouch at Piko's left hip; never a necklace, never two strands, the pouch never hangs at the middle of the belly. Before the slurp Piko is dry; from the slurp on, a few tiny water droplets bounce around Piko's jelly body.
Exactly four main characters, plus the tiny valley creatures where @Video 1 shows them (about one sixth of Lumo's height); never anyone else. Paws and hands always as in the references, never human anatomy.

CAMERA
Strictly follow the camera work of @Video 1, 1:1 and frame-aligned for all 28.8 seconds. Keep every shot exactly as framed in @Video 1, never tighter, never wider; the shot sizes named below are only labels. Exactly 6 shots, hard cuts exactly at 3.9s, 9.6s, 13.4s, 19.8s and 26.4s; no added shots, no new angles. Shot 3 is a wide establishing shot with a slow drift; every other shot is static. The camera stays at the characters' eye level, as in the video.

RULES
1. Exactly four characters at every moment (some may be outside the frame, as in @Video 1). Never a fifth. The only other living things are the tiny valley creatures (@Image 7) where @Video 1 shows them; they sit still, droopy and sad.
2. The dewdrop is the only water in the valley: one small drop on the leaf, caught in Piko's mouth in one gulp. No rain, no puddles, no water anywhere else.
3. Lumo's trip is comic, not scary: the crack is narrow and shallow; Lumo only tips forward over it and never falls in; Tavi catches the strap of Lumo's bag; nobody gets hurt.
4. Nori's light is a soft warm glow, never a laser, never sparks or fire.
5. Until Lumo pulls it out, the Wonder Compass stays hidden inside Lumo's bag; only a small gold glow blinks there. Out of the bag, its star needle spins, then points at Piko's pouch: the longest, brightest point of the star is its tip, and a thin gold beam runs from the tip to the pouch. The gold glint comes only from the pouch's mouth.
6. No text anywhere: the film title is added later in editing, so during the title moment the upper part of the frame stays calm: only sky, a few small white clouds, the floating islands and the cloud sea far away, as in @Image 5. No rain, no grey or dark cloud; near the hill, the thin band clinging to the summit is the only cloud.
7. No speech sound: when a character talks, only the mouth moves.
8. Characters that @Video 1 shows at a frame edge stay visible at that edge, partly cut; nobody vanishes within a shot, and nothing passes in front of a character's face. Faces stay cute and readable: no angry frowns, no side-eye.

TIMELINE
0–3.9s — SHOT 1 (camera per @Video 1: close shot, eye level, static; the curled dry leaf on the twig at the upper left with the last dewdrop on it, Piko large in the center right looking up, the small flower at the lower right). From 0.3s the dewdrop glints in the sunlight. From 0.8s Piko stares up at it, eyes wide and round, mouth slightly open, jelly body breathing softly; the little flower stretches up toward the drop too. From 1.6s the dewdrop rolls toward the leaf tip in short slides: it rolls… stops… rolls… stops; each time it stops, Piko leans back a little further and the flower leans toward it. END 3.9s: the drop halfway along the leaf, Piko and the flower waiting.

3.9–6.0s — SHOT 2 (camera per @Video 1: medium shot of Piko, eye level, static; the twig and the leaf on the left, the flower on the right, the edge of Lumo at the left edge). The drop rolls on to the very tip of the leaf by 5.4s and hangs there, heavy and trembling. At 5.3s Piko squashes down like a spring and bounces straight up; at 5.65s Piko catches the dewdrop in the mouth in one gulp. Piko lands softly by 6.0s with a jelly squish; a few tiny water droplets now bounce around Piko's body. END 6.0s: Piko back on the ground, cheeks full, the leaf tip empty.

6.0–9.6s — SHOT 2 continues, same camera. 6.3–7.0s the little flower droops, its head hanging down. 7.0–7.4s Piko licks the lips, happy. 7.5–8.1s Piko turns and looks down at the drooping flower. 8.1–9.4s Piko squashes into a sheepish grin, one tiny paw rubbing the cheek, a drop of sweat on the forehead; 8.5–9.0s Piko peeks at the flower with one eye, then grins again. END 9.6s: Piko grinning sheepishly beside the drooped flower.

9.6–13.4s — SHOT 3 (camera per @Video 1: wide establishing shot of the parched valley, eye level, slow drift to the right; Tavi and Lumo small at the left, slumped and sad; Piko by the garden bed; the big dry hill with its cloud band on the right; a few tiny valley creatures sitting droopy under their leaf hats). Piko bounces gently in place. 10.0–13.0s the film title will be added here in editing: no text, keep the sky calm. 10.5–13.6s Nori flies in from the right edge, across the sky in front of the hill, and glides down toward the garden, wings fluttering, light trail glowing. END 13.4s: Nori gliding down toward the garden, the others still slumped.

13.4–17.6s — SHOT 4 (camera per @Video 1: medium shot, eye level, static; Tavi at the left edge, Lumo slumped at the left, Nori hovering in the center, the thin seedling and a tiny creature in front, Piko at the right, facing away and bouncing gently). From 13.8s Nori points one tiny paw down and shines a soft beam of warm light onto the thinnest seedling. 14.0–15.1s the tiny creature beside it gives a big sigh and its dry leaf hat slides down over its eyes. 15.2–17.2s Nori talks softly, mouth moving, no voice, eyes sad. Lumo listens, ears drooping, tail down. END 17.6s: Lumo still slumped, Nori's light on the seedling.

17.6–19.8s — SHOT 4 continues, same camera. 17.6–18.1s Lumo springs up with a little hop, ears shooting up, tail wagging. 18.3–19.7s Lumo talks, mouth moving, no voice, determined, one paw thrust forward toward the garden. Nori's light stays on the seedling until 19.8s. END 19.8s: Lumo ready to run.

19.8–22.8s — SHOT 5 (camera per @Video 1: medium-wide, eye level, static; Tavi on the left, Lumo in the center, the crack in front of the garden, Nori floating above, Piko at the right). 19.9–20.7s Lumo dashes toward the garden: one step, two steps. At 20.7s Lumo's foot catches in the narrow crack and Lumo stumbles forward, paws flailing, until 21.2s. 20.75–21.2s Tavi lunges and grabs the strap of Lumo's leather bag. 21.2–22.2s Lumo tips forward over the crack, held by Tavi, round eyes staring down, tail up; Nori looks down, worried. 22.2–22.8s Tavi pulls Lumo back upright. END 22.8s: both standing, Lumo safe.

22.8–26.4s — SHOT 5 continues, same camera. 22.9–24.3s Tavi talks, mouth moving, no voice, pointing down at the crack; Lumo looks down, ears drooping, and shrugs, embarrassed. 24.4–25.0s Tavi steps back. 24.5–25.8s the compass beeps three times inside Lumo's bag, a small gold glow blinking there; Lumo looks down at the bag, ears up. At 25.0s Piko turns toward Lumo. 25.8–26.4s Lumo pulls the Wonder Compass out of the bag and holds it in front with both paws. END 26.4s: Lumo looking down at the compass.

26.4–28.8s — SHOT 6 (camera per @Video 1: close-up over Lumo's paws: the Wonder Compass in the lower left foreground, its face tilted toward us; Piko and the pouch in the background on the right). 26.6–27.7s the glowing star needle spins wildly, then slows and stops, pointing at Piko's pouch: its longest, brightest point aims at the pouch and a thin gold beam runs from it to the pouch. Right after it stops, the pouch's mouth glints gold. Hold to 28.8s. END 28.8s: the needle pointing at the pouch.

AUDIO
No music, no dialogue, no voice. Sound effects: soft dry breeze. Timed accents: 0.3s tiny sparkle on the dewdrop; 5.65s slurp sound; 6.3s soft droop; 14.0s small sigh; 17.6s springy boing; 20.7s stumble thump; 24.5–25.8s three soft compass beeps; 26.6–27.7s whirring spin ending in a click, then a gold twinkle.

HOLD
@Video 1 camera 1:1 for all 28.8 seconds; 6 shots, cuts at 3.9 / 9.6 / 13.4 / 19.8 / 26.4s. Exactly four characters; @Image 1–4 identities constant; Piko's pouch on ONE diagonal gold cord at the left hip, as in @Image 4; characters at frame edges stay visible; Tavi's Inventor Pack as in @Image 8; the compass as in @Image 6; the tiny valley creatures as in @Image 7. Lumo only tips over the narrow crack and never falls in. No rain, no text (the title is added later), no logos, no watermarks, nothing scary.
```

## Take

- Chưa sinh.
