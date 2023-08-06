# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
try:
    from django.urls import re_path as compat_url
except ImportError:
    from django.conf.urls import url as compat_url

from contrast.test.apptest import django_views as views

apptest_urlpatterns = [
    compat_url(r"^$", views.home),
    compat_url(r"^static-image/?$", views.static_image),
    compat_url(r"^xss-autoescape/?$", views.django_autoescape),
    compat_url(r"^xss-autoescape-safe/?$", views.django_autoescape_safe),
    compat_url(r"^xss-no-autoescape/?$", views.django_no_autoescape),
    compat_url(r"^file-contents/?$", views.file_contents),
    compat_url(r"^uce-base64/?$", views.uce_base64),
    compat_url(r"^cmdi-file/?$", views.cmdi_file),
    compat_url(r"^nosqli/?$", views.nosqli),
    compat_url(r"^stream-source/?$", views.stream_source),
    compat_url(r"^cookie-source/?$", views.cookie_source),
    compat_url(r"^header-source/?$", views.header_source),
    compat_url(r"^header-key-source/?$", views.header_key_source),
    compat_url(r"^xss/?$", views.xss),
    compat_url(r"^xss-jinja/?$", views.xss_jinja),
    compat_url(r"^xss-mako/?$", views.xss_mako),
    compat_url(r"^xss-cookie/?$", views.xss_cookie),
    compat_url(r"^xss-csv/?$", views.xss_csv),
    compat_url(r"^raw-xss-streaming/?$", views.raw_xss_streaming),
    compat_url(r"^logout/?$", views.logout),
    compat_url(r"^unvalidated-redirect/?$", views.unvalidated_redirect),
    compat_url(r"^two-vulns/?$", views.two_vulns),
    compat_url(r"^dynamic-sources/?$", views.dynamic_sources),
    compat_url(r"^stored-xss/?$", views.stored_xss),
    compat_url(r"^xpath-injection/?$", views.xpath_injection),
    compat_url(r"^trust-boundary-violation/?$", views.trust_boundary_violation),
    compat_url(r"^crypto-bad-ciphers/?$", views.crypto_bad_ciphers),
    compat_url(r"^streaming/?$", views.streaming),
    compat_url(r"^dynamic_url_view/?$", views.dynamic_url_view),
    compat_url(
        r"^import_package_with_relative_imports/?$",
        views.import_package_with_relative_imports,
    ),
    compat_url(r"^import_namespace_package/?$", views.import_sample_namespace_package),
    compat_url(r"^import_package_onefile/?$", views.import_package_onefile),
    compat_url(
        r"^import_sample_dist_multiple_tlds/?$", views.import_sample_dist_multiple_tlds
    ),
]
