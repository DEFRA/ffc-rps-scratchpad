import duckdb
from pathlib import Path
from pydantic import BaseModel


class LandFeature(BaseModel):
    "A Land Feature record."""

    feature_id: int
    feature_type: str
    below_moorland: bool
    in_sda: bool
    is_manmade: bool
    is_natural: bool
    is_historic: bool
    is_culvert: bool
    is_water_feature: bool
    has_vegetation: bool
    contains_water: bool
    requires_hefer: bool

class Rule(BaseModel):
    """A record representing a rule."""

    name: str
    field: list[str]
    operator: list[str]
    value: list

    def test_operator(self, operator: str, values: list):
        """Applies the operator to the values."""
        if operator == "equals":
            result = values[0] == values[1]
        elif operator == "greater":
            result = values[0] > values[1]
        else:
            result = False
        return result

    def evaluate(self, input_values: list):
        """Evaluates the rule against the inputs."""
        for f, o, v in zip(self.field, self.operator, self.value):
            if not self.test_operator(f, o, v):
                return (False, [f, o, v])
        return (True, [None, None, None])

class LandParcel(BaseModel):
    """A Land Parcel record."""

    parcel_id: int
    area: float
    perimeter: float
    is_moorland: bool
    is_sssi: bool
    historic_eligible: bool
    feature_ids: list[int]

    def evaluate_rule(self, rule: Rule):
        """Evaluates a given rule against this parcel."""



def read_landparcels(infile: Path):
    """Populates a duckDB table from the supplied land parcels file."""
    duckdb.read_csv("example.csv")
    return True

def read_landfeatures(infile: Path):
    pass

def join_features():
    """Join the features to the land parcels by feature id."""
    pass

def load_data():
    """Read in the parcels and features, join them."""
    read_landparcels(Path("land_parcels.csv"))
    read_landfeatures(Path("land_features.csv"))
    join_features()

def read_rules(infile: Path):
    """Reads in a set of rules from a json document."""
    return True