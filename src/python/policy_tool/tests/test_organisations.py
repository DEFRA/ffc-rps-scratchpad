import unittest
import json
from app.organisation import Organisation
from pathlib import Path
import tempfile

class TestOrganisation(unittest.TestCase):

    def setUp(self):
        # Set up temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_dir_path = Path(self.temp_dir.name)

        # Test data
        self.json_data = {
            "name": "Test Organisation",
            "address": "123 Test St",
            "employees": 50
        }
        self.json_str = json.dumps(self.json_data)

        # Path to the temporary JSON file in the temp directory
        self.temp_json_file = self.temp_dir_path / 'temp_organisation.json'

        # Write temporary JSON data to file using Pathlib
        self.temp_json_file.write_text(self.json_str, encoding='utf-8')

    def tearDown(self):
        # Clean up the temporary directory after tests
        self.temp_dir.cleanup()

    def test_create_instance_from_json(self):
        # Test the create_instance_from_json method
        instance = Organisation.create_instance_from_json(self.json_data)

        # Assertions to check that the instance was created correctly
        self.assertIsInstance(instance, Organisation)
        self.assertEqual(instance.name, "Test Organisation")
        self.assertEqual(instance.address, "123 Test St")
        self.assertEqual(instance.employees, 50)

    def test_create_instance_from_file(self):
        # Test the create_instance_from_file method
        instance = Organisation.create_instance_from_file(self.temp_json_file)

        # Assertions to check that the instance was created correctly from the file
        self.assertIsInstance(instance, Organisation)
        self.assertEqual(instance.name, "Test Organisation")
        self.assertEqual(instance.address, "123 Test St")
        self.assertEqual(instance.employees, 50)

# This ensures that the tests will run if the script is executed
if __name__ == '__main__':
    unittest.main()
