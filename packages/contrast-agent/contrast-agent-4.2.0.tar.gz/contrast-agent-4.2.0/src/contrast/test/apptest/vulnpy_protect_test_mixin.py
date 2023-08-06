# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import pytest

from contrast.agent.middlewares.base_middleware import BaseMiddleware
from contrast.api.dtm_pb2 import UserInput
from contrast.api.settings_pb2 import (
    AgentSettings,
    InputAnalysis,
    InputAnalysisResult,
    ProtectState,
)
from contrast.extern import six


class _MockedInputAnalysisMixin(object):
    def mock_input_analysis(self, mocker, rule_id, attack, security_exception=False):
        """
        Assemble a fake response for speedracer's input analysis, then mock
        communication with speedracer during input analysis to return this response.
        """
        fake_state = ProtectState(
            uuid="012345678987654",
            track_request=True,
            security_exception=security_exception,
        )
        fake_result = InputAnalysisResult(
            rule_id=rule_id,
            value=attack,
            path="user_input",
            key="user_input",
            input_type=UserInput.PARAMETER_VALUE,
            score_level=InputAnalysisResult.DEFINITEATTACK,
            ids=[],
        )
        fake_analysis = InputAnalysis(results=[fake_result])
        fake_response = AgentSettings(
            protect_state=fake_state, input_analysis=fake_analysis
        )
        mocker.patch(
            "contrast.agent.speedracer_input_analysis.service_client.send_messages_get_responses",
            return_value=[fake_response],
        )

    @pytest.mark.parametrize(
        "trigger", ["sqlite3-execute", "sqlite3-executemany", "sqlite3-executescript"]
    )
    def test_sqli(self, trigger, mocker):
        rule_id = "sql-injection"
        attack = "foo' OR 1=1; DROP TABLE Users--"
        self.mock_input_analysis(mocker, rule_id, attack)

        response = self.client.get(
            "/vulnpy/sqli/{}".format(trigger), {"user_input": attack}, status=403
        )

        # 3 queries per vulnpy request: database reset, attack, fetch results
        # we skip the last one here because the second causes a SecurityException
        assert self.request_context.activity.query_count == 2
        self.assert_blocked(response, rule_id)

    @pytest.mark.parametrize("trigger", ["io-open", "open"])
    def test_path_traversal(self, trigger, mocker):
        rule_id = "path-traversal"
        attack = "../../../../etc/passwd"
        self.mock_input_analysis(mocker, rule_id, attack)

        response = self.client.get(
            "/vulnpy/pt/{}".format(trigger), {"user_input": attack}, status=403,
        )

        self.assert_blocked(response, rule_id)

    def test_xss(self, mocker):
        """
        XSS is BAP only - we need SR to tell us to raise a security exception
        """
        rule_id = "reflected-xss"
        attack = "<script>alert(1);</script>"
        self.mock_input_analysis(mocker, rule_id, attack, security_exception=True)

        response = self.client.get(
            "/vulnpy/xss/raw", {"user_input": attack}, status=403,
        )

        self.assert_blocked(response, rule_id)

    @pytest.mark.parametrize(
        "trigger",
        [
            "legacy-urlopen",
            "urlopen-str",
            "httpconnection-putrequest-method",
            "httpsconnection-putrequest-method",
            "httpconnection-request-method",
            "httpsconnection-request-method",
        ],
    )
    def test_ssrf(self, trigger, mocker):
        """
        This attack vector doesn't really make sense with the `-method` triggers.
        However, we wouldn't flag something like BADVERB as an attack, so this is
        probably still the most realistic scenario.
        """
        rule_id = "ssrf"
        attack = "http://www.attacker.com/evil"
        self.mock_input_analysis(mocker, rule_id, attack)

        response = self.client.get(
            "/vulnpy/ssrf/{}".format(trigger), {"user_input": attack}, status=403,
        )

        self.assert_blocked(response, rule_id)

    @pytest.mark.parametrize(
        "trigger",
        [
            "httpconnection-putrequest-url",
            "httpsconnection-putrequest-url",
            "httpconnection-request-url",
            "httpsconnection-request-url",
        ],
    )
    def test_ssrf_safe(self, trigger, mocker):
        """
        For assess, labs determined that the URL itself (without protocol/host)
        isn't vulnerable to SSRF. We extended this logic to protect.
        """
        attack = "http://www.attacker.com/evil"
        self.mock_input_analysis(mocker, "ssrf", attack)

        self.client.get(
            "/vulnpy/ssrf/{}".format(trigger), {"user_input": attack}, status=200,
        )

    def test_unsafe_file_upload(self, mocker):
        """
        This test doesn't prove much, for now. It's more of a placeholder for when
        we start using a real connection to the service.
        """
        rule_id = "unsafe-file-upload"
        attack = "some_dangerous_file.php"
        self.mock_input_analysis(mocker, rule_id, attack, security_exception=True)

        response = self.client.post(
            "/vulnpy",
            upload_files=[("user_file", attack, b"file content doesn't matter")],
            status=403,
        )

        self.assert_blocked(response, rule_id)

    @pytest.mark.parametrize(
        "attack",
        [
            # a word of caution: these execute for real on your machine
            "grep 'passwd' && echo",
            "echo a | boom",
            "/bin/sh -c ls -al; cat /etc/passwd",
        ],
    )
    @pytest.mark.parametrize("trigger", ["subprocess-popen", "os-system"])
    def test_cmdi_command_backdoor_disabled(self, trigger, attack, mocker):
        """
        Here's a really interesting case - which directly tests CMDi REP
        detect_chained_commands. The input analysis is for CMDi, but a totally
        different string. However, we run detect_chained_commands on the
        string that makes it to the trigger as long as there is at least one
        evaluation result for cmd-injection.
        """
        self.settings.config.put(
            "protect.rules.cmd-injection.detect_parameter_command_backdoors", False
        )

        rule_id = "cmd-injection"
        self.mock_input_analysis(mocker, rule_id, "a totally unrelated string")

        response = self.client.get(
            "/vulnpy/cmdi/{}".format(trigger),
            {"user_input": "grep 'passwd' && echo"},
            status=403,
        )

        self.assert_blocked(response, rule_id)

    @pytest.mark.parametrize("trigger", ["subprocess-popen", "os-system"])
    def test_cmdi_command_backdoor_disabled_safe(self, trigger, mocker):
        """
        Same as above, but without malicious input; leads to 200 instead of 403.
        """
        self.settings.config.put(
            "protect.rules.cmd-injection.detect_parameter_command_backdoors", False
        )

        self.mock_input_analysis(mocker, "cmd-injection", "a totally unrelated string")

        self.client.get(
            "/vulnpy/cmdi/{}".format(trigger),
            {"user_input": "harmless input"},
            status=200,
        )


