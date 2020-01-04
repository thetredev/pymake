# =============================================================================
# >> IMPORTS
# =============================================================================
# PyMake Imports
#   Toolchains
from pymake.toolchains.base import ToolchainBase


# =============================================================================
# >> GCC TOOLCHAIN FAMILY TYPE DEFINITION
# =============================================================================
class GccToolchainFamily(ToolchainBase):
    """Class used to describe a toolchain of the GCC family."""

    def output_string(self, output_path):
        """Return the formatted output string."""
        return f"-o {output_path}"

    def flags(self, target_data):
        """Return formatted target flags for this toolchain."""
        return self.from_target_data(target_data).data.flags

    def definitions(self, target_data):
        """Yield formatted target definitions for this toolchain."""
        for definition in self.from_target_data(target_data).data.definitions:
            yield f"-D {definition}"


# =============================================================================
# >> GCC TOOLCHAIN TYPE DEFINITIONS
# =============================================================================
class GccToolchainC(GccToolchainFamily):
    """Class used to describe the GCC toolchain for the C language."""

    name = "gcc"


class GccToolchainCXX(GccToolchainFamily):
    """Class used to describe the GCC toolchain for the C++ language."""

    name = "g++"
