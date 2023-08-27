import bpy
from bpy_types import PoseBone
from mathutils import Quaternion, Matrix, Vector
from typing import Callable

from . import utils
from .utils import PoseBoneOrObject


def rotate_in_view(target: PoseBoneOrObject, view_delta_quat: Quaternion):
    world_delta_quat = convert_rot_view_to_world(view_delta_quat)
    apply_rotation(target, world_delta_quat)


def translate_in_view(target: PoseBoneOrObject, view_delta_trans: Vector):
    world_delta_trans = convert_trans_view_to_world(view_delta_trans)
    apply_translation(target, world_delta_trans)


def translate_and_rotate_in_view(target: PoseBoneOrObject, view_delta_trans: Vector, view_delta_quat: Quaternion):
    world_delta_trans = convert_trans_view_to_world(view_delta_trans)
    world_delta_quat = convert_rot_view_to_world(view_delta_quat)
    if utils.is_pose_bone(target):
        def add_translation_and_rotation(matrix: Matrix):
            loc, rot, scale = matrix.decompose()
            rot = world_delta_quat @ rot
            loc += world_delta_trans
            return Matrix.LocRotScale(loc, rot, scale)

        apply_world_matrix_to_bone(target, add_translation_and_rotation)
    else:
        target.matrix_world.translation += world_delta_trans
        target.rotation_mode = "QUATERNION"
        target.rotation_quaternion = world_delta_quat @ target.rotation_quaternion


def apply_rotation(target, world_delta_quat):
    if utils.is_pose_bone(target):
        def add_rotation(matrix: Matrix):
            loc, rot, scale = matrix.decompose()
            rot = world_delta_quat @ rot
            return Matrix.LocRotScale(loc, rot, scale)

        apply_world_matrix_to_bone(target, add_rotation)
    else:
        target.rotation_mode = "QUATERNION"
        target.rotation_quaternion = world_delta_quat @ target.rotation_quaternion


def apply_translation(target, world_delta_trans):
    if isinstance(target, bpy.types.PoseBone):
        def add_translation(matrix: Matrix):
            matrix.translation += world_delta_trans
            return matrix

        apply_world_matrix_to_bone(target, add_translation)

    else:
        target.matrix_world.translation += world_delta_trans


def convert_rot_view_to_world(view_quat: Quaternion) -> Quaternion:
    view_rot = utils.get_active_region3d().view_rotation
    return view_rot @ view_quat @ view_rot.inverted()


def convert_trans_view_to_world(view_trans: Vector) -> Vector:
    view_rot = utils.get_active_region3d().view_rotation
    return view_rot @ view_trans


def apply_world_matrix_to_bone(pose_bone: PoseBone, func: Callable[[Matrix], Matrix]) -> None:
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
