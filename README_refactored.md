# Flashcards Application - Refactored Version

## Overview
This is a refactored version of Flashcards 0.5, with the code organized into separate modules for better maintainability and reusability.

## File Structure

### Main Entry Point
- `main.py` - Main application file that runs the program

### Core Modules
- `import_utils.py` - Functions for importing and converting flashcard files (Quizlet format)
- `deck_utils.py` - Utilities for managing flashcard decks
- `display_utils.py` - Functions for formatting and displaying flashcards with box graphics
- `constants.py` - Application constants and menu strings

### Quiz Modules
- `quiz_multiple_choice.py` - Multiple choice quiz functionality
- `quiz_write_answer.py` - Write-in answer quiz functionality
- `quiz_self_report.py` - Self-report quiz functionality

### Game Module
- `memory_game.py` - Memory matching game functionality

### Package Files
- `__init__.py` - Package initialization file
- `requirements.txt` - Python dependencies (currently none, uses standard library only)

## How to Run
```bash
python main.py
```

## Features Preserved
- All original functionality from Flashcards_0.5.py is maintained
- Import Quizlet flashcard exports
- Create, view, and manage flashcard decks
- Three quiz types: Multiple choice, Write answer, Self-report
- Memory matching game
- Deck switching and persistence

## Improvements
- **Modular Structure**: Each function is now in its own logical module
- **Better Organization**: Related functions are grouped together
- **Easier Maintenance**: Changes to one feature don't affect others
- **Import Flexibility**: Individual modules can be imported and reused
- **Clear Separation of Concerns**: Display, quiz logic, games, and utilities are separated

## Usage Example
To use individual modules in other projects:
```python
from display_utils import card_displayer
from quiz_multiple_choice import multiple_choice_quiz

# Use the functions independently
display = card_displayer("Sample Card")
print(display)
```

## Notes
- The program expects JSON files for flashcard decks in the same directory
- Text files can be imported and converted to JSON format
- All original bugs fixes from version 0.5 are preserved
