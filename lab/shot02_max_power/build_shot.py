"""
Shot 02 - "MAX POWER" (demo The Wonderlings, trích Act 2->3 tập 01).
Piko vô tình đè nút MAX POWER của máy Rain-O-Matic 3000 -> mây kéo về -> mưa -> BOP.
Xem SHOTLIST.md để biết nhịp từng shot.

Chạy (tạo shot02.blend cạnh script này):
    blender -b --factory-startup -P build_shot.py
"""
import math
import os
import random
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector, noise
from mathutils.bvhtree import BVHTree

HERE = os.path.dirname(os.path.abspath(__file__))
STUDIO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(STUDIO, "pipeline"))
sys.path.insert(0, HERE)
from lablib import (asset_collection, assign, camera, cut_to, drive, drive_frame, emissive, facing,  # noqa: E402
                    fcurves_of, hex_rgba, import_file, instance, key_socket, keys, lerp, link_obj, mesh_obj,
                    new_collection, new_mat, nla_sequence, principled, reset_scene, rgba, set_interp, setup_render,
                    smoothstep, visible_between)
from timing import (BOP, FLASHES, FPS, FRAMES, PERK0, PERK1, PRESS, RAIN_HEAVY, RAIN_LIGHT, SHOTS,  # noqa: E402,F401
                    STORM0, STORM1, WET0, WET1)

# ---------------------------------------------------------------- CONFIG
SEED = 11
OUT_BLEND = os.path.join(HERE, "shot02.blend")
ASSETS = os.path.join(STUDIO, "02_ASSET_LIBRARY", "Third_Party", "quaternius")
AUDIO_MIX = os.path.join(HERE, "audio", "shot02_mix.wav")   # tạo bởi build_audio.py
HOUSE_SPOTS = [(-4.6, 4.8, 1.0), (5.6, 5.2, 1.25), (-7.6, 1.2, 0.9), (8.2, -1.4, 1.1), (1.2, 8.8, 1.4)]  # (x, y, scale)

PIKO_HOME = Vector((0.55, -0.74, 0.0))
HERO_FLOWER = Vector((-0.95, -0.35, 0.0))
TINY_CLOUD = Vector((-0.95, -0.35, 2.3))
NOZZLE_TOP = Vector((0.0, 0.0, 1.78))

PANEL_LOC, PANEL_TILT = Vector((0.0, -0.5, 0.31)), math.radians(-25)
BUTTON_LOCAL = Vector((0.115, -0.062, -0.035))
BUTTON_WORLD = Matrix.Translation(PANEL_LOC) @ Matrix.Rotation(PANEL_TILT, 4, "X") @ (BUTTON_LOCAL + Vector((0, -0.013, 0)))
TO_BUTTON = (BUTTON_WORLD - PIKO_HOME).xy.normalized().to_3d()   # lưng Piko quay về phía nút khi đáp đất
LAND = PIKO_HOME + TO_BUTTON * 0.15

random.seed(SEED)
C = hex_rgba


# ---------------------------------------------------------------- small helpers
def fsock(node, name, out=False):
    socks = node.outputs if out else node.inputs
    return next(x for x in socks if x.name == name and x.type == "VALUE")


def frame_value(N):
    v = N.new("ShaderNodeValue")
    drive_frame(v.outputs[0])
    return v.outputs[0]


def math_node(N, L, op, a, b=None, c=None):
    n = N.new("ShaderNodeMath")
    n.operation = op
    for i, x in enumerate((a, b, c)):
        if x is None:
            continue
        if isinstance(x, (int, float)):
            n.inputs[i].default_value = x
        else:
            L.new(x, n.inputs[i])
    return n.outputs[0]


def osc(N, L, speed, lo, hi, phase=0.0):
    """lo + (hi-lo) * (0.5 + 0.5*sin(frame*speed + phase))."""
    t = math_node(N, L, "MULTIPLY_ADD", frame_value(N), speed, phase)
    s = math_node(N, L, "SINE", t)
    s = math_node(N, L, "MULTIPLY_ADD", s, 0.5 * (hi - lo), 0.5 * (hi + lo))
    return s


def mix_float(N, L, fac, a, b):
    m = N.new("ShaderNodeMix")
    m.data_type = "FLOAT"
    for name, x in (("Factor", fac), ("A", a), ("B", b)):
        if isinstance(x, (int, float)):
            fsock(m, name).default_value = x
        else:
            L.new(x, fsock(m, name))
    return fsock(m, "Result", True)


def keyed_value(N, name, frames_values):
    v = N.new("ShaderNodeValue")
    v.name = v.label = name
    key_socket(v.outputs[0], frames_values)
    return v.outputs[0]


def child(obj, parent, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
    obj.parent = parent
    obj.location, obj.rotation_euler, obj.scale = loc, rot, scale
    return obj


def empty(name, coll, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    e = link_obj(bpy.data.objects.new(name, None), coll)
    e.empty_display_size = 0.05
    if parent:
        child(e, parent, loc, rot)
    else:
        e.location, e.rotation_euler = loc, rot
    return e


def sphere(name, r, mat, coll, seg=32, rings=16):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    return assign(mesh_obj(name, bm, coll), mat)


def cylinder(name, r, depth, mat, coll, seg=32, r2=None, axis="Z", smooth_sides=True):
    bm = bmesh.new()
    m = Matrix.Rotation(math.pi / 2, 4, "X") if axis == "Y" else Matrix()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r if r2 is None else r2,
                          depth=depth, matrix=m)
    obj = mesh_obj(name, bm, coll)
    if smooth_sides:  # nắp phẳng, thân tròn
        ax = Vector((0, 1, 0)) if axis == "Y" else Vector((0, 0, 1))
        for p in obj.data.polygons:
            p.use_smooth = abs(p.normal.dot(ax)) < 0.9
    return assign(obj, mat)


def rbox(name, size, bevel, mat, coll, segments=4):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    obj = mesh_obj(name, bm, coll)
    mod = obj.modifiers.new("Bevel", "BEVEL")
    mod.width, mod.segments, mod.harden_normals = bevel, segments, True
    return assign(obj, mat)


def hemisphere(name, r, mat, coll, seg=40, rings=20):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=rings, radius=r)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context="VERTS")
    bmesh.ops.holes_fill(bm, edges=bm.edges[:], sides=0)
    return assign(mesh_obj(name, bm, coll), mat)


def curve_tube(name, pts, radius, mat, coll, kind="BEZIER"):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = radius, 6, True
    if kind == "POLY":
        sp = cu.splines.new("POLY")
        sp.points.add(len(pts) - 1)
        for p, co in zip(sp.points, pts):
            p.co = (*co, 1)
    else:
        sp = cu.splines.new("BEZIER")
        sp.bezier_points.add(len(pts) - 1)
        for p, co in zip(sp.bezier_points, pts):
            p.co = co
            p.handle_left_type = p.handle_right_type = "AUTO"
    cu.materials.append(mat)
    return link_obj(bpy.data.objects.new(name, cu), coll)


def text_obj(name, body, size, mat, coll):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body, cu.size = body, size
    cu.align_x, cu.align_y = "CENTER", "CENTER"
    cu.extrude = 0.0015
    cu.materials.append(mat)
    return link_obj(bpy.data.objects.new(name, cu), coll)


def metacloud(name, elems, mat, coll, res=0.08):
    mb = bpy.data.metaballs.new(name)
    mb.resolution, mb.render_resolution = res * 2, res
    for x, y, z, r in elems:
        e = mb.elements.new()
        e.co, e.radius = (x, y, z), r
    mb.materials.append(mat)
    return link_obj(bpy.data.objects.new(name, mb), coll)


def cloud_blob(scale, n=7, seed=0):
    """Các phần tử metaball tạo hình một đám mây bông (dẹt đáy)."""
    rnd = random.Random(seed)
    out = [(0, 0, 0.15 * scale, 1.15 * scale)]
    for i in range(n - 1):
        a = i / (n - 1) * math.tau + rnd.uniform(-0.3, 0.3)
        d = rnd.uniform(0.55, 0.95) * scale
        out.append((math.cos(a) * d, math.sin(a) * d * 0.7, rnd.uniform(-0.05, 0.3) * scale,
                    rnd.uniform(0.7, 1.0) * scale))
    return out


# ---------------------------------------------------------------- reset
scene = reset_scene("shot02_max_power", FPS, FRAMES)
scene["lab_stills"] = "40,150,240,298,308,380,470,560,610,646,690"
ENV = new_collection("Environment")
MACH = new_collection("RainOMatic")
PIKO_C = new_collection("Piko")
FX = new_collection("FX")
CAMS = new_collection("Cameras")


