# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Definitions of blueprints that can be used in flask test apps
"""
import html
import io
import os
from os import path

from flask import Blueprint, render_template, request, redirect
from flask.sessions import SecureCookieSession
import contrast
from contrast.test.library_analysis import (
    remove_sys_module_entries,
    import_with_relative_imports,
    import_namespace_package,
    import_sample_package_onefile,
    import_multiple_tlds,
)

APPTEST_DIR = path.join(path.dirname(contrast.__file__), "..")
TEMPLATE_DIR = path.join(APPTEST_DIR, "templates", "flask")
router = Blueprint("contrast", __name__, template_folder=TEMPLATE_DIR)


@router.route(
    "/import_package_with_relative_imports", methods=["GET"], strict_slashes=False
)
def import_package_with_relative_imports():
    rm_modules = request.args.get("rm_sys_mod_entries", None)

    if rm_modules:
        remove_sys_module_entries()

    import_with_relative_imports()

    return ""


@router.route("/import_namespace_package", methods=["GET"], strict_slashes=False)
def import_sample_namespace_package():
    # Deleting top level namespace modules breaks them in py2.
    # Namespace name is cached in sys modules, but shows up
    # as a builtin module in py2.
    import_namespace_package()

    return ""


@router.route("/import_package_onefile", methods=["GET"], strict_slashes=False)
def import_package_onefile():
    rm_modules = request.args.get("rm_sys_mod_entries", None)

    if rm_modules:
        remove_sys_module_entries()

    import_sample_package_onefile()

    return ""


@router.route(
    "/import_sample_dist_multiple_tlds", methods=["GET"], strict_slashes=False
)
def import_sample_dist_multiple_tlds():
    rm_modules = request.args.get("rm_sys_mod_entries", None)

    if rm_modules:
        remove_sys_module_entries()

    import_multiple_tlds()

    return ""


@router.route(
    "/markupsafe-sanitized-xss", methods=["GET", "POST"], strict_slashes=False
)
def markupsafe_sanitized_xss():
    """
    This is a test for Markupsafe.escape as it gets called by the template engine.
    """
    user_input = request.args.get("user_input")
    ret = render_template("sanitized_xss.html", user_input=user_input)
    return ret


@router.route("/html-sanitized-xss", methods=["GET", "POST"], strict_slashes=False)
def html_sanitized_xss():
    """
    This is a test for Markupsafe.escape as it gets called by the template engine.
    """
    user_input = request.args.get("user_input")
    ret = html.escape(user_input)
    return ret


@router.route("/dynamic-sources", methods=["GET", "POST"], strict_slashes=False)
def dynamic_sources():
    source = request.args.get("source", "")
    user_input = ""

    if source == "args":
        user_input = request.args.get("user_input")
    elif source == "base_url":
        user_input = request.base_url
    elif source == "referer_header":
        user_input = request.headers.get("Referer")
    elif source == "host":
        user_input = request.host
    elif source == "host_url":
        user_input = request.host_url
    elif source == "files" and request.method == "POST":
        stream = request.files.get("file_upload")
        user_input = stream.read()
    elif source == "form" and request.method == "POST":
        user_input = request.form.get("user_input")
    elif source == "full_path":
        user_input = request.full_path
    elif source == "path":
        user_input = request.path
    elif source == "query_string":
        user_input = request.query_string
    elif source == "remote_addr":
        user_input = request.remote_addr
    elif source == "scheme":
        user_input = request.scheme
    elif source == "url":
        user_input = request.url
    elif source == "url_root":
        user_input = request.url_root
    elif source == "values":
        user_input = request.values.get("user_input")
    elif source == "values_get_item":
        user_input = request.values["user_input"]
    elif source == "wsgi.input":
        user_input = request.environ["wsgi.input"].read()
        # restore wsgi.input so that it can still be read later if needed
        request.environ["wsgi.input"] = io.BytesIO(user_input)

    return render_template("xss.html", user_input=user_input)


@router.route("/cookie-source", methods=["GET", "POST"], strict_slashes=False)
def cookie_source():
    user_input = request.cookies["user_input"]
    os.system("echo {}".format(user_input))
    return render_template("xss.html", user_input=user_input)


@router.route("/header-source", methods=["GET", "POST"], strict_slashes=False)
def header_source():
    user_input = request.headers.get("Test-Header")
    os.system("echo {}".format(user_input))
    return render_template("xss.html", user_input=user_input)


@router.route("/header-key-source", methods=["GET", "POST"], strict_slashes=False)
def header_key_source():
    header_keys = list(request.headers.keys())
    # Make sure we grab a header that we know will not come from another source, so it
    # will not have any other tags. For example, the 'Host' header has source type URI,
    # and so gets tagged with CROSS_SITE, so we don't want to test with that one.
    user_input = header_keys[header_keys.index("Test-Header")]
    os.system("echo {}".format(user_input))
    return render_template("xss.html", user_input=user_input)


@router.route("/method-source", methods=["GET", "POST"], strict_slashes=False)
def method_source():
    user_input = request.method
    os.system("echo {}".format(user_input))
    return render_template("xss.html", user_input=user_input)


@router.route("/multidict-sources", methods=["GET", "POST"], strict_slashes=False)
def multidict_sources():
    source = request.args.get("source", "")
    user_input = ""

    if request.method == "GET":
        if source == "items":
            user_input = [
                x for x in list(request.args.items()) if x[0] == "user_input"
            ][0][1]
        elif source == "lists":
            user_input = [
                x for x in list(request.args.lists()) if x[0] == "user_input"
            ][0][1][0]
        elif source == "listvalues":
            user_input = list(request.args.listvalues())[0][0]
        elif source == "values":
            user_input = list(request.args.values())[0]
    elif request.method == "POST":
        if source == "items":
            user_input = [
                x for x in list(request.form.items()) if x[0] == "user_input"
            ][0][1]
        elif source == "lists":
            user_input = [
                x for x in list(request.form.lists()) if x[0] == "user_input"
            ][0][1][0]
        elif source == "listvalues":
            user_input = list(request.form.listvalues())[0][0]
        elif source == "values":
            user_input = list(request.form.values())[0]

    return render_template("xss.html", user_input=user_input)


@router.route("/unvalidated-redirect", methods=["GET", "POST"], strict_slashes=False)
def unvalidated_redirect():
    user_input = request.args.get("user_input")
    if request.args.get("with_kwarg", str(False)) == str(True):
        return redirect(location=user_input)
    return redirect(user_input)


@router.route("/trust-boundary-violation", methods=["GET"], strict_slashes=False)
def trust_boundary_violation():
    user_input = request.args.get("user_input")
    session = SecureCookieSession()

    if request.args.get("setdefault") == "True":
        session.setdefault("user_input", user_input)
    else:
        session["user_input"] = user_input

    return "<p>Trust boundary violation</p>"
