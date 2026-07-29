"""Simulator-neutral AC metric calculations from complex simulator outputs."""

import cmath
import math
from typing import Tuple


def y_to_s(
    y11: complex,
    y12: complex,
    y21: complex,
    y22: complex,
    reference_impedance: float = 50.0,
) -> Tuple[complex, complex, complex, complex]:
    """Convert a two-port admittance matrix to S parameters.

    The returned order is S11, S12, S21, S22.  This is the same physical
    definition used in the canonical ngspice benchmark netlist:
    ``S = (I - Z0*Y) * inv(I + Z0*Y)``.
    """
    z0 = float(reference_impedance)
    a11 = 1.0 + z0 * y11
    a12 = z0 * y12
    a21 = z0 * y21
    a22 = 1.0 + z0 * y22
    b11 = 1.0 - z0 * y11
    b12 = -z0 * y12
    b21 = -z0 * y21
    b22 = 1.0 - z0 * y22
    determinant = a11 * a22 - a12 * a21
    if abs(determinant) < 1e-30:
        raise ValueError("singular I + Z0*Y matrix")
    return (
        (b11 * a22 - b12 * a21) / determinant,
        (-b11 * a12 + b12 * a11) / determinant,
        (b21 * a22 - b22 * a21) / determinant,
        (-b21 * a12 + b22 * a11) / determinant,
    )


def polar(value: complex) -> Tuple[float, float]:
    """Return magnitude and phase in degrees for a complex value."""
    return abs(value), math.degrees(cmath.phase(value))

