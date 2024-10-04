import json
from pydantic import BaseModel
from pathlib import Path

class Organisation(BaseModel):
    """An abstraction for an organisation including a name and description and the factorty method to produce an autogen agent with those two items"""

    name: str
    prompt: str

    def from_json_file(input_file: Path):
        """Construct an object from a json file"""

def create_instance_from_json(json_data: dict, cls: BaseModel):
    return cls(**json_data)

def create_instance_from_file(json_file: Path, cls: BaseModel):
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    return create_instance_from_file(json_data, cls)


def create_orgs_from_md_files_in_directory(directory_path: str):
    orgs = []

    # Create a Path object for the directory
    directory = Path(directory_path)

    # Iterate over all .md files in the directory
    for file_path in directory.glob('*.md'):
        # Get the file name without the .md extension
        file_name_without_extension = file_path.stem

        # Read the contents of the .md file
        file_contents = file_path.read_text(encoding='utf-8')

        # create an organisation from the file
        org = create_instance_from_json({"name": file_name_without_extension, "prompt": file_contents}, Organisation)

        # append the org to the list
        orgs.append(org)

    return orgs


# Usage
# to make a class from some json
example_json_data = {"name": "Natural England", "prompt": "you are natural england. Rejoice!"}
example_instance = create_instance_from_json(example_json_data, Organisation)

# to read in a directory of md files and create orgs for each
example_orgs = create_orgs_from_md_files_in_directory('organisations/md')
