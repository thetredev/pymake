# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Dataclasses
from dataclasses import dataclass
#   Distutils
import distutils.spawn
#   Pathlib
from pathlib import Path


# =============================================================================
# >> TOOLCHAIN DATA TYPE DEFINITION
# =============================================================================
@dataclass(slots=True)
class ToolchainData(object):
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
            print(f"[WARN] Could not find toolchain executable: {executable}. Skipping this one...")
            return None

        return Path(spawn_result)

    @staticmethod
    def flags_from_data(data):
        """Return a tuple of flags from the YAML data."""
        return tuple(data.get("flags", tuple()))

    @staticmethod
    def definitions_from_data(data):
        """Return a tuple of definitions from the YAML data."""
        definitions: dict = data.get("definitions", dict())

        if not definitions:
            return definitions

        return [
            *definitions.get("macros", list()),
            *[
                rf'{key}=\"{value}\"' if isinstance(value, str) else f"{key}={value}"
                for key, value in definitions.get("tokenized", dict()).items()
            ]
        ]

    @staticmethod
    def create(name, data):
        """Return a `ToolchainData` instance from the YAML data."""
        toolchain_path = ToolchainData.path_from_data(name)

        if toolchain_path is None and name != "global":
            return None

        return ToolchainData(
            name=name,
            path=toolchain_path,
            flags=ToolchainData.flags_from_data(data),
            definitions=ToolchainData.definitions_from_data(data)
        )
