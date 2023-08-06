#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
import io

import setuptools
from setuptools.command.build_py import build_py

NAME = "ciomax"
DESCRIPTION = "Max plugin for Conductor Cloud Rendering Platform."
URL = "https://github.com/AtomicConductor/conductor-max"
EMAIL = "info@conductortech.com"
AUTHOR = "conductor"
REQUIRES_PYTHON = "~=2.7"
REQUIRED = ["ciocore>=0.2.15,<1.0.0"]
HERE = os.path.abspath(os.path.dirname(__file__))
DEV_VERSION = "dev.999"

with open(os.path.join(HERE, 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

long_description = ""

with open(os.path.join(HERE, 'README.md')) as readme:
    long_description = readme.read().strip()

long_description += "\n\n## Changelog\n\n"
with open(os.path.join(HERE, 'CHANGELOG.md')) as changelog:
    long_description += changelog.read().strip()   
 



class BuildCommand(build_py):
    def run(self):
        build_py.run(self)
        if not self.dry_run:
            target_dir = os.path.join(self.build_lib, NAME)
            self.write_version_info(target_dir)
 
    def write_version_info(self, target_dir):
        with open(os.path.join(target_dir, "VERSION"), "w") as f:
            f.write(VERSION)


# OS Independent - because, even though Max only runs on Windows, a studio may
# wish to install the plugin on a linux server and make it accessible to
# Windows workstations.
setuptools.setup(
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Multimedia :: Graphics :: 3D Rendering",
    ],
    cmdclass={"build_py": BuildCommand},
    description=DESCRIPTION,
    install_requires=REQUIRED,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=NAME,
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    include_package_data=True,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    version=VERSION,
    zip_safe=False,
    package_data={NAME: ["Conductor.ms"]}
)
