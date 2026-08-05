# Contributing

Contributions are welcome through GitHub issues and pull requests.

## Development setup

Python 3.10 or newer, [uv](https://docs.astral.sh/uv/), and Git are required.

```console
uv sync --all-groups
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

Run all checks before opening a pull request:

```console
uv run pre-commit run --all-files
uv run pytest
uv run pyright
uv build
uvx twine check dist/*
```

## Changes

- Keep geometry at the default origin. Placement belongs to consumer designs.
- Preserve explicit units and document every distance as millimetres.
- Add tests for geometry calculations, validation, and public API changes.
- Base new presets on measured hardware and document the product or source.
- Update user-facing documentation with behavior changes.

## Commit messages

Every commit and pull-request title must follow
[Conventional Commits](https://www.conventionalcommits.org/):

```text
feat: add a measured 30 mm pin preset
fix: forward tessellation to knob cylinders
docs: explain edge-to-edge knob spacing
```

Use `!` or a `BREAKING CHANGE:` footer for incompatible API changes. The
release automation uses these messages to choose the semantic version and
generate the changelog. See [VERSIONING.md](VERSIONING.md).

## Pull requests

Keep pull requests focused, explain how the result was tested, and ensure all
required checks pass.
