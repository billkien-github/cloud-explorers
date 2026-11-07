"""Ghép nhiều ảnh thành một tấm làm ảnh tham chiếu Seedance, để mỗi tấm chỉ chiếm một suất @Image:
- Ảnh xoay (turnaround) của một nhân vật: ảnh trước bên trái, ảnh sau bên phải, cùng chiều cao nhân vật, chân cùng một
  đường.
- Tấm gộp nhiều món (đạo cụ, nhân vật nền…) khi đoạn cần quá 30 ảnh tham chiếu (giới hạn của Seedance 2.5): thêm --hop, mỗi món co cho vừa một ô
  vuông (cạnh dài nhất bằng nhau) thay vì cùng chiều cao, nên vật dài, vật dẹt không bị phóng quá to.
- Ảnh xếp hàng đúng cỡ (cast_lineup.png: bốn nhân vật chính cùng đường chân, cao đúng tỉ lệ Character Bible): thêm
  --cao 1,0.85,0.7,0.8 (một số cho mỗi ảnh, theo thứ tự); mọi món một hàng, món cao nhất cao CAO_NV px.
Nền xám trơn, không chữ. Nhiều món thì tự xếp nhiều hàng sao cho tỉ lệ rộng/cao của tấm gần 16:9 nhất trong giới hạn
0.4–2.5 của API; cạnh dài quá 6000 px thì co lại. Quy tắc dùng: `04_PRODUCTION/SEEDANCE.md`, mục "Ảnh tham chiếu".

Chạy (macOS; Windows thay đường dẫn Blender):
    /Applications/Blender.app/Contents/MacOS/Blender -b --python-exit-code 1 -P pipeline/turnaround.py -- \
        <ảnh ra> <ảnh 1> <ảnh 2> [<ảnh 3> …] [--hop | --cao h1,h2,…]
Ảnh xoay: <ảnh 1> là ảnh trước, <ảnh 2> là ảnh sau. Tấm gộp: thứ tự ảnh là thứ tự trái sang phải, trên xuống dưới.

Cách làm:
- Nền mỗi ảnh lấy theo trung vị viền ngoài; cả ảnh được dời màu cho nền về cùng một màu xám, nên các ô không lệch nền.
- Vật là vùng khác nền rõ (> NGUONG); co giãn để vật cao CAO_NV px (--hop: cạnh dài nhất CAO_NV px), cắt sát vật kèm lề,
  dán lên nền chung với mép cắt làm mờ dần để không lộ đường nối.
"""
import math
import sys

import bpy
import numpy as np

CAO_NV = 1300        # chiều cao nhân vật trong ảnh ra (px); --hop: cạnh dài nhất của mỗi món
LE_DOC = 0.07        # lề trên, dưới, tính theo CAO_NV
LE_NGANG = 0.07      # lề trái, phải và nửa khoảng hở giữa hai ô
NGUONG = 0.12        # khác nền bao nhiêu thì tính là vật (thang 0..1)
CANH_MAX = 6000      # cạnh dài nhất API nhận (px)


def doc_anh(path, w=None, h=None):
    """Đọc ảnh thành mảng (cao, rộng, 4) theo thứ tự hàng từ trên xuống; có w, h thì co giãn trước."""
    img = bpy.data.images.load(path, check_existing=False)
    if w:
        img.scale(w, h)
    W, H = img.size
    px = np.array(img.pixels[:], dtype=np.float32).reshape(H, W, 4)[::-1].copy()
    bpy.data.images.remove(img)
    return px


def mau_nen(px):
    """Trung vị các dải viền 2% quanh ảnh."""
    H, W = px.shape[:2]
    b = max(2, int(min(H, W) * 0.02))
    vien = np.concatenate([px[:b].reshape(-1, 4), px[-b:].reshape(-1, 4),
                           px[:, :b].reshape(-1, 4), px[:, -b:].reshape(-1, 4)])
    return np.median(vien[:, :3], axis=0)


def khung_nv(px, nen):
    """Khung bao vật (trên, dưới, trái, phải), dưới và phải là chỉ số cuối + 1."""
    mask = np.abs(px[..., :3] - nen).max(axis=2) > NGUONG
    hang = np.where(mask.any(axis=1))[0]
    cot = np.where(mask.any(axis=0))[0]
    if not len(hang):
        sys.exit("Không tìm thấy vật trong ảnh")
    return hang[0], hang[-1] + 1, cot[0], cot[-1] + 1


def chuan_bi(path, nen_chung, hop, he_so=1.0):
    """Co giãn ảnh cho vật cao CAO_NV × he_so (hop: cạnh dài nhất CAO_NV), dời nền về nen_chung, trả về (ảnh, khung vật)."""
    px = doc_anh(path)
    nen = mau_nen(px)
    tr, du, tra, ph = khung_nv(px, nen)
    s = CAO_NV * he_so / (max(du - tr, ph - tra) if hop else du - tr)
    H, W = px.shape[:2]
    px = doc_anh(path, max(1, round(W * s)), max(1, round(H * s)))
    px[..., :3] += nen_chung - nen
    np.clip(px, 0.0, 1.0, out=px)
    return px, khung_nv(px, nen_chung)


