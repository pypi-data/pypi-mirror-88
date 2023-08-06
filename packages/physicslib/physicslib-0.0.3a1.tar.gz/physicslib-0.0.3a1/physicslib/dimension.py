"""Module with Dimension class and dimension constants."""

from typing import Final

from physicslib.formating import superscripted


class Dimension:
    """Physics dimension."""

    BASE_DIMENSIONS_NUMBER = 7

    def __init__(
        self,
        length: int = 0,
        mass: int = 0,
        time: int = 0,
        amperage: int = 0,
        temperature: int = 0,
        substance_amount: int = 0,
        luminous_intensity: int = 0
    ):
        self.data = [length, mass, time, amperage, temperature, substance_amount, luminous_intensity]

    def __repr__(self) -> str:
        string = "Dimension("
        for i in range(self.BASE_DIMENSIONS_NUMBER):
            string += f"{self.data[i]}, "
        return string[:-2] + ")"

    def __str__(self) -> str:
        name_chars = ["L", "M", "T", "I", "\u0398", "N", "J"]
        string = ""
        for i in range(self.BASE_DIMENSIONS_NUMBER):
            if self.data[i] == 0:
                continue
            string += name_chars[i]
            if self.data[i] != 1:
                string += superscripted(self.data[i])
        return string if string else "scalar"

    def __mul__(self, other):
        return Dimension(*(self.data[i] + other.data[i] for i in range(self.BASE_DIMENSIONS_NUMBER)))

    def __imul__(self, other):
        for i in range(5):
            self.data[i] += other.data[i]
        return self

    def __truediv__(self, other):
        return Dimension(*(self.data[i] - other.data[i] for i in range(self.BASE_DIMENSIONS_NUMBER)))

    def __itruediv__(self, other):
        for i in range(self.BASE_DIMENSIONS_NUMBER):
            self.data[i] -= other.data[i]
        return self

    def __pow__(self, power):
        return Dimension(*(self.data[i] * power for i in range(self.BASE_DIMENSIONS_NUMBER)))

    def __ipow__(self, power):
        for i in range(self.BASE_DIMENSIONS_NUMBER):
            self.data[i] *= power
        return self

    def __eq__(self, other) -> bool:
        return self.data == other.data

    def copy(self):
        """Copy object."""
        return Dimension(*self.data)


# Base dimensions
SCALAR: Final = Dimension()
LENGTH: Final = Dimension(length=1)
TIME: Final = Dimension(time=1)
MASS: Final = Dimension(mass=1)
AMPERAGE: Final = Dimension(amperage=1)
TEMPERATURE: Final = Dimension(temperature=1)
SUBSTANCE_AMOUNT: Final = Dimension(substance_amount=1)
LUMINOUS_INTENSITY: Final = Dimension(luminous_intensity=1)

# Derived dimensions
SQUARE: Final = LENGTH ** 2
VOLUME: Final = LENGTH ** 3
DENSITY: Final = MASS / VOLUME
VELOCITY: Final = LENGTH / TIME
ACCELERATION: Final = VELOCITY / TIME
FORCE: Final = MASS * ACCELERATION
PRESSURE: Final = FORCE / SQUARE
MOMENTUM: Final = VELOCITY * MASS
ENERGY: Final = FORCE * LENGTH
POWER: Final = ENERGY / TIME
ELECTRIC_CHARGE: Final = AMPERAGE * TIME
ELECTRIC_POTENTIAL: Final = ENERGY / ELECTRIC_CHARGE
ELECTRIC_RESISTANCE: Final = ELECTRIC_POTENTIAL / AMPERAGE
CAPACITANCE: Final = ELECTRIC_CHARGE / ELECTRIC_POTENTIAL
