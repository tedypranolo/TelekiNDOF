import bpy
from bpy.props import FloatVectorProperty, FloatProperty
from mathutils import Vector
from . import spacenavigator
from . import space_utils
from . import utils
from .threeple import Threeple


class NdofOperator(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "object.space_transform"
    bl_label = "Simple Modal Operator"

    addon_keymaps = {}
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

    @staticmethod
    def is_shortcut_invoked(event):
        _, kmi = NdofOperator.addon_keymaps.get("9DCCD", (None, None))
        if kmi:
            # Check against the registered keymap
            if event.type == kmi.type and event.value == 'PRESS':
                if event.ctrl == kmi.ctrl and \
                        event.alt == kmi.alt and \
                        event.shift == kmi.shift:
                    print("Finishing the modal operator due to same shortcut.")
                    return True
        return False

    def modal(self, context, event):
        if self.is_shortcut_invoked(event):
            return {"FINISHED"}

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

            target = utils.get_active_object()

            rotation_quat = (delta_rotation * self.sensr).as_euler().to_quaternion()
            delta_trans = (delta_location * self.sens).vector
            space_utils.translate_in_view(target, delta_trans)
            space_utils.rotate_in_view(target, rotation_quat)
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

    @staticmethod
    def register_keymap():
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
            NdofOperator.addon_keymaps['9DCCD'] = (km, kmi)

    @staticmethod
    def unregister_keymap():
        for key in NdofOperator.addon_keymaps:
            km, kmi = NdofOperator.addon_keymaps[key]
            km.keymap_items.remove(kmi)
        NdofOperator.addon_keymaps.clear()