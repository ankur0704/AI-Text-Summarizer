# Testing Guide

This document explains how to set up and run the test suite for the AI Text Summarizer project.

## Quick Start

### 1. Activate your virtual environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### 2. Install test dependencies

```bash
pip install -r requirements.txt
```

This installs `pytest` and all other project dependencies.

### 3. Run the tests

```bash
pytest -q
```

Expected output (all tests should pass):
```
.......                                                                                           [100%]
7 passed in 0.02s
```

## Test Structure

The test suite is organized as follows:

```
tests/
├── conftest.py                      # pytest configuration (sets sys.path)
├── test_summarizer_chunking.py      # Tests for text chunking logic
└── test_summarizer_api.py           # Tests for API mocking and error handling
```

## What Each Test File Tests

### `test_summarizer_chunking.py` (3 tests)
Tests the `chunk_text()` function from `summarizer.py`:
- **`test_chunk_text_basic()`** — Verifies text is split into chunks at sentence boundaries
- **`test_chunk_text_empty()`** — Verifies empty input returns an empty list
- **`test_chunk_text_nonstring()`** — Verifies `TypeError` is raised for non-string input

### `test_summarizer_api.py` (4 tests)
Tests API interaction and error handling using a mock model:
- **`test_summarize_chunk_calls_model()`** — Verifies the function calls the mocked model and returns text
- **`test_summarize_chunk_handles_error()`** — Verifies API errors are wrapped into `SummarizationError`
- **`test_consolidate_and_summarize_success()`** — Verifies consolidation works with a mock model
- **`test_consolidate_and_summarize_error()`** — Verifies consolidation errors are handled gracefully

## Running Tests with More Details

### Show verbose output
```bash
pytest -v
```

Example output:
```
tests/test_summarizer_chunking.py::test_chunk_text_basic PASSED
tests/test_summarizer_chunking.py::test_chunk_text_empty PASSED
tests/test_summarizer_chunking.py::test_chunk_text_nonstring PASSED
tests/test_summarizer_api.py::test_summarize_chunk_calls_model PASSED
tests/test_summarizer_api.py::test_summarize_chunk_handles_error PASSED
tests/test_summarizer_api.py::test_consolidate_and_summarize_success PASSED
tests/test_summarizer_api.py::test_consolidate_and_summarize_error PASSED
```

### Run a specific test file
```bash
pytest tests/test_summarizer_chunking.py -v
```

### Run a specific test function
```bash
pytest tests/test_summarizer_api.py::test_summarize_chunk_calls_model -v
```

### Run with coverage report
```bash
pytest --cov=summarizer --cov-report=term-missing
```

This shows which lines of `summarizer.py` are covered by tests.

## How Mocking Works

The tests use a `DummyModel` class to mock the Gemini API:

```python
class DummyModel:
    def __init__(self, response_text="ok", raise_exc=False):
        self.response_text = response_text
        self.raise_exc = raise_exc

    def generate_content(self, prompt: str):
        if self.raise_exc:
            raise RuntimeError("api error")
        return SimpleNamespace(text=self.response_text)
```

This allows us to:
- Test without making actual API calls
- Control the response (success or failure)
- Run tests offline and very fast (~0.02s)
- Avoid rate limits and API costs

## Troubleshooting

### "ModuleNotFoundError: No module named 'summarizer'"
**Solution:** Ensure `tests/conftest.py` exists and contains the sys.path configuration. The conftest file should automatically add the project root to Python's import path.

**Or manually set PYTHONPATH before running pytest:**
```powershell
$env:PYTHONPATH = '.'; pytest -q
```

### "pytest: command not found"
**Solution:** Install pytest via requirements.txt:
```bash
pip install -r requirements.txt
```

### Tests fail unexpectedly
**Solution:** Ensure you're in the project root directory:
```bash
cd c:\Users\VENU SONAVANE\Desktop\text-summarizer
```

And that your virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
```

## CI/CD Integration

To run tests in a CI/CD pipeline (e.g., GitHub Actions), use:
```bash
pytest --tb=short -q
```

This provides concise output suitable for logs.

## Adding New Tests

To add a new test:
1. Create a new function in an existing test file or a new file (e.g., `test_new_feature.py`)
2. Name the function `test_*` so pytest automatically discovers it
3. Use `assert` statements to validate behavior
4. For mocking, use the `DummyModel` class (see `test_summarizer_api.py` for examples)

Example:
```python
def test_my_new_feature():
    result = some_function("input")
    assert result == "expected_output"
```

Then run:
```bash
pytest tests/test_new_feature.py -v
```

## Further Reading

- [pytest documentation](https://docs.pytest.org/)
- [unittest.mock documentation](https://docs.python.org/3/library/unittest.mock.html) (for advanced mocking)
- [Testing best practices](https://docs.python-guide.org/writing/tests/)
