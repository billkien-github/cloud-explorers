"""
Đề xuất cách chia một cảnh thành các đoạn để sinh Seedance, mỗi đoạn một lần gọi API (quy tắc: 04_PRODUCTION/SEEDANCE.md,
mục "Chia cảnh thành đoạn"):
    python pipeline/chia_doan.py <timing.py của cảnh> [--max 30] [--duoi 0.5] [--so-cach 3]

- Chỉ chia ở điểm cắt máy giữa hai cú liền nhau trong SHOTS, không bao giờ chia giữa một cú.
- Mỗi đoạn: độ dài trong cảnh (SEGMENT) cộng phần đuôi (cú máy cuối giữ thêm, lúc dựng cắt bỏ) tối đa --max giây
  (15 cho dòng Seedance 2.0, 30 cho 2.5). SECONDS = SEGMENT + đuôi, làm tròn lên số nguyên, ít nhất 4.
- Chọn ít đoạn nhất; cùng số đoạn thì ưu tiên đoạn ngắn nhất dài nhất có thể (không có đoạn vụn), rồi đoạn dài nhất ngắn
  nhất có thể (đều nhau). In vài cách tốt nhất, mỗi chỗ nối kèm ghi chú của hai cú máy hai bên để chọn theo nhịp truyện.
- Cú máy nào một mình đã dài quá --max thì báo và thoát mã 1: thêm điểm cắt trong previz 2D.
Chỉ dùng thư viện chuẩn, không cần Blender.
"""
import argparse
import ast
import math
import pathlib
import re
import sys


def doc_shots(path):
    """SHOTS của timing.py: [(tên, giây đầu, giây cuối)] và ghi chú cuối dòng của từng cú."""
    src = path.read_text(encoding="utf-8")
    shots = None
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "SHOTS" for t in node.targets):
            shots = ast.literal_eval(node.value)
    if not shots:
        sys.exit(f"{path}: không có SHOTS")
    ghi_chu = {m.group(1): m.group(2).strip()
               for m in re.finditer(r'\(\s*"([^"]+)"\s*,[^)\n]*\)\s*,?[ \t]*#[ \t]*([^\n]*)', src)}
    return [(n, float(a), float(b)) for n, a, b in shots], ghi_chu


def cac_cach(diem, gioi_han, so_doan):
    """Mọi cách chia diem[0]..diem[-1] thành đúng so_doan đoạn, mỗi đoạn dài tối đa gioi_han."""
    n = len(diem) - 1
    it_nhat = [math.inf] * (n + 1)          # it_nhat[i]: số đoạn ít nhất từ điểm i tới cuối
    it_nhat[n] = 0
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            if diem[j] - diem[i] > gioi_han + 1e-9:
                break
            it_nhat[i] = min(it_nhat[i], it_nhat[j] + 1)
    out = []

    def di(i, con, duong):
        if len(out) >= 20000:
            return
        if i == n:
            if con == 0:
                out.append(duong)
            return
        if con < it_nhat[i]:
            return
        for j in range(i + 1, n + 1):
            if diem[j] - diem[i] > gioi_han + 1e-9:
                break
            di(j, con - 1, duong + [j])

    di(0, so_doan, [0])
    return out, it_nhat[0]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Đề xuất cách chia cảnh thành các đoạn sinh Seedance")
    ap.add_argument("timing")
    ap.add_argument("--max", type=int, default=30, help="giây tối đa mỗi lần sinh (Seedance 2.5: 30)")
    ap.add_argument("--duoi", type=float, default=0.5, help="giây giữ thêm cú máy cuối mỗi đoạn, lúc dựng cắt bỏ")
    ap.add_argument("--so-cach", type=int, default=3)
    a = ap.parse_args()

    path = pathlib.Path(a.timing).resolve()
    shots, ghi_chu = doc_shots(path)
    for (n1, _, b1), (n2, a2, _) in zip(shots, shots[1:]):
        if abs(b1 - a2) > 1e-6:
            sys.exit(f"SHOTS hở hay chồng giữa {n1} và {n2} ({b1} ≠ {a2})")
    gioi_han = a.max - a.duoi
    dai = [(n, b - s) for n, s, b in shots if b - s > gioi_han + 1e-9]
    tong = shots[-1][2] - shots[0][1]
    print(f"{path.name} ({path.parent.name}): {tong:g} s, {len(shots)} cú máy; mỗi đoạn tối đa {a.max} s "
          f"(gồm đuôi {a.duoi:g} s, nên tối đa {gioi_han:g} s trong cảnh)")
    if dai:
        for n, d in dai:
            print(f"[Lỗi] {n} dài {d:g} s, một mình đã quá {gioi_han:g} s: thêm điểm cắt máy trong previz 2D (timing.py), "
                  f"hay dùng Seedance 2.5 cho cảnh này (đắt hơn, hỏi người dùng trước)")
        sys.exit(1)

    diem = [shots[0][1]] + [b for _, _, b in shots]
    _, k = cac_cach(diem, gioi_han, 0)
    cach, _ = cac_cach(diem, gioi_han, k)
    do_dai = lambda c: [diem[j] - diem[i] for i, j in zip(c, c[1:])]  # noqa: E731
    cach.sort(key=lambda c: (-min(do_dai(c)), max(do_dai(c)), c))
    print(f"Ít nhất {k} đoạn; có {len(cach)} cách. {min(a.so_cach, len(cach))} cách tốt nhất "
          "(đoạn ngắn nhất dài nhất, rồi đều nhau):")
    goi = lambda s: (s[:70] + "…") if len(s) > 71 else s  # noqa: E731
    for so, c in enumerate(cach[:a.so_cach], 1):
        print(f"\nCách {so}")
        for d, (i, j) in enumerate(zip(c, c[1:]), 1):
            seg = diem[j] - diem[i]
            ten = shots[i][0] if j - i == 1 else f"{shots[i][0]}–{shots[j - 1][0]}"
            print(f"  đoạn {d}  {ten:<9} {diem[i]:6.2f}–{diem[j]:6.2f}  OFFSET = {diem[i]:g}  SEGMENT = {seg:.2f}  "
                  f"SECONDS = {max(4, math.ceil(seg + a.duoi - 1e-9))}")
        for i in c[1:-1]:
            print(f"  nối ở {diem[i]:g} s: {shots[i - 1][0]} «{goi(ghi_chu.get(shots[i - 1][0], ''))}»"
                  f"  |  {shots[i][0]} «{goi(ghi_chu.get(shots[i][0], ''))}»")


if __name__ == "__main__":
    main()
