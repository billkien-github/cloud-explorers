"""Ghép ảnh nhìn trước và ảnh nhìn sau của một nhân vật thành một ảnh xoay (turnaround) để làm ảnh tham chiếu Seedance.

Mỗi nhân vật chiếm một suất @Image mà vẫn có cả hai góc nhìn. Ảnh trước bên trái, ảnh sau bên phải, cùng chiều cao nhân vật,
chân cùng một đường, nền xám trơn, không chữ. Quy tắc dùng ảnh: `04_PRODUCTION/SEEDANCE.md`, mục "Ảnh tham chiếu".

Chạy (macOS; Windows thay đường dẫn Blender):
    /Applications/Blender.app/Contents/MacOS/Blender -b --python-exit-code 1 -P pipeline/turnaround.py -- \
        <ảnh ra> <ảnh trước> <ảnh sau>

Cách làm:
- Nền mỗi ảnh lấy theo trung vị viền ngoài; cả ảnh được dời màu cho nền về cùng một màu xám, nên hai nửa không lệch nền.
- Nhân vật là vùng khác nền rõ (> NGUONG); co giãn để nhân vật cao CAO_NV px, cắt sát nhân vật kèm lề, dán lên nền chung
  với mép cắt làm mờ dần để không lộ đường nối.
"""
import sys

import bpy
import numpy as np

CAO_NV = 1300        # chiều cao nhân vật trong ảnh ra (px)
LE_DOC = 0.07        # lề trên, dưới, tính theo chiều cao nhân vật
LE_NGANG = 0.07      # lề trái, phải và nửa khoảng hở giữa hai góc nhìn
NGUONG = 0.12        # khác nền bao nhiêu thì tính là nhân vật (thang 0..1)


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
    """Khung bao nhân vật (trên, dưới, trái, phải), dưới và phải là chỉ số cuối + 1."""
    mask = np.abs(px[..., :3] - nen).max(axis=2) > NGUONG
    hang = np.where(mask.any(axis=1))[0]
    cot = np.where(mask.any(axis=0))[0]
    if not len(hang):
        sys.exit("Không tìm thấy nhân vật trong ảnh")
    return hang[0], hang[-1] + 1, cot[0], cot[-1] + 1


def chuan_bi(path, nen_chung):
    """Co giãn ảnh cho nhân vật cao CAO_NV, dời nền về nen_chung, trả về (ảnh, khung nhân vật)."""
    px = doc_anh(path)
    nen = mau_nen(px)
    tr, du, _, _ = khung_nv(px, nen)
    s = CAO_NV / (du - tr)
    H, W = px.shape[:2]
    px = doc_anh(path, max(1, round(W * s)), max(1, round(H * s)))
    px[..., :3] += nen_chung - nen
    np.clip(px, 0.0, 1.0, out=px)
    return px, khung_nv(px, nen_chung)


def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) != 3:
        sys.exit("Cần 3 đối số: <ảnh ra> <ảnh trước> <ảnh sau>")
    ra, truoc, sau = args

    nen_chung = (mau_nen(doc_anh(truoc)) + mau_nen(doc_anh(sau))) / 2
    hai = [chuan_bi(truoc, nen_chung), chuan_bi(sau, nen_chung)]

    le_d = round(CAO_NV * LE_DOC)
    le_n = round(CAO_NV * LE_NGANG)
    rong = [k[3] - k[2] for _, k in hai]
    W = sum(rong) + 4 * le_n
    H = CAO_NV + 2 * le_d
    nen_anh = np.empty((H, W, 4), dtype=np.float32)
    nen_anh[..., :3] = nen_chung
    nen_anh[..., 3] = 1.0

    x = le_n
    for (px, (tr, du, tra, ph)), r in zip(hai, rong):
        # vùng cắt: khung nhân vật + lề, giới hạn trong ảnh nguồn
        c0, c1 = max(0, tr - le_d), min(px.shape[0], du + le_d)
        l0, l1 = max(0, tra - le_n), min(px.shape[1], ph + le_n)
        manh = px[c0:c1, l0:l1]
        # vị trí trên nền chung: chân nhân vật ở H - le_d, mép trái nhân vật ở x
        y0 = (H - le_d) - (du - c0)
        x0 = x - (tra - l0)
        # trọng số mờ dần ở mép mảnh cắt (trong phần lề, không chạm nhân vật)
        mh, mw = manh.shape[:2]
        mo = max(1, int(min(le_d, le_n) * 0.8))
        wy = np.clip(np.minimum(np.arange(mh), np.arange(mh)[::-1]) / mo, 0, 1)
        wx = np.clip(np.minimum(np.arange(mw), np.arange(mw)[::-1]) / mo, 0, 1)
        a = (wy[:, None] * wx[None, :])[..., None]
        # cắt phần rơi ra ngoài nền chung
        ys, xs = max(0, -y0), max(0, -x0)
        ye, xe = min(mh, H - y0), min(mw, W - x0)
        vung = nen_anh[y0 + ys:y0 + ye, x0 + xs:x0 + xe]
        vung[:] = vung * (1 - a[ys:ye, xs:xe]) + manh[ys:ye, xs:xe] * a[ys:ye, xs:xe]
        x += r + 2 * le_n

    nen_anh[..., 3] = 1.0
    out = bpy.data.images.new("turnaround", W, H, alpha=False)
    out.pixels = nen_anh[::-1].ravel()
    out.filepath_raw = ra
    out.file_format = "PNG"
    out.save()
    print(f"{ra}: {W}x{H}")


main()