# ---------------------------------------------------------------- environment
def height(x, y):
    r = math.hypot(x, y)
    bumps = 0.035 * noise.noise(Vector((x * 0.8, y * 0.8, 0.3)))
    f = 0.5 + 0.5 * noise.noise(Vector((x * 0.03, y * 0.03, 1.7)))
    hills = smoothstep(9, 45, r) * (4 + 9 * f)
    return bumps + hills


def build_ground():
    n, half = 241, 60.0
    step = 2 * half / (n - 1)
    verts = [(-half + i * step, -half + j * step, height(-half + i * step, -half + j * step))
             for j in range(n) for i in range(n)]
    faces = [(j * n + i, j * n + i + 1, (j + 1) * n + i + 1, (j + 1) * n + i)
             for j in range(n - 1) for i in range(n - 1)]
    me = bpy.data.meshes.new("ground")
    me.from_pydata(verts, [], faces)
    for p in me.polygons:
        p.use_smooth = True
    obj = link_obj(bpy.data.objects.new("Ground", me), ENV)

    m, N, L = new_mat("M_Ground")
    b = N["Principled BSDF"]
    geo = N.new("ShaderNodeNewGeometry")
    sep = N.new("ShaderNodeSeparateXYZ")
    L.new(geo.outputs["Position"], sep.inputs[0])
    comb = N.new("ShaderNodeCombineXYZ")
    L.new(sep.outputs["X"], comb.inputs["X"])
    L.new(sep.outputs["Y"], comb.inputs["Y"])
    rlen = N.new("ShaderNodeVectorMath")
    rlen.operation = "LENGTH"
    L.new(comb.outputs[0], rlen.inputs[0])
    garden = N.new("ShaderNodeMapRange")       # 1 trong vườn, 0 ngoài đồi
    garden.inputs["From Min"].default_value, garden.inputs["From Max"].default_value = 6, 11
    garden.inputs["To Min"].default_value, garden.inputs["To Max"].default_value = 1, 0
    L.new(rlen.outputs["Value"], garden.inputs["Value"])

    nz = N.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 1.5
    L.new(geo.outputs["Position"], nz.inputs["Vector"])
    soil = N.new("ShaderNodeValToRGB")
    soil.color_ramp.elements[0].color = C("#E3A766")
    soil.color_ramp.elements[1].color = C("#C98A4E")
    L.new(nz.outputs["Fac"], soil.inputs[0])
    grass = N.new("ShaderNodeValToRGB")
    grass.color_ramp.elements[0].color = C("#D4B45E")
    grass.color_ramp.elements[1].color = C("#B0A052")
    L.new(nz.outputs["Fac"], grass.inputs[0])
    land = N.new("ShaderNodeMix")
    land.data_type = "RGBA"
    L.new(garden.outputs[0], land.inputs["Factor"])
    L.new(grass.outputs["Color"], rgba(land, "A"))
    L.new(soil.outputs["Color"], rgba(land, "B"))

    # vết nứt đất khô
    warp = N.new("ShaderNodeTexNoise")
    warp.inputs["Scale"].default_value = 3.0
    warp.inputs["Detail"].default_value = 3.0
    L.new(geo.outputs["Position"], warp.inputs["Vector"])
    wvec = N.new("ShaderNodeVectorMath")
    wvec.operation = "MULTIPLY_ADD"
    L.new(warp.outputs["Color"], wvec.inputs[0])
    wvec.inputs[1].default_value = (0.25, 0.25, 0.25)
    L.new(geo.outputs["Position"], wvec.inputs[2])
    vor = N.new("ShaderNodeTexVoronoi")
    vor.feature = "DISTANCE_TO_EDGE"
    vor.inputs["Scale"].default_value = 2.2
    vor.inputs["Randomness"].default_value = 1.0
    L.new(wvec.outputs["Vector"], vor.inputs["Vector"])
    crack = N.new("ShaderNodeMapRange")
    crack.inputs["From Min"].default_value, crack.inputs["From Max"].default_value = 0.0, 0.016
    crack.inputs["To Min"].default_value, crack.inputs["To Max"].default_value = 1, 0
    L.new(vor.outputs["Distance"], crack.inputs["Value"])
    wet = keyed_value(N, "Wet", [(1, 0.0), (WET0, 0.0), (WET1, 1.0)])
    dry = math_node(N, L, "SUBTRACT", 1.0, wet)
    cmask = math_node(N, L, "MULTIPLY", crack.outputs[0], garden.outputs[0])
    cmask = math_node(N, L, "MULTIPLY", cmask, dry)
    cracked = N.new("ShaderNodeMix")
    cracked.data_type = "RGBA"
    L.new(cmask, cracked.inputs["Factor"])
    L.new(rgba(land, "Result", True), rgba(cracked, "A"))
    rgba(cracked, "B").default_value = C("#7A4E2A")
    # ướt -> tối màu, bóng hơn
    darken = N.new("ShaderNodeMix")
    darken.data_type = "RGBA"
    darken.blend_type = "MULTIPLY"
    L.new(math_node(N, L, "MULTIPLY", wet, 0.55), darken.inputs["Factor"])
    L.new(rgba(cracked, "Result", True), rgba(darken, "A"))
    rgba(darken, "B").default_value = C("#3A4250")
    L.new(rgba(darken, "Result", True), b.inputs["Base Color"])
    L.new(mix_float(N, L, wet, 0.92, 0.35), b.inputs["Roughness"])
    assign(obj, m)

    # vũng nước dâng dần khi mưa
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=64, radius=8.0)
    pud = mesh_obj("Puddles", bm, ENV)
    keys(pud, "location", [(1, (0, 0, -0.08)), (WET0 + 40, (0, 0, -0.04)), (FRAMES, (0, 0, 0.018))])
    pm, N, L = new_mat("M_Puddle")
    b = N["Principled BSDF"]
    b.inputs["Base Color"].default_value = C("#2E3A48")
    b.inputs["Roughness"].default_value = 0.04
    rip = N.new("ShaderNodeTexNoise")
    rip.noise_dimensions = "4D"
    rip.inputs["Scale"].default_value = 18
    drive_frame(rip.inputs["W"], "frame/6")
    bump = N.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.15
    L.new(rip.outputs["Fac"], bump.inputs["Height"])
    L.new(bump.outputs["Normal"], b.inputs["Normal"])
    assign(pud, pm)


