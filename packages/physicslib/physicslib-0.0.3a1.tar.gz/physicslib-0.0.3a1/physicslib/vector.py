from math import acos


class Vector:
    """3D Vector. Could be used as 2D."""

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.data = [x, y, z]

    def __add__(self, other):
        return Vector(*(self.data[i] + other.data[i] for i in range(3)))

    def __iadd__(self, other):
        for i in range(3):
            self.data += other.data[i]
        return self

    def __mul__(self, coefficient: float):
        return Vector(*(self.data[i] * coefficient for i in range(3)))

    def __imul__(self, coefficient: float):
        for i in range(3):
            self.data[i] *= coefficient
        return self

    def __neg__(self):
        return Vector(*(-self.data[i] for i in range(3)))

    def __sub__(self, other):
        return Vector(*(self.data[i] - other.data[i] for i in range(3)))

    def __isub__(self, other):
        for i in range(3):
            self.data[i] -= other.data[i]
        return self

    def __truediv__(self, coefficient: float):
        return Vector(*(self.data[i] / coefficient for i in range(3)))

    def __itruediv__(self, coefficient: float):
        for i in range(3):
            self.data[i] /= coefficient
        return self

    def __eq__(self, other):
        return self.data == other.data

    def __repr__(self):
        return f"Vector({self.data[0]}, {self.data[1]}, {self.data[2]})"

    def length(self):
        """Vector euclidean length."""
        return sum(self.data[i] ** 2 for i in range(3)) ** 0.5

    def x(self) -> float:
        """Vector x-projection."""
        return self.data[0]

    def y(self) -> float:
        """Vector y-projection."""
        return self.data[1]

    def z(self) -> float:
        """Vector z-projection."""
        return self.data[2]

    def x_vector(self):
        """Vector x-projection as vector parallel of x-axis."""
        return Vector(self.data[0], 0, 0)

    def y_vector(self):
        """Vector y-projection as vector parallel of y-axis."""
        return Vector(0, self.data[1], 0)

    def z_vector(self):
        """Vector z-projection as vector parallel of z-axis."""
        return Vector(0, 0, self.data[2])

    def cross(self, other) -> float:
        """Cross product of self and other."""
        return sum(self.data[i] * other.data[i] for i in range(3))

    def angle_cos(self, other=None) -> float:
        """Cosine of angle between self and other."""
        if other is None:
            other = Vector(1, 0)
        return self.cross(other) / (self.length() * other.length())

    def angle(self, other) -> float:
        """Angle between self and other in radians."""
        return acos(self.angle(other))
