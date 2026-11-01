"""
Kiểm tra rig: đặt tư thế theo trục thế giới, đo độ méo lưới so với tư thế nghỉ.
    reset_pose(rig); rest = {o.name: mesh_stats(o) for o in meshes}
    apply_pose(rig, {"hand_ik.L": {"loc": (0, 0, 0.1), "rot": [((1, 0, 0), 30)]}})
    bad, vol, amin, amax = distortion(rest[o.name], o)
Chỉ số:
  bad%      = % mặt lưới bị bóp (< 40% diện tích) hoặc giãn (> 250%). Đạt: dưới ~2%
  vol       = thể tích sau / trước (lý tưởng ~1.0; thấp = bị xẹp)
  amin/amax = mặt bị bóp/giãn nhiều nhất
"""
import math

import bmesh
import bpy
import numpy as np
from mathutils import Quaternion, Vector


def reset_pose(rig):
    for pb in rig.pose.bones:
        pb.location = (0, 0, 0)
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.scale = (1, 1, 1)


def apply_pose(rig, pose):
    """pose: {xương: {"loc": dịch chuyển theo trục thế giới (m), "rot": [(trục thế giới, độ), ...]}}"""
    reset_pose(rig)
    for name, spec in pose.items():
        pb = rig.pose.bones[name]
        inv = pb.bone.matrix_local.to_3x3().inverted()
        if "loc" in spec:
            pb.location = inv @ Vector(spec["loc"])
        q = Quaternion()
        for axis, deg in spec.get("rot", []):
            q = Quaternion(inv @ Vector(axis), math.radians(deg)) @ q
        pb.rotation_quaternion = q


def mesh_stats(obj):
    dg = bpy.context.evaluated_depsgraph_get()
    ev = obj.evaluated_get(dg)
    me = ev.to_mesh()
    areas = np.array([p.area for p in me.polygons])
    bm = bmesh.new()
    bm.from_mesh(me)
    vol = bm.calc_volume()
    bm.free()
    ev.to_mesh_clear()
    return areas, vol


def distortion(rest, obj):
    a0, v0 = rest
    a1, v1 = mesh_stats(obj)
    ratio = a1 / np.maximum(a0, 1e-12)
    bad = float(np.mean((ratio < 0.4) | (ratio > 2.5)) * 100)
    return bad, v1 / v0, float(ratio.min()), float(ratio.max())