def flower_mats(name, vivid):
    """Material hoa: héo (xỉn) -> tươi khi Bloom tăng."""
    m, N, L = new_mat(name)
    b = N["Principled BSDF"]
    mix = N.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    dull = list(vivid)
    lum = 0.3 * vivid[0] + 0.55 * vivid[1] + 0.15 * vivid[2]
    dull = (lerp(lum, vivid[0], 0.25) * 0.75, lerp(lum, vivid[1], 0.25) * 0.65, lerp(lum, vivid[2], 0.25) * 0.5, 1)
    rgba(mix, "A").default_value = dull
    rgba(mix, "B").default_value = vivid
    bloom = keyed_value(N, "Bloom", [(1, 0.0), (PERK0, 0.0), (PERK1, 1.0)])
    L.new(bloom, mix.inputs["Factor"])
    L.new(rgba(mix, "Result", True), b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.6
    return m


def build_flowers():
    coll = new_collection("Flowers")
    petal_cols = ["#FF8A7A", "#FF9EC7", "#C9A2F0", "#FFD45E"]
    petal_mats = [flower_mats(f"M_Petal{i}", C(h)) for i, h in enumerate(petal_cols)]
    hero_petal = principled("M_PetalHero", C("#FF9EC7"), 0.6)
    stem_m = flower_mats("M_Stem", C("#6DBE45"))
    hero_stem = principled("M_StemHero", C("#6DBE45"), 0.6)
    center_m = principled("M_FlowerCenter", C("#FFB84D"), 0.5)

    def flower(i, pos, hero=False):
        rnd = random.Random(i * 7 + 3)
        base = empty(f"Flower{i:02d}", coll, loc=(pos.x, pos.y, height(pos.x, pos.y) - 0.01))
        base.rotation_euler.z = rnd.uniform(0, math.tau)
        s = rnd.uniform(0.85, 1.35) * (1.25 if hero else 1)
        base.scale = (s, s, s)
        sm = hero_stem if hero else stem_m
        child(cylinder(f"F{i:02d}_stem1", 0.008, 0.2, sm, coll, seg=8), base, (0, 0, 0.1))
        leaf = child(sphere(f"F{i:02d}_leaf", 0.04, sm, coll, 12, 6), base, (0.03, 0, 0.06),
                     (0, -0.6, 0), (1, 0.35, 0.12))
        leaf.rotation_euler.z = rnd.uniform(0, 3)
        mid = empty(f"F{i:02d}_mid", coll, base, (0, 0, 0.2))
        child(cylinder(f"F{i:02d}_stem2", 0.007, 0.16, sm, coll, seg=8), mid, (0, 0, 0.08))
        head = empty(f"F{i:02d}_head", coll, mid, (0, 0, 0.16), (0.25, 0, 0))
        child(sphere(f"F{i:02d}_ctr", 0.022, center_m, coll, 16, 8), head, (0, 0, 0.0), scale=(1, 1, 0.7))
        pm = hero_petal if hero else petal_mats[i % len(petal_mats)]
        for k in range(6):
            a = k / 6 * math.tau
            child(sphere(f"F{i:02d}_p{k}", 0.03, pm, coll, 12, 6), head,
                  (math.cos(a) * 0.035, math.sin(a) * 0.035, -0.004), (0, 0.15, a), (1.0, 0.5, 0.18))
        droop = 0.2 if hero else rnd.uniform(1.4, 1.9)
        if hero:
            mid.rotation_euler.x = droop
        else:
            t0 = PERK0 + rnd.randint(0, 50)
            keys(mid, "rotation_euler", [(1, (droop, 0, 0)), (t0, (droop, 0, 0)), (t0 + 30, (-0.12, 0, 0)),
                                         (t0 + 40, (0.08, 0, 0)), (t0 + 50, (0, 0, 0))])

    flower(0, HERO_FLOWER, hero=True)
    cams = [Vector(p) for p in ((-0.42, -2.25), (1.6, -2.6), (-0.25, -1.05), (1.15, -1.95), (0.35, -3.0))]
    placed, tries = 1, 0
    while placed < 30 and tries < 3000:
        tries += 1
        a, r = random.uniform(0, math.tau), random.uniform(0.95, 3.4)
        p = Vector((math.cos(a) * r, math.sin(a) * r, 0))
        if p.y < -0.3 and -1.0 < p.x < 1.4 and r < 2.6:
            continue
        if (p.xy - PIKO_HOME.xy).length < 0.55 or any((p.xy - c).length < 0.6 for c in cams):
            continue
        if (p.xy - HERO_FLOWER.xy).length < 0.35 or (p.xy - Vector((-0.75, 0.2))).length < 0.3:
            continue
        flower(placed, p)
        placed += 1


def build_village():
    stem_m = principled("M_MushStem", C("#F3E3C3"), 0.7)
    door_m = principled("M_Door", C("#7A5236"), 0.6)
    dot_m = principled("M_Dot", C("#FFF8EE"), 0.5)
    win_m, _ = emissive("M_Window", C("#FFD27A"), 0.6)
    caps = ["#E8655A", "#F2A65A", "#B48EE0", "#E8655A", "#7FC8A9"]
    for i, (x, y, s) in enumerate(HOUSE_SPOTS):
        root = empty(f"House{i}", ENV, loc=(x, y, height(x, y) - 0.05))
        root.scale = (s, s, s)
        root.rotation_euler.z = facing(-x, -y)   # cửa nhìn về phía máy
        child(cylinder(f"H{i}_stem", 0.6, 1.3, stem_m, ENV, 40, r2=0.5), root, (0, 0, 0.65))
        child(rbox(f"H{i}_door", (0.34, 0.08, 0.55), 0.12, door_m, ENV), root, (0, -0.56, 0.3))
        child(cylinder(f"H{i}_win", 0.11, 0.05, win_m, ENV, 24, axis="Y"), root, (0.32, -0.47, 0.95),
              (0, 0, 0.55))
        cap_m = principled(f"M_Cap{i}", C(caps[i]), 0.55)
        child(hemisphere(f"H{i}_cap", 1.0, cap_m, ENV), root, (0, 0, 1.2), scale=(1.25, 1.25, 0.75))
        rnd = random.Random(i)
        for k in range(9):
            a, el = rnd.uniform(0, math.tau), rnd.uniform(0.3, 1.2)
            p = Vector((math.cos(a) * math.cos(el) * 1.25, math.sin(a) * math.cos(el) * 1.25,
                        1.2 + math.sin(el) * 0.75))
            d = child(sphere(f"H{i}_dot{k}", 0.13, dot_m, ENV, 12, 6), root, p, scale=(1, 1, 0.35))
            d.rotation_euler = (p - Vector((0, 0, 1.2))).to_track_quat("Z", "Y").to_euler()


# ---------------------------------------------------------------- asset Quaternius (CC0)
NATURE = os.path.join(ASSETS, "stylized_nature_megakit", "glTF")
PROPS = os.path.join(ASSETS, "fantasy_props_megakit", "Exports", "glTF")
MONSTERS = os.path.join(ASSETS, "cute_animated_monsters", "glTF")
CAM_SPOTS = [Vector(p) for p in ((-0.42, -2.25), (1.6, -2.6), (-0.22, -1.08), (1.2, -2.0), (-1.15, -2.95),
                                 (2.8, -6.5), (-5.4, -8.8))]


def free_spot(p, near_r=3.6):
    """Chỗ trống: không chắn tầm nhìn camera, không đè máy, Piko hay nhà nấm."""
    r = p.length
    if r < 1.3 or (p.y < -0.3 and -1.6 < p.x < 2.2 and r < near_r):
        return False
    if any((p - c).length < 1.0 for c in CAM_SPOTS):
        return False
    return all((p - Vector((x, y))).length > 1.9 * s for x, y, s in HOUSE_SPOTS)


def scatter(rnd, n, rmin, rmax, ok=free_spot):
    pts = []
    while len(pts) < n:
        a, r = rnd.uniform(0, math.tau), rnd.uniform(rmin, rmax)
        p = Vector((math.cos(a) * r, math.sin(a) * r))
        if ok(p):
            pts.append(p)
    return pts


def build_vegetation():
    lib = {}

    def src(name, folder=NATURE):
        if name not in lib:
            lib[name] = asset_collection(os.path.join(folder, name + ".gltf"), "SRC_" + name)
        return lib[name]

    rnd = random.Random(21)
    veg = new_collection("Vegetation")

    # cây: khô ở mép thung lũng, xanh và thông ở đồi xa
    def far_ok(p):
        return not (p.y < -6 and abs(p.x) < 14) and free_spot(p)

    groups = [("DeadTree", 12, 10, 19, 0.42, 0.65), ("CommonTree", 30, 14, 45, 0.6, 0.95), ("Pine", 14, 22, 48, 0.7, 1.0)]
    for base, n, r0, r1, s0, s1 in groups:
        for i, p in enumerate(scatter(rnd, n, r0, r1, far_ok)):
            instance(src(f"{base}_{rnd.randint(1, 5)}"), f"{base}{i:02d}", (p.x, p.y, height(p.x, p.y) - 0.15),
                     rnd.uniform(0, math.tau), rnd.uniform(s0, s1), veg)
    # cỏ khô, đá, sỏi trong vườn và quanh thung lũng
    for i, p in enumerate(scatter(rnd, 130, 2.0, 16)):
        kind = rnd.choice(["Grass_Wispy_Short", "Grass_Wispy_Tall", "Grass_Wispy_Short"])
        instance(src(kind), f"Grass{i:03d}", (p.x, p.y, height(p.x, p.y) - 0.02), rnd.uniform(0, math.tau),
                 rnd.uniform(0.22, 0.42), veg)
    for i, p in enumerate(scatter(rnd, 14, 2.6, 11)):
        instance(src(f"Rock_Medium_{rnd.randint(1, 3)}"), f"Rock{i:02d}", (p.x, p.y, height(p.x, p.y) - 0.05),
                 rnd.uniform(0, math.tau), rnd.uniform(0.12, 0.28), veg)
    for i, p in enumerate(scatter(rnd, 22, 1.6, 6)):
        instance(src(f"Pebble_Round_{rnd.randint(1, 5)}"), f"Pebble{i:02d}", (p.x, p.y, height(p.x, p.y) - 0.02),
                 rnd.uniform(0, math.tau), rnd.uniform(0.08, 0.16), veg)
    # nấm mọc quanh chân nhà nấm
    for h, (x, y, s) in enumerate(HOUSE_SPOTS):
        for k in range(3):
            a = rnd.uniform(0, math.tau)
            p = Vector((x, y)) + Vector((math.cos(a), math.sin(a))) * (1.0 * s + rnd.uniform(0.2, 0.6))
            instance(src("Mushroom_Common"), f"Mush{h}{k}", (p.x, p.y, height(p.x, p.y)), rnd.uniform(0, math.tau),
                     rnd.uniform(0.8, 1.5), veg)

    # đạo cụ: cái xô gỗ rỗng (hạn hán), thùng, sọt cà rốt, ghế dài cạnh nhà
    props = [("Bucket_Wooden_1", (-1.32, 0.05), 0.7, 1.1), ("Barrel", (-3.1, 4.0), 0.3, 0.9),
             ("FarmCrate_Carrot", (4.3, 4.1), -0.5, 0.9), ("Bench", (-6.3, 2.2), 1.2, 0.9),
             ("Barrel_Apples", (6.9, -0.6), 2.0, 0.85)]
    for name, (x, y), rz, s in props:
        instance(src(name, PROPS), name, (x, y, height(x, y) - 0.01), rz, s, veg)


def build_critters():
    """4 sinh vật nhỏ của thung lũng: đứng xem (Idle), máy gầm thì giật mình (No), mưa xuống thì nhảy múa."""
    crit = new_collection("Critters")
    spots = [("Cactus", (-2.3, 1.7)), ("Chicken", (2.5, 1.9)), ("Mushroom", (-3.2, -0.3)), ("Pig", (3.4, 0.4))]
    rnd = random.Random(9)
    for i, (name, (x, y)) in enumerate(spots):
        new, acts = import_file(os.path.join(MONSTERS, name + ".gltf"))
        junk = [o for o in new if o.name.startswith("Icosphere") and o.parent is None]   # quả cầu thừa 2m
        new = [o for o in new if o not in junk]
        for o in junk:
            bpy.data.objects.remove(o)
        root = empty(f"Critter_{name}", crit, loc=(x, y, height(x, y)))
        root.rotation_euler.z = facing(-x, -y) + rnd.uniform(-0.3, 0.3)
        s = 0.42 / 1.64
        root.scale = (s, s, s)
        for o in new:
            for c in list(o.users_collection):
                c.objects.unlink(o)
            crit.objects.link(o)
            if o.parent is None:
                o.parent = root
        arm = next(o for o in new if o.type == "ARMATURE")
        off = rnd.randint(0, 40)
        nla_sequence(arm, acts, [("Idle", 1 - off, PRESS + 8), ("No", PRESS + 10, PRESS + 46),
                                 ("Idle", PRESS + 48, RAIN_LIGHT + 10 + 2 * i),
                                 ("Dance", RAIN_LIGHT + 12 + 2 * i, FRAMES + 20)])


# ---------------------------------------------------------------- Rain-O-Matic 3000
def build_machine():
    mint = principled("M_Mint", C("#72D5B5"), 0.32, **{"Coat Weight": 0.3})
    orange = principled("M_Orange", C("#FFB84D"), 0.35, **{"Coat Weight": 0.3})
    teal = principled("M_Teal", C("#397D78"), 0.4)
    ivory = principled("M_Ivory", C("#E9F5E8"), 0.4)
    white = principled("M_NozzleWhite", C("#F4F8FB"), 0.45)
    glass = principled("M_Glass", C("#E6FBFF"), 0.02, **{"Transmission Weight": 1.0, "IOR": 1.45})
    dark = principled("M_Screen", C("#0E1C24"), 0.15)

    root = empty("RainOMatic", MACH)
    body = child(cylinder("Body", 0.45, 0.8, mint, MACH, 64), root, (0, 0, 0.45))
    bev = body.modifiers.new("Bevel", "BEVEL")
    bev.width, bev.segments, bev.limit_method = 0.05, 4, "ANGLE"
    for z in (0.85, 0.1):
        bm = bmesh.new()
        bmesh.ops.create_cone(bm, cap_ends=False, segments=64, radius1=0.46, radius2=0.46, depth=0.04)
        child(assign(mesh_obj(f"Band{z}", bm, MACH), orange), root, (0, 0, z))
    for k in range(3):
        a = math.radians(30 + 120 * k)
        child(sphere(f"Foot{k}", 0.09, orange, MACH, 24, 12), root, (math.cos(a) * 0.34, math.sin(a) * 0.34, 0.06),
              scale=(1, 1, 0.7))

    # vòm kính + lõi tinh thể
    child(hemisphere("Dome", 0.36, glass, MACH, 48, 24), root, (0, 0, 0.85))
    child(cylinder("Pedestal", 0.1, 0.06, teal, MACH, 32), root, (0, 0, 0.88))
    core_m, N, L = new_mat("M_Core")
    N.remove(N["Principled BSDF"])
    em = N.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = C("#74E5EA")
    key_socket(em.inputs["Strength"], [(1, 4.0), (PRESS + 2, 4.0), (PRESS + 10, 40.0), (FRAMES, 30.0)])
    L.new(em.outputs[0], N["Material Output"].inputs["Surface"])
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.105)
    core = child(assign(mesh_obj("Core", bm, MACH, smooth=False), core_m), root, (0, 0, 1.03), scale=(1, 1, 1.5))
    keys(core, "rotation_euler", [(1, (0, 0, 0)), (PRESS, (0, 0, PRESS * 0.03)),
                                  (FRAMES, (0, 0, PRESS * 0.03 + (FRAMES - PRESS) * 0.3))], interp="LINEAR")
    ld = bpy.data.lights.new("CoreLight", "POINT")
    ld.color, ld.shadow_soft_size = C("#74E5EA")[:3], 0.08
    keys(ld, "energy", [(1, 6.0), (PRESS + 2, 6.0), (PRESS + 10, 90.0), (FRAMES, 70.0)])
    child(link_obj(bpy.data.objects.new("CoreLight", ld), MACH), root, (0, 0, 1.03))

    # ống dẫn hơi vòng qua vòm lên vòi mây + ống hút xuống đất
    pipe = curve_tube("Pipe", [(0.36, 0.12, 0.72), (0.5, 0.1, 1.08), (0.4, 0.05, 1.42), (0.14, 0.0, 1.58)],
                      0.045, orange, MACH)
    child(pipe, root)
    hose = curve_tube("Hose", [(-0.4, 0.12, 0.38), (-0.6, 0.18, 0.26), (-0.72, 0.25, 0.08), (-0.86, 0.3, 0.02)],
                      0.04, teal, MACH)
    child(hose, root)
    child(cylinder("HoseMouth", 0.07, 0.05, teal, MACH, 24, r2=0.05), root, (-0.88, 0.31, 0.03))
    noz = metacloud("NozzleCloud", [(-0.15, 0, 1.6, 0.17), (0, 0, 1.66, 0.22), (0.15, 0, 1.61, 0.17),
                                    (0.06, 0.06, 1.72, 0.15), (-0.07, -0.05, 1.7, 0.15)], white, MACH, 0.02)
    child(noz, root)
    # ăng-ten
    child(cylinder("Antenna", 0.012, 0.42, teal, MACH, 12), root, (-0.26, 0.16, 1.05))
    tip_m, N, L = new_mat("M_AntennaTip")
    b = N["Principled BSDF"]
    b.inputs["Base Color"].default_value = C("#FFB84D")
    b.inputs["Emission Color"].default_value = C("#FFB84D")
    armed = keyed_value(N, "Armed", [(1, 0.0), (PRESS, 0.0), (PRESS + 1, 1.0)])
    set_interp(tip_m.node_tree, "default_value", "CONSTANT")
    L.new(mix_float(N, L, armed, osc(N, L, 0.25, 0.0, 3.0), osc(N, L, 1.6, 0.0, 12.0)), b.inputs["Emission Strength"])
    child(sphere("AntennaTip", 0.035, tip_m, MACH, 16, 8), root, (-0.26, 0.16, 1.28))

    # bảng tên
    child(rbox("Plaque", (0.36, 0.03, 0.13), 0.012, orange, MACH), root, (0, -0.445, 0.66))
    child(text_obj("Label1", "RAIN-O-MATIC", 0.042, teal, MACH), root, (0, -0.462, 0.676), (math.pi / 2, 0, 0))
    child(text_obj("Label2", "3000", 0.034, teal, MACH), root, (0, -0.462, 0.625), (math.pi / 2, 0, 0))

    # bảng điều khiển nghiêng
    panel = empty("Panel", MACH, root, PANEL_LOC, (PANEL_TILT, 0, 0))
    child(rbox("PanelBox", (0.46, 0.12, 0.25), 0.03, ivory, MACH), panel)
    child(rbox("ScreenBg", (0.22, 0.01, 0.075), 0.008, dark, MACH), panel, (0, -0.062, 0.062))
    lvl_m, lvl_em = emissive("M_TextLevel", C("#7CFF9A"), 4.0)
    max_m, N, L = new_mat("M_TextMax")
    N.remove(N["Principled BSDF"])
    em = N.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = C("#FF4A3D")
    L.new(osc(N, L, 1.1, 1.0, 9.0), em.inputs["Strength"])
    L.new(em.outputs[0], N["Material Output"].inputs["Surface"])
    t_lvl = child(text_obj("TxtLevel", "LEVEL 1", 0.034, lvl_m, MACH), panel, (0, -0.069, 0.062), (math.pi / 2, 0, 0))
    t_max = child(text_obj("TxtMax", "MAX POWER!", 0.028, max_m, MACH), panel, (0, -0.069, 0.062),
                  (math.pi / 2, 0, 0))
    visible_between(t_lvl, 1, PRESS + 1)
    visible_between(t_max, PRESS + 1, FRAMES + 1)

    dial = empty("Dial", MACH, panel, (-0.12, -0.062, -0.035))
    child(cylinder("DialKnob", 0.045, 0.03, teal, MACH, 32, axis="Y"), dial)
    child(rbox("DialPointer", (0.01, 0.012, 0.04), 0.003, orange, MACH), dial, (0, -0.018, 0.022))
    keys(dial, "rotation_euler", [(1, (0, 1.0, 0)), (PRESS + 1, (0, 1.0, 0)), (PRESS + 6, (0, -1.45, 0)),
                                  (PRESS + 9, (0, -1.15, 0)), (PRESS + 12, (0, -1.3, 0))])

    button = empty("Button", MACH, panel, BUTTON_LOCAL)
    yellow = principled("M_ButtonRing", C("#FFE16A"), 0.4)
    child(cylinder("ButtonRing", 0.062, 0.018, yellow, MACH, 40, axis="Y"), button)
    cap_m, N, L = new_mat("M_ButtonCap")
    b = N["Principled BSDF"]
    b.inputs["Base Color"].default_value = C("#E8251B")
    b.inputs["Roughness"].default_value = 0.22
    b.inputs["Coat Weight"].default_value = 0.6
    b.inputs["Emission Color"].default_value = C("#FF3B30")
    armed = keyed_value(N, "Armed", [(1, 0.0), (PRESS, 0.0), (PRESS + 1, 1.0)])
    L.new(mix_float(N, L, armed, osc(N, L, 0.42, 0.05, 1.4), osc(N, L, 1.3, 0.8, 3.0)), b.inputs["Emission Strength"])
    cap = child(sphere("ButtonCap", 0.046, cap_m, MACH, 32, 16), button, (0, -0.014, 0), scale=(1, 0.55, 1))
    keys(cap, "location", [(1, (0, -0.014, 0)), (PRESS - 2, (0, -0.014, 0)), (PRESS + 1, (0, -0.001, 0))])

    # máy rung sau khi bật MAX
    keys(root, "location", [(1, (0, 0, 0))])
    for fc in fcurves_of(root):
        mod = fc.modifiers.new("NOISE")
        mod.scale, mod.strength = 1.3, 0.03 if fc.array_index < 2 else 0.018
        mod.phase = random.uniform(0, 50)
        mod.use_restricted_range = True
        mod.frame_start, mod.frame_end, mod.blend_in = PRESS + 4, FRAMES, 8

    return root, BUTTON_WORLD


