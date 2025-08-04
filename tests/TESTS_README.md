# Display Utils Test Suite

This directory contains comprehensive unit tests for the `display_utils.py` module from the PythonFlashCards project.

## Structure

- `test_display_utils.py` - Main test file containing all unit tests
- `conftest.py` - Pytest configuration and shared fixtures
- `requirements.txt` - Testing dependencies

## Running the Tests

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
# Run tests with verbose output
pytest test_display_utils.py -v

# Run with coverage report
pytest test_display_utils.py --cov=display_utils --cov-report=html

# Run specific test class
pytest test_display_utils.py::TestGridBuilder -v

# Run specific test method
pytest test_display_utils.py::TestGridBuilder::test_simple_string_under_rowlen -v
```

## Test Coverage

The test suite covers the following functions from `display_utils.py`:

### 1. `grid_builder(cardstr, rowlen=80)`
Tests include:
- Simple strings under row length
- Strings exactly at row length
- Long strings requiring wrapping
- Word boundary handling with hyphenation
- Multiline input handling
- Empty string and edge cases
- Leading whitespace stripping

### 2. `out_put_builder(grid)`
Tests include:
- Single line grids
- Multiple lines with same/different lengths
- Empty grids
- Very long lines
- Proper box formatting and padding

### 3. `card_displayer(card)`
Tests include:
- Simple card display
- Multiline cards
- Long text wrapping
- Empty cards
- Integration of grid_builder and out_put_builder

### 4. `display_deck(deck_dict)`
Tests include:
- Empty deck display
- Single and multiple card decks
- Long content handling
- Multiline content
- Special characters
- Proper formatting with arrows

## Edge Cases Covered

- Unicode character support
- Tab character handling
- Duplicate items in grids
- Very small/large row lengths
- Special characters in text

## Fixtures

The `conftest.py` file provides several fixtures:
- `sample_deck` - A sample flashcard deck
- `long_text` - Long text for wrapping tests
- `multiline_text` - Multiline text samples
- `special_chars_text` - Text with special characters

## Notes

- The tests assume the source code is located at `../../inputs/PythonFlashCards/`
- All tests are independent and can be run in any order
- The test suite uses pytest's class-based organization for clarity

## Future Improvements

While the current test suite is comprehensive, potential improvements could include:
1. Property-based testing with hypothesis
2. Performance benchmarking
3. Testing with different terminal encodings
4. Integration tests with the full flashcard application
