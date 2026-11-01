"""
Face rig, viết và kiểm tra trên bản Lumo rig bằng Rigify: vị trí mắt, lông mày, miệng đang theo mặt bản đó,
xương đầu HEAD_BONE = "DEF-spine.006". Nhân vật mới: đo lại vị trí; rig Meshy dùng "mixamorig:Head".
Các bộ phận mặt rời gắn vào xương đầu, điều khiển bằng thuộc tính số trên rig
(keyframe được, kéo tay được). Driver chỉ dùng biểu thức đơn giản -> chạy không cần cho phép script.

Thuộc tính (đặt trên object RIG-Lumo):
  eye_open_L/R   0 nhắm .. 1 bình thường .. 1.2 trợn
  lower_lid_L/R  0 .. 1 (mí dưới đẩy lên = mắt cười ^^)
  lid_tilt_L/R   -1 rủ buồn .. +1 xếch giận
  pupil          0.6 .. 1.4 (to = dễ thương, nhỏ = sốc)
  look_x, look_z -1 .. 1 (liếc ngang / dọc)
  brow_raise_L/R -1 cau .. 1 nhướng
  brow_tilt_L/R  -1 buồn .. 1 giận
  mouth_smile, mouth_grin, mouth_open, mouth_frown, mouth_flat, mouth_wavy   0 .. 1
  blush, sweat   0 .. 1
"""
import math

import bmesh
import bpy
from mathutils import Matrix, Vector
from mathutils.bvhtree import BVHTree

HEAD_BONE = "DEF-spine.006"

PROPS = {  # tên: (mặc định, min, max)
    "eye_open_L": (1.0, 0.0, 1.25), "eye_open_R": (1.0, 0.0, 1.25),
    "lower_lid_L": (0.0, 0.0, 1.0), "lower_lid_R": (0.0, 0.0, 1.0),
    "lid_tilt_L": (0.0, -1.0, 1.0), "lid_tilt_R": (0.0, -1.0, 1.0),
    "pupil": (1.0, 0.6, 1.4), "look_x": (0.0, -1.0, 1.0), "look_z": (0.0, -1.0, 1.0),
    "brow_raise_L": (0.0, -1.0, 1.0), "brow_raise_R": (0.0, -1.0, 1.0),
    "brow_tilt_L": (0.0, -1.0, 1.0), "brow_tilt_R": (0.0, -1.0, 1.0),
    "mouth_smile": (0.0, 0.0, 1.0), "mouth_grin": (0.0, 0.0, 1.0), "mouth_open": (0.0, 0.0, 1.0),
    "mouth_frown": (0.0, 0.0, 1.0), "mouth_flat": (0.0, 0.0, 1.0), "mouth_wavy": (0.0, 0.0, 1.0),
    "blush": (0.0, 0.0, 1.0), "sweat": (0.0, 0.0, 1.0),
}


def drive(target, path, index, rig, prop, expr):
    """target.path[index] = expr(v), với v = rig[prop]."""
    fc = target.driver_add(path, index) if index is not None else target.driver_add(path)
    d = fc.driver
    d.type = "SCRIPTED"
    var = d.variables.new()
    var.name = "v"
    var.targets[0].id_type = "OBJECT"
    var.targets[0].id = rig
    var.targets[0].data_path = f'["{prop}"]'
    d.expression = expr
    return fc


