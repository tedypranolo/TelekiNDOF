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

from .ndof_operator import NdofOperator

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

import bpy
import bpy.utils.previews

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
            if "9DCCD" in NdofOperator.addon_keymaps:
                _, kmi = NdofOperator.addon_keymaps["9DCCD"]
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
            bpy.ops.object.space_transform('INVOKE_DEFAULT')
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
    NdofOperator.register_keymap()
    bpy.utils.register_class(SNA_OT_Telekin)
    bpy.utils.register_class(SNA_PT_Axis_Sensitivity_9D7BA)
    bpy.utils.register_class(SNA_PT_Shortcut_B5987)
    bpy.utils.register_class(SNA_PT_Inverse_Axis_3C0BA)
    bpy.utils.register_class(SNA_PT_Axis_binding_220EE)
    bpy.utils.register_class(NdofOperator)


# --------------------   UNREGISTER ADDON
def unregister():
    sn_unregister_icons()
    sn_unregister_properties()
    bpy.utils.unregister_class(NdofOperator)
    bpy.utils.unregister_class(SNA_PT_Axis_binding_220EE)
    bpy.utils.unregister_class(SNA_PT_Inverse_Axis_3C0BA)
    bpy.utils.unregister_class(SNA_PT_Shortcut_B5987)
    bpy.utils.unregister_class(SNA_PT_Axis_Sensitivity_9D7BA)
    bpy.utils.unregister_class(SNA_OT_Telekin)
    NdofOperator.unregister_keymap()
    bpy.utils.unregister_class(SNA_PT_Action_FC1AB)
    bpy.utils.unregister_class(SNA_PT_Axis_Settings_8B68A)
    bpy.utils.unregister_class(SNA_PT_Shortcut_2C5D2)
