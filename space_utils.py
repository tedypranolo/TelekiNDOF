import bpy
from bpy_types import PoseBone
from mathutils import Quaternion, Matrix
from typing import Callable

from . import utils


def apply_translation(target, world_delta_trans):
    if isinstance(target, bpy.types.PoseBone):
        def add_translation(matrix: Matrix):
            matrix.translation += world_delta_trans
            return matrix
        apply_world_matrix_to_bone(target, add_translation)

    else:
        target.matrix_world.translation += world_delta_trans


def convert_rot_active_view_to_world(view_quat: Quaternion) -> Quaternion:
    view_rot = utils.get_active_region3d()
    return view_rot @ view_quat @ view_rot.inverted()


def apply_rotation_in_view_space(target, view_rot, view_delta_quat):
    world_delta_quat = convert_rot_active_view_to_world(view_delta_quat.to_matrix())

    # Check if the target is a pose bone
    if utils.is_pose_bone(target):
        def add_rotation(matrix: Matrix):
            loc, rot, scale = matrix.decompose()
            rot = world_delta_quat @ rot
            return Matrix.LocRotScale(loc, rot, scale)

        apply_world_matrix_to_bone(target, add_rotation)
    else:
        target.rotation_mode = "QUATERNION"
        target.rotation_quaternion = world_delta_quat @ target.rotation_quaternion


def apply_world_matrix_to_bone(pose_bone: PoseBone, func: Callable[[Matrix], None]) -> None:
    armature = pose_bone.id_data
    bone_world_matrix = armature.convert_space(pose_bone=pose_bone,
                                               matrix=pose_bone.matrix,
                                               from_space='POSE',
                                               to_space='WORLD')
    modified = func(bone_world_matrix)
    pose_bone.matrix = armature.convert_space(pose_bone=pose_bone,
                                              matrix=modified,
                                              from_space='WORLD',
                                              to_space='POSE')
