import bpy


def get_user_view():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            return area.spaces.active.region_3d


def is_pose_bone(obj):
    return isinstance(obj, bpy.types.PoseBone)
