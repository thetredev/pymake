# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Importlib
import importlib.util
#   Pathlib
from pathlib import Path

# PyMake Imports
#   Projects
from pymake.projects import ProjectData
#   Toolchains: Clang
from pymake.toolchains.clang import ClangToolchainC
from pymake.toolchains.clang import ClangToolchainCXX
#   Toolchains: GCC
from pymake.toolchains.gcc import GccToolchainC
from pymake.toolchains.gcc import GccToolchainCXX


def register_toolchains():
    """Register toolchains."""
    toolschains = (
        ClangToolchainC,
        ClangToolchainCXX,
        GccToolchainC,
        GccToolchainCXX
    )

    for toolchain in toolschains:
        toolchain.register()


def main():
    register_toolchains()

    # Load the make.py module, if it exists
    make_py = Path("make.py")

    if make_py.exists():
        spec = importlib.util.spec_from_file_location("make", make_py.as_posix())
        make = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(make)

    # Get project data from the YAML file inside the current working directory
    data = ProjectData.read("pymake.yml")

    # Build the target sequentially
    # data.build()

    # Build the target in parallel
    data.build_parallel()
