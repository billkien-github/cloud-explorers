"""
Hàm dùng chung cho mọi build script (Blender 5.2).
Import trong build script (ví dụ 04_PRODUCTION/EP001_.../sh010/build_shot.py, lùi lên tới thư mục gốc studio/):
    STUDIO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.insert(0, os.path.join(STUDIO, "pipeline"))
    from lablib import *
"""
import math

import bpy


# ---------------------------------------------------------------- math
def smoothstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def hex_rgba(h, a=1.0):
    """'#F5A45D' (sRGB) -> tuple linear RGBA cho Blender."""
    h = h.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return (*out, a)


def facing(fx, fy):
    """Góc rotation Z để mặt trước (-Y local) nhìn theo hướng (fx, fy)."""
    return math.atan2(fx, -fy)


# ---------------------------------------------------------------- scene
def reset_scene(name, fps=24, frames=720):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.name = name
    sc.render.fps = fps
    sc.frame_start, sc.frame_end = 1, frames
    return sc


def link_obj(obj, coll=None):
    (coll or bpy.context.scene.collection).objects.link(obj)
    return obj


def new_collection(name):
    c = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(c)
    return c


def mesh_obj(name, bm, coll=None, smooth=True):
    """bmesh -> object (bm được free)."""
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    return link_obj(bpy.data.objects.new(name, me), coll)


# ---------------------------------------------------------------- animation
def fcurves_of(id_data):
    """fcurves của action - tương thích layered actions (Blender 4.4+/5.x)."""
    ad = id_data.animation_data
    act = ad.action
    if hasattr(act, "fcurves"):
        return act.fcurves
    from bpy_extras import anim_utils
    return anim_utils.action_get_channelbag_for_slot(act, ad.action_slot).fcurves


def keys(target, path, frames_values, interp=None):
    """Keyframe một thuộc tính: keys(obj, 'location', [(1, (0,0,0)), (24, (1,0,0))])."""
    for f, v in frames_values:
        setattr(target, path, v)
        target.keyframe_insert(path, frame=f)
    if interp:
        set_interp(target, path, interp)


def set_interp(target, path, interp):
    for fc in fcurves_of(target.id_data):
        if fc.data_path.endswith(path):
            for kp in fc.keyframe_points:
                kp.interpolation = interp


def key_socket(sock, frames_values):
    for f, v in frames_values:
        sock.default_value = v
        sock.keyframe_insert("default_value", frame=f)


def drive(sock_or_struct, prop, expr):
    d = sock_or_struct.driver_add(prop).driver
    d.type = "SCRIPTED"
    d.expression = expr
    return d


def drive_frame(sock, expr="frame"):
    return drive(sock, "default_value", expr)


def visible_between(obj, f_on, f_off):
    """Chỉ hiện obj trong khoảng [f_on, f_off)."""
    seq = [(1, False), (f_off, True)] if f_on <= 1 else [(1, True), (f_on, False), (f_off, True)]
    for f, hide in seq:
        obj.hide_render = hide
        obj.hide_viewport = hide
        obj.keyframe_insert("hide_render", frame=f)
        obj.keyframe_insert("hide_viewport", frame=f)
    set_interp(obj, "hide_render", "CONSTANT")
    set_interp(obj, "hide_viewport", "CONSTANT")


# ---------------------------------------------------------------- materials
def new_mat(name):
    m = bpy.data.materials.new(name)
    return m, m.node_tree.nodes, m.node_tree.links


def rgba(node, name, out=False):
    """ShaderNodeMix có nhiều socket trùng tên (float/vector/color) - lấy bản màu."""
    socks = node.outputs if out else node.inputs
    return next(x for x in socks if x.name == name and x.type == "RGBA")


def principled(name, color, rough=0.5, **inputs):
    """Material Principled nhanh. inputs: tên socket -> giá trị."""
    m, N, L = new_mat(name)
    b = N["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Roughness"].default_value = rough
    for k, v in inputs.items():
        b.inputs[k].default_value = v
    return m


