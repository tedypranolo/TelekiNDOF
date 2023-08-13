from enum import Enum


class Axis(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'
    PITCH = 'pitch'
    YAW = 'yaw'
    ROLL = 'roll'
    TRANSLATION = frozenset([X, Y, Z])
    ROTATION = frozenset([X, Y, Z])


class PanelProperties:
    def __init__(self):
        # Inversion flags
        self.inverse_x = False
        self.inverse_y = False
        self.inverse_z = False
        self.inverse_pitch = False
        self.inverse_yaw = False
        self.inverse_roll = False

        # Axis mapping
        self.map_x = Axis.X
        self.map_y = Axis.Y
        self.map_z = Axis.Z
        self.map_pitch = Axis.PITCH
        self.map_yaw = Axis.YAW
        self.map_roll = Axis.ROLL

        # Sensitivity properties for translations
        self.trans_sensitivity_x = 1.0
        self.trans_sensitivity_y = 1.0
        self.trans_sensitivity_z = 1.0

        # Sensitivity properties for rotations
        self.rotate_sensitivity_pitch = 1.0
        self.rotate_sensitivity_yaw = 1.0
        self.rotate_sensitivity_roll = 1.0


def process_value(self, state, axis_type):
    """
    Process a value from the state based on inversion and sensitivity settings.
    axis_type: 'x', 'y', 'z', 'pitch', 'yaw', 'roll'
    """
    mapped_axis = getattr(self, f"map_{axis_type}")
    value = getattr(state, mapped_axis)

    if axis_type in Axis.TRANSLATION:  # translation axis
        sensitivity = getattr(self, f"trans_sensitivity_{mapped_axis}")
    else:  # rotation axis
        sensitivity = getattr(self, f"rotate_sensitivity_{mapped_axis}")

    if getattr(self, f"inverse_{axis_type}"):
        value *= -1

    return value * sensitivity
