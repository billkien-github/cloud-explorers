"""
Lumo (Cloudling - cáo mây) dựng + rig hoàn toàn bằng code, để kiểm chứng rig tự động.
    blender -b --factory-startup -P build_lumo.py        -> lumo.blend
Quy trình: metaball -> mesh -> voxel remesh (lưới sạch) -> tô màu theo vùng -> metarig Rigify
(thân người rút gọn + 2 tai + đuôi) -> generate rig -> gắn da tự động -> gắn mắt/mũi/miệng vào xương đầu.
"""
import math
import os
import sys

import addon_utils
import bpy
from mathutils import Euler, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "pipeline"))
from lablib import hex_rgba, link_obj, principled, smoothstep  # noqa: E402
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "pipeline", "rigging"))
from face_rig import build_face  # noqa: E402
from skin import fix_skin  # noqa: E402

OUT_BLEND = os.path.join(HERE, "lumo.blend")
C = hex_rgba
PEACH, CREAM, CLOUD, MINT, ACCENT = C("#F5A45D"), C("#FFF0D5"), C("#FFF8EB"), C("#52C6B5"), C("#D97736")

# ---------------------------------------------------------------- hình khối (mét, Lumo nhìn về -Y)
STIFF = 8.0                     # metaball "cứng" -> ít dính nhau ngoài ý muốn
EAR_TILT = math.radians(15)
EAR_BASE, EAR_LEN = (0.06, 0.005, 0.42), 0.15
TAIL_PATH = [(0, 0.085, 0.115), (0, 0.145, 0.14), (0, 0.2, 0.19), (0, 0.235, 0.26), (0, 0.24, 0.335), (0, 0.22, 0.405)]

BODY_PARTS = [  # (tâm, bán kính nhìn thấy, tỉ lệ xyz, xoay Euler)
    ((0, -0.005, 0.345), 0.125, (1.06, 1.0, 0.95), (0, 0, 0)),        # đầu
    ((0, -0.105, 0.315), 0.045, (1.1, 0.9, 0.75), (0, 0, 0)),         # mõm
    ((0, -0.092, 0.284), 0.042, (1.15, 0.85, 0.75), (0, 0, 0)),       # cằm: đỡ dưới mõm để miệng há không bị khuất
    ((0.095, -0.045, 0.30), 0.045, (1, 1, 1), (0, 0, 0)),             # má bông
    ((-0.095, -0.045, 0.30), 0.045, (1, 1, 1), (0, 0, 0)),
    ((0, 0.005, 0.175), 0.095, (1.0, 0.92, 1.15), (0, 0, 0)),         # thân
    ((0, -0.04, 0.16), 0.06, (1, 1, 1), (0, 0, 0)),                   # bụng
]
for sx in (1, -1):
    BODY_PARTS += [
        ((sx * 0.052, 0.0, 0.085), 0.042, (1, 1, 1), (0, 0, 0)),               # đùi
        ((sx * 0.058, -0.022, 0.028), 0.036, (1, 1.4, 0.75), (0, 0, 0)),       # bàn chân
        ((sx * 0.092, -0.01, 0.225), 0.03, (1, 1, 1), (0, 0, 0)),              # vai
        ((sx * 0.107, -0.022, 0.195), 0.028, (1, 1, 1), (0, 0, 0)),            # khuỷu: nối vai-bàn tay liền khối
        ((sx * 0.12, -0.035, 0.165), 0.028, (1, 1, 1.1), (0, 0, 0)),           # bàn tay
    ]
    mid = (sx * (EAR_BASE[0] + 0.5 * EAR_LEN * math.sin(EAR_TILT)), EAR_BASE[1],
           EAR_BASE[2] + 0.5 * EAR_LEN * math.cos(EAR_TILT))
    BODY_PARTS.append((mid, 0.05, (1.12, 0.42, 1.5), (0, sx * EAR_TILT, 0)))     # tai cáo: chân rộng
TAIL_PARTS = [(p, r, (1, 1, 1), (0, 0, 0)) for p, r in zip(TAIL_PATH, (0.045, 0.055, 0.065, 0.07, 0.07, 0.06))]
TAIL_PARTS += [((sx * 0.04, p[1] + 0.01, p[2]), 0.045, (1, 1, 1), (0, 0, 0)) for sx in (1, -1) for p in TAIL_PATH[2:5]]


def ball_radius(visible):
    """Bán kính ảnh hưởng của metaball để bề mặt nhìn thấy có bán kính = visible."""
    return visible / math.sqrt(1 - (0.6 / STIFF) ** (1 / 3))


