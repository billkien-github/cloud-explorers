"""
Previz khối Cảnh 4 tập 000A (Cây cầu sập) dẫn Seedance (04_PRODUCTION/SEEDANCE.md): bối cảnh, đạo cụ, Lumo và chú
chim dạng khối (pipeline/blocks.py), máy quay từng cú. Mọi mốc lấy từ timing.py của previz 2D (TIMING trong
build_shot.py của đoạn), không gõ lại số. Diễn theo previz 2D đã chốt: 03_CONTENT/Previz_2D/EP000A_Mysterious_Compass/scene04/.

Bốn đoạn (Seedance 2.5, tối đa 30 giây), nối ở 14.8, 38.6, 61.6 s. `pipeline/split_segments.py` cho một cách 3 đoạn duy nhất,
nối ở 27.2 và 56.6, cả hai chỗ đều tránh theo nhịp truyện (dưới đây), nên giữ 4 đoạn:
    sh080: 0–14.8 s  (S1–S4: cửa mở, toàn cảnh cầu, TÍT trong túi, rút la bàn, cận la bàn chỉ ngôi sao đá)
    sh090: 14.8–38.6 (S5–S11: "Ngay phía trước!", lao lên cầu, CREAAAAK, "Không sao…", CRACK, cầu sập xuống lưới,
           túm dây leo, PHỊCH, chim cười, "Một chiếc cầu… rất cũ!", cận la bàn vẫn chỉ ngôi sao)
    sh100: 38.6–61.6 (S12–S19: nhìn kỹ, vạch bụi cây, "Nhìn kỹ trước đã.", lối bậc đá, chim bắt chước, toàn lối nhỏ,
           tới bệ đá, ấn ngôi sao, CẠCH, phiến đá trượt lộ bản đồ khắc)
    sh110: 61.6–84.8 (S20–S25: chim đậu mép bệ, bản đồ giấy cầm ngược rồi xoay khớp, đài thiên văn khắc lóe, la bàn chỉ
           đảo khắc rồi chân trời, "Chưa từng có hòn đảo này…", chim bay đi)
Lý do chọn chỗ nối (SEEDANCE.md, "Chia cảnh thành đoạn", luật 4), trong các cách 4 đoạn của split_segments.py:
- Không nối ở 25.4 (giữa CREAK và CRACK: cú gag chờ sỏi rồi sập phải nằm trong một lần sinh) hay 27.2 (giữa cú sập và
  cú túm dây leo). Vì đoạn tối đa 29.5 s, chỗ nối đầu chỉ còn 14.8 hoặc 18.0. Bỏ 18.0: cú lấy đà lao lên cầu (RUSH
  17.6–18.55) vắt qua điểm cắt, và S5, S6 cùng góc trung cảnh Lumo ở đầu cầu (cắt nhảy, chỗ nối lộ nhất). Chọn 14.8:
  hết cận la bàn (rút la bàn và mũi sao chỉ nằm trọn đoạn đầu), sang trung cảnh Lumo bắt đầu ý mới (câu hô lần 2, mở
  màn gag cầu); đổi cỡ cảnh mạnh từ cận sang trung.
- 38.6: hết cận la bàn "vẫn chỉ ngôi sao" (khép ý "rất cũ"), sang ý mới "nhìn kỹ trước đã"; cận sang trung. Không nối
  ở 33.4 (chim cười – Lumo đáp), 36.4 (nâng la bàn – cận la bàn), 44.0 (vạch bụi cây – chim thôi cười).
- 61.6: hết cú cận mặt bệ (ấn ngôi sao, CẠCH, phiến đá trượt, lộ bản đồ khắc: hành động và kết quả trong một đoạn),
  sang trung cảnh và ý mới so hai bản đồ; bản đồ giấy chỉ lên hình ở đoạn cuối. Không nối ở 56.6 (đang bước liền
  xuống bậc, tiếng TÍT dày vắt qua điểm cắt) hay 59.0 (với tay – ấn ngôi sao).
Đoạn dài 14.8, 23.8, 23.0, 23.2 s; đoạn đầu ngắn hơn vì không còn chỗ nối nào khác hợp nhịp truyện.

Diễn dựng cho cả cảnh để các đoạn nối liền; khung 1 của đoạn = giây bắt đầu (blocks.T0), chỉ dựng máy quay của các cú
trong đoạn. Cú cận la bàn (S4, S11) và cú nhìn mặt bệ từ trên (S19, S21, S23) là cú nhìn của Lumo: máy ở sau gáy
hoặc trên đầu, đầu Lumo ẩn bằng scale 0 suốt cú (tới hết video nếu là cú cuối của đoạn, vì đuôi giữ máy cú đó). S4,
S11: máy lùi sau gáy 1.1 m, chếch phải, ống 70 mm, tia nhìn tới ngôi sao đá đi giữa hai hàng cột cầu; la bàn giơ dưới
cằm, lệch ra phía tay cầm, nửa dưới khung trên dải CC; bệ đá và ngôi sao (đá vàng nâu, nổi cao in lên nền biển mây)
ở nửa trên. S4, S11, S23: đầu chỉ ngắm theo màn hình (hướng hình chiếu về đích), không theo hướng 3D.
Cú S21: tấm giấy cùng cỡ bản đồ khắc, đặt ngay dưới (cạnh) bản đồ khắc, cùng trục; ẩn hai tay thật, hai bàn tay khối
giữ hai mép bên của tấm giấy (trong tầm với), rương ở giữa mép dưới không bị che; khung lia cuối thấy cùng lúc đài
thiên văn khắc (trên) và góc mây trống của giấy cùng cột (dưới). S12 máy cao trên đầu bụi phía xa, nhìn ngược về cửa:
thấy mặt Lumo ở ba nhịp nhìn, vạch bụi thì hai nửa dạt trái, phải màn hình; S15 máy sau lưng chếch trái thấy tay vịn;
S24 máy sau lưng chếch trái, Lumo mép trái, chân trời mép phải (SEEDANCE.md, "Nhân vật nhìn vật ở chân trời trong cùng
khung"); S25 máy cao chếch phải, ống dài cho chim cất cánh đủ to, ngẩng theo chim rồi mở rộng thành toàn.
Toạ độ (m, Lumo cao 1.00 tới đỉnh đầu): máy phía -Y nhìn về +Y, trục X như previz 2D. Mặt cầu Z 0, X 0.9…5.84, Y
-0.4…0.4, 26 tấm ván, cột thành cầu ở Y ±0.42, thành cầu Z 0.45 (ngang ngực Lumo). Khe núi X 0.9…5.84 kéo dài về phía
máy (Y < 1.0), lưới dây leo dưới mặt cầu Z -0.8…-1.05, dâng lên tới chân lối nhỏ ở Y 1.0; không thấy đáy. Bậc cửa phủ
rêu X -1.6…0.9, Y -1.2…1.3; cửa đá trong vách sau (mặt vách Y 1.3), tâm X -0.75, mở ra phía máy; mặt trong cánh cửa
(lúc mở quay về phía cầu) có hình mây phát sáng, tắt dần. Lối nhỏ men vách sau Y 1.0…1.6: 5 bậc lên từ X 0.15, gờ Z 0.9
tới X 4.6, 5 bậc xuống tới bãi đất bên phải ở X 6.1; tay vịn dây leo phía vách; mặt lối cùng tông vách. Bụi cây trùm
kín năm bậc lên và tay vịn (X -0.05…1.75): trước khi vạch chỉ thấy bụi, gờ phía sau nửa khuất; vạch thì nửa ngoài ngả
ra khe, nửa trong ngả vào vách, cả hai ép thấp xuống. Bệ đá X 6.75…7.6, Y -0.45…0.72, mặt bệ Z 0.45: ngôi sao đá (4
cánh dài, 4 cánh ngắn, cao 0.13) nổi như cái nút ở góc gần, trái (6.97, 0.22); bản đồ khắc trong hốc sâu ở (7.3, -0.12), mọi
hình khắc nằm dưới phiến đá che (phiến trượt về +Y, lút vào trong bệ); đài thiên văn khắc là thân tháp có mái vòm,
cao hơn cây trên đảo, không ô cửa sẫm. Lumo tới bệ đứng trước ngôi sao (6.52, 0.12), lúc chim đậu bước sang trước bản đồ khắc (6.52, -0.12), nhìn +X. Chân trời (mũi sao chỉ cuối cảnh, chim bay đi) theo hướng
(1, -1): bên phải và hơi về phía máy, để ở cú ngang thấy mặt Lumo, ở cú nhìn từ trên mũi sao chỉ lên góc phải.
La bàn: vỏ tròn vàng đường kính 0.17 (to hơn cỡ thật một chút), mặt kem phát sáng, mũi sao 7 cánh ngắn trắng và một
đầu chỉ dài sẫm (gần gấp đôi cánh ngắn); tâm la bàn trước bàn tay 0.1 (tay nắm mép vỏ), mặt la bàn ngửa chếch 45° về
phía Lumo, la bàn tay gần chếch thêm 30° về phía máy; đầu chỉ ngắm từng khung về mục tiêu (ngôi sao đá, đảo khắc, chân
trời) bằng hình chiếu lên mặt la bàn. La bàn lóe theo đài thiên văn khắc bằng tiếng TÍT và rung trong túi, không đổi
màu: đài khắc không phải hòn đảo thật, luật lóe xanh ngọc cùng nhịp (03_CONTENT/README.md, "Tín hiệu nối bốn tập")
chỉ áp cho hòn đảo có Wonder Hub.
Màu: Lumo cam, chú chim nâu (ô trắng = hướng mặt); bối cảnh, đạo cụ xám; la bàn vàng, mặt kem; hình mây trên cửa,
đài thiên văn khắc (lóe xanh ngọc) phát sáng.
"""
import importlib.util
import math
import pathlib
import random
import sys

import bmesh
import bpy
from bpy_extras import anim_utils
from mathutils import Euler, Matrix, Vector

HERE = pathlib.Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / "CLAUDE.md").exists())
sys.path.insert(0, str(ROOT / "pipeline"))
from blocks import *  # noqa: E402,F403  khối, vật liệu, nhân vật dạng khối, keyframe theo giây, máy quay

HOLD = 1 / 24                                                    # một khung: key ẩn và key hiện cách nhau ít hơn thì rơi vào cùng khung
RIGHT = 70                                                       # Lumo ở bậc cửa nhìn sang cầu, ba phần tư về phía máy
BRIDGE = (0.9, 5.84)
PLANK_W, PITCH, DECK = 0.17, 0.19, 0.4                           # bề ngang tấm ván, bước ván, nửa bề rộng mặt cầu
PLANKS = [BRIDGE[0] + PITCH * i for i in range(26)]              # mép trái từng tấm ván
POSTS = [0.96 + 0.54 * k for k in range(10)]                     # cột thành cầu; 0, 1 sát cửa, 8, 9 bên kia
RAIL_Z, POST_TOP, RAIL_Y = 0.45, 0.55, 0.42
CREAK_PLANK, FALL, FALL_POSTS = 3, range(4, 22), range(2, 8)     # tấm ván bật lên; dãy ván rơi; cột rơi
LEDGE_Z, LEDGE_END = 0.9, 4.6
PATH_Y0, PATH_Y1, PATH_Y = 1.0, 1.6, 1.3                         # lối nhỏ: mép ngoài, vách, giữa lối (Lumo đi)
HRAIL_Y = 1.52                                                   # tay vịn dây leo sát vách
BIRD_PATH_Y = 1.1                                                # chim nhảy theo ở mép ngoài lối
DOOR_X, DOOR_W, DOOR_H, DOOR_Y = -0.75, 0.74, 1.0, 1.3           # tâm cửa, bề rộng, chiều cao thân (vòm ở trên), mặt vách
PLINTH = (6.75, 7.6, -0.45, 0.72)
PTOP = 0.45
STAR_AT = Vector((6.97, 0.22, PTOP))
CMAP, CMAP_V, CMAP_U = Vector((7.3, -0.12, PTOP)), 0.42, 0.5     # bản đồ khắc: tâm, dài theo X (trên–dưới), theo Y (trái–phải)
LUMO_PLINTH = (6.52, -0.12)                                      # đứng trước bản đồ khắc (S20–S25)
LUMO_STAR = (6.52, 0.12)                                         # tới bệ: đứng trước ngôi sao đá (S18–S19)
HORIZON = Vector((6.6, -0.1, 0.9)) + Vector((1.0, -1.0, 0.03)).normalized() * 80
ISLANDS = [(-0.32, 0.3), (0.02, 0.33), (-0.33, -0.22), (0.22, -0.3)]   # đảo trên cả hai bản đồ (u phải, v trên)
OBS_UV = (0.37, 0.12)                                            # đảo có đài thiên văn: chỉ trên bản đồ khắc, mép phải
COMPASS_TILT = (-45, 0, 0)                                       # mặt la bàn ngửa chếch về phía mắt Lumo
COMPASS_TILT_R = (-45, -30, 0)                                   # tay gần máy: mặt chếch thêm về phía máy (không thấy cạnh)
CPOS = (0, -0.1, 0.03)                                           # tâm la bàn trước bàn tay: tay nắm mép vỏ, không đè mặt kính
SIT_Z = -0.24


def load_timing(timing):
    spec = importlib.util.spec_from_file_location("scene04_timing", ROOT / timing)
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    return tm


def path_z(x):
    """Mặt lối nhỏ: 5 bậc lên (rộng 0.3, cao 0.15) từ X 0.15, gờ phẳng tới 4.6, 5 bậc xuống tới bãi đất ở 6.1."""
    if x < 0.15 or x >= LEDGE_END + 1.5:
        return 0.0
    if x < 1.65:
        return 0.15 * math.ceil((x - 0.15) / 0.3 + 1e-9)
    if x < LEDGE_END:
        return LEDGE_Z
    return LEDGE_Z - 0.15 * math.ceil((x - LEDGE_END) / 0.3 + 1e-9)


PROFILE = [(0.15, 0.0)]
for _k in range(1, 6):
    PROFILE += [(0.15 + 0.3 * (_k - 1), 0.15 * _k), (0.15 + 0.3 * _k, 0.15 * _k)]
PROFILE += [(LEDGE_END, LEDGE_Z)]
for _k in range(1, 6):
    PROFILE += [(LEDGE_END + 0.3 * (_k - 1), LEDGE_Z - 0.15 * _k), (LEDGE_END + 0.3 * _k, LEDGE_Z - 0.15 * _k)]


def net_base(x):
    u = min(1.0, max(0.0, (x - BRIDGE[0]) / (BRIDGE[1] - BRIDGE[0])))
    return -0.8 - 0.25 * math.sin(math.pi * u)


def net_surf(x, y):
    """Mặt lưới dây leo: võng dưới cầu, giăng tới sát chân vách dưới lối nhỏ (Y 1.0), mép trong hơi vểnh lên.
    Không dâng lên tới mặt lối như hình cắt 2D: dựng 3D thì mặt lưới dâng dốc thành một bức tường lưới."""
    zb = net_base(x)
    if y <= 0.2:
        return zb
    v = min(1.0, (y - 0.2) / (PATH_Y0 - 0.2))
    return zb + 0.12 * v * v


def yaw_to(src, dst):
    """Hướng (yaw) để nhìn từ src tới dst: 0 = -Y, 90 = +X."""
    return math.degrees(math.atan2(dst[0] - src[0], -(dst[1] - src[1])))


def wrap(a):
    return (a + 180) % 360 - 180


def prism(profile, y0, y1, bm=None):
    """Khối lăng trụ: đa giác (x, z) kéo dài theo Y từ y0 tới y1."""
    bm = bm or bmesh.new()
    a = [bm.verts.new((x, y0, z)) for x, z in profile]
    b = [bm.verts.new((x, y1, z)) for x, z in profile]
    bm.faces.new(list(reversed(a)))
    bm.faces.new(b)
    n = len(profile)
    for i in range(n):
        bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    return bm


