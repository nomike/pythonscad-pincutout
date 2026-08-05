"""Parametric PythonSCAD geometry for brooch-pin recesses."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pythonscad import PyOpenSCAD


def _require_positive_real(name: str, value: object) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and greater than zero")


def _require_nonnegative_real(name: str, value: object) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and non-negative")


def _require_fn(value: object) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("fn must be an integer")
    if value < 3:
        raise ValueError("fn must be at least 3")


@dataclass(frozen=True, slots=True)
class PinCutout:
    """A rectangular pin recess with two circular glue-retention knobs.

    All measurements are millimetres. ``knob_gap`` is the edge-to-edge gap
    between the two circular knobs, not their centre-to-centre distance.
    Geometry is returned at the PythonSCAD default origin; placement belongs
    to the consuming design.
    """

    length: float = 25.5
    width: float = 5.1
    depth: float = 0.4
    knob_diameter: float = 2.0
    knob_gap: float = 6.0
    epsilon: float = 0.001
    fn: int = 256

    def __post_init__(self) -> None:
        """Validate that all dimensions describe renderable geometry."""
        for name in ("length", "width", "depth", "knob_diameter", "epsilon"):
            _require_positive_real(name, getattr(self, name))

        _require_nonnegative_real("knob_gap", self.knob_gap)
        _require_fn(self.fn)

        if self.knob_diameter > self.width:
            raise ValueError("knob_diameter must not exceed width")
        if self.knob_gap + 2 * self.knob_diameter > self.length:
            raise ValueError("knobs and their gap must fit inside length")

    @classmethod
    def generic_25mm(
        cls,
        *,
        length: float = 25.5,
        width: float = 5.1,
        depth: float = 0.4,
        knob_diameter: float = 2.0,
        knob_gap: float = 6.0,
        epsilon: float = 0.001,
        fn: int = 256,
    ) -> PinCutout:
        """Return the generic 25 mm pin preset, optionally customized."""
        return cls(
            length=length,
            width=width,
            depth=depth,
            knob_diameter=knob_diameter,
            knob_gap=knob_gap,
            epsilon=epsilon,
            fn=fn,
        )

    @property
    def knob_centers(self) -> tuple[tuple[float, float], tuple[float, float]]:
        """Return the two XY knob centres, useful for inspection and testing."""
        offset = self.knob_gap / 2 + self.knob_diameter / 2
        center_x = self.length / 2
        center_y = self.width / 2
        return (
            (center_x - offset, center_y),
            (center_x + offset, center_y),
        )

    def render(self) -> PyOpenSCAD:
        """Build and return the cutout at the PythonSCAD default origin."""
        from pythonscad import cube, cylinder

        cutter_height = self.depth + self.epsilon * 3
        result = cube([self.length, self.width, self.depth + self.epsilon])

        for center_x, center_y in self.knob_centers:
            knob = cylinder(
                d=self.knob_diameter,
                h=cutter_height,
                fn=self.fn,
            ).translate([center_x, center_y, -self.epsilon])
            result = result - knob

        return result.down(self.epsilon)
