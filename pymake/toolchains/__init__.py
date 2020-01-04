# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Distutils
import distutils.spawn
#   Pathlib
from pathlib import Path
#   Typing
from typing import NamedTuple


# =============================================================================
# >> TOOLCHAIN DATA TYPE DEFINITION
# =============================================================================
class ToolchainData(NamedTuple):
    """Class used to hold read-only toolchain data."""

    name: str
    path: Path
    flags: tuple
    definitions: tuple

    @staticmethod
    def path_from_data(executable):
        """Return the toolchain executable path from the YAML data."""
        # Return None if we're dealing with the global target
        if executable == "global":
            return None

        # Get the path to the specified executable
        path = Path(executable)

        # Return the executable path if it exists
        if path.exists():
            return path

        # Try to find the executable if the executable path doesn't exist
        spawn_result = distutils.spawn.find_executable(path)

        if spawn_result is None:
            raise ValueError(f"Could not find toolchain executable: {executable}")

        return Path(spawn_result)

    @staticmethod
    def flags_from_data(data):
        """Return a tuple of flags from the YAML data."""
        return tuple(data.get("flags", tuple()))

    @staticmethod
    def definitions_from_data(data):
        """Return a tuple of definitions from the YAML data."""
        return tuple(data.get("definitions", tuple()))

    @staticmethod
    def create(name, data):
        """Return a `ToolchainData` instance from the YAML data."""
        return ToolchainData(
            name=name,
            path=ToolchainData.path_from_data(name),
            flags=ToolchainData.flags_from_data(data),
            definitions=ToolchainData.definitions_from_data(data)
        )
