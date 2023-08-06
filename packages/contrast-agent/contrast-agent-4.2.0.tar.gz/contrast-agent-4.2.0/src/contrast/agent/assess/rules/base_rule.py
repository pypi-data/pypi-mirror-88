# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.settings_state import SettingsState
from contrast.utils.digest_utils import Digest

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


class BaseRule(object):
    """
    Base rule object that all assess rules will inherit
    """

    @property
    def name(self):
        return "assess-base-rule"

    @property
    def disabled(self):
        """
        Property indicating whether rule is disabled
        """
        return SettingsState().is_assess_rule_disabled(self.name)

    def add_events_to_finding(self, finding, events=None, **kwargs):
        if events is not None:
            finding.events.extend(events)

    def generate_preflight_hash(self, **kwargs):
        hasher = Digest()
        hasher.update(self.name)

        self.update_preflight_hash(hasher, **kwargs)

        return hasher.finish()

    def update_preflight_hash(self, hasher, **kwargs):
        """
        Update preflight hash with additional rule-specific data

        Child classes should override this method in order to customize the
        kind of data that is used to generate the preflight hash.

        @param hasher: Hash class to be updated with additional data
        @param **kwargs: Placeholder for keyword args used by child classes
        """
        raise NotImplementedError
