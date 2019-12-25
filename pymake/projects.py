# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   PyYAML
import yaml
#   Collections
from collections import namedtuple
#   Pathlib
from pathlib import Path


# =============================================================================
# >> PROJECT DATA TYPE DEFINITION
# =============================================================================
# Definition of the project data keys
ProjectDataKeys = (
    "name",
    "description",
    "version",
    "build_dir",
    "targets"
)


# Definition of the ProjectData type
ProjectData = namedtuple("ProjectData", ProjectDataKeys)


# =============================================================================
# >> PROJECT DATA READER CLASS DEFINITION
# =============================================================================
class ProjectDataReader(object):
    """Class used to read a YAML file and verify its PyMake project data integrity."""

    def __init__(self, yaml_file):
        """C'tor."""
        # Store the YAML file path
        self.path = Path(yaml_file)

        # Raise an error if the file doesn't exist
        if not self.path.exists():
            raise FileNotFoundError(f"YAML file {yaml_file} could not be found.")

    def read(self):
        """Read a YAML file and verify its data."""
        # Read the YAML file via PyYAML
        with self.path.open() as data_fp:
            data = yaml.load(data_fp, Loader=yaml.CLoader)

        # Verify its data
        if not self.verify(data):

            # Return False if the YAML data does not represent a PyMake project
            return False

        # Create and return a new ProjectData object using the YAML file data
        return ProjectData(**data)

    @staticmethod
    def verify(data):
        """PyMake project data integrity check."""
        # For now, just do this...
        # TODO: Check for valid targets, too!
        return sorted(ProjectDataKeys) == sorted(data)
