#
# Copyright (C) 2020 Arm Mbed. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
"""Configure and build a CMake project."""
import logging
import pathlib
import subprocess

from typing import Optional

from mbed_tools.build.exceptions import MbedBuildError


logger = logging.getLogger(__name__)


def build_project(build_dir: pathlib.Path, target: Optional[str] = None) -> None:
    """Build a project using CMake to invoke Ninja.

    Args:
        build_dir: Path to the CMake build tree.
        target: The CMake target to build (e.g 'install')
    """
    target_flag = ["--target", target] if target is not None else []
    _cmake_wrapper("--build", str(build_dir), *target_flag)


def generate_build_system(source_dir: pathlib.Path, build_dir: pathlib.Path, profile: str) -> None:
    """Configure a project using CMake.

    Args:
        source_dir: Path to the CMake source tree.
        build_dir: Path to the CMake build tree.
        profile: The Mbed build profile (develop, debug or release).
    """
    _cmake_wrapper("-S", str(source_dir), "-B", str(build_dir), "-GNinja", f"-DCMAKE_BUILD_TYPE={profile}")


def _cmake_wrapper(*cmake_args: str) -> None:
    try:
        logger.debug("Running CMake with args: %s", cmake_args)
        subprocess.run(["cmake", *cmake_args], check=True)
    except subprocess.CalledProcessError:
        raise MbedBuildError("CMake invocation failed!")
