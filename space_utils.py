import bpy


def get_region3d():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    return area.spaces[0].region_3d
    return None


# # Get the active object
# obj = bpy.context.active_object
#
# # Get the 3D view matrix
# view_matrix = get_region3d()
#
# if view_matrix:
#     # The forward direction for the view is the negative Z-axis
#     view_direction = -view_matrix.to_3x3().col[2]
#
#     # Scale the direction vector by the desired distance
#     distance = 1
#     move_vector = view_direction.normalized() * distance
#
#     # Update the object's location
#     obj.location += move_vector


def get_active_object():
    return bpy.context.active_pose_bone or bpy.context.active_object


def set_world_transformation(target, world_transform_matrix):
    """
    Sets the world translation of a given pose bone additively in view space.

    Args:
    - pose_bone (bpy.types.PoseBone): The pose bone to modify.
    - view_rotation (mathutils.Quaternion): The rotation of the active viewport.
    - delta_translation (mathutils.Vector): The delta translation in view space.
    """
    if isinstance(target, bpy.types.PoseBone):
        print("is bone")
        pose_bone = target
        armature = pose_bone.id_data
        # bone_world_matrix = armature.matrix_world @ pose_bone.matrix
        # translated_bone_mw = Matrix.Translation(world_delta_translation)
        bone_world_matrix = armature.convert_space(pose_bone=pose_bone,
                                                   matrix=pose_bone.matrix,
                                                   from_space='POSE',
                                                   to_space='WORLD')
        print(f"world delta {world_transform_matrix}")
        bone_world_matrix @= world_transform_matrix

        pose_bone.matrix = armature.convert_space(pose_bone=pose_bone,
                                                  matrix=bone_world_matrix,
                                                  from_space='WORLD',
                                                  to_space='POSE')
    else:
        target.matrix_world @= world_transform_matrix

def set_world_translation(target, world_delta_translation):
    """
    Sets the world translation of a given pose bone additively in view space.

    Args:
    - pose_bone (bpy.types.PoseBone): The pose bone to modify.
    - view_rotation (mathutils.Quaternion): The rotation of the active viewport.
    - delta_translation (mathutils.Vector): The delta translation in view space.
    """
    if isinstance(target, bpy.types.PoseBone):
        print("is bone")
        pose_bone = target
        armature = pose_bone.id_data
        # bone_world_matrix = armature.matrix_world @ pose_bone.matrix
        # translated_bone_mw = Matrix.Translation(world_delta_translation)
        bone_world_matrix = armature.convert_space(pose_bone=pose_bone,
                                                   matrix=pose_bone.matrix,
                                                   from_space='POSE',
                                                   to_space='WORLD')
        print(f"world delta {world_delta_translation}")
        bone_world_matrix.translation += world_delta_translation

        pose_bone.matrix = armature.convert_space(pose_bone=pose_bone,
                                                  matrix=bone_world_matrix,
                                                  from_space='WORLD',
                                                  to_space='POSE')
    else:
        target.matrix_world.translation += world_delta_translation


