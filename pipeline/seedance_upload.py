"""
Tạo thư mục tải lên Seedance của một shot, renders/seedance_upload/, theo bảng số tham chiếu trong seedance/prompt.md:
    python pipeline/seedance_upload.py <thư mục shot>

- Bảng trong prompt.md có dạng | `@Image1` | `image1_lumo.png` | `<nguồn>` |: cột 2 là tên file tải lên, cột 3 là
  nguồn, tính từ thư mục shot nếu có, không thì từ gốc dự án (video previz: `renders/sh010_ref.mp4`, render bằng run ref).
- Xoá file cũ trong thư mục, chép từng nguồn thành tên file tải lên, ghi khối ```text của prompt ra prompt.txt.
- Thiếu nguồn thì báo từng file và thoát mã 1; các file còn lại vẫn được chép.
Sửa prompt hay đổi ảnh trong bảng thì chạy lại. Dùng khi sinh bằng tay trên console; sinh qua API thì dùng
pipeline/seedance_gen.py (đọc prompt.md bằng hàm load() ở đây). Quy trình: 04_PRODUCTION/SEEDANCE.md.
"""
import pathlib
import re
import shutil
import sys

# cùng mẫu với .claude/skills/review/check_prompt.py, để các script đọc bảng và khối prompt như nhau
ROW = re.compile(r"\|\s*`@(Video|Image) ?(\d+)`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`")
PROMPT = re.compile(r"```text\n(.*?)\n```", re.S)


def load(shot):
    """Đọc seedance/prompt.md của shot. Trả (gốc dự án, prompt, refs); refs theo thứ tự bảng, mỗi phần tử là
    (loại "Video"/"Image", số, tên file tải lên, nguồn ghi trong bảng, đường dẫn tìm được hoặc None)."""
    shot = pathlib.Path(shot).resolve()
    root = next(p for p in [shot, *shot.parents] if (p / "CLAUDE.md").exists())
    f = shot / "seedance" / "prompt.md"
    if not f.is_file():
        sys.exit(f"Không có {f}")
    md = f.read_text(encoding="utf-8")
    rows, prompt = ROW.findall(md), PROMPT.search(md)
    if not rows or not prompt:
        sys.exit("prompt.md thiếu bảng số tham chiếu hoặc khối ```text của prompt")
    refs = [(kind, int(n), name, src, next((p for p in (shot / src, root / src) if p.is_file()), None))
            for kind, n, name, src in rows]
    return root, prompt.group(1).strip(), refs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    shot = pathlib.Path(sys.argv[1]).resolve()
    root, prompt, refs = load(shot)
    out = shot / "renders" / "seedance_upload"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.iterdir():
        if old.is_file():
            old.unlink()

    missing = 0
    for kind, n, name, src, path in refs:
        if path is None:
            print(f"Thiếu nguồn của @{kind}{n}: {src}")
            missing += 1
            continue
        shutil.copy2(path, out / name)
        print(f"@{kind}{n}  {name}  <-  {src}")
    (out / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    print(f"{out.relative_to(root)}: {len(refs) - missing}/{len(refs)} file + prompt.txt")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
