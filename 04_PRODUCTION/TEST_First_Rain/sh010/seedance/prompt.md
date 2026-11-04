# TEST_First_Rain sh010 — prompt Seedance

Sinh trên Higgsfield, Seedance 2.5, video-to-video, 16:9, 1080p, 27 giây. Quy trình: `04_PRODUCTION/SEEDANCE.md`. Mốc giây lấy từ hằng số đầu `build_shot.py`; đổi timing previz thì sửa prompt theo.

Tải lên đúng thứ tự số. Thư mục gom sẵn: `renders/seedance_upload/` (không lên git; mất thì chép lại theo bảng, video render bằng `run.ps1 ref`).

| Số | File tải lên | Nguồn |
|---|---|---|
| `@Video 1` | `video1_previz.mp4` | `renders/sh010_ref.mp4` |
| `@Image 1` | `image1_lumo.png` | `02_ASSET_LIBRARY/Characters/Lumo/concept/lumo_hero.png` (tạm: ảnh tham chiếu Lumo chưa chốt) |
| `@Image 2` | `image2_tavi.png` | `02_ASSET_LIBRARY/Characters/Tavi/concept/tavi_hero.png` |
| `@Image 3` | `image3_nori.png` | `02_ASSET_LIBRARY/Characters/Nori/concept/nori_hero.png` |
| `@Image 4` | `image4_piko.png` | `02_ASSET_LIBRARY/Characters/Piko/concept/piko_hero.png` |
| `@Image 5` | `image5_world.png` | `01_BRAND/Brand_Guideline/world_key_art.png` |

- Máy Rain-O-Matic chưa có ảnh concept, đang tả bằng chữ. Có ảnh thì thêm `@Image 6` và thay đoạn tả máy trong ACTIVE REFERENCES.
- AUDIO đang để tiếng động (có sinh tiếng động hay không: chưa chốt). Không muốn tiếng thì thay cả khối AUDIO bằng `No sound at all.`
- Thoại theo phân cảnh, chỉ để khớp miệng (lồng tiếng ở hậu kỳ): LUMO "NƯỚC!" 7.5–8.3s · LUMO (thì thầm) "Thêm chút nữa thôi…" 19.5–20.5s · TAVI "Không chạm nút—!" 22.0–23.0s.

## Prompt

