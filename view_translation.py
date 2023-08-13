import bpy
import bpy


class ViewTranslation:

    # Define a function to get the 3D view matrix
    def get_3d_view_matrix(self):
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return area.spaces[0].region_3d.view_matrix
        return None

    # Get the active object
    obj = bpy.context.active_object

    # Get the 3D view matrix
    view_matrix = get_3d_view_matrix()

    if view_matrix:
        # The forward direction for the view is the negative Z-axis
        view_direction = -view_matrix.to_3x3().col[2]

        # Scale the direction vector by the desired distance
        distance = 1
        move_vector = view_direction.normalized() * distance

        # Update the object's location
        obj.location += move_vector
