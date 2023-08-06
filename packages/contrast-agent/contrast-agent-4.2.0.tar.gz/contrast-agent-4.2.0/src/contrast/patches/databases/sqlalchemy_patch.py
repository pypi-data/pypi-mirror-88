# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.patches.databases import dbapi2
from contrast.extern.wrapt import register_post_import_hook
from contrast.agent.policy import patch_manager

ENGINE_BASE_MODULE = "sqlalchemy.engine.base"


def patch_sqlalchemy_base_execute(sqlalchemy_engine_base):
    dbapi2._instrument_cursor_method(
        ENGINE_BASE_MODULE, sqlalchemy_engine_base.Connection, "execute"
    )


def register_patches():
    register_post_import_hook(patch_sqlalchemy_base_execute, ENGINE_BASE_MODULE)


def reverse_patches():
    base_module = sys.modules.get(ENGINE_BASE_MODULE)
    if base_module:
        patch_manager.reverse_patches_by_owner(base_module.Connection)
