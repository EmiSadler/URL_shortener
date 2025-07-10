#!/bin/bash

# Local CI/CD simulation script
# Run this before pushing to ensure CI will pass

set -e  # Exit on any error

echo "🚀 Running local CI/CD checks..."
echo

# Check if development dependencies are installed
if ! command -v black &> /dev/null; then
    echo "❌ Development dependencies not found. Please run:"
    echo "   pip install -r requirements-dev.txt"
    exit 1
fi

echo "1️⃣ Code Formatting (Black)..."
black --check --diff . || (echo "❌ Code formatting issues found. Run 'black .' to fix." && exit 1)
echo "✅ Code formatting OK"
echo

echo "2️⃣ Import Sorting (isort)..."
isort --check-only --diff . || (echo "❌ Import sorting issues found. Run 'isort .' to fix." && exit 1)
echo "✅ Import sorting OK"
echo

echo "3️⃣ Linting (flake8)..."
flake8 . || (echo "❌ Linting issues found." && exit 1)
echo "✅ Linting OK"
echo

echo "4️⃣ Type Checking (mypy)..."
mypy app/ --ignore-missing-imports || (echo "❌ Type checking issues found." && exit 1)
echo "✅ Type checking OK"
echo

echo "5️⃣ Security Scanning (bandit)..."
bandit -r app/ -q || (echo "❌ Security issues found." && exit 1)
echo "✅ Security scan OK"
echo

echo "6️⃣ Dependency Security (safety)..."
safety check --json > /dev/null || (echo "❌ Vulnerable dependencies found." && exit 1)
echo "✅ Dependencies secure"
echo

echo "7️⃣ Running Tests..."
pytest --cov=app --cov-report=term-missing --cov-fail-under=95 || (echo "❌ Tests failed." && exit 1)
echo "✅ All tests passed"
echo

echo "🎉 All checks passed! Your code is ready to push."
echo
echo "Next steps:"
echo "  git add ."
echo "  git commit -m 'Your commit message'"
echo "  git push origin your-branch"