# ---------------------------------------------------------------- Piko
def build_piko():
    r = 0.25
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=48, v_segments=28, radius=r)
    for v in bm.verts:
        x, y, z = v.co
        if z > 0:   # đỉnh thuôn như giọt nước
            k = 1 - 0.3 * (z / r) ** 1.6
            x, y, z = x * k, y * k, z * 1.12
        if z < -0.16:   # đáy bẹt
            z = -0.16 + (z + 0.16) * 0.3
        v.co = Vector((x, y, z))
    zmin = min(v.co.z for v in bm.verts)
    for v in bm.verts:
        v.co.z -= zmin
    H = max(v.co.z for v in bm.verts)
    bvh = BVHTree.FromBMesh(bm)
    body_co = [v.co.copy() for v in bm.verts]

    def surf(x, z, back=False):
        o, d = (Vector((x, 1, z)), Vector((0, -1, 0))) if back else (Vector((x, -1, z)), Vector((0, 1, 0)))
        loc, nrm, _, _ = bvh.ray_cast(o, d)
        return loc, nrm

    def top(x, y):
        loc, nrm, _, _ = bvh.ray_cast(Vector((x, y, 2)), Vector((0, 0, -1)))
        return loc, nrm

    skin, N, L = new_mat("M_PikoSkin")
    b = N["Principled BSDF"]
    tc = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ")
    L.new(tc.outputs["Object"], sep.inputs[0])
    fy = N.new("ShaderNodeMapRange")
    fy.inputs["From Min"].default_value, fy.inputs["From Max"].default_value = -0.12, -0.22
    L.new(sep.outputs["Y"], fy.inputs["Value"])
    fz = N.new("ShaderNodeMapRange")
    fz.inputs["From Min"].default_value, fz.inputs["From Max"].default_value = 0.30, 0.2
    L.new(sep.outputs["Z"], fz.inputs["Value"])
    belly = N.new("ShaderNodeMix")
    belly.data_type = "RGBA"
    L.new(math_node(N, L, "MULTIPLY", fy.outputs[0], fz.outputs[0]), belly.inputs["Factor"])
    rgba(belly, "A").default_value = C("#58CDE0")
    rgba(belly, "B").default_value = C("#B6F0F2")
    L.new(rgba(belly, "Result", True), b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.25
    b.inputs["Subsurface Weight"].default_value = 0.35
    b.inputs["Subsurface Radius"].default_value = (0.3, 0.7, 0.9)
    b.inputs["Subsurface Scale"].default_value = 0.05
    b.inputs["Coat Weight"].default_value = 0.6
    b.inputs["Coat Roughness"].default_value = 0.08

    root = empty("Piko", PIKO_C, loc=PIKO_HOME)
    body = mesh_obj("PikoBody", bm, PIKO_C)
    assign(body, skin)
    child(body, root)

    # shape key "Bulge": phần lưng phình ra (dùng để đè nút)
    body.shape_key_add(name="Basis")
    sk = body.shape_key_add(name="Bulge", from_mix=False)
    zc = H * 0.5
    for i, co in enumerate(body_co):
        w = max(0.0, co.y / r) ** 1.3 * math.exp(-((co.z - zc) / 0.14) ** 2)
        sk.data[i].co = co + Vector((0, 0.2 * w, 0.11 * w))

    # mắt
    white = principled("M_EyeWhite", (1, 1, 1, 1), 0.12, **{"Coat Weight": 0.5})
    iris_m = principled("M_Iris", C("#286A83"), 0.2)
    pupil_m = principled("M_Pupil", C("#0B1820"), 0.1)
    hl_m, _ = emissive("M_EyeHL", (1, 1, 1, 1), 1.6)
    eyes = []
    for side, x in (("L", 0.085), ("R", -0.085)):
        p, n = surf(x, H * 0.6)
        piv = empty(f"Eye{side}", PIKO_C, body, p - n * 0.02)
        child(sphere(f"EyeWhite{side}", 0.062, white, PIKO_C, 32, 16), piv)
        child(sphere(f"Iris{side}", 0.036, iris_m, PIKO_C, 24, 12), piv, (0, -0.05, 0), scale=(1, 0.38, 1))
        child(sphere(f"Pupil{side}", 0.021, pupil_m, PIKO_C, 16, 8), piv, (0, -0.058, 0), scale=(1, 0.3, 1))
        child(sphere(f"Glint{side}", 0.011, hl_m, PIKO_C, 12, 6), piv, (-0.014, -0.06, 0.018))
        eyes.append(piv)

    # miệng, má, sừng, ngôi sao
    mouth_m = principled("M_Mouth", C("#173445"), 0.4)
    p, n = surf(0, H * 0.4)
    mouth = child(sphere("Mouth", 1.0, mouth_m, PIKO_C, 24, 12), body, p + n * 0.002, scale=(0.04, 0.01, 0.012))
    blush = principled("M_Blush", C("#FF9EB5"), 0.5)
    for side, x in (("L", 0.15), ("R", -0.15)):
        p, n = surf(x, H * 0.47)
        c = child(sphere(f"Cheek{side}", 1.0, blush, PIKO_C, 16, 8), body, p + n * 0.001, scale=(0.028, 0.006, 0.016))
        c.rotation_euler = n.to_track_quat("-Y", "Z").to_euler()
    horn_m = skin
    tip_m = principled("M_HornTip", C("#FFE16A"), 0.35)
    for side, x in (("L", 0.075), ("R", -0.075)):
        p, n = top(x, 0.0)
        axis = (n + Vector((x * 3, 0, 0))).normalized()
        h = child(cylinder(f"Horn{side}", 0.034, 0.08, horn_m, PIKO_C, 20, r2=0.014), body, p + axis * 0.03)
        h.rotation_euler = axis.to_track_quat("Z", "Y").to_euler()
        child(sphere(f"HornTip{side}", 0.016, tip_m, PIKO_C, 12, 6), body, p + axis * 0.075)
    star_m = principled("M_Star", C("#FFE16A"), 0.35, **{"Emission Color": C("#FFE16A"), "Emission Strength": 0.4})
    sbm = bmesh.new()
    pts = [sbm.verts.new((math.cos(math.pi / 2 + k * math.pi / 5) * (0.03 if k % 2 == 0 else 0.013),
                          0, math.sin(math.pi / 2 + k * math.pi / 5) * (0.03 if k % 2 == 0 else 0.013)))
           for k in range(10)]
    f = sbm.faces.new(pts)
    bmesh.ops.extrude_face_region(sbm, geom=[f])
    sbm.verts.ensure_lookup_table()
    for v in sbm.verts[10:]:
        v.co.y += 0.006
    p, n = surf(0, H * 0.82)
    star = child(assign(mesh_obj("Star", sbm, PIKO_C, smooth=False), star_m), body, p - n * 0.002)
    star.rotation_euler = n.to_track_quat("-Y", "Z").to_euler()
    return root, body, eyes, mouth, H


def animate_piko(root, body, eyes, mouth, H, button_world):
    def face(frames_psi):
        keys(root, "rotation_euler", [(f, (0, 0, psi)) for f, psi in frames_psi])

    def squash(frames_sz):
        keys(body, "scale", [(f, (sxy, sxy, sz)) for f, sxy, sz in frames_sz])

    def lean(frames_ax):
        keys(body, "rotation_euler", [(f, (ax, 0, 0)) for f, ax in frames_ax])

    def hop(frames_xyz):
        keys(root, "location", [(f, Vector(p)) for f, p in frames_xyz])

    def look(frames_targets):
        """Xoay hai mắt nhìn về điểm world (ước lượng theo hướng thân ở frame đó)."""
        for f, psi, tgt in frames_targets:
            src = PIKO_HOME + Vector((0, 0, H * 0.6))
            d = Vector(tgt) - src
            c, s = math.cos(-psi), math.sin(-psi)
            lx, ly = c * d.x - s * d.y, s * d.x + c * d.y
            a = max(-0.45, min(0.45, math.atan2(lx, -ly)))
            bta = max(-0.45, min(0.45, -math.atan2(d.z, math.hypot(lx, ly))))
            for e in eyes:
                e.rotation_euler = (bta, 0, a)
                e.keyframe_insert("rotation_euler", frame=f)

    def eye_scale(frames_s):
        for e in eyes:
            keys(e, "scale", [(f, s) for f, s in frames_s])

    def mouth_shape(frames_s):
        keys(mouth, "scale", [(f, s) for f, s in frames_s])

    home = tuple(PIKO_HOME)
    psi_idle = facing(-0.6, -0.8)
    psi_btn = facing(-0.95, -0.3)
    psi_away = facing(-TO_BUTTON.x, -TO_BUTTON.y)
    psi_mach = facing(-0.7, -0.7)
    psi_cam7 = facing(0.66, -1.29)
    back = LAND - PIKO_HOME
    land2 = tuple(LAND)
    sky = (0.2, 0.5, 6.0)

    # S1 - nhún nhảy tò mò
    face([(1, psi_idle), (96, psi_idle), (100, psi_idle), (108, psi_btn), (217, psi_btn), (229, psi_away),
          (341, psi_away), (348, psi_mach - 0.15), (352, psi_mach), (470, psi_mach), (490, psi_cam7 - 0.4),
          (577, psi_cam7), (FRAMES, psi_cam7)])
    hop([(1, home), (28, home), (34, (home[0], home[1], 0.1)), (40, home), (62, home), (68, (home[0], home[1], 0.1)),
         (74, home), (240, home), (246, (home[0], home[1], 0.22)), (252, home), (272, home),
         (281, (home[0] + back.x * 0.5, home[1] + back.y * 0.5, 0.34)), (292, land2), (500, land2),
         (507, (land2[0], land2[1], 0.12)), (514, land2), (522, land2), (529, (land2[0], land2[1], 0.12)),
         (536, land2), (586, land2), (592, (land2[0], land2[1], 0.08)), (598, land2), (FRAMES, land2)])
    squash([(1, 1, 1), (24, 1.04, 0.92), (28, 1.08, 0.85), (32, 0.94, 1.12), (40, 1.1, 0.86), (46, 1, 1),
            (58, 1.08, 0.85), (64, 0.94, 1.12), (74, 1.1, 0.86), (80, 1, 1),
            # S2 rướn tới nút
            (110, 1, 1), (150, 0.94, 1.12), (160, 0.94, 1.12), (170, 1.02, 0.97), (182, 1, 1),
            # S3 nhảy
            (228, 1, 1), (236, 1.12, 0.8), (240, 0.92, 1.2), (246, 1, 1.02), (252, 1.14, 0.8), (258, 1, 1),
            (262, 1, 1), (270, 1.16, 0.74), (274, 0.9, 1.26), (284, 1, 1.03), (292, 1.2, 0.78), (298, 1.32, 0.7),
            # S4 giữ bẹp rồi bật lại
            (312, 1.32, 0.7), (318, 0.92, 1.16), (324, 1.06, 0.92), (330, 0.98, 1.03), (336, 1, 1),
            # S5 sốc phồng to
            (350, 1, 1), (354, 1.32, 1.32), (358, 1.26, 1.26), (362, 1.3, 1.3), (400, 1.28, 1.28), (420, 1.1, 1.1),
            (470, 1, 1), (500, 1, 1), (504, 1.08, 0.9), (514, 1.08, 0.88), (520, 1, 1), (536, 1, 1),
            # S7 hứng mưa rồi BOP
            (586, 1, 1), (590, 1.06, 0.92), (598, 1.06, 0.9), (604, 1, 1), (BOP, 1, 1.02), (BOP + 3, 1.62, 0.3),
            (BOP + 9, 1.48, 0.4), (BOP + 15, 1.6, 0.29), (BOP + 21, 1.54, 0.34), (BOP + 28, 1.57, 0.31),
            (FRAMES, 1.57, 0.31)])
    lean([(1, 0), (110, 0), (150, 0.3), (160, 0.3), (168, -0.05), (182, 0), (600, 0), (614, -0.32),
          (640, -0.3), (BOP, -0.1), (BOP + 3, 0)])
    # lắc đầu "không được"
    shake = [(160, psi_btn)] + [(162 + 4 * k, psi_btn + (0.28 if k % 2 == 0 else -0.28)) for k in range(5)] + \
        [(182, psi_btn)]
    for f, psi in shake:
        root.rotation_euler = (0, 0, psi)
        root.keyframe_insert("rotation_euler", frame=f)

    tiny = tuple(TINY_CLOUD)
    look([(1, psi_idle, tiny), (90, psi_idle, tiny), (104, psi_btn, button_world), (160, psi_btn, button_world),
          (166, psi_btn, (2, -3, 0.3)), (217, psi_btn, (2, -3, 0.3)), (226, psi_away, (2, -3, 0.5)),
          (300, psi_away, (2, -3, 0.5)), (346, psi_mach, (0, 0, 1.1)), (430, psi_mach, (0, 0, 1.6)),
          (440, psi_mach, sky), (577, psi_cam7, (1.15, -1.95, 0.34)), (604, psi_cam7, (1.15, -1.95, 0.34)),
          (612, psi_cam7, (0.4, -0.2, 4)), (BOP + 20, psi_cam7, (0.4, -0.2, 4))])
    eye_scale([(1, (1, 1, 1)), (58, (1, 1, 1)), (60, (1, 1, 0.1)), (63, (1, 1, 1)), (128, (1, 1, 1)),
               (130, (1, 1, 0.1)), (133, (1, 1, 1)), (350, (1, 1, 1)), (354, (1.3, 1.3, 1.35)), (420, (1.3, 1.3, 1.35)),
               (440, (1, 1, 1)), (468, (1, 1, 1)), (470, (1, 1, 0.1)), (473, (1, 1, 1)), (BOP, (1, 1, 1)),
               (BOP + 3, (0.72, 0.72, 2.1)), (686, (0.72, 0.72, 2.1)), (688, (0.72, 0.72, 0.25)),
               (692, (0.72, 0.72, 2.1)), (708, (0.72, 0.72, 2.1)), (710, (0.72, 0.72, 0.25)), (714, (0.72, 0.72, 2.1))])
    smile, line, o_small, o_big, grin = (0.04, 0.01, 0.012), (0.03, 0.01, 0.006), (0.02, 0.01, 0.02), \
        (0.04, 0.012, 0.055), (0.055, 0.01, 0.018)
    mouth_shape([(1, smile), (140, smile), (150, o_small), (162, line), (190, line), (200, smile), (222, smile),
                 (228, grin), (300, grin), (350, grin), (354, o_big), (420, o_big), (440, o_small), (500, smile),
                 (506, grin), (540, grin), (604, smile), (612, o_big), (BOP, o_big), (BOP + 3, line),
                 (FRAMES, line)])
    key = body.data.shape_keys.key_blocks["Bulge"]
    for f, v in [(1, 0.0), (292, 0.0), (300, 0.8), (306, 1.0), (312, 1.0), (320, 0.0)]:
        key.value = v
        key.keyframe_insert("value", frame=f)


# ---------------------------------------------------------------- weather FX
def build_fx(piko_body, H):
    cloud_m, N, L = new_mat("M_Cloud")
    b = N["Principled BSDF"]
    key_socket(b.inputs["Base Color"], [(1, C("#FFFFFF")), (STORM0, C("#F2F4F7")), (STORM1, C("#6E7784")),
                                        (FRAMES, C("#646D7A"))])
    b.inputs["Roughness"].default_value = 1.0
    b.inputs["Subsurface Weight"].default_value = 0.2
    b.inputs["Subsurface Radius"].default_value = (1, 1, 1)
    b.inputs["Subsurface Scale"].default_value = 0.3

    # mây tí hon tưới hoa (lúc máy chạy Level 1) -> lớn dần thành mây bão
    tiny = metacloud("TinyCloud", cloud_blob(0.17, 6, 1), cloud_m, FX, 0.025)
    keys(tiny, "location", [(1, tuple(TINY_CLOUD)), (PRESS + 10, tuple(TINY_CLOUD)),
                            (520, (-2.0, 1.5, 9.0)), (FRAMES, (-2.5, 2.0, 9.5))])
    keys(tiny, "scale", [(1, (1, 1, 1)), (PRESS + 10, (1, 1, 1)), (520, (16, 16, 12)), (FRAMES, (17, 17, 12))])

    # cụm mây bão kéo về từ chân trời
    rnd = random.Random(5)
    for i in range(14):
        a0 = math.radians(10 + i * 12 + rnd.uniform(-5, 5))
        r0, r1 = rnd.uniform(45, 65), rnd.uniform(7, 26)
        a1 = a0 + rnd.uniform(-0.5, 0.5)
        start = (math.cos(a0) * r0, math.sin(a0) * r0, rnd.uniform(14, 20))
        end = (math.cos(a1) * r1, math.sin(a1) * r1 + 6, rnd.uniform(10, 14))
        s1 = rnd.uniform(1.7, 2.6)
        c = metacloud(f"Storm{chr(65 + i)}", cloud_blob(3.0, 8, 10 + i), cloud_m, FX, 0.35)
        t0 = STORM0 - 20 + rnd.randint(0, 40)
        keys(c, "location", [(1, start), (t0, start), (t0 + 140, end), (FRAMES, end)])
        keys(c, "scale", [(1, (0.7, 0.7, 0.5)), (t0, (0.7, 0.7, 0.5)), (t0 + 140, (s1, s1, s1 * 0.8)),
                          (FRAMES, (s1, s1, s1 * 0.8))])

    # hơi nước phụt từ vòi mây
    steam_m, N, L = new_mat("M_Steam")
    N.remove(N["Principled BSDF"])
    b = N.new("ShaderNodeBsdfDiffuse")      # khuếch tán thuần: không phản xạ -> hết đốm sáng li ti
    b.inputs["Color"].default_value = C("#F6F9FC")
    oi = N.new("ShaderNodeObjectInfo")
    tr = N.new("ShaderNodeBsdfTransparent")
    mix = N.new("ShaderNodeMixShader")
    L.new(oi.outputs["Alpha"], mix.inputs[0])
    L.new(tr.outputs[0], mix.inputs[1])
    L.new(b.outputs[0], mix.inputs[2])
    L.new(mix.outputs[0], N["Material Output"].inputs["Surface"])
    steam_m.surface_render_method = "BLENDED"
    steam_m.use_backface_culling = True          # không vẽ mặt sau của quả cầu trong suốt
    steam_m.use_transparency_overlap = False
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
    puff_me = bpy.data.meshes.new("puff")
    bm.to_mesh(puff_me)
    bm.free()
    puff_me.shade_smooth()
    puff_me.materials.append(steam_m)

    def puff(i, f0, life, p0, p1, s0, s1, a0):
        o = link_obj(bpy.data.objects.new(f"Puff{i:03d}", puff_me), FX)
        o.visible_shadow = False
        keys(o, "location", [(f0, p0), (f0 + life, p1)])
        keys(o, "scale", [(f0, (s0, s0, s0)), (f0 + life, (s1, s1, s1 * 0.85))])
        keys(o, "color", [(f0, (1, 1, 1, a0)), (f0 + int(life * 0.6), (1, 1, 1, a0 * 0.8)), (f0 + life, (1, 1, 1, 0))])
        visible_between(o, f0, f0 + life)

    i = 0
    for f0 in range(-40, PRESS, 14):      # Level 1: hơi nhẹ bay sang mây tí hon
        j = Vector((random.uniform(-0.05, 0.05), random.uniform(-0.05, 0.05), 0))
        puff(i, f0, 40, tuple(NOZZLE_TOP), tuple(TINY_CLOUD + j), 0.05, 0.15, 0.9)
        i += 1
    for f0 in range(PRESS + 6, 600, 3):    # MAX: cột hơi phụt thẳng lên trời
        j = Vector((random.uniform(-1, 1), random.uniform(-1, 1), 0))
        puff(i, f0, 70, tuple(NOZZLE_TOP + j * 0.05), tuple(Vector((0, 0, 14)) + j * 2.5),
             random.uniform(0.12, 0.2), random.uniform(1.8, 3.0), 0.95)
        i += 1

    # mưa: hạt instancing
    drop_m, N, L = new_mat("M_Rain")
    b = N["Principled BSDF"]
    b.inputs["Base Color"].default_value = C("#DDEBFA")
    b.inputs["Roughness"].default_value = 0.1
    b.inputs["Alpha"].default_value = 0.55
    b.inputs["Emission Color"].default_value = C("#DDEBFA")
    b.inputs["Emission Strength"].default_value = 0.25
    drop_m.surface_render_method = "BLENDED"

    def drop_src(name, length, rad=0.007):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=1, radius=1.0)
        for v in bm.verts:
            v.co = Vector((v.co.x * rad, v.co.y * rad, v.co.z * length))
        o = assign(mesh_obj(name, bm, FX), drop_m)
        o.location = (0, 0, -60)
        return o

    streak = drop_src("DropStreak", 0.06)
    fine = drop_src("DropFine", 0.03, 0.0028)
    dribble = drop_src("DropSmall", 0.018, 0.006)

    def emitter(name, size, loc):
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size / 2)
        o = mesh_obj(name, bm, FX)
        o.location = loc
        o.show_instancer_for_render = False
        o.show_instancer_for_viewport = False
        return o

    def rain(em, name, count, f0, f1, life, vel, src, seed):
        mod = em.modifiers.new(name, "PARTICLE_SYSTEM")
        ps = mod.particle_system
        ps.seed = seed
        st = ps.settings
        st.name = name
        st.count = count
        st.frame_end = f1
        st.frame_start = f0
        st.lifetime, st.lifetime_random = life, 0.1
        st.emit_from, st.distribution = "FACE", "RAND"
        st.physics_type = "NEWTON"
        st.normal_factor = 0.0
        st.object_align_factor = (0, 0, -vel)
        st.factor_random = vel * 0.04
        st.effector_weights.gravity = 0.0
        st.render_type, st.instance_object = "OBJECT", src
        st.particle_size, st.size_random = 1.0, 0.35
        st.display_method = "DOT"

    sky = emitter("RainEmitter", 40, (0, -1, 11))
    rain(sky, "RainLight", 6000, RAIN_LIGHT, FRAMES, 22, 14, streak, 1)
    rain(sky, "RainHeavy", 30000, RAIN_HEAVY, FRAMES, 22, 15, streak, 2)
    near = emitter("RainNear", 3.5, (0.8, -1.3, 3.2))
    rain(near, "RainClose", 6000, 560, FRAMES, 8, 12, fine, 3)
    driz = emitter("DrizzleEmitter", 0.3, tuple(TINY_CLOUD - Vector((0, 0, 0.14))))
    rain(driz, "Drizzle", 260, 1, PRESS + 30, 30, 2.2, dribble, 4)

    # giọt mưa to "BOP" + bắn tung tóe
    big_m = principled("M_BigDrop", C("#BFE6FF"), 0.04, **{"Coat Weight": 1.0, "Transmission Weight": 0.5})
    top = LAND + Vector((0, 0, H))
    big = sphere("BigDrop", 0.055, big_m, FX, 24, 12)
    big.scale = (1, 1, 1.35)
    keys(big, "location", [(BOP - 22, tuple(top + Vector((0, 0, 2.8)))), (BOP, tuple(top))], interp="LINEAR")
    visible_between(big, BOP - 22, BOP + 1)
    for k in range(8):
        a = k / 8 * math.tau + 0.2
        s = sphere(f"Splash{k}", 0.018, big_m, FX, 12, 6)
        p0 = top - Vector((0, 0, H * 0.68))
        out = Vector((math.cos(a), math.sin(a), 0))
        keys(s, "location", [(BOP + 1, tuple(p0 + out * 0.08)), (BOP + 6, tuple(p0 + out * 0.32 + Vector((0, 0, 0.16)))),
                             (BOP + 12, tuple(p0 + out * 0.5 - Vector((0, 0, 0.08))))])
        visible_between(s, BOP + 1, BOP + 12)

    # sét
    bolt_m, _ = emissive("M_Bolt", C("#E8F0FF"), 60.0)
    for n, (f, base) in enumerate(zip(FLASHES, ((-13, 42), (16, 38)))):
        pts, x, y = [], base[0], base[1]
        for k in range(9):
            pts.append((x + random.uniform(-1.6, 1.6), y + random.uniform(-0.5, 0.5), 26 - k * 3))
        bolt = curve_tube(f"Bolt{n}", pts, 0.18, bolt_m, FX, kind="POLY")
        visible_between(bolt, f, f + 3)


