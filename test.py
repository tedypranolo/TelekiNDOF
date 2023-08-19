from mathutils import Matrix, Vector, Euler
from math import radians
import math

translation = Vector((0, 0, 0))
rotation = Euler((0, 0, radians(10)), 'XYZ')
print(f"rotation {rotation}")
mat_translation = Matrix.Translation(translation)
mat_rotation = rotation.to_matrix().to_4x4()


transform_matrix = mat_translation @ mat_rotation
print(transform_matrix)
