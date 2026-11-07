"""
Đề xuất cách chia một cảnh thành các đoạn để sinh Seedance, mỗi đoạn một lần gọi API (quy tắc: 04_PRODUCTION/SEEDANCE.md,
mục "Chia cảnh thành đoạn"):
    python pipeline/split_segments.py <timing.py của cảnh> [--max 30] [--tail 0.5] [--options 3]

- Chỉ chia ở điểm cắt máy giữa hai cú liền nhau trong SHOTS, không bao giờ chia giữa một cú.
- Mỗi đoạn: độ dài trong cảnh (SEGMENT) cộng phần đuôi (cú máy cuối giữ thêm, lúc dựng cắt bỏ) tối đa --max giây
  (15 cho dòng Seedance 2.0, 30 cho 2.5). SECONDS = SEGMENT + đuôi, làm tròn lên số nguyên, ít nhất 4.
- Chọn ít đoạn nhất; cùng số đoạn thì ưu tiên đoạn ngắn nhất dài nhất có thể (không có đoạn vụn), rồi đoạn dài nhất ngắn
  nhất có thể (đều nhau). In vài cách tốt nhất, mỗi chỗ nối kèm ghi chú của hai cú máy hai bên để chọn theo nhịp truyện.
- Cú máy nào một mình đã dài quá --max thì báo và thoát mã 1: thêm điểm cắt trong previz 2D.
- --check <thư mục tập>: soát các đoạn đã chia (mọi <thư mục tập>/sh*/build_shot.py có TIMING là timing.py này) theo
  luật 1–3: nối ở điểm cắt máy, phủ liền cả cảnh, SECONDS ≤ --max và đúng bằng SEGMENT + đuôi làm tròn lên, số đoạn
  bằng số ít nhất (nhiều hơn chỉ cảnh báo, vì luật 4 cho chọn theo nhịp truyện); báo thêm đoạn sát trần (kéo dài thêm
  dưới 1 s là chạm --max, phải chia lại). Thoát mã 1 nếu có lỗi. Chạy lại mỗi lần sửa timing.py của cảnh đã chia đoạn.
Chỉ dùng thư viện chuẩn, không cần Blender.
"""
import argparse
import ast
import math
import pathlib
import re
import sys


def read_shots(path):
    """SHOTS của timing.py: [(tên, giây đầu, giây cuối)] và ghi chú cuối dòng của từng cú."""
    src = path.read_text(encoding="utf-8")
    shots = None
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SHOTS" for t in node.targets):
            shots = ast.literal_eval(node.value)
    if not shots:
        sys.exit(f"{path}: không có SHOTS")
    notes = {m.group(1): m.group(2).strip()
             for m in re.finditer(r'\(\s*"([^"]+)"\s*,[^)\n]*\)\s*,?[ \t]*#[ \t]*([^\n]*)', src)}
    return [(n, float(a), float(b)) for n, a, b in shots], notes


def all_splits(points, limit, count):
    """Mọi cách chia points[0]..points[-1] thành đúng count đoạn, mỗi đoạn dài tối đa limit."""
    n = len(points) - 1
    fewest = [math.inf] * (n + 1)          # fewest[i]: số đoạn ít nhất từ điểm i tới cuối
    fewest[n] = 0
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            if points[j] - points[i] > limit + 1e-9:
                break
            fewest[i] = min(fewest[i], fewest[j] + 1)
    out = []

    def walk(i, left, path):
        if len(out) >= 20000:
            return
        if i == n:
            if left == 0:
                out.append(path)
            return
        if left < fewest[i]:
            return
        for j in range(i + 1, n + 1):
            if points[j] - points[i] > limit + 1e-9:
                break
            walk(j, left - 1, path + [j])

    walk(0, count, [0])
    return out, fewest[0]


def read_segments(episode_dir, timing):
    """Các đoạn đã chia: [(tên shot, OFFSET, SEGMENT hay None, SECONDS)] của build_shot.py có TIMING là timing."""
    root = pathlib.Path(__file__).resolve().parent.parent
    out = []
    for f in sorted(pathlib.Path(episode_dir).glob("*/build_shot.py")):
        src = f.read_text(encoding="utf-8")
        m = re.search(r'^TIMING\s*=\s*"([^"]+)"', src, re.M)
        if not m or (root / m.group(1)).resolve() != timing:
            continue
        num = lambda k: re.search(rf"^{k}\s*=\s*([\d.]+)", src, re.M)  # noqa: E731
        secs = re.search(r"^FPS,\s*SECONDS\s*=\s*\d+,\s*([\d.]+)", src, re.M) or num("SECONDS")
        off, seg = num("OFFSET"), num("SEGMENT")
        out.append((f.parent.name, float(off.group(1)) if off else 0.0, float(seg.group(1)) if seg else None,
                    float(secs.group(1)) if secs else None))
    return sorted(out, key=lambda d: d[1])


