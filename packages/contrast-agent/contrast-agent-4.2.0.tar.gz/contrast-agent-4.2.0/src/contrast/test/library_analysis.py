# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.extern.six import iteritems
from contrast.api.dtm_pb2 import Activity

TEST_MODULES = (
    # deleting sample_namespace_lib_analysis from sys.modules will not allow us
    # to re import it in PY2. sample_namespace_lib_analysis shows up in sys.modules
    # as a builtin module. We only use it in one test, so its not necessary to do so anyway
    "sample_package_onefile",
    "sample_package_tld",
    "sample_package_tld.sample_tld",
    "sample_package_tld2",
    "sample_package_tld2.sample_tld2",
    "sample_package_tld2.subpackage",
    "sample_package_tld2.subpackage.import_file_in_subpackage",
    "sample_package_relative_imports",
    "sample_package_relative_imports.relative_import_same_dir_level",
    "sample_package_relative_imports.module_to_be_imported_in_samedir",
    "sample_package_relative_imports.subpackage",
    "sample_package_relative_imports.subpackage.sample_module_relative_import_parent_module",
    "sample_package_relative_imports.module_to_be_imported_by_subpackage_module",
)

TEST_MODULES_RELATIVE_IMPORT_DIST = (
    "sample_package_relative_imports/__init__.py",
    "sample_package_relative_imports/relative_import_same_dir_level.py",
    "sample_package_relative_imports/module_to_be_imported_in_samedir.py",
    "sample_package_relative_imports/subpackage/__init__.py",
    "sample_package_relative_imports/subpackage/sample_module_relative_import_parent_module.py",
    "sample_package_relative_imports/module_to_be_imported_by_subpackage_module.py",
)

TEST_MODULES_NAMESPACE_DIST = (
    "sample_namespace_lib_analysis/pkg2/sample_module_pkg2.py",
    "sample_namespace_lib_analysis/pkg2/__init__.py",
    "sample_namespace_lib_analysis/pkg1/sample_module_pkg1.py",
    "sample_namespace_lib_analysis/pkg1/__init__.py",
)

TEST_MODULES_MULTIPLE_TLDS_DIST = (
    "sample_package_tld/__init__.py",
    "sample_package_tld/sample_tld.py",
    "sample_package_tld2/__init__.py",
    "sample_package_tld2/sample_tld2.py",
    "sample_package_tld2/subpackage/__init__.py",
    "sample_package_tld2/subpackage/import_file_in_subpackage.py",
)

TEST_MODULE_ONEFILE = ("sample_package_onefile.py",)


def remove_sys_module_entries():
    for mod in TEST_MODULES:
        try:
            del sys.modules[mod]
        except:
            pass


def assert_files_loaded(activity, expected_modules_loaded, hash_filter=None):
    assert isinstance(activity, Activity)

    loaded_file_cnt = 0
    loaded_files = activity.library_usages

    for dist_hash, lib_update in iteritems(loaded_files):
        # leave hash_filter empty if you expect exactly expected_modules_loaded to be in activity.library_usages
        if hash_filter and dist_hash not in hash_filter:
            continue

        for file_loaded in lib_update.class_names.keys():
            assert file_loaded in expected_modules_loaded
            loaded_file_cnt += 1

    assert loaded_file_cnt == len(expected_modules_loaded)


def import_with_relative_imports():
    from sample_package_relative_imports import relative_import_same_dir_level
    from sample_package_relative_imports.subpackage import (
        sample_module_relative_import_parent_module,
    )

    relative_import_same_dir_level.SampleClass()
    sample_module_relative_import_parent_module.SampleClass()


def import_namespace_package():
    from sample_namespace_lib_analysis.pkg1 import sample_module_pkg1
    from sample_namespace_lib_analysis.pkg2 import sample_module_pkg2

    sample_module_pkg1.func_sample_namespace_pkg1()
    sample_module_pkg2.func_sample_namespace_pkg2()


def import_multiple_tlds():
    import sample_package_tld.sample_tld
    import sample_package_tld2.sample_tld2
    from sample_package_tld2.subpackage.import_file_in_subpackage import (
        SAMPLE_GLOBAL_VARIABLE_SUBPACKAGE,
    )

    sample_package_tld.sample_tld.SampleClassTLD()
    sample_package_tld2.sample_tld2.SampleClassTLD()
    x = SAMPLE_GLOBAL_VARIABLE_SUBPACKAGE  # pylint: disable=unused-variable


def import_sample_package_onefile():
    import sample_package_onefile

    sample_package_onefile.SampleClassOneFile()
