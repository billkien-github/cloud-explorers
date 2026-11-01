"""
Shot 01 - "Dawn" (Bình minh)
30s one-shot: camera trôi qua rừng thông lúc đêm có đom đóm, trời hửng dần,
mặt trời ló qua dãy núi sau hồ.

Chạy (tạo file shot01.blend cạnh script này):
    blender -b --factory-startup -P build_shot.py

Mọi tham số chỉnh nhanh nằm trong khối CONFIG bên dưới.
"""
import bpy
import bmesh
import math
import random
import os
from mathutils import Matrix, Vector, noise

# ---------------------------------------------------------------- CONFIG
FPS = 24
FRAMES = 30 * FPS                     # 720 frame = 30s
SEED = 7
LAKE = Vector((0.0, 62.0))            # tâm hồ (x, y)
LAKE_R = 32.0
N_TREES_NEAR = 420
N_TREES_FAR = 260
N_FIREFLIES = 160
OUT_BLEND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shot01.blend")

# keyframe ánh sáng / thời gian trong ngày
NIGHT, PREDAWN, SUNRISE, END = 1, 300, 560, FRAMES

random.seed(SEED)


# ---------------------------------------------------------------- helpers
def smoothstep(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def fbm(x, y, octaves=4):
    v, amp, f = 0.0, 1.0, 1.0
    for _ in range(octaves):
        v += amp * noise.noise(Vector((x * f, y * f, 0.37)))
        amp *= 0.5
        f *= 2.0
    return v


def height(x, y):
    """Địa hình: đồi thấp quanh rừng, hồ ở giữa, núi phía xa (có 'khe' ở giữa cho mặt trời mọc)."""
    n = fbm(x * 0.02, y * 0.02)
    h = 1.2 + 2.0 * n + 0.4 * noise.noise(Vector((x * 0.1, y * 0.1, 1.3)))
    d = math.hypot(x - LAKE.x, (y - LAKE.y) * 0.85)
    h = lerp(-3.0, h, smoothstep(LAKE_R - 6, LAKE_R + 8, d))
    far = smoothstep(110, 240, y)
    side = smoothstep(70, 160, abs(x))
    mtn = max(far, side * 0.7)
    ridge = 1 - abs(noise.noise(Vector((x * 0.012, y * 0.012 + 5, 2.1))))
    notch = lerp(0.4, 1.0, smoothstep(15, 90, abs(x)))
    h += mtn * notch * (25 + 45 * ridge ** 2 + 8 * n)
    return h


def fcurves_of(id_data):
    """Lấy fcurves của action - tương thích layered actions (Blender 4.4+/5.x)."""
    ad = id_data.animation_data
    act = ad.action
    if hasattr(act, "fcurves"):
        return act.fcurves
    from bpy_extras import anim_utils
    return anim_utils.action_get_channelbag_for_slot(act, ad.action_slot).fcurves


def key_socket(sock, frames_values):
    for f, v in frames_values:
        sock.default_value = v
        sock.keyframe_insert("default_value", frame=f)


def drive_frame(sock, expr="frame"):
    d = sock.driver_add("default_value").driver
    d.type = "SCRIPTED"
    d.expression = expr


def new_mat(name):
    m = bpy.data.materials.new(name)
    if hasattr(m, "use_nodes"):
        try:
            m.use_nodes = True
        except Exception:
            pass
    return m, m.node_tree.nodes, m.node_tree.links


def link(links, a, b):
    links.new(a, b)


def rgba(node, name, out=False):
    """ShaderNodeMix có nhiều socket trùng tên (float/vector/color) - lấy bản màu."""
    socks = node.outputs if out else node.inputs
    return next(x for x in socks if x.name == name and x.type == "RGBA")


def link_obj(obj):
    bpy.context.scene.collection.objects.link(obj)
    return obj


# ---------------------------------------------------------------- reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "shot01_dawn"
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, FRAMES


# ---------------------------------------------------------------- terrain
def build_terrain():
    x0, x1, y0, y1, step = -200, 200, -80, 300, 2.0
    nx = int((x1 - x0) / step) + 1
    ny = int((y1 - y0) / step) + 1
    verts = [(x0 + i * step, y0 + j * step, height(x0 + i * step, y0 + j * step))
             for j in range(ny) for i in range(nx)]
    faces = [(j * nx + i, j * nx + i + 1, (j + 1) * nx + i + 1, (j + 1) * nx + i)
             for j in range(ny - 1) for i in range(nx - 1)]
    me = bpy.data.meshes.new("terrain")
    me.from_pydata(verts, [], faces)
    me.update()
    obj = link_obj(bpy.data.objects.new("Terrain", me))

    m, N, L = new_mat("M_Terrain")
    bsdf = N["Principled BSDF"]
    geo = N.new("ShaderNodeNewGeometry")
    sep = N.new("ShaderNodeSeparateXYZ")
    rng = N.new("ShaderNodeMapRange")
    rng.inputs["From Min"].default_value = -3
    rng.inputs["From Max"].default_value = 70
    ramp = N.new("ShaderNodeValToRGB")
    els = ramp.color_ramp.elements
    els[0].position, els[0].color = 0.0, (0.10, 0.08, 0.05, 1)
    els[1].position, els[1].color = 0.07, (0.035, 0.07, 0.02, 1)
    for pos, col in [(0.30, (0.05, 0.07, 0.04, 1)), (0.55, (0.16, 0.15, 0.14, 1)),
                     (0.80, (0.75, 0.78, 0.82, 1))]:
        e = els.new(pos)
        e.color = col
    # sườn dốc -> đá
    sepn = N.new("ShaderNodeSeparateXYZ")
    slope = N.new("ShaderNodeMapRange")
    slope.inputs["From Min"].default_value = 0.85
    slope.inputs["From Max"].default_value = 0.70
    mix = N.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    rgba(mix, "B").default_value = (0.14, 0.13, 0.12, 1)
    link(L, geo.outputs["Position"], sep.inputs[0])
    link(L, sep.outputs["Z"], rng.inputs["Value"])
    link(L, rng.outputs[0], ramp.inputs[0])
    link(L, geo.outputs["Normal"], sepn.inputs[0])
    link(L, sepn.outputs["Z"], slope.inputs["Value"])
    link(L, slope.outputs[0], mix.inputs["Factor"])
    link(L, ramp.outputs["Color"], rgba(mix, "A"))
    link(L, rgba(mix, "Result", True), bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.95
    me.materials.append(m)
    return obj


# ---------------------------------------------------------------- water
def build_water():
    bpy.ops.mesh.primitive_plane_add(size=1, location=(LAKE.x, LAKE.y, 0.0))
    obj = bpy.context.active_object
    obj.name = "Water"
    obj.scale = (110, 110, 1)
    m, N, L = new_mat("M_Water")
    bsdf = N["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.005, 0.012, 0.02, 1)
    bsdf.inputs["Roughness"].default_value = 0.03
    bsdf.inputs["IOR"].default_value = 1.33
    tc = N.new("ShaderNodeTexCoord")
    nz = N.new("ShaderNodeTexNoise")
    nz.noise_dimensions = "4D"
    nz.inputs["Scale"].default_value = 0.6
    nz.inputs["Detail"].default_value = 4
    drive_frame(nz.inputs["W"], "frame/90")
    bump = N.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.08
    link(L, tc.outputs["Object"], nz.inputs["Vector"])
    link(L, nz.outputs["Fac"], bump.inputs["Height"])
    link(L, bump.outputs["Normal"], bsdf.inputs["Normal"])
    obj.data.materials.append(m)


# ---------------------------------------------------------------- trees & rocks
def pine_mesh():
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.13, radius2=0.09, depth=1.4,
                          matrix=Matrix.Translation((0, 0, 0.7)))
    trunk_faces = set(bm.faces)
    for z, r, d in [(1.6, 1.15, 1.9), (2.6, 0.88, 1.7), (3.5, 0.58, 1.5)]:
        bmesh.ops.create_cone(bm, cap_ends=True, segments=7, radius1=r, radius2=0.0, depth=d,
                              matrix=Matrix.Translation((0, 0, z)))
    for f in bm.faces:
        f.material_index = 0 if f in trunk_faces else 1
    me = bpy.data.meshes.new("pine")
    bm.to_mesh(me)
    bm.free()

    mt, N, L = new_mat("M_Trunk")
    N["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.03, 0.02, 1)
    ml, N, L = new_mat("M_Leaves")
    bsdf = N["Principled BSDF"]
    oi = N.new("ShaderNodeObjectInfo")
    ramp = N.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].color = (0.012, 0.035, 0.015, 1)
    ramp.color_ramp.elements[1].color = (0.04, 0.07, 0.02, 1)
    link(L, oi.outputs["Random"], ramp.inputs[0])
    link(L, ramp.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.8
    me.materials.append(mt)
    me.materials.append(ml)
    return me


def scatter(me, n, xr, yr, ok, smin, smax, prefix, coll):
    placed, tries = 0, 0
    while placed < n and tries < n * 30:
        tries += 1
        x, y = random.uniform(*xr), random.uniform(*yr)
        if not ok(x, y):
            continue
        o = bpy.data.objects.new(f"{prefix}{placed:04d}", me)
        z = height(x, y)
        o.location = (x, y, z - 0.15)
        s = random.uniform(smin, smax)
        o.scale = (s, s, s * random.uniform(0.9, 1.25))
        o.rotation_euler = (random.uniform(-0.04, 0.04), random.uniform(-0.04, 0.04), random.uniform(0, 6.28))
        coll.objects.link(o)
        placed += 1


def build_forest():
    coll = bpy.data.collections.new("Forest")
    scene.collection.children.link(coll)
    me = pine_mesh()

    def lake_d(x, y):
        return math.hypot(x - LAKE.x, (y - LAKE.y) * 0.85)

    def near_ok(x, y):
        corridor = abs(x - cam_x_at(y)) < 3.2 and y < 34
        return not corridor and lake_d(x, y) > LAKE_R + 4

    def far_ok(x, y):
        h = height(x, y)
        return lake_d(x, y) > LAKE_R + 5 and 0 < h < 30 and random.random() < 1.2 - h / 30

    scatter(me, N_TREES_NEAR, (-70, 70), (-80, 34), near_ok, 0.75, 1.7, "PineN", coll)
    scatter(me, N_TREES_FAR, (-150, 150), (34, 190), far_ok, 0.9, 1.9, "PineF", coll)

    # đá ven hồ
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
    for v in bm.verts:
        v.co *= random.uniform(0.75, 1.15)
    rock = bpy.data.meshes.new("rock")
    bm.to_mesh(rock)
    bm.free()
    mr, N, L = new_mat("M_Rock")
    N["Principled BSDF"].inputs["Base Color"].default_value = (0.09, 0.085, 0.08, 1)
    N["Principled BSDF"].inputs["Roughness"].default_value = 0.9
    rock.materials.append(mr)
    rocks = []
    for i in range(46):
        a = random.uniform(0, 6.28)
        r = LAKE_R + random.uniform(-3, 4)
        x, y = LAKE.x + math.cos(a) * r, LAKE.y + math.sin(a) * r / 0.85
        o = bpy.data.objects.new(f"Rock{i:03d}", rock)
        o.location = (x, y, max(height(x, y), -0.4))
        s = random.uniform(0.3, 1.4)
        o.scale = (s * random.uniform(1, 1.8), s, s * random.uniform(0.4, 0.8))
        o.rotation_euler = (0, 0, random.uniform(0, 6.28))
        coll.objects.link(o)


# ---------------------------------------------------------------- camera path
# (frame, x, y, cao-trên-mặt-đất) và điểm nhìn (frame, x, y, z)
CAM_KEYS = [(1, 0.0, -48, 1.7), (240, 0.6, -22, 1.9), (480, -0.4, 4, 2.6), (FRAMES, 0.0, 24, 7.5)]
AIM_KEYS = [(1, 0.0, -20, 2.0), (240, 0.0, 10, 2.6), (480, 0.0, 90, 7.0), (FRAMES, 0.0, 240, 20.0)]


def cam_x_at(y):
    pts = [(k[2], k[1]) for k in CAM_KEYS]
    for (ya, xa), (yb, xb) in zip(pts, pts[1:]):
        if ya <= y <= yb:
            return lerp(xa, xb, (y - ya) / (yb - ya))
    return 0.0


def build_camera():
    cam_data = bpy.data.cameras.new("Cam")
    cam_data.lens = 28
    cam_data.clip_start = 0.1
    cam_data.clip_end = 2000
    cam = link_obj(bpy.data.objects.new("Camera", cam_data))
    scene.camera = cam
    aim = link_obj(bpy.data.objects.new("CamTarget", None))
    for f, x, y, up in CAM_KEYS:
        cam.location = (x, y, height(x, y) + up)
        cam.keyframe_insert("location", frame=f)
    for f, x, y, z in AIM_KEYS:
        aim.location = (x, y, z)
        aim.keyframe_insert("location", frame=f)
    # rung tay nhẹ
    for fc in fcurves_of(aim):
        mod = fc.modifiers.new("NOISE")
        mod.scale = 55
        mod.strength = 0.25
        mod.phase = random.uniform(0, 100)
    c = cam.constraints.new("TRACK_TO")
    c.target = aim
    c.track_axis = "TRACK_NEGATIVE_Z"
    c.up_axis = "UP_Y"


# ---------------------------------------------------------------- fireflies
def build_fireflies():
    coll = bpy.data.collections.new("Fireflies")
    scene.collection.children.link(coll)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.035)
    me = bpy.data.meshes.new("firefly")
    bm.to_mesh(me)
    bm.free()

    m, N, L = new_mat("M_Firefly")
    N.remove(N["Principled BSDF"])
    em = N.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.85, 0.25, 1)
    oi = N.new("ShaderNodeObjectInfo")
    t = N.new("ShaderNodeValue")
    drive_frame(t.outputs[0])
    # flicker = (0.5 + 0.5*sin(frame*0.11 + rand*100)) ^ 3
    mul = N.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 100
    mul2 = N.new("ShaderNodeMath"); mul2.operation = "MULTIPLY"; mul2.inputs[1].default_value = 0.11
    add = N.new("ShaderNodeMath"); add.operation = "ADD"
    sin = N.new("ShaderNodeMath"); sin.operation = "SINE"
    remap = N.new("ShaderNodeMath"); remap.operation = "MULTIPLY_ADD"
    remap.inputs[1].default_value = 0.5; remap.inputs[2].default_value = 0.5
    pw = N.new("ShaderNodeMath"); pw.operation = "POWER"; pw.inputs[1].default_value = 3
    fade = N.new("ShaderNodeValue"); fade.name = "Fade"
    key_socket(fade.outputs[0], [(NIGHT, 60.0), (330, 60.0), (520, 0.0)])
    strength = N.new("ShaderNodeMath"); strength.operation = "MULTIPLY"
    link(L, oi.outputs["Random"], mul.inputs[0])
    link(L, t.outputs[0], mul2.inputs[0])
    link(L, mul.outputs[0], add.inputs[0])
    link(L, mul2.outputs[0], add.inputs[1])
    link(L, add.outputs[0], sin.inputs[0])
    link(L, sin.outputs[0], remap.inputs[0])
    link(L, remap.outputs[0], pw.inputs[0])
    link(L, pw.outputs[0], strength.inputs[0])
    link(L, fade.outputs[0], strength.inputs[1])
    link(L, strength.outputs[0], em.inputs["Strength"])
    tr = N.new("ShaderNodeBsdfTransparent")
    addsh = N.new("ShaderNodeAddShader")
    link(L, em.outputs[0], addsh.inputs[0])
    link(L, tr.outputs[0], addsh.inputs[1])
    link(L, addsh.outputs[0], N["Material Output"].inputs["Surface"])
    m.surface_render_method = "BLENDED"
    me.materials.append(m)

    for i in range(N_FIREFLIES):
        y = random.uniform(-46, 28)
        x = cam_x_at(y) + random.gauss(0, 6)
        o = bpy.data.objects.new(f"Firefly{i:03d}", me)
        o.location = (x, y, height(x, y) + random.uniform(0.3, 2.8))
        coll.objects.link(o)
        o.keyframe_insert("location", frame=1)
        for fc in fcurves_of(o):
            mod = fc.modifiers.new("NOISE")
            mod.scale = random.uniform(40, 90)
            mod.strength = 1.2 if fc.array_index < 2 else 0.6
            mod.phase = random.uniform(0, 500)


# ---------------------------------------------------------------- sky / world
def build_world():
    w = bpy.data.worlds.new("Sky")
    scene.world = w
    if hasattr(w, "use_nodes"):
        try:
            w.use_nodes = True
        except Exception:
            pass
    N, L = w.node_tree.nodes, w.node_tree.links
    N.clear()
    out = N.new("ShaderNodeOutputWorld")
    tc = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ")
    link(L, tc.outputs["Generated"], sep.inputs[0])

    # zenith/horizon gradient
    grad = N.new("ShaderNodeMapRange")
    grad.inputs["From Min"].default_value = -0.02
    grad.inputs["From Max"].default_value = 0.35
    link(L, sep.outputs["Z"], grad.inputs["Value"])
    zen = N.new("ShaderNodeRGB"); zen.label = "Zenith"
    hor = N.new("ShaderNodeRGB"); hor.label = "Horizon"
    sky = N.new("ShaderNodeMix"); sky.data_type = "RGBA"
    link(L, grad.outputs[0], sky.inputs["Factor"])
    link(L, hor.outputs[0], rgba(sky, "A"))
    link(L, zen.outputs[0], rgba(sky, "B"))

    # glow phía mặt trời (+Y)
    dot = N.new("ShaderNodeVectorMath"); dot.operation = "DOT_PRODUCT"
    dot.inputs[1].default_value = (0, 0.995, 0.1)
    link(L, tc.outputs["Generated"], dot.inputs[0])
    gmap = N.new("ShaderNodeMapRange")
    gmap.inputs["From Min"].default_value = 0.8
    gmap.inputs["From Max"].default_value = 1.0
    link(L, dot.outputs["Value"], gmap.inputs["Value"])
    gpow = N.new("ShaderNodeMath"); gpow.operation = "POWER"; gpow.inputs[1].default_value = 3.0
    link(L, gmap.outputs[0], gpow.inputs[0])
    glow = N.new("ShaderNodeRGB"); glow.label = "Glow"
    gcol = N.new("ShaderNodeMix"); gcol.data_type = "RGBA"; gcol.blend_type = "MULTIPLY"
    gcol.inputs["Factor"].default_value = 1.0
    rgba(gcol, "A").default_value = (1, 1, 1, 1)
    link(L, gpow.outputs[0], rgba(gcol, "A"))
    link(L, glow.outputs[0], rgba(gcol, "B"))
    add = N.new("ShaderNodeMix"); add.data_type = "RGBA"; add.blend_type = "ADD"
    add.inputs["Factor"].default_value = 1.0
    link(L, rgba(sky, "Result", True), rgba(add, "A"))
    link(L, rgba(gcol, "Result", True), rgba(add, "B"))

    # sao
    vor = N.new("ShaderNodeTexVoronoi")
    vor.inputs["Scale"].default_value = 260
    link(L, tc.outputs["Generated"], vor.inputs["Vector"])
    smap = N.new("ShaderNodeMapRange")
    smap.inputs["From Min"].default_value = 0.035
    smap.inputs["From Max"].default_value = 0.0
    link(L, vor.outputs["Distance"], smap.inputs["Value"])
    above = N.new("ShaderNodeMapRange")
    above.inputs["From Min"].default_value = 0.02
    above.inputs["From Max"].default_value = 0.25
    link(L, sep.outputs["Z"], above.inputs["Value"])
    starv = N.new("ShaderNodeValue"); starv.label = "Stars"
    s1 = N.new("ShaderNodeMath"); s1.operation = "MULTIPLY"
    s2 = N.new("ShaderNodeMath"); s2.operation = "MULTIPLY"
    s3 = N.new("ShaderNodeMath"); s3.operation = "MULTIPLY"
    vrand = N.new("ShaderNodeMath"); vrand.operation = "GREATER_THAN"; vrand.inputs[1].default_value = 0.6
    link(L, vor.outputs["Color"], vrand.inputs[0])
    link(L, smap.outputs[0], s1.inputs[0])
    link(L, above.outputs[0], s1.inputs[1])
    link(L, s1.outputs[0], s2.inputs[0])
    link(L, starv.outputs[0], s2.inputs[1])
    link(L, s2.outputs[0], s3.inputs[0])
    link(L, vrand.outputs[0], s3.inputs[1])
    stars_rgb = N.new("ShaderNodeMix"); stars_rgb.data_type = "RGBA"; stars_rgb.blend_type = "ADD"
    link(L, s3.outputs[0], stars_rgb.inputs["Factor"])
    link(L, rgba(add, "Result", True), rgba(stars_rgb, "A"))
    rgba(stars_rgb, "B").default_value = (1.2, 1.25, 1.4, 1)

    bg = N.new("ShaderNodeBackground")
    link(L, rgba(stars_rgb, "Result", True), bg.inputs["Color"])
    link(L, bg.outputs[0], out.inputs["Surface"])

    # Không dùng World Volume: EEVEE coi nó là vô hạn -> nuốt mất bầu trời.
    # Sương/khí quyển nằm trong khối GroundMist (build_mist).

    C = lambda r, g, b: (r, g, b, 1)
    key_socket(zen.outputs[0], [(NIGHT, C(0.002, 0.004, 0.014)), (PREDAWN, C(0.012, 0.02, 0.06)),
                                (SUNRISE, C(0.03, 0.07, 0.2)), (END, C(0.05, 0.13, 0.34))])
    key_socket(hor.outputs[0], [(NIGHT, C(0.006, 0.012, 0.03)), (PREDAWN, C(0.09, 0.05, 0.08)),
                                (SUNRISE, C(0.7, 0.3, 0.14)), (END, C(0.75, 0.45, 0.25))])
    key_socket(glow.outputs[0], [(NIGHT, C(0, 0, 0)), (PREDAWN, C(0.35, 0.12, 0.05)),
                                 (SUNRISE, C(2.2, 0.75, 0.22)), (END, C(2.4, 1.1, 0.4))])
    key_socket(starv.outputs[0], [(NIGHT, 1.0), (260, 1.0), (440, 0.0)])


# ---------------------------------------------------------------- ground mist
def build_mist():
    # khối sương phủ cả cảnh: lớp sương dày sát mặt đất + một chút haze cho chiều sâu núi xa
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 110, 57))
    obj = bpy.context.active_object
    obj.name = "GroundMist"
    obj.scale = (400, 380, 120)
    m, N, L = new_mat("M_Mist")
    N.remove(N["Principled BSDF"])
    vol = N.new("ShaderNodeVolumePrincipled")
    vol.inputs["Color"].default_value = (0.8, 0.85, 1.0, 1)
    vol.inputs["Anisotropy"].default_value = 0.35
    geo = N.new("ShaderNodeNewGeometry")
    sep = N.new("ShaderNodeSeparateXYZ")
    mr = N.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = -1.0
    mr.inputs["From Max"].default_value = 6.0
    mr.inputs["To Min"].default_value = 1.0
    mr.inputs["To Max"].default_value = 0.0
    dens = N.new("ShaderNodeValue"); dens.name = "MistDensity"
    key_socket(dens.outputs[0], [(NIGHT, 0.025), (PREDAWN, 0.04), (SUNRISE, 0.03), (END, 0.012)])
    mul = N.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    link(L, geo.outputs["Position"], sep.inputs[0])
    link(L, sep.outputs["Z"], mr.inputs["Value"])
    haze = N.new("ShaderNodeMath"); haze.operation = "ADD"; haze.name = "Haze"
    haze.inputs[1].default_value = 0.0004
    link(L, mr.outputs[0], mul.inputs[0])
    link(L, dens.outputs[0], mul.inputs[1])
    link(L, mul.outputs[0], haze.inputs[0])
    link(L, haze.outputs[0], vol.inputs["Density"])
    link(L, vol.outputs[0], N["Material Output"].inputs["Volume"])
    obj.data.materials.append(m)