def blob_mesh(name, parts, voxel=0.0055):
    mb = bpy.data.metaballs.new(name)
    mb.resolution = mb.render_resolution = 0.004
    for co, vis, scl, rot in parts:
        e = mb.elements.new(type="ELLIPSOID")
        e.co, e.radius, e.stiffness = co, ball_radius(vis), STIFF
        e.size_x, e.size_y, e.size_z = scl
        e.rotation = Euler(rot).to_quaternion()
    mobj = link_obj(bpy.data.objects.new(name + "_mb", mb))
    dg = bpy.context.evaluated_depsgraph_get()
    raw = bpy.data.meshes.new_from_object(mobj.evaluated_get(dg))
    tmp = link_obj(bpy.data.objects.new(name + "_raw", raw))
    rm = tmp.modifiers.new("Remesh", "REMESH")           # lưới đều, toàn tứ giác -> biến dạng đẹp
    rm.mode, rm.voxel_size = "VOXEL", voxel
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(tmp.evaluated_get(dg))
    me.name = name
    for o in (mobj, tmp):
        bpy.data.objects.remove(o)
    me.shade_smooth()
    return link_obj(bpy.data.objects.new(name, me))


def paint(obj, fn):
    """Tô màu từng đỉnh theo hàm vị trí -> thuộc tính 'Col'."""
    me = obj.data
    attr = me.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
    for v, c in zip(me.vertices, attr.data):
        c.color = fn(v.co)