# ---------------------------------------------------------------- sky & lights
def build_sky():
    w = bpy.data.worlds.new("Sky")
    scene.world = w
    N, L = w.node_tree.nodes, w.node_tree.links
    N.clear()
    out = N.new("ShaderNodeOutputWorld")
    tc = N.new("ShaderNodeTexCoord")
    sep = N.new("ShaderNodeSeparateXYZ")
    L.new(tc.outputs["Generated"], sep.inputs[0])
    grad = N.new("ShaderNodeMapRange")
    grad.inputs["From Min"].default_value, grad.inputs["From Max"].default_value = -0.05, 0.6
    L.new(sep.outputs["Z"], grad.inputs["Value"])
    zen, hor = N.new("ShaderNodeRGB"), N.new("ShaderNodeRGB")
    zen.label, hor.label = "Zenith", "Horizon"
    sky = N.new("ShaderNodeMix")
    sky.data_type = "RGBA"
    L.new(grad.outputs[0], sky.inputs["Factor"])
    L.new(hor.outputs[0], rgba(sky, "A"))
    L.new(zen.outputs[0], rgba(sky, "B"))
    flash = N.new("ShaderNodeValue")
    flash.label = "Flash"
    fl = N.new("ShaderNodeMix")
    fl.data_type = "RGBA"
    fl.blend_type = "ADD"
    L.new(flash.outputs[0], fl.inputs["Factor"])
    L.new(rgba(sky, "Result", True), rgba(fl, "A"))
    rgba(fl, "B").default_value = (0.8, 0.85, 1.0, 1)
    bg = N.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = 0.75
    L.new(rgba(fl, "Result", True), bg.inputs["Color"])
    L.new(bg.outputs[0], out.inputs["Surface"])
    key_socket(zen.outputs[0], [(1, C("#4E9FE6")), (STORM0, C("#4E9FE6")), (STORM1, C("#3C4654")),
                                (FRAMES, C("#38414E"))])
    key_socket(hor.outputs[0], [(1, C("#F6E7C1")), (STORM0, C("#F6E7C1")), (STORM1, C("#737D8B")),
                                (FRAMES, C("#6C7684"))])
    fk = [(1, 0.0)]
    for f in FLASHES:
        fk += [(f - 1, 0.0), (f, 1.2), (f + 2, 0.2), (f + 3, 0.9), (f + 6, 0.0)]
    key_socket(flash.outputs[0], fk)
    set_interp(w.node_tree, "default_value", "LINEAR")

    sd = bpy.data.lights.new("Sun", "SUN")
    sd.angle = math.radians(3)
    sun = link_obj(bpy.data.objects.new("Sun", sd), ENV)
    sun.rotation_euler = Vector((0.45, 0.55, -0.7)).to_track_quat("-Z", "Y").to_euler()
    ek = [(1, 5.0), (STORM0, 5.0), (STORM1, 1.5), (FRAMES, 1.4)]
    for f in FLASHES:
        ek += [(f - 1, 1.5), (f, 7.0), (f + 2, 1.8), (f + 3, 5.0), (f + 6, 1.5)]
    keys(sd, "energy", sorted(ek))
    keys(sd, "color", [(1, (1.0, 0.93, 0.8)), (STORM0, (1.0, 0.93, 0.8)), (STORM1, (0.75, 0.82, 1.0))])
    keys(scene.view_settings, "exposure", [(1, 0.0), (STORM0, 0.0), (STORM1, 0.45), (FRAMES, 0.45)])


