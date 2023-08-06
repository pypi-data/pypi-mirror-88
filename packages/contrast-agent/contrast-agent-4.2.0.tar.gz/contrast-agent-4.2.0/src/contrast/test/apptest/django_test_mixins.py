# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
# pylint: disable=too-many-lines
import copy
import os
import six  # pylint: disable=did-not-import-extern

import pytest
from app import settings
from app.urls import urlpatterns

import django
from django.utils.html import escape
from contrast.agent.protect.rule.deserialization_rule import Deserialization
from contrast.api.dtm_pb2 import AttackResult, ObservedRoute
from contrast.api.settings_pb2 import ProtectionRule
from contrast.test import mocks

from contrast.test.library_analysis import (
    assert_files_loaded,
    import_sample_package_onefile,
    TEST_MODULES_RELATIVE_IMPORT_DIST,
    TEST_MODULES_NAMESPACE_DIST,
    TEST_MODULE_ONEFILE,
    TEST_MODULES_MULTIPLE_TLDS_DIST,
)

from contrast.test.contract.findings import (
    assert_event_sources,
    param_is_tracked,
    validate_finding,
    validate_any_finding,
    validate_source_finding,
    validate_header_sources,
    validate_cookies_sources,
    validate_nondataflow_finding,
    validate_ssrf_finding,
)
from contrast.test.apptest_utils import (
    assert_route_appended,
    assert_routes_count,
    current_routes_by_url,
    validate_observed_route,
    assert_subprocess_popen_finding_events,
)

from contrast.test.helper import (
    mock_build_update_messages,
    mock_send_messages,
    python2_only,
)
from contrast.test.mongo import skip_no_mongo_db

from vulnpy.trigger import sqli

URLPATTERNS_COPY = copy.copy(urlpatterns)
DATA_DIR = os.path.join(settings.BASE_DIR, os.pardir, "data")


SOURCE_OPTIONS = (
    "parameter",
    "host",
    "port",
    "raw_uri",
    "scheme",
    "referer_header",
)

# full_path_info is only in newer versions of django.
# We do not test full_path* for POST requests since in this case the path does not contain
# a query, and so the entire path is actually sanitized.
GET_SOURCES = (
    SOURCE_OPTIONS
    + ("full_path",)
    + (("full_path_info",) if django.VERSION >= (2, 1) else ())
)
POST_SOURCES = ("files", "body",) + SOURCE_OPTIONS


