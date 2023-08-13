from mathutils import Vector, Euler
from .item_access import ItemAccess


class Threeple(ItemAccess):
    def __init__(self, *args):
        if len(args) == 1:
            if isinstance(args[0], (tuple, list)) and len(args[0]) == 3:
                x, y, z = args[0]
            elif isinstance(args[0], Vector):
                x, y, z = args[0][0], args[0][1], args[0][2]
            elif isinstance(args[0], Euler):
                x, y, z = args[0].x, args[0].y, args[0].z
            # For handling FloatVectorProperty, you'd likely need to access the underlying collection
            # based on your specific use case. If it behaves just like a list, then the following should work:
            elif hasattr(args[0], '__getitem__') and len(args[0]) == 3:  # This should handle FloatVectorProperty
                x, y, z = args[0][0], args[0][1], args[0][2]
            else:
                raise ValueError(f"Invalid argument for initialization: {args}")
        elif len(args) == 3:
            x, y, z = args
        else:
            raise ValueError(f"Invalid arguments for initialization: {args}")

        self.vector = Vector((x, y, z))

    @property
    def x(self):
        return self.vector.x

    @x.setter
    def x(self, value):
        self.vector.x = value

    @property
    def y(self):
        return self.vector.y

    @y.setter
    def y(self, value):
        self.vector.y = value

    @property
    def z(self):
        return self.vector.z

    @z.setter
    def z(self, value):
        self.vector.z = value

    roll = x
    pitch = y
    yaw = z

    def as_tuple(self):
        return self.vector.x, self.vector.y, self.vector.z

    def __getitem__(self, key):
        if isinstance(key, str):
            return ItemAccess.__getitem__(self, key)  # Explicitly call the mixin's method
        elif isinstance(key, int):
            return self.vector[key]
        else:
            raise TypeError(f"Invalid key type: {type(key)}")

    def __setitem__(self, key, value):
        if isinstance(key, str):
            ItemAccess.__setitem__(self, key, value)  # Explicitly call the mixin's method
        elif isinstance(key, int):
            self.vector[key] = value
        else:
            raise TypeError(f"Invalid key type: {type(key)}")

    def __mul__(self, other):
        if isinstance(other, (Vector, Euler, Threeple)):
            return Threeple(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            new_vector = self.vector * other
            return Threeple(new_vector.x, new_vector.y, new_vector.z)
        # Handle bpy_prop_array by checking for sequence-like behavior
        elif hasattr(other, '__len__') and hasattr(other, '__getitem__') and len(other) == 3:
            return Threeple(self.x * other[0], self.y * other[1], self.z * other[2])
        else:
            raise ValueError(f"Unsupported operand type for *: '{type(other)}'")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __add__(self, other):
        if isinstance(other, (Vector, Euler, Threeple)):
            return Threeple(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise ValueError(f"Unsupported operand type for +: '{type(other)}'")

    def __radd__(self, other):
        return self.__add__(other)

    def __iter__(self):
        return iter(self.vector)
