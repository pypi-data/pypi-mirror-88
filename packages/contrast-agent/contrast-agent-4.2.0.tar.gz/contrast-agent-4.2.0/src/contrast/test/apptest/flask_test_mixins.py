# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from os import path

import pytest
import six  # pylint: disable=did-not-import-extern

from contrast.agent.policy import constants
from contrast.agent.assess.utils import get_properties
from contrast.api.dtm_pb2 import TraceEvent
from contrast.test import mocks
from contrast.test.contract.events import check_event
from contrast.test.contract.findings import (
    validate_finding,
    validate_source_finding,
    validate_header_sources,
    validate_cookies_sources,
    validate_ssrf_finding,
)

from vulnpy.trigger import sqli

from contrast.test.library_analysis import (
    assert_files_loaded,
    import_sample_package_onefile,
    TEST_MODULES_RELATIVE_IMPORT_DIST,
    TEST_MODULES_NAMESPACE_DIST,
    TEST_MODULE_ONEFILE,
    TEST_MODULES_MULTIPLE_TLDS_DIST,
)

SOURCE_OPTIONS_MAP = {
    "args": "QUERYSTRING",
    "base_url": "URI",
    "full_path": "URI",
    "referer_header": "HEADER",
    "host": "URI",
    "host_url": "URI",
    "path": "URI",
    "query_string": "QUERYSTRING",
    "scheme": "OTHER",
    "url": "URI",
    "url_root": "URI",
    "values": "PARAMETER",
    "values_get_item": "PARAMETER",
}
# REMOTE_ADDR does not appear to be present in environ in Py27
SOURCE_OPTIONS_MAP.update({"remote_addr": "URI"} if six.PY3 else {})


POST_OPTIONS_MAP = {
    "files": "MULTIPART_CONTENT_DATA",
    "form": "MULTIPART_FORM_DATA",
    "wsgi.input": "BODY",
}

MULTIDICT_GET_OPTIONS_MAP = {
    "items": "QUERYSTRING",  # args.items()
    "lists": "QUERYSTRING",  # args.lists()
    "listvalues": "QUERYSTRING",  # args.listvalues()
    "values": "QUERYSTRING",  # args.values()
}

MULTIDICT_POST_OPTIONS_MAP = {
    "items": "MULTIPART_FORM_DATA",  # form.items()
    "lists": "MULTIPART_FORM_DATA",  # form.lists()
    "listvalues": "MULTIPART_FORM_DATA",  # form.listvalues()
    "values": "MULTIPART_FORM_DATA",  # form.values()
}


ALL_OPTIONS_MAP = {}
ALL_OPTIONS_MAP.update(SOURCE_OPTIONS_MAP)
ALL_OPTIONS_MAP.update(POST_OPTIONS_MAP)


SOURCE_OPTIONS = tuple(SOURCE_OPTIONS_MAP.keys())
POST_OPTIONS = tuple(POST_OPTIONS_MAP.keys())


def assert_flask_sqli_finding_events(finding, source_class_name):
    assert len(finding.events) == 17

    event_idx = 0
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.CREATION_TYPE),
        class_name=source_class_name,
        method_name="QUERY_STRING",
        source_types=["QUERYSTRING"],
        first_parent=None,
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="encode",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="split",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="replace",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.OBJECT_KEY + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="decode",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 4
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="concat",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )

    # There are a few f-string propagation events here that previously were
    # omitted because they have no effect (i.e. the resulting string is
    # identical to the input). They are now showing up because we had to make a
    # fix to join propagation, which affects f-strings as well.

    event_idx += 4
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(
            constants.ALL_TYPE + constants.TO_MARKER + constants.RETURN_KEY
        ),
        class_name="str",
        method_name="CAST",
        source_types=[],
        # TODO: PYT-922 for some reason this event doesn't have any parent_object_ids
        first_parent=None,
    )
    event_idx += 1
    check_event(
        finding.events[event_idx],
        event_type=TraceEvent.TYPE_PROPAGATION,
        action=TraceEvent.Action.Value(constants.TRIGGER_TYPE),
        class_name="sqlite3.Cursor",
        method_name="execute",
        source_types=[],
        first_parent=finding.events[event_idx - 1],
    )