# ---------------------------------------------------------------- lights & sun disk
def sun_rot(elev_deg, az_deg=0.0):
    return (math.radians(-(90 - elev_deg)), 0.0, math.radians(az_deg))


def build_lights():
    sun_d = bpy.data.lights.new("Sun", "SUN")
    sun_d.angle = math.radians(1.2)
    sun = link_obj(bpy.data.objects.new("Sun", sun_d))
    for f, e, en, col in [(NIGHT, -8, 0.0, (1, 0.4, 0.2)), (440, 0.0, 0.0, (1, 0.4, 0.2)),
                          (SUNRISE, 4.0, 3.0, (1, 0.55, 0.3)), (END, 9.0, 4.5, (1, 0.72, 0.5))]:
        sun.rotation_euler = sun_rot(e)
        sun.keyframe_insert("rotation_euler", frame=f)
        sun_d.energy = en
        sun_d.color = col
        sun_d.keyframe_insert("energy", frame=f)
        sun_d.keyframe_insert("color", frame=f)

    moon_d = bpy.data.lights.new("Moon", "SUN")
    moon_d.color = (0.55, 0.65, 1.0)
    moon_d.angle = math.radians(0.6)
    moon = link_obj(bpy.data.objects.new("Moon", moon_d))
    moon.rotation_euler = (math.radians(50), 0, math.radians(150))
    for f, en in [(NIGHT, 0.35), (PREDAWN, 0.25), (SUNRISE, 0.0)]:
        moon_d.energy = en
        moon_d.keyframe_insert("energy", frame=f)

    # đĩa mặt trời
    bpy.ops.mesh.primitive_uv_sphere_add(radius=14, segments=24, ring_count=12)
    disk = bpy.context.active_object
    disk.name = "SunDisk"
    m, N, L = new_mat("M_SunDisk")
    N.remove(N["Principled BSDF"])
    em = N.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (1.0, 0.62, 0.3, 1)
    em.inputs["Strength"].default_value = 60
    link(L, em.outputs[0], N["Material Output"].inputs["Surface"])
    disk.data.materials.append(m)
    D = 620
    for f, e in [(NIGHT, -8), (440, 0.0), (SUNRISE, 4.0), (END, 9.0)]:
        r = math.radians(e)
        disk.location = (0, 24 + D * math.cos(r), 7 + D * math.sin(r))
        disk.keyframe_insert("location", frame=f)
    disk.visible_shadow = False


