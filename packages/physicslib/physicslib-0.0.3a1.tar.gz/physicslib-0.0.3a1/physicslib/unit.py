"""Unit class and unit constants."""

from typing import Final, Union

from physicslib import dimension
from physicslib.formating import superscripted


def convert_float(func):
    """
    Decorator for Unit class.
    Converts second argument (`other`) to Unit.
    """
    def wrapper(self, other):
        if not isinstance(other, Unit):
            other = Unit(other)
        return func(self, other)

    return wrapper


class Unit:
    """Unit of measurement."""

    def __init__(self, coefficient: float = 1, dim: dimension.Dimension = dimension.SCALAR):
        self.coefficient = coefficient
        self.dimension = dim.copy()

    def __repr__(self):
        return f"Unit({self.coefficient}, {repr(self.dimension)})"

    def __str__(self):
        string = ""
        if self.coefficient == -1:
            string += "-"
        elif self.coefficient != 1:
            string += str(self.coefficient)
            if self.dimension != dimension.SCALAR:
                string += "\u22C5"
        base_units = ["m", "kg", "s", "A", "K", "mol", "cd"]
        for i in range(dimension.Dimension.BASE_DIMENSIONS_NUMBER):
            if self.dimension.data[i] == 0:
                continue
            if string and string[-1].isalpha():
                string += "\u22C5"
            string += base_units[i]
            if self.dimension.data[i] != 1:
                string += superscripted(self.dimension.data[i])
        return string if string else "scalar_unit"

    @convert_float
    def __mul__(self, other):
        return Unit(self.coefficient * other.coefficient, self.dimension * other.dimension)

    @convert_float
    def __rmul__(self, other):
        return self * other

    @convert_float
    def __imul__(self, other):
        self.coefficient *= other.coefficient
        self.dimension *= other.dimension
        return self

    @convert_float
    def __truediv__(self, other):
        return Unit(self.coefficient / other.coefficient, self.dimension / other.dimension)

    @convert_float
    def __rtruediv__(self, other):
        return other / self

    @convert_float
    def __itruediv__(self, other):
        self.coefficient /= other.coefficient
        self.dimension /= other.dimension
        return self

    def __pow__(self, power):
        return Unit(self.coefficient ** power, self.dimension ** power)

    def __ipow__(self, power):
        self.coefficient **= power
        self.dimension **= power
        return self

    @convert_float
    def __eq__(self, other):
        return self.coefficient == self.coefficient and self.dimension == other.dimension

    def copy(self):
        """Unit copy."""
        return Unit(self.coefficient, self.dimension)


# Base SI units
ONE: Final = Unit()
METER: Final = Unit(1, dimension.LENGTH)
SECOND: Final = Unit(1, dimension.TIME)
KILOGRAM: Final = Unit(1, dimension.MASS)
AMPER: Final = Unit(1, dimension.AMPERAGE)
KELVIN: Final = Unit(1, dimension.TEMPERATURE)
MOLE: Final = Unit(1, dimension.SUBSTANCE_AMOUNT)
CANDELA: Final = Unit(1, dimension.LUMINOUS_INTENSITY)

# Derived SI units
NEWTON: Final = Unit(1, dimension.FORCE)
PASCAL: Final = Unit(1, dimension.PRESSURE)
JOULE: Final = Unit(1, dimension.ENERGY)
WATT: Final = Unit(1, dimension.POWER)
COULOMB: Final = Unit(1, dimension.ELECTRIC_CHARGE)
VOLT: Final = Unit(1, dimension.ELECTRIC_POTENTIAL)
OHM: Final = Unit(1, dimension.ELECTRIC_RESISTANCE)
FARAD: Final = Unit(1, dimension.CAPACITANCE)

# non-SI units
MINUTE: Final = 60 * SECOND
HOUR: Final = 60 * MINUTE
GRAM: Final = 0.001 * KILOGRAM
TON: Final = 1000 * KILOGRAM