def emissive(name, color, strength=5.0):
    m, N, L = new_mat(name)
    N.remove(N["Principled BSDF"])
    em = N.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = color
    em.inputs["Strength"].default_value = strength
    L.new(em.outputs[0], N["Material Output"].inputs["Surface"])
    return m, em


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


# ---------------------------------------------------------------- camera
def camera(name, loc, target, lens=35, coll=None):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.clip_start = 0.02
    cd.clip_end = 1500
    cam = link_obj(bpy.data.objects.new(name, cd), coll)
    cam.location = loc
    aim = link_obj(bpy.data.objects.new(name + "_aim", None), coll)
    aim.location = target
    c = cam.constraints.new("TRACK_TO")
    c.target = aim
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"
    return cam, aim


def cut_to(cam, frame):
    """Marker đổi camera tại frame."""
    m = bpy.context.scene.timeline_markers.new(cam.name, frame=frame)
    m.camera = cam


# ---------------------------------------------------------------- assets
def import_file(path):
    """Import .gltf/.glb/.fbx -> (object mới, {tên action: action} mới)."""
    before, before_a = set(bpy.data.objects), set(bpy.data.actions)
    if path.lower().endswith(".fbx"):
        bpy.ops.import_scene.fbx(filepath=path)
    else:
        bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    acts = {a.name.split(".")[0]: a for a in bpy.data.actions if a not in before_a}
    return new, acts


def asset_collection(path, name):
    """Import một model vào collection riêng (không nằm trong scene) để làm nguồn instance."""
    new, _ = import_file(path)
    coll = bpy.data.collections.new(name)
    for o in new:
        for c in list(o.users_collection):
            c.objects.unlink(o)
        coll.objects.link(o)
    return coll


def instance(coll, name, loc, rot_z=0.0, scale=1.0, parent_coll=None):
    """Đặt một bản instance của collection (dùng chung mesh, rất nhẹ)."""
    e = bpy.data.objects.new(name, None)
    e.instance_type, e.instance_collection = "COLLECTION", coll
    e.location, e.rotation_euler = loc, (0, 0, rot_z)
    e.scale = (scale, scale, scale)
    return link_obj(e, parent_coll)


def nla_sequence(arm, acts, plan):
    """Thay animation của armature bằng chuỗi strip NLA: plan = [(tên action, frame bắt đầu, frame kết thúc)]."""
    ad = arm.animation_data or arm.animation_data_create()
    ad.action = None
    for t in list(ad.nla_tracks):
        ad.nla_tracks.remove(t)
    track = ad.nla_tracks.new()
    for name, f0, f1 in plan:
        act = acts[name]
        length = act.frame_range[1] - act.frame_range[0]
        st = track.strips.new(name, int(f0), act)
        st.repeat = max(0.1, (f1 - f0) / max(length, 1))


# ---------------------------------------------------------------- render
def setup_render(samples=32, bloom=0.6, threshold=1.0):
    sc = bpy.context.scene
    r = sc.render
    r.engine = "BLENDER_EEVEE"
    r.resolution_x, r.resolution_y = 1920, 1080
    r.resolution_percentage = 50
    ee = sc.eevee
    ee.taa_render_samples = samples
    ee.use_raytracing = True
    try:
        sc.view_settings.view_transform = "AgX"
        sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception as e:
        print("color management:", e)
    try:
        ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
        ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
        rl = ng.nodes.new("CompositorNodeRLayers")
        gl = ng.nodes.new("CompositorNodeGlare")
        gl.inputs["Type"].default_value = "Bloom"
        gl.inputs["Quality"].default_value = "High"
        gl.inputs["Threshold"].default_value = threshold
        gl.inputs["Strength"].default_value = bloom
        gl.inputs["Size"].default_value = 0.6
        out = ng.nodes.new("NodeGroupOutput")
        ng.links.new(rl.outputs["Image"], gl.inputs["Image"])
        ng.links.new(gl.outputs["Image"], out.inputs[0])
        sc.compositing_node_group = ng
        r.use_compositing = True
    except Exception as e:
        print("compositor skipped:", e)
