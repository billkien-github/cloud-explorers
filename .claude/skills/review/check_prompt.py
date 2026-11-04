"""
Kiểm seedance/prompt.md của một shot previz theo quy tắc trong 04_PRODUCTION/SEEDANCE.md, trước khi sinh:
    python .claude/skills/review/check_prompt.py <thư mục shot> [<review.json của previz>]
Đọc hằng số mốc ở đầu build_shot.py (không cần Blender). review.json do extract_shot.py tạo, có điểm cắt đo được.
In từng lỗi theo mức Chặn / Nên sửa / Gợi ý của skill /review.
"""
import ast
import json
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True  # không để __pycache__ cạnh timing.py của cảnh
shot = pathlib.Path(sys.argv[1]).resolve()
review = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")) if len(sys.argv) > 2 else None
root = next(p for p in [shot, *shot.parents] if (p / "CLAUDE.md").exists())
found = []


def say(level, msg):
    found.append(level)
    print(f"[{level}] {msg}")


def near(a, b, tol=0.05):
    return abs(a - b) <= tol


# ---- build_shot.py: FPS, SECONDS, SHOTS và các hằng số mốc (số hoặc cặp số) ở cấp module
src = (shot / "build_shot.py").read_text(encoding="utf-8")
consts = {}
for node in ast.parse(src).body:
    if not (isinstance(node, ast.Assign) and len(node.targets) == 1):
        continue
    tgt, val = node.targets[0], node.value
    if isinstance(tgt, ast.Name):
        pairs = [(tgt, val)]
    elif isinstance(tgt, ast.Tuple) and isinstance(val, ast.Tuple):  # chỉ lấy FPS, SECONDS từ dạng `FPS, SECONDS = 24, 27`
        pairs = [(t, v) for t, v in zip(tgt.elts, val.elts) if isinstance(t, ast.Name) and t.id in ("FPS", "SECONDS")]
    else:
        continue
    for t, v in pairs:
        try:
            consts[t.id] = ast.literal_eval(v)
        except ValueError:
            pass
# shot thuộc một cảnh có previz 2D: mốc nằm trong timing.py của cảnh (TIMING, tính từ gốc repo), trừ OFFSET
if isinstance(consts.get("TIMING"), str):
    import importlib.util
    spec = importlib.util.spec_from_file_location("timing", root / consts["TIMING"])
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    off, end = float(consts.get("OFFSET", 0.0)), float(consts.get("SECONDS", 1e9))
    for name, v in vars(tm).items():
        vals = v if isinstance(v, tuple) else (v,)
        if name.isupper() and name not in consts and name not in ("FPS", "SECONDS", "FRAMES", "SHOTS", "CC") \
                and vals and all(isinstance(x, (int, float)) for x in vals) \
                and all(-0.01 <= float(x) - off <= end + 0.01 for x in vals):  # chỉ mốc nằm trong đoạn này
            consts[name] = tuple(float(x) - off for x in vals) if isinstance(v, tuple) else float(v) - off
fps, seconds, shots = consts.get("FPS", 24), consts.get("SECONDS"), consts.get("SHOTS", [])
cuts_code = [s[1] for s in shots[1:]]
marks = {}
for name, v in consts.items():
    vals = v if isinstance(v, tuple) else (v,)
    if name not in ("FPS", "SECONDS", "FRAMES", "OFFSET") and vals and all(isinstance(x, float) for x in vals):
        for x in vals:
            marks.setdefault(round(x, 2), name)
allowed = set(marks) | {round(s[1], 2) for s in shots} | {round(s[2], 2) for s in shots} | {0.0}
in_code = {round(n.value, 2) for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Constant) and isinstance(n.value, float)}

# ---- prompt.md: khối ```text đầu tiên là prompt gửi đi
md_path = shot / "seedance" / "prompt.md"
md = md_path.read_text(encoding="utf-8")
m = re.search(r"```text\n(.*?)\n```", md, re.S)
if not m:
    sys.exit(f"Không thấy khối ```text trong {md_path}")