def xep_hang(rong, le_n, hang_cao):
    """Chia các ô thành hàng (đều nhau, theo thứ tự) sao cho tỉ lệ rộng/cao của tấm gần 16:9 nhất trong 0.4–2.5."""
    n, cach = len(rong), []
    for so_hang in range(1, n + 1):
        moi = math.ceil(n / so_hang)
        hang = [list(range(i, min(i + moi, n))) for i in range(0, n, moi)]
        W = max(sum(rong[j] + 2 * le_n for j in h) for h in hang)
        cach.append((hang, W, len(hang) * hang_cao))
    hop_le = [c for c in cach if 0.4 <= c[1] / c[2] <= 2.5] or cach
    return min(hop_le, key=lambda c: abs(math.log(c[1] / c[2] / (16 / 9))))


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    hop = "--hop" in args
    args = [a for a in args if a != "--hop"]
    cao = None
    if "--cao" in args:
        i = args.index("--cao")
        cao = [float(x) for x in args[i + 1].split(",")]
        args = args[:i] + args[i + 2:]
    if len(args) < 3:
        sys.exit("Cần: <ảnh ra> <ảnh 1> <ảnh 2> [<ảnh 3> …] [--hop]")
    ra, nguon = args[0], args[1:]

    nen_chung = np.mean([mau_nen(doc_anh(p)) for p in nguon], axis=0)
    if cao and len(cao) != len(nguon):
        sys.exit("--cao cần đúng một số cho mỗi ảnh")
    he_so = [h / max(cao) for h in cao] if cao else [1.0] * len(nguon)
    manh = [chuan_bi(p, nen_chung, hop, k) for p, k in zip(nguon, he_so)]

    le_d = round(CAO_NV * LE_DOC)
    le_n = round(CAO_NV * LE_NGANG)
    rong = [k[3] - k[2] for _, k in manh]
    hang_cao = CAO_NV + 2 * le_d
    if cao:                                                              # xếp hàng đúng cỡ: luôn một hàng
        hang = [list(range(len(manh)))]
        W, H = sum(r + 2 * le_n for r in rong), hang_cao
    else:
        hang, W, H = xep_hang(rong, le_n, hang_cao)
    nen_anh = np.empty((H, W, 4), dtype=np.float32)
    nen_anh[..., :3] = nen_chung
    nen_anh[..., 3] = 1.0

    for i, h in enumerate(hang):
        day = (i + 1) * hang_cao - le_d                                  # đường chân của hàng
        x = (W - sum(rong[j] + 2 * le_n for j in h)) // 2 + le_n         # hàng ngắn hơn tấm thì canh giữa
        for j in h:
            px, (tr, du, tra, ph) = manh[j]
            # vùng cắt: khung vật + lề, giới hạn trong ảnh nguồn
            c0, c1 = max(0, tr - le_d), min(px.shape[0], du + le_d)
            l0, l1 = max(0, tra - le_n), min(px.shape[1], ph + le_n)
            m = px[c0:c1, l0:l1]
            # vị trí trên nền chung: chân vật ở đường chân của hàng, mép trái vật ở x
            y0 = day - (du - c0)
            x0 = x - (tra - l0)
            # trọng số mờ dần ở mép mảnh cắt (trong phần lề, không chạm vật)
            mh, mw = m.shape[:2]
            mo = max(1, int(min(le_d, le_n) * 0.8))
            wy = np.clip(np.minimum(np.arange(mh), np.arange(mh)[::-1]) / mo, 0, 1)
            wx = np.clip(np.minimum(np.arange(mw), np.arange(mw)[::-1]) / mo, 0, 1)
            a = (wy[:, None] * wx[None, :])[..., None]
            # cắt phần rơi ra ngoài nền chung
            ys, xs = max(0, -y0), max(0, -x0)
            ye, xe = min(mh, H - y0), min(mw, W - x0)
            vung = nen_anh[y0 + ys:y0 + ye, x0 + xs:x0 + xe]
            vung[:] = vung * (1 - a[ys:ye, xs:xe]) + m[ys:ye, xs:xe] * a[ys:ye, xs:xe]
            x += rong[j] + 2 * le_n

    nen_anh[..., 3] = 1.0
    out = bpy.data.images.new("sheet", W, H, alpha=False)
    out.pixels = nen_anh[::-1].ravel()
    if max(W, H) > CANH_MAX:
        k = CANH_MAX / max(W, H)
        W, H = round(W * k), round(H * k)
        out.scale(W, H)
    out.filepath_raw = ra
    out.file_format = "PNG"
    out.save()
    print(f"{ra}: {W}x{H}, {len(hang)} hàng")


main()