# ---------------------------------------------------------------- cameras
def build_cameras(piko_body, button_world):
    def cam(name, shot, loc0, loc1, aim0, aim1, lens, focus=None, fstop=2.8):
        c, aim = camera(name, loc0, aim0, lens, CAMS)
        f0, f1 = SHOTS[shot]
        keys(c, "location", [(f0, loc0), (f1, loc1)])
        keys(aim, "location", [(f0, aim0), (f1, aim1)])
        if focus is not None:
            c.data.dof.use_dof = True
            if isinstance(focus, bpy.types.Object):
                c.data.dof.focus_object = focus
            else:
                c.data.dof.focus_distance = (Vector(focus) - Vector(loc0)).length
            c.data.dof.aperture_fstop = fstop
        cut_to(c, f0)
        return c, aim

    land = LAND
    s1, _ = cam("CamS1", "S1", (-5.4, -8.8, 2.1), (-4.5, -7.4, 1.8), (0.1, 0.2, 0.9), (0.1, 0.2, 0.9), 32)
    cam("CamS2", "S2", (-0.42, -2.25, 0.42), (-0.3, -1.95, 0.4), (0.3, -0.62, 0.3), (0.32, -0.62, 0.3), 42,
        piko_body, 2.8)
    cam("CamS3", "S3", (1.65, -2.65, 0.55), (1.55, -2.5, 0.5), (0.35, -0.6, 0.3), (0.32, -0.58, 0.28), 38,
        piko_body, 4.0)
    cam("CamS4", "S4", (-0.22, -1.08, 0.46), (-0.18, -1.0, 0.44), tuple(button_world), tuple(button_world), 55,
        tuple(button_world), 4.0)
    cam("CamS5", "S5", (-1.15, -2.95, 0.95), (-1.05, -2.8, 1.0), (0.15, -0.35, 0.82), (0.15, -0.35, 0.92), 30)
    cam("CamS6", "S6", (2.8, -6.5, 0.35), (2.6, -6.2, 0.35), (-0.5, 2.0, 5.5), (-0.5, 2.0, 8.5), 22)
    c7, a7 = cam("CamS7", "S7", (1.2, -2.0, 0.36), (1.12, -1.9, 0.3), tuple(land + Vector((0, 0, 0.25))),
                 tuple(land + Vector((0, 0, 0.1))), 45, piko_body, 2.8)
    keys(c7, "location", [(BOP, (1.08, -1.8, 0.36)), (BOP + 12, (1.12, -1.9, 0.3))])
    keys(a7, "location", [(BOP, tuple(land + Vector((0, 0, 0.22)))), (BOP + 10, tuple(land + Vector((0, 0, 0.1))))])
    scene.camera = s1


# ---------------------------------------------------------------- build
build_ground()
build_flowers()
build_village()
build_vegetation()
build_critters()
machine, button_world = build_machine()
piko_root, piko_body, eyes, mouth, H = build_piko()
animate_piko(piko_root, piko_body, eyes, mouth, H, button_world)
build_fx(piko_body, H)
build_sky()
build_cameras(piko_body, button_world)
setup_render(samples=32, bloom=0.5, threshold=1.2)
scene.render.resolution_percentage = 50

if os.path.exists(AUDIO_MIX):   # nhạc nền / tiếng động: mở Blender bấm Space là nghe
    scene.sequence_editor_create().strips.new_sound("Soundtrack", AUDIO_MIX, 1, 1)

scene.frame_set(1)
bpy.ops.ptcache.bake_all(bake=True)
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", OUT_BLEND, "objects:", len(bpy.data.objects), "H=", round(H, 3), "button=", tuple(round(c, 3) for c in button_world))