```text
# TEST_First_Rain sh010 — THE FIRST RAIN (27s, video-to-video)

On a dry hilltop above the clouds, four friends switch on a homemade rain machine for their thirsty seedling garden. A tiny cloud drops one raindrop on Lumo's nose, a gentle rain wakes the garden and Piko turns into a bowl to drink it. Lumo spots one strip still dry, reaches toward the forbidden red MAX POWER button and stops just short; then Piko, dazzled by the button's glint, bounces onto Lumo's back and the push presses Lumo's paw onto it. The machine goes wild and a huge dark cloud swells over the four stunned friends. Sunny afternoon. The hilltop is parched: pale cracked soil, dry yellow grass, small pale sprouts in a dark soil garden bed. Video-to-video pass driven by @Video 1.

ACTIVE REFERENCES
@Video 1 = the Blender previz (27s, 648 frames, 24fps), frame-aligned: 7 shots with hard cuts at 5.0s, 9.0s, 14.5s, 18.5s, 23.0s and 24.5s. SOLE authority for the camera (position, path, framing, lens, cut timing) and for every character's position and motion. Block figures, color = identity: the ORANGE blocks with tall ears = Lumo (@Image 1); the GREEN blocks with a long tail and a brown pack = Tavi (@Image 2); the floating LAVENDER sphere with wings and two antennae = Nori (@Image 3); the AQUA blob with two dark-blue horns = Piko (@Image 4). The small WHITE patch on each head marks where that character's face looks. The grey box with a glass dome and a chimney nozzle = the Rain-O-Matic 3000 machine; the RED disc on its right side = the MAX POWER button; the dark knob and the white dial on its left side = the GENTLE knob and the gauge. White puffy shapes = clouds. The dark rectangle with grey cones = the seedling garden; the pale strip along its far right edge = the patch that stays dry. Every block becomes the real character or object its position implies. Do NOT take any material, color, texture or lighting from @Video 1. If the text and the video disagree about motion, the video wins.
@Image 1 = Lumo — defines design, proportions, colors, red cape and brown shoulder bag. Background, pose and lighting not inherited.
@Image 2 = Tavi — defines design, proportions, colors, glowing crystal spikes, aviator cap with goggles, vest, belt and pouches. Background, pose and lighting not inherited.
@Image 3 = Nori — defines design, soft glow, four wings, star antennae and light trail. Background, pose and lighting not inherited.
@Image 4 = Piko — defines design, translucent jelly body, horns and floating water droplets. Background, pose and lighting not inherited.
@Image 5 = the world — defines palette, sunlight and the distant floating islands, pagodas, waterfalls and cloud sea. Its lush green ground is NOT inherited: this hilltop is dry. Camera angle not inherited.
The Rain-O-Matic 3000 has no reference image: a chunky rounded machine of riveted pastel metal panels on four stubby legs, a glowing glass dome on top, a small chimney nozzle that puffs clouds, a round GENTLE knob and a round gauge on its left side, one big round red MAX POWER button on its right side. Playful and handmade. No lettering anywhere on it.

STYLE
Soft stylized 3D animated film for young children: rounded soft shapes, pastel colors, warm gentle light, soft shadows. Every character keeps the materials of its reference image. Friendly and safe: nothing scary, no injuries, no realism, no live-action, no text, no logos, no watermarks. Original, no IP.

CHARACTERS
Lumo: small fox explorer, the tallest of the four; head almost half the body height; very short arms: the paws reach only to chin height, raised paws reach ear level at most; big ears that move with every emotion; fluffy tail.
Tavi: small green reptile inventor, about 85% of Lumo's height; short legs, long tail, hands with four fingers.
Nori: small round light spirit, about 70% of Lumo's height; always floating, never touches the ground; the wings flutter all the time.
Piko: jelly blob, about 80% of Lumo's height; no legs, moves only by bouncing, squashing and stretching like jelly.
Exactly four characters, never extras, no other creatures. Paws and hands always as in the references, never human anatomy.

CAMERA
Strictly follow the camera work of @Video 1, 1:1 and frame-aligned for all 27 seconds. Exactly 7 shots, hard cuts exactly at 5.0s, 9.0s, 14.5s, 18.5s, 23.0s and 24.5s; no added shots, no new angles. The camera stays low, at the characters' eye level, as in the video.

RULES
1. Exactly four characters at every moment (some may be outside the frame, as in @Video 1). Never a fifth.
2. Lumo never presses the button on purpose: at 20.5s the paw stops just short and starts pulling back. Only Piko's landing at 21.5s pushes the paw onto the button.
3. Piko lands softly on Lumo's back like a jelly pillow; nobody falls, nobody gets hurt.
4. The tiny cloud is exactly head-sized and is gone by 9.0s. Rain falls only from the cloud over the garden, from 9.0s on; the strip at the garden's right edge stays dry. No rain falls on the four friends.
5. The dark cloud at the end is comic, not scary: no lightning, no thunderbolts, no storm wind.
6. No speech sound: when a character talks, only the mouth moves.
7. No text, no letters, no numbers on the machine, the button, the gauge or anywhere in frame.

TIMELINE
0–5.0s — SHOT 1 (camera per @Video 1: wide, low, behind the group, slow push-in, tilting up at the end). Tavi stands at the machine's left side, reaching for the knob; Lumo on tiptoe in front of the machine, bouncing, tail wagging; Piko bouncing in place beside Lumo; Nori floating over the dry garden, wings fluttering. At 1.0s Tavi turns the GENTLE knob: the dome glows soft blue, the machine hums, the gauge needle rises. At 3.0s POOF: a tiny head-sized white cloud puffs out of the nozzle. 3.0–5.0s the cloud drifts over the group toward the camera; every head follows it; 3.6–4.6s Lumo turns around to keep watching it. END 5.0s: all four face the camera, looking up at the tiny cloud above Lumo.

5.0–9.0s — SHOT 2 (camera per @Video 1: medium close-up of Lumo, frontal, eye level, very slow push-in). At 5.5s the tiny cloud settles right on top of Lumo's head, ear tips poking out. At 6.0s Lumo looks up, cross-eyed with curiosity. At 7.0s one raindrop lands on Lumo's nose: plink; the ears spring straight up. 7.5–8.3s Lumo shouts one joyful word, mouth wide open, both paws up at ear level, tail wagging fast. 8.5–9.0s the tiny cloud fades into mist. Face: wide eyes, pure delight. END 9.0s: Lumo beaming, the cloud gone.

9.0–14.5s — SHOT 3 (camera per @Video 1: wide, from the front-right corner of the garden, slow lateral move). 9.0–10.2s a soft white rain cloud flows out of the nozzle and spreads over the garden; a gentle drizzle begins and the pale sprouts lift and turn greener. 9.0–10.0s Piko bounces into the garden. 9.3–9.9s Lumo turns and takes two steps toward the garden to watch. 9.5–10.5s Nori twirls one full turn in the rain, glowing brighter. At 11.0s Piko flattens into a wide bowl shape, mouth up, catching raindrops. At 12.5s Piko gulps the water and pops back to round, wobbling happily. 13.0–14.2s at the machine's left side, Tavi checks the gauge and nods, satisfied. 13.6–14.3s Piko hops to the garden's left edge, closest to the machine. END 14.5s: the garden is wet except one dry strip along its right edge with a wilted sprout.

14.5–18.5s — SHOT 4 (camera per @Video 1: Lumo in the left foreground seen from behind, the garden and the dry strip on the right; at 16.8s the camera swings left and pushes in to the red button on the machine's right side). 14.5–15.5s Lumo stares at the dry strip. At 15.5s Lumo's ears droop and the head tilts. At 16.5s Lumo's head turns toward the machine. 16.8–18.5s the camera pushes in until the red MAX POWER button fills the center of the frame. END 18.5s: the button, close, glossy, tempting.

18.5–23.0s — SHOT 5 (camera per @Video 1: wide frontal, low, static; Tavi on the left by the machine, the machine in the center, Piko at the garden edge on the right). 18.5–19.5s Lumo tiptoes around to the machine's right side and faces the button. 19.5–20.5s Lumo whispers (mouth moves only), one paw creeping toward the button. At 20.5s the paw stops just short; Lumo hesitates, ears flatten, and starts to pull the paw back. At 20.8s the button glints; Piko, dazzled, crouches and springs. At 21.5s Piko lands softly on Lumo's back with a jelly squish; the push presses Lumo's paw onto the button: CLICK. 21.6–22.0s Tavi steps out in front of the machine and sees them. 22.0–23.0s Tavi raises a hand and shouts (mouth moves only). END 23.0s: Lumo frozen with the paw on the button, Piko stuck on Lumo's back, eyes wide.

23.0–24.5s — SHOT 6 (camera per @Video 1: close-up insert of the button from the front-right). Lumo's paw on the sunken red button; the button light starts blinking. END 24.5s: the button blinking.

24.5–27.0s — SHOT 7 (camera per @Video 1: wide, very low angle from the front, looking up, static). At 24.5s the machine starts to shake and rattle, the dome flashes red, the gauge needle shivers at the end of the scale. 24.5–25.5s Nori floats out in front of the group. 25.0–26.0s the rain cloud rolls over the machine, swells to about three times its size and darkens to charcoal grey. At 25.0s all four look up and freeze, mouths open; Nori's star antennae flicker; Piko still on Lumo's back. Hold the final frame to 27.0s.

AUDIO
No music, no dialogue, no voice. Sound effects: machine hum from 1.0s, gentle rain patter from 9.0s. Timed accents: 1.0s knob click; 3.0s soft poof; 7.0s plink; 12.5s slurp; 14.3s boing; 20.8s sparkle ting and boing; 21.5s jelly squish and button click; 24.5s rattling machine and a rising VRRRM; 25.0–27.0s low rolling cloud rumble, no thunder crack.

HOLD
@Video 1 camera 1:1 for all 27 seconds; 7 shots, cuts at 5.0 / 9.0 / 14.5 / 18.5 / 23.0 / 24.5s. Exactly four characters; @Image 1–4 identities constant. Lumo's paw stops on its own at 20.5s; the button is pressed only by Piko's landing at 21.5s. No text, no logos, no watermarks, nothing scary.
```

## Take

- `sh010_take01.mp4`: chưa soát.
