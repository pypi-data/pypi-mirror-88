"""Module with ScalarPhysical and VectorPhysical classes."""

from typing import Final

from physicslib import unit
from physicslib.vector import Vector


def unit_convert(func):
    """
    Decorator for Physical's methods.
    Converts second argument (`other`) to `other.to_unit(self.unit)`.
    """
    def wrapper(self, other):
        return func(self, other.to_unit(self.unit))

    return wrapper


def convert_float(func):
    """
    Decorator for Physical's methods.
    Converts second argument (`other`) to ScalarPhysical.
    """
    def wrapper(self, other):
        if not isinstance(other, (ScalarPhysical, VectorPhysical)):
            other = ScalarPhysical(other)
        return func(self, other)

    return wrapper


class ScalarPhysical:
    """Scalar physical quantity, like mass value or distance length."""
    def __init__(self, value: float = 0, unit_: unit.Unit = unit.ONE):
        self.value = value
        self.unit = unit_.copy()

    def __repr__(self):
        return f"ScalarPhysical({self.value}, {repr(self.unit)})"

    def __str__(self):
        return f"{self.value}\u22C5{str(self.unit)}" if self.unit != unit.ONE else str(self.value)

    @convert_float
    @unit_convert
    def __add__(self, other):
        return ScalarPhysical(self.value + other.value, self.unit)

    def __radd__(self, other):
        return self + other

    @convert_float
    @unit_convert
    def __iadd__(self, other):
        self.value += other.value
        return self

    @convert_float
    def __mul__(self, other):
        if isinstance(other, VectorPhysical):
            return other * self
        return ScalarPhysical(self.value * other.value, self.unit * other.unit)

    def __rmul__(self, other):
        return self * other

    @convert_float
    def __imul__(self, other):
        self.value *= other.value
        self.unit *= other.unit

    def __neg__(self):
        return ScalarPhysical(-self.value, self.unit)

    @convert_float
    @unit_convert
    def __sub__(self, other):
        return ScalarPhysical(self.value - other.value, self.unit)

    def __rsub__(self, other):
        return -self + other

    @convert_float
    @unit_convert
    def __isub__(self, other):
        self.value -= other.value
        return self

    @convert_float
    def __truediv__(self, other):
        return ScalarPhysical(self.value / other.value, self.unit / other.unit)

    @convert_float
    def __rtruediv__(self, other):
        return other / self

    @convert_float
    def __itruediv__(self, other):
        self.value /= other.value
        self.unit /= other.unit
        return self

    def __pow__(self, power):
        return ScalarPhysical(self.value ** power, self.unit ** power)

    def __ipow__(self, power):
        self.value **= power
        self.unit **= power

    @convert_float
    @unit_convert
    def __eq__(self, other):
        return self.value == other.value

    def to_unit(self, unit_: unit.Unit):
        """Equal physical quantity with new unit."""
        if self.unit.dimension != unit_.dimension:
            raise AttributeError(f"Bad unit dimension: expected {repr(self.unit.dimension)} but got {repr(unit_)}.")
        return ScalarPhysical(self.value * self.unit.coefficient / unit_.coefficient, unit_)

    def copy(self):
        return ScalarPhysical(self.value, self.unit)


class VectorPhysical:
    """Vector physical quantity, like velocity or force."""
    def __init__(self, value: Vector = Vector(), unit_: unit.Unit = unit.ONE):
        self.value = value
        self.unit = unit_

    def __repr__(self):
        return f"VectorPhysical({self.value}, {repr(self.unit)})"

    def __str__(self):
        return f"{self.value}\u22C5{str(self.unit)}" if self.unit != unit.ONE else str(self.value)

    @unit_convert
    def __add__(self, other):
        return ScalarPhysical(self.value + other.value, self.unit)

    @unit_convert
    def __iadd__(self, other):
        self.value += other.value
        return self

    @convert_float
    def __mul__(self, other: ScalarPhysical):
        return VectorPhysical(self.value * other.value, self.unit * other.unit)

    @convert_float
    def __imul__(self, other: ScalarPhysical):
        self.value *= other.value
        self.unit *= other.unit
        return self

    def __rmul__(self, other: ScalarPhysical):
        return self * other

    def __neg__(self):
        return VectorPhysical(-self.value, self.unit)

    @unit_convert
    def __sub__(self, other):
        return VectorPhysical(self.value - other.value, self.unit)

    @unit_convert
    def __isub__(self, other):
        self.value -= other.value
        return self

    @convert_float
    def __truediv__(self, other):
        return VectorPhysical(self.value / other.value, self.unit / other.unit)

    @convert_float
    def __itruediv__(self, other):
        self.value /= other.value
        self.unit /= other.unit
        return self

    @unit_convert
    def __eq__(self, other):
        return self.value == other.value

    def to_unit(self, unit_: unit.Unit):
        """Equal physical quantity with new unit."""
        if self.unit.dimension != unit_.dimension:
            raise AttributeError("Bad unit dimension.")
        return VectorPhysical(self.value * self.unit.coefficient / unit_.coefficient, unit_)

    def to_scalar(self) -> ScalarPhysical:
        """ScalarPhysical with value equal to the length of self.value and the same unit."""
        return ScalarPhysical(self.value.length(), self.unit)

    def x(self) -> ScalarPhysical:
        return ScalarPhysical(self.value.x(), self.unit)

    def y(self) -> ScalarPhysical:
        return ScalarPhysical(self.value.y(), self.unit)

    def z(self) -> ScalarPhysical:
        return ScalarPhysical(self.value.z(), self.unit)

    def x_vector(self):
        return VectorPhysical(self.value.x_vector(), self.unit)

    def y_vector(self):
        return VectorPhysical(self.value.y_vector(), self.unit)

    def z_vector(self):
        return VectorPhysical(self.value.z_vector(), self.unit)


Physical = ScalarPhysical
