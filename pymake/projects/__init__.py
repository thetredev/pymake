# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   PyYAML
import yaml
#   Pathlib
from pathlib import Path

# PyMake
from pymake.projects.data import ProjectData


# =============================================================================
# >> PROJECT CLASS DEFINITION
# =============================================================================
class Project(object):
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
            project_data = yaml.load(data_fp, Loader=yaml.Loader)

        # Verify its data
        if not self.verify(project_data):

            # Return False if the YAML data does not represent a PyMake project
            return False

        # Create and return a new ProjectData object using the YAML file data
        return ProjectData(**project_data)

    @staticmethod
    def verify(project_data):
        """PyMake project data integrity check."""
        # For now, just do this...
        # TODO: Check for valid targets, too!
        return sorted(ProjectData.keys()) == sorted(project_data)
