#!coding: utf-8
import os
import subprocess as sp
import json
import sys

import setuptools

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# Generate a version file and get version number
def generate_version_file() -> dict:
    """
    Automatically generate a version file for the package.

    :return: version data
    """
    # Get package directory. Because pip will move to a temporary directory, the better way is to rely on the PWD
    # environment variable on Unix systems. For Windows, the cd variable is used instead
    if sys.platform == "win32":
        source_dir = os.environ["cd"]
    else:
        source_dir = os.environ["PWD"]

    # Get the path to the version file within the package
    version_file = os.path.join(source_dir, "src", "mylib", "version.json")

    # Get information from git command line
    commit = sp.check_output(args=["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
    build = sp.check_output(args=["git", "describe", "--tags", "--long"]).decode("utf-8").strip()
    version = build.split("-")[0].strip("vV")

    # Save version data to file
    version_data = {"version": version, "build": build, "commit": commit}
    with open(version_file, mode="w", encoding="utf-8") as file_object:
        data = json.dumps(version_data, indent=4)
        file_object.write(f"{data}\n")

    # Return version data
    return version_data


# Setup of package
setuptools.setup(
    version=generate_version_file()["version"],
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"mylib": ["version.json"]},
    python_requires=">=3.6",
)
