from __future__ import absolute_import

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    def items(self):
        return ["home", "cookies", "privacy", "terms"]

    def location(self, item):
        return reverse(item)