def build_face(rig, body, mats):
    """mats: dict tên -> material (white, iris, pupil, glint, dark, blush, star, fur, brow, mouth, sweat)."""
    for k, (val, lo, hi) in PROPS.items():
        rig[k] = val
        rig.id_properties_ui(k).update(min=lo, max=hi, default=val)

    bm = bmesh.new()
    bm.from_mesh(body.data)
    bvh = BVHTree.FromBMesh(bm)
    bm.free()

    def surf(x, z):
        loc, nrm, _, _ = bvh.ray_cast(Vector((x, -1, z)), Vector((0, 1, 0)))
        return loc, nrm

    pb = rig.pose.bones[HEAD_BONE]
    parent_inv = (rig.matrix_world @ pb.matrix @ Matrix.Translation((0, pb.bone.length, 0))).inverted()
    coll = bpy.context.scene.collection

    def new(name, data=None):
        o = bpy.data.objects.new(name, data)
        coll.objects.link(o)
        if data is None:
            o.empty_display_size = 0.015
        return o

    def on_head(obj, world_loc, rot=(0, 0, 0)):
        obj.parent, obj.parent_type, obj.parent_bone = rig, "BONE", HEAD_BONE
        obj.matrix_parent_inverse = parent_inv
        obj.location, obj.rotation_euler = world_loc, rot
        return obj

    def child(obj, parent, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        obj.parent = parent
        obj.location, obj.rotation_euler, obj.scale = loc, rot, scale
        return obj

    def mesh_from(name, bm2, mat, smooth=True):
        me = bpy.data.meshes.new(name)
        bm2.to_mesh(me)
        bm2.free()
        if smooth:
            me.shade_smooth()
        me.materials.append(mat)
        return new(name, me)

    def sphere(name, r, mat):
        b = bmesh.new()
        bmesh.ops.create_uvsphere(b, u_segments=32, v_segments=16, radius=r)
        return mesh_from(name, b, mat)

    def half_sphere(name, r, mat, top=True):
        b = bmesh.new()
        bmesh.ops.create_uvsphere(b, u_segments=40, v_segments=20, radius=r)
        bmesh.ops.delete(b, geom=[v for v in b.verts if (v.co.z < -1e-5 if top else v.co.z > 1e-5)], context="VERTS")
        bmesh.ops.holes_fill(b, edges=b.edges[:], sides=0)
        return mesh_from(name, b, mat)

    # ------------------------------------------------ mắt: hốc (đứng yên) > nhãn cầu (liếc) + mí trên/dưới
    for side, x, sgn in (("L", 0.052, 1), ("R", -0.052, -1)):
        p, n = surf(x, 0.358)
        socket = on_head(new(f"LumoEyeSocket{side}"), p - n * 0.014)
        look = child(new(f"LumoEyeLook{side}"), socket)
        drive(look, "rotation_euler", 2, rig, "look_x", "v*0.42")
        drive(look, "rotation_euler", 0, rig, "look_z", "-v*0.35")
        child(sphere(f"LumoEyeWhite{side}", 0.04, mats["white"]), look, scale=(1, 1, 1.1))
        iris_grp = child(new(f"LumoIrisGroup{side}"), look)
        for axis in (0, 2):
            drive(iris_grp, "scale", axis, rig, "pupil", "v")
        child(sphere(f"LumoIris{side}", 0.025, mats["iris"]), iris_grp, (0, -0.033, 0.002), scale=(1, 0.38, 1.1))
        child(sphere(f"LumoPupil{side}", 0.014, mats["pupil"]), iris_grp, (0, -0.038, 0.002), scale=(1, 0.3, 1.1))
        child(sphere(f"LumoGlint{side}", 0.007, mats["glint"]), iris_grp, (-0.009, -0.04, 0.014))
        # mí trên: nửa cầu che phía trên; xoay quanh X để khép (90°) / mở (-55°) / trợn (-84°)
        up = child(half_sphere(f"LumoLidUp{side}", 0.0425, mats["fur"], top=True), socket, scale=(1, 1, 1.1))
        drive(up, "rotation_euler", 0, rig, f"eye_open_{side}", "radians(90 - 145*v)")
        drive(up, "rotation_euler", 1, rig, f"lid_tilt_{side}", f"radians({-sgn}*22*v)")
        lo = child(half_sphere(f"LumoLidLow{side}", 0.0422, mats["fur"], top=False), socket, scale=(1, 1, 1.1))
        drive(lo, "rotation_euler", 0, rig, f"lower_lid_{side}", "radians(62 - 85*v)")

    # ------------------------------------------------ lông mày nổi (biểu cảm mạnh nhất)
    for side, x, sgn in (("L", 0.057, 1), ("R", -0.057, -1)):
        p, n = surf(x, 0.414)                                # đủ cao để mí mắt không che khi cau mày
        sock = on_head(new(f"LumoBrowSocket{side}"), p + n * 0.006, n.to_track_quat("-Y", "Z").to_euler())
        b = bmesh.new()
        bmesh.ops.create_uvsphere(b, u_segments=24, v_segments=12, radius=1.0)
        for v in b.verts:
            v.co = Vector((v.co.x * 0.022, v.co.y * 0.004, v.co.z * 0.006))
            v.co.z -= 9.0 * v.co.x ** 2                       # cong hình vòm
        brow = child(mesh_from(f"LumoBrow{side}", b, mats["brow"]), sock)
        drive(brow, "location", 2, rig, f"brow_raise_{side}", "v*0.009")
        drive(brow, "rotation_euler", 1, rig, f"brow_tilt_{side}", f"radians({-sgn}*24*v)")   # +1: đầu trong cụp xuống

    # ------------------------------------------------ miệng: một vòng đỉnh, mỗi hình miệng là một shape key
    N, SCALE = 48, 1.7
    p_mouth, n_mouth = surf(0, 0.292)
    rot_mouth = n_mouth.to_track_quat("-Y", "Z")
    M = Matrix.Translation(p_mouth) @ rot_mouth.to_matrix().to_4x4()
    M_inv = M.inverted()

    def outline(top, bottom, w):
        pts = []
        for i in range(N // 2):
            u = -1 + 2 * i / (N // 2 - 1)
            pts.append((w * u, top(u)))
        for i in range(N // 2):
            u = 1 - 2 * i / (N // 2 - 1)
            pts.append((w * u, bottom(u)))
        return pts

    def sq(u):
        return math.sqrt(max(0.0, 1 - u * u))

    shapes = {
        "Basis": outline(lambda u: 0.004 * u * u - 0.001, lambda u: 0.004 * u * u - 0.001 - 0.0016 * (1 - u * u), 0.015),
        "mouth_smile": outline(lambda u: 0.008 * u * u - 0.003, lambda u: 0.008 * u * u - 0.003 - 0.0035 * (1 - u * u), 0.021),
        "mouth_grin": outline(lambda u: 0.004 * u * u - 0.0005, lambda u: 0.004 * u * u - 0.0005 - 0.016 * sq(u), 0.023),
        "mouth_open": outline(lambda u: 0.011 * sq(u) - 0.004, lambda u: -0.011 * sq(u) - 0.004, 0.0105),
        "mouth_frown": outline(lambda u: -0.007 * u * u + 0.0015, lambda u: -0.007 * u * u + 0.0015 - 0.0018 * (1 - u * u), 0.017),
        "mouth_flat": outline(lambda u: 0.0007, lambda u: -0.0007 - 0.0004 * (1 - u * u), 0.015),
        "mouth_wavy": outline(lambda u: 0.0018 * math.sin(2.6 * math.pi * u) + 0.0008,
                              lambda u: 0.0018 * math.sin(2.6 * math.pi * u) + 0.0008 - 0.0016 * (1 - u * u), 0.018),
    }

    def to3(pt):
        """Điểm 2D của hình miệng -> chiếu lên bề mặt mõm (ôm sát da theo cả chiều ngang lẫn dọc)."""
        x, z = pt[0] * SCALE, pt[1] * SCALE
        c = M @ Vector((x, 0, z))
        loc, nrm, _, _ = bvh.ray_cast(c + n_mouth * 0.04, -n_mouth)
        if loc is None:
            return Vector((x, 0, z))
        return M_inv @ (loc + nrm * 0.0013)

    b = bmesh.new()
    ring = [b.verts.new(to3(pt)) for pt in shapes["Basis"]]
    center = b.verts.new(to3((0, sum(z for _, z in shapes["Basis"]) / N)))
    for i in range(N):
        b.faces.new((center, ring[i], ring[(i + 1) % N]))
    mouth = mesh_from("LumoMouth", b, mats["mouth"])
    on_head(mouth, p_mouth, rot_mouth.to_euler())
    mouth.shape_key_add(name="Basis")
    for name, pts in shapes.items():
        if name == "Basis":
            continue
        k = mouth.shape_key_add(name=name, from_mix=False)
        for i, pt in enumerate(pts):
            k.data[i].co = to3(pt)
        k.data[N].co = to3((0, sum(z for _, z in pts) / N))
        drive(k, "value", None, rig, name, "v")

    # ------------------------------------------------ mũi, má hồng, ngôi sao, giọt mồ hôi
    p, n = surf(0, 0.322)
    on_head(child(sphere("LumoNose", 0.016, mats["dark"]), None, scale=(1.25, 0.8, 0.85)), p + n * 0.004)
    for side, x in (("L", 0.085), ("R", -0.085)):
        p, n = surf(x, 0.322)
        bl = on_head(sphere(f"LumoBlush{side}", 1.0, mats["blush"]), p + n * 0.001, n.to_track_quat("-Y", "Z").to_euler())
        drive(bl, "scale", 0, rig, "blush", "0.018*(0.7 + 0.8*v)")
        bl.scale[1] = 0.004
        drive(bl, "scale", 2, rig, "blush", "0.011*(0.7 + 0.8*v)")
    sbm = bmesh.new()
    pts = [sbm.verts.new((math.cos(math.pi / 2 + k * math.pi / 5) * (0.022 if k % 2 == 0 else 0.009), 0,
                          math.sin(math.pi / 2 + k * math.pi / 5) * (0.022 if k % 2 == 0 else 0.009)))
           for k in range(10)]
    bmesh.ops.extrude_face_region(sbm, geom=[sbm.faces.new(pts)])
    sbm.verts.ensure_lookup_table()
    for v in sbm.verts[10:]:
        v.co.y += 0.004
    p, n = surf(0, 0.425)
    on_head(mesh_from("LumoStar", sbm, mats["star"], smooth=False), p - n * 0.001, n.to_track_quat("-Y", "Z").to_euler())
    db = bmesh.new()
    bmesh.ops.create_uvsphere(db, u_segments=24, v_segments=12, radius=0.012)
    for v in db.verts:                                  # giọt nước: đỉnh nhọn
        if v.co.z > 0:
            k = 1 - v.co.z / 0.012
            v.co.x *= k
            v.co.y *= k
            v.co.z *= 1.8
    drop = on_head(mesh_from("LumoSweat", db, mats["sweat"]), (0.118, -0.03, 0.43), (0, math.radians(-20), 0))
    for axis in range(3):
        drive(drop, "scale", axis, rig, "sweat", "v")
