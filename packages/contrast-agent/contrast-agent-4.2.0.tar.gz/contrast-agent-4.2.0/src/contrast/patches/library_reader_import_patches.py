# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

import contrast

from contrast.utils.decorators import fail_safely
from contrast.extern.six import iteritems
from contrast.extern.six import PY2
from contrast.extern.six.moves import builtins
from contrast.extern.ported_cpython_code.import_functionality import (
    resolve_relative_import_name,
)
from contrast.extern.wrapt import register_post_import_hook
from contrast.utils.patch_utils import patch_cls_or_instance
from contrast.utils.library_reader.patched_state import DistributionContext
from contrast.agent import scope
from contrast.utils.library_reader.utils import (
    normalize_file_name,
    get_file_from_module,
    append_files_loaded_to_activity,
)


def names_to_possible_sys_module_entries(possible_sys_module_entries):
    """This function converts something like : name = "a.b.c", fromlist = ("d") into
    sys_module_cache = {
        "a": sys.modules["a"],
        "a.b": sys.modules["a.b"],
        "a.b.c": sys.modules["a.b.c"]
        "a.b.c.d": sys.modules["a.b.c.d"] (NOTE: item "d" in the fromlist can be a class or a variable to import.
            We aren't 100% sure if its a module/package because we don't have direct control over what gets set
            on sys.modules. In this scenario this is in part an estimation. Hence the checks in sys.modules
            using sys_module_cache before and after import)
    }
    Calling this function before and after import is used to see what files where actually loaded and then cached.
    This has to be done because __import__ only returns the top level module (e.g sys_modules["a"]) or
    a single specific module if a fromlist is not none.

    arguments: possible_sys_module_entries - a list of possible entries in sys modules
    return: a dictionary containing entries in sys modules based on the tuple possible_sys_module_entries
    """
    sys_module_cache = {}

    if not possible_sys_module_entries:
        return None

    for entry in possible_sys_module_entries:
        sys_module_cache[entry] = sys.modules.get(entry, None)

    return sys_module_cache


def build_possible_sys_module_keys(name, level, global_namespace, fromlist):
    """
    The purpose of this function is to create a list of keys that could be cached in sys.modules
    arguments:
    name - name of module to be imported
    fromlist - list of modules, variables and classes to import
    e.g if the import was performed: from module import SomeClass, fromlist=('SomeClass',)
    """
    possible_sys_module_entries = set()

    if level > 0:
        name = resolve_relative_import_name(name, level, global_namespace)

    if not name:
        return None

    parents = name.split(".")

    for i in range(len(parents)):
        possible_sys_module_entries.add(".".join(parents[0 : i + 1]))

    if fromlist and fromlist[0] != "*":
        for import_item in fromlist:
            possible_sys_module_entries.add("{}.{}".format(name, import_item))

    return possible_sys_module_entries


def build_new_loaded_files(before_import_sys_modules, after_import_sys_modules):
    """
    The purpose of this function is to compare the values in both dictionaries.
    If before_import_sys_modules doesn't contain a value given a key and
    after_import_sys_modules does, than that module was just loaded and we report on it.
    """
    dist_ctx = DistributionContext()
    modules_loaded = {}

    if not before_import_sys_modules or not after_import_sys_modules:
        return modules_loaded

    for sys_module_key in before_import_sys_modules.keys():
        if (
            not before_import_sys_modules[sys_module_key]
            and after_import_sys_modules[sys_module_key]
        ):
            module = after_import_sys_modules[sys_module_key]
            module_file = get_file_from_module(module)

            # If dist_hash is None, that means we didn't detect the module loaded in the current env
            dist_hash = dist_ctx.get_dist_hash_from_file_path(module_file)
            if dist_hash:
                normalized_file_name = normalize_file_name(module_file)
                files_loaded = modules_loaded.get(dist_hash, None)
                if files_loaded:
                    files_loaded.append(normalized_file_name)
                else:
                    modules_loaded[dist_hash] = [normalized_file_name]

    return modules_loaded


# Default level changed between PY2 and PY3
# -1 means attempt abs and relative import
# 0 means attempt abs import
if PY2:
    LEVEL = -1
else:
    LEVEL = 0


@fail_safely(
    "Failed to determine sys module keys to perform analysis on",
    return_value=(None, None, None),
)
# Need to use original key name for globals/locals to make sure its unpacked properly when in key=value form.
# Arguments can be passed as either a list (e.g __import__(name, globals_dict, locals_dict, ...)) or
# key=value so we need to make sure we account for both cases
# pylint: disable=redefined-builtin
def pre__import__analysis(
    name, globals=None, locals=None, fromlist=(), level=LEVEL, **kwargs
):
    perform_analysis = False

    possible_sys_module_keys = build_possible_sys_module_keys(
        name, level, globals, fromlist
    )

    if possible_sys_module_keys:
        perform_analysis = True

        before_import_sys_modules = names_to_possible_sys_module_entries(
            possible_sys_module_keys
        )

    return perform_analysis, possible_sys_module_keys, before_import_sys_modules


@fail_safely("Failed to determine loaded files")
def post__import__analysis(
    req_context, before_import_sys_modules, possible_sys_module_keys
):
    after_import_sys_modules = names_to_possible_sys_module_entries(
        possible_sys_module_keys
    )

    loaded_files_dict = build_new_loaded_files(
        before_import_sys_modules, after_import_sys_modules
    )

    if len(loaded_files_dict) > 0:
        for dist_hash, loaded_files in iteritems(loaded_files_dict):
            append_files_loaded_to_activity(
                req_context.activity, loaded_files, dist_hash
            )


def builtin__import__patch(orig_builtin__import__, patch_policy, *args, **kwargs):
    req_context = contrast.CS__CONTEXT_TRACKER.current()
    name = None

    if len(args) > 0:
        name = args[0]

    with scope.contrast_scope():
        possible_sys_module_keys = None

        # We only support reporting this information in the context of a request.
        # Verify we can get request context before doing any processing
        perform_analysis = req_context and name and not name.startswith("contrast")

        if perform_analysis:
            (
                perform_analysis,
                possible_sys_module_keys,
                before_import_sys_modules,
            ) = pre__import__analysis(*args, **kwargs)

    # Don't perform import in contrast scope because there may be analysis we can do during
    # import (i.e first time executing + caching the module)
    result = orig_builtin__import__(*args, **kwargs)

    with scope.contrast_scope():
        if perform_analysis:
            post__import__analysis(
                req_context, before_import_sys_modules, possible_sys_module_keys
            )

        return result


def patch_import(builtins_module):
    patch_cls_or_instance(builtins_module, "__import__", builtin__import__patch)


def register_patches():
    register_post_import_hook(patch_import, builtins.__name__)
