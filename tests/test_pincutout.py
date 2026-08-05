"""Tests for the public pin-cutout API."""

from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError
from types import SimpleNamespace

import pytest

from pincutout import PinCutout


class FakeShape:
    """Record the small subset of PythonSCAD operations used by the library."""

    def __init__(self, operation, *arguments):
        self.operation = operation
        self.arguments = arguments

    def translate(self, vector):
        return FakeShape("translate", self, vector)

    def down(self, distance):
        return FakeShape("down", self, distance)

    def __sub__(self, other):
        return FakeShape("difference", self, other)


@pytest.fixture
def fake_pythonscad(monkeypatch):
    calls = {"cube": [], "cylinder": []}

    def cube(size):
        calls["cube"].append(size)
        return FakeShape("cube", size)

    def cylinder(*, d, h, fn):
        arguments = {"d": d, "h": h, "fn": fn}
        calls["cylinder"].append(arguments)
        return FakeShape("cylinder", arguments)

    module = SimpleNamespace(cube=cube, cylinder=cylinder)
    monkeypatch.setitem(sys.modules, "pythonscad", module)
    return calls


def test_defaults_and_generic_preset_are_equivalent():
    expected = PinCutout(
        length=25.5,
        width=5.1,
        depth=0.4,
        knob_diameter=2.0,
        knob_gap=6.0,
        epsilon=0.001,
        fn=256,
    )

    assert PinCutout() == expected
    assert PinCutout.generic_25mm() == expected
    assert PinCutout.generic_25mm(depth=0.6, fn=64).depth == 0.6
    assert PinCutout.generic_25mm(depth=0.6, fn=64).fn == 64


def test_model_is_immutable():
    model = PinCutout()

    with pytest.raises(FrozenInstanceError):
        model.length = 30


def test_knob_centers_use_edge_to_edge_gap():
    model = PinCutout(length=20, width=6, knob_diameter=2, knob_gap=4)

    assert model.knob_centers == ((7.0, 3.0), (13.0, 3.0))
    center_distance = model.knob_centers[1][0] - model.knob_centers[0][0]
    assert center_distance - model.knob_diameter == model.knob_gap


@pytest.mark.parametrize(
    ("field", "value", "exception"),
    [
        ("length", "25", TypeError),
        ("width", True, TypeError),
        ("depth", 0, ValueError),
        ("knob_diameter", -1, ValueError),
        ("epsilon", float("inf"), ValueError),
        ("knob_gap", "6", TypeError),
        ("knob_gap", -1, ValueError),
        ("knob_gap", float("nan"), ValueError),
        ("fn", 3.5, TypeError),
        ("fn", True, TypeError),
        ("fn", 2, ValueError),
    ],
)
def test_invalid_scalar_parameters_are_rejected(field, value, exception):
    with pytest.raises(exception):
        PinCutout(**{field: value})


def test_knobs_must_fit_width_and_length():
    with pytest.raises(ValueError, match="must not exceed width"):
        PinCutout(width=1, knob_diameter=2)

    with pytest.raises(ValueError, match="must fit inside length"):
        PinCutout(length=9, knob_diameter=2, knob_gap=6)

    assert PinCutout(length=10, width=2, knob_diameter=2, knob_gap=6)


def test_render_forwards_geometry_parameters_at_default_origin(fake_pythonscad):
    model = PinCutout(
        length=20,
        width=6,
        depth=0.5,
        knob_diameter=2,
        knob_gap=4,
        epsilon=0.01,
        fn=48,
    )

    rendered = model.render()

    assert fake_pythonscad["cube"] == [[20, 6, 0.51]]
    assert fake_pythonscad["cylinder"] == [
        {"d": 2, "h": 0.53, "fn": 48},
        {"d": 2, "h": 0.53, "fn": 48},
    ]
    assert rendered.operation == "down"
    assert rendered.arguments[1] == 0.01

    second_difference = rendered.arguments[0]
    first_difference = second_difference.arguments[0]
    left_translation = first_difference.arguments[1]
    right_translation = second_difference.arguments[1]
    assert left_translation.arguments[1] == [7.0, 3.0, -0.01]
    assert right_translation.arguments[1] == [13.0, 3.0, -0.01]
