"""
Extended unit tests for display_utils.py - additional edge cases and scenarios
"""

import pytest
import sys
import os

# Add the parent directory to the path to import display_utils
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../inputs/PythonFlashCards'))

from display_utils import grid_builder, out_put_builder, card_displayer, display_deck


class TestGridBuilderExtended:
    """Extended test cases for grid_builder function"""
    
    def test_consecutive_spaces(self):
        """Test handling of consecutive spaces"""
        test_str = "Hello    World    Test"
        result = grid_builder(test_str, rowlen=80)
        assert result == ["Hello    World    Test"]
    
    def test_newline_at_end(self):
        """Test string ending with newline"""
        test_str = "Hello\nWorld\n"
        result = grid_builder(test_str, rowlen=80)
        assert result == ["Hello", "World", ""]
    
    def test_mixed_whitespace(self):
        """Test mixed tabs and spaces"""
        test_str = "Hello\t\tWorld  \tTest"
        result = grid_builder(test_str, rowlen=80)
        assert "Hello" in result[0]
        assert "World" in result[0]
        assert "Test" in result[0]
    
    def test_very_small_rowlen_with_spaces(self):
        """Test very small rowlen with spaces in text"""
        test_str = "Hello World Test"
        result = grid_builder(test_str, rowlen=6)
        assert len(result) >= 3
    
    def test_single_very_long_word(self):
        """Test a single word that's much longer than rowlen"""
        test_str = "supercalifragilisticexpialidocious"
        result = grid_builder(test_str, rowlen=10)
        # Each line should be at most 11 chars (10 + hyphen)
        for line in result[:-1]:  # All but last line
            assert len(line) <= 11  # rowlen + hyphen
    
    def test_rowlen_of_1(self):
        """Test with rowlen of 1 - extreme case"""
        test_str = "ABC"
        result = grid_builder(test_str, rowlen=1)
        # With rowlen=1, hyphens are added and behavior may be unusual
        assert len(result) == 4  # Due to the algorithm's behavior
        assert "A" in result[0]
        assert "B" in result[1] 
        assert "C" in result[2] or "C" in result[3]
    
    def test_only_spaces(self):
        """Test string with only spaces"""
        test_str = "     "
        result = grid_builder(test_str, rowlen=80)
        assert result == ["     "]
    
    def test_alternating_alpha_and_space(self):
        """Test alternating letters and spaces at boundary"""
        # Create a string where the boundary falls on different character types
        test_str = "a b c d e f g h i j k l m n o p q r s t u v w x y z " * 3
        result = grid_builder(test_str, rowlen=20)
        for line in result:
            assert len(line) <= 20


class TestOutputBuilderExtended:
    """Extended test cases for out_put_builder function"""
    
    def test_grid_with_only_spaces(self):
        """Test grid containing only space strings"""
        grid = ["   ", " ", "     "]
        result = out_put_builder(grid)
        # Should still create a proper box
        assert "|" in result
        assert "_" in result
        lines = result.split("\n")
        # All lines should have same width
        widths = [len(line) for line in lines if line]
        assert all(w == widths[0] for w in widths)
    
    def test_grid_with_special_unicode(self):
        """Test grid with various unicode characters"""
        grid = ["Hello 🌍", "Привет мир", "你好世界", "مرحبا بالعالم"]
        result = out_put_builder(grid)
        # All original text should be preserved
        for text in grid:
            assert text in result
    
    def test_single_character_grid(self):
        """Test grid with single character strings"""
        grid = ["A", "B", "C"]
        result = out_put_builder(grid)
        assert "| A |" in result
        assert "| B |" in result
        assert "| C |" in result
    
    def test_grid_with_max_length_difference(self):
        """Test grid where one line is much longer than others"""
        grid = ["a", "b" * 100, "c"]
        result = out_put_builder(grid)
        lines = result.split("\n")
        # Check that short lines are padded correctly
        for line in lines:
            if "| a" in line:
                assert line.endswith(" |")
                # Should have 99 spaces after 'a'
                assert line.count(" ") >= 99


class TestIntegrationExtended:
    """Extended integration tests"""
    
    def test_card_displayer_with_rowlen_wrapping(self):
        """Test card_displayer with text that wraps multiple times"""
        long_text = "This is a very long sentence that should wrap multiple times when displayed in the card format. " * 5
        result = card_displayer(long_text)
        # Should create a valid box with wrapped text
        lines = result.split("\n")
        assert len(lines) > 5  # Should have multiple content lines
        
    def test_display_deck_with_empty_values(self):
        """Test deck with empty string values"""
        deck = {
            "Question 1": "",
            "": "Answer 2",
            "Question 3": "Answer 3"
        }
        result = display_deck(deck)
        # Should handle empty strings gracefully
        assert "Question 1" in result
        assert "Answer 2" in result
        assert "Question 3" in result
    
    def test_display_deck_ordering(self, sample_deck):
        """Test that deck maintains some order in display"""
        result = display_deck(sample_deck)
        # Check that all pairs are displayed
        for card_pair in sample_deck:
            for front_or_back in card_pair:
                side_index = card_pair.index(front_or_back)
                assert sample_deck[card_pair][side_index] in result
    
    def test_nested_boxes(self):
        """Test creating a card that contains box-like characters"""
        text_with_boxes = "| This | looks | like | a | table |"
        result = card_displayer(text_with_boxes)
        # Original text should be preserved inside the box
        assert text_with_boxes in result
    
    def test_performance_large_deck(self):
        """Test performance with a large deck"""
        # Create a deck with 100 items
        large_deck = {f"Question {i}": f"Answer {i}" for i in range(100)}
        result = display_deck(large_deck)
        # Should complete without issues and contain all items
        assert len(result) > 0
        assert "Question 0" in result
        assert "Question 99" in result
        assert "Answer 0" in result
        assert "Answer 99" in result


class TestErrorHandling:
    """Test error handling and boundary conditions"""
    
    def test_grid_builder_zero_rowlen(self):
        """Test grid_builder with zero rowlen - should handle gracefully"""
        with pytest.raises(ZeroDivisionError):
            grid_builder("Hello", rowlen=0)
    
    def test_grid_builder_negative_rowlen(self):
        """Test grid_builder with negative rowlen"""
        # Should either raise an error or handle gracefully
        # The current implementation might not handle this well
        result = grid_builder("Hello", rowlen=-5)
        # Just check it doesn't crash - actual behavior may vary
        assert isinstance(result, list)
    
    def test_out_put_builder_with_none(self):
        """Test out_put_builder with None in grid"""
        # This will likely cause an error in the current implementation
        grid = ["Hello", None, "World"]
        with pytest.raises(TypeError):
            out_put_builder(grid)
    
    def test_display_deck_with_none_key(self):
        """Test display_deck with None as a key"""
        deck = {None: "Answer", "Question": "Answer2"}
        with pytest.raises(AttributeError):
            # Will raise AttributeError when trying to call split() on None
            display_deck(deck)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
