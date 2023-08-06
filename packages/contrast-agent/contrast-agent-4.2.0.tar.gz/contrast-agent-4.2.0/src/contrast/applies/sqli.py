# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Rule applicator for SQLi for dbapi2-compliant modules
"""
import contrast
from contrast.agent import scope
from contrast.agent.protect.rule.sqli_rule import SqlInjection
from contrast.agent.policy.loader import Policy
from contrast.agent.assess.policy.utils import skip_analysis
from contrast.agent.assess.policy.trigger_policy import TriggerPolicy
from contrast.agent.settings_state import SettingsState
from contrast.applies import (
    DATABASE_SQLITE,
    DATABASE_CASSANDRA,
    DATABASE_PG,
    DATABASE_MYSQL,
    DATABASE_SQL_ALCHEMY,
)
from contrast.utils.decorators import fail_safely


# This represents a map of adapters (modules) to underlying db technologies
# The adapter name is used for policy lookup/trace reporting purposes, but the
# technology name is used for inventory reporting.
ADAPTER_TO_DATABASE = {
    "sqlite3": DATABASE_SQLITE,
    "pysqlite2.dbapi2": DATABASE_SQLITE,
    "pycassa": DATABASE_CASSANDRA,
    "psycopg2": DATABASE_PG,
    "pymysql": DATABASE_MYSQL,
    "sqlalchemy.engine.base": DATABASE_SQL_ALCHEMY,
}


@fail_safely("Error running SQLi assess rule")
def assess_rule(context, adapter, method, result, args, kwargs):
    """
    Apply assess SQLi rule

    @param context: Current RequestContext instance
    @param adapter: String representing the adapter module (e.g. "sqlite3")
    @param method: String representing the database method (e.g. "execute")
    @param result: Object representing result of database action
    @param args: The args tuple passed to the original database function
    @param kwargs: The kwargs dict passed to the original database function
    """
    if scope.in_trigger_scope():
        return

    context.activity.query_count += 1

    policy = Policy()

    rule = policy.triggers["sql-injection"]
    trigger_nodes = rule.find_trigger_nodes("{}.Cursor".format(adapter), method)

    modified_args, modified_kwargs = _convert_query_to_string(
        trigger_nodes, args, kwargs
    )

    with scope.trigger_scope():
        TriggerPolicy.apply(rule, trigger_nodes, result, modified_args, modified_kwargs)


def apply_rule(adapter, method, orig_func, args, kwargs):
    """
    Common API for applying SQLi rule (applies both protect and assess rules)

    Applies the assess rule if assess is enabled. If protect is enabled,
    applies the protect rule. Important caveats:
      - neither rule will be applied if there is not an active request context
      - the assess rule will not be applied if we are already in scope

    The protect rule *must* be applied prior to calling the original function.
    This is the only way that we can raise a SecurityException if the rule is
    in BLOCK mode.

    The assess rule *must* be applied even if the original function results in
    an exception. Otherwise we won't detect vulnerable dataflows that may have
    just happened to result in an exception under testing.

    @param adapter: String representing the adapter (e.g. "sqlite3")
    @param method: String representing the database method (e.g. "execute")
    @param orig_func: Original function (i.e. the one replaced by the patch)
    @param *args: The *args passed to the original database function
    @param **kwargs: The **kwargs passed to the original database function

    @return: Returns the object that is returned by calling orig_func
    """
    context = contrast.CS__CONTEXT_TRACKER.current()

    if context is not None:
        _protect_rule(context, adapter, method, args, kwargs)

    try:
        result = orig_func(*args, **kwargs)
    except Exception:
        result = None
        raise
    finally:
        if not skip_analysis(context):
            assess_rule(context, adapter, method, result, args, kwargs)

    return result


@fail_safely("Error running SQLi protect rule")
def _protect_rule(context, adapter, method, args, kwargs):
    """
    Run protect SQLi analysis if it's enabled.
    """
    if not SettingsState().is_protect_enabled() or len(args) <= 1:
        return

    # args[0] is self, args[1] is the query
    sql = _get_query_as_string(args[1])

    database = ADAPTER_TO_DATABASE.get(adapter, adapter)

    # TODO: PYT-986: remove creating fake policy node and patch loc policy
    from contrast.agent.policy.patch_location_policy import PatchLocationPolicy
    from contrast.agent.policy.trigger_node import TriggerNode

    trigger_node = TriggerNode(database, "unused", True, method, "ARG_0")
    patch_policy = PatchLocationPolicy(trigger_node)

    rule = SettingsState().defend_rules.get(SqlInjection.NAME)
    rule.protect(patch_policy, sql, args, kwargs)


def _convert_query_to_string(trigger_nodes, args, kwargs):
    """
    Make the query a string - necessary for SQLAlchemy. Returns modified copies
    of args and kwargs to be used for reporting.
    """
    if len(trigger_nodes) != 1:
        return args, kwargs

    modified_args = list(args)
    modified_kwargs = dict(kwargs)

    sources = trigger_nodes[0].sources

    for source in sources:
        if isinstance(source, int) and len(modified_args) < source:
            modified_args[source] = _get_query_as_string(args[source])
            break
        elif isinstance(source, str) and source in modified_kwargs:
            modified_kwargs[source] = _get_query_as_string(kwargs[source])
            break

    return tuple(modified_args), modified_kwargs


def _get_query_as_string(query):
    """
    SQLAlchemy queries are sometimes passed in as a special TextClause type.
    For our analysis to succeed, we need this value to be a string. This function
    extracts the raw string if necessary.

    It's possible that in the future we may need to expand on this method;
    alternatively, if we find different (better) triggers in SQLAlchemy, we
    may be able to remove this.
    """
    return getattr(query, "text", None) or query
