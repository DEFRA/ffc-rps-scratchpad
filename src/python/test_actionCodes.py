import unittest
from actionCodes import ActionCodes, all_sfi2024_codes, ActionCodeProcessingResult, NULLRESULT


class TestExtraction(unittest.TestCase):

    def test_compile_all_known_codes(self):
        codes = ActionCodes()
        codes.add_category('cat1', ["cat1code1", "cat1code2"])
        codes.add_category('two', ["cat2code1", "cat2code2"])
        result = codes._all_known_codes
        expected = ["CAT1CODE1", "CAT1CODE2", "CAT2CODE1", "CAT2CODE2"]
        self.assertCountEqual(result, expected)

    def test_split_instr_with_commas(self):
        codes = ActionCodes()
        items = codes.split_instr("list, with, commas")
        assert items == ["list", "with", "commas"]

    def test_check_for_none(self):
        codes = ActionCodes()
        result1 = codes.check_for_none("no codes")
        result2 = codes.check_for_none("None")
        result3 = codes.check_for_none("some, codes")
        assert result1 is None
        assert result2 is None
        assert result3 == "some, codes"

    def test_extract_from_only_codes(self):
        """Test that all the codes are successfully read from a list containing only codes."""

        codes = ActionCodes()
        codes.add_category('cat1', ["cat1code1", "cat1code2"])
        codes.add_category('two', ["cat2code1", "cat2code2"])

        extracted_codes = codes.extract_codes_from_items(["cat1code1", "cat1code2"])
        result = extracted_codes.codes
        expected = ["CAT1CODE1", "CAT1CODE2"]
        print(result)
        self.assertCountEqual(result, expected)
        assert extracted_codes.remnant == []

    def test_extract_from_codes_and_other(self):
        """Test that all the codes are successfully read from a list containing only codes."""

        codes = ActionCodes()
        codes.add_category('cat1', ["cat1code1", "cat1code2"])
        codes.add_category('two', ["cat2code1", "cat2code2"])

        extracted_codes = codes.extract_codes_from_items(["cat1code1", "cat1code2", "notacode"])
        result = extracted_codes.codes
        expected = ["CAT1CODE1", "CAT1CODE2"]
        print(result)
        self.assertCountEqual(result, expected)
        assert extracted_codes.remnant == ["notacode"]

    def test_match_category(self):
        """Test that we can expand a substring into a known category of codes and collect them all up."""

        codes = ActionCodes()
        codes.add_category('cat1', ["cat1code1", "cat1code2"])
        codes.add_category('two', ["cat2code1", "cat2code2"])

        input_items = ["All CAT1 items", "cat2code1"]

        result = codes.match_all_category(input_items, expandable_string="All CAT1 items", category="cat1")
        expected_codes = ["CAT1CODE1", "CAT1CODE2"]
        expected_remnant = ["cat2code1"]
        self.assertCountEqual(result.codes, expected_codes)
        self.assertCountEqual(result.remnant, expected_remnant)

    def test_process_string_all_discrete(self):
        """Test the whole process of extracting and expanding from string."""

        codes = ActionCodes()
        codes.add_category('cat1', ["cat1code1", "cat1code2"])
        codes.add_category('two', ["cat2code1", "cat2code2"])

        found_codes = codes.process_string("cat1code1, cat2code2")
        result = found_codes
        expected = ["CAT1CODE1", "CAT2CODE2"]
        self.assertCountEqual(result, expected)

    def test_process_string_mixture(self):
        """Test the whole process of extracting and expanding from string."""

        codes = ActionCodes()
        codes.add_category('cat1', ["cat1code1", "cat1code2"])
        codes.add_category('two', ["cat2code1", "cat2code2"])

        found_codes = codes.process_string("All cat1 items, cat2code2")
        result = found_codes
        expected = ["CAT1CODE1", "CAT1CODE2", "CAT2CODE2"]
        self.assertCountEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
