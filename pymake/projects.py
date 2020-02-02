# =============================================================================
# >> IMPORTS
# =============================================================================
# Python Imports
#   Multiprocessing
import multiprocessing
#   PyYAML
import yaml
#   Pathlib
from pathlib import Path
#   Typing
from typing import NamedTuple

# PyMake Imports
#   Projects
from pymake.listeners.managers import ListenerManager
#   Targets
from pymake.targets import TargetData
#   Toolchains
from pymake.toolchains import ToolchainData


# =============================================================================
# >> PROJECT DATA TYPE DEFINITION
# =============================================================================
class ProjectData(NamedTuple):
    """Class used to hold read-only project data."""

    name: str
    description: str
    version: str

    source_dir: Path
    build_dir: Path

    targets: tuple

    def __repr__(self):
        """Brief object representation."""
        return f"<{self.name}> {self.description}\n in: {str(self.build_dir.resolve())}"

    def build(self):
        """Build the project sequentially."""
        # Notify `PreBuildProject` listeners
        ListenerManager.pre_build_project(self)

        # Build the project
        for target in self.targets:
            for toolchain in target.toolchains:
                target.build(toolchain)

        # Notify `PostBuildProject` listeners
        ListenerManager.post_build_project(self)

    def build_parallel(self, processes=multiprocessing.cpu_count()):
        """Build the project in parallel."""
        # Notify `PreBuildProject` listeners
        ListenerManager.pre_build_project(self)

        # Create a multiprocessing pool
        pool = multiprocessing.Pool(processes)

        # Build the project
        for target in self.targets:
            pool.map(target.build, target.toolchains)

        # Notify `PostBuildProject` listeners
        ListenerManager.post_build_project(self)

    @staticmethod
    def name_from_data(data):
        """Return the project name from the YAML data."""
        return data["name"]

    @staticmethod
    def description_from_data(data):
        """Return the project description from the YAML data."""
        return data["description"]

    @staticmethod
    def version_from_data(data):
        """Return the project version from the YAML data."""
        return data["version"]

    @staticmethod
    def source_dir_from_data(data):
        """Return the project source dir from the YAML data as a `Path` instance."""
        return Path(data.get("source_dir", Path.cwd()).relative_to(Path.cwd()))

    @staticmethod
    def build_dir_from_data(data):
        """Return the project build dir from the YAML data as a `Path` instance."""
        return Path(data["build_dir"])

    @staticmethod
    def toolchains_from_data(data):
        """Yield a `ToolchainData` instance for each toolchain from the YAML data."""
        for name, toolchain_data in data.items():
            yield ToolchainData.create(name, toolchain_data)

    @staticmethod
    def targets_from_data(build_dir, toolchains, source_dir, data):
        """Yield a `TargetData` instance for each target from the YAML data."""
        for name, target_data in data.items():
            yield TargetData.create(build_dir, name, toolchains, source_dir, target_data)

    @staticmethod
    def create(data):
        """Return a `ProjectData` instance from the YAML data."""
        source_dir = ProjectData.source_dir_from_data(data)
        build_dir = ProjectData.build_dir_from_data(data)

        # Notify `PreConfigureProject` listeners
        ListenerManager.pre_configure_project(source_dir, build_dir)

        toolchains = ProjectData.toolchains_from_data(data.get("toolchains", dict()))

        project_data = ProjectData(
            name=ProjectData.name_from_data(data),
            description=ProjectData.description_from_data(data),
            version=ProjectData.version_from_data(data),
            source_dir=source_dir,
            build_dir=build_dir,
            targets=tuple(
                ProjectData.targets_from_data(build_dir, toolchains, source_dir, data.get("targets", dict()))
            )
        )

        # Notify `PostConfigureProject` listeners
        ListenerManager.post_configure_project(project_data)

        return project_data

    @staticmethod
    def read(yaml_file):
        """Read a YAML file and return a corresponding `ProjectData` instance."""
        # Make sure we're dealing with a `Path` object
        yaml_file = Path(yaml_file)

        # Raise an error if the file doesn't exist
        if not yaml_file.exists():
            raise FileNotFoundError(f"YAML file {yaml_file} could not be found.")

        # Read the YAML file via PyYAML and return a `ProjectData` instance.
        with yaml_file.open() as data_fp:
            project_data_yaml = yaml.load(data_fp, Loader=yaml.Loader)
            return ProjectData.create(project_data_yaml)
