# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import pip
import hashlib
import json
from io import open

from contrast.agent import scope

CONTRAST_AGENT_DIST = "contrast-agent"

# Both of these metadata files contain a file list of what is installed under the top level dirs
RECORD = "RECORD"
SOURCES = "SOURCES.txt"

NAMESPACE_PACKAGE = "namespace_packages.txt"
TOP_LEVEL_TXT = "top_level.txt"

PY_SUFFIX = ".py"
SO_SUFFIX = ".so"

SITE_PACKAGES_DIR = "{}site-packages{}".format(os.sep, os.sep)
DIST_PACKAGES_DIR = "{}dist-packages{}".format(os.sep, os.sep)


def normalize_file_name(file_path):
    """
    This function converts a file ending in .pyc to .py. The reason for this
    is due to how screener is configured to verify a file was reported (only supports
    exact match not a regex)
    @param file_path: full path to a python file ending in .pyc or .py
    @return: file_path ending in .py
    """
    file_to_report = file_path.rpartition(SITE_PACKAGES_DIR)

    if not file_to_report[1]:
        file_to_report = file_path.rpartition(DIST_PACKAGES_DIR)
        if not file_to_report[1]:
            return None

    normalized_file_name = file_to_report[2]
    if normalized_file_name.endswith(".pyc"):
        normalized_file_name = normalized_file_name[: len(normalized_file_name) - 1]

    return normalized_file_name


def get_installed_distributions():
    """
    Wrapper used to get list of installed distributions in current active environment.
    This is necessary because the function definition location changed between different pip versions
    """
    with scope.contrast_scope():
        pip_version = pip.__version__
        major_version = int(pip_version.split(".")[0])

        # newest versions of pip
        if major_version >= 10:  # ['10', '18', '19']
            from pip._internal.utils.misc import get_installed_distributions

            return get_installed_distributions()

        if 6 <= major_version <= 9:  # ['6', '7', '8', '9']
            # 9 and below; these releases go back until Dec 22, 2014
            return pip.get_installed_distributions()

        return []


def _parse_top_level_dirs_from_manifest_file(dist, namespace, metadata_filename):
    """
    @param dist: Distribution object used to check to see what
    metadata files exist for us to parse
    @type dist: pip._vendor.pkg_resources.DistInfoDistribution
    @param namespace: The name of the namespace to search
    @type namespace: string
    @param metadata_filename: Name of metadata file to parse
    @type metadata_filename: string
    """
    top_level_dirs = set()

    if dist.has_metadata(metadata_filename):
        for line in dist.get_metadata_lines(metadata_filename):
            if line.startswith(namespace + os.sep):
                dirs = line.split(os.sep)
                if len(dirs) > 1:
                    top_level_dirs.add(dirs[1])

    return top_level_dirs


def get_top_level_directories_namespace_pkg(dist, namespace):
    """
    @param dist: Distribution object used to check to see what
    metadata files exist for us to parse
    @type dist: pip._vendor.pkg_resources.DistInfoDistribution
    @param namespace: The name of the namespace to search
    @type namespace: string
    @return: The top level importable packages/modules under the namespace
    @rtype: string
    """
    top_level_dirs = set()
    manifest_files = (RECORD, SOURCES)

    if not dist:
        return top_level_dirs

    for manifest in manifest_files:
        top_level_dirs = _parse_top_level_dirs_from_manifest_file(
            dist, namespace, manifest
        )
        if top_level_dirs:
            break

    return top_level_dirs


