# =============================================================================
# >> IMPORTS
# =============================================================================
# PyMake Imports
#   Toolchains: Clang
from pymake.toolchains.clang import ClangToolchainC
from pymake.toolchains.clang import ClangToolchainCXX
#   Toolchains: GCC
from pymake.toolchains.gcc import GccToolchainC
from pymake.toolchains.gcc import GccToolchainCXX


# =============================================================================
# >> REGISTER TOOLCHAINS
# =============================================================================
# Register Clang family toolchains
ClangToolchainC.register()
ClangToolchainCXX.register()

# Register GCC family toolchains
GccToolchainC.register()
GccToolchainCXX.register()
