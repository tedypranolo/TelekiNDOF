# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# This addon was created with the Serpens - Visual Scripting Addon.
# This code is generated from nodes and is not intended for manual editing.
# You can find out more about Serpens at <https://blendermarket.com/products/serpens>.

from datetime import datetime

bl_info = {
    "name": "TelekiNDOF",
    "description": "This addon add mouvement control to object with 3d Connexion Space Mouse, I want a take the opportunity to thanks github user johnhw for the code pyspacenavigator used by this addon",
    "author": "Julien Roy",
    "version": (1, 1, 1),
    "blender": (2, 93, 0),
    "location": "This addon lives  in it's own propertie panel accessible on the right of the 3d view windows",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}

# --------------------   IMPORTS
import sys
import os
import subprocess

# py_exec = str(sys.executable)
# # ensure pip is installed
# subprocess.call([py_exec, "-m", "ensurepip", "--user"])
# # update pip (not mandatory but highly recommended)
# subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip"])
# # install packages
# subprocess.call([py_exec, "-m", "pip", "install", f"--target={py_exec[:-14]}" + "lib", "pywinusb"])

# -------------------- Add Space Navigator
# ----------------------------------------------
# Add to Python path (once only)
# ----------------------------------------------
path = sys.path
flag = False
for item in path:
    if "TelekiNDOF-main" in item:
        flag = True
if not flag:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'TelekiNDOF-main'))

# ----------------------------------------------
# Import modules
# ----------------------------------------------
if "bpy" in locals():
    import importlib
    import spacenavigator

    importlib.reload(spacenavigator)

    import threeple

    importlib.reload(threeple)
else:
    from . import spacenavigator

from .threeple import Threeple

import bpy
import bpy.utils.previews
from bpy.props import FloatVectorProperty, FloatProperty
from mathutils import Vector, Matrix, Quaternion, Euler

#   INITALIZE VARIABLES
telekindof = {
    "upinverse": True,
}


#   SERPENS FUNCTIONS
def exec_line(line):
    exec(line)


def sn_print(tree_name, *args):
    if tree_name in bpy.data.node_groups:
        item = bpy.data.node_groups[tree_name].sn_graphs[0].prints.add()
        for arg in args:
            item.value += str(arg) + ";;;"
        if bpy.context and bpy.context.screen:
            for area in bpy.context.screen.areas:
                area.tag_redraw()
    print(*args)


def sn_cast_string(value):
    return str(value)


def sn_cast_boolean(value):
    if type(value) == tuple:
        for data in value:
            if bool(data):
                return True
        return False
    return bool(value)


def sn_cast_float(value):
    if type(value) == str:
        try:
            value = float(value)
            return value
        except:
            return float(bool(value))
    elif type(value) == tuple:
        return float(value[0])
    elif type(value) == list:
        return float(len(value))
    elif not type(value) in [float, int, bool]:
        try:
            value = len(value)
            return float(value)
        except:
            return float(bool(value))
    return float(value)


def sn_cast_int(value):
    return int(sn_cast_float(value))


def sn_cast_boolean_vector(value, size):
    if type(value) in [str, bool, int, float]:
        return_value = []
        for i in range(size):
            return_value.append(bool(value))
        return tuple(return_value)
    elif type(value) == tuple:
        return_value = []
        for i in range(size):
            return_value.append(bool(value[i]) if len(value) > i else bool(value[0]))
        return tuple(return_value)
    elif type(value) == list:
        return sn_cast_boolean_vector(tuple(value), size)
    else:
        try:
            value = tuple(value)
            return sn_cast_boolean_vector(value, size)
        except:
            return sn_cast_boolean_vector(bool(value), size)


def sn_cast_float_vector(value, size):
    if type(value) in [str, bool, int, float]:
        return_value = []
        for i in range(size):
            return_value.append(sn_cast_float(value))
        return tuple(return_value)
    elif type(value) == tuple:
        return_value = []
        for i in range(size):
            return_value.append(sn_cast_float(value[i]) if len(value) > i else sn_cast_float(value[0]))
        return tuple(return_value)
    elif type(value) == list:
        return sn_cast_float_vector(tuple(value), size)
    else:
        try:
            value = tuple(value)
            return sn_cast_float_vector(value, size)
        except:
            return sn_cast_float_vector(sn_cast_float(value), size)