class FlaskTestLibraryAnalysisBuiltinImport(object):
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


class FlaskAssessTestMixin(object):
    def validate_source_finding(self, response, mocked, source, options_map=None):
        validate_source_finding(
            self.request_context.activity.findings,
            response,
            mocked,
            source,
            "reflected-xss",
            1,
            options_map or ALL_OPTIONS_MAP,
        )

    def assert_propagation_happened(self, apply_trigger):
        """
        This tests that apply_trigger was called with the "ret" argument
        that has an HTML_ENCODED tag, indicating that propagation did occur.
        """
        assert apply_trigger.called
        call_args = apply_trigger.call_args
        ret_arg = call_args[0][2]
        assert "HTML_ENCODED" in get_properties(ret_arg).tags

    @pytest.mark.parametrize("method_name", ["get", "post"])
    @mocks.build_finding
    def test_xss(self, mocked, method_name):
        user_input = "whatever"
        method = getattr(self.client, method_name)

        response = method("/vulnpy/xss/raw", {"user_input": user_input})

        assert response.status_code == 200
        validate_finding(
            self.request_context.activity.findings,
            response,
            user_input,
            response.body,
            mocked,
            "reflected-xss",
            1,
        )

        finding = self.request_context.activity.findings[0]

        trigger_event = finding.events[-1]
        assert trigger_event.signature.class_name == "flask.app.Flask"
        assert trigger_event.signature.method_name == "wsgi_app"

    @pytest.mark.parametrize("user_input", ["something <> dangerous", "something safe"])
    @pytest.mark.parametrize("sanitizer", ["markupsafe", "html"])
    @mocks.apply_trigger
    @mocks.build_finding
    def test_sanitized_xss(self, build_finding, apply_trigger, user_input, sanitizer):
        response = self.client.post(
            "/{}-sanitized-xss?user_input={}".format(sanitizer, user_input)
        )

        assert response.status_code == 200

        self.assert_propagation_happened(apply_trigger)
        assert not build_finding.called
        assert len(self.request_context.activity.findings) == 0

    @pytest.mark.parametrize("source", SOURCE_OPTIONS)
    @mocks.build_finding
    def test_all_get_sources(self, mocked, source):
        self.client.set_cookie("user_input", "attack_cookie")
        response = self.client.get(
            "/dynamic-sources/",
            {"user_input": self.ATTACK_VALUE, "source": source},
            headers={"Referer": "www.python.org"},
            extra_environ={"REMOTE_ADDR": "localhost"},
        )

        self.validate_source_finding(response, mocked, source)

    @pytest.mark.parametrize("source", SOURCE_OPTIONS + POST_OPTIONS)
    @mocks.build_finding
    def test_all_post_sources(self, mocked, source):
        self.client.set_cookie("user_input", "attack_cookie")
        file_path = path.join(self.app.root_path, "..", "..", "data", "testfile.txt")
        response = self.client.post(
            "/dynamic-sources/?user_input={}&source={}".format(
                self.ATTACK_VALUE, source
            ),
            {"user_input": self.ATTACK_VALUE},
            headers={"Referer": "www.python.org"},
            upload_files=[("file_upload", file_path)],
            extra_environ={"REMOTE_ADDR": "localhost"},
        )

        self.validate_source_finding(response, mocked, source)

    @pytest.mark.parametrize("source", MULTIDICT_GET_OPTIONS_MAP.keys())
    @mocks.build_finding
    def test_all_get_multidict(self, mocked, source):
        response = self.client.get(
            "/multidict-sources",
            {"user_input": self.ATTACK_VALUE, "source": source},
            headers={"user_input": self.ATTACK_VALUE},
        )

        self.validate_source_finding(
            response, mocked, source, MULTIDICT_GET_OPTIONS_MAP
        )

    @pytest.mark.parametrize("source", MULTIDICT_POST_OPTIONS_MAP.keys())
    @mocks.build_finding
    def test_all_post_multidict(self, mocked, source):
        response = self.client.post(
            "/multidict-sources?source={}".format(source),
            {"user_input": self.ATTACK_VALUE},
            headers={"user_input": self.ATTACK_VALUE},
        )

        self.validate_source_finding(
            response, mocked, source, MULTIDICT_POST_OPTIONS_MAP
        )

    def test_cookie_get(self):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.client.set_cookie("user_input", "attack_cookie")
        self.client.get("/cookie-source")
        validate_cookies_sources(self.request_context.activity.findings)

    def test_cookie_post(self):
        """Cookies shouldn't trigger xss, so we need a separate cookie source test"""
        self.client.set_cookie("user_input", "attack_cookie")
        self.client.post("/cookie-source")
        validate_cookies_sources(self.request_context.activity.findings)

    @pytest.mark.parametrize(
        "route,source_name",
        [("/header-source/", "header"), ("/header-key-source/", "header_key")],
    )
    @pytest.mark.parametrize("method_name", ["get", "post"])
    def test_non_xss_sources(self, method_name, route, source_name):
        method = getattr(self.client, method_name)
        method(route, headers={"Test-Header": "whatever"})

        validate_header_sources(self.request_context.activity.findings, source_name)

    @pytest.mark.parametrize("method_name", ("get", "post"))
    def test_http_method_not_source(self, method_name):
        getattr(self.client, method_name)("/method-source/")
        assert len(self.request_context.activity.findings) == 0

    @mocks.build_finding
    def test_sqli_sqlalchemy(self, mocked):
        param_val = "doesnt matter"
        response = self.client.get("/sqli/", {"user_input": param_val})

        query = "SELECT * FROM user WHERE user.email = 'doesnt matter'"

        findings = self.request_context.activity.findings
        validate_finding(
            findings, response, param_val, query, mocked, "sql-injection", 1
        )
        # the exact event sequence is different for PY2/PY3
        if six.PY3:
            assert_flask_sqli_finding_events(findings[0], "wsgi.environ")

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
            "/vulnpy/sqli/{}".format(trigger), {"user_input": user_input},
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

    @mocks.build_finding
    @pytest.mark.parametrize("with_kwarg", [False, True])
    def test_unvalidated_redirect(self, mocked, with_kwarg):
        redirect_route = "/cmdi"
        response = self.client.get(
            "/unvalidated-redirect",
            {"user_input": redirect_route, "with_kwarg": with_kwarg},
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

    @pytest.mark.parametrize("setdefault", [False, True])
    def test_trust_boundary_violation(self, setdefault):
        user_input = "hello"
        self.client.get(
            "/trust-boundary-violation",
            {"user_input": user_input, "setdefault": setdefault},
        )

        assert len(self.request_context.activity.findings) == 1
        assert (
            self.request_context.activity.findings[0].rule_id
            == "trust-boundary-violation"
        )

    @pytest.mark.parametrize("endpoint", ["exec", "eval", "compile"])
    def test_untrusted_code_exec(self, endpoint):
        user_input = "1 + 2 + 3"
        self.client.get(
            "/vulnpy/unsafe_code_exec/{}".format(endpoint), {"user_input": user_input},
        )

        assert len(self.request_context.activity.findings) == 1
        assert (
            self.request_context.activity.findings[0].rule_id
            == u"unsafe-code-execution"
        )

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
            "/vulnpy/ssrf/{}".format(trigger), {"user_input": "/some/path"}
        )
        assert response.status_code == 200
        assert not mocked.called
        assert len(self.request_context.activity.findings) == 0
