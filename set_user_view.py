import bpy
from mathutils import Vector


def set_viewport_camera(viewport, location, look_at):
    # Calculate the direction vector
    direction = look_at - location

    # Set the view rotation
    rot_quat = direction.to_track_quat('-Z', 'Y')
    viewport.view_rotation = rot_quat

    # Set the focus to the origin
    viewport.view_location = look_at

    # Set the distance from the focus point to the desired location
    viewport.view_distance = direction.length

    # Print the location and direction
    print("Viewport Direction:", direction.normalized())
    print("Viewport Distance from Focus:", viewport.view_distance)


location = Vector((10.0, 10.0, 10.0))
look_at = Vector((0, 0, 0))

# Iterate through all the areas to find the 3D viewports
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        viewport = area.spaces.active.region_3d
        set_viewport_camera(viewport, location, look_at)



bpy.ops.transform.rotate(value=radians(10), orient_axis='Z', orient_type='VIEW', orient_matrix=((-0.000364032, -0.997883, 0.0650404), (0.270798, 0.0625117, 0.960604), (-0.962636, 0.0179623, 0.270201)), orient_matrix_type='VIEW')


bpy.ops.transform.rotate(value=0.163956, orient_axis='Z', orient_type='VIEW', orient_matrix=((0.448383, -0.893841, 2.76603e-07), (0.00624076, 0.00313102, 0.999976), (-0.89382, -0.448372, 0.00698222)), orient_matrix_type='VIEW', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True, use_snap_nonedit=True, use_snap_selectable=False, release_confirm=True)