# ---------------------------------------------------------------- render setup
def setup_render():
    r = scene.render
    r.engine = "BLENDER_EEVEE"
    r.resolution_x, r.resolution_y = 1920, 1080
    r.resolution_percentage = 50
    r.film_transparent = False
    ee = scene.eevee
    ee.taa_render_samples = 32
    ee.use_raytracing = True
    ee.volumetric_start = 0.1
    ee.volumetric_end = 420
    ee.volumetric_tile_size = "8"
    ee.volumetric_samples = 64
    ee.use_volumetric_shadows = True
    ee.volumetric_shadow_samples = 16
    try:
        scene.view_settings.view_transform = "AgX"
        scene.view_settings.look = "AgX - Medium High Contrast"
    except Exception as e:
        print("color management:", e)

    # compositor: bloom nhẹ
    try:
        ng = bpy.data.node_groups.new("Comp", "CompositorNodeTree")
        ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
        rl = ng.nodes.new("CompositorNodeRLayers")
        gl = ng.nodes.new("CompositorNodeGlare")
        gl.inputs["Type"].default_value = "Bloom"
        gl.inputs["Quality"].default_value = "High"
        gl.inputs["Threshold"].default_value = 1.0
        gl.inputs["Strength"].default_value = 0.6
        gl.inputs["Size"].default_value = 0.6
        out = ng.nodes.new("NodeGroupOutput")
        ng.links.new(rl.outputs["Image"], gl.inputs["Image"])
        ng.links.new(gl.outputs["Image"], out.inputs[0])
        scene.compositing_node_group = ng
        r.use_compositing = True
    except Exception as e:
        print("compositor skipped:", e)


# ---------------------------------------------------------------- build
build_terrain()
build_water()
build_camera()          # trước forest vì forest cần corridor của camera
build_forest()
build_fireflies()
build_world()
build_mist()
build_lights()
setup_render()
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", OUT_BLEND, "objects:", len(bpy.data.objects))
