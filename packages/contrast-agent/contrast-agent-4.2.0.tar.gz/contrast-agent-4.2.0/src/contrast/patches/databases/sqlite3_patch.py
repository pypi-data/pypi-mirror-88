# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.wrapt import register_post_import_hook
import sys
import contrast
from contrast.agent.policy import patch_manager
from contrast.patches.databases import dbapi2
from contrast.utils import inventory_utils
from contrast.utils.patch_utils import patch_cls_or_instance

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


SQLITE3 = "sqlite3"
PYSQLITE2_DBAPI2 = "pysqlite2.dbapi2"
VENDOR = "SQLite3"


def patch_connect(module):
    def _connect(orig_func, patch_policy=None, *args, **kwargs):
        """Record DB inventory for SQLite3 connection"""
        try:
            context = contrast.CS__CONTEXT_TRACKER.current()
            if context is not None:
                # sqlite does not use a server, so no need for host/port
                database = kwargs.get("database") or (
                    args[0] if len(args) > 0 else "unknown"
                )
                db_inventory = dict(vendor=VENDOR, database=database)
                inventory_utils.append_db(context.activity, db_inventory)
        except Exception:
            logger.exception("Failed to add inventory for %s", VENDOR)

        return orig_func(*args, **kwargs)

    patch_cls_or_instance(module, "connect", _connect)


def instrument_sqlite_dbapi2(sqlite3):
    dbapi2.instrument_cursor(SQLITE3, sqlite3.Cursor)
    dbapi2.instrument_executescript(SQLITE3, sqlite3.Cursor)
    patch_connect(sqlite3)


def instrument_pysqlite2_dbapi2(pysqlite2):
    """Supports the older pysqlite module in Py2"""
    dbapi2.instrument_cursor(PYSQLITE2_DBAPI2, pysqlite2.Cursor)
    dbapi2.instrument_executescript(PYSQLITE2_DBAPI2, pysqlite2.Cursor)
    patch_connect(pysqlite2)


def register_patches():
    register_post_import_hook(instrument_sqlite_dbapi2, SQLITE3)
    register_post_import_hook(instrument_pysqlite2_dbapi2, PYSQLITE2_DBAPI2)


def reverse_patches():
    sqlite3 = sys.modules.get(SQLITE3)
    if sqlite3:
        patch_manager.reverse_patches_by_owner(sqlite3)
        patch_manager.reverse_patches_by_owner(sqlite3.Cursor, force=True)

    psqlite = sys.modules.get(PYSQLITE2_DBAPI2)
    if psqlite:
        patch_manager.reverse_patches_by_owner(psqlite)
        patch_manager.reverse_patches_by_owner(psqlite.Cursor, force=True)
