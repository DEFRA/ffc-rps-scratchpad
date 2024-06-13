import unittest
from actionCodes import ActionCodes, all_sfi2024_codes


class TestExtraction(unittest.TestCase):

    def test_extract_from_only_codes(self):
        """Test that all the codes are successfully read from a list containing only codes."""

        codes = ActionCodes()
        codes.add_category('SFI2024', all_sfi2024_codes)

        (res, remainder) = codes.extract_code_from_string("AHW1, AHW3, AHW6, AHW7, AHW8, AHW9, AHW10, AHW11, AHW12")
        assert res == ['AHW1', 'AHW3', 'AHW6', 'AHW7', 'AHW8', 'AHW9', 'AHW10', 'AHW11', 'AHW12']
        assert remainder == []

    def test_extract_from_codes_and_other(self):
        """Test that all the codes are successfully read from a list containing only codes."""

        codes = ActionCodes()
        codes.add_category('SFI2024', all_sfi2024_codes)

        (res, remainder) = codes.extract_code_from_string("AHW1, AHW3, AHW6, AHW7, AHW8, AHW9, AHW10, AHW11, AHW12, notacode")
        assert res == ['AHW1', 'AHW3', 'AHW6', 'AHW7', 'AHW8', 'AHW9', 'AHW10', 'AHW11', 'AHW12']
        assert remainder == ['notacode']


if __name__ == "__main__":
    unittest.main()