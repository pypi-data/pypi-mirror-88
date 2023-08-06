# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.service_client import send_messages
from contrast.agent.assess.rules.base_rule import BaseRule
from contrast.api import Finding
from contrast.api.dtm_pb2 import Activity


class StaticRule(BaseRule):
    """
    Base class for provider and config-based rules

    These kinds of rules send their findings immediately rather than relying on a
    request context.
    """

    def build_and_send_finding(self, properties, **kwargs):
        finding_msg = Finding(self, properties, **kwargs).get_finding_msg()
        finding_msg.version = Finding.pick_version(finding_msg)

        activity = Activity()
        activity.findings.extend([finding_msg])

        send_messages([activity])
