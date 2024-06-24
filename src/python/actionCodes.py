from pydantic import BaseModel

all_sfi2024_codes = [
    'WBD2', 'WBD1', 'OFA3', 'AGF1', 'AGF2', 'CHRW1', 'CHRW2', 'CHRW3', 'BND1', 'BND2', 'CAHL4', 'CIGL3', 'BFS1', 'BFS2', 'BFS3', 'BFS4',
    'BFS5', 'BFS6', 'CAHL1', 'CAHL2', 'CAHL3', 'AHW1', 'AHW2', 'AHW3', 'AHW4', 'AHW5', 'AHW6', 'AHW7', 'AHW8', 'AHW9', 'AHW10', 'AHW11',
    'AHW12', 'CIGL1', 'CIGL2', 'CLIG3', 'GRH1', 'GRH7', 'GRH8', 'GRH10', 'GRH11', 'SCR1', 'SCR2', 'HEF1', 'HEF2', 'HEF5', 'HEF6', 'HEF8',
    'CIPM1', 'CIPM2', 'CIPM3', 'CIPM4', 'CMOR1', 'UPL1', 'UPL2', 'UPL3', 'UPL4', 'UPL5', 'UPL6', 'UPL7', 'UPL8', 'UPL9', 'UPL10', 'CNUM1',
    'CNUM2', 'CNUM3', 'OFC1', 'OFC2', 'OFC3', 'OFC4', 'OFC5', 'OFM1', 'OFM2', 'OFM3', 'OFM4', 'OFM5', 'OFM6', 'OFA1', 'OFA6', 'PRF1', 'PRF2',
    'PRF3', 'PRF4', 'SPM2', 'SPM3', 'SPM4', 'SPM5', 'CSAM1', 'CSAM2', 'CSAM3', 'SOH1', 'SOH2', 'SOH3', 'SOH4', 'WBD3', 'WBD4', 'WBD5', 'WBD6',
    'WBD7', 'WBD8', 'WBD9'
    ]

historic_codes = [
    'AB1', 'AB10', 'AB11', 'AB13', 'AB14', 'AB15', 'AB16', 'AB2', 'AB3', 'AB5', 'AB6', 'AB7', 'AB8', 'AB9', 'AHL1', 'AHL2', 'AHL3', 'AHL4',
    'BE1', 'BE2', 'BE4', 'BE5', 'CT1', 'CT2', 'CT3', 'CT4', 'CT5', 'CT7', 'GS1', 'GS10', 'GS11', 'GS12', 'GS13', 'GS14', 'GS2', 'GS3', 'GS4',
    'GS5', 'GS6', 'GS7', 'GS8', 'GS9', 'HRW2', 'HRW3', 'HS2', 'HS3', 'HS4', 'HS5', 'HS6', 'HS7', 'HS9', 'IGL1', 'IGL2', 'IGL3', 'ILG3', 'IPM1',
    'IPM2', 'IPM3', 'IPM4', 'LH1', 'LH2', 'LH3', 'LIG1', 'LIG2', 'MOR1', 'MOR1', 'NUM1', 'NUM2', 'NUM3', 'OP1', 'OP2', 'OP4', 'OP5', 'OR1',
    'OR2', 'OR3', 'OR4', 'OR5', 'OT1', 'OT2', 'OT3', 'OT4', 'OT5', 'OT6', 'SAM1', 'SAM2', 'SAM3', 'SP7', 'SW1', 'SW10', 'SW11', 'SW12', 'SW13',
    'SW15', 'SW16', 'SW17', 'SW18', 'SW2', 'SW3', 'SW4', 'SW5', 'SW6', 'SW7', 'SW8', 'SW9', 'UP1', 'UP2', 'WD10', 'WD11', 'WD12', 'WD2', 'WD3',
    'WD4', 'WD5', 'WD6', 'WT1', 'WT10', 'WT2', 'WT6', 'WT7', 'WT8', 'WT9',
    ]

class ActionCodeProcessingResult(BaseModel):
    """A named tuple of (list of codes identified, list of remaining unidentified items), to be used as a fallthrough."""
    codes: list[str]
    remnant: list[str]

    def hasResults(self):
        return len(self.codes) > 0

    def hasRemainingText(self):
        return len(self.remnant) > 0


NULLRESULT = ActionCodeProcessingResult(codes=[], remnant=[])