def poly_bm(pts, z0, z1, bm=None):
    """Khối dẹt: đa giác (x, y) kéo theo Z từ z0 tới z1."""
    bm = bm or bmesh.new()
    a = [bm.verts.new((x, y, z0)) for x, y in pts]
    b = [bm.verts.new((x, y, z1)) for x, y in pts]
    bm.faces.new(list(reversed(a)))
    bm.faces.new(b)
    n = len(pts)
    for i in range(n):
        bm.faces.new((a[i], a[(i + 1) % n], b[(i + 1) % n], b[i]))
    return bm


def star_pts(radii, inner, start=90.0):
    """Đa giác ngôi sao: cánh k ở góc start + 45k (độ, từ +X ngược chiều kim đồng hồ), dài radii[k]."""
    pts = []
    n = len(radii)
    for k in range(n):
        a = math.radians(start + 360 * k / n)
        b = math.radians(start + 360 * (k + 0.5) / n)
        pts += [(radii[k] * math.cos(a), radii[k] * math.sin(a)), (inner * math.cos(b), inner * math.sin(b))]
    return pts


def rod(name, p0, p1, r, mat, col, bm_only=False, bm=None, segs=8):
    """Trụ từ p0 tới p1 (cột, dây thành cầu, tay vịn)."""
    p0, p1 = Vector(p0), Vector(p1)
    q = (p1 - p0).to_track_quat("Z", "Y")
    m = Matrix.Translation((p0 + p1) / 2) @ q.to_matrix().to_4x4()
    bm = bm or bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r, depth=(p1 - p0).length, matrix=m)
    if bm_only:
        return bm
    return add_obj(name, bm, mat, col)


def chain(name, pts, r, mat, col):
    bm = None
    for p0, p1 in zip(pts, pts[1:]):
        bm = rod(name, p0, p1, r, mat, col, bm_only=True, bm=bm)
    return add_obj(name, bm, mat, col)


def linear(ob):
    """Mọi key của ob nội suy LINEAR (máy di chuyển đều: để ease thì Seedance dồn chuyển động thành một cú vụt)."""
    ad = ob.animation_data
    if ad and ad.action:
        for fc in anim_utils.action_get_channelbag_for_slot(ad.action, ad.action_slot).fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def emit_key(mat, t, strength):
    s = bsdf_in(mat, "Emission Strength")
    s.default_value = strength
    s.keyframe_insert("default_value", frame=fr(t))


class Act:
    """Giữ (nghiêng, lăn, hướng) và vị trí của gốc nhân vật để mỗi key ghi đủ ba trục. Gọi theo thứ tự thời gian."""

    def __init__(self, rig, x, y, yaw, eye=0.75):
        self.r, self.x, self.y, self.z, self.yaw, self.lean, self.roll, self.eye = rig, x, y, 0.0, yaw, 0.0, 0.0, eye

    def pose(self, t, lean=None, yaw=None, roll=None):
        self.lean = self.lean if lean is None else lean
        self.yaw = self.yaw if yaw is None else yaw
        self.roll = self.roll if roll is None else roll
        rot(self.r.root, [(t, (self.lean, self.roll, self.yaw))])

    def go(self, t, x=None, z=0.0, y=None):
        self.x = self.x if x is None else x
        self.y = self.y if y is None else y
        self.z = z
        key(self.r.root, "location", t, Vector((self.x, self.y, z)))

    def matrix(self):
        return (Matrix.Translation((self.x, self.y, self.z))
                @ Euler((math.radians(self.lean), math.radians(self.roll), math.radians(self.yaw))).to_matrix().to_4x4())

    def look_angles(self, p):
        """(cúi, quay) của đầu so với thân để nhìn điểm p (thế giới)."""
        yaw = max(-110, min(110, wrap(yaw_to((self.x, self.y), p) - self.yaw)))
        horiz = math.hypot(p[0] - self.x, p[1] - self.y)
        pitch = math.degrees(math.atan2(self.z + self.eye - p[2], max(horiz, 0.05)))
        return max(-40, min(24, pitch)), yaw                       # cúi quá 24° thì khối đầu trông như cả người chúi


def build_bird(loc, mat):
    """Chú chim nhỏ cỡ nắm tay Lumo (như Cảnh 1): thân tròn, đầu, chỏm lông, đuôi, hai cánh."""
    B = Rig()
    B.root = empty("BIRD", "CAST", loc=loc)
    add_obj("Bird_Body", sphere_bm(0.042, (0, 0, 0.045), (1.0, 1.1, 0.95)), mat, "CAST", parent=B.root)
    B.neck = empty("Bird_Neck", "CAST", parent=B.root, loc=(0, -0.01, 0.095))
    B.head = add_obj("Bird_Head", sphere_bm(0.032, (0, 0, 0.0)), mat, "CAST", parent=B.neck)
    face_marker("Bird_Face", B.head, 0.03, 0.02, -0.03, 0.0)
    add_obj("Bird_Tuft", box_bm((0.012, 0.025, 0.03), (0, 0.01, 0.04)), mat, "CAST", parent=B.head)
    add_obj("Bird_Tail", box_bm((0.02, 0.05, 0.04), (0, 0.06, 0.07)), mat, "CAST", parent=B.root)
    B.wing = add_obj("Bird_Wing", box_bm((0.012, 0.05, 0.03), (0, 0.015, -0.02)), mat, "CAST", parent=B.root,
                     loc=(-0.045, 0.0, 0.065))
    B.wing_far = add_obj("Bird_WingFar", box_bm((0.012, 0.05, 0.03), (0, 0.015, -0.02)), mat, "CAST", parent=B.root,
                         loc=(0.045, 0.0, 0.065))
    return B


