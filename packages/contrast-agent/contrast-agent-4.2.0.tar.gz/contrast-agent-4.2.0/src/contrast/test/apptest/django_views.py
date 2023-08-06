# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Definitions of view functions that can be used in django app tests.
"""
import base64
import csv
import io
import json
import os
import pickle
from xml.etree import ElementTree


import lxml.etree
import six  # pylint: disable=did-not-import-extern
from Crypto.Cipher import Blowfish

import django
from django.contrib.auth import logout as DjangoLogout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from contrast.test.mongo import create_mongo_client

from contrast.test.library_analysis import (
    remove_sys_module_entries,
    import_with_relative_imports,
    import_namespace_package,
    import_sample_package_onefile,
    import_multiple_tlds,
)

from vulnpy.trigger import cmdi

try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url

try:
    from app.models import Message
except ImportError:
    Message = None

from app import settings

try:
    from app.jinja2_env import environment as jinja2_environment

    JINJA_ENV = jinja2_environment()
except ImportError:
    JINJA_ENV = None


# This ends up resolving to a path relative to the apptest dir so that we don't
# have to package this data file with the contrast module.
DATA_DIR = os.path.join("..", "data")


def home(request):
    return render(request, "base.html")


def static_image(request):
    filename = request.GET.get("filename", "image.jpg")
    image_path = os.path.join(DATA_DIR, filename)
    with open(image_path, "rb") as image_fh:
        return StreamingHttpResponse(image_fh.readlines(), content_type="image/jpeg")


def django_autoescape(request):
    """Uses a django template with autoescaping (enabled by default)"""
    user_input = request.GET.get("user_input", "")
    return render(request, "xss.html", {"user_input": user_input}, using="django")


def django_autoescape_safe(request):
    """Uses a django template with autoescaping but marks value as safe"""
    user_input = request.GET.get("user_input", "")
    return render(
        request, "xss_autoescape_safe.html", {"user_input": user_input}, using="django"
    )


def django_no_autoescape(request):
    user_input = request.GET.get("user_input", "")
    return render(
        request, "xss_no_autoescape.html", {"user_input": user_input}, using="django"
    )


@require_http_methods(["POST"])
def file_contents(request):
    """
    This view is intended to demonstrate that simply calling request.FILES
    tracks the contents of a file because
    django.utils.datastructures.MultiValueDict __getitem__ is a source in policy.json
    """
    request.FILES["upload"]
    return render(request, "base.html")


def uce_base64(request):
    """
    Adapted from a vulnerable view in lets-be-bad-guys.
    The user_input param must base64 encoded string.
    Example: X19pbXBvcnRfXygnb3MnKS5zeXN0ZW0oJ2VjaG8gaGFja2VkJyk%3D
    this decodes to "__import__('os').system('echo hacked')"
    Note that in the example, UCE can lead to CMDi!
    """
    user_input = six.ensure_str(request.GET.get("user_input", None))

    # provide altchars to ensure a call to str.translate()
    decoded_input = base64.b64decode(user_input, altchars="-_")

    eval(decoded_input)

    return render(
        request,
        "unsafe_code_exec.html",
        {
            "result": "decoded input: {}".format(decoded_input),
            "user_input": "user input not displayed to prevent XSS",
        },
    )


def nosqli(request):
    if request.method == "GET":
        return render(request, "nosqli.html")
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        with_kwarg = request.POST.get("with_kwarg", str(False)) == str(True)
        if user_input:
            try:
                method = request.POST["method_to_test"]
            except KeyError:
                raise Exception(
                    "Must indicate which pymongo collection method to test."
                )

            data = run_pymongo(method, user_input, with_kwarg)
            result = [x for x in data]
        else:
            result = "no user input"

    return render(request, "nosqli.html", {"result": result})


def run_pymongo(method, user_input, with_kwarg):
    """
    :param method: Pymongo Collection method to run
    :param user_input: input to pass in to method to run
    :return: any data returned from pymongo query
    """
    client = create_mongo_client()
    db = client.pymongo_test_db

    data = []
    if method == "find":
        data = (
            db.posts.find(filter={"title": user_input})
            if with_kwarg
            else db.posts.find({"title": user_input})
        )
    elif method == "insert_one":
        new_record = json.loads(user_input)
        db.posts.insert_one(document=new_record) if with_kwarg else db.posts.insert_one(
            new_record
        )
    elif method == "insert_many":
        if with_kwarg:
            db.posts.insert_many(documents=[{"title": user_input}])
        else:
            db.posts.insert_many([{"title": user_input}])
    elif method == "update":
        record = {"title": "Old title", "content": "PyMongo is fun!", "author": "Dani"}
        db.posts.insert_one(record)
        db.posts.update_one(record, {"$set": {"title": user_input}})
    elif method == "delete":
        db.posts.delete_one({"title": user_input})
    else:
        raise Exception("Pymongo query for method {} not implemented".format(method))

    return data


def xss(request):
    user_input = request.GET.get("user_input", "")
    should_escape = request.GET.get("django_escape", "False") == "True"

    if should_escape:
        from django.utils.html import escape

        user_input = escape(user_input)
    return render(request, "xss.html", {"user_input": user_input})


def raw_xss_streaming(request):
    user_input = request.GET.get("user_input", "")
    return StreamingHttpResponse(["<p>Looks like xss: " + user_input + "</p>"])


def xss_csv(request):
    user_input = request.GET.get("user_input", "")
    response = HttpResponse(content_type="text/csv")

    # write a csv-like response because agent currently does not support propagation thru the csv module
    response.write(",".join(["First row", user_input, "Bar", "Baz"]))
    return response


def render_to_response(filename, context=None):
    if context is None:
        context = {}
    template = JINJA_ENV.get_template(filename)
    return HttpResponse(template.render(**context))


def xss_jinja(request):
    user_input = request.GET.get("user_input", "")
    return render_to_response("xss.html", {"user_input": user_input})


def xss_mako(request):
    user_input = request.GET.get("user_input", "")

    return render(
        template_name="xss.html",
        context={"user_input": user_input},
        request=request,
        using="mako",
    )


def xss_cookie(request):
    cookie = request.COOKIES["user_input"]
    return render(request, "xss.html", {"user_input": cookie})


@require_http_methods(["POST"])
@csrf_exempt
def cmdi_file(request):
    """
    This view is intended to replicate (more-or-less) the SQLi vuln in djangoat
    """
    uploaded_file = request.FILES["upload"]
    data_path = os.path.join(settings.MEDIA_ROOT, "data")

    # Tests string propagation through path methods
    full_file_name = os.path.join(data_path, uploaded_file.name)
    content = ContentFile(uploaded_file.read())
    default_storage.save(full_file_name, content)

    bak_file_path = full_file_name + ".bak"
    # This is really cheesy isn't it?
    cmdi.do_os_system("cp {} {}".format(full_file_name, bak_file_path))

    return render(request, "cmdi.html")


@require_http_methods(["GET"])
def stream_source(request):
    """
    Emulates the case where a stream is marked as a source
    """
    user_input = b"\x80\x03]q\x00(K\x01K\x02K\x03e."  # [1, 2, 3]
    stream = io.BytesIO(user_input)

    try:
        # This is artificial and would never happen inside a real app, but it
        # allows us to test the case where a stream is treated as a source
        stream.cs__source = True
        result = pickle.load(stream)
    except Exception as e:
        result = str(e)

    return render(
        request, "deserialization.html", {"user_input": "ud", "result": result}
    )


def unvalidated_redirect(request):
    user_input = request.GET.get("user_input", "/cmdi/")
    permanent = request.GET.get("permanent", False)
    return redirect(user_input, permanent=permanent)


@require_http_methods(["GET"])
def two_vulns(request):
    """
    This view contains two vulnerabilities.
    """
    user_input = request.GET.get("user_input", "")

    try:
        cmdi.do_subprocess_popen(user_input)
    except Exception:
        pass

    # Second vulnerability: reflected-xss
    return HttpResponse("<p>{}</p>".format(user_input))


def xpath_injection(request):
    query = request.GET.get("query", "")
    module = request.GET.get("module", "")

    xml_doc = """<foo><bar name='whatever'>42</bar></foo>"""

    result = None

    try:
        if module == "xml":
            node = ElementTree.fromstring(xml_doc)
            result = node.find(query)
        elif module == "lxml":
            node = lxml.etree.fromstring(xml_doc)
            result = node.find(query)
    except Exception as e:
        result = str(e)

    return HttpResponse("<p>result = {}</p>".format(result))


def logout(request):
    DjangoLogout(request)
    return render(request, "logout.html")


def get_dynamic_source(request, request_dict, source):
    user_input = ""

    if source == "parameter":
        user_input = request_dict.get("user_input")
    elif source == "body":
        user_input = request.body
    elif source == "host":
        user_input = request.get_host()
    elif source == "port":
        user_input = request.get_port()
    elif source == "raw_uri":
        user_input = request.get_raw_uri()
    elif source == "files" and request.method == "POST":
        file_stream = request.FILES.get("user_input")
        user_input = file_stream.read()
    elif source == "full_path":
        user_input = request.get_full_path()
    elif source == "full_path_info":
        user_input = request.get_full_path_info()
    elif source == "scheme":
        user_input = request.scheme
    elif source == "encoding":
        user_input = request.encoding
    elif source == "referer_header":
        user_input = (
            request.headers["Referer"]
            if django.VERSION >= (2,)
            else request.META["HTTP_REFERER"]
        )
    elif source == "http_method":
        user_input = request.method

    return user_input


def dynamic_sources(request):
    request_dict = request.POST if request.method == "POST" else request.GET
    source = request_dict.get("source", "")
    user_input = get_dynamic_source(request, request_dict, source)

    if isinstance(user_input, bytes):
        # TODO: PYT-714 be able to remove this conversion when .format can propagate tags
        user_input = str(user_input)

    cmdi.do_os_system("echo {}".format(user_input))

    return HttpResponse("<p>tested sources </p>")


def cookie_source(request):
    user_input = request.COOKIES["user_input"]
    cmdi.do_os_system("echo {}".format(user_input))

    return HttpResponse("<p>echoed cookie: {}</p>".format(user_input))


def header_source(request):
    use_environ = request.environ.get("use_environ", False)

    if use_environ:
        user_input = request.environ.get("HTTP_TEST_HEADER")
    else:
        user_input = (
            request.headers["Test-Header"]
            if django.VERSION >= (2,)
            else request.META["HTTP_TEST_HEADER"]
        )

    cmdi.do_os_system("echo {}".format(user_input))

    return HttpResponse("<p>echoed header: {}</p>".format(user_input))


def header_key_source(request):
    use_environ = request.environ.get("use_environ", False)

    if use_environ:
        source_dict = request.environ
    else:
        source_dict = request.headers if django.VERSION >= (2,) else request.META

    # roundabout way of getting the key we want out of the dictionary without changing its id
    user_input = [
        k for k in source_dict.keys() if k in ("HTTP_TEST_HEADER", "Test-Header")
    ][0]

    cmdi.do_os_system("echo {}".format(user_input))

    return HttpResponse("<p>echoed header key: {}</p>".format(user_input))


def stored_xss(request):
    user_input = request.GET.get("user_input", "hello")
    test_type = request.GET.get("test_type")

    if test_type == "create_method":
        msg = Message.objects.create(name=user_input)
    elif test_type == "init_direct":
        msg = Message(name=user_input)
        msg.save()
    elif test_type == "filter":
        _ = Message.objects.create(name=user_input)
        msgs = Message.objects.filter(name=user_input)
        msg = msgs[0]
    elif test_type == "multi-column":
        msg = Message.objects.create(name=user_input, content=user_input)
    else:
        raise Exception("Pass a test_type to test")

    html = "<p>Looks like xss: " + msg.name + "</p>"
    return HttpResponse(html)


def trust_boundary_violation(request):
    user_input = request.GET.get("user_input")
    setdefault = request.GET.get("setdefault") == "True"

    if setdefault:
        request.session.setdefault("whatever", user_input)
    else:
        request.session["whatever"] = user_input

    return HttpResponse("<p>Trust boundary violation</p>")


def crypto_bad_ciphers(request):
    cipher_result = Blowfish.new(b"example_len16key", mode=Blowfish.MODE_EAX)

    return render(request, "crypto_bad_ciphers.html", {"result": str(cipher_result)})


class Echo:
    def write(self, value):
        return value


def streaming(request):
    # Taken from https://docs.djangoproject.com/en/2.0/howto/outputting-csv/#streaming-large-csv-files
    if request.method == "GET":
        attack = request.GET.get("attack", False)
        if attack:
            rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)
            response = StreamingHttpResponse(
                (writer.writerow(row) for row in rows), content_type="text/csv"
            )
            response[
                "Content-Disposition"
            ] = 'attachment; filename="runescapetrivia.csv"'
            return response
        return render(request, "streaming.html", {"result": ""})
    return render(request, "streaming.html", {"result": "Try a GET Request instead."})


def new_dynamic(request):
    return render(request, "base.html")


def other_dynamic(request):
    return render(request, "base.html")


def dynamic_url_view(request):
    from app.urls import urlpatterns

    user_input = request.GET.get("user_input", "new_dynamic")

    func = new_dynamic if user_input == "new_dynamic" else other_dynamic
    urlpatterns.append(compat_url(r"^{}/?$".format(user_input), func))
    return render(request, "base.html")


def nosqli_seed(request):
    client = create_mongo_client()
    db = client.pymongo_test_db
    posts = db.posts
    post_1 = {
        "id": "Python and MongoDB",
        "content": "PyMongo is fun, you guys",
        "author": "Scott",
    }
    post_2 = {
        "title": "Virtual Environments",
        "content": "Use virtual environments, you guys",
        "author": "Scott",
    }
    post_3 = {
        "title": "Learning Python",
        "content": "Learn Python, it is easy",
        "author": "Bill",
    }
    posts.insert_many([post_1, post_2, post_3])
    return render(request, "nosqli.html", {"error": "DB Seeded."})


def import_package_with_relative_imports(request):
    rm_modules = request.GET.get("rm_sys_mod_entries", None)

    if rm_modules:
        remove_sys_module_entries()

    import_with_relative_imports()

    return HttpResponse("")


def import_sample_namespace_package(request):
    # Deleting top level namespace modules breaks them in py2.
    # Namespace name is cached in sys modules, but shows up
    # as a builtin module in py2.
    import_namespace_package()

    return HttpResponse("")


def import_package_onefile(request):
    rm_modules = request.GET.get("rm_sys_mod_entries", None)

    if rm_modules:
        remove_sys_module_entries()

    import_sample_package_onefile()

    return HttpResponse("")


def import_sample_dist_multiple_tlds(request):
    rm_modules = request.GET.get("rm_sys_mod_entries", None)

    if rm_modules:
        remove_sys_module_entries()

    import_multiple_tlds()

    return HttpResponse("")
