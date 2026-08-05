# PythonSCAD Pin Cutout

[![CI](https://github.com/nomike/pythonscad-pincutout/actions/workflows/ci.yml/badge.svg)](https://github.com/nomike/pythonscad-pincutout/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pythonscad-pincutout)](https://pypi.org/project/pythonscad-pincutout/)
[![Python](https://img.shields.io/pypi/pyversions/pythonscad-pincutout)](https://pypi.org/project/pythonscad-pincutout/)

Reusable, parametric recesses for hot-gluing metal brooch pins into
[PythonSCAD](https://pythonscad.org/) models.

The generated cutter is a rectangular pocket with two circular recesses. The
recesses leave matching knobs in the printed part, which locate the pin and
give the hot glue more surface area.

## Installation

PythonSCAD Pin Cutout requires PythonSCAD 1.1.0 or newer:

```console
pip install pythonscad-pincutout
```

## Usage

Import the package, render a cutter, position it for your design, and subtract
it from the solid:

```python
import pincutout
from pythonscad import cube

base = cube([40, 40, 2])
pin_cutter = pincutout.PinCutout.generic_25mm().render().translate([7.25, 17.45, 0])

show(base - pin_cutter)
```

`render()` deliberately applies no X/Y positioning or model-specific
centering. The pocket begins at PythonSCAD's default origin and is shifted
downward only by `epsilon` to make the boolean operation robust.

### Custom dimensions

All dimensions are in millimetres:

```python
cutout = pincutout.PinCutout(
    length=30.0,
    width=6.0,
    depth=0.6,
    knob_diameter=2.4,
    knob_gap=8.0,
    epsilon=0.001,
    fn=128,
).render()
```

- `length`, `width`, and `depth` describe the rectangular pocket.
- `knob_diameter` is the diameter of each circular recess.
- `knob_gap` is the **edge-to-edge** space between the recesses. Their
  centre-to-centre distance is `knob_gap + knob_diameter`.
- `epsilon` extends overlapping geometry to avoid coincident boolean faces.
- `fn` controls the circular tessellation.

Invalid or non-finite dimensions are rejected before rendering. The knobs
must fit completely within the pocket.

### Presets

`PinCutout.generic_25mm()` reproduces the measured geometry this project was
extracted from: a `25.5 × 5.1 × 0.4 mm` pocket with `2 mm` knobs separated by
a `6 mm` edge-to-edge gap. It is intentionally generic and does not claim
compatibility with a particular vendor.

Preset values can be overridden:

```python
cutout = pincutout.PinCutout.generic_25mm(depth=0.6, fn=64)
```

Future presets should be based on measured hardware and identify their source.

## Development

Clone the repository and install the project and development tools:

```console
git clone https://github.com/nomike/pythonscad-pincutout.git
cd pythonscad-pincutout
uv sync --all-groups
pre-commit install --hook-type pre-commit --hook-type commit-msg
uv run pre-commit run --all-files
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for commits and pull requests,
[VERSIONING.md](VERSIONING.md) for automated releases, and
[PUBLISHING.md](PUBLISHING.md) for the one-time GitHub and package-index setup.

## License

[MIT](LICENSE)
