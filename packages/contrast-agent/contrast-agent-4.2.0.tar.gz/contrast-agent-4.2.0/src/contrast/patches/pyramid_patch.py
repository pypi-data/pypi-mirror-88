# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

import contrast
from contrast.extern.wrapt import register_post_import_hook
from contrast.agent.assess.policy.utils import perform_analysis
from contrast.agent.policy import patch_manager
from contrast.agent.policy.applicator import apply_assess_patch
from contrast.agent.policy.loader import Policy
from contrast.utils.decorators import fail_safely
from contrast.utils.patch_utils import patch_cls_or_instance


@fail_safely("Failed to apply policy to new session class")
def _apply_policy(session_cls):
    policy = Policy()

    for patch_policy in policy.policy_by_module["pyramid.session"]:
        if patch_policy.class_name == "CookieSession":
            apply_assess_patch(session_cls, patch_policy)


@fail_safely("Failed to apply assess policy for BaseCookieSessionFactory")
def _apply_assess(result, args, kwargs):
    context = contrast.CS__CONTEXT_TRACKER.current()

    policy = Policy()
    patch_policy = policy.policy_by_name["pyramid.session.BaseCookieSessionFactory"]

    perform_analysis(context, patch_policy, result, args, kwargs)


def BaseCookieSessionFactory(orig_func, patch_policy, *args, **kwargs):
    """
    BaseCookieSessionFactory is a function that returns a new CookieSession class

    Since we can't instrument the new class directly using normal policy machinery, we
    instead apply our policy on-demand to the newly created class.
    """
    session_cls = None

    try:
        session_cls = orig_func(*args, **kwargs)
        _apply_policy(session_cls)
    finally:
        _apply_assess(session_cls, args, kwargs)

    return session_cls


def patch_pyramid(pyramid_session):
    patch_cls_or_instance(
        pyramid_session, "BaseCookieSessionFactory", BaseCookieSessionFactory
    )


def register_patches():
    register_post_import_hook(patch_pyramid, "pyramid.session")


def reverse_patches():
    pyramid_session = sys.modules.get("pyramid.session")
    if not pyramid_session:
        return

    patch_manager.reverse_patches_by_owner(pyramid_session)
