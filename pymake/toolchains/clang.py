# =============================================================================
# >> IMPORTS
# =============================================================================
# PyMake Imports
#   Toolchains
from pymake.toolchains.base import ToolchainBase


# =============================================================================
# >> CLANG TOOLCHAIN FAMILY TYPE DEFINITION
# =============================================================================
class ClangToolchainFamily(ToolchainBase):
    """Class used to describe a toolchain of the Clang family."""

    def output_string(self, output_path):
        """Return the formatted output string."""
        return f"-o {output_path}"

    def flags(self, target_data):
        """Return formatted target flags for this toolchain."""
        return self.from_target_data(target_data).data.flags

    def definitions(self, target_data):
        """Yield formatted target definitions for this toolchain."""
        for definition in self.from_target_data(target_data).data.definitions:
            yield "-D"
            yield definition


# =============================================================================
# >> CLANG TOOLCHAIN TYPE DEFINITIONS
# =============================================================================
class ClangToolchainC(ClangToolchainFamily):
    """Class used to describe the Clang toolchain for the C language."""

    name = "clang"


class ClangToolchainCXX(ClangToolchainFamily):
    """Class used to describe the Clang toolchain for the C++ language."""

    name = "clang++"