class DjangoTestLibraryAnalysisBuiltinImport(object):
    def test_relative_import_hook(self):
        response = self.client.get(
            "/import_package_with_relative_imports/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(
            self.request_context.activity, TEST_MODULES_RELATIVE_IMPORT_DIST
        )

    def test_namespace_sample_package_import_hook(self):
        response = self.client.get(
            "/import_namespace_package/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(self.request_context.activity, TEST_MODULES_NAMESPACE_DIST)

    def test_module_import_onefile(self):
        response = self.client.get(
            "/import_package_onefile/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(self.request_context.activity, TEST_MODULE_ONEFILE)

    def test_sample_module_multiple_tlds(self):
        response = self.client.get(
            "/import_sample_dist_multiple_tlds/", {"rm_sys_mod_entries": 1}
        )

        assert response.status_code == 200

        assert_files_loaded(
            self.request_context.activity, TEST_MODULES_MULTIPLE_TLDS_DIST
        )

    def test_module_already_imported(self):
        import_sample_package_onefile()

        response = self.client.get("/import_package_onefile/")

        assert response.status_code == 200

        assert len(self.request_context.activity.library_usages) == 0


class DjangoProtectNoSqliTestMixin(object):
    """
    Screener does not currently test nosqli protect so we test it more thoroughly.
    """

    def make_nosqli_request(self, method, param_val, with_kwarg):
        self.client.post(
            "/nosqli/",
            {
                "user_input": param_val,
                "method_to_test": method,
                "with_kwarg": with_kwarg,
            },
            status=403,
        )

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_find_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = "Record One"

        self.make_nosqli_request("find", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 1

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_insert_one_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = '{"title": "Record One"}'

        self.make_nosqli_request("insert_one", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 1

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_insert_many_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = "Record One"

        self.make_nosqli_request("insert_many", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 1

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_update_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = "Record One"

        self.make_nosqli_request("update", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 2

    @skip_no_mongo_db
    @mocks.nosqli_input_analysis_mock
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_delete_blocked(self, mocked_input_analysis, with_kwarg):
        param_val = "Record One"

        self.make_nosqli_request("delete", param_val, with_kwarg)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "nosql-injection"
        assert self.request_context.activity.query_count == 1


class DjangoProtectTestMixinBlock(DjangoProtectNoSqliTestMixin):
    """
    Provides test cases to be used across all django protect apptests
    """

    PROTECT_RULES_MODE_BLOCK = [
        {
            "id": "cmd-injection",
            "name": "Command Injection",
            "mode": ProtectionRule.BLOCK,
        },
        {
            "id": "path-traversal",
            "name": "Path Traversal",
            "mode": ProtectionRule.BLOCK,
        },
        {
            "mode": ProtectionRule.BLOCK,
            "id": Deserialization.NAME,
            "name": "Untrusted Deserialization",
        },
        {"id": "nosql-injection", "name": "NosQLI", "mode": ProtectionRule.BLOCK},
    ]

    @pytest.mark.parametrize("path", ["os-system", "subprocess-popen"])
    def test_cmdi(self, path):
        self.client.get(
            "/vulnpy/cmdi/{}".format(path),
            {"user_input": "; echo /etc/passwd | nc"},
            status=403,
        )
        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert self.request_context.activity.results[0].rule_id == "cmd-injection"

    @pytest.mark.parametrize("method_name", ["get", "post"])
    @pytest.mark.parametrize("trigger", ["pickle-load", "pickle-loads"])
    def test_pickle(self, trigger, method_name):
        param_val = "csubprocess\ncheck_output\n(S'ls'\ntR."

        params = dict(user_input=param_val)
        method = getattr(self.client, method_name)

        method("/vulnpy/deserialization/{}".format(trigger), params, status=403)

        assert len(self.request_context.activity.results) == 1
        assert self.request_context.activity.results[0].response == AttackResult.BLOCKED
        assert (
            self.request_context.activity.results[0].rule_id
            == "untrusted-deserialization"
        )


class DjangoAssessTestMixin(object):
    """
    Provides test cases to be used across all django assess apptests
    """

    def test_track_django_sources(self):
        param_val = "; echo /etc/passwd | nc"
        response = self.client.get("/vulnpy/cmdi/os-system", {"user_input": param_val})

        assert response is not None
        assert param_is_tracked(param_val)

    @mocks.build_finding
    def test_xss_django_autoescape(self, mocked):
        """Autoescaping is enabled by default and should not lead to a finding"""
        param_val = "im an attack!"
        response = self.client.get("/xss-autoescape/", {"user_input": param_val})
        assert response.status_code == 200

        assert len(self.request_context.activity.findings) == 0
        assert not mocked.called

    @mocks.build_finding
    def test_xss_django_autoescape_safe(self, mocked):
        """
        Autoescaping is enabled but the value is marked as safe in the template
        which prevents it from being escaped. This should result in a finding.
        """
        param_val = "im an attack!"
        response = self.client.get("/xss-autoescape-safe/", {"user_input": param_val})
        assert response.status_code == 200

        assert len(self.request_context.activity.findings) == 1

        assert mocked.called
        assert mocked.call_args[0][1].name == "reflected-xss"

    @mocks.build_finding
    def test_xss_django_no_autoescape(self, mocked):
        """Autoescaping is disabled so we should get a finding"""
        param_val = "im an attack!"
        response = self.client.get("/xss-no-autoescape/", {"user_input": param_val})
        assert response.status_code == 200

        assert len(self.request_context.activity.findings) == 1

        assert mocked.called
        assert mocked.call_args[0][1].name == "reflected-xss"

    def test_byte_file_contents_are_tracked(self):
        filename = "logo.png"
        file_path = os.path.join(DATA_DIR, filename)

        self.client.post("/file-contents/", upload_files=[("upload", file_path)])

        assert param_is_tracked(filename)

        contents = open(file_path, "rb").read()
        file_start = contents[:6]
        file_end = contents[-18:]

        # we cannot simply assert param_is_tracked(contents) because the contents
        # are split up into chunks in the string tracker and tracked in these chunks
        assert param_is_tracked(file_start)
        assert param_is_tracked(file_end)

    @mocks.build_finding
    def test_uce_base64(self, mocked):
        # this string is "__import__('os').system('echo hacked')" b64 encoded
        encoded_input = "X19pbXBvcnRfXygnb3MnKS5zeXN0ZW0oJ2VjaG8gaGFja2VkJyk="
        response = self.client.get("/uce-base64/", {"user_input": encoded_input})

        assert response.status_code == 200
        assert len(self.request_context.activity.findings) == 1
        assert mocked.called
        args, _ = mocked.call_args
        orig_args = args[-2]
        orig_kwargs = args[-1]

        assert args[1].name == "unsafe-code-execution"
        assert orig_args == (b"__import__('os').system('echo hacked')",)
        assert orig_kwargs == {}

    @skip_no_mongo_db
    @mocks.build_finding
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_find(self, mocked, with_kwarg):
        param_val = "book title"
        response = self.client.post(
            "/nosqli/",
            {
                "user_input": param_val,
                "method_to_test": "find",
                "with_kwarg": with_kwarg,
            },
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "nosql-injection",
            1,
        )

    @skip_no_mongo_db
    @mocks.build_finding
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_insert_one(self, mocked, with_kwarg):
        values = ("Record One", "PyMongo is fun!", "Dani")
        param_val = (
            '{"title": "'
            + values[0]
            + '", "content": "'
            + values[1]
            + '", "author": "'
            + values[2]
            + '"}'
        )

        response = self.client.post(
            "/nosqli/",
            {
                "user_input": param_val,
                "method_to_test": "insert_one",
                "with_kwarg": with_kwarg,
            },
        )

        validate_any_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            values,
            mocked,
            "nosql-injection",
            1,
        )

    @skip_no_mongo_db
    @mocks.build_finding
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_nosqli_rule_post_insert_many(self, mocked, with_kwarg):
        param_val = (
            '{{"title": "Record One", "content": "PyMongo is fun!", "author":'
            ' "Dani"},{"title": "Record Two", "content": "PyMongo is alright",'
            ' "author": "Dani"}}'
        )

        response = self.client.post(
            "/nosqli/",
            {
                "user_input": param_val,
                "method_to_test": "insert_many",
                "with_kwarg": with_kwarg,
            },
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "nosql-injection",
            2,  # extra weak-randomness finding
        )

    @skip_no_mongo_db
    @mocks.build_finding
    def test_nosqli_rule_post_update(self, mocked):
        param_val = "New Title"

        response = self.client.post(
            "/nosqli/", {"user_input": param_val, "method_to_test": "update"},
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "nosql-injection",
            1,
        )

    @skip_no_mongo_db
    @mocks.build_finding
    def test_nosqli_rule_post_delete(self, mocked):
        param_val = (
            '{"title": "Record One", "content": "PyMongo is fun!", "author": "Dani"}'
        )

        response = self.client.post(
            "/nosqli/", {"user_input": param_val, "method_to_test": "delete"},
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "nosql-injection",
            1,
        )

    @pytest.mark.parametrize("path", ["os-system", "subprocess-popen"])
    @pytest.mark.parametrize("method", ["get", "post"])
    @mocks.build_finding
    def test_cmdi(self, mocked, method, path):
        param_val = "echo attack"
        get_or_post = getattr(self.client, method)
        response = get_or_post(
            "/vulnpy/cmdi/{}".format(path), {"user_input": param_val}
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "cmd-injection",
            1,
        )
        if (
            path == "subprocess-popen"
            and method == "get"
            and not os.environ.get("USE_DJANGO_WSGI")  # TODO: PYT-1102
        ):
            assert_subprocess_popen_finding_events(
                self.request_context.activity.findings
            )

    @pytest.mark.parametrize("method_name", ["get", "post"])
    @pytest.mark.parametrize("trigger", ["pickle-load", "pickle-loads"])
    @mocks.build_finding
    def test_ud_pickle(self, mocked, trigger, method_name):
        param_val = "(dp0\nS'lion'\np1\nS'yellow'\np2\nsS'kitty'\np3\nS'red'\np4\ns."

        params = dict(user_input=param_val)

        method = getattr(self.client, method_name)
        method("/vulnpy/deserialization/{}".format(trigger), params)

        assert (
            self.request_context.activity.findings[0].rule_id
            == "untrusted-deserialization"
        )

    @pytest.mark.parametrize("trigger", ["yaml-load", "yaml-load-all"])
    @mocks.build_finding
    def test_ud_yaml(self, mocked, trigger):
        param_val = "!!map {\n" '  ? !!str "goodbye"\n' "}"

        path = "/vulnpy/deserialization/{}/".format(trigger, param_val)
        response = self.client.get(path, {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "untrusted-deserialization",
            1,
        )

    @mocks.build_finding
    def test_xss_escaped_no_vuln(self, mocked):
        param_val = "<script>alert(1)</script>"
        response = self.client.get(
            "/xss/", {"user_input": param_val, "django_escape": "True"},
        )

        assert response is not None
        assert param_is_tracked(param_val)
        assert param_is_tracked(escape(param_val))

        assert not mocked.called
        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize(
        "xml_url",
        ["xml-dom-pulldom-parsestring", "lxml-etree-fromstring", "xml-sax-parsestring"],
    )
    @mocks.build_finding
    def test_xxe(self, mocked, xml_url):
        param_val = "<root>attack</root>"

        response = self.client.get("/vulnpy/xxe/" + xml_url, {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "xxe",
            1,
        )

    @mocks.build_finding
    def test_xss_jinja(self, mocked):
        param_val = "im an attack!"
        response = self.client.get("/xss-jinja/", {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            response.body,
            mocked,
            "reflected-xss",
            1,
        )

    @mocks.build_finding
    def test_xss_mako(self, mocked):
        if django.VERSION[:1] == (3,):
            pytest.xfail("djangomako is broken in Django 3")

        param_val = "im an attack!"
        response = self.client.get("/xss-mako/", {"user_input": param_val})

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            response.body,
            mocked,
            "reflected-xss",
            1,
        )

    @pytest.mark.parametrize("route", ["/vulnpy/xss/raw", "/raw-xss-streaming/"])
    @mocks.build_finding
    def test_xss_raw(self, mocked, route):
        param_val = "im an attack!"

        response = self.client.get(route, {"user_input": param_val})
        assert response.status_code == 200

        if "streaming" in route:
            # Make sure that our middleware doesn't consume streaming content
            content = response.body
            assert content == b"<p>Looks like xss: im an attack!</p>"
        else:
            assert "<p>XSS: {}</p>".format(param_val) in str(response.body)

        assert mocked.called
        assert mocked.call_args[0][1].name == "reflected-xss"
        assert len(self.request_context.activity.findings) == 1

    @mocks.build_finding
    def test_xss_csv_does_not_send_finding(self, mocked):
        param_val = "im an attack!"
        response = self.client.get("/xss-csv/", {"user_input": param_val})

        assert response.status_code == 200

        assert not mocked.called
        assert len(self.request_context.activity.findings) == 0

    @mocks.build_finding
    def test_cmdi_from_filename_and_contents(self, mocked):
        filename = "testfile.txt"
        file_path = os.path.join(DATA_DIR, filename)

        response = self.client.post("/cmdi-file/", upload_files=[("upload", file_path)])

        data_path = os.path.join(settings.MEDIA_ROOT, "data")
        result = "cp {0}/testfile.txt {0}/testfile.txt.bak".format(data_path)
        validate_finding(
            self.request_context.activity.findings,
            response,
            filename,
            result,
            mocked,
            "cmd-injection",
            1,
        )

        file_contents = (
            b"This file contains extremely dangerous data. Use at your own risk!\n"
        )
        param_is_tracked(file_contents)

    @mocks.build_finding
    def test_stream_source(self, mocked):
        response = self.client.get("/stream-source/")
        assert response.status_code == 200

        assert mocked.called
        assert mocked.call_args[0][1].name == "untrusted-deserialization"
        assert len(self.request_context.activity.findings) == 1

    @pytest.mark.parametrize(
        "trigger", ["legacy-urlopen", "urlopen-str", "urlopen-obj"]
    )
    @pytest.mark.parametrize("safe", [False, True])
    @mocks.build_finding
    def test_ssrf_urllib(self, mocked, trigger, safe):
        user_input = "not.a.url" if safe else "http://attacker.com/?q=foobar"
        response = self.client.get(
            "/vulnpy/ssrf/{}".format(trigger), {"user_input": user_input},
        )
        assert response.status_code == 200
        if not safe:
            validate_ssrf_finding(trigger, self.request_context, mocked)
        else:
            assert not mocked.called
            assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("trigger_class", ["httpconnection", "httpsconnection"])
    @pytest.mark.parametrize(
        "trigger_method", ["request-method", "putrequest-method", "init"]
    )
    @mocks.build_finding
    def test_ssrf_httplib(self, mocked, trigger_method, trigger_class):
        trigger = "-".join([trigger_class, trigger_method])
        user_input = "www.attacker.com" if trigger_method == "init" else "DELETE"
        response = self.client.get(
            "/vulnpy/ssrf/{}".format(trigger), {"user_input": user_input},
        )
        assert response.status_code == 200
        validate_ssrf_finding(trigger, self.request_context, mocked)

    @pytest.mark.parametrize("trigger_class", ["httpconnection", "httpsconnection"])
    @pytest.mark.parametrize("trigger_method", ["request", "putrequest"])
    @mocks.build_finding
    def test_ssrf_httplib_safe(self, mocked, trigger_method, trigger_class):
        """
        HTTP*Connection.*request isn't vulnerable to SSRF via the "url" argument.
        This is because it only takes a path / querystring, which isn't vulnerable
        to ssrf.
        """
        trigger = "-".join([trigger_class, trigger_method, "url"])
        response = self.client.get(
            "/vulnpy/ssrf/{}".format(trigger), {"user_input": "/some/path"},
        )
        assert response.status_code == 200
        assert not mocked.called
        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("permanent_redirect", [True, False])
    @mocks.build_finding
    def test_unvalidated_redirect(self, mocked, permanent_redirect):
        """
        By passing a permanent redirect bool flag, we can test that both
        HttpResponsePermanentRedirect and HttpResponseRedirect are patched
        because they inherit from HttpResponseRedirectBase
        """
        redirect_route = "/vulnpy"
        response = self.client.get(
            "/unvalidated-redirect/",
            {"user_input": redirect_route, "permanent": permanent_redirect},
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            redirect_route,
            redirect_route,
            mocked,
            "unvalidated-redirect",
            1,
        )

    def test_preflight_hash_same_request(self):
        """
        Two requests that look exactly the same should generate the same hash
        """
        # This test will pass in isolation on django-1.10.8, but when the full test
        # suite runs, it will not. The findings are both present, but the first one
        # has way more events than the second one for some reason. It seems like
        # something in the test environment is polluting this test state somehow.
        if django.VERSION[:2] == (1, 10):
            pytest.xfail("Known weirdness with events on django-1.10.8 apptest")

        self.client.get("/vulnpy/cmdi/os-system", {"user_input": "first attack"})

        assert len(self.request_context.activity.findings) == 1
        first_finding = self.request_context.activity.findings[0]

        self.client.get("/vulnpy/cmdi/os-system", {"user_input": "second attack"})
        assert len(self.request_context.activity.findings) == 1
        second_finding = self.request_context.activity.findings[0]

        assert second_finding is not first_finding
        assert second_finding.hash_code == first_finding.hash_code
        assert second_finding.preflight == first_finding.preflight

    def test_preflight_hash_different_requests(self):
        """
        Two different requests that find the same vuln should have different hashes

        In this case, the two requests are the same except one uses GET and the
        other uses POST. Since the HTTP method contributes to the hash, we
        should get different preflight values.
        """
        param_val = "im an attack!"
        self.client.get("/vulnpy/cmdi/subprocess-popen", {"user_input": param_val})

        assert len(self.request_context.activity.findings) == 1
        first_finding = self.request_context.activity.findings[0]

        self.client.post("/vulnpy/cmdi/subprocess-popen", {"user_input": param_val})
        assert len(self.request_context.activity.findings) == 1
        second_finding = self.request_context.activity.findings[0]

        assert second_finding is not first_finding
        assert second_finding.hash_code != first_finding.hash_code
        assert second_finding.preflight != first_finding.preflight

    def test_preflight_hash_same_request_different_vulns(self):
        """
        The same request that generates two different vulns should have different hashes
        """
        param_val = "im an attack!"
        self.client.get("/two-vulns/", {"user_input": param_val})

        assert len(self.request_context.activity.findings) == 2

        first_finding = self.request_context.activity.findings[0]
        second_finding = self.request_context.activity.findings[1]

        assert second_finding.hash_code != first_finding.hash_code
        assert second_finding.preflight != first_finding.hash_code

    @pytest.mark.parametrize("endpoint", ["exec", "eval", "compile"])
    def test_untrusted_code_exec(self, endpoint):
        user_input = "1 + 2 + 3"
        self.client.get(
            "/vulnpy/unsafe_code_exec/{}/".format(endpoint), dict(user_input=user_input)
        )

        assert (
            len(self.request_context.activity.findings) == 2
            if six.PY2 and endpoint == "eval"
            else 1
        )
        assert (
            self.request_context.activity.findings[0].rule_id
            == u"unsafe-code-execution"
        )

    @python2_only
    @pytest.mark.xfail(
        os.environ.get("USE_DJANGO_WSGI") is not None, reason="TODO: PYT-1096"
    )
    def test_untrusted_execfile(self):
        user_input = "fake_filename.py"
        self.client.get("/vulnpy/pt/execfile/", dict(user_input=user_input))

        assert len(self.request_context.activity.findings) == 1
        assert self.request_context.activity.findings[0].rule_id == u"path-traversal"

    @pytest.mark.xfail(django.VERSION[:2] == (1, 9), reason="TODO: PYT-1050")
    @pytest.mark.parametrize(
        "test_type",
        [
            "create_method",
            "init_direct",
            "filter",
            "multi-column",  # TODO: PYT-583 still need to test multi-trigger / multi findings
        ],
    )
    @pytest.mark.django_db(transaction=False)
    @mocks.build_finding
    def test_stored_xss(self, mocked, test_type):
        param_val = "hello"
        response = self.client.get(
            "/stored-xss/", {"user_input": param_val, "test_type": test_type}
        )

        findings = self.request_context.activity.findings

        validate_finding(
            findings, response, param_val, response.body, mocked, "reflected-xss", 1
        )

        assert_event_sources(findings, "database", {"database": "TAINTED_DATABASE"})

    @pytest.mark.parametrize("module_name", ["xml", "lxml"])
    def test_xpath_injection(self, module_name):
        query = ".//*[@name='whatever']"
        self.client.get("/xpath-injection/", dict(query=query, module=module_name))

        findings = self.request_context.activity.findings
        assert len(findings) == 1
        assert findings[0].rule_id == "xpath-injection"

    @pytest.mark.parametrize("trigger", ["io-open", "open"])
    @mocks.build_finding
    def test_path_traversal(self, mocked, trigger):
        param_val = "doesnt matter"
        response = self.client.get(
            "/vulnpy/pt/{}".format(trigger), {"user_input": param_val}
        )

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            param_val,
            mocked,
            "path-traversal",
            1,
        )

    @pytest.mark.django_db(transaction=False)
    @pytest.mark.parametrize("method", ["get", "post"])
    @mocks.build_finding
    def test_sqli_via_django_orm(self, mocked, method):
        param_val = "doesnt matter"
        get_or_post = getattr(self.client, method)
        response = get_or_post("/sqli/", {"user_input": param_val})

        query = "SELECT * FROM app_message WHERE id = 'doesnt matter'"

        validate_finding(
            self.request_context.activity.findings,
            response,
            param_val,
            query,
            mocked,
            "sql-injection",
            1,
        )

    @pytest.mark.parametrize(
        "trigger,query_fmt",
        [
            ("sqlite3-execute", sqli.EXECUTE_QUERY_FMT),
            ("sqlite3-executemany", sqli.EXECUTEMANY_QUERY_FMT),
            ("sqlite3-executescript", sqli.EXECUTESCRIPT_QUERY_FMT,),
        ],
    )
    @mocks.build_finding
    def test_sqli(self, mocked, trigger, query_fmt):
        user_input = "any value works"
        response = self.client.get(
            "/vulnpy/sqli/{}".format(trigger), {"user_input": user_input}
        )

        query = query_fmt.format(user_input)

        validate_finding(
            self.request_context.activity.findings,
            response,
            user_input,
            query,
            mocked,
            "sql-injection",
            1,
        )


class DjangoAssessTestNondataflowMixin(object):
    @pytest.mark.parametrize("trigger", ["random", "randint", "randrange", "uniform"])
    @mocks.build_finding
    def test_crypto_weak_randomness(self, mocked, trigger):
        response = self.client.get(
            "/vulnpy/rand/{}".format(trigger), {"user_input": "abc123"}
        )
        validate_nondataflow_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            "crypto-weak-randomness",
            1,
        )

    @pytest.mark.parametrize("trigger", ["hashlib-md5", "hashlib-sha1", "hashlib-new"])
    @mocks.build_finding
    def test_crypto_bad_mac(self, mocked, trigger):
        response = self.client.get(
            "/vulnpy/hash/{}".format(trigger), {"user_input": "def456"}
        )
        validate_nondataflow_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            "crypto-bad-mac",
            1,
        )

    @mocks.build_finding
    def test_crypto_bad_ciphers(self, mocked):
        response = self.client.get("/crypto-bad-ciphers/")

        validate_nondataflow_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            "crypto-bad-ciphers",
            8,
            1,
        )


class DjangoRouteCoverageTestMixin(object):
    @mock_build_update_messages
    def test_finds_app_routes(self, build_update_message):
        self.client.get("/vulnpy")

        routes = build_update_message.call_args[0][0]
        cmdi_routes = current_routes_by_url(routes, "vulnpy/cmdi/os-system")
        assert_routes_count(cmdi_routes, 2)

    @mock_build_update_messages
    def test_reports_dynamic_route_in_discovery(self, build_update_message):
        """
        Tests that a dynamically-created route is found because the first request
        made is to the endpoint that creates this route. The dynamically-created
        route is not visited.
        """
        new_view = "new_dynamic"
        original_url_names = [x.name for x in URLPATTERNS_COPY[1:]]
        assert new_view not in original_url_names

        self.client.get("/dynamic_url_view/", {"user_input": new_view})

        routes = build_update_message.call_args[0][0]
        dynamic_routes = current_routes_by_url(routes, new_view)
        assert_routes_count(dynamic_routes, 2)

    @mock_send_messages
    @mock_build_update_messages
    def test_reports_dynamic_route_by_observed_route(
        self, build_update_message, send_messages
    ):
        """
        Tests that a dynamically-created route is found because it is visited. The
        endpoint that created this route was not the first request to the app.
        """
        new_view = "other_dynamic"
        original_url_names = [x.name for x in URLPATTERNS_COPY[1:]]
        assert new_view not in original_url_names
        self.client.get("/")

        routes = build_update_message.call_args[0][0]
        current_routes = current_routes_by_url(routes, new_view)
        # new_dynamic has not been created so it is not found
        assert_routes_count(current_routes, 0)

        assert len(send_messages.call_args[0][0]) == 4

        self.client.get("/dynamic_url_view/?user_input=" + new_view)

        assert len(send_messages.call_args[0][0]) == 3

        new_path = "/" + new_view + "/"
        self.client.get(new_path)
        call_args = send_messages.call_args[0][0]
        assert len(call_args) == 3

        observed_route = call_args[2]
        assert isinstance(observed_route, ObservedRoute)
        assert observed_route.url == new_path
        assert (
            observed_route.signature
            == "contrast.test.apptest.django_views.other_dynamic(request,)"
        )

    def test_route_appended_to_xss_vuln(self):
        param_val = "im an attack!"
        response = self.client.get("/xss/", {"user_input": param_val})

        assert response
        assert len(self.request_context.activity.findings) > 0
        assert_route_appended(self.request_context.activity.findings, "xss", "GET")

    @pytest.mark.django_db(transaction=False)
    def test_observed_route_appended(self):
        param_val = "im an attack!"
        param_name = "user_input"
        url = "/sqli"
        response = self.client.get(url, {param_name: param_val})

        assert response
        assert len(self.request_context.activity.findings) == 1
        validate_observed_route(
            self.request_context, "GET", url[1:], param_name, "PARAMETER"
        )

    @pytest.mark.xfail(
        os.environ.get("USE_DJANGO_WSGI") is not None and six.PY2,
        reason="TODO: PYT-1096",
    )
    @pytest.mark.parametrize("setdefault", [False, True])
    def test_trust_boundary_violation(self, setdefault):
        self.client.get(
            "/trust-boundary-violation/?user_input=whatever&setdefault={}".format(
                setdefault
            )
        )

        # the wsgi middleware is early enough to see a crypto-bad-mac in an earlier middleware
        # the django middleware is last in the middleware stack, so it misses this vulnerability
        assert (
            len(self.request_context.activity.findings) == 2
            if os.environ.get("USE_DJANGO_WSGI")  # TODO: PYT-1102
            else 1
        )
        assert (
            self.request_context.activity.findings[0].rule_id
            == "trust-boundary-violation"
        )


class DjangoAssessTestDynamicSourcesMixin(object):

    ATTACK_VALUE = "im an attack!"
    DYNAMIC_SOURCE_RULE_ID = "cmd-injection"

    def set_dangerous_cookie(self):
        self.client.set_cookie("user_input", self.ATTACK_VALUE)

    @mocks.build_finding
    def test_xss_from_cookie(self, mocked):
        self.set_dangerous_cookie()
        self.client.get("/xss-cookie/")

        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("source", GET_SOURCES)
    @mocks.build_finding
    def test_all_get_sources(self, mocked, source):
        self.set_dangerous_cookie()
        response = self.client.get(
            "/dynamic-sources/",
            {"user_input": self.ATTACK_VALUE, "source": source},
            headers={"Referer": "www.python.org"},
            # **{source: self.ATTACK_VALUE}
        )

        validate_source_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            source,
            self.DYNAMIC_SOURCE_RULE_ID,
            1,
        )

    @pytest.mark.parametrize("source", POST_SOURCES)
    @mocks.build_finding
    def test_all_post_sources(self, mocked, source):
        self.set_dangerous_cookie()
        if source == "files":
            file_path = os.path.join(DATA_DIR, "testfile.txt")
            response = self.client.post(
                "/dynamic-sources/",
                {"source": source},
                upload_files=[("user_input", file_path)],
                headers={"Referer": "www.python.org"},
            )

        else:
            response = self.client.post(
                "/dynamic-sources/",
                {"user_input": self.ATTACK_VALUE, "source": source},
                headers={"Referer": "www.python.org"},
                # **{source: self.ATTACK_VALUE}
            )

        validate_source_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            source,
            self.DYNAMIC_SOURCE_RULE_ID,
            1,
        )

    @mocks.build_finding
    def test_cookie_get(self, mocked):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.set_dangerous_cookie()
        self.client.get("/cookie-source/")
        validate_cookies_sources(self.request_context.activity.findings)

    @mocks.build_finding
    def test_cookie_post(self, mocked):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.set_dangerous_cookie()
        self.client.post("/cookie-source/")
        validate_cookies_sources(self.request_context.activity.findings)

    @pytest.mark.parametrize(
        "route,source_name",
        [("/header-source/", "header"), ("/header-key-source/", "header_key")],
    )
    @pytest.mark.parametrize("method_name", ["get", "post"])
    @pytest.mark.parametrize("use_environ", [False, True])
    @mocks.build_finding
    def test_header_source(self, mocked, use_environ, method_name, route, source_name):
        method = getattr(self.client, method_name)
        method(route, headers={"Test-Header": "whatever"})

        validate_header_sources(self.request_context.activity.findings, source_name)

    @pytest.mark.parametrize("method_name", ["get", "post"])
    def test_http_method_not_source(self, method_name):
        method = getattr(self.client, method_name)
        method("/dynamic-sources/", dict(source="http_method"))

        assert len(self.request_context.activity.findings) == 0
