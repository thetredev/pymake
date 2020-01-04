# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   OS
import os
#   Pathlib
from pathlib import Path


# =============================================================================
# >> UTILITY FUNCTIONS
# =============================================================================
def recursive_mkdir(parts):
    """Recursively call `Path`.mkdir() given an iterable of path parts."""
    # Raise an error if we're dealing with wrong input data
    if not all(isinstance(part, str) for part in parts):
        raise ValueError("`parts` must be an iterable of `pathlib.Path` instances!")

    # Recursively call .mkdir() for each path part concatenated with its previous parts
    for i in range(len(parts)):
        part = Path(os.sep.join(parts[:i]))
        Path(part).mkdir(exist_ok=True)