def check(segments, shots, fewest, a):
    """In từng đoạn kèm lỗi theo luật 1–3; trả về số lỗi."""
    total = shots[-1][2]
    cut_points = {round(s, 3) for _, s, _ in shots}
    errors, prev_end = 0, shots[0][1]
    for name, off, seg, secs in segments:
        seg = total - off if seg is None else seg
        end = off + seg
        inside = [n for n, s, _ in shots if off - 1e-3 <= s < end - 1e-3]
        notes = []
        if secs is None:
            notes.append("[Lỗi] không đọc được SECONDS")
        else:
            expected = max(4, math.ceil(seg + a.tail - 1e-9))
            if secs > a.max:
                notes.append(f"[Lỗi] sinh {secs:g} s > {a.max} s")
            if secs - seg < a.tail - 1e-6:
                notes.append(f"[Lỗi] đuôi {secs - seg:.2f} s < {a.tail:g} s")
            if secs != expected:
                notes.append(f"[Lỗi] SECONDS nên là {expected}")
            room = a.max - a.tail - seg
            if room < 1.0 - 1e-6:
                notes.append(f"[Sát trần] chỉ kéo dài thêm được {room:.1f} s, hơn nữa là phải chia lại")
        if abs(off - prev_end) > 1e-3:
            notes.append(f"[Lỗi] không nối liền đoạn trước (đoạn trước hết ở {prev_end:g} s)")
        if off > shots[0][1] + 1e-3 and round(off, 3) not in cut_points:
            notes.append("[Lỗi] nối giữa một cú, không ở điểm cắt máy")
        errors += sum(n.startswith("[Lỗi]") for n in notes)
        span = f"{inside[0]}–{inside[-1]}" if inside else "?"
        print(f"  {name:<6} {span:<9} {off:6.2f}–{end:6.2f}  SEGMENT = {seg:.2f}  SECONDS = {secs:g}  "
              f"{'; '.join(notes) if notes else 'OK'}")
        prev_end = end
    if abs(prev_end - total) > 1e-3:
        print(f"[Lỗi] các đoạn hết ở {prev_end:g} s, cảnh dài {total:g} s")
        errors += 1
    if len(segments) > fewest:
        print(f"[Nhiều đoạn hơn cần] {len(segments)} đoạn, ít nhất chỉ cần {fewest}: chia lại (luật 3), trừ khi docstring "
              "đã ghi lý do nhịp truyện (luật 4)")
    return errors


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Đề xuất cách chia cảnh thành các đoạn sinh Seedance")
    ap.add_argument("timing")
    ap.add_argument("--max", type=int, default=30, help="giây tối đa mỗi lần sinh (Seedance 2.5: 30)")
    ap.add_argument("--tail", type=float, default=0.5, help="giây giữ thêm cú máy cuối mỗi đoạn, lúc dựng cắt bỏ")
    ap.add_argument("--options", type=int, default=3, help="số cách chia tốt nhất in ra")
    ap.add_argument("--check", metavar="EPISODE_DIR", help="soát các đoạn đã chia trong thư mục tập")
    a = ap.parse_args()

    path = pathlib.Path(a.timing).resolve()
    shots, notes = read_shots(path)
    for (n1, _, b1), (n2, a2, _) in zip(shots, shots[1:]):
        if abs(b1 - a2) > 1e-6:
            sys.exit(f"SHOTS hở hay chồng giữa {n1} và {n2} ({b1} ≠ {a2})")
    limit = a.max - a.tail
    too_long = [(n, b - s) for n, s, b in shots if b - s > limit + 1e-9]
    total = shots[-1][2] - shots[0][1]
    print(f"{path.name} ({path.parent.name}): {total:g} s, {len(shots)} cú máy; mỗi đoạn tối đa {a.max} s "
          f"(gồm đuôi {a.tail:g} s, nên tối đa {limit:g} s trong cảnh)")
    if too_long:
        for n, d in too_long:
            print(f"[Lỗi] {n} dài {d:g} s, một mình đã quá {limit:g} s: thêm điểm cắt máy trong previz 2D (timing.py), "
                  f"hay dùng Seedance 2.5 cho cảnh này (đắt hơn, hỏi người dùng trước)")
        sys.exit(1)

    points = [shots[0][1]] + [b for _, _, b in shots]
    _, fewest = all_splits(points, limit, 0)
    if a.check:
        segments = read_segments(a.check, path)
        if not segments:
            sys.exit(f"Không có build_shot.py nào trong {a.check} dùng {path}")
        print(f"Ít nhất {fewest} đoạn; đã chia {len(segments)} đoạn:")
        sys.exit(1 if check(segments, shots, fewest, a) else 0)
    splits, _ = all_splits(points, limit, fewest)
    lengths = lambda c: [points[j] - points[i] for i, j in zip(c, c[1:])]  # noqa: E731
    splits.sort(key=lambda c: (-min(lengths(c)), max(lengths(c)), c))
    print(f"Ít nhất {fewest} đoạn; có {len(splits)} cách. {min(a.options, len(splits))} cách tốt nhất "
          "(đoạn ngắn nhất dài nhất, rồi đều nhau):")
    clip = lambda s: (s[:70] + "…") if len(s) > 71 else s  # noqa: E731
    for k, c in enumerate(splits[:a.options], 1):
        print(f"\nCách {k}")
        for d, (i, j) in enumerate(zip(c, c[1:]), 1):
            seg = points[j] - points[i]
            name = shots[i][0] if j - i == 1 else f"{shots[i][0]}–{shots[j - 1][0]}"
            print(f"  đoạn {d}  {name:<9} {points[i]:6.2f}–{points[j]:6.2f}  OFFSET = {points[i]:g}  SEGMENT = {seg:.2f}  "
                  f"SECONDS = {max(4, math.ceil(seg + a.tail - 1e-9))}")
        for i in c[1:-1]:
            print(f"  nối ở {points[i]:g} s: {shots[i - 1][0]} «{clip(notes.get(shots[i - 1][0], ''))}»"
                  f"  |  {shots[i][0]} «{clip(notes.get(shots[i][0], ''))}»")


if __name__ == "__main__":
    main()
