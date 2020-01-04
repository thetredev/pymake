

# =============================================================================
# >> LISTENER MANAGER TYPE DEFINITION
# =============================================================================
class ListenerManager(list):
    """List class used to conveniently call listener decorator callbacks."""

    @staticmethod
    def call(manager, *args):
        """Call all `ListenerManager` instances of a certain type with proper arguments."""
        for instance in manager:
            instance.callback(*args)

    @staticmethod
    def pre_configure_project(source_dir, build_dir):
        """Call all `PreConfigureProject` instances with proper arguments."""
        ListenerManager.call(_project_pre_configure_manager, source_dir, build_dir)

    @staticmethod
    def post_configure_project(project_data):
        """Call all `PostConfigureProject` instances with proper arguments."""
        ListenerManager.call(_project_post_configure_manager, project_data)

    @staticmethod
    def post_build_project(project_data):
        """Call all `PreBuildProject` instances with proper arguments."""
        ListenerManager.call(_project_post_build_manager, project_data)

    @staticmethod
    def pre_build_project(project_data):
        """Call all `PostBuildProject` instances with proper arguments."""
        ListenerManager.call(_project_pre_build_manager, project_data)

    @staticmethod
    def pre_configure_target(name):
        """Call all `PreConfigureTarget` instances with proper arguments."""
        ListenerManager.call(_target_pre_configure_manager, name)

    @staticmethod
    def post_configure_target(target_data):
        """Call all `PostConfigureTarget` instances with proper arguments."""
        ListenerManager.call(_target_post_configure_manager, target_data)

    @staticmethod
    def pre_build_target(target_data, toolchain):
        """Call all `PreBuildTarget` instances with proper arguments."""
        ListenerManager.call(_target_pre_build_manager, target_data, toolchain)

    @staticmethod
    def post_build_target(target_data, toolchain):
        """Call all `PostConfigureTarget` instances with proper arguments."""
        ListenerManager.call(_target_post_build_manager, target_data, toolchain)


# =============================================================================
# >> LISTENER MANAGER DEFINITIONS
# =============================================================================
# Project managers
_project_pre_configure_manager = ListenerManager()
_project_post_configure_manager = ListenerManager()
_project_pre_build_manager = ListenerManager()
_project_post_build_manager = ListenerManager()

# Target managers
_target_pre_configure_manager = ListenerManager()
_target_post_configure_manager = ListenerManager()
_target_pre_build_manager = ListenerManager()
_target_post_build_manager = ListenerManager()
