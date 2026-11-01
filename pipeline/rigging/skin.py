"""
Sửa da sau khi gắn tự động (parent_set ARMATURE_AUTO), dùng chung cho mọi nhân vật.
    sys.path.insert(0, os.path.join(STUDIO, "pipeline", "rigging"))
    from skin import fix_skin
    fix_skin(body, head_bone="DEF-spine.006", head_zones=[((0, -0.02, 0.345), 0.128)], keep_prefix="DEF-ear")
Rig Meshy (khung Mixamo) dùng head_bone="mixamorig:Head". head_zones đo theo hình từng nhân vật.
"""
import numpy as np


def smooth_weights(obj, iters=6, amount=0.5, head_bone=None, head_zones=(), keep_prefix=None):
    """Làm mượt trọng số da (Laplacian trên lưới) rồi chuẩn hoá -> chuyển tiếp đều giữa các xương.
    head_bone + head_zones (danh sách (tâm, bán kính)): vùng đầu, mõm, cằm đi theo xương đầu 100%, để các
    bộ phận mặt gắn cứng vào xương đầu (mắt, miệng, mũi) luôn khớp với da. Nhóm có tên bắt đầu bằng
    keep_prefix (ví dụ xương tai) giữ nguyên trọng số."""
    me, groups = obj.data, obj.vertex_groups
    n = len(me.vertices)
    W = np.zeros((n, len(groups)))
    for v in me.vertices:
        for g in v.groups:
            W[v.index, g.group] = g.weight
    e = np.array([ed.vertices[:] for ed in me.edges])
    deg = np.bincount(e.ravel(), minlength=n)[:, None]
    for _ in range(iters):
        s = np.zeros_like(W)
        np.add.at(s, e[:, 0], W[e[:, 1]])
        np.add.at(s, e[:, 1], W[e[:, 0]])
        W = (1 - amount) * W + amount * s / np.maximum(deg, 1)
    W[W < 0.01] = 0
    W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
    if head_bone and head_bone in groups:
        co = np.array([v.co[:] for v in me.vertices])
        mask = np.zeros(n)
        for c, r in head_zones:
            d = np.linalg.norm(co - np.array(c), axis=1)
            mask = np.maximum(mask, 1 - np.clip((d - (r - 0.012)) / 0.03, 0, 1))
        keep_groups = np.array([bool(keep_prefix) and g.name.startswith(keep_prefix) for g in groups])
        head = groups[head_bone].index
        keep = W[:, keep_groups].sum(1)
        other = ~keep_groups
        W[:, other] *= (1 - mask)[:, None]
        W[:, head] += mask * (1 - keep)
        W /= np.maximum(W.sum(1, keepdims=True), 1e-9)
    allv = list(range(n))
    for gi, vg in enumerate(groups):
        vg.remove(allv)
        for i in np.nonzero(W[:, gi])[0]:
            vg.add([int(i)], float(W[i, gi]), "REPLACE")


def fix_skin(obj, iters=14, head_bone=None, head_zones=(), keep_prefix=None):
    """Giữ thể tích + làm mượt trọng số + Corrective Smooth. Với Lumo bản code: bad% ở vai, cổ, chân giảm
    khoảng 1/3, thể tích từ 0.91–0.96 lên 0.98–1.00."""
    arm = next(m for m in obj.modifiers if m.type == "ARMATURE")
    arm.use_deform_preserve_volume = True          # dual quaternion: chống xoắn kiểu "giấy gói kẹo"
    smooth_weights(obj, iters, head_bone=head_bone, head_zones=head_zones, keep_prefix=keep_prefix)
    cs = obj.modifiers.new("CorrectiveSmooth", "CORRECTIVE_SMOOTH")   # mượt lại chỗ nếp gấp so với dáng nghỉ
    cs.iterations, cs.factor, cs.rest_source = 12, 0.5, "ORCO"
    cs.smooth_type = "LENGTH_WEIGHTED"