def build(timing, offset, seconds, out_blend, segment=None):
    """seconds: độ dài video render (số nguyên giây Seedance nhận); segment: độ dài đoạn trong cảnh. Từ segment tới
    seconds chỉ giữ cú máy cuối (diễn vẫn chạy tiếp), lúc dựng cắt bỏ."""
    segment = seconds if segment is None else segment
    tm = load_timing(timing)
    start(tm.FPS, seconds, offset)
    random.seed(4)
    S = {n: (a, b) for n, a, b in tm.SHOTS}
    end_t = offset + segment
    video_end = offset + seconds
    T_END = max(video_end, tm.SECONDS) + 1.0                       # diễn cuối cảnh chạy tới đây (qua cả đuôi đoạn cuối)
    in_seg = {n: offset - 1e-6 <= a < end_t - 1e-6 for n, a, b in tm.SHOTS}
    last_shot = [n for n, a, b in tm.SHOTS if in_seg[n]][-1]

    def until(n):
        """Hết cú n; cú cuối của đoạn thì tới hết video (đuôi giữ máy cú này)."""
        return video_end + 1.0 if n == last_shot else S[n][1]

    # ============================================================ vật liệu
    rock_m = material("M_Rock", (0.5, 0.49, 0.47), 0.9)
    wall_m = material("M_Wall", (0.56, 0.55, 0.53), 0.9)
    stone_m = material("M_Stone", (0.66, 0.65, 0.62), 0.8)          # bậc cửa, lối nhỏ, bệ đá
    stone_d = material("M_StoneDark", (0.38, 0.37, 0.35), 0.85)
    path_m = material("M_PathStone", (0.5, 0.49, 0.47), 0.9)          # lối nhỏ cùng tông vách: lùi trong vách, không nổi hơn cầu
    star_m = material("M_StarStone", (0.72, 0.5, 0.22), 0.7)      # đá vàng nâu như ảnh bệ đá: nổi trên mặt bệ xám và trên nền
                                                                   # biển mây trắng (từ đầu cầu nhìn ngang, ngôi sao in lên nền mây)
    moss_m = material("M_Moss", (0.36, 0.38, 0.35), 0.95)
    grass_m = material("M_Grass", (0.46, 0.47, 0.44), 0.95)
    wood_m = material("M_Wood", (0.58, 0.55, 0.51), 0.8)            # ván cầu, cột
    vine_m = material("M_Vine", (0.32, 0.34, 0.31), 0.85)           # dây thành cầu, tay vịn
    net_m = material("M_Net", (0.27, 0.29, 0.26), 0.95)             # đệm dây leo dày dưới mắt lưới
    netw_m = material("M_NetCord", (0.68, 0.7, 0.66), 0.8)          # sợi lưới
    bush_m = material("M_Bush", (0.33, 0.35, 0.32), 0.9)
    dark_m = material("M_Doorway", (0.1, 0.1, 0.11), 0.9)
    cloud_m = material("M_CloudCarve", (0.85, 0.78, 0.55), 0.4, emit=((1.0, 0.85, 0.35), 3.0))
    sea_m = material("M_CloudSea", (0.86, 0.88, 0.9), 0.9, emit=((0.9, 0.92, 0.95), 0.4))
    island_m = material("M_Island", (0.52, 0.51, 0.5), 0.9)
    prop = material("M_Prop", (0.85, 0.85, 0.83), 0.6)             # bản đồ giấy
    prop_dark = material("M_PropDark", (0.12, 0.12, 0.13), 0.6)
    gold_m = material("M_CompassGold", (0.95, 0.72, 0.18), 0.35)
    cface_m = material("M_CompassFace", (0.95, 0.94, 0.86), 0.4, emit=((1.0, 0.95, 0.7), 0.6))
    needle_m = material("M_CompassPoints", (0.97, 0.98, 1.0), 0.4)
    pointer_m = material("M_CompassPointer", (0.08, 0.1, 0.18), 0.4)
    teal_m = material("M_TealFlash", (0.1, 0.75, 0.68), 0.3, emit=((0.1, 0.8, 0.7), 1.5))   # sáng vừa đủ để còn ra màu xanh ngọc
    bird_m = material("M_Bird_Brown", (0.32, 0.15, 0.06), 0.6)
    lumo_m = cast_materials()["lumo"]

    # ============================================================ bối cảnh
    # vách trái cao, bậc cửa phủ rêu, vách sau có cửa đá; bãi đất bên phải; biển mây, trời, đảo xa
    add_obj("CliffLeft", box_bm((4.4, 13.3, 7.6), (-3.8, -5.35, -0.4)), rock_m, "SET")          # X -6…-1.6, Y -12…1.3
    add_obj("Threshold", box_bm((2.5, 2.5, 4.0), (-0.35, 0.05, -2.0)), stone_m, "SET")          # bậc cửa X -1.6…0.9, Y -1.2…1.3
    add_obj("ThresholdLip", box_bm((0.06, 2.5, 0.04), (0.87, 0.05, -0.02)), stone_d, "SET")     # mép bậc cửa giáp đầu cầu
    add_obj("ThresholdMoss", box_bm((1.5, 1.1, 0.03), (-0.55, 0.45, 0.012)), moss_m, "SET")     # đệm rêu chỗ ngã ngồi
    add_obj("LedgeBelow", box_bm((2.5, 10.8, 3.1), (-0.35, -6.6, -2.45)), rock_m, "SET")        # trước bậc cửa: đá dưới mặt lưới
    # vách sau: phần có cửa (mặt Y 1.3) tới X -0.15, phần lối nhỏ (mặt Y 1.6) từ X -0.15 tới 6.3
    dl, dr, dtop = DOOR_X - DOOR_W / 2, DOOR_X + DOOR_W / 2, DOOR_H + DOOR_W / 2
    add_obj("DoorWall_L", box_bm((dl + 6.0, 2.7, 6.4), ((dl - 6.0) / 2, 2.65, -0.8)), wall_m, "SET")
    add_obj("DoorWall_R", box_bm((-0.15 - dr, 0.3, 2.35), ((dr - 0.15) / 2, 1.45, 1.175)), wall_m, "SET")
    add_obj("DoorWall_Top", box_bm((DOOR_W, 0.3, 2.35 - dtop), (DOOR_X, 1.45, (dtop + 2.35) / 2)), wall_m, "SET")
    add_obj("DoorArch", sphere_bm(DOOR_W / 2, (DOOR_X, 1.36, DOOR_H), (1.0, 0.25, 1.0), segs=20), dark_m, "SET")
    add_obj("DoorArchFill", box_bm((DOOR_W, 0.15, DOOR_W / 2), (DOOR_X, 1.525, DOOR_H + DOOR_W / 4)), wall_m, "SET")
    add_obj("Doorway", box_bm((DOOR_W, 0.06, DOOR_H), (DOOR_X, 1.56, DOOR_H / 2)), dark_m, "SET")   # trong vòm: tối
    add_obj("BackWall", box_bm((6.45, 2.4, 6.75), (3.075, 2.8, -1.025)), wall_m, "SET")         # X -0.15…6.3, mặt Y 1.6, đỉnh Z 2.35
    add_obj("BackWallTop", box_bm((12.3, 2.4, 0.3), (0.15, 2.8, 2.45)), moss_m, "SET")
    clouds_bm = None
    for cx, cz, s in ((DOOR_X, dtop + 0.22, 0.32), (DOOR_X - 0.42, DOOR_H + 0.1, 0.2), (DOOR_X + 0.43, DOOR_H + 0.1, 0.2)):
        for dx, dz, r in ((-0.45, 0, 0.3), (0.0, 0.12, 0.38), (0.45, 0, 0.28)):
            clouds_bm = sphere_bm(r * s, (cx + dx * s, DOOR_Y - 0.01, cz + dz * s), (1.0, 0.25, 0.8), bm=clouds_bm, segs=12)
    add_obj("LintelClouds", clouds_bm, cloud_m, "SET")              # mây khắc trên khung cửa, phát sáng rồi tắt cùng mây trên cánh cửa
    add_obj("GroundRight", box_bm((3.66, 18.0, 4.0), (7.67, -3.0, -2.0)), grass_m, "SET")      # X 5.84…9.5, Y -12…6
    add_obj("CloudSea", box_bm((200.0, 200.0, 0.1), (60.0, 40.0, -4.0)), sea_m, "SET")
    bm = None
    for cx, cy, cz, s in ((-10.0, 55.0, 3.5, 3.0), (6.0, 62.0, 4.5, 3.6), (-24.0, 48.0, 2.5, 2.4), (24.0, 70.0, 5.0, 2.8)):
        bm = cyl_bm(0.0, s * 0.7, (cx, cy, cz - s * 0.35), bm=bm, cone_top=s, segs=12)         # đảo xa: phía sau, thấp, không ở hướng chân trời
        bm = sphere_bm(s, (cx, cy, cz), (1.0, 1.0, 0.2), bm=bm, segs=12)
    add_obj("Islands", bm, island_m, "SET")
    bm = None
    for cx, cy, r in ((8.9, 2.2, 0.45), (9.25, 0.9, 0.38), (9.2, 3.4, 0.5)):
        bm = sphere_bm(r, (cx, cy, r * 0.6), (1.0, 1.0, 0.75), bm=bm, segs=14)
    add_obj("HedgeRight", bm, bush_m, "SET")

    # lối nhỏ: mặt bậc (lăng trụ theo PROFILE), gờ đá thấp mép ngoài, tay vịn dây leo sát vách, cọc giữ tay vịn
    prof = PROFILE + [(LEDGE_END + 1.5, 0.0), (LEDGE_END + 1.5, -1.2), (0.15, -1.2)]
    add_obj("PathSteps", prism(prof, PATH_Y0, PATH_Y1), path_m, "SET")
    add_obj("PathLanding", box_bm((0.3, 0.3, 0.04), (0.0, 1.45, -0.02)), path_m, "SET")
    lip = [(x, z + 0.07) for x, z in PROFILE] + [(x, z - 0.02) for x, z in reversed(PROFILE)]
    add_obj("PathLip", prism(lip, PATH_Y0 - 0.02, PATH_Y0 + 0.05), stone_d, "SET")
    rail_pts = [(x, HRAIL_Y, path_z(x - 1e-3 if x > 0.2 else x) + 0.46) for x in
                [0.0] + [p[0] for p in PROFILE[1::2]] + [LEDGE_END + 1.6]]
    chain("PathHandrail", rail_pts, 0.025, vine_m, "SET")
    bm = None
    for x, _, z in rail_pts[1::2]:
        bm = rod("", (x, HRAIL_Y, z - 0.46), (x, HRAIL_Y, z + 0.02), 0.018, wood_m, "SET", bm_only=True, bm=bm)
    add_obj("PathRailPegs", bm, wood_m, "SET")

    # lưới dây leo: mặt lưới dâng tới chân lối nhỏ, đệm dày bên dưới; sợi lưới bằng modifier Wireframe (vật liệu thứ hai)
    xs = [-1.6 + 0.2 * i for i in range(38)] + [BRIDGE[1]]
    ys = [-12.0 + 0.2 * j for j in range(66)]
    bm = bmesh.new()
    grid = [[bm.verts.new((x, y, net_surf(x, y))) for x in xs] for y in ys]
    for j in range(len(ys) - 1):
        for i in range(len(xs) - 1):
            bm.faces.new((grid[j][i], grid[j][i + 1], grid[j + 1][i + 1], grid[j + 1][i]))
    net = add_obj("VineNet", bm, net_m, "SET")
    net.data.materials.append(netw_m)
    wf = net.modifiers.new("Cords", "WIREFRAME")
    wf.thickness, wf.use_replace, wf.material_offset, wf.offset = 0.024, False, 1, 1.0
    basis = net.shape_key_add(name="Basis")
    sag = net.shape_key_add(name="Sag")                            # lưới võng xuống đỡ ván rồi nảy bập bềnh
    for v in sag.data:
        x, y = v.co.x, v.co.y
        u = min(1.0, max(0.0, (x - BRIDGE[0]) / (BRIDGE[1] - BRIDGE[0])))
        w = 1.0 if y <= 0.2 else max(0.0, 1 - 0.6 * (y - 0.2) / 0.8)
        v.co.z -= 0.18 * math.sin(math.pi * u) * w
    del basis

    # cầu ván cổ: ván, cột hai bên, dây thành cầu quấn dây leo
    planks = []
    for i, x0 in enumerate(PLANKS):
        pv = empty(f"Plank{i}", "SET", loc=(x0, 0.0, 0.0))
        add_obj(f"Plank{i}_Shape", box_bm((PLANK_W, 2 * DECK, 0.05), (PLANK_W / 2, 0, -0.025)), wood_m, "SET", parent=pv)
        planks.append(pv)
    halves = []
    for k in (0, 1):                                               # tấm ván trước mũi chân gãy làm hai (theo chiều dài)
        hv = empty(f"PlankHalf{k}", "SET", loc=(PLANKS[FALL[0]] + PLANK_W / 2, (k - 0.5) * DECK, 0.0))
        add_obj(f"PlankHalf{k}_Shape", box_bm((PLANK_W, DECK, 0.05), (0, 0, -0.025)), wood_m, "SET", parent=hv)
        halves.append(hv)
    posts = {}
    for side, y in (("near", -RAIL_Y), ("far", RAIL_Y)):
        for k, x in enumerate(POSTS):
            pv = empty(f"Post_{side}{k}", "SET", loc=(x, y, 0.0))
            add_obj(f"Post_{side}{k}_Shape", box_bm((0.075, 0.075, 0.62), (0, 0, 0.24)), wood_m, "SET", parent=pv)
            posts[side, k] = pv
    rails = {}
    for side, y in (("near", -RAIL_Y), ("far", RAIL_Y)):
        for k in range(9):
            rails[side, k] = chain(f"Rail_{side}{k}", [(POSTS[k], y, RAIL_Z), ((POSTS[k] + POSTS[k + 1]) / 2, y, RAIL_Z - 0.03),
                                                       (POSTS[k + 1], y, RAIL_Z)], 0.025, vine_m, "SET")
        droop = [(POSTS[1] + (POSTS[8] - POSTS[1]) * i / 16, y, RAIL_Z - 0.75 * math.sin(math.pi * i / 16)) for i in range(17)]
        rails[side, "droop"] = chain(f"Rail_{side}_Droop", droop, 0.025, vine_m, "SET")   # dây thành cầu chùng xuống giữa khe

    # bụi cây trùm kín năm bậc lên và tay vịn (X -0.05…1.75): từ mọi máy phía trước chỉ thấy bụi, gờ phía sau nửa khuất.
    # Hai nửa theo chiều sâu (mép ngoài lối, sát vách); vạch thì nửa ngoài ngả ra khe, nửa trong ngả vào vách, máy S12
    # đặt sau vai Lumo nhìn theo lối nên hai nửa dạt sang phải, trái màn hình (SEEDANCE.md, "Vật vạch ra trước lối đi")
    bush = []
    near_blobs = ((-0.75, 0.0, 0.42, 0.34), (-0.4, 0.02, 0.6, 0.38), (-0.02, 0.02, 0.78, 0.4), (0.38, 0.02, 0.98, 0.4),
                  (0.76, 0.0, 1.15, 0.36), (-0.6, 0.0, 0.95, 0.26), (0.15, 0.0, 1.3, 0.28), (0.6, 0.0, 1.45, 0.24))
    far_blobs = ((-0.72, -0.05, 0.5, 0.3), (-0.35, -0.05, 0.72, 0.34), (0.05, -0.05, 0.92, 0.36), (0.45, -0.05, 1.12, 0.36),
                 (0.8, -0.05, 1.3, 0.32), (-0.2, -0.05, 1.15, 0.26), (0.55, -0.05, 1.55, 0.24))
    for name, py, blobs in (("BushNear", 1.02, near_blobs), ("BushFar", 1.55, far_blobs)):
        pv = empty(name, "SET", loc=(0.85, py, 0.0))
        bm = None
        for cx, cy, cz, r in blobs:
            bm = sphere_bm(r, (cx, cy, cz), (1.0, 0.75, 1.0), bm=bm, segs=14)
        add_obj(name + "_Shape", bm, bush_m, "SET", parent=pv)
        bush.append(pv)

    # cửa đá: bản lề ở mép trái lỗ cửa, mở ra phía máy; mây khắc ở mặt trong (quay về phía cầu khi mở)
    door = empty("DoorSlab", "SET", loc=(dl, DOOR_Y + 0.04, 0.0))
    bm = box_bm((DOOR_W - 0.02, 0.08, DOOR_H), (DOOR_W / 2, 0, DOOR_H / 2))
    bm = cyl_bm(DOOR_W / 2 - 0.01, 0.08, (DOOR_W / 2, 0, DOOR_H), axis="Y", bm=bm, segs=20)
    add_obj("DoorSlab_Shape", bm, stone_m, "SET", parent=door)
    bm = None
    for cx, cz, s in ((DOOR_W / 2, 0.98, 0.42), (DOOR_W / 2 - 0.12, 0.52, 0.3), (DOOR_W / 2 + 0.13, 0.3, 0.3)):
        for dx, dz, r in ((-0.45, 0, 0.3), (0.0, 0.12, 0.38), (0.45, 0, 0.28)):
            bm = sphere_bm(r * s, (cx + dx * s, 0.045, cz + dz * s), (1.0, 0.25, 0.8), bm=bm, segs=12)
    add_obj("DoorClouds", bm, cloud_m, "SET", parent=door)

    # bệ đá: khối có hốc bản đồ khắc; ngôi sao đá nổi như cái nút; phiến đá che hốc, trượt về +Y lút vào trong bệ
    px0, px1, py0, py1 = PLINTH
    hx0, hx1 = CMAP.x - CMAP_V / 2, CMAP.x + CMAP_V / 2
    hy0, hy1 = CMAP.y - CMAP_U / 2, CMAP.y + CMAP_U / 2
    floor_z = PTOP - 0.11                                          # hốc sâu: cây, đài thiên văn khắc nằm trọn dưới phiến che
    bm = box_bm((px1 - px0, py1 - py0, floor_z), ((px0 + px1) / 2, (py0 + py1) / 2, floor_z / 2))
    for bx0, bx1, by0, by1 in ((px0, hx0, py0, py1), (hx1, px1, py0, py1), (hx0, hx1, py0, hy0), (hx0, hx1, hy1, py1)):
        bm = box_bm((bx1 - bx0, by1 - by0, PTOP - floor_z), ((bx0 + bx1) / 2, (by0 + by1) / 2, (floor_z + PTOP) / 2), bm=bm)
    add_obj("Plinth", bm, stone_m, "SET")
    bm = None
    for dx, dz, r in ((-0.12, 0, 0.09), (0.0, 0.04, 0.12), (0.12, 0, 0.085)):   # mây khắc ở mặt trước bệ
        bm = sphere_bm(r, ((px0 + px1) / 2 + dx, py0 - 0.005, 0.2 + dz), (1.0, 0.2, 0.8), bm=bm, segs=12)
    add_obj("Plinth_Cloud", bm, stone_d, "SET")

    def map_xy(u, v):
        return Vector((CMAP.x + v * CMAP_V, CMAP.y - u * CMAP_U, floor_z))

    bm = None
    for u, v in ISLANDS:
        bm = cyl_bm(0.05, 0.02, map_xy(u, v) + Vector((0, 0, 0.01)), bm=bm, segs=14)
        bm = cyl_bm(0.02, 0.045, map_xy(u, v) + Vector((0, 0.01, 0.0425)), bm=bm, cone_top=0.0, segs=8)   # cây hình chóp
    obs = map_xy(*OBS_UV)
    bm = box_bm((0.1, 0.1, 0.02), obs + Vector((0, 0, 0.01)), bm=bm)                               # đế vuông: khác các đảo
    bm = cyl_bm(0.026, 0.05, obs + Vector((0, 0, 0.045)), bm=bm, segs=14)                           # thân tháp cao
    bm = sphere_bm(0.03, obs + Vector((0, 0, 0.07)), (1.0, 1.0, 0.75), bm=bm, segs=12)               # mái vòm, không ô cửa sẫm
    for k in range(5):                                             # vạch mây gợn sóng
        bm = box_bm((0.012, 0.08, 0.006), map_xy(-0.1 + 0.08 * k, -0.02 + 0.05 * (k % 2)) + Vector((0, 0, 0.003)), bm=bm)
    add_obj("Plinth_CarvedMap", bm, stone_d, "SET")
    flash = add_obj("ObsFlash", sphere_bm(0.06, (0, 0, 0), (1.0, 1.0, 0.6), segs=14), teal_m, "PROPS", loc=obs + Vector((0, 0, 0.055)))
    cover = empty("Plinth_Cover", "SET")
    add_obj("Plinth_CoverShape", box_bm((CMAP_V - 0.01, CMAP_U - 0.01, 0.034), (CMAP.x, CMAP.y, PTOP - 0.019)), stone_m, "SET",
            parent=cover)
    pstar = empty("Plinth_Star", "SET", loc=STAR_AT)
    add_obj("Plinth_StarShape", poly_bm(star_pts([0.14, 0.08] * 4, 0.04), 0.0, 0.13), star_m, "SET", parent=pstar)   # nổi cao như cái nút: từ đầu cầu thấy một nút sáng
    add_obj("Plinth_StarRing", cyl_bm(0.16, 0.006, (STAR_AT.x, STAR_AT.y, PTOP + 0.002), segs=24), stone_d, "SET")

    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    COLS["SET"].objects.link(sun)
    sun.data.energy, sun.data.angle = 3.5, math.radians(4)
    sun.rotation_euler = (math.radians(50), 0, math.radians(-25))
    world = bpy.data.worlds.new("Sky")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.50, 0.66, 0.92, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.9

    # ============================================================ Lumo, túi da, tay cầm đồ, la bàn, bản đồ, chú chim
    L = build_lumo((DOOR_X, 1.42, 0.0))
    lumo = Act(L, DOOR_X, 1.42, 0)
    bag = add_obj("Lumo_Bag", box_bm((0.1, 0.06, 0.09)), prop_dark, "CAST", parent=L.root, loc=(-0.2, -0.1, 0.3))
    BAG = Vector((-0.2, -0.1, 0.3))
    BAG_TOP = BAG + Vector((0, -0.04, 0.09))                       # miệng túi: đồ ló ra, chui vào ở đây, túi giữ nguyên

    # mỗi tay có một khối "bàn tay" (empty ở đầu tay) xoay ngược tay để đồ cầm giữ hướng theo thân
    hands = {}
    for side, arm in (("R", L.arm_r), ("L", L.arm_l)):
        hands[side] = empty(f"Lumo_Hand{side}", "PROPS", parent=arm, loc=(0, -0.02, -0.27))

    def arm_key(t, side, ax, out=0.0):
        """Tay side ('R' gần máy khi Lumo nhìn +X, 'L' xa) xoay ax quanh vai (âm = ra trước), out = dang sang bên."""
        arm = L.arm_r if side == "R" else L.arm_l
        ay = out if side == "R" else -out
        e = Euler((math.radians(ax), math.radians(ay), 0.0))
        rot(arm, [(t, (ax, ay, 0))])
        inv = e.to_matrix().inverted().to_euler("XYZ")
        key(hands[side], "rotation_euler", t, inv)

    def arms(t, r, l=None, out_r=0.0, out_l=0.0):
        arm_key(t, "R", r, out_r)
        arm_key(t, "L", r if l is None else l, out_l)

    def reach(t, side, p, extra=(0.0, 0.0)):
        """Xoay tay side để bàn tay chạm điểm p (thế giới) theo tư thế hiện tại của lumo (gọi sau go/pose ở t)."""
        sh = Vector((-0.2 if side == "R" else 0.2, 0.0, 0.55))
        M = lumo.matrix()
        d = (M.to_3x3().inverted() @ (Vector(p) - M @ sh)).normalized()
        ax = math.degrees(math.asin(max(-1, min(1, d.y))))
        ay = math.degrees(math.atan2(-d.x, -d.z))
        arm = L.arm_r if side == "R" else L.arm_l
        e = Euler((math.radians(ax + extra[0]), math.radians(ay + extra[1]), 0.0))
        rot(arm, [(t, (ax + extra[0], ay + extra[1], 0))])
        key(hands[side], "rotation_euler", t, e.to_matrix().inverted().to_euler("XYZ"))

    def make_compass(name, parent, tilt=COMPASS_TILT):
        root = empty(name, "PROPS", parent=parent, loc=CPOS)
        root.rotation_euler = tuple(math.radians(a) for a in tilt)
        add_obj(name + "_Case", cyl_bm(0.085, 0.03, (0, 0, 0), segs=28), gold_m, "PROPS", parent=root)
        add_obj(name + "_Bow", cyl_bm(0.018, 0.012, (0, 0.095, 0), axis="Y", segs=12), gold_m, "PROPS", parent=root)
        add_obj(name + "_Face", cyl_bm(0.07, 0.006, (0, 0, 0.014), segs=28), cface_m, "PROPS", parent=root)
        needle = empty(name + "_Needle", "PROPS", parent=root, loc=(0, 0, 0.02))
        add_obj(name + "_Points", poly_bm(star_pts([0.0] + [0.04] * 7, 0.012), 0.0, 0.006), needle_m, "PROPS", parent=needle)
        bm = poly_bm([(-0.012, 0.0), (0.012, 0.0), (0.0, 0.078)], 0.002, 0.01)          # đầu chỉ: cánh dài, sẫm
        bm = sphere_bm(0.009, (0, 0.07, 0.008), bm=bm, segs=8)
        add_obj(name + "_Pointer", bm, pointer_m, "PROPS", parent=needle)
        return root, needle

    compass_r, needle_r = make_compass("CompassR", hands["R"], COMPASS_TILT_R)
    compass_l, needle_l = make_compass("CompassL", hands["L"])

    def map_shapes(parent, tag):
        """Bản đồ giấy to cỡ đầu Lumo, mặt vẽ là +Z cục bộ; đúng chiều: trên = -Y, phải = -X (cục bộ). Mũi tên chỉ
        xuống, rương dưới mũi tên, bốn đảo như bản đồ khắc; mép phải để trống (biển mây). Hình vẽ nằm trọn trước mặt
        giấy, không ló ra mặt sau."""
        W, H = 0.36, 0.3
        add_obj(f"Map{tag}_Sheet", box_bm((W, H, 0.008)), prop, "PROPS", parent=parent)
        bm = box_bm((0.035, 0.08, 0.006), (0, -0.04, 0.007))         # thân mũi tên
        bm = poly_bm([(-0.05, 0.0), (0.05, 0.0), (0, 0.055)], 0.004, 0.01, bm=bm)   # đầu mũi tên chỉ xuống (+Y)
        bm = box_bm((0.1, 0.034, 0.006), (0, 0.127, 0.007), bm=bm)   # rương: thân chữ nhật, đáy phẳng ở phía dưới
        bm = poly_bm([(-0.05 + 0.1 * i / 8, 0.11 - 0.03 * math.sin(math.pi * i / 8)) for i in range(9)], 0.004, 0.01,
                     bm=bm)                                         # nắp vòm nhô hẳn lên một phía: lộn ngược là thấy
        bm = box_bm((0.016, 0.014, 0.006), (0, 0.105, 0.012), bm=bm)  # khoá giữa nắp và thân
        add_obj(f"Map{tag}_Marks", bm, prop_dark, "PROPS", parent=parent)
        bm = None
        for (u, v), (sx, sy) in zip(ISLANDS, ((1.5, 0.8), (1.2, 0.7), (1.35, 0.9), (1.1, 0.65))):
            bm = sphere_bm(0.028, (-u * W, -v * H, 0.006), (sx, sy, 0.12), bm=bm, segs=12)
        add_obj(f"Map{tag}_Islands", bm, island_m, "PROPS", parent=parent)

    map_hold = empty("Lumo_MapHold", "PROPS", parent=L.root)       # bản đồ hai tay cầm (trước ngực, trên mặt bệ)
    map_spin = empty("Lumo_MapSpin", "PROPS", parent=map_hold)     # quay quanh pháp tuyến: 0 đúng chiều, 180 cầm ngược
    map_shapes(map_spin, "")
    paw_rig = empty("Lumo_MapPawRig", "PROPS", parent=map_hold)   # xoay theo tấm giấy từng nấc, rồi xoay về khi đổi tay cầm
    PAW_EDGE = 0.19                                                 # bàn tay sát hai mép bên tấm giấy (chỉ ở cú nhìn S21), cách vai
    turn_paws = [add_obj(f"Lumo_MapPaw{s:+d}", box_bm((0.08, 0.1, 0.05), (s * PAW_EDGE, 0.12, 0.02)), lumo_m, "CAST",
                         parent=paw_rig) for s in (-1, 1)]         # ≤ 0.25 m; rương giữa mép dưới, góc mây trống không bị che
    map_far = empty("Lumo_MapFar", "PROPS", parent=hands["L"], loc=(0.0, -0.05, -0.02))   # bản đồ ở tay xa: dựng đứng, mặt ra trước
    map_far.rotation_euler = (math.radians(90), 0, 0)
    map_far_spin = empty("Lumo_MapFarSpin", "PROPS", parent=map_far)
    map_far_spin.rotation_euler = (0, 0, math.radians(180))
    map_shapes(map_far_spin, "Far")

    B = build_bird((POSTS[1] + 0.8, -RAIL_Y, 1.3), bird_m)
    moss_bits = [add_obj(f"MossBit{i}", box_bm((0.06, 0.04, 0.012)), moss_m, "PROPS") for i in range(6)]

    def show(ob, t, on, s=1.0):
        key(ob, "scale", t - HOLD, Vector((s, s, s)) if not on else Vector((0, 0, 0)))
        key(ob, "scale", t, Vector((s, s, s)) if on else Vector((0, 0, 0)))

    for ob in (compass_r, compass_l, map_hold, map_far, B.root, flash, *moss_bits, *halves, rails["near", "droop"],
               rails["far", "droop"], *turn_paws):
        key(ob, "scale", -1.0, Vector((0, 0, 0)))                   # ẩn bằng scale 0 tới lúc xuất hiện
    for ob in (planks[FALL[0]], *(rails[side, k] for side in ("near", "far") for k in range(1, 8)), L.head, L.arm_r, L.arm_l):
        key(ob, "scale", -1.0, Vector((1, 1, 1)))

    def head(t, pitch=0.0, yaw=0.0, roll=0.0):
        rot(L.head, [(t, (pitch, roll, yaw))])

    def look(t, p, dp=0.0):
        pitch, yaw = lumo.look_angles(p)
        head(t, pitch + dp, yaw)

    def ears(t, a):
        for ear, side in L.ears:
            rot(ear, [(t, (a, 0, 0))])

    def tail(t, up, side=0.0):
        rot(L.tail, [(t, (up, 0, side))])

    def squash(t, sx, sz):
        key(L.root, "scale", t, Vector((sx, sx, sz)))

    def legs(t, a=0.0):
        for lg in L.legs:
            rot(lg, [(t, (a, 0, 0))])

    def steps(lgs, t0, t1, n, amp=25):
        """Bước chân: hai chân đánh ngược nhau, đầu và cuối về 0 (không để key lệch kéo chân dạng ra từ trước)."""
        for i in range(n + 1):
            t = t0 + (t1 - t0) * i / n
            a = 0 if i in (0, n) else amp * (1 if i % 2 else -1)
            rot(lgs[0], [(t, (a, 0, 0))])
            rot(lgs[1], [(t, (-a, 0, 0))])

    def jitter(ob, t0, t1, amp, period=0.05, base=None):
        base = Vector(ob.location) if base is None else Vector(base)
        t, i = t0, 0
        while t < t1:
            key(ob, "location", t, base + Vector((amp * (1 if i % 2 else -1), 0, amp * (0.5 if i % 3 else -0.5))))
            t, i = t + period, i + 1
        key(ob, "location", t1, base)

    def bag_beep(t, amp=0.006, dur=0.25):
        key(bag, "location", t - 0.02, BAG)
        jitter(bag, t, t + dur, amp, 0.045, BAG)

    def glow(t, s):
        emit_key(cface_m, t, s)

    glow(-1.0, 0.6)                                                 # la bàn sáng le lói

    # ============================================================ S1: cửa mở hẳn, mây tắt dần; Lumo loạng choạng ra bậc cửa
    rot(door, [(0.0, (0, 0, -52)), (tm.DOOR_OPEN[0] + 0.25, (0, 0, -72)), (tm.DOOR_OPEN[1], (0, 0, -100))])   # đã hé đủ rộng: Lumo không xuyên cánh cửa
    emit_key(cloud_m, -1.0, 3.0)
    emit_key(cloud_m, tm.CLOUDS_FADE[0], 3.0)
    emit_key(cloud_m, (tm.CLOUDS_FADE[0] + tm.CLOUDS_FADE[1]) / 2, 0.8)
    emit_key(cloud_m, tm.CLOUDS_FADE[1], 0.0)
    lumo.go(0.0, DOOR_X, 0.0, 1.42)
    lumo.pose(0.0, lean=14, yaw=10)                                 # đang đẩy cửa hết sức
    arms(0.0, -95, -100)
    ears(0.0, -30)
    tail(0.0, 20)
    head(0.0, 10)
    s0, s1 = tm.LUMO_STUMBLE
    lumo.go(s0, DOOR_X, 0.0, 1.42)
    lumo.pose(s0, lean=14)
    lumo.go(s0 + 0.25, -0.66, 0.05, 1.05)                           # hụt tay, chúi tới
    lumo.pose(s0 + 0.25, lean=26)
    lumo.go(s0 + 0.5, -0.56, 0.0, 0.78)
    lumo.pose(s0 + 0.6, lean=-12, yaw=20)                           # bật ngửa lại giữ thăng bằng
    lumo.go(s0 + 0.75, -0.48, 0.04, 0.58)
    lumo.go(s1, -0.42, 0.0, 0.45)
    lumo.pose(s1, lean=0, yaw=35)
    legs(s0, 0)
    steps(L.legs, s0, s1, 6, 30)
    for i, t in enumerate([s0 + 0.1 + 0.12 * k for k in range(8)]):    # tay quơ giữ thăng bằng
        arms(t, -140 if i % 2 else -70, -70 if i % 2 else -140, 20, 20)
    arms(s1, -10, -5)
    ears(s0 + 0.1, 20)
    ears(s1, 2)
    tail(s0, 20)
    tail(s0 + 0.3, 55)
    tail(s1, 25)
    head(s0 + 0.1, -10)
    head(s1, 0)
    wo = tm.LUMO_WOW                                                # thấy cây cầu: tròn mắt, dựng tai
    lumo.pose(wo - 0.45, yaw=35)
    lumo.pose(wo - 0.1, yaw=RIGHT)
    head(wo - 0.1, 0)
    head(wo, -6)
    ears(wo - 0.05, 2)
    ears(wo + 0.12, 18)
    ears(wo + 0.3, 8)
    squash(0.0, 1, 1)
    squash(wo, 1, 1)
    squash(wo + 0.12, 0.96, 1.05)
    squash(wo + 0.3, 1, 1)
    wag(L.tail, wo, 9.0, 0.7, 16, base=(28, 0, 0))

    # ============================================================ S2: toàn cảnh; mắt đi dọc cây cầu sang bệ đá
    a0, a1 = tm.LOOK_ACROSS
    look(a0 - 0.3, (1.3, 0.0, 0.0))                                 # mặt cầu ngay trước chân
    look(a0, (1.3, 0.0, 0.0))
    look(a0 + 0.8, (3.4, 0.0, 0.1))
    look(a1, STAR_AT)                                               # tới bệ đá bên kia
    lumo.pose(a1, yaw=RIGHT)
    lumo.pose(a1 + 0.3, yaw=80)

    # ============================================================ S3: túi da rung, TÍT… TÍT…; rút la bàn
    for t in tm.BEEPS_BAG:
        bag_beep(t)
    b0 = tm.BEEPS_BAG[0]
    ears(b0, 8)
    ears(b0 + 0.1, 24)                                              # tai giật lên khi nghe TÍT
    ears(b0 + 0.3, 6)
    look(b0 + 0.05, STAR_AT)
    head(b0 + 0.3, 22, -35)                                         # liếc xuống túi bên hông phải
    c0, c1 = tm.COMPASS_OUT
    CHEST = -72
    arms(c0 - 0.2, -10, -5)
    arm_key(c0 + 0.1, "R", -14)                                     # tay vào miệng túi
    key(compass_r, "location", c0 + 0.15, Vector((0, -0.04, 0.06)))
    show(compass_r, c0 + 0.15, True, 0.4)                           # la bàn ló ra ở miệng túi (túi giữ nguyên)…
    key(compass_r, "location", c1, Vector(CPOS))
    key(compass_r, "scale", c1, Vector((1, 1, 1)))                  # …kéo lên ngang ngực
    arm_key(c1, "R", CHEST)
    head(c1, 18, -10)                                               # nhìn la bàn
    ears(c1, -12)

    # ============================================================ S4: cận la bàn (cú nhìn): mũi sao chỉ ngôi sao đá
    arm_key(S["S4"][0] - 0.2, "R", CHEST)
    arm_key(S["S4"][0], "R", -95, 30)                               # nâng la bàn lên trước mắt (dưới cằm), lệch ra phía tay cầm
    arm_key(S["S4"][1], "R", -95, 30)                               # giữ tới hết cú (không trôi xuống khỏi khung)
    jitter(compass_r, S["S4"][0], S["S4"][1], 0.0015, 0.07, CPOS)   # rung khẽ: còn cách cả khe

    # ============================================================ S5: dựng tai, chìa la bàn; "Ngay phía trước!"; lấy đà
    p0, p1 = tm.POSE
    ears(p0 - 0.25, -12)
    ears(p0, -30)
    ears(p0 + 0.15, 16)                                             # bật dựng thẳng hai tai
    ears(p1, 2)
    arm_key(p0, "R", -50, 15)
    arm_key(p0 + 0.25, "R", -50, 45)                                # chìa la bàn ra trước ngang ngực, lệch ra cạnh người
    lumo.pose(p0, lean=-3, yaw=80)
    lumo.pose(p0 + 0.25, lean=-6)
    squash(p0, 1, 1)
    squash(p0 + 0.12, 1.08, 0.92)                                   # nhún mạnh
    squash(p0 + 0.25, 0.95, 1.06)
    squash(p1, 1, 1)
    look(p0 + 0.15, STAR_AT)                                        # mắt dán vào bệ đá bên kia
    l0, l1 = tm.LINE_AHEAD
    arm_key(l0 + 0.3, "R", -50, 45)
    arm_key(l0 + 0.5, "R", -50, 45)                                 # la bàn giữ ngang ngực, cạnh người, không đưa lên trước mõm
    lumo.pose(l0 + 0.3, lean=-6)
    lumo.pose(l0 + 0.55, lean=7)                                    # "ngay phía trước": cả thân đẩy tới
    tail(l1, 30)
    r0, r1 = tm.RUSH
    STAND_X = 1.2                                                   # chỗ Lumo khựng lại trên cầu (tấm ván 1)
    squash(r0, 1, 1)
    squash(r0 + 0.15, 1.08, 0.9)                                    # lấy đà
    squash(r0 + 0.3, 0.97, 1.04)
    squash(r0 + 0.45, 1, 1)
    lumo.pose(r0, lean=2)
    lumo.pose(r0 + 0.15, lean=12)
    lumo.pose(r0 + 0.35, lean=16, yaw=88)                           # lao tới
    ears(r0 + 0.2, -25)                                             # tai bạt ra sau
    arms(r0 + 0.2, -60, 20)
    lumo.go(r0, -0.42, 0.0, 0.45)
    lumo.go(r0 + 0.2, -0.42, 0.0, 0.45)
    for i in range(1, 6):
        u = i / 5
        lumo.go(r0 + 0.2 + (r1 - r0 - 0.2) * u, -0.42 + (STAND_X + 0.42) * u, 0.06 if i % 2 else 0.0, 0.45 * (1 - u))
    steps(L.legs, r0 + 0.2, r1, 5, 35)
    for i, t in enumerate([r0 + 0.3 + 0.18 * k for k in range(4)]):
        arm_key(t, "L", 30 if i % 2 else -40)
    lumo.pose(r1, yaw=90)
    look(r0 + 0.1, STAR_AT)
    wag(L.tail, r0, r1, 0.25, 20, base=(40, 0, 0))

    # ============================================================ S6: CREAAAAK, chờ sỏi, "Không sao…", mắt vẫn ngước mà bước tiếp
    creak = planks[CREAK_PLANK]
    rot(creak, [(tm.CREAK - 0.02, (0, 0, 0)), (tm.CREAK + 0.08, (0, -40, 0)), (tm.CREAK + 0.3, (0, -4, 0)),
                (tm.CREAK + 0.42, (0, -14, 0)), (tm.CREAK + 0.6, (0, -3, 0)), (tm.CREAK + 0.8, (0, 0, 0))])   # tấm ván bật lên
    ck = tm.CREAK
    lumo.go(ck, STAND_X)
    lumo.go(ck + 0.1, STAND_X - 0.03, 0.03)                         # khựng lại
    lumo.go(ck + 0.25, STAND_X - 0.03)
    lumo.pose(ck, lean=14)
    lumo.pose(ck + 0.1, lean=-10)
    lumo.pose(ck + 0.3, lean=-2)
    ears(ck + 0.03, 25)
    arms(ck + 0.05, -75, -60)
    arms(ck + 0.4, -45, -20)
    tail(ck, 30)
    tail(ck + 0.1, 65)                                              # đuôi dựng đứng
    look(ck + 0.1, (PLANKS[CREAK_PLANK] + 0.1, 0.0, 0.1))           # nhìn tấm ván
    w0, w1 = tm.WAIT_PEBBLE
    ears(w0, 10)
    ears(w0 + 0.15, -55)                                            # cụp tai
    head(w0, 30)
    head(w0 + 0.2, -40)                                             # ngước nhìn trời, chờ hòn sỏi
    squash(w0, 1, 1)
    squash(w0 + 0.2, 1.05, 0.94)                                    # rụt cổ
    tail(w0 + 0.2, 10)
    arms(w0 + 0.2, -22, -15)
    head(w1, -40)
    np_ = tm.NO_PEBBLE                                              # không có sỏi: thở phào
    ears(np_, -55)
    ears(np_ + 0.2, 6)
    squash(np_, 1.05, 0.94)
    squash(np_ + 0.25, 0.98, 1.03)
    squash(np_ + 0.45, 1, 1)
    tail(np_ + 0.2, 28)
    head(np_ + 0.2, -32)
    e0, e1 = tm.LINE_OLD                                            # "Không sao. Một chiếc cầu hơi cũ thôi.": vẫn ngước trời
    arm_key(e0, "R", -22)
    arm_key(e0 + 0.3, "R", -60)
    arm_key(e0 + 0.6, "R", -30)                                     # phẩy tay cầm la bàn: không sao
    for t, a in ((e0, -32), (e0 + 0.9, -26), (e0 + 1.3, -34), (e1 - 0.4, -28)):
        head(t, a)
    wag(L.tail, e0, e1, 0.6, 14, base=(26, 0, 0))
    st0, st1 = tm.STEP_ON
    head(st0, -36)                                                  # vẫn ngước trời
    lumo.pose(st0, lean=-2)
    lumo.pose(st0 + 0.3, lean=-6)
    STEP_X = STAND_X + 0.2                                          # mũi chân ở tấm ván 3; tấm 4 ngay trước mũi chân
    lumo.go(st0, STAND_X - 0.03)
    lumo.go(st0 + 0.35, STAND_X + 0.08, 0.07)                       # nhấc chân thong thả
    lumo.go(st1 - 0.1, STEP_X, 0.0)
    steps(L.legs, st0, st1 - 0.1, 2, 30)
    arms(st0, -30, -15)
    arms(st0 + 0.4, -40, 10)

    # ============================================================ S7, S8: CRACK, dãy ván rơi xuống lưới; chới với, túm dây leo, ngã ngồi
    swap = S["S7"][0]                                               # la bàn sang tay xa để tay gần túm dây leo
    arm_key(swap - 0.3, "L", -40)
    show(compass_r, swap, False)
    show(compass_l, swap, True)
    cr = tm.CRACK
    show(planks[FALL[0]], cr, False)                                # tấm ván trước mũi chân gãy làm hai
    for k, h in enumerate(halves):
        sd = -1 if k == 0 else 1
        x0 = PLANKS[FALL[0]] + PLANK_W / 2
        y0 = (k - 0.5) * DECK
        show(h, cr, True)
        key(h, "location", cr, Vector((x0, y0, 0.0)))
        rot(h, [(cr, (0, 0, 0)), (cr + 0.12, (sd * 25, 30, 0))])
        for t, z, a in ((cr + 0.25, -0.25, 70), (cr + 0.5, net_base(x0) + 0.03, 150), (cr + 0.65, net_base(x0) + 0.1, 160),
                        (cr + 0.85, net_base(x0) + 0.03, 170)):
            key(h, "location", t, Vector((x0 + 0.06, y0 + sd * 0.08, z)))
            rot(h, [(t, (sd * 40, a, 0))])
    for n, i in enumerate(FALL[1:]):
        t0 = cr + 0.05 + 0.045 * n                                  # kéo theo cả dãy, từ gần tới xa
        x0 = PLANKS[i]
        xc = x0 + PLANK_W / 2
        a = random.choice((-1, 1)) * random.uniform(15, 55)
        b = random.uniform(-25, 25)
        zn = net_base(xc)
        rot(planks[i], [(t0, (0, 0, 0))])
        for t, dz, dx in ((t0, 0.0, 0.0), (t0 + 0.2, -0.22, 0.01), (t0 + 0.42, zn + 0.04, 0.02), (t0 + 0.58, zn + 0.12, 0.02),
                          (t0 + 0.78, zn + 0.02, 0.02), (t0 + 0.95, zn + 0.07, 0.02), (t0 + 1.15, zn + 0.03, 0.02)):
            key(planks[i], "location", t, Vector((x0 + dx, 0.0, dz)))
        rot(planks[i], [(t0 + 0.42, (b, a, 0)), (t0 + 1.15, (b * 0.6, a * 0.6, 0))])
    for side in ("near", "far"):
        for n, k in enumerate(FALL_POSTS):
            t0 = cr + 0.08 + 0.13 * n
            x = POSTS[k]
            y = -RAIL_Y if side == "near" else RAIL_Y
            zn = net_base(x)
            rot(posts[side, k], [(t0, (0, 0, 0)), (t0 + 0.45, (0, 75 if n % 2 else -80, 0))])
            for t, z in ((t0, 0.0), (t0 + 0.45, zn + 0.06), (t0 + 0.65, zn + 0.13), (t0 + 0.85, zn + 0.06)):
                key(posts[side, k], "location", t, Vector((x + (0.15 if t > t0 else 0.0), y, z)))
        for k in range(1, 8):
            show(rails[side, k], cr + 0.25, False)
        show(rails[side, "droop"], cr + 0.25, True)
    sk = net.data.shape_keys.key_blocks["Sag"]
    for t, s in ((cr + 0.3, 0.0), (cr + 0.55, 1.0), (cr + 0.8, -0.4), (cr + 1.05, 0.6), (cr + 1.3, -0.15), (cr + 1.6, 0.25),
                 (cr + 2.0, 0.0)):
        sk.value = s
        sk.keyframe_insert("value", frame=fr(t))                     # lưới võng xuống đỡ ván, nảy bập bềnh
    # Lumo: mắt giật xuống, chới với ở mép khoảng trống
    head(cr + 0.02, 30)
    ears(cr + 0.02, 28)
    tail(cr, 30)
    tail(cr + 0.08, 65)
    lumo.go(cr, STEP_X)
    lumo.pose(cr, lean=-4)
    lumo.pose(cr + 0.15, lean=16)                                   # chúi về phía khoảng trống
    f0, f1 = tm.FLAIL
    t, i = f0, 0
    while t < f1 - 0.1:
        arms(t, -145 if i % 2 else -80, -85 if i % 2 else -145, 15, 15)   # hai tay quay tít, không quá ngang tai
        lumo.pose(t, lean=16 if i % 2 else 6, roll=5 if i % 2 else -5)
        ears(t, 30 if i % 2 else 10)
        t, i = t + 0.13, i + 1
    wag(L.tail, f0, f1, 0.13, 25, base=(55, 0, 0))
    GX = STEP_X - 0.04
    lumo.go(f1 - 0.3, GX, 0.02)
    lumo.pose(f1 - 0.1, roll=0)
    ROPE = Vector((0.5 * (POSTS[0] + POSTS[1]), -RAIL_Y, RAIL_Z - 0.02))   # dây leo ở thành cầu sát cửa, phía máy
    g0, g1 = tm.GRAB
    lumo.go(g0 - 0.12, GX)
    arm_key(g0 - 0.12, "R", 30, 50)                                 # tay gần vung ra sau
    for t, ln in ((g0, 10), (g0 + 0.2, 2), (g0 + 0.4, -6), (g1, -10)):  # túm dây leo, kéo người ngả về phía cửa
        lumo.pose(t, lean=ln)
        lumo.go(t, GX)
        reach(t, "R", ROPE)
    arm_key(g0, "L", -110)
    arm_key(g1, "L", -75)
    head(g0, 10)
    head(g1, 0)
    arm_key(g1 + 0.1, "R", -70)                                     # buông dây, loạng choạng lùi
    lumo.go(g1 + 0.15, GX - 0.2, 0.03, 0.05)
    lumo.go(g1 + 0.35, 0.62, 0.04, 0.1)
    lumo.go(g1 + 0.48, 0.2, 0.0, 0.14)
    lumo.pose(g1 + 0.2, lean=-20)
    lumo.pose(g1 + 0.45, lean=-26)
    ears(g1 + 0.2, 20)
    legs(tm.PHICH - 0.1, 0)
    lumo.go(tm.PHICH - 0.08, -0.02, 0.0, 0.15)
    ph = tm.PHICH
    lumo.go(ph, -0.15, SIT_Z, 0.15)                                 # ngã ngồi trên đệm rêu: PHỊCH
    lumo.pose(ph - 0.08, lean=-30)
    lumo.pose(ph, lean=-12)
    legs(ph, -85)                                                   # hai chân duỗi ra trước
    squash(ph - 0.02, 1, 1)
    squash(ph + 0.05, 1.12, 0.86)
    squash(ph + 0.2, 0.96, 1.05)
    squash(ph + 0.4, 1, 1)
    lumo.pose(ph + 0.35, lean=-8)
    arms(ph - 0.05, -110, -10, 0, 30)
    arms(ph + 0.1, -125, -5, 0, 35)                                 # tay gần hất lên theo cú dội; tay xa cầm la bàn chống xuống đệm
    arms(ph + 0.45, -35, -5, 0, 25)                                 # rêu bên hông (la bàn thấp, không nằm sau mõm trên màn hình)
    tail(ph - 0.1, 40)
    tail(ph, -5)                                                    # đáp lên cái đuôi bông, đuôi bẹp trên đệm rêu
    key(L.tail, "scale", ph - 0.02, Vector((1, 1, 1)))
    key(L.tail, "scale", ph + 0.05, Vector((1.35, 1.0, 0.6)))
    key(L.tail, "scale", ph + 0.25, Vector((0.92, 1.0, 1.12)))
    key(L.tail, "scale", ph + 0.45, Vector((1, 1, 1)))
    tail(ph + 0.5, 12)
    ears(ph, 30)
    ears(ph + 0.15, -40)
    ears(ph + 0.4, -20)
    head(ph, 10)
    for k, ob in enumerate(moss_bits):                              # rêu bật lên quanh chỗ ngồi
        p0v = Vector((-0.4 + 0.1 * k, 0.1 + 0.06 * (k % 3), 0.04))
        p1v = Vector((-0.75 + 0.24 * k, -0.15 - 0.05 * (k % 2), 0.02))
        show(ob, ph + 0.02 * k, True)
        for q in range(5):
            u = q / 4
            key(ob, "location", ph + 0.02 * k + 0.6 * u, p0v.lerp(p1v, u) + Vector((0, 0, 0.25 * math.sin(math.pi * u))))
            rot(ob, [(ph + 0.02 * k + 0.6 * u, (0, 240 * u, 60 * u))])
        show(ob, ph + 0.7 + 0.02 * k, False)
    look(ph + 0.7, (1.8, 0.0, 0.3))                                 # ngơ ngác nhìn khoảng trống

    # ============================================================ S9, S10: chú chim đáp xuống cột cầu, cười; "Được rồi! Một chiếc cầu… rất cũ!"
    PERCH = Vector((POSTS[1], -RAIL_Y, POST_TOP + 0.005))
    BYAW = -75                                                      # nhìn về phía Lumo, hơi quay về phía máy
    bl0, bl1 = tm.BIRD_LAND
    show(B.root, bl0, True)
    for t, p in ((bl0, PERCH + Vector((0.8, 0.0, 0.75))), (bl0 + 0.25, PERCH + Vector((0.45, 0.0, 0.4))),
                 (bl0 + 0.5, PERCH + Vector((0.12, 0.0, 0.11))), (bl1, PERCH)):
        key(B.root, "location", t, p)
    rot(B.root, [(bl0, (0, 0, -90)), (bl1, (0, 0, BYAW))])
    t, i = bl0, 0
    while t < bl1 - 0.05:
        rot(B.wing, [(t, (0, 0, -70 if i % 2 else 10))])
        rot(B.wing_far, [(t, (0, 0, 70 if i % 2 else -10))])
        t, i = t + 0.06, i + 1
    rot(B.wing, [(bl1, (0, 0, 0))])
    rot(B.wing_far, [(bl1, (0, 0, 0))])
    keys(B.root, "scale", [(bl1, Vector((1.1, 1.1, 0.86))), (bl1 + 0.15, Vector((1, 1, 1)))])   # đáp xuống, nhún
    rot(B.head, [(tm.BIRD_LOOK - 0.2, (0, 0, 0)), (tm.BIRD_LOOK, (0, 25, 0))])   # nghiêng đầu nhìn Lumo

    def bird_laugh(c, big=True):
        rot(B.wing, [(c - 0.18, (-30, 0, 0)), (c, (-95, 0, -35)), (c + 0.1, (-60, 0, -20)), (c + 0.2, (-95, 0, -35)),
                     (c + 0.3, (-30, 0, 0) if big else (0, 0, 0))])
        if big:
            key(B.root, "location", c - 0.1, PERCH)
            key(B.root, "location", c + 0.05, PERCH + Vector((0, 0, 0.06)))
            key(B.root, "location", c + 0.25, PERCH)
            rot(B.root, [(c - 0.1, (0, 0, BYAW)), (c + 0.05, (-24, 0, BYAW)), (c + 0.25, (0, 0, BYAW))])   # cả thân ngửa ra sau rồi bật lại
            rot(B.head, [(c, (-20, 0, 0)), (c + 0.3, (6, 10, 0))])  # ngửa đầu cười

    for c in tm.CHIRPS:                                             # lấy cánh vỗ bụng: CHÍP CHÍP CHÍP!
        bird_laugh(c)
    rot(B.wing, [(tm.BIRD_LAUGH[1] + 0.2, (0, 0, 0))])
    for c in (35.2, 36.1, 39.6, 41.0, 42.3):                        # còn khúc khích trong lúc Lumo chống chế, nhìn quanh
        bird_laugh(c, False)
    bird_laugh(tm.BIRD_STOP - 0.5)                                  # đầu S13 còn cười một nhịp rồi mới thôi
    rot(B.head, [(tm.BIRD_STOP, (0, 0, 0)), (tm.BIRD_STOP + 0.25, (0, 28, 0))])   # thôi cười, nghiêng đầu
    # Lumo: nghe CHÍP, nhìn chú chim, ngượng; chống chế
    bl = tm.BIRD_LAUGH[0]
    look(bl + 0.1, PERCH)
    ears(bl + 0.8, -20)
    ears(bl + 1.1, -48)                                             # cụp tai ngượng
    tail(bl + 0.8, 0)
    v0, v1 = tm.LINE_VERY_OLD
    ears(v0 - 0.1, -48)
    ears(v0 + 0.15, 4)
    arms(v0, -35, -5, 0, 25)
    arms(v0 + 0.25, -25, -5, 60, 30)                                # xoè tay gần ra: chịu thua; tay xa cầm la bàn để thấp bên hông
    arms(v0 + 0.7, -40, -5, 0, 25)
    squash(v0, 1, 1)
    squash(v0 + 0.2, 1.03, 0.97)
    squash(v0 + 0.5, 1, 1)
    look(v0 + 0.8, (2.4, 0.0, -0.4))                                # liếc khoảng trống
    pv_, yv_ = lumo.look_angles((2.4, 0.0, -0.4))
    for t, a in ((v1 - 0.6, pv_ - 6), (v1 - 0.4, pv_ + 10), (v1 - 0.2, pv_ - 2), (v1, pv_ + 4)):
        head(t, a, yv_)                                             # gật mạnh ở "rất cũ!"
    ears(v1 - 0.45, 8)
    ears(v1 - 0.3, -25)
    ears(v1, -10)
    lc = tm.LOOK_COMPASS
    arms(lc - 0.2, -45, -45)                                        # chụm hai tay: la bàn về tay gần
    show(compass_l, lc - 0.05, False)
    show(compass_r, lc - 0.05, True)
    arms(lc + 0.3, -95, -25, 30)                                    # nâng la bàn lên nhìn (dưới cằm), lệch ra phía tay cầm
    arms(S["S11"][1], -95, -25, 30)                                 # giữ tới hết cú nhìn S11
    head(lc + 0.3, 20, -12)

    # ============================================================ S11: cận la bàn qua khoảng trống (cú nhìn): vẫn chỉ ngôi sao đá
    jitter(compass_r, S["S11"][0], S["S11"][1], 0.0015, 0.07, CPOS)

    # ============================================================ S12: đứng dậy, nhìn khoảng trống, vách đá, bụi cây; vạch bụi cây
    u0, u1 = tm.STAND_UP
    lumo.go(u0, -0.15, SIT_Z, 0.15)
    lumo.go(u0 + 0.25, -0.15, SIT_Z + 0.12, 0.15)
    lumo.go(u1, -0.15, 0.0, 0.15)
    lumo.pose(u0, lean=-8)
    lumo.pose(u0 + 0.2, lean=16)
    lumo.pose(u1, lean=0)
    legs(u0, -85)
    legs(u1, 0)
    arms(u0, -75, -30)
    arms(u1, -50, -10)
    tail(u1, 22)
    for (t0, t1), p, ea, by in ((tm.LOOK_GAP, (2.6, 0.0, -0.6), 6, 88), (tm.LOOK_WALL, (1.6, 1.6, 2.1), 12, 115),
                                (tm.LOOK_BUSH, (0.45, 1.1, 0.4), 14, 132)):
        lumo.pose(t0 - 0.05, yaw=lumo.yaw)
        lumo.pose(t0 + 0.2, yaw=by)                                 # quay cả thân về thứ đang nhìn, giữ tới hết nhịp
        look(t0 + 0.2, p)
        look(t1, p)
        ears(t0 + 0.1, ea - 12)
        ears(t0 + 0.25, ea + 10)                                    # mỗi lần nhìn một nhịp tai
        ears(t1, ea)
    q0 = tm.TO_BUSH[0]
    BUSH_X, BUSH_Y = -0.5, 1.15                                     # đứng sát bên trái bụi cây, quay mặt sang bụi cây
    lumo.go(q0, -0.15, 0.0, 0.15)
    lumo.go(tm.TO_BUSH[1], BUSH_X, 0.0, BUSH_Y)
    lumo.pose(q0, yaw=90)
    lumo.pose(tm.TO_BUSH[1], yaw=90)
    steps(L.legs, q0, tm.TO_BUSH[1], 3, 28)
    look(tm.TO_BUSH[1], (0.6, 1.2, 0.4))
    q0, q1 = tm.PART_BUSH
    arms(q0, -90, -95)                                              # đưa hai tay vào bụi cây
    arms(q0 + 0.3, -100, -100)
    arms(q1, -95, -95, 40, 40)                                      # vạch ra hai bên
    lumo.pose(q0, lean=4)
    lumo.pose(q1, lean=8)
    for pv, a in zip(bush, (34, -22)):                              # nửa ngoài ngả ra khe, nửa trong ngả vào vách: lối hở giữa
        rot(pv, [(q0 + 0.2, (0, 0, 0)), (q1, (a, 0, 0)), (q1 + 0.15, (a * 1.08, 0, 0)), (q1 + 0.3, (a, 0, 0))])
        keys(pv, "scale", [(q0 + 0.2, Vector((1, 1, 1))), (q1, Vector((1, 1, 0.72)))])   # bị ép thấp xuống, không trùm lên cột cầu
    ears(q1, 4)
    ears(q1 + 0.12, 20)                                             # những bậc đá rộng hiện ra
    ears(q1 + 0.3, 8)
    look(q1 + 0.05, (1.2, 1.3, 0.6))
    arms(q1 + 0.5, -60, -50)
    lumo.pose(q1 + 0.5, lean=0)
    wag(L.tail, q1, tm.LINE_LOOK[0], 0.6, 14, base=(28, 0, 0))

    # ============================================================ S14: "Nhìn kỹ trước đã."
    k0, k1 = tm.LINE_LOOK
    lumo.pose(S["S14"][0], yaw=90)
    lumo.pose(k0 - 0.1, yaw=68)                                     # quay ba phần tư về phía máy, nhìn lối bậc đá
    look(k0 - 0.1, (1.0, 0.3, 0.6))                                 # nhìn bậc đá dưới, chú chim ở cột cầu bên cạnh
    pk, yk = lumo.look_angles((1.0, 0.3, 0.6))
    head(k1 - 0.3, pk + 10, yk)                                     # gật nhẹ
    head(k1, pk, yk)
    ears(k0 - 0.2, 0)

    # ============================================================ S15: cất la bàn, bám tay vịn, đi chậm từng bậc; chim bắt chước
    m0, m1 = tm.STOW_COMPASS
    lumo.pose(m0, yaw=68)
    arm_key(m0, "R", -45)
    arm_key(m0 + 0.3, "R", -14)                                     # tay xuống túi
    key(compass_r, "location", m0 + 0.05, Vector(CPOS))
    key(compass_r, "location", m0 + 0.3, Vector((0, -0.04, 0.06)))
    key(compass_r, "scale", m0 + 0.3, Vector((0.5, 0.5, 0.5)))
    show(compass_r, m0 + 0.32, False, 0.5)
    arm_key(m1, "R", 6)
    look(m0, (BUSH_X, BUSH_Y - 0.2, 0.0))
    gr0, gr1 = tm.GRAB_RAIL
    lumo.go(gr0, BUSH_X, 0.0, BUSH_Y)
    arm_key(gr0, "L", -30)
    lumo.go(gr1, BUSH_X + 0.08, 0.0, PATH_Y)
    lumo.pose(gr1, yaw=90)
    reach(gr1, "L", (BUSH_X + 0.3, HRAIL_Y, 0.46))                  # tay xa đặt lên tay vịn dây leo (ngang ngực)
    look(gr1, (0.6, PATH_Y, 0.2))
    lumo_steps = []                                                 # (nhấc chân, đặt chân, x, z): chú chim bắt chước theo
    xp, zp = BUSH_X + 0.08, 0.0

    def lumo_step(t0, t1, x, z, lift=0.025, rail=True):
        nonlocal xp, zp
        lumo.go(t0, xp, zp, PATH_Y)
        lumo.go((t0 + t1) / 2, (xp + x) / 2, max(zp, z) + lift, PATH_Y)   # nhấc chân chậm
        lumo.go(t1, x, z, PATH_Y)
        lumo.pose(t0, lean=2)
        lumo.pose((t0 + t1) / 2, lean=5)
        lumo.pose(t1, lean=2)
        sgn = 1 if len(lumo_steps) % 2 else -1                     # hai chân đánh ngược nhau, đổi chân mỗi bước
        for lg, a in zip(L.legs, (sgn * 16, -sgn * 10)):
            rot(lg, [(t0, (0, 0, 0)), ((t0 + t1) / 2, (a, 0, 0)), (t1, (0, 0, 0))])
        if rail:
            reach(t1, "L", (x + 0.25, HRAIL_Y, path_z(x + 0.25) + 0.46))
        lumo_steps.append((t0, t1, x, z))
        xp, zp = x, z

    step_t = (tm.CLIMB[1] - tm.CLIMB[0]) / 5
    for k in range(1, 6):
        t = tm.CLIMB[0] + step_t * (k - 1)
        lumo_step(t, t + 0.4, 0.3 * k, 0.15 * k)
    for i, t in enumerate([tm.CLIMB[0] + 0.35 * k for k in range(int((tm.CLIMB[1] - tm.CLIMB[0]) / 0.35) + 1)]):
        head(t, 18 if i % 2 else 12, 0)                             # nhìn chân bước
    wag(L.tail, tm.CLIMB[0], tm.CLIMB[1], 0.7, 12, base=(24, 0, 0))

    # ============================================================ S17: men vách, vòng qua đầu khe; la bàn trong túi kêu dày dần
    pw0, pw1 = tm.PATH_WALK
    W0 = 3.3                                                        # cắt cảnh: đã đi được hơn nửa gờ
    walk = [(W0 + 0.3 * k, LEDGE_Z) for k in range(1, 5)] + [(LEDGE_END + 0.15 + 0.3 * k, LEDGE_Z - 0.15 * (k + 1)) for k in range(3)]
    period = (pw1 - pw0) / len(walk)
    lumo.go(pw0 - HOLD, xp, zp, PATH_Y)
    lumo.go(pw0, W0, LEDGE_Z, PATH_Y)
    reach(pw0, "L", (W0 + 0.25, HRAIL_Y, LEDGE_Z + 0.46))
    xp, zp = W0, LEDGE_Z
    for i, (x, z) in enumerate(walk):
        t0 = pw0 + 0.05 + i * period
        lumo_step(t0, t0 + 0.6 * period, x, z, 0.02)
    head(pw0, 10, 0)
    wag(L.tail, pw0, pw1, 0.6, 14, base=(26, 0, 0))
    for k, tb in enumerate(tm.BEEPS_PATH):                          # rung mạnh dần, kêu dày dần
        bag_beep(tb, 0.004 + 0.0015 * k, 0.15)
    bp0 = tm.BEEPS_PATH[0]
    ears(bp0, 4)
    ears(bp0 + 0.1, 18)
    ears(bp0 + 0.3, 6)
    head(bp0 + 0.1, 22, -35)                                        # liếc túi
    head(bp0 + 0.7, 8, 0)                                           # rồi nhìn phía trước

    # ============================================================ S18: xuống bãi đất, tới bệ đá; S19: ấn ngôi sao, CẠCH, phiến đá trượt mở
    ar0, ar1 = tm.ARRIVE
    lumo.go(ar0 - HOLD, xp, zp, PATH_Y)
    down = [(ar0 + 0.3, 5.65, 0.3, 1.25), (ar0 + 0.6, 5.95, 0.15, 1.18), (ar0 + 0.9, 6.25, 0.0, 1.05)]   # từng bậc, 0.3 s một bậc
    xq, zq, yq = xp, zp, PATH_Y
    lumo.go(ar0, xq, zq, yq)
    for t, x, z, y in down:
        lumo.go(t - 0.15, (xq + x) / 2, max(zq, z) + 0.03, (yq + y) / 2)
        lumo.go(t, x, z, y)
        xq, zq, yq = x, z, y
    walk_to = [(ar0 + 1.15, 6.33, 0.72), (ar0 + 1.4, 6.42, 0.42), (ar1 - 0.05, LUMO_STAR[0], LUMO_STAR[1])]   # ba bước tới trước ngôi sao
    for t, x, y in walk_to:
        lumo.go(t - 0.12, (xq + x) / 2, 0.025, (yq + y) / 2)
        lumo.go(t, x, 0.0, y)
        xq, yq = x, y
    lumo.go(ar1, LUMO_STAR[0], 0.0, LUMO_STAR[1])
    turn = yaw_to((6.25, 1.05), LUMO_STAR)
    lumo.pose(ar0 + 0.6, yaw=90)
    lumo.pose(ar0 + 1.1, yaw=turn)                                  # quay một lần, chậm, về phía bệ
    lumo.pose(ar1 - 0.1, yaw=turn)
    lumo.pose(ar1 + 0.3, yaw=90, lean=0)                            # tới nơi mới quay vào mặt bệ
    steps(L.legs, ar0, ar1, 6, 22)
    arms(ar0, -20, -10)
    look(ar0 + 0.2, (6.1, 0.9, 0.0))                                # nhìn bậc dưới chân
    look(ar0 + 1.0, STAR_AT)
    for t in (58.1, 58.25):                                         # sát bệ: kêu dày, rung mạnh
        bag_beep(t, 0.014, 0.12)
    ps0, ps1 = tm.PRESS_STAR
    lumo.pose(ps0, lean=0)
    lumo.pose(ps0 + 0.3, lean=18)
    arm_key(ps0, "L", -20)
    reach(ps0 + 0.3, "L", STAR_AT + Vector((0, 0, 0.13)))            # với tay đặt lên ngôi sao
    reach(ps1, "L", STAR_AT + Vector((0, 0, 0.06)))                 # ấn xuống
    look(ps0, STAR_AT)
    cc = tm.CACH
    key(pstar, "location", cc - 0.05, STAR_AT)
    key(pstar, "location", cc, STAR_AT - Vector((0, 0, 0.07)))       # ngôi sao lún xuống: CẠCH
    ears(cc, 5)
    ears(cc + 0.1, 22)
    ears(cc + 0.3, 8)
    reach(cc + 0.35, "L", STAR_AT + Vector((0, 0, 0.045)))
    arm_key(cc + 0.6, "L", -40)
    lumo.pose(cc + 0.4, lean=4)
    sl0, sl1 = tm.SLAB_SLIDE
    key(cover, "location", sl0, Vector((0, 0, 0)))
    key(cover, "location", sl1, Vector((0, CMAP_U + 0.02, 0)))       # trượt về +Y, lút vào trong bệ
    look(sl0, CMAP)

    # ============================================================ S20: chú chim đậu lên mép bệ; Lumo rút bản đồ giấy
    BIRD_EDGE = Vector((px1 - 0.06, py0 + 0.06, PTOP))
    bp0, bp1 = tm.BIRD_PERCH
    rot(B.root, [(bp0, (0, 0, 90)), (bp1, (0, 0, -60))])            # đậu, quay về phía Lumo
    t, i = bp0 + 0.05, 0
    while t < bp1 - 0.05:
        rot(B.wing, [(t, (0, 0, -70 if i % 2 else 10))])
        rot(B.wing_far, [(t, (0, 0, 70 if i % 2 else -10))])
        t, i = t + 0.06, i + 1
    rot(B.wing, [(bp1, (0, 0, 0))])
    rot(B.wing_far, [(bp1, (0, 0, 0))])
    keys(B.root, "scale", [(bp1, Vector((1.1, 1.1, 0.86))), (bp1 + 0.15, Vector((1, 1, 1)))])
    rot(B.head, [(bp1 + 0.3, (0, 15, 0))])
    look(bp0 + 0.2, BIRD_EDGE)                                      # nhìn chú chim
    sd0 = bp0 + 0.1                                                 # bước sang trước bản đồ khắc (hai bước ngang)
    lumo.go(sd0, *LUMO_STAR[:1], 0.0, LUMO_STAR[1])
    lumo.go(sd0 + 0.15, LUMO_STAR[0], 0.025, 0.06)
    lumo.go(sd0 + 0.3, LUMO_STAR[0], 0.0, 0.0)
    lumo.go(sd0 + 0.45, LUMO_STAR[0], 0.025, -0.06)
    lumo.go(sd0 + 0.6, LUMO_PLINTH[0], 0.0, LUMO_PLINTH[1])
    steps(L.legs, sd0, sd0 + 0.6, 2, 14)
    n0, n1 = tm.MAP_OUT
    MAP_CHEST = ((0, -0.31, 0.42), (-72, 0, 0))                     # cầm ngang ngực, mặt vẽ quay về Lumo
    MAP_FLAT = ((0, -0.36, 0.47), (0, 0, 0))                        # đặt cạnh (ngay dưới) bản đồ khắc, cùng trục, nằm ngang
    MAP_BIG = 1.39                                                  # ở cú so, tấm giấy cùng cỡ bản đồ khắc (0.5 × 0.42): đảo khớp
                                                                    # theo cột; mép trên giấy chạm mép hốc, mép dưới trước bụng Lumo
    arm_key(n0, "R", -14)                                           # tay vào túi
    key(map_hold, "location", n0 + 0.2, BAG_TOP)
    rot(map_hold, [(n0 + 0.2, (-60, 0, 0))])
    show(map_hold, n0 + 0.2, True, 0.3)                             # ló ra ở miệng túi rồi kéo lên, mở ra
    rot(map_spin, [(n0 + 0.2, (0, 0, 180))])                        # lại cầm ngược: rương lộn ngược
    key(map_hold, "location", n1, Vector(MAP_CHEST[0]))
    rot(map_hold, [(n1, MAP_CHEST[1])])
    key(map_hold, "scale", n1, Vector((1, 1, 1)))
    arms(n1, -78, -78)
    look(n1, (6.86, -0.12, 0.42))
    head(n1 + 0.2, 24, 0)
    tf = S["S21"][0]
    key(map_hold, "location", tf - 0.4, Vector(MAP_CHEST[0]))
    rot(map_hold, [(tf - 0.4, MAP_CHEST[1])])
    key(map_hold, "location", tf - 0.05, Vector(MAP_FLAT[0]))       # hạ xuống đặt cạnh bản đồ khắc
    rot(map_hold, [(tf - 0.05, MAP_FLAT[1])])
    keys(map_spin, "scale", [(tf - 0.4, Vector((1, 1, 1))), (tf - 0.05, Vector((MAP_BIG,) * 3))])
    arms(tf - 0.4, -78, -78)
    arms(tf - 0.05, -88, -88)

    # ============================================================ S21: hai bản đồ (cú nhìn từ trên); xoay lại: khớp; đài thiên văn khắc lóe
    mt0, mt1 = tm.MAP_TURN
    t, i = tf, 0
    while t < mt0 - 0.2:                                            # nhích theo nhịp thở
        key(map_hold, "location", t, Vector(MAP_FLAT[0]) + Vector((0.004 if i % 2 else -0.004, 0, 0.005 if i % 2 else 0)))
        t, i = t + 0.45, i + 1
    # xoay lại cho đúng chiều: tấm giấy đang ở xa (cạnh bản đồ khắc), tay Lumo ngắn không xoay được ở đó, nên nhấc lên
    # sát trên ngực, nắm gần tâm, xoay ba nấc 60° (tay xoay theo giấy), giữa các nấc tay nhích về như đổi tay cầm, rồi
    # đặt lại cạnh bản đồ khắc (SEEDANCE.md, "Tay cầm vật phải đi theo vật"; mọi lúc tâm bàn tay cách vai ≤ 0.25 m)
    LIFT = Vector((0, -0.11, 0.6))                                  # sát trên ngực, trên mặt thân (đầu đã ẩn trong cú nhìn)
    lf0, ld1 = mt0 - 0.3, mt1 + 0.45
    key(map_hold, "location", lf0, Vector(MAP_FLAT[0]))
    key(map_hold, "location", mt0 - 0.02, LIFT)
    key(map_hold, "location", mt1 + 0.15, LIFT)
    key(map_hold, "location", ld1, Vector(MAP_FLAT[0]))
    keys(map_spin, "scale", [(lf0, Vector((MAP_BIG,) * 3)), (mt0 - 0.02, Vector((1, 1, 1))), (mt1 + 0.15, Vector((1, 1, 1))),
                             (ld1, Vector((MAP_BIG,) * 3))])
    for k, ob in enumerate(turn_paws):                              # từ hai mép bên vào nắm gần tâm giấy, rồi ra lại
        sd = -1 if k == 0 else 1
        grip = Vector((-sd * (PAW_EDGE - 0.055), -0.12, 0.0))
        keys(ob, "location", [(lf0, Vector()), (mt0 - 0.02, grip), (mt1 + 0.15, grip), (ld1, Vector())])
    step, hand = (mt1 - mt0 - 0.3) / 3, 0.15                        # 3 nấc 0.1 s, 2 lần đổi tay 0.15 s
    t, ang = mt0, 180
    spin_k, rig_k = [(t, (0, 0, ang))], [(t, (0, 0, 0))]
    for n in range(3):
        t, ang = t + step, ang + 60
        spin_k.append((t, (0, 0, ang)))
        rig_k.append((t, (0, 0, 60)))                               # tay xoay cùng giấy
        t2 = t + hand
        spin_k.append((t2, (0, 0, ang)))
        rig_k.append((t2, (0, 0, 0)))                               # giấy đứng yên, tay nhích về: đổi tay cầm
        t = t2 if n < 2 else t
    rot(map_spin, spin_k)
    rot(paw_rig, rig_k)
    if in_seg["S21"]:
        a, b = S["S21"]
        for ob in (L.arm_r, L.arm_l):
            show(ob, a, False)
            show(ob, until("S21"), True)
        for ob in turn_paws:
            show(ob, a, True)
            show(ob, until("S21"), False)
    fl0, fl1 = tm.OBS_FLASH
    show(flash, fl0, True)
    t, i = fl0, 0
    while t < fl1 - 0.2:                                            # lóe xanh ngọc, nhấp nháy
        s = 0.9 if i == 0 else 1.25 if i % 2 else 1.0
        key(flash, "scale", t, Vector((s, s, s)))
        t, i = t + 0.2, i + 1
    show(flash, fl1, False, 1.0)

    # ============================================================ S22: la bàn trong túi rung TÍT TÍT TÍT; chuyển bản đồ sang tay kia; rút la bàn
    for tb in tm.BEEPS_FLASH + (S["S22"][0] + 0.1, S["S22"][0] + 0.35):
        bag_beep(tb, 0.014, 0.2)
    bf = tm.BEEPS_FLASH[0]
    ears(bf, 25)
    ears(bf + 0.3, 10)
    look(bf + 0.25, lumo.matrix() @ (BAG + Vector((0, -0.1, 0))))   # nhìn túi da
    lumo.pose(bf, lean=4)
    lumo.pose(bf + 0.1, lean=-6)
    lumo.pose(bf + 0.4, lean=0)
    x0, x1 = tm.COMPASS_OUT2
    key(map_hold, "location", x0 - 0.6, Vector(MAP_FLAT[0]))
    rot(map_hold, [(x0 - 0.6, MAP_FLAT[1])])
    key(map_hold, "location", x0 - 0.3, Vector(MAP_CHEST[0]))
    rot(map_hold, [(x0 - 0.3, MAP_CHEST[1])])
    keys(map_spin, "scale", [(x0 - 0.6, Vector((MAP_BIG,) * 3)), (x0 - 0.3, Vector((1, 1, 1)))])
    arms(x0 - 0.6, -88, -88)
    arms(x0 - 0.3, -78, -78)
    show(map_hold, x0 - 0.15, False)                                # chuyển bản đồ sang tay xa
    show(map_far, x0 - 0.15, True)
    arm_key(x0 - 0.15, "L", -55)
    arm_key(x0 + 0.05, "R", -14)                                    # tay gần vào túi
    key(compass_r, "location", x0 + 0.15, Vector((0, -0.04, 0.06)))
    show(compass_r, x0 + 0.15, True, 0.4)
    key(compass_r, "location", x1, Vector(CPOS))
    key(compass_r, "scale", x1, Vector((1, 1, 1)))
    arm_key(x1, "R", -78, 30)
    glow(x0 + 0.1, 0.6)
    glow(x0 + 0.15, 1.8)                                            # còn sáng mạnh: ngay cạnh đài thiên văn vừa lóe
    arm_key(x1 + 0.3, "L", -15)                                     # bản đồ thõng bên hông (ra khỏi cú nhìn S23)
    look(x1, lumo.matrix() @ Vector((-0.2, -0.35, 0.5)))

    # ============================================================ S23: la bàn trên mặt bệ (cú nhìn từ trên): mũi sao về đảo khắc, rồi ra chân trời
    jitter(compass_r, S["S23"][0], tm.NEEDLE_ISLAND[0], 0.003, 0.05, CPOS)   # rung mạnh tới khi mũi sao rời ngôi sao
    glow(tm.DIM[0], 1.8)
    glow(tm.DIM[1], 0.6)                                            # dịu xuống, chỉ còn le lói

    # ============================================================ S24, S25: "Chưa từng có hòn đảo này…"; chú chim bay đi
    i0, i1 = tm.LINE_ISLAND
    s24 = S["S24"][0]
    lumo.pose(s24 - HOLD, yaw=90)                                   # giữ thân tới hết S23 (la bàn trong cú nhìn)
    lumo.pose(s24 + 0.2, yaw=33)                                    # hướng chân trời, chéo 12° về phía máy (sau lưng bên trái)
    look(s24 + 0.25, HORIZON)
    ears(s24 + 0.2, 16)
    arm_key(i0 + 0.3, "R", -40, 45)                                 # chìa la bàn ra cạnh người về phía chân trời, ngang bụng
    arm_key(i0 + 1.45, "R", -40, 40)                                # (thấp hẳn dưới mõm cả khi nhìn từ sau lưng)
    arm_key(i0 + 1.45, "L", -15)
    arm_key(i0 + 1.7, "L", -85)                                     # giơ bản đồ giấy lên ở "bản đồ của mình"
    look(i0 + 1.6, lumo.matrix() @ Vector((0.2, -0.3, 0.6)))        # liếc bản đồ giấy
    look(i1 - 0.2, HORIZON)
    squash(i0 + 1.5, 1, 1)
    squash(i0 + 1.7, 1.03, 0.97)
    squash(i0 + 1.9, 0.98, 1.03)
    squash(i1, 1, 1)
    arm_key(i1, "L", -60)
    wag(L.tail, i0, T_END, 0.5, 18, base=(30, 0, 0))
    fy0, fy1 = tm.BIRD_FLY
    rot(B.head, [(i0 + 0.2, (0, 0, 0)), (i0 + 0.5, (0, 20, 0))])
    rot(B.root, [(fy0, (0, 0, -60)), (fy0 + 0.18, (0, 0, yaw_to(BIRD_EDGE, HORIZON)))])   # quay về phía chân trời
    keys(B.root, "scale", [(fy0, Vector((1, 1, 1))), (fy0 + 0.1, Vector((1.12, 1.12, 0.85))), (fy0 + 0.2, Vector((1, 1, 1)))])
    hd = (HORIZON - BIRD_EDGE)
    hd.z = 0
    hd.normalize()
    for t, d, up in ((fy0 + 0.18, 0.0, 0.02), (fy0 + 0.4, 0.35, 0.25), (fy0 + 0.7, 1.0, 0.6), (fy1, 2.4, 1.2),
                     (T_END, 4.5, 2.0)):
        key(B.root, "location", t, BIRD_EDGE + hd * d + Vector((0, 0, up)))
    t, i = fy0 + 0.15, 0
    while t < T_END:
        rot(B.wing, [(t, (0, 0, -70 if i % 2 else 10))])
        rot(B.wing_far, [(t, (0, 0, 70 if i % 2 else -10))])
        t, i = t + 0.06, i + 1
    look(fy0 + 0.3, BIRD_EDGE + hd * 1.0 + Vector((0, 0, 0.6)))     # nhìn theo chú chim
    look(fy1, BIRD_EDGE + hd * 2.4 + Vector((0, 0, 1.2)))
    ears(fy0 + 0.3, 10)

    # ============================================================ chú chim nhảy theo sau Lumo, bắt chước bước chậm (S15–S18)
    bf0 = tm.BIRD_FOLLOW
    key(B.root, "location", bf0 - 0.4, PERCH)
    rot(B.root, [(bf0 - 0.35, (0, 0, BYAW)), (bf0 - 0.2, (0, 0, 90))])   # quay theo hướng Lumo đi
    key(B.root, "location", bf0, PERCH + Vector((-0.1, 0.0, 0.15)))
    key(B.root, "location", bf0 + 0.15, Vector((0.8, 0.6, 0.45)))
    key(B.root, "location", bf0 + 0.3, Vector((0.3, BIRD_PATH_Y, path_z(0.3))))   # xuống bậc đầu sau lưng Lumo
    t, i = bf0, 0
    while t < bf0 + 0.28:
        rot(B.wing, [(t, (0, 0, -70 if i % 2 else 10))])
        rot(B.wing_far, [(t, (0, 0, 70 if i % 2 else -10))])
        t, i = t + 0.06, i + 1
    rot(B.wing, [(bf0 + 0.3, (0, 0, 0))])
    rot(B.wing_far, [(bf0 + 0.3, (0, 0, 0))])
    bx, bz = 0.3, path_z(0.3)
    for t0, t1, x, z in [s for s in lumo_steps if s[0] > bf0 + 0.2]:
        nx = x - 0.4                                                # sát sau Lumo, mỗi bước nhấc chân y hệt, chậm nửa nhịp
        nz = path_z(nx)
        d = 0.22
        key(B.root, "location", t0 + d, Vector((bx, BIRD_PATH_Y, bz)))
        keys(B.root, "scale", [(t0 + d, Vector((1, 1, 1))), (t0 + d + 0.08, Vector((0.92, 0.92, 1.12)))])   # nhón người
        key(B.root, "location", t0 + d + 0.12, Vector(((bx + nx) / 2, BIRD_PATH_Y, max(bz, nz) + 0.08)))
        key(B.root, "location", t1 + d, Vector((nx, BIRD_PATH_Y, nz)))
        keys(B.root, "scale", [(t1 + d, Vector((1.08, 1.08, 0.92))), (t1 + d + 0.1, Vector((1, 1, 1)))])
        rot(B.wing, [(t0 + d, (0, 0, 0)), (t0 + d + 0.12, (0, 0, -35)), (t1 + d, (0, 0, 0))])   # cánh giang như tay giữ thăng bằng
        bx, bz = nx, nz
        if t0 > pw1:
            break
    key(B.root, "location", ar0 - HOLD, Vector((bx, BIRD_PATH_Y, bz)))
    key(B.root, "location", ar0, Vector((5.3, BIRD_PATH_Y, path_z(5.3))))   # cắt cảnh: theo xuống bậc
    key(B.root, "location", ar0 + 0.35, Vector((5.65, BIRD_PATH_Y, path_z(5.65))))
    key(B.root, "location", ar0 + 0.55, Vector((5.95, BIRD_PATH_Y, path_z(5.95))))
    key(B.root, "location", ar1 + 0.2, Vector((6.2, 0.75, 0.0)))     # xuống bãi đất, đứng sau lưng Lumo
    key(B.root, "location", bp0, Vector((6.2, 0.75, 0.0)))
    keys(B.root, "scale", [(bp0, Vector((1, 1, 1))), (bp0 + 0.05, Vector((1.1, 1.1, 0.9))), (bp0 + 0.12, Vector((1, 1, 1)))])
    key(B.root, "location", bp0 + 0.2, Vector((6.6, 0.6, 0.7)))      # bay vòng qua sau lưng Lumo, lên mép bệ
    key(B.root, "location", bp1, BIRD_EDGE)
    key(B.root, "location", tm.BIRD_FLY[0], BIRD_EDGE)

    # ============================================================ cú nhìn của Lumo: đầu ẩn, máy ở trên đầu
    for n in ("S4", "S11", "S19", "S21", "S23"):
        if not in_seg[n]:
            continue
        a = S[n][0]
        key(L.head, "scale", a - HOLD, Vector((1, 1, 1)))
        key(L.head, "scale", a, Vector((0, 0, 0)))
        key(L.head, "scale", until(n) - HOLD, Vector((0, 0, 0)))
        key(L.head, "scale", until(n), Vector((1, 1, 1)))

    # ============================================================ mũi sao: ngắm mục tiêu trong thế giới, mỗi hai khung một key
    scene = bpy.context.scene
    ISL = map_xy(*OBS_UV) + Vector((0, 0, 0.03))
    ni, nh = tm.NEEDLE_ISLAND, tm.NEEDLE_HORIZON
    S23_CAM = ((6.58, -0.72, 1.2), (6.98, -0.42, 0.46))               # cận mặt bệ từ trên: la bàn dưới khung, đảo khắc phía trên
    POV_EYE, POV_FRAC, POV_LENS = (-0.3, 1.1, 0.95), 0.42, 70    # S4, S11: máy sau gáy 1.1 m, cao hơn vai (đầu ẩn): tia
                                                                   # nhìn tới ngôi sao đi giữa hai hàng cột cầu, la bàn lệch
                                                                   # phải không che ngôi sao

    def between(c, far, frac):
        """Nhìn giữa la bàn và far (3D): la bàn ở nửa dưới khung, far ở nửa trên, cùng một đường thẳng."""
        def f(e):
            dc = (c.matrix_world.translation - e).normalized()
            ds = (Vector(far) - e).normalized()
            return e + dc.lerp(ds, frac).normalized()
        return f

    def compass_frame(needle):
        c = needle.parent                                           # vỏ la bàn có thể đang ẩn (scale 0): dựng khung từ bàn tay
        return c.parent.matrix_world @ Matrix.LocRotScale(Vector(CPOS), c.rotation_euler, None)

    def bearing(needle, tgt):
        M = compass_frame(needle)
        d = M.to_3x3().normalized().inverted() @ (tgt - M.translation)
        return math.degrees(math.atan2(-d.x, d.y))

    def bearing_screen(needle, tgt, cam):
        """Góc đầu chỉ sao cho trên màn hình (máy cam = (vị trí, điểm nhìn)) đầu chỉ hướng về tgt trên màn hình
        (SEEDANCE.md, "Cú cận vật cầm trước ngực…"): dò từng độ, chọn góc có hướng hình chiếu gần nhất."""
        pos, at = Vector(cam[0]), Vector(cam[1])
        f = (at - pos).normalized()
        r = f.cross(Vector((0, 0, 1))).normalized()
        u = r.cross(f)

        def proj(q):
            d = q - pos
            z = max(d.dot(f), 1e-4)
            return Vector((d.dot(r) / z, d.dot(u) / z))

        M = compass_frame(needle)
        c2 = proj(M.translation)
        want = proj(tgt) - c2
        best, a_best = None, 0.0
        for k in range(360):
            a = math.radians(k)
            tip = M @ Vector((-math.sin(a) * 0.07, math.cos(a) * 0.07, 0.02))
            v = proj(tip) - c2
            err = abs(wrap(math.degrees(math.atan2(v.x, v.y) - math.atan2(want.x, want.y))))
            if best is None or err < best:
                best, a_best = err, float(k)
        return a_best

    def aim(needle, t0, t1):
        t0, t1 = max(t0, offset - 0.5), min(t1, video_end + 0.5)
        if t1 <= t0:
            return
        prev = None
        f = fr(t0)
        while f <= fr(t1):
            scene.frame_set(f)
            t = (f - 1 + round(offset * FPS)) / FPS
            tg = (STAR_AT + Vector((0, 0, 0.06)), ISL, HORIZON)
            pov_n = [n for n in ("S4", "S11") if S[n][0] - 1e-6 <= t < S[n][1]]
            if S["S23"][0] - 1e-6 <= t < S["S23"][1]:              # cú nhìn từ trên: ngắm theo màn hình
                a_s, a_i, a_h = (bearing_screen(needle, q, S23_CAM) for q in tg)
            elif pov_n:                                             # cú nhìn qua la bàn: ngắm theo màn hình của máy sau vai
                e = L.root.matrix_world @ Vector(POV_EYE)
                cam = (e, between(compass_r, STAR_AT + Vector((0, 0, 0.06)), POV_FRAC)(e))
                a_s, a_i, a_h = (bearing_screen(needle, q, cam) for q in tg)
            else:
                a_s, a_i, a_h = (bearing(needle, q) for q in tg)
            a_i = a_s + wrap(a_i - a_s)
            a_h = a_i + wrap(a_h - a_i)
            if t < ni[0]:
                a = a_s
            elif t < ni[1]:
                a = a_s + (a_i - a_s) * ss((t - ni[0]) / (ni[1] - ni[0]))
            elif t < nh[0]:
                a = a_i + 7 * math.sin(14 * (t - ni[1])) * math.exp(-5 * (t - ni[1]))   # lắc khi tới nơi
            elif t < nh[1]:
                a = a_i + (a_h - a_i) * ss((t - nh[0]) / (nh[1] - nh[0]))
            else:
                a = a_h + 7 * math.sin(14 * (t - nh[1])) * math.exp(-5 * (t - nh[1]))
            if prev is not None:
                a = prev + wrap(a - prev)
            prev = a
            needle.rotation_euler = (0, 0, math.radians(a))
            needle.keyframe_insert("rotation_euler", frame=f)
            f += 2

    aim(needle_r, tm.COMPASS_OUT[0], S["S7"][0] + 0.1)
    aim(needle_l, S["S7"][0] - 0.1, tm.LOOK_COMPASS + 0.1)
    aim(needle_r, tm.LOOK_COMPASS - 0.1, tm.STOW_COMPASS[0] + 0.4)
    aim(needle_r, tm.COMPASS_OUT2[0], T_END)
    scene.frame_set(1)

    # ============================================================ máy quay (một máy mỗi cú; chỉ dựng các cú trong đoạn)
    def side(cx, cz, w, ys=0.0, lens=35, up=0.25, at=None):
        """Máy ngang nhìn +Y thay khung 2D (tâm X, tâm Z, bề ngang w ở mặt phẳng Y = ys), nâng máy lên up, nhìn hơi xuống."""
        d = w * lens / 36
        return (cx, ys - d, cz + up), (cx, ys, cz if at is None else at), lens

    def pov(n, eye, tgt_fn, lens, dt=0.25):
        """Cú nhìn: máy ở eye (toạ độ theo thân Lumo), nhìn tgt_fn(vị trí máy); bám theo thân Lumo từng dt giây."""
        a, b = S[n]
        out, t = [], a
        while t <= b + dt - 1e-6:
            scene.frame_set(fr(min(t, b)))
            e = L.root.matrix_world @ Vector(eye)
            out.append((min(t, b), tuple(e), tuple(tgt_fn(e)), lens))
            t += dt
        return out

    def comp_target(c, far, down):
        """Nhìn về phía far (hướng ngang lệch chút về la bàn), chúc xuống down độ: la bàn ở dưới khung, far ở trên."""
        def f(e):
            hs = Vector(far) - e
            hc = c.matrix_world.translation - e
            hs.z = hc.z = 0
            h = (hs.normalized() * 0.75 + hc.normalized() * 0.25).normalized()
            return e + h + Vector((0, 0, -math.tan(math.radians(down))))
        return f

    cams_def = {   # (giây, vị trí máy, điểm nhìn, tiêu cự mm)
        "S1": [(S["S1"][0], (0.85, -1.9, 0.78), (-0.55, 1.0, 0.62), 24)],                  # cửa từ phía cầu; Lumo loạng choạng ra
        "S2": [(S["S2"][0], (3.0, -9.6, 1.5), (3.0, 0.6, 0.35), 28)],                      # toàn: cầu, lưới, lối nhỏ, bệ đá
        "S3": [(S["S3"][0],) + side(-0.35, 0.5, 2.9, 0.45)],                               # Lumo ở bậc cửa, rộng hơn cần
        "S4": "pov",                                                                     # cận la bàn: chỉ ngôi sao đá
        "S5": [(S["S5"][0], (-1.55, -1.3, 1.15), (0.9, 0.5, 0.45), 24)],                   # sau lưng chếch phải, thấp: Lumo bên trái,
                                                                                         # cầu chạy vào sâu tới bệ đá, bụi sau lưng Lumo
        "S6": [(S["S6"][0], (3.3, -0.12, 1.1), (1.3, 0.0, 0.52), 30)],                   # trên mặt cầu phía trước, nhìn ngược về
                                                                                         # Lumo: thấy mặt, chân và tấm ván kêu, không
                                                                                         # cột hay dây thành cầu nào cắt ngang người
        "S7": [(S["S7"][0], (2.9, -5.6, 0.85), (2.9, 0.0, -0.25), 32)],                   # toàn hơn: dãy ván rơi xuống lưới
        "S8": [(S["S8"][0],) + side(0.55, 0.45, 3.0, 0.1)],                                # túm dây leo, ngã ngồi
        "S9": [(S["S9"][0], (0.98, -1.35, 0.72), (POSTS[1] - 0.05, -RAIL_Y, 0.6), 45)],    # cận chú chim trên cột cầu
        "S10": [(S["S10"][0], (0.65, -2.5, 0.62), (0.65, 0.0, 0.32), 30)],                # Lumo ngồi và chú chim
        "S11": "pov",                                                                    # cận la bàn qua khoảng trống
        "S12": [(S["S12"][0], (2.7, 0.95, 2.9), (-0.25, 0.85, 0.4), 26)],                 # cao trên đầu bụi phía xa, nhìn ngược về
                                                                                         # cửa: thấy mặt Lumo ở ba nhịp nhìn (máy ở
                                                                                         # hướng Lumo nhìn); vạch bụi thì nửa ngoài
                                                                                         # dạt trái, nửa trong dạt phải màn hình
        "S13": [(S["S13"][0], (1.2, 0.2, 0.78), (POSTS[1] + 0.02, -RAIL_Y, 0.6), 45)],     # cận chim từ phía Lumo: nền là trời,
                                                                                         # không còn nửa bụi đã ngả sau lưng chim
        "S14": [(S["S14"][0], (BUSH_X + 0.05, -0.3, 0.86), (BUSH_X + 0.05, BUSH_Y, 0.8), 35)],  # cận Lumo nhìn ngang, bụi cây bên phải
        "S15": [(S["S15"][0], (-1.45, 0.3, 1.7), (0.3, 1.3, 0.55), 24), (tm.CLIMB[0], (-1.45, 0.3, 1.7), (0.3, 1.3, 0.55), 24),
                (S["S15"][1], (-1.0, 0.5, 1.85), (1.0, 1.3, 0.9), 24)],                 # sau lưng chếch trái: tay vịn bên trái
        "S16": [(S["S16"][0], (-0.6, 1.2, 0.62), (0.5, 1.25, 0.22), 28),
                (S["S16"][1], (0.2, 1.2, 0.97), (1.3, 1.25, 0.57), 28)],                # cận bậc đá, máy theo sau chú chim lên bậc: chân Lumo ở mép trên
        "S17": [(S["S17"][0], (5.3, 0.15, 2.4), (2.6, 1.3, 1.25), 28),
                (S["S17"][1], (7.5, 0.0, 2.0), (5.0, 1.25, 0.8), 28)],                   # trước mặt chếch phía khe, cao: Lumo đi
                                                                                         # về phía máy, tay trái bám tay vịn (bên
                                                                                         # phải màn hình), chim theo sau, lưới dưới
        "S18": [(S["S18"][0],) + side(6.2, 0.6, 3.3, 0.2, up=0.45, at=0.55),               # xuống từng bậc (đầu còn cao trên bậc)
                (tm.ARRIVE[0] + 1.0,) + side(6.3, 0.45, 3.0, 0.2, up=0.45, at=0.35)],      # rồi hạ dần theo Lumo tới bệ đá
        "S19": [(S["S19"][0], (6.42, -0.1, 1.42), (7.12, 0.02, 0.43), 26)],               # cận mặt bệ từ trên (cú nhìn)
        "S20": [(S["S20"][0],) + side(6.9, 0.5, 2.6, 0.0, up=0.45, at=0.4)],              # chim đậu mép bệ, rút bản đồ
        "S21": [(S["S21"][0], (6.52, -0.13, 1.5), (6.98, -0.12, 0.44), 28),               # cận hai bản đồ (cú nhìn): giấy ngay dưới
                (tm.CAM_EDGE[0], (6.52, -0.13, 1.5), (6.98, -0.12, 0.44), 28),            # bản đồ khắc, rương ở mép dưới giấy trên dải CC
                (tm.CAM_EDGE[1], (6.8, -0.48, 1.18), (7.12, -0.3, 0.44), 32),              # tới mép phải hai bản đồ
                (tm.CAM_PAN[0], (6.8, -0.48, 1.18), (7.12, -0.3, 0.44), 32),
                (tm.CAM_PAN[0] + 1.0, (7.05, -0.45, 1.0), (7.36, -0.31, 0.4), 35),         # đài thiên văn khắc
                (tm.CAM_PAN[0] + 2.0, (6.72, -0.45, 1.08), (7.14, -0.31, 0.43), 35)],      # đài khắc (trên) và cùng chỗ đó trên
                                                                                         # giấy là góc mây trống (dưới); giữ tới hết
                                                                                         # cú, qua cả lúc đài khắc lóe
        "S22": [(S["S22"][0],) + side(6.85, 0.5, 2.6, 0.0, up=0.45, at=0.4)],
        "S23": [(S["S23"][0],) + S23_CAM + (32,)],                                         # cận mặt bệ từ trên, la bàn to, đảo khắc
        "S24": [(S["S24"][0], (4.16, -0.33, 1.0), (6.98, -1.36, 0.75), 24)],             # sau lưng chếch trái: Lumo mép trái,
                                                                                         # chân trời mép phải (không thấy đảo xa)
        "S25": [(S["S25"][0], (3.8, -1.8, 1.8), (7.45, -0.45, 0.68), 70),                # cao, xa, chếch phải sau lưng, ống dài: chim
                (tm.BIRD_FLY[0] + 0.3, (3.8, -1.8, 1.8), (7.45, -0.45, 0.68), 70),
                (tm.BIRD_FLY[0] + 0.9, (3.75, -1.7, 1.85), (7.9, -0.95, 1.35), 50),         # ngẩng theo chim bay lên            # cất cánh đủ to; rồi mở rộng dần (1.6 s) thành toàn
                (tm.BIRD_FLY[0] + 1.9, (2.95, -0.72, 2.2), (8.6, -2.2, 0.55), 24)],        # (cùng phía -Y với
                                                                                         # S24): Lumo nhỏ mép trái, chim bay nhỏ
                                                                                         # dần về chân trời bên phải; khác hẳn S24
    }
    shots = [(n, a, b) for n, a, b in tm.SHOTS if a < end_t - 1e-6 and b > offset + 1e-6]
    use = {}
    for n, _, _ in shots:
        c = cams_def[n]
        if c == "pov":                                              # máy sau gáy (đầu ẩn), nhìn qua la bàn sang ngôi sao đá:
            c = pov(n, POV_EYE, between(compass_r, STAR_AT + Vector((0, 0, 0.06)), POV_FRAC), POV_LENS)   # sau vai trái
                                                                                         # (cánh tay cầm la bàn không chắn mặt la bàn),
                                                                                         # thấp gần tầm la bàn: bệ đá và ngôi sao ở nửa
                                                                                         # trên, la bàn nửa dưới trên dải CC
        use[n] = c
    cams = cameras(shots, use)
    for n, cam in cams.items():
        linear(cam)
        linear(cam.data)
        linear(bpy.data.objects[f"Aim_{n}"])

    H = Vector((0, 0, 0.2))
    must = {"S1": [(L.head, H)], "S2": [(L.root, Vector((0, 0, 0.5))), (pstar, Vector())], "S3": [(L.head, H)],
            "S4": [(compass_r, Vector())], "S5": [(L.head, H)], "S6": [(L.head, H)], "S7": [(L.root, Vector((0, 0, 0.5)))],
            "S8": [(L.root, Vector((0, 0, 0.5)))], "S9": [], "S10": [(L.head, H), (B.head, Vector())],
            "S11": [(compass_r, Vector())], "S12": [(L.head, H)], "S13": [(B.head, Vector())], "S14": [(L.head, H)],
            "S15": [(L.head, H)], "S16": [(B.head, Vector())], "S17": [(L.root, Vector((0, 0, 0.5))), (B.root, Vector())],
            "S18": [(L.head, H)], "S19": [(pstar, Vector())], "S20": [(L.head, H), (B.head, Vector())],
            "S21": [], "S22": [(L.head, H)], "S23": [(compass_r, Vector())], "S24": [(L.head, H)],
            "S25": [(L.head, H)]}
    extra = [("S9", B.head, tm.BIRD_LAND[1], S["S9"][1]), ("S21", map_spin, S["S21"][0], tm.CAM_PAN[0]),
             ("S21", map_spin, tm.CAM_PAN[1], S["S21"][1]), ("S25", B.head, S["S25"][0], S["S25"][1]), ("S20", B.head, tm.BIRD_PERCH[1], S["S20"][1]),
             ("S22", B.head, S["S22"][0], S["S22"][1])]
    check_in_frame(shots, cams, {n: must.get(n, []) for n, _, _ in shots}, extra)
    stills = [round((a + b) / 2, 2) for _, a, b in shots]
    stills += [t for t in (tm.LUMO_STUMBLE[0] + 0.5, tm.COMPASS_OUT[1], tm.LINE_AHEAD[0] + 0.6, tm.RUSH[1], tm.CREAK + 0.1,
                           tm.WAIT_PEBBLE[0] + 0.6, tm.CRACK + 0.5, tm.CRACK + 1.4, tm.GRAB[0] + 0.3, tm.PHICH + 0.1,
                           tm.CHIRPS[1], tm.LINE_VERY_OLD[0] + 0.4, tm.PART_BUSH[1] + 0.2, tm.CLIMB[0] + 1.5, tm.CACH + 0.1,
                           tm.SLAB_SLIDE[1] + 0.2, tm.MAP_OUT[1], tm.MAP_TURN[0] - 0.5, tm.MAP_TURN[1] + 0.3,
                           tm.CAM_PAN[0] + 1.1, tm.OBS_FLASH[0] + 0.3, tm.COMPASS_OUT2[1], tm.NEEDLE_ISLAND[1] + 0.3,
                           tm.NEEDLE_HORIZON[1] + 0.3, tm.LINE_ISLAND[0] + 2.0, tm.BIRD_FLY[0] + 0.7) if offset <= t < end_t]
    finish(out_blend, sorted(set(stills)))
