# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Enum
from enum import IntEnum
#   Pathlib
from pathlib import Path
#   Typing
from typing import NamedTuple

# PyMake Imports
from pymake.listeners.managers import ListenerManager
#   Toolchains
from pymake.toolchains import ToolchainData
from pymake.toolchains.base import ToolchainBase


# =============================================================================
# >> OUTPUT TYPES DEFINITION
# =============================================================================
class OutputTypes(IntEnum):
    """Enum used to hold valid output types."""

    EXECUTABLE = 0


# =============================================================================
# >> TARGET DATA TYPE DEFINITION
# =============================================================================
class TargetData(NamedTuple):
    """Class used to hold read-only target data."""

    name: str
    build_dir: Path
    source_files: tuple
    output: str
    output_type: str
    toolchains: tuple

    def __repr__(self):
        """Brief object representation."""
        return f"{self.name}: [{str(self.build_dir.joinpath(self.output))}] as [{self.output_type}]"

    def build(self, toolchain):
        """Build the target using the given toolchain."""
        # Notify `PreBuildTarget` listeners
        ListenerManager.pre_build_target(self, toolchain)

        # Build the target using the given toolchain
        toolchain.build(self)

        # Notify `PostBuildTarget` listeners
        ListenerManager.post_build_target(self, toolchain)

    @staticmethod
    def source_files_from_data(source_dir, data):
        """Return the culmination of source files from the YAML data."""
        # Get a tuple of existing source files
        existing = tuple(
            filter(lambda source_file: source_dir.joinpath(source_file).exists(), map(Path, data))
        )

        # Get a set of glob patterns for source files to resolve
        glob_patterns = set(data) - set(existing)

        # Generate resolved file names using recursive glob for each glob pattern
        resolved = (
            filename for pattern in glob_patterns for filename in source_dir.rglob(pattern)
        )

        # Return a tuple of all file names found
        # TODO: Raise an error if a file doesn't exist and couldn't be rglobbed
        return tuple({
            *existing,
            *resolved
        })

    @staticmethod
    def output_from_data(data):
        """Return the output from the YAML data."""
        return data["output"]

    @staticmethod
    def output_type_from_data(data):
        """Return the output type from the YAML data."""
        # Get the names of valid output types
        valid_output_types = (
            valid_output_type.name for valid_output_type in OutputTypes
        )

        # Get the output type from the YAML data
        output_type = data.get("output_type", "")

        # Raise an error if the YAML output type isn't valid
        if output_type.upper() not in valid_output_types:
            raise KeyError(f"{output_type} is not a valid target output type!")

        # Return the valid output type
        return output_type

    @staticmethod
    def toolchains_from_data(toolchains_data):
        """Generate toolchains from the YAML data."""
        # Create a temporary toolchain lookup table
        toolchains_lookup = {
            toolchain.name: toolchain
            for toolchain in toolchains_data
        }

        # Get the global toolchain from the YAML data or or None if not specified
        global_toolchain = toolchains_lookup.pop("global", None)

        # Generate the global toolchain flags
        global_flags = () if global_toolchain is None else global_toolchain.flags

        # Generate the global toolchain definitions
        global_definitions = () if global_toolchain is None else global_toolchain.definitions

        # Yield new specific toolchain instances using the culmination of
        # the global toolchain flags and definitions and target-specific ones
        for toolchain in toolchains_lookup.values():
            yield ToolchainBase.instances[toolchain.name](ToolchainData(
                name=toolchain.name,
                path=toolchain.path,
                flags=tuple({*global_flags, *toolchain.flags}),
                definitions=tuple({*global_definitions, *toolchain.definitions})
            ))

    @classmethod
    def create(cls, build_dir, name, toolchains, source_dir, data):
        """Return a `TargetData` instance from the YAML data."""
        # Notify `PreConfigureTarget` listeners
        ListenerManager.pre_configure_target(name)

        # Create a `TargetData` instance from the YAML data
        target_data = TargetData(
            name=name,
            source_files=TargetData.source_files_from_data(source_dir, data["source_files"]),
            output=TargetData.output_from_data(data),
            output_type=TargetData.output_type_from_data(data),
            build_dir=build_dir,
            toolchains=tuple(TargetData.toolchains_from_data(toolchains))
        )

        # Notify `PostConfigureTarget` listeners
        ListenerManager.post_configure_target(target_data)

        # Return the `TargetData` instance
        return target_data