class ActionCodes(BaseModel):
    """Holds a list of the codes and allows for it to be added to and removed from.
    Uses this to extract codes from strings and expand general statements into explicit lists."""

    # the keys in this dict represent categories of Action such as SFI2024 or ES.
    # the value is then a list of codes, as strings and in uppercase

    # you can create the class with this dictionary explicitly constructed or you can use the builder methods add_category()
    known_codes: dict = None
    _all_known_codes: list = None

    _runninglist: list[str] = None
    _remnant: list[str] = None

    def model_post_init(self, *args, **kwargs):
        if self.known_codes is None:
            self.known_codes = {}

    def add_category(self, category: str, codes: list[str]):
        """Adds a new named category of Actions."""

        # trusting the user to supply a proper list of codes. Might have to add error handling if this goes wrong a lot
        if category in self.known_codes.keys():
            print(f"Category {category} already exists, ignoring.")
        else:
            self.known_codes[category] = [code.upper() for code in codes]
            # regenerate the main list
            self._all_known_codes = self.all_codes()
            print(f"Added category {category}")
            # print(f"Regenerated all_codes: {self._all_codes}")

    def all_codes(self):
        return list(set([item for k, v in self.known_codes.items() for item in v]))

    def split_instr(self, instr: str):
        if "," in instr:
            items = instr.split(",")
            items = [item.strip() for item in items]
        else:
            items = instr.strip()
        return items

    def check_for_none(self, instr: str):
        """Clears out strings which resolve to an empty list."""
        s = instr.lower()
        if s.startswith('no '):
            return None
        elif s.startswith('none'):
            return None
        elif s == '':
            return None
        else:
            return instr

    def match_all_category(self, items: str, expandable_string: str, category: str):
        extracted_codes = []
        remnant = []

        codes_in_category = self.known_codes.get(category, [])
        for item in items:
            # if the item matches an expandable string we expand it, add it to the list and move on
            if item == expandable_string:
                extracted_codes.extend(codes_in_category)
            elif item.startswith("All ES codes except"):
                string_of_items_to_exclude = item.split("except")[1].strip()
                exclusions = string_of_items_to_exclude.split(" ").strip()
                expanded_codes = list(set(codes_in_category) - set(exclusions))
                extracted_codes.extend(expanded_codes)
            # otherwise we retain the item to pass back out
            else:
                remnant.append(item)
        # now we have iterated all the items we should have a list of expanded codes and the stuff we didn't process

        return ActionCodeProcessingResult(codes=extracted_codes, remnant=remnant)

    def extract_codes_from_items(self, items: list[str]):
        extracted_codes = []
        remnant = []

        for item in items:
            if item.upper() in self._all_known_codes:
                extracted_codes.append(item.upper())
            else:
                remnant.append(item)
        return ActionCodeProcessingResult(codes=extracted_codes, remnant=remnant)

    def process_string(self, instr: str):
        result = self.check_for_none(instr)
        if result is None:
            print(f"No codes extracted, finished")
            return None
        # now split the items and run all the extraction methods against the list, consuming as we go
        items = self.split_instr(instr)
        found_codes = []

        result = self.extract_codes_from_items(items)
        print(f"Extracted codes {result.codes}, remaining {result.remnant}")
        found_codes.extend(result.codes)

        result = self.match_all_category(result.remnant, expandable_string='All ES codes', category='ES')
        print(f"Expanded codes {result.codes}, remaining {result.remnant}")
        found_codes.extend(result.codes)

        return found_codes



    # def process_string(self, instr: str, category: str):
    #     res = self.check_for_none(instr)
    #     if res is None:
    #         print("No codes to extract")
    #         return None
    #     # now we split up the string by commas and consume items either by matching them to the known codes or expanding text into lists of know codes
    #     # as a code or a description are consumed we need to remove them from the list so we can check what's left and add more methods accordingly
    #     items = self.split_instr(instr)
    #     res = self.match_all_ES(instr)

    #     res = self.extract_codes_from_string(items)
    #     if res.hasResults():
    #         self.codes[category] = res.codes
    #         print(f"Added {res.codes} as category {category}")
    #     if res.hasRemainingText():
    #         print(f"Unable to process remaining text {res.remnant}")
    #     return None



    # def extract_codes_from_string(self, items: list[str]):
    #     """Extracts any valid codes from the supplied string and returns that and the remainder."""

    #     # populate the output list
    #     # we'll just output the whole lot in one list for now. Later we can output a list per category
    #     codes = []
    #     remnant = []
    #     # first split by comma
    #     items = instr.split(",")
    #     items = [item.strip() for item in items]
    #     return ActionCodeProcessingResult([], items)

    #     for item in items:
    #         if item.upper() in self._all_codes:
    #             codes.append(item)
    #         else:
    #             remnant.append(item)
    #     return ActionCodeProcessingResult(codes=codes, remnant=remnant)

    # def process_string(self, instr: str)
    #     # first check for none
    #     res = self._check_for_none(instr)
    #     if res.

    # def process_string(self, instr: str):
    #     """Sequences through the various other class methods to determine codes from the input string."""
    #     result = self._check_for_none(instr)
    #     if result.hasRemainingText():
    #         print(f"Unable to fully parse description, remainder: {result.remnant}")
    #         return codes
    #     codes = []
    #     result = self.extract_codes_from_string(result.remnant)
    #     codes.extend(result.codes)






# new approach:

#     self.codes
#     self.remnant


#     first check for none
#     then split up

#     then the methods
#     don't need the special class
