# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os

import pytest

from contrast.test.apptest.base_django_test import BaseDjangoTest
from contrast.test.apptest_utils import assert_subprocess_popen_finding_events
from contrast.test.contract.findings import (
    validate_finding_in_context,
    validate_ssrf_finding_no_mock,
)
from contrast.test.helper import python2_only


class VulnpyAssessTestMixin(object):
    @pytest.mark.parametrize("trigger", ["os-system", "subprocess-popen"])
    def test_cmdi(self, trigger):
        user_input = "echo attack"
        self.client.get("/vulnpy/cmdi/{}".format(trigger), {"user_input": user_input})

        validate_finding_in_context(self.request_context, "cmd-injection")

        if (
            isinstance(self, BaseDjangoTest)
            and trigger == "subprocess-popen"
            and not os.environ.get("USE_DJANGO_WSGI")  # TODO: PYT-1102
        ):
            assert_subprocess_popen_finding_events(
                self.request_context.activity.findings
            )

    @pytest.mark.parametrize(
        "trigger", ["pickle-load", "pickle-loads", "yaml-load", "yaml-load-all"]
    )
    def test_untrusted_deserialization(self, trigger):
        user_input = "some data to deserialize"
        try:
            self.client.get(
                "/vulnpy/deserialization/{}".format(trigger), {"user_input": user_input}
            )
        except Exception:
            # this view function doesn't handle its own errors, so we do it here
            pass

        validate_finding_in_context(self.request_context, "untrusted-deserialization")

    @pytest.mark.parametrize("trigger", ["io-open", "open"])
    def test_path_traversal(self, trigger):
        user_input = "does not matter"
        self.client.get("/vulnpy/pt/{}/".format(trigger), {"user_input": user_input})

        validate_finding_in_context(self.request_context, "path-traversal")

    @python2_only
    @pytest.mark.xfail(
        os.environ.get("USE_DJANGO_WSGI") is not None, reason="TODO: PYT-1096"
    )
    def test_path_traversal_execfile(self):
        user_input = "does not matter"
        self.client.get("/vulnpy/pt/execfile/", {"user_input": user_input})

        validate_finding_in_context(self.request_context, "path-traversal")

    @pytest.mark.parametrize(
        "trigger", ["sqlite3-execute", "sqlite3-executemany", "sqlite3-executescript"]
    )
    def test_sqli(self, trigger):
        user_input = "any value works"
        self.client.get(
            "/vulnpy/sqli/{}".format(trigger), params={"user_input": user_input}
        )

        # 3 queries per vulnpy request: database reset, attack, fetch results
        assert self.request_context.activity.query_count == 3
        validate_finding_in_context(self.request_context, "sql-injection")

    @pytest.mark.parametrize(
        "trigger", ["legacy-urlopen", "urlopen-str", "urlopen-obj"]
    )
    @pytest.mark.parametrize("safe", [False, True])
    def test_ssrf_urllib(self, trigger, safe):
        user_input = "not.a.url" if safe else "http://attacker.com/?q=foobar"
        self.client.get("/vulnpy/ssrf/{}".format(trigger), {"user_input": user_input})

        if not safe:
            validate_ssrf_finding_no_mock(trigger, self.request_context)
        else:
            assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("trigger_class", ["httpconnection", "httpsconnection"])
    @pytest.mark.parametrize(
        "trigger_method", ["request-method", "putrequest-method", "init"]
    )
    def test_ssrf_httplib(self, trigger_method, trigger_class):
        trigger = "-".join([trigger_class, trigger_method])
        user_input = "www.attacker.com" if trigger_method == "init" else "DELETE"
        self.client.get("/vulnpy/ssrf/{}".format(trigger), {"user_input": user_input})

        validate_ssrf_finding_no_mock(trigger, self.request_context)

    @pytest.mark.parametrize("trigger_class", ["httpconnection", "httpsconnection"])
    @pytest.mark.parametrize("trigger_method", ["request", "putrequest"])
    def test_ssrf_httplib_safe(self, trigger_method, trigger_class):
        """
        HTTP*Connection.*request isn't vulnerable to SSRF via the "url" argument.
        This is because it only takes a path / querystring, which isn't vulnerable
        to ssrf.
        """
        trigger = "-".join([trigger_class, trigger_method, "url"])
        self.client.get("/vulnpy/ssrf/{}".format(trigger), {"user_input": "/some/path"})

        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("trigger", ["random", "randint", "randrange", "uniform"])
    def test_weak_randomness(self, trigger):
        user_input = "abc123"
        self.client.get("/vulnpy/rand/{}".format(trigger), {"user_input": user_input})

        validate_finding_in_context(
            self.request_context, "crypto-weak-randomness", nondataflow=True
        )

    @pytest.mark.parametrize("trigger", ["hashlib-md5", "hashlib-sha1", "hashlib-new"])
    def test_insecure_hash(self, trigger):
        user_input = "def456"
        self.client.get("/vulnpy/hash/{}".format(trigger), {"user_input": user_input})

        validate_finding_in_context(
            self.request_context, "crypto-bad-mac", nondataflow=True
        )

    @pytest.mark.parametrize("trigger", ["exec", "eval", "compile"])
    def test_untrusted_code_exec(self, trigger):
        user_input = "1 + 2 + 3"
        self.client.get(
            "/vulnpy/unsafe_code_exec/{}".format(trigger), {"user_input": user_input}
        )

        validate_finding_in_context(self.request_context, "unsafe-code-execution")

    def test_raw_xss(self):
        user_input = "im an attack!"
        self.client.get("/vulnpy/xss/raw", {"user_input": user_input})

        validate_finding_in_context(self.request_context, "reflected-xss")

    @pytest.mark.parametrize(
        "trigger",
        ["xml-dom-pulldom-parsestring", "lxml-etree-fromstring", "xml-sax-parsestring"],
    )
    def test_xxe(self, trigger):
        param_val = "<root>attack</root>"
        self.client.get("/vulnpy/xxe/{}".format(trigger), {"user_input": param_val})

        validate_finding_in_context(self.request_context, "xxe")