class _NoInputAnalysisMixin(object):
    @pytest.mark.parametrize("trigger", ["subprocess-popen", "os-system"])
    def test_cmdi_command_backdoor_no_input_analysis(self, trigger):
        """
        When an argument to a CMDi trigger matches an HTTP parameter, the
        agent detects a "command backdoor" and blocks. This occurs even
        without input analysis from speedracer.
        """
        attack = "interestingly this does not matter"
        response = self.client.get(
            "/vulnpy/cmdi/{}".format(trigger), {"user_input": attack}, status=403
        )

        self.assert_blocked(response, "cmd-injection")

    @pytest.mark.parametrize("trigger", ["subprocess-popen", "os-system"])
    def test_cmdi_command_backdoor_disabled_no_input_analysis(self, trigger):
        """
        With no input analysis AND command backdoors disabled, even real attacks
        will not lead to a 403 response.
        """
        self.settings.config.put(
            "protect.rules.cmd-injection.detect_parameter_command_backdoors", False
        )

        attack = "grep 'passwd' && echo"
        self.client.get(
            "/vulnpy/cmdi/{}".format(trigger), {"user_input": attack}, status=200
        )

    @pytest.mark.parametrize(
        "trigger", ["yaml-load", "yaml-load-all", "pickle-load", "pickle-loads"]
    )
    @pytest.mark.parametrize(
        "attack",
        [
            '!!map { ? !!str "goodbye" : !!python/object/apply:subprocess.check_output [ !!str "ls", ], }',
            "cos system (S'/bin/sh' tR.",
        ],
    )
    def test_deserialization_no_input_analysis(self, trigger, attack):
        """
        Both deserialization triggers (yaml and pickle) check for attacks that would only work
        against specific triggers. It's possible that in the future we may want to make this
        more specific. However, for now we're free to mix and match attacks and triggers.
        """
        response = self.client.get(
            "/vulnpy/deserialization/{}".format(trigger),
            {"user_input": attack},
            status=403,
        )

        self.assert_blocked(response, "untrusted-deserialization")

    @pytest.mark.parametrize(
        "trigger",
        ["lxml-etree-fromstring", "xml-dom-pulldom-parsestring", "xml-sax-parsestring"],
    )
    def test_xxe_no_input_analysis(self, trigger):
        """
        This particular attack is designed to work against lxml specifically.
        However, all 3 XXE triggers will still see this as an attack.
        """
        attack = (
            '<!DOCTYPE doc [ <!ENTITY lxml SYSTEM file:///etc/passwd"> ]>\n'
            "<root>\n"
            "<element>&lxml;</element>\n"
            "</root>\n"
        )
        response = self.client.get(
            "/vulnpy/xxe/{}".format(trigger), {"user_input": attack}, status=403,
        )

        self.assert_blocked(response, "xxe")

    @pytest.mark.parametrize(
        "attack", ["../../../../etc/passwd", "super/duper/../../etc/hosts", "::$DATA"],
    )
    @pytest.mark.parametrize("trigger", ["io-open", "open"])
    def test_path_traversal_no_input_analysis_unsafe(self, trigger, attack):
        response = self.client.get(
            "/vulnpy/pt/{}".format(trigger), {"user_input": attack}, status=403,
        )

        self.assert_blocked(response, "path-traversal")

    @pytest.mark.parametrize("trigger", ["io-open", "open"])
    def test_path_traversal_no_input_analysis_safe(self, trigger):
        self.client.get(
            "/vulnpy/pt/{}".format(trigger), {"user_input": "normal"}, status=200,
        )


class VulnpyProtectTestMixin(_MockedInputAnalysisMixin, _NoInputAnalysisMixin):
    def assert_blocked(self, response, rule_id):
        assert response.status_int == 403
        assert six.ensure_str(response.body) == BaseMiddleware.OVERRIDE_MESSAGE
        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].rule_id == rule_id