prompt = m.group(1)
heads = ["ACTIVE REFERENCES", "STYLE", "CHARACTERS", "CAMERA", "RULES", "TIMELINE", "AUDIO", "HOLD"]
sec, cur = {h: "" for h in ["TITLE"] + heads}, "TITLE"
for line in prompt.splitlines():
    if line.strip() in heads:
        cur = line.strip()
    else:
        sec[cur] += line + "\n"
for h in heads:
    if not sec[h].strip():
        say("Nên sửa", f"Prompt thiếu khối {h} (SEEDANCE.md, mục Prompt theo giây)")

# ---- thời lượng, số khung
if seconds:
    t = re.search(r"\((\d+(?:\.\d+)?)s", sec["TITLE"])
    if t and not near(float(t.group(1)), seconds):
        say("Chặn", f"Tiêu đề ghi {t.group(1)}s, build_shot.py SECONDS = {seconds}")
    f = re.search(r"(\d+) frames", sec["ACTIVE REFERENCES"])
    if f and int(f.group(1)) != fps * seconds:
        say("Chặn", f"ACTIVE REFERENCES ghi {f.group(1)} frames, build_shot.py là {fps * seconds}")
if review and seconds and not near(review["duration_s"], seconds, 0.1):
    say("Chặn", f"Video previz dài {review['duration_s']}s, build_shot.py SECONDS = {seconds}: render lại previz")

