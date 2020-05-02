# -*- coding: utf-8 -*-

import json

from django.utils.safestring import mark_safe


def generate_site_navigation_element_json_ld(name, url):
    return mark_safe(json.dumps({
        "@context": "http://schema.org",
        "@type": "SiteNavigationElement",
        "name": mark_safe(name),
        "url": mark_safe(url)
    }, ensure_ascii=False))
