# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy import constants
from contrast.agent.policy.policy_node import PolicyNode


class DeadZoneNode(PolicyNode):
    def __init__(
        self, module, class_name, method_name, instance_method=True,
    ):
        super(DeadZoneNode, self).__init__(
            module=module,
            class_name=class_name,
            method_name=method_name,
            instance_method=instance_method,
        )

    @staticmethod
    def from_dict(obj):
        return DeadZoneNode(
            obj[constants.JSON_MODULE],
            obj.get(constants.JSON_CLASS_NAME, ""),
            obj[constants.JSON_METHOD_NAME],
            obj.get(constants.JSON_INSTANCE_METHOD, True),
        )