def sn_cast_int_vector(value, size):
    return tuple(map(int, sn_cast_float_vector(value, size)))


def sn_cast_color(value, use_alpha):
    length = 4 if use_alpha else 3
    value = sn_cast_float_vector(value, length)
    tuple_list = []
    for data in range(length):
        data = value[data] if len(value) > data else value[0]
        tuple_list.append(sn_cast_float(min(1, max(0, data))))
    return tuple(tuple_list)


def sn_cast_list(value):
    if type(value) in [str, tuple, list]:
        return list(value)
    elif type(value) in [int, float, bool]:
        return [value]
    else:
        try:
            value = list(value)
            return value
        except:
            return [value]


def sn_cast_blend_data(value):
    if hasattr(value, "bl_rna"):
        return value
    elif type(value) in [tuple, bool, int, float, list]:
        return None
    elif type(value) == str:
        try:
            value = eval(value)
            return value
        except:
            return None
    else:
        return None


def sn_cast_enum(string, enum_values):
    for it in enum_values:
        if it[1] == string:
            return it[0]
        elif it[0] == string.upper():
            return it[0]
    return string


# --------------------   IMPERATIVE CODE
#   TelekiNDOF
addon_keymaps = {}


# --------------------   EVALUATED CODE
#    TelekiNDOF
class SNA_PT_Axis_Sensitivity_9D7BA(bpy.types.Panel):
    bl_label = "Axis Sensitivity"
    bl_idname = "SNA_PT_Axis_Sensitivity_9D7BA"
    bl_parent_id = "SNA_PT_Axis_Settings_8B68A"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Axis Sensitivity subpanel header")

    def draw(self, context):
        try:
            layout = self.layout
            layout.prop(bpy.context.scene, 'transsens', text=r"Translation", emboss=True, slider=False, )
            layout.prop(bpy.context.scene, 'rotsens', text=r"Rotation", emboss=True, slider=False, )
        except Exception as exc:
            print(str(exc) + " | Error in Axis Sensitivity subpanel")


class SNA_PT_Shortcut_B5987(bpy.types.Panel):
    bl_label = "Shortcut"
    bl_idname = "SNA_PT_Shortcut_B5987"
    bl_parent_id = "SNA_PT_Shortcut_2C5D2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Shortcut subpanel header")

    def draw(self, context):
        try:
            layout = self.layout
            if "9DCCD" in addon_keymaps:
                _, kmi = addon_keymaps["9DCCD"]
                layout.prop(kmi, "type", text=r"Telekinesys Shortcut", full_event=True, toggle=False)
            else:
                layout.label(text="Couldn't find keymap item!", icon="ERROR")
        except Exception as exc:
            print(str(exc) + " | Error in Shortcut subpanel")


class SNA_PT_Inverse_Axis_3C0BA(bpy.types.Panel):
    bl_label = "Inverse Axis"
    bl_idname = "SNA_PT_Inverse_Axis_3C0BA"
    bl_parent_id = "SNA_PT_Axis_Settings_8B68A"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Inverse Axis subpanel header")

    def draw(self, context):
        try:
            layout = self.layout
            layout.prop(bpy.context.scene, 'rightinv', icon_value=0, text=r"RightInv", emboss=True, toggle=False,
                        invert_checkbox=False, )
            layout.prop(bpy.context.scene, 'frontinv', icon_value=0, text=r"FrontInv", emboss=True, toggle=False,
                        invert_checkbox=False, )
            layout.prop(bpy.context.scene, 'upinv', icon_value=0, text=r"Up", emboss=True, toggle=False,
                        invert_checkbox=False, )
            layout.prop(bpy.context.scene, 'rollinv', icon_value=0, text=r"Roll", emboss=True, toggle=False,
                        invert_checkbox=False, )
            layout.prop(bpy.context.scene, 'pitchinv', icon_value=0, text=r"Pitch", emboss=True, toggle=False,
                        invert_checkbox=False, )
            layout.prop(bpy.context.scene, 'yawinv', icon_value=0, text=r"Yaw", emboss=True, toggle=False,
                        invert_checkbox=False, )
        except Exception as exc:
            print(str(exc) + " | Error in Inverse Axis subpanel")


