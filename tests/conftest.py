"""
Pytest configuration file for test fixtures and shared test setup
"""

import pytest
import sys
import os

# Add the source directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../PythonFlashCards'))


@pytest.fixture
def sample_deck():
    """Fixture providing a sample deck for testing"""
    return {
        "What is Python?": "A high-level programming language",
        "What is a list?": "An ordered, mutable collection",
        "What is a tuple?": "An ordered, immutable collection"
    }


@pytest.fixture
def long_text():
    """Fixture providing long text for testing wrapping"""
    return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Lorem ipsum dolor sit amet"


@pytest.fixture
def multiline_text():
    """Fixture providing multiline text for testing"""
    return """First line of text\nSecond line of text\nThird line of text\nFourth line with some extra content"""


@pytest.fixture
def special_chars_text():
    """Fixture providing text with special characters"""
    return "Special chars: @#$%^&*()_+-=[]{}|;':\",./<>?"
