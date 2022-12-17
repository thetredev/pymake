# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   OS
import os
#   Subprocess
from subprocess import call

# PyMake Imports
#   Toolchains
from pymake.toolchains import ToolchainData
#   Utils
from pymake.utils import recursive_mkdir


# =============================================================================
# >> TOOLCHAIN BASE TYPE DEFINITION
# =============================================================================
class ToolchainBase(object):
    """Class used to interact with a toolchain."""

    # Static toolchain name
    name = None

    # A dict holding non-generic toolchain instances by name
    instances = dict()

    def __init__(self, data: ToolchainData):
        """C'tor."""
        # Store the given `ToolchainData` object.
        self.data = data

    @classmethod
    def register(cls):
        """Register the non-generic toolchain class by name."""
        if cls.name is None:
            raise ValueError(f"Cannot register generic toolchain {cls.__name__}!")

        cls.instances[cls.name] = cls

    def build_command(self, target_data):
        """Generate a build command for the target via this toolchain."""
        # Join the source files to a string separated by whitespace
        source_files_string = " ".join(
            source_file.as_posix() for source_file in target_data.source_files
        )

        # Get the target output path
        output_path = self.output_path(target_data)

        # Make sure the output path exists
        recursive_mkdir(output_path.as_posix().split(os.sep))

        # Compile the target via this toolchain
        compile_cmd = [
            self.data.path.as_posix(),
            *self.definitions(target_data),
            *self.flags(target_data),
            source_files_string,
            self.output_string(output_path)
        ]

        return " ".join(compile_cmd)

    def build(self, target_data):
        """Compile the target via this toolchain."""
        call(self.build_command(target_data), shell=True)

    def output_path(self, target_data):
        """Get the full output path for the given target, i.e. '<build_dir>/<toolchain>/<target_output>'."""
        return target_data.build_dir.joinpath(self.name).joinpath(target_data.output)

    def output_string(self, output_path):
        """Return the toolchain output string."""
        raise NotImplementedError(f"{type(self).__name__} has no clue how to format an output string!")

    def flags(self, target_data):
        """Return formatted target flags for this toolchain."""
        raise NotImplementedError(f"{type(self).__name__} has no clue how to format compile flags!")

    def definitions(self, target_data):
        """Return formatted target definitions for this toolchain."""
        raise NotImplementedError(f"{type(self).__name__} has no clue how to format preprocessor definitions!")

    def from_target_data(self, target_data):
        """Return the target toolchain instance."""
        # Create a temporary target toolchain lookup table
        target_toolchain_lookup = {
            toolchain.name: toolchain
            for toolchain in target_data.toolchains
        }

        # Return the toolchain instance we're looking for
        return target_toolchain_lookup[self.data.name]
