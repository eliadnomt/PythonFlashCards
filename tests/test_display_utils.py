"""
Unit tests for display_utils.py using pytest
"""

import pytest
import sys
import os

# Add the parent directory to the path to import display_utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

from tests.conftest import multiline_text, long_text
from display_utils import grid_builder, out_put_builder, card_displayer, display_deck


class TestGridBuilder:
    """Test cases for the grid_builder function"""
    
    def test_simple_string_under_rowlen(self):
        """Test a simple string that is shorter than rowlen"""
        result = grid_builder("Hello World", rowlen=80)
        assert result == ["Hello World"]
    
    def test_string_exactly_rowlen(self):
        """Test a string that is exactly rowlen characters"""
        test_str = "x" * 80
        result = grid_builder(test_str, rowlen=80)
        assert result == [test_str]
    
    def test_string_with_word_break_at_boundary(self):
        """Test string where word break happens at rowlen boundary"""
        # Create a string where position 79 is alpha and position 80 is not a space
        test_str = "a" * 79 + "word"
        result = grid_builder(test_str, rowlen=80)
        assert len(result) == 2
        assert result[0] == "a" * 79 + "w-"  # Takes one char from 'word' and adds hyphen
        assert result[1] == "ord"
    
    def test_string_with_natural_break(self):
        """Test string with natural word break (space after rowlen)"""
        test_str = "a" * 79 + " word"
        result = grid_builder(test_str, rowlen=80)
        assert len(result) == 2
        assert result[0] == "a" * 79 + " "
        assert result[1] == "word"  # Should be stripped
    
    def test_multiline_input(self, multiline_text):
        """Test input with multiple lines separated by newlines"""
        result = grid_builder(multiline_text, rowlen=80)
        expected = multiline_text.split('\n')
        assert result == expected
    
    def test_multiline_with_long_lines(self, long_text):
        """Test multiline input where some lines exceed rowlen"""
        line1 = "short line"
        test_str = f"{line1}\n{long_text}"
        result = grid_builder(test_str, rowlen=80)
        expected_pt1 = long_text[:80] + "-"
        expected_pt2 = long_text[80:]
        assert len(result) == 3
        assert result[0] == line1
        assert result[1] == expected_pt1  # Hyphen is added
        assert result[2] == expected_pt2
    
    def test_empty_string(self):
        """Test empty string input"""
        result = grid_builder("", rowlen=80)
        assert result == [""]
    
    def test_only_newlines(self):
        """Test string with only newlines"""
        result = grid_builder("\n\n\n", rowlen=80)
        assert result == ["", "", "", ""]
    
    def test_small_rowlen(self):
        """Test with very small rowlen"""
        test_str = "Hello World"
        result = grid_builder(test_str, rowlen=5)
        assert len(result) == 3
        assert result[0] == "Hello"
        assert result[1] == "Worl-"  # Should add hyphen
        assert result[2] == "d"
    
    def test_leading_whitespace_stripped(self, long_text):
        """Test that leading whitespace is stripped from wrapped lines"""
        test_str = long_text[:80] + "   " + long_text[80:]
        result = grid_builder(test_str, rowlen=80)
        assert result[1] == long_text[80:]  # Leading spaces should be stripped


class TestOutputBuilder:
    """Test cases for the out_put_builder function"""
    
    def test_single_line_grid(self):
        """Test output with single line grid"""
        grid = ["Hello"]
        result = out_put_builder(grid)
        expected_lines = [
            "",
            "_________",
            "|       |",
            "| Hello |",
            "|_______|"
        ]
        assert result == "\n".join(expected_lines) + "\n"
    
    def test_multiple_lines_same_length(self):
        """Test output with multiple lines of same length"""
        grid = ["Hello", "World"]
        result = out_put_builder(grid)
        expected_lines = [
            "",
            "_________",
            "|       |",
            "| Hello |",
            "| World |",
            "|_______|"
        ]
        assert result == "\n".join(expected_lines) + "\n"
    
    def test_multiple_lines_different_lengths(self, multiline_text):
        """Test output with lines of different lengths"""
        multiline_elements = multiline_text.split('\n')
        result = out_put_builder(multiline_elements)
        lines = result.strip().split("\n")

        # Check that all lines have the same width
        line_lengths = [len(line) for line in lines[1:]]  # Skip first empty line
        assert all(length == line_lengths[-1] for length in line_lengths)

    def test_multiple_lines_padding(self):
        """Test output with lines of different lengths"""
        grid = ["Short", "A longer line", "Mid"]
        result = out_put_builder(grid)

        # Check content lines are padded correctly (note: only one space before closing |)
        assert "| Short         |" in result
        assert "| A longer line |" in result
        assert "| Mid           |" in result
    
    def test_empty_grid(self):
        """Test output with empty grid"""
        grid = [""]
        result = out_put_builder(grid)
        expected_lines = [
            "",
            "____",
            "|  |",
            "|  |",
            "|__|"
        ]
        assert result == "\n".join(expected_lines) + "\n"
    
    def test_very_long_line(self):
        """Test output with very long line"""
        long_text = "x" * 100
        grid = [long_text]
        result = out_put_builder(grid)
        lines = result.split("\n")
        
        # Check structure (first line is empty, then top border)
        assert lines[0] == ""  # First line is empty
        assert lines[1].startswith("__")  # Top border
        assert lines[1].endswith("__")
        assert lines[-2].startswith("|_")  # Bottom border (last line is empty)
        assert lines[-2].endswith("_|")


