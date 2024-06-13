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


class ActionCodes(BaseModel):
    """Holds a list of the codes and allows for it to be added to and removed from.
    Uses this to extract codes from strings and expand general statements into explicit lists."""

    # the keys in this dict represent categories of Action such as SFI2024 or ES.
    # the value is then a list of codes, as strings and in uppercase

    # you can create the class with this dictionary explicitly constructed or you can use the builder methods add_category()
    codes: dict = None

    def model_post_init(self, *args, **kwargs):
        if self.codes is None:
            self.codes = {}

    def add_category(self, category: str, codes: list[str]):
        """Adds a new named category of Actions."""

        # trusting the user to supply a proper list of codes. Might have to add error handling if this goes wrong a lot
        if category in self.codes.keys():
            print(f"Category {category} already exists, ignoring.")
        else:
            self.codes[category] = codes

    def all_codes(self):
        return [item for k, v in self.codes.items() for item in v]

    def extract_code_from_string(self, instr: str):
        """Obtains a list of valid codes from the supplied string and returns that and the remainder."""
        # first split by comma
        items = instr.split(",")
        items = [item.strip() for item in items]
        # populate the output list
        # we'll just output the whole lot in one list for now. Later we can output a list per category
        res = []
        remainder = []
        all_codes = self.all_codes()
        for item in items:
            if item.upper() in all_codes:
                res.append(item)
            else:
                remainder.append(item)
        return (res, remainder)