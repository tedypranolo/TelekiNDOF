import bpy
from typing import Union

PoseBoneOrObject = Union[bpy.types.PoseBone, bpy.types.Object]


def is_pose_bone(obj: PoseBoneOrObject) -> bool:
    return isinstance(obj, bpy.types.PoseBone)


def get_active_region3d() -> bpy.types.RegionView3D:
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    return area.spaces[0].region_3d
    return None


def get_active_object() -> PoseBoneOrObject:
    return bpy.context.active_pose_bone or bpy.context.active_object
