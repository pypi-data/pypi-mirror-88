"""
Declarations of some physical constants. See https://en.wikipedia.org/wiki/Physical_constant for information.
Also see https://en.wikipedia.org/wiki/List_of_physical_constants for list of them.
"""

from typing import Final

from physicslib import unit
from physicslib.physical import Physical, Vector, VectorPhysical

LIGHT_SPEED: Final = Physical(299_792_458, unit.METER / unit.SECOND)
"""Speed of light in vacuum (`c`). See https://en.wikipadia.org/wiki/Speed_of_light for information."""
GRAVITATIONAL_CONSTANT: Final = Physical(6.674_301_515, 1e-11 * unit.METER ** 3 * unit.SECOND ** -2 / unit.KILOGRAM)
"""Gravitational constant (`G`). See https://en.wikipedia.org/wiki/Gravitational_constant for information."""
PLANCK_CONSTANT: Final = Physical(6.626_070_15, 1e-34 * unit.JOULE / unit.SECOND)
"""Plank constant (`h`). See https://en.wikipedia.org/wiki/Planck_constant for information."""
VACUUM_PERMITTIVITY: Final = Physical(8.854_187_812_813, 1e-12 * unit.FARAD / unit.METER)
"""Vacuum permittivity (`epsilon-zero`). See https://en.wikipedia.org/wiki/Vacuum_permittivity for information."""
ELEMENTARY_CHARGE: Final = Physical(1.602_176_634, 1e-19 * unit.COULOMB)
"""Charge of electron (`e`). See https://en.wikipedia.org/wiki/Elementary_charge for information."""
AVOGADRO_CONSTANT: Final = Physical(6.022_140_76, 1e-23 / unit.MOLE)
"""Avogadro constant (`N_A`). See https://en.wikipedia.org/wiki/Avogadro_constant for information."""
BOLTZMANN_CONSTANT: Final = Physical(1.380_649, 1e-23 * unit.JOULE / unit.KELVIN)
"""Boltzmann constant (`k`). See https://en.wikipedia.org/wiki/Boltzmann_constant for information."""
GAS_CONSTANT: Final = Physical(8.314_462_618_153_24, unit.JOULE / (unit.KELVIN * unit.MOLE))
"""Universal gas constant (`R`). See https://en.wikipedia.org/wiki/Gas_constant for information."""
ELECTRON_MASS: Final = Physical(9.109_383_701_528, 1e-31 * unit.KILOGRAM)
"""Mass of electron (`m_e`). See https://en.wikipedia.org/wiki/Electron for information."""
PROTON_MASS: Final = Physical(1.672_621_923_695, 1e-27 * unit.KILOGRAM)
"""Mass of proton (`m_p`). See https://en.wikipedia.org/wiki/Proton for information."""
NEUTRON_MASS: Final = Physical(1.674_927_498_05, 1e-27 * unit.KILOGRAM)
"""Mass of neutron. See https://en.wikipedia.org/wiki/Neutron for information."""
