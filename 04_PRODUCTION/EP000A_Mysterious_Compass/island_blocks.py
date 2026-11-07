"""
Hòn đảo có Wonder Hub dạng khối, dùng chung cho Cảnh 5 (scene05_blocks.py) và post-credit (scene06_blocks.py) tập 000A,
để hai cảnh cùng một dáng (như 02_ASSET_LIBRARY/Environments/Wonder_Hub/concept/wonder_hub_island_hero.png): đồi cỏ dáng
nón tròn đỉnh, chân đảo là nền đá, đài thiên văn mái vòm ở sườn trước (lệch trái đỉnh đồi), dãy nhà thấp bên phải,
sương ở chân đảo. Mặt trước là -Y (phía máy), +X là bên phải. Không có ô cửa tròn sẫm trên mái vòm (chấm sẫm trước nền
sáng đọc thành con mắt: 04_PRODUCTION/SEEDANCE.md, mục Previz).
"""
from mathutils import Vector

from blocks import add_obj, box_bm, cyl_bm, sphere_bm  # noqa: E402  pipeline/ đã ở sys.path của module gọi


def build_island(dome, sea_z, mats, parent=None, k=1.0, col="SET"):
    """Dựng hòn đảo quanh tâm mái vòm dome (Vector), mặt biển mây ở độ cao sea_z, mọi kích thước nhân k (k = 1: cỡ của
    post-credit, mái vòm bán kính 2.1). mats: hill, rock, hub, mist, và tuỳ chọn band (đai vàng chân mái vòm), dome
    (mái vòm khác màu nhà). Trả về dict các object."""
    hill_c = dome + Vector((0.8, 3.0, 0.0)) * k
    bm = sphere_bm(1.0, (hill_c.x, hill_c.y, sea_z + 0.5 * k), (6.5 * k, 4.5 * k, 7.5 * k), segs=20)
    for v in bm.verts:                                                                         # vuốt nhọn dần lên đỉnh
        h = (v.co.z - sea_z) / (8.0 * k)
        if h > 0:
            f = max(1.0 - 0.75 * h, 0.15)
            v.co.x = hill_c.x + (v.co.x - hill_c.x) * f
            v.co.y = hill_c.y + (v.co.y - hill_c.y) * f
    out = {"hill": add_obj("Island_Hill", bm, mats["hill"], col, parent=parent)}
    out["rock"] = add_obj("Island_Rock", cyl_bm(7.0 * k, 1.6 * k, (hill_c.x, hill_c.y, sea_z + 0.4 * k), cone_top=6.6 * k,
                                                 segs=20), mats["rock"], col, parent=parent)
    bm = cyl_bm(2.3 * k, 1.4 * k, tuple(dome + Vector((0, 0, -0.7)) * k), segs=24)            # tầng có vòm cửa dưới mái vòm
    bm = box_bm((3.0 * k, 1.8 * k, 1.1 * k), tuple(dome + Vector((3.4, 0.6, -0.85)) * k), bm=bm)   # dãy nhà bên phải
    if mats.get("dome"):                                                                       # mái vòm
        out["hub"] = add_obj("Hub", bm, mats["hub"], col, parent=parent)
        out["dome"] = add_obj("Hub_Dome", sphere_bm(2.1 * k, tuple(dome), (1, 1, 0.95), segs=24), mats["dome"], col,
                              parent=parent)
    else:
        bm = sphere_bm(2.1 * k, tuple(dome), (1, 1, 0.95), bm=bm, segs=24)
        out["hub"] = out["dome"] = add_obj("Hub", bm, mats["hub"], col, parent=parent)
    if mats.get("band"):
        out["band"] = add_obj("Hub_Band", cyl_bm(2.2 * k, 0.28 * k, tuple(dome + Vector((0, 0, 0.05)) * k), segs=24),
                              mats["band"], col, parent=parent)
    bm = None
    for cx, cz, sx in ((-5.5, 0.0, 4.5), (5.0, 0.2, 5.0)):
        bm = sphere_bm(1.0, (dome.x + cx * k, dome.y - 4.0 * k, sea_z + cz * k), (sx * k, 1.5 * k, 0.8 * k), bm=bm, segs=12)
    out["mist"] = add_obj("Island_Mist", bm, mats["mist"], col, parent=parent)                # sương chân đảo
    return out
