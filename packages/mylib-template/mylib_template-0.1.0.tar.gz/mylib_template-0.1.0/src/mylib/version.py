#!coding: utf-8
import os
import json


def get_version_file() -> str:
    """
    Return the full path to version.json file within package.

    :return: full path of version file
    """
    return os.path.join(os.path.dirname(__file__), "version.json")


def get_version_data() -> dict:
    """
    Get version data of package. The version data includes:

    - the version number
    - the build number
    - the commit number

    :return: version data
    """
    version_file = get_version_file()
    data = {"version": "N/A", "build": "N/A", "commit": "N/A"}
    if os.path.exists(version_file):
        with open(version_file, mode="r", encoding="utf-8") as file_object:
            data = json.loads(file_object.read())
    return data


def version() -> str:
    """
    Return the version number of the package.

    :return: version number
    """
    return get_version_data()["version"]


def build() -> str:
    """
    Return the build number of the package.

    :return: build number
    """
    return get_version_data()["build"]


def commit() -> str:
    """
    Return the commit identifier of the package.

    :return: commit if
    """
    return get_version_data()["commit"]