def mix(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def body_color(p):
    x, y, z = p
    belly = smoothstep(-0.03, -0.075, y) * smoothstep(0.09, 0.12, z) * (1 - smoothstep(0.22, 0.26, z)) \
        * (1 - smoothstep(0.05, 0.08, abs(x)))
    muzzle = smoothstep(-0.07, -0.11, y) * (1 - smoothstep(0.32, 0.345, z)) * smoothstep(0.26, 0.28, z)
    cheek = smoothstep(-0.02, -0.07, y) * smoothstep(0.07, 0.11, abs(x)) * (1 - smoothstep(0.31, 0.34, z)) \
        * smoothstep(0.255, 0.275, z)
    c = mix(PEACH, CREAM, max(belly, muzzle, cheek))
    c = mix(c, ACCENT, smoothstep(0.52, 0.55, z))                     # chóp tai
    c = mix(c, ACCENT, 1 - smoothstep(0.012, 0.03, z))                # gan bàn chân
    return c


def skin_material():
    m = bpy.data.materials.new("M_LumoFur")
    N, L = m.node_tree.nodes, m.node_tree.links
    b = N["Principled BSDF"]
    a = N.new("ShaderNodeAttribute")
    a.attribute_name = "Col"
    L.new(a.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.55
    b.inputs["Sheen Weight"].default_value = 0.5
    b.inputs["Sheen Roughness"].default_value = 0.4
    b.inputs["Subsurface Weight"].default_value = 0.1
    b.inputs["Subsurface Radius"].default_value = (0.8, 0.4, 0.25)
    b.inputs["Subsurface Scale"].default_value = 0.02
    return m


# ---------------------------------------------------------------- metarig
SPINE_Z = [0.095, 0.14, 0.185, 0.225, 0.255, 0.27, 0.29, 0.47]
SPINE_Y = [0.01, 0.008, 0.005, 0.0, 0.0, -0.002, -0.004, -0.004]
LIMBS = {  # tên xương: (đầu, đuôi) cho phía trái (x>0); bên phải lật x
    "shoulder": ((0.015, -0.01, 0.245), (0.075, 0.0, 0.235)),
    "upper_arm": ((0.088, -0.005, 0.228), (0.105, 0.005, 0.198)),
    "forearm": ((0.105, 0.005, 0.198), (0.115, -0.025, 0.172)),
    "hand": ((0.115, -0.025, 0.172), (0.12, -0.04, 0.152)),
    "thigh": ((0.05, 0.0, 0.105), (0.054, -0.014, 0.065)),
    "shin": ((0.054, -0.014, 0.065), (0.057, 0.0, 0.03)),
    "foot": ((0.057, 0.0, 0.03), (0.058, -0.045, 0.012)),
    "toe": ((0.058, -0.045, 0.012), (0.058, -0.065, 0.012)),
    "heel.02": ((0.035, 0.02, 0.0), (0.08, 0.02, 0.0)),
}


def chain_points(a, b, n):
    a, b = Vector(a), Vector(b)
    return [a.lerp(b, i / n) for i in range(n + 1)]


def build_metarig():
    bpy.ops.object.armature_basic_human_metarig_add()
    mr = bpy.context.active_object
    bpy.ops.object.mode_set(mode="EDIT")
    eb = mr.data.edit_bones
    for name in ("breast.L", "breast.R", "pelvis.L", "pelvis.R"):
        eb.remove(eb[name])
    names = ["spine"] + [f"spine.{i:03d}" for i in range(1, 7)]
    for i, n in enumerate(names):
        eb[n].head = (0, SPINE_Y[i], SPINE_Z[i])
        eb[n].tail = (0, SPINE_Y[i + 1], SPINE_Z[i + 1])
    for side, sx in ((".L", 1), (".R", -1)):
        for base, (h, t) in LIMBS.items():
            b = eb[base + side]
            b.head = (sx * h[0], h[1], h[2])
            b.tail = (sx * t[0], t[1], t[2])
    # tai: chuỗi 3 xương mỗi bên, gắn vào xương đầu
    for side, sx in ((".L", 1), (".R", -1)):
        base = Vector((sx * EAR_BASE[0], EAR_BASE[1], EAR_BASE[2]))
        tip = base + Vector((sx * math.sin(EAR_TILT), 0, math.cos(EAR_TILT))) * EAR_LEN
        prev = None
        for k, (a, b) in enumerate(zip(chain_points(base, tip, 3)[:-1], chain_points(base, tip, 3)[1:])):
            bone = eb.new("ear" + ("" if k == 0 else f".{k:03d}") + side)
            bone.head, bone.tail = a, b
            bone.align_roll(Vector((0, -1, 0)))
            bone.parent = prev or eb["spine.006"]
            bone.use_connect = prev is not None
            prev = bone
    # đuôi: chuỗi 5 xương theo đường đuôi, gắn vào hông
    prev = None
    for k, (a, b) in enumerate(zip(TAIL_PATH[:-1], TAIL_PATH[1:])):
        bone = eb.new("tail" + ("" if k == 0 else f".{k:03d}"))
        bone.head, bone.tail = a, b
        bone.align_roll(Vector((1, 0, 0)))
        bone.parent = prev or eb["spine"]
        bone.use_connect = prev is not None
        prev = bone
    bpy.ops.object.mode_set(mode="OBJECT")
    for n in ("ear.L", "ear.R", "tail"):
        mr.pose.bones[n].rigify_type = "limbs.simple_tentacle"
    return mr


# ---------------------------------------------------------------- sửa da sau khi gắn tự động
HEAD_ZONES = [((0, -0.02, 0.345), 0.128), ((0, -0.1, 0.3), 0.06)]   # (tâm, bán kính): đầu, mõm + cằm


# ---------------------------------------------------------------- mặt (face rig: xem face_rig.py)
def face_materials():
    return {
        "white": principled("M_LumoEyeWhite", (1, 1, 1, 1), 0.12, **{"Coat Weight": 0.5}),
        "iris": principled("M_LumoIris", MINT, 0.2),
        "pupil": principled("M_LumoPupil", C("#10202A"), 0.1),
        "glint": principled("M_LumoGlint", (1, 1, 1, 1), 0.2, **{"Emission Color": (1, 1, 1, 1), "Emission Strength": 1.6}),
        "dark": principled("M_LumoNose", C("#2A1A14"), 0.3, **{"Coat Weight": 0.6}),
        "blush": principled("M_LumoBlush", C("#FF9E8A"), 0.5),
        "star": principled("M_LumoStar", CREAM, 0.4, **{"Emission Color": CREAM, "Emission Strength": 0.3}),
        "fur": principled("M_LumoLid", PEACH, 0.55, **{"Sheen Weight": 0.5}),
        "brow": principled("M_LumoBrow", C("#B85E2A"), 0.5),
        "mouth": principled("M_LumoMouth", C("#5A2420"), 0.45),
        "sweat": principled("M_LumoSweat", C("#9ED8F5"), 0.05, **{"Coat Weight": 1.0}),
    }


# ---------------------------------------------------------------- build
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("rigify", default_set=True)
scene = bpy.context.scene
scene.name = "Lumo"

fur = skin_material()
body = blob_mesh("LumoBody", BODY_PARTS)
paint(body, body_color)
tail = blob_mesh("LumoTail", TAIL_PARTS)
paint(tail, lambda p: mix(CLOUD, C("#F3E4CF"), 1 - smoothstep(0.12, 0.2, p.z)))
for o in (body, tail):
    o.data.materials.append(fur)

metarig = build_metarig()
bpy.context.view_layer.objects.active = metarig
metarig.select_set(True)
bpy.ops.pose.rigify_generate()
rig = bpy.context.active_object
rig.name = "RIG-Lumo"
metarig.hide_viewport = metarig.hide_render = True

# gắn da tự động (bone heat) cho thân và đuôi
bpy.ops.object.select_all(action="DESELECT")
for o in (body, tail):
    o.select_set(True)
rig.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.object.parent_set(type="ARMATURE_AUTO")
if "--raw" not in sys.argv:          # --raw: giữ da gắn tự động nguyên bản để so sánh
    for o in (body, tail):
        fix_skin(o, head_bone="DEF-spine.006", head_zones=HEAD_ZONES, keep_prefix="DEF-ear")

build_face(rig, body, face_materials())
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
vg = {o.name: len(o.vertex_groups) for o in (body, tail)}
print("LUMO_SAVED", OUT_BLEND, "body verts", len(body.data.vertices), "tail verts", len(tail.data.vertices),
      "vertex groups", vg, "rig bones", len(rig.data.bones))
