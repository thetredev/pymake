"""
Command line interface for the PyMake library.
"""
# =============================================================================
# >> IMPORTS
# =============================================================================
# PyMake Imports
#   Projects
from pymake.projects import ProjectData


# Get project data from the YAML file inside the current working directory
data = ProjectData.read("pymake.yml")

# Build the target sequentially
# data.build()

# Build the target in parallel
data.build_parallel()