class TestCardDisplayer:
    """Test cases for the card_displayer function"""
    
    def test_simple_card(self):
        """Test displaying a simple card"""
        result = card_displayer("Hello World")
        
        # Check that it contains the boxed text
        assert "Hello World" in result
        assert "|" in result
        assert "_" in result
    
    def test_multiline_card(self, multiline_text):
        """Test displaying a multiline card"""
        result = card_displayer(multiline_text)
        expected = multiline_text.split('\n')
        # Check all lines are present
        for item in expected:
            assert item in result

    def test_long_card_wrapping(self):
        """Test card with text that needs wrapping"""
        long_text = "x" * 100
        result = card_displayer(long_text)
        
        # Should be wrapped into multiple lines
        lines = result.strip().split("\n")
        # At least 2 content lines plus borders
        assert len(lines) >= 5
    
    def test_empty_card(self):
        """Test displaying an empty card"""
        result = card_displayer("")
        
        # Should still create a box
        assert "|" in result
        assert "_" in result


class TestDisplayDeck:
    """Test cases for the display_deck function"""
    
    def test_empty_deck(self):
        """Test displaying an empty deck"""
        result = display_deck({})
        
        # Should display headers but no cards
        assert "Front" in result
        assert "Back" in result
        assert "V" in result  # Arrow indicator
    
    def test_single_card_deck(self):
        """Test displaying a deck with one card"""
        deck = {"Question": "Answer"}
        result = display_deck(deck)
        
        # Check headers
        assert "Front" in result
        assert "Back" in result
        
        # Check card content
        assert "Question" in result
        assert "Answer" in result
        
        # Check multiple arrow indicators (one for header, one for card)
        assert result.count("V") >= 2
    
    def test_multiple_cards_deck(self):
        """Test displaying a deck with multiple cards"""
        deck = {
            "Q1": "A1",
            "Question 2": "Answer 2",
            "Third Question": "Third Answer"
        }
        result = display_deck(deck)
        
        # Check all questions and answers are present
        for key, value in deck.items():
            assert key in result
            assert value in result
        
        # Check we have arrow indicators for header + each card
        assert result.count("V") >= 4
    
    def test_deck_with_long_content(self):
        """Test displaying deck with long questions/answers"""
        long_question = "This is a very long question " * 5
        long_answer = "This is a very long answer " * 5
        deck = {long_question: long_answer}
        
        result = display_deck(deck)
        
        # Content should be wrapped but still present
        assert "This is a very long question" in result
        assert "This is a very long answer" in result
    
    def test_deck_with_multiline_content(self):
        """Test displaying deck with multiline questions/answers"""
        multiline_q = "Line 1\nLine 2\nLine 3"
        multiline_a = "Answer 1\nAnswer 2\nAnswer 3"
        deck = {multiline_q: multiline_a}
        
        result = display_deck(deck)
        
        # All lines should be present
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result
        assert "Answer 1" in result
        assert "Answer 2" in result
        assert "Answer 3" in result
    
    def test_deck_with_special_characters(self):
        """Test displaying deck with special characters"""
        deck = {
            "What is 2+2?": "4",
            "Define π": "3.14159...",
            "What is O(n²)?": "Quadratic time complexity"
        }
        
        result = display_deck(deck)
        
        # Check special characters are preserved
        assert "2+2?" in result
        assert "π" in result
        assert "O(n²)" in result


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_grid_builder_with_none_rowlen(self):
        """Test grid_builder with very large rowlen"""
        test_str = "Hello World"
        result = grid_builder(test_str, rowlen=1000)
        assert result == ["Hello World"]
    
    def test_output_builder_duplicate_items(self):
        """Test out_put_builder with duplicate items in grid"""
        grid = ["Same", "Same", "Different", "Same"]
        result = out_put_builder(grid)
        
        # Should handle duplicates correctly
        lines = result.strip().split("\n")
        content_lines = [line for line in lines if "Same" in line]
        assert len(content_lines) == 3
    
    def test_unicode_characters(self):
        """Test handling of unicode characters"""
        unicode_text = "Hello 世界 🌍"
        result = card_displayer(unicode_text)
        
        assert "Hello" in result
        assert "世界" in result
        assert "🌍" in result
    
    def test_tab_characters(self):
        """Test handling of tab characters"""
        tab_text = "Column1\tColumn2\tColumn3"
        result = card_displayer(tab_text)
        
        # Tabs should be preserved or handled appropriately
        assert "Column1" in result
        assert "Column2" in result
        assert "Column3" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
