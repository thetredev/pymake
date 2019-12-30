# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Typing
from typing import NamedTuple

# PyMake
import pymake


# =============================================================================
# >> PROJECT DATA TYPE DEFINITION
# =============================================================================
class ProjectData(NamedTuple):
    """Class used to describe project data."""

    name: str
    description: str
    version: str
    build_dir: str
    targets: dict

    @classmethod
    def keys(cls):
        """Shorthand for receiving custom class keys."""
        return pymake.get_cls_keys(cls)
