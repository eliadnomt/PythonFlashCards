# Display Utils Test Suite Summary

## Overview
This test suite provides comprehensive unit testing for the `display_utils.py` module from the PythonFlashCards project. The tests are written using pytest and achieve 100% code coverage.

## Test Files

1. **`test_display_utils.py`** (30 tests)
   - Core functionality tests for all four functions
   - Basic edge cases and typical usage scenarios
   - Well-organized into test classes by function

2. **`test_display_utils_extended.py`** (21 tests)
   - Additional edge cases and boundary conditions
   - Performance tests with large datasets
   - Error handling and exceptional cases
   - Unicode and special character support

## Test Statistics
- **Total Tests**: 51
- **Code Coverage**: 100%
- **Functions Tested**: 4
  - `grid_builder()`
  - `out_put_builder()`
  - `card_displayer()`
  - `display_deck()`

## Key Test Categories

### 1. Grid Builder Tests (23 tests)
- Text wrapping and line breaking
- Hyphenation at word boundaries
- Multiline input handling
- Edge cases (empty strings, very small rowlen, etc.)
- Whitespace handling

### 2. Output Builder Tests (10 tests)
- Box formatting with proper borders
- Padding and alignment
- Handling of different line lengths
- Unicode support

### 3. Card Displayer Tests (6 tests)
- Integration of grid_builder and out_put_builder
- Long text wrapping
- Empty and multiline cards

### 4. Display Deck Tests (8 tests)
- Multiple card display
- Empty decks
- Special characters
- Large deck performance

### 5. Error Handling Tests (4 tests)
- None values
- Zero/negative parameters
- Type errors

## Running the Tests

```bash
# Run all tests
pytest test_display_utils.py test_display_utils_extended.py -v

# Run with coverage
pytest test_display_utils.py test_display_utils_extended.py --cov=display_utils

# Run specific test file
pytest test_display_utils.py -v

# Use the test runner
python run_tests.py
```
