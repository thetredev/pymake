
from pymake.listeners import PreConfigureProject
from pymake.listeners import PostConfigureProject

from pymake.listeners import PreBuildProject
from pymake.listeners import PostBuildProject

from pymake.listeners import PreConfigureTarget
from pymake.listeners import PostConfigureTarget

from pymake.listeners import PreBuildTarget
from pymake.listeners import PostBuildTarget


@PreConfigureProject()
def project_pre_configure(source_dir, build_dir):
    print("PreConfigureProject:", source_dir, build_dir, "\n")


@PostConfigureProject()
def project_post_configure(project_data):
    print("PostConfigureProject:", project_data, "\n")


@PreBuildProject()
def project_pre_build(project_data):
    print("PreBuildProject:", project_data, "\n")


@PostBuildProject()
def project_post_build(project_data):
    print("PostBuildProject:", project_data, "\n")


@PreConfigureTarget()
def target_pre_configure(name):
    print("PreConfigureTarget:", name, "\n")


@PostConfigureTarget()
def target_post_configure(target_data):
    print("PostConfigureTarget:", target_data, "\n")


@PreBuildTarget()
def target_pre_build(target_data, toolchain):
    print("PreBuildTarget:", target_data, "\n", toolchain.build_command(target_data), "\n")


@PostBuildTarget()
def target_post_build(target_data, toolchain):
    print("PostBuildTarget:", target_data, "\n", toolchain.build_command(target_data), "\n")
