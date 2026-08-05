# Publishing setup

The workflows use GitHub's OpenID Connect identity and PyPI trusted publishing.
No PyPI API-token secret is required.

## One-time GitHub setup

1. Create public repository `nomike/pythonscad-pincutout` with default branch
   `main`.
2. In **Settings → Environments**, create `testpypi` and `pypi`.
3. Optionally protect `pypi` with required reviewers. Do not add secrets.
4. In **Settings → Actions → General**, allow GitHub Actions to create and
   approve pull requests so release-please can maintain its release PR.
5. Protect `main` and require the CI, pre-commit, and commit-message checks
   after their first successful runs.

Release creation and publishing are jobs in one workflow. This avoids a
personal access token solely to trigger a second workflow from a
`GITHUB_TOKEN`-created release.

## One-time TestPyPI setup

At <https://test.pypi.org/manage/account/publishing/>, add a pending trusted
publisher:

- PyPI project name: `pythonscad-pincutout`
- Owner: `nomike`
- Repository: `pythonscad-pincutout`
- Workflow: `publish.yml`
- Environment: `testpypi`

The pending publisher can create the project on its first successful upload.
Every push to `main` publishes a unique development version.

## One-time PyPI setup

At <https://pypi.org/manage/account/publishing/>, add the same pending trusted
publisher with environment `pypi`. The release workflow publishes to TestPyPI
first and production PyPI second.

## Permanent forks

A fork owner should:

1. Change project URLs and author metadata in `pyproject.toml`.
2. Choose a unique distribution name; PyPI names are global.
3. Change badge and clone URLs in `README.md`.
4. Create matching GitHub environments.
5. Register trusted publishers using the fork owner, repository, workflow
   filename, and environment names.
6. Update this document's examples.

No workflow secrets contain the original owner's identity. The OIDC claim is
derived from the repository and environment at runtime.
