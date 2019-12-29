# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   PyYAML
import yaml
#   Pathlib
from pathlib import Path
#   Tempfile
from tempfile import gettempdir
#   Unittest
from unittest import TestCase

# PyMake imports
from pymake.projects import Project
from pymake.projects import ProjectData


# =============================================================================
# >> CONSTANTS
# =============================================================================
# Definition of the temporary YAML test file
YAML_FILE = Path(gettempdir()).joinpath("pymake_test", "test.yml")

# Definition of the YAML test file data
YAML_FILE_DATA = {
    "name": "Test Project",
    "description": "...",
    "version": "1.0",
    "build_dir": "./build",
    "targets": dict()
}


# =============================================================================
# >> PYMAKE CONFIG TEST CLASS DEFINITION
# =============================================================================
class PyMakeProjectsTest(TestCase):
    """Unit test for the pymake.project module."""

    def tearDown(self):
        """Remove temporary files and folders if they exists."""
        if YAML_FILE.exists():
            YAML_FILE.unlink()

        if YAML_FILE.parent.exists():
            YAML_FILE.parent.rmdir()

    def test_reader_verify(self):
        """Test the config.ProjectDataReader.verify() method."""
        # Make sure the YAML test file data is correct
        self.assertTrue(Project.verify(YAML_FILE_DATA))

        # Get a copy of the YAML test file data and update it with invalid data
        test_yaml = YAML_FILE_DATA.copy()
        test_yaml.update({
            "misc": "T",
            "two": 2
        })

        # Make sure the updated data is indeed marked as invalid
        # i.e. .verify() returning False
        self.assertFalse(Project.verify(test_yaml))

    def test_reader_init(self):
        """Test the config.ProjectDataReader constructor."""
        # Make sure the constructor raises an error if the YAML file given does not exist
        self.assertRaises(FileNotFoundError, Project, str(YAML_FILE))

        # Create the YAML test file
        self.create_yaml_file(YAML_FILE_DATA)

        # Make sure the constructor works when the YAML file given exists
        project = Project(str(YAML_FILE))
        self.assertEqual(YAML_FILE, project.path)

    def test_reader_read(self):
        """Test the config.ProjectDataReader.read() method."""
        # Create a ProjectData object with the expected data
        project_data_expected = ProjectData(**YAML_FILE_DATA)

        # Create the YAML test file
        self.create_yaml_file(YAML_FILE_DATA)

        # Create a ProjectDataReader object for the YAML test file and read its data
        project_data_reader = Project(str(YAML_FILE))
        project_data = project_data_reader.read()

        # Make sure the expected project data is equal to the project data read
        self.assertEqual(project_data_expected, project_data)

    @staticmethod
    def create_yaml_file(data):
        """Create the YAML test file in the temporary directory."""
        # Make sure the temporary file directory exists
        YAML_FILE.parent.mkdir(exist_ok=True)

        # Dump the YAML data to file
        with YAML_FILE.open("w") as data_fp:
            yaml.dump(data, data_fp, Dumper=yaml.Dumper)
