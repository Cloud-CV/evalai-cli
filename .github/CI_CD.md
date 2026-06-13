# CI/CD and Release

This repository uses [GitHub Actions](https://github.com/Cloud-CV/evalai-cli/actions) for continuous integration and package publishing.

## Workflows

| Workflow | Purpose |
|----------|---------|
| `ci-cd.yml` | Lint, test, and publish packages |
| `upload-coverage.yml` | Upload test coverage to Codecov after CI succeeds |

## Required repository secrets

Configure these under **Settings → Secrets and variables → Actions**:

| Secret | Used for |
|--------|----------|
| `CODECOV_TOKEN` | Codecov upload |
| `TEST_PYPI_USERNAME` | TestPyPI publish on `staging` pushes |
| `TEST_PYPI_PASSWORD` | TestPyPI publish on `staging` pushes |
| `PYPI_API_TOKEN` | Production PyPI publish on tag pushes |

## GitHub environments

Create optional environments for publish job scoping and approvals:

- `staging` — TestPyPI publishes from the `staging` branch
- `production` — PyPI publishes from git tags

## Release process

1. Bump the version in `evalai/version.py`.
2. Push to `staging` to publish a test build to [TestPyPI](https://test.pypi.org/project/evalai/).
3. Create and push a git tag to publish to [PyPI](https://pypi.org/project/evalai/).

CI runs on pull requests and pushes to `master` and `staging`.