class SNA_PT_Axis_binding_220EE(bpy.types.Panel):
    bl_label = "Axis binding"
    bl_idname = "SNA_PT_Axis_binding_220EE"
    bl_parent_id = "SNA_PT_Axis_Settings_8B68A"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Axis binding subpanel header")

    def draw(self, context):
        try:
            layout = self.layout
            layout.prop(bpy.context.scene, 'rightbinding', icon_value=0, text=r"Right", emboss=True, expand=False, )
            layout.prop(bpy.context.scene, 'frontbinding', icon_value=0, text=r"Front", emboss=True, expand=False, )
            layout.prop(bpy.context.scene, 'upbinding', icon_value=0, text=r"Up", emboss=True, expand=False, )
            layout.prop(bpy.context.scene, 'rollbinding', icon_value=0, text=r"Roll of mouse", emboss=True,
                        expand=False, )
            layout.prop(bpy.context.scene, 'pitchbinding', icon_value=0, text=r"Pitch of mouse", emboss=True,
                        expand=False, )
            layout.prop(bpy.context.scene, 'yawbinding', icon_value=0, text=r"Yaw of Space Mouse", emboss=True,
                        expand=False, )
        except Exception as exc:
            print(str(exc) + " | Error in Axis binding subpanel")


class SNA_PT_Shortcut_2C5D2(bpy.types.Panel):
    bl_label = "Shortcut"
    bl_idname = "SNA_PT_Shortcut_2C5D2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'TelekiNDOF'
    bl_options = {"DEFAULT_CLOSED", }
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Shortcut panel header")

    def draw(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Shortcut panel")


class SNA_PT_Axis_Settings_8B68A(bpy.types.Panel):
    bl_label = "Axis Settings"
    bl_idname = "SNA_PT_Axis_Settings_8B68A"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'TelekiNDOF'
    bl_options = {"DEFAULT_CLOSED", }
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Axis Settings panel header")

    def draw(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Axis Settings panel")


class SNA_PT_Action_FC1AB(bpy.types.Panel):
    bl_label = "Action"
    bl_idname = "SNA_PT_Action_FC1AB"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'TelekiNDOF'
    bl_order = 0

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Action panel header")

    def draw(self, context):
        try:
            layout = self.layout
            op = layout.operator("sna.telekin", text=r"Telekinesis", emboss=True, depress=False, icon_value=594)
        except Exception as exc:
            print(str(exc) + " | Error in Action panel")


def register_key_9DCCD():
    kc = bpy.context.window_manager.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Window", space_type="EMPTY")
        kmi = km.keymap_items.new("sna.telekin",
                                  type="W",
                                  value="PRESS",
                                  repeat=False,
                                  ctrl=True,
                                  alt=False,
                                  shift=False)
        addon_keymaps['9DCCD'] = (km, kmi)


class ModalOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "object.modal_operator"
    bl_label = "Simple Modal Operator"

    # Location related properties
    first_state_location: FloatVectorProperty(size=3)
    first_value_location: FloatVectorProperty(size=3)
    value_location: FloatVectorProperty(size=3)

    # Rotation related properties
    first_state_rotation: FloatVectorProperty(size=3, name="First State Rotation")
    first_value_rotation: FloatVectorProperty(size=3, name="First Value Rotation")
    value_rotation: FloatVectorProperty(size=3, name="Value Rotation")

    # Sensitivities for translation and rotation
    sens: FloatVectorProperty(size=3, name="Translation Sensitivity")
    sensr: FloatVectorProperty(size=3, name="Rotation Sensitivity")

    # Inversions
    invup: FloatProperty()
    invfront: FloatProperty()
    invright: FloatProperty()
    invroll: FloatProperty()
    invpitch: FloatProperty()
    invyaw: FloatProperty()

    def move_and_rotate(obj, state, panel_properties):

        # Process values using the new method
        x = panel_properties.process_value(state, 'x')
        y = panel_properties.process_value(state, 'y')
        z = panel_properties.process_value(state, 'z')

        # Move the object
        obj.location.x += x
        obj.location.y += y
        obj.location.z += z

        # Process values for rotations
        pitch = panel_properties.process_value(state, 'pitch')
        yaw = panel_properties.process_value(state, 'yaw')
        roll = panel_properties.process_value(state, 'roll')

        # Rotate the object
        obj.rotation_euler.x += pitch
        obj.rotation_euler.y += yaw
        obj.rotation_euler.z += roll

    def apply_rotation_in_view_space(self, view_rot, target, controller_rot):
        # Compute rotations in view space for each axis
        rotation_x_in_view = Quaternion((1, 0, 0), controller_rot.y)
        rotation_y_in_view = Quaternion((0, 1, 0), controller_rot.z)
        rotation_z_in_view = Quaternion((0, 0, 1), controller_rot.x)

        # Combine the rotations
        combined_rotation_in_view = rotation_x_in_view @ rotation_y_in_view @ rotation_z_in_view

        # Convert the combined rotation from view space to world space
        combined_rotation_in_world = view_rot @ combined_rotation_in_view @ view_rot.inverted()

        target.rotation_mode = "QUATERNION"
        # Apply the computed rotation to the object
        target.rotation_quaternion = combined_rotation_in_world @ target.rotation_quaternion

    def modal(self, context, event):
        _, kmi = addon_keymaps.get("9DCCD", (None, None))
        if kmi:
            # Check against the registered keymap
            if event.type == kmi.type and event.value == 'PRESS':
                if event.ctrl == kmi.ctrl and \
                        event.alt == kmi.alt and \
                        event.shift == kmi.shift:
                    print("Finishing the modal operator due to same shortcut.")
                    return {'FINISHED'}

        if event.type == 'NDOF_MOTION':

            state = spacenavigator.read()

            # Mappings
            bindings = ['upbinding', 'rightbinding', 'frontbinding', 'rollbinding', 'pitchbinding', 'yawbinding']
            states = {'upbinding': 'z', 'rightbinding': 'x', 'frontbinding': 'y', 'rollbinding': 'roll',
                      'pitchbinding': 'pitch', 'yawbinding': 'yaw'}
            inversions = {'upbinding': 'invup', 'rightbinding': 'invright', 'frontbinding': 'invfront',
                          'rollbinding': 'invroll', 'pitchbinding': 'invpitch', 'yawbinding': 'invyaw'}

            # Initialize vectors
            delta_location = Threeple((0, 0, 0))
            delta_rotation = Threeple((0, 0, 0))

            first_state_loc = Threeple(self.first_state_location)
            first_state_rot = Threeple(self.first_state_rotation)
            # Compute deltas
            for binding in bindings:
                binding_value = getattr(bpy.context.scene, binding)
                state_value = getattr(state, states[binding]) * getattr(self, inversions[binding])
                mapped_attr = states[binding]
                if binding_value in ['x', 'y', 'z']:
                    delta_location[mapped_attr] = first_state_loc[binding_value] - state_value
                else:
                    delta_rotation[mapped_attr] = first_state_rot[binding_value] - state_value

            print(f"states {state}")
            # Update locations and rotations
            target = context.active_object
            # Get the current view matrix
            view_rotation = bpy.context.region_data.view_rotation
            translation_vector = (delta_location * self.sens).vector
            target.location += view_rotation @ translation_vector
            controller_rotation = (delta_rotation * self.sensr).as_euler()
            self.apply_rotation_in_view_space(view_rotation, target, controller_rotation)
            # Set current position value to variable for next increment
            self.value_location = target.location.copy()
            self.value_rotation = target.rotation_euler.copy()
        elif event.type == 'LEFTMOUSE':
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.object.location = self.first_value_location
            context.object.rotation_euler = self.first_value_rotation
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    is_running = False

    def invoke(self, context, event):
        if self.is_running:
            print("Stopping the modal operator.")
            self.is_running = False
            return {'CANCELLED'}
        else:
            print("Starting the modal operator.")
            self.is_running = True
            success = spacenavigator.open()
            if context.object:
                # Initialize first_state vectors
                self.first_state_location = Vector((0, 0, 0))
                self.first_state_rotation = Vector((0, 0, 0))

                # Copy object's location and rotation
                self.first_value_location = context.object.location.copy()
                self.value_location = context.object.location.copy()
                self.first_value_rotation = context.object.rotation_euler.copy()
                self.value_rotation = context.object.rotation_euler.copy()

                # Sensitivities
                self.sens = bpy.context.scene.transsens
                self.sensr = bpy.context.scene.rotsens

                if bpy.context.scene.upinv:
                    self.invup = -1
                else:
                    self.invup = 1
                if bpy.context.scene.frontinv:
                    self.invfront = -1
                else:
                    self.invfront = 1
                if bpy.context.scene.rightinv:
                    self.invright = -1
                else:
                    self.invright = 1
                if bpy.context.scene.rollinv:
                    self.invroll = -1
                else:
                    self.invroll = 1
                if bpy.context.scene.pitchinv:
                    self.invpitch = -1
                else:
                    self.invpitch = 1
                if bpy.context.scene.yawinv:
                    self.invyaw = -1
                else:
                    self.invyaw = 1
                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}
            else:
                self.report({'WARNING'}, "No active object, could not finish")
                return {'CANCELLED'}


class SNA_OT_Telekin(bpy.types.Operator):
    bl_idname = "sna.telekin"
    bl_label = "telekin"
    bl_description = "Run the telekinesis script"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            print("telekin")
            bpy.ops.object.modal_operator('INVOKE_DEFAULT')
        except Exception as exc:
            print(str(exc) + " | Error in execute function of telekin")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            print("telekin invoke")
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of telekin")
        return self.execute(context)


# --------------------   REGISTER ICONS
def sn_register_icons():
    icons = []
    bpy.types.Scene.telekindof_icons = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    for icon in icons:
        bpy.types.Scene.telekindof_icons.load(icon, os.path.join(icons_dir, icon + ".png"), 'IMAGE')


def sn_unregister_icons():
    bpy.utils.previews.remove(bpy.types.Scene.telekindof_icons)


# --------------------   REGISTER PROPERTIES
def sn_register_properties():
    bpy.types.Scene.upbinding = bpy.props.EnumProperty(name='UpBinding', description='Up/Down axes of the Space Mouse',
                                                       options=set(),
                                                       items=[('z', 'z', ''), ('x', 'x', ''), ('y', 'y', ''),
                                                              ('roll', 'roll', ''), ('pitch', 'pitch', ''),
                                                              ('yaw', 'yaw', '')])
    bpy.types.Scene.rightbinding = bpy.props.EnumProperty(name='RightBinding',
                                                          description='Right/Left Axis of the Space Mouse',
                                                          options=set(),
                                                          items=[('x', 'x', ''), ('y', 'y', ''), ('z', 'z', ''),
                                                                 ('roll', 'roll', ''), ('pitch', 'pitch', ''),
                                                                 ('yaw', 'yaw', '')])
    bpy.types.Scene.frontbinding = bpy.props.EnumProperty(name='FrontBinding',
                                                          description='Front/Back Axis Of Space Mouse', options=set(),
                                                          items=[('y', 'y', ''), ('x', 'x', ''), ('z', 'z', ''),
                                                                 ('roll', 'roll', ''), ('pitch', 'pitch', ''),
                                                                 ('yaw', 'yaw', '')])
    bpy.types.Scene.rollbinding = bpy.props.EnumProperty(name='RollBinding', description='Roll Axis of Space mouse',
                                                         options=set(),
                                                         items=[('roll', 'roll', ''), ('x', 'x', ''), ('y', 'y', ''),
                                                                ('z', 'z', ''), ('pitch', 'pitch', ''),
                                                                ('yaw', 'yaw', '')])
    bpy.types.Scene.pitchbinding = bpy.props.EnumProperty(name='PitchBinding', description='Pitch Axis of Space Mouse',
                                                          options=set(),
                                                          items=[('pitch', 'pitch', ''), ('x', 'x', ''), ('y', 'y', ''),
                                                                 ('z', 'z', ''), ('roll', 'roll', ''),
                                                                 ('yaw', 'yaw', '')])
    bpy.types.Scene.yawbinding = bpy.props.EnumProperty(name='YawBinding', description='Yaw axis of Space Mouse',
                                                        options=set(),
                                                        items=[('yaw', 'yaw', ''), ('x', 'x', ''), ('y', 'y', ''),
                                                               ('z', 'z', ''), ('roll', 'roll', ''),
                                                               ('picth', 'picth', '')])
    bpy.types.Scene.upinv = bpy.props.BoolProperty(name='UpInv', description='', options=set(), default=True)
    bpy.types.Scene.frontinv = bpy.props.BoolProperty(name='FrontInv', description='', options=set(), default=True)
    bpy.types.Scene.rightinv = bpy.props.BoolProperty(name='RightInv', description='', options=set(), default=True)
    bpy.types.Scene.transsens = bpy.props.FloatVectorProperty(name='TransSens',
                                                              description='Sensibility of movement in translation (x y z)',
                                                              subtype='NONE', unit='NONE', options=set(), precision=3,
                                                              default=(0.009999999776482582, 0.009999999776482582,
                                                                       0.009999999776482582), size=3, soft_min=0.0)
    bpy.types.Scene.rotsens = bpy.props.FloatVectorProperty(name='RotSens',
                                                            description='Sensibility of movement in rotation (roll pitch yaw)',
                                                            subtype='NONE', unit='NONE', options=set(), precision=3,
                                                            default=(0.009999999776482582, 0.009999999776482582,
                                                                     0.009999999776482582), size=3, soft_min=0.0)
    bpy.types.Scene.pitchinv = bpy.props.BoolProperty(name='PitchInv', description='', options=set(), default=True)
    bpy.types.Scene.rollinv = bpy.props.BoolProperty(name='RollInv', description='', options=set(), default=True)
    bpy.types.Scene.yawinv = bpy.props.BoolProperty(name='YawInv', description='', options=set(), default=True)


def sn_unregister_properties():
    del bpy.types.Scene.upbinding
    del bpy.types.Scene.rightbinding
    del bpy.types.Scene.frontbinding
    del bpy.types.Scene.rollbinding
    del bpy.types.Scene.pitchbinding
    del bpy.types.Scene.yawbinding
    del bpy.types.Scene.upinv
    del bpy.types.Scene.frontinv
    del bpy.types.Scene.rightinv
    del bpy.types.Scene.transsens
    del bpy.types.Scene.rotsens
    del bpy.types.Scene.pitchinv
    del bpy.types.Scene.rollinv
    del bpy.types.Scene.yawinv


# --------------------   REGISTER ADDON
def register():
    print("register")
    sn_register_icons()
    sn_register_properties()
    bpy.utils.register_class(SNA_PT_Shortcut_2C5D2)
    bpy.utils.register_class(SNA_PT_Axis_Settings_8B68A)
    bpy.utils.register_class(SNA_PT_Action_FC1AB)
    register_key_9DCCD()
    bpy.utils.register_class(SNA_OT_Telekin)
    bpy.utils.register_class(SNA_PT_Axis_Sensitivity_9D7BA)
    bpy.utils.register_class(SNA_PT_Shortcut_B5987)
    bpy.utils.register_class(SNA_PT_Inverse_Axis_3C0BA)
    bpy.utils.register_class(SNA_PT_Axis_binding_220EE)
    bpy.utils.register_class(ModalOperator)


# --------------------   UNREGISTER ADDON
def unregister():
    sn_unregister_icons()
    sn_unregister_properties()
    bpy.utils.unregister_class(ModalOperator)
    bpy.utils.unregister_class(SNA_PT_Axis_binding_220EE)
    bpy.utils.unregister_class(SNA_PT_Inverse_Axis_3C0BA)
    bpy.utils.unregister_class(SNA_PT_Shortcut_B5987)
    bpy.utils.unregister_class(SNA_PT_Axis_Sensitivity_9D7BA)
    bpy.utils.unregister_class(SNA_OT_Telekin)
    for key in addon_keymaps:
        km, kmi = addon_keymaps[key]
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(SNA_PT_Action_FC1AB)
    bpy.utils.unregister_class(SNA_PT_Axis_Settings_8B68A)
    bpy.utils.unregister_class(SNA_PT_Shortcut_2C5D2)