def get_top_level_directories(dist):
    """

    @param dist: Distribution object used to check to see what
    metadata files exist for us to parse
    @type dist: pip._vendor.pkg_resources.DistInfoDistribution
    @return: list of top level importable modules/packages for the dist
    @rtype: list
    """
    # some packages have multiple top level directories, so check for all of them
    top_level_dirs = []

    # file storing directory names for top level directories of package
    if dist.has_metadata(TOP_LEVEL_TXT):
        top_level_dirs = list(dist.get_metadata_lines(TOP_LEVEL_TXT))
    elif dist.has_metadata(RECORD):
        # TODO: PYT-927 Code needs to properly parse TLDs from RECORD file
        metadata_lines = [d.split(",")[0] for d in dist.get_metadata_lines(RECORD)]

        top_level_dirs = [
            x
            for x in metadata_lines
            if "/" in x and x.split(os.sep)[1] == "__init__.py"
        ]
    else:
        # TODO: PYT-927 replace this code with a log message since we don't know if it actually works.
        # Log message will give us more information on the distribution that enters this statement
        if isinstance(dist._provider, pip._vendor.pkg_resources.FileMetadata):
            path = "/".join([dist._provider.path, TOP_LEVEL_TXT])
        else:
            # pip._vendor.pkg_ressample_namespace_lib_analysisources.PathMetadata
            path = "/".join([dist._provider.egg_info, TOP_LEVEL_TXT])

        try:
            with open("/".join([path, TOP_LEVEL_TXT]), "rb") as tl:
                top_level_dirs = tl.readlines()
        except IOError as _:
            pass

    return top_level_dirs


def get_file_from_module(module):
    if hasattr(module, "__file__") and module.__file__:
        return os.path.realpath(module.__file__)

    return None


def get_data(dist):
    """
    Given a dist, pulls name, version, manifest, and url out of the metadata
    :param dist: the distribution package whose package info is being retrieved
    :return: the package info from the metadata
    """
    version = dist.version
    manifest = dist.get_metadata(dist.PKG_INFO)

    # If the data has a .json format
    if dist.PKG_INFO == "METADATA":
        url = get_metadata(dist)

    # If the data is in PKG-INFO form
    elif dist.PKG_INFO == "PKG-INFO":
        url = get_pkg_info(dist)

    # If the metadata is not in either form
    else:
        raise Exception(dist.PKG_INFO, "Package metadata not found")

    return version, manifest, str(url)


EXTENTIONS = "extensions"
HOME = "Home"
PROJECT_URLS = "project_urls"
PYTHON_DETAILS = "python.details"


def get_metadata(dist):
    """
    Gets the library data if PKG_INFO is packaged in a json
    :param dist: the distribution package who's data is being parsed
    :return: the url of the package
    """

    try:
        metadata = json.loads(dist.get_metadata("metadata.json"))

        if PROJECT_URLS in metadata[EXTENTIONS][PYTHON_DETAILS]:
            return metadata[EXTENTIONS][PYTHON_DETAILS][PROJECT_URLS][HOME]
    except:
        pass

    try:
        metadata = json.loads(dist.get_metadata("pydist.json"))
        if PROJECT_URLS in metadata:
            return metadata[PROJECT_URLS][HOME]
    except:
        pass

    return ""


HOME_PAGE = "Home-page: "


def get_pkg_info(dist):
    """
    Gets the library data if PKG_INFO is packaged in a text file
    :param dist: the distribution package who's data is being parsed
    :return: the url of the package
    """

    # Split metadata so it can be searched
    metadata = list(dist.get_metadata_lines(dist.PKG_INFO))

    # Search metadata for homepage
    for line in metadata:
        if line.startswith(HOME_PAGE):
            return line.split(HOME_PAGE)[1]

    return ""


def get_hash(name, version):
    """
    DO NOT ALTER OR REMOVE
    """
    to_hash = name + " " + version

    return hashlib.sha1(to_hash.encode("utf-8")).hexdigest()


def append_files_loaded_to_activity(activity_dtm, loaded_files, dist_hash):
    """
    @param activity_dtm: library_usages are added to this message
    @param loaded_files: List of loaded files to report
    @param dist_hash: Hash of distribution to report files loaded
    @return: Number of files to be reported
    """

    total_loaded_files_cnt = 0
    # In Protocol Buffers maps, referencing an undefined key creates the key in the map with a
    # zero/false/empty value. https://developers.google.com/protocol-buffers/docs/reference/python-generated
    # Have to reuse existing usage update message because if we don't, embedded imports wont be reported properly.
    # For example, if we do this: import x -> (in x) import y, than the last module, y will be
    # reported (x will be lost)
    usage_update = activity_dtm.library_usages[dist_hash]
    usage_update.hash_code = dist_hash
    # 0 - unused in newer TS endpoint
    usage_update.count = 0

    for f in loaded_files:
        if f:
            total_loaded_files_cnt += 1
            usage_update.class_names[f] = True

    return total_loaded_files_cnt
