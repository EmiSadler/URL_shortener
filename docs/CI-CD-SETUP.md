# CI/CD Pipeline Setup Guide

This document explains how to set up and use the GitHub Actions CI/CD pipeline for the URL Shortener project.

## 🏗️ Pipeline Overview

The CI/CD pipeline automatically runs on:

- **Push** to `main` and `develop` branches
- **Pull Requests** to `main` and `develop` branches

### Pipeline Jobs

1. **🧪 Test Suite**: Multi-version Python testing (3.8-3.11)
2. **🔒 Security**: Vulnerability and security scanning
3. **📋 Quality**: Code formatting and type checking
4. **🔗 Integration**: End-to-end API testing
5. **📊 Status**: Aggregate results and reporting

## 🚀 Quick Setup

### 1. Repository Setup

```bash
# Push the CI configuration to GitHub
git add .github/ scripts/ pyproject.toml setup.cfg requirements-dev.txt
git commit -m "Add CI/CD pipeline configuration"
git push origin main
```

### 2. Branch Protection Rules

In your GitHub repository settings:

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Restrict pushes that create merge conflicts
   - Select required status checks:
     - `Test Suite (3.11)` (main version)
     - `Security Scan`
     - `Code Quality`
     - `Integration Tests`

### 3. Codecov Integration (Optional)

1. Visit [codecov.io](https://codecov.io) and sign in with GitHub
2. Add your repository
3. Copy the repository token
4. In GitHub: **Settings** → **Secrets** → **Actions**
5. Add `CODECOV_TOKEN` with your token value

## 🛠️ Local Development

### Install Development Tools

```bash
# Install all development dependencies
pip install -r requirements-dev.txt
```

### Pre-Commit Checks

Run local checks before pushing:

```bash
# Use the provided script
./scripts/run-checks.sh

# Or run individual checks
black .                                    # Format code
isort .                                    # Sort imports
flake8 .                                   # Lint code
mypy app/                                  # Type check
bandit -r app/                             # Security scan
safety check                              # Check dependencies
pytest --cov=app --cov-fail-under=95      # Run tests
```

### Auto-formatting Setup

Configure your editor for automatic formatting:

#### VS Code

```json
{
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

#### PyCharm

1. Install Black plugin
2. Configure external tool for isort
3. Enable format on save

## 📋 Quality Standards

### Code Coverage

- **Minimum**: 95% line coverage
- **Target**: 100% line coverage
- **Branch Coverage**: 90%+ recommended

### Code Style

- **Formatter**: Black (88 character line limit)
- **Import Sorting**: isort (Black-compatible profile)
- **Linting**: flake8 with complexity limit 10
- **Type Hints**: Required for all functions

### Security

- **Dependencies**: Regular vulnerability scanning
- **Code**: Static analysis with bandit
- **Updates**: Automated via Dependabot

## 🔧 Troubleshooting

### Common CI Failures

#### 1. Test Failures

```bash
# Run locally to debug
pytest -v --tb=long
```

#### 2. Code Formatting

```bash
# Fix automatically
black .
isort .
```

#### 3. Type Errors

```bash
# Check specific issues
mypy app/ --show-error-codes
```

#### 4. Security Issues

```bash
# Detailed security report
bandit -r app/ -f json
```

### Pipeline Debugging

1. **Check logs**: Click on failed job in GitHub Actions
2. **Local reproduction**: Use same commands as CI
3. **Environment differences**: Check Python versions
4. **Dependency issues**: Update requirements.txt

## 📈 Metrics and Monitoring

### Coverage Reports

- **Local**: `htmlcov/index.html`
- **CI**: Uploaded to Codecov
- **Trends**: Track coverage over time

### Performance

- **Test Duration**: Monitor in CI logs
- **Build Time**: Optimize for faster feedback

### Security

- **Vulnerability Alerts**: GitHub Security tab
- **Dependency Updates**: Dependabot PRs
- **Security Reports**: Stored as artifacts

## 🔄 Workflow Examples

### Feature Development

```bash
# 1. Create feature branch
git checkout -b feature/new-endpoint

# 2. Make changes
# ... code changes ...

# 3. Run local checks
./scripts/run-checks.sh

# 4. Commit and push
git add .
git commit -m "Add new endpoint with tests"
git push origin feature/new-endpoint

# 5. Create PR - CI runs automatically
# 6. Review and merge after CI passes
```

### Hotfix Process

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Fix issue with tests
# ... fix code ...

# 3. Verify locally
./scripts/run-checks.sh

# 4. Fast-track PR with CI validation
git push origin hotfix/critical-bug
# Create PR with "hotfix" label
```

## 🏷️ Release Process

1. **Version Bump**: Update version in relevant files
2. **Changelog**: Document changes
3. **Tag Release**: Create Git tag
4. **Deploy**: Automated deployment (if configured)

## 📞 Support

For CI/CD issues:

1. Check this documentation
2. Review GitHub Actions logs
3. Test locally with same commands
4. Check repository settings and permissions

---

**The CI/CD pipeline ensures code quality and prevents bugs from reaching production!** 🚀