# ---- điểm cắt: CAMERA so với SHOTS và với điểm cắt đo được
cam = re.search(r"cuts? (?:exactly )?at ((?:[^.;\n]|\.(?=\d))*)", sec["CAMERA"])  # dấu chấm chỉ đi tiếp khi là số thập phân
cuts_prompt = [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*s\b", cam.group(1))] if cam else []
if cuts_code and not cuts_prompt:
    say("Chặn", f"CAMERA không ghi điểm cắt; SHOTS có cắt ở {cuts_code}")
elif cuts_prompt and [round(x, 2) for x in cuts_prompt] != [round(x, 2) for x in cuts_code]:
    say("Chặn", f"CAMERA cắt ở {cuts_prompt}, SHOTS trong build_shot.py cắt ở {cuts_code}")
if review:
    measured = [c["time_s"] for c in review["cuts"]]
    if [round(x, 1) for x in measured] != [round(x, 1) for x in cuts_code]:
        say("Chặn", f"Video previz đo được điểm cắt {measured}, SHOTS là {cuts_code}: video cũ hoặc build lệch")

# ---- khối TIMELINE: liền nhau từ 0 tới hết, không vắt qua điểm cắt
blocks = [(float(a), float(b)) for a, b in
          re.findall(r"^(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)s\s*—", sec["TIMELINE"], re.M)]
if blocks:
    if not near(blocks[0][0], 0):
        say("Chặn", f"TIMELINE bắt đầu ở {blocks[0][0]}s, không phải 0s")
    for (a1, b1), (a2, b2) in zip(blocks, blocks[1:]):
        if not near(b1, a2):
            say("Chặn", f"TIMELINE hở hoặc chồng: khối {a1}–{b1}s rồi {a2}–{b2}s")
    if seconds and not near(blocks[-1][1], seconds):
        say("Chặn", f"TIMELINE kết thúc ở {blocks[-1][1]}s, previz dài {seconds}s")
    for a, b in blocks:
        inside = [c for c in cuts_code if a + 0.05 < c < b - 0.05]
        if inside:
            say("Nên sửa", f"Khối TIMELINE {a}–{b}s vắt qua điểm cắt {inside}: tách khối ở chỗ cắt")
        if b - a > 5.0 + 1e-6:
            say("Gợi ý", f"Khối TIMELINE {a}–{b}s dài {b - a:.1f}s, quy tắc là 2–5 giây một khối")
else:
    say("Chặn", "Không đọc được khối nào trong TIMELINE (dạng `0–3.5s — ...`)")

# ---- mốc giây trong TIMELINE, AUDIO, HOLD phải là hằng số của build_shot.py
text = sec["TIMELINE"] + sec["AUDIO"] + sec["HOLD"]
times = set()
for a, b in re.findall(r"(\d+(?:\.\d+)?)\s*[–-]\s*(\d+(?:\.\d+)?)\s*s\b", text):
    times |= {round(float(a), 2), round(float(b), 2)}
times |= {round(float(x), 2) for x in re.findall(r"(\d+(?:\.\d+)?)\s*s\b", text)}
for t in sorted(times - allowed):
    if seconds and t > seconds:
        continue
    if t in in_code:
        say("Gợi ý", f"Mốc {t:g}s có trong code nhưng không phải hằng số đầu build_shot.py: đưa lên hằng số")
    else:
        say("Nên sửa", f"Mốc {t:g}s trong prompt không có trong build_shot.py (prompt lấy số từ hằng số, không đo bằng mắt)")
unused = sorted({n for t, n in marks.items() if t not in times})
if unused:
    say("Gợi ý", f"Hằng số mốc chưa có trong prompt: {', '.join(unused)}")

# ---- @Video, @Image: định nghĩa, dùng, file tải lên, file nguồn
defined = {(k, int(n)) for k, n in re.findall(r"^@(Video|Image) (\d+) =", sec["ACTIVE REFERENCES"], re.M)}
used = {(k, int(n)) for k, n in re.findall(r"@(Video|Image) (\d+)(?![–-]\d)", prompt)}
for k, a, b in re.findall(r"@(Video|Image) (\d+)[–-](\d+)", prompt):
    used |= {(k, i) for i in range(int(a), int(b) + 1)}
for k in ("Video", "Image"):
    nums = sorted(n for kk, n in defined if kk == k)
    if nums and nums != list(range(1, len(nums) + 1)):
        say("Chặn", f"Số @{k} không liền từ 1: {nums}")
for k, n in sorted(used - defined):
    say("Chặn", f"@{k} {n} được nhắc trong prompt nhưng chưa khai trong ACTIVE REFERENCES")
upload = shot / "renders" / "seedance_upload"
if upload.is_dir():
    files = {(("Video" if p.name.startswith("video") else "Image"), int(mm.group(1))): p.name
             for p in upload.iterdir() if (mm := re.match(r"(?:video|image)(\d+)_", p.name))}
    for k, n in sorted(defined - files.keys()):
        say("Chặn", f"@{k} {n} chưa có file trong renders/seedance_upload/")
    for (k, n), name in sorted(files.items()):
        if (k, n) not in defined:
            say("Nên sửa", f"renders/seedance_upload/{name} không ứng với @{k} nào trong prompt")
    ptxt = upload / "prompt.txt"
    if ptxt.exists() and ptxt.read_text(encoding="utf-8").strip() != prompt.strip():
        say("Chặn", "renders/seedance_upload/prompt.txt khác khối prompt trong prompt.md: chép lại trước khi sinh")
else:
    say("Nên sửa", "Chưa có renders/seedance_upload/ (gom file tải lên theo số tham chiếu)")
for k, n, up, src_path in re.findall(r"\|\s*`@(Video|Image) (\d+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`", md):
    if not ((shot / src_path).exists() or (root / src_path).exists()):
        say("Nên sửa", f"Nguồn của @{k} {n} không tồn tại: {src_path}")

# ---- mỗi nhân vật một tên
for alias in sorted(set(re.findall(r"\bthe (fox|reptile|lizard|spirit|slime|blob|jelly|hero|creature)\b",
                                   sec["TIMELINE"] + sec["HOLD"], re.I))):
    say("Nên sửa", f'TIMELINE gọi "the {alias}": mỗi nhân vật luôn gọi đúng một tên')

n = {lv: found.count(lv) for lv in ("Chặn", "Nên sửa", "Gợi ý")}
print(f"PROMPT_CHECKED {md_path.relative_to(root)}: {n['Chặn']} Chặn, {n['Nên sửa']} Nên sửa, {n['Gợi ý']} Gợi ý")
