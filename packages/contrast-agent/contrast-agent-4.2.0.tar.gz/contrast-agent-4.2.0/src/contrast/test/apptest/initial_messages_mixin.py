# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast


class InitialMsgsTestMixin(object):
    def test_initial_msgs(self, mocker):
        self.client.get("/", status="*")

        # send_dtm is the last mock mocker created in disable_service_client
        send_dtm_mock = mocker._mocks[-1]

        initial_messages = send_dtm_mock.call_args_list[:2]

        first_msg = initial_messages[0][0][0]
        assert first_msg.app_name == "root"
        assert first_msg.app_language == "Python"
        assert first_msg.app_path == "/app-path"

        agent_startup = first_msg.agent_startup
        app_create = initial_messages[1][0][0].application_create

        assert agent_startup.version == contrast.__version__
        assert agent_startup.server_version == contrast.__version__

        assert agent_startup.server_name == "test_server_name"
        assert agent_startup.server_path == "/test/server/path"
        assert agent_startup.server_tags == "some_test_server_tag"
        assert agent_startup.application_tags == "some_test_application_tag"
        assert agent_startup.library_tags == "some_test_library_tag"
        assert agent_startup.finding_tags == "some_test_assess_tag"

        assert app_create.group == "some_test_group"
        assert app_create.app_version == "some_test_version"
        assert app_create.code == "some_test_application_code"
