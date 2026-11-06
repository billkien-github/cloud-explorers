"""
Tạo thư mục tải lên Seedance của một shot, renders/seedance_upload/, theo bảng số tham chiếu trong seedance/prompt.md:
    python pipeline/seedance_upload.py <thư mục shot>

- Bảng trong prompt.md có dạng | `@Image1` | `image1_lumo.png` | `<nguồn>` |: cột 2 là tên file tải lên, cột 3 là
  nguồn, tính từ thư mục shot nếu có, không thì từ gốc dự án (video previz: `renders/sh010_ref.mp4`, render bằng run ref).
- Xoá file cũ trong thư mục, chép từng nguồn thành tên file tải lên, ghi khối ```text của prompt ra prompt.txt.
- Thiếu nguồn thì báo từng file và thoát mã 1; các file còn lại vẫn được chép.
Sửa prompt hay đổi ảnh trong bảng thì chạy lại. Quy trình: 04_PRODUCTION/SEEDANCE.md.
"""
import pathlib
import re
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
shot = pathlib.Path(sys.argv[1]).resolve()
root = next(p for p in [shot, *shot.parents] if (p / "CLAUDE.md").exists())
md = (shot / "seedance" / "prompt.md").read_text(encoding="utf-8")
# cùng mẫu với .claude/skills/review/check_prompt.py, để hai script đọc bảng và khối prompt như nhau
rows = re.findall(r"\|\s*`@(Video|Image) ?(\d+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`", md)
prompt = re.search(r"```text\n(.*?)\n```", md, re.S)
if not rows or not prompt:
    sys.exit("prompt.md thiếu bảng số tham chiếu hoặc khối ```text của prompt")

out = shot / "renders" / "seedance_upload"
out.mkdir(parents=True, exist_ok=True)
for old in out.iterdir():
    if old.is_file():
        old.unlink()

missing = 0
for kind, n, name, src in rows:
    path = next((p for p in (shot / src, root / src) if p.is_file()), None)
    if path is None:
        print(f"Thiếu nguồn của @{kind}{n}: {src}")
        missing += 1
        continue
    shutil.copy2(path, out / name)
    print(f"@{kind}{n}  {name}  <-  {src}")
(out / "prompt.txt").write_text(prompt.group(1).strip() + "\n", encoding="utf-8")
print(f"{out.relative_to(root)}: {len(rows) - missing}/{len(rows)} file + prompt.txt")
sys.exit(1 if missing else 0)
