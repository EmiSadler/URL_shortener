# URL Shortener - Testing Guide

This document provides comprehensive testing instructions for the URL Shortener project, including setup, execution, and coverage reporting.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Test Setup](#test-setup)
- [Running Tests](#running-tests)
- [Coverage Reports](#coverage-reports)
- [Test Structure](#test-structure)
- [Writing New Tests](#writing-new-tests)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

Before running tests, ensure you have the following installed:

```bash
# Python 3.8+ required
python --version

# Install dependencies
pip install -r requirements.txt

# Verify pytest installation
pytest --version
```

## ⚙️ Test Setup

### Initial Setup

1. **Clone the repository** (if not already done):

   ```bash
   git clone <repository-url>
   cd URL_shortener
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Verify project structure**:
   ```
   URL_shortener/
   ├── app/
   │   ├── __init__.py
   │   ├── config.py
   │   ├── db.py
   │   ├── error_handlers.py
   │   ├── models.py
   │   ├── routes.py
   │   ├── shortener.py
   │   └── validators.py
   ├── tests/
   │   ├── __init__.py
   │   ├── conftest.py
   │   ├── test_*.py files
   │   └── TEST_README.md (this file)
   ├── main.py
   ├── requirements.txt
   └── README.md
   ```

## 🏃 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run all tests with verbose output
pytest -v

# Run tests with short summary
pytest -q
```

### Running Specific Tests

```bash
# Run tests for a specific module
pytest tests/test_routes.py
pytest tests/test_validators.py
pytest tests/test_models.py

# Run a specific test class
pytest tests/test_routes.py::TestShortenEndpoint

# Run a specific test method
pytest tests/test_routes.py::TestShortenEndpoint::test_shorten_success

# Run tests matching a pattern
pytest -k "test_shorten"
pytest -k "not integration"
```

### Test Output Options

```bash
# Show local variables on failures
pytest -l

# Show captured output (print statements)
pytest -s

# Stop after first failure
pytest -x

# Stop after N failures
pytest --maxfail=3

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto
```

## 📊 Coverage Reports

### Basic Coverage

```bash
# Run tests with coverage (terminal output)
pytest --cov=app tests/

# Show missing lines in terminal
pytest --cov=app --cov-report=term-missing tests/
```

### HTML Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html tests/

# View the report
open htmlcov/index.html  # macOS
# or
xdg-open htmlcov/index.html  # Linux
# or navigate to htmlcov/index.html in your browser
```

### Coverage Options

```bash
# Both terminal and HTML reports
pytest --cov=app --cov-report=term-missing --cov-report=html tests/

# XML report (for CI/CD)
pytest --cov=app --cov-report=xml tests/

# Fail if coverage below threshold
pytest --cov=app --cov-fail-under=90 tests/
```

### Coverage Configuration

Create a `.coveragerc` file for advanced coverage configuration:

```ini
[run]
source = app
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 📁 Test Structure

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_db.py              # Database functionality tests
├── test_error_handlers.py  # Error handling tests
├── test_models.py          # Data model tests
├── test_routes.py          # API endpoint tests
├── test_shortener.py       # URL shortening algorithm tests
└── test_validators.py      # Input validation tests
```

### Test Categories

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test component interactions
- **API Tests**: Test HTTP endpoints and responses
- **Database Tests**: Test data persistence and retrieval

### Test Fixtures (conftest.py)

Common test utilities and fixtures are defined in `conftest.py`:

```python
# Example fixtures available in all tests
@pytest.fixture
def temp_db():
    """Temporary database for testing"""
    # Implementation...

@pytest.fixture
def test_app():
    """Flask test application"""
    # Implementation...
```

## ✍️ Writing New Tests

### Test Naming Conventions

- Test files: `test_<module_name>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<description>`

### Example Test Structure

```python
import pytest
from app.module import function_to_test

class TestFunctionName:
    """Test the function_to_test function"""

    def test_function_success_case(self):
        """Test successful operation"""
        # Arrange
        input_data = "test_input"
        expected = "expected_output"

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result == expected

    def test_function_edge_case(self):
        """Test edge case handling"""
        # Test implementation...

    def test_function_error_case(self):
        """Test error handling"""
        with pytest.raises(ValueError):
            function_to_test(invalid_input)
```

### Mock and Patch Examples

```python
from unittest.mock import patch, MagicMock

class TestWithMocking:
    @patch('app.db.get_db_connection')
    def test_database_operation(self, mock_db):
        """Test with mocked database"""
        mock_db.return_value = MagicMock()
        # Test implementation...
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**

   ```bash
   # Add project root to Python path
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   pytest
   ```

2. **Database Conflicts**

   ```bash
   # Remove test database files
   rm -f url_shortener.db
   rm -f test_*.db
   ```

3. **Cache Issues**

   ```bash
   # Clear pytest cache
   pytest --cache-clear

   # Remove __pycache__ directories
   find . -type d -name "__pycache__" -exec rm -rf {} +
   ```

### Test Data Cleanup

Tests use temporary databases and fixtures to avoid data conflicts. If you encounter issues:

```python
# Each test gets a fresh database
@pytest.fixture
def temp_db():
    # Creates isolated test database
```

### Debugging Tests

```bash
# Run with Python debugger
pytest --pdb

# Drop into debugger on first failure
pytest --pdb -x

# Show full traceback
pytest --tb=long
```

## 📈 Current Test Coverage

The project maintains **100% test coverage** across all modules:

- ✅ `app/db.py` - 100% coverage
- ✅ `app/error_handlers.py` - 100% coverage
- ✅ `app/models.py` - 100% coverage
- ✅ `app/routes.py` - 100% coverage
- ✅ `app/shortener.py` - 100% coverage
- ✅ `app/validators.py` - 100% coverage

### Coverage Goals

- Maintain **≥95%** line coverage
- Maintain **≥90%** branch coverage
- All critical paths must be tested
- Error handling must be thoroughly tested

## 📞 Need Help?

If you encounter issues:

1. Check this README for common solutions
2. Review test output and error messages
3. Ensure all dependencies are installed
4. Verify Python version compatibility
5. Check that the database is accessible

---

**Happy Testing!** 🎉
