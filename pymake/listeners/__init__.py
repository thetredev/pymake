# =============================================================================
# >> IMPORTS
# =============================================================================
# PyMake Imports
#   Listeners: Base
from pymake.listeners.base import ListenerBase
#   Listeners: Managers / Project
from pymake.listeners.managers import _project_pre_configure_manager
from pymake.listeners.managers import _project_post_configure_manager
from pymake.listeners.managers import _project_pre_build_manager
from pymake.listeners.managers import _project_post_build_manager
#   Listeners: Managers / Target
from pymake.listeners.managers import _target_pre_configure_manager
from pymake.listeners.managers import _target_post_configure_manager
from pymake.listeners.managers import _target_pre_build_manager
from pymake.listeners.managers import _target_post_build_manager


# =============================================================================
# >> LISTENER DEFINITIONS
# =============================================================================
class PreConfigureProject(ListenerBase):
    """Decorator class used to call a callback before configuring a project."""

    manager = _project_pre_configure_manager


class PostConfigureProject(ListenerBase):
    """Decorator class used to call a callback after configuring a project."""

    manager = _project_post_configure_manager


class PreBuildProject(ListenerBase):
    """Decorator class used to call a callback before building a project."""

    manager = _project_pre_build_manager


class PostBuildProject(ListenerBase):
    """Decorator class used to call a callback after building a project."""

    manager = _project_post_build_manager


class PreConfigureTarget(ListenerBase):
    """Decorator class used to call a callback before configuring a target."""

    manager = _target_pre_configure_manager


class PostConfigureTarget(ListenerBase):
    """Decorator class used to call a callback after configuring a target."""

    manager = _target_post_configure_manager


class PreBuildTarget(ListenerBase):
    """Decorator class used to call a callback before building a target."""

    manager = _target_pre_build_manager


class PostBuildTarget(ListenerBase):
    """Decorator class used to call a callback after building a target."""

    manager = _target_post_build_manager
