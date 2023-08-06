# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.extern.wrapt import register_post_import_hook
from contrast.agent import scope
from contrast.agent.policy import patch_manager
from contrast.agent.assess.utils import copy_from, track_string

from contrast.utils.patch_utils import patch_cls_or_instance

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")

SAFESTRING_MODULE_NAME = "django.utils.safestring"
MARK_SAFE_NAME = "mark_safe"


def _get_source(args, kwargs):
    if args:
        return args[0]
    if kwargs:
        return kwargs.get("s")
    return None


def mark_safe_patch(orig_func, patch_policy, *args, **kwargs):
    """
    This patch implements a more optimized "deadzoned" original mark_safe call.

    We are deadzoning calling the original mark_safe because it may call SafeText,
    a class that inherits from str and that ends up propagating excessively.

    Because mark_safe is called many times when Django renders a template,
    excessive propagation is incredibly costly. So instead, we do the same work as
    the KEEP propagator would, but with a deadzoned call to the original function.
    """
    # if we're already in scope, don't bother doing any analysis
    if scope.in_scope():
        return orig_func(*args, **kwargs)

    # if we're not yet in scope, call orig_func and analysis in scope
    with scope.contrast_scope():
        # We don't wrap orig_func call in try/catch because if it raises an error
        # we don't want to do any analysis.
        result = orig_func(*args, **kwargs)

        try:
            logger.debug("Analyzing in %s custom propagator.", MARK_SAFE_NAME)
            source = _get_source(args, kwargs)
            track_string(result)
            copy_from(result, source)
        except Exception as e:
            logger.debug(
                "Failed to analyse in %s propagator. %s", MARK_SAFE_NAME, str(e)
            )

    return result


def patch_django(safestring_module):
    patch_cls_or_instance(safestring_module, MARK_SAFE_NAME, mark_safe_patch)


def register_patches():
    register_post_import_hook(patch_django, SAFESTRING_MODULE_NAME)


def reverse_patches():
    safestring_module = sys.modules.get(SAFESTRING_MODULE_NAME)
    if not safestring_module:
        return

    patch_manager.reverse_patches_by_owner(safestring_module)
