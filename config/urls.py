from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages import views as flatpage_views
from django.contrib.flatpages.sitemaps import FlatPageSitemap

# NOTE: This is needed to control language switcher
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from filebrowser.sites import site as filebrowser

from pengcrest.mode.views import enable_dark_mode, enable_light_mode, exhrate, home

from config.sitemaps import StaticViewSitemap
from pengcrest.users.views import check_username, check_email

sitemaps = {
    "static": StaticViewSitemap,
    # "photologue_galleries": GallerySitemap,
    # "photologue_photos": PhotoSitemap,
}

urlpatterns = [
    # dark mode and light mode urls
    path("dark_mode/", view=enable_dark_mode, name="mode"),
    path("light_mode/", view=enable_light_mode, name="lmode"),
    # path("exchange/", view=exhrate, name="exchange"),

    path("accounts/signup/check-username/", view=check_username, name='check-username'),
    path("accounts/signup/check-email/", view=check_email, name='check-email'),


    path("", view=exhrate, name="home"),
    path("ref/<uid>/", view=home, name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
        "contact/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"
    ),
    path(
        "affiliate-program/", TemplateView.as_view(template_name="pages/affiliate.html"), name="affiliate"
    ),


    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_FILEBROWSER_URL, filebrowser.urls),
    path('admin/', include('admin_honeypot.urls', 'admin_honeypot')),
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ADMIN_DOC_URL, include("django.contrib.admindocs.urls")),


    # User management
    path('rosetta/', include('rosetta.urls')),
    path("users/", include("pengcrest.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),


    # Your stuff: custom urls includes go here
    path('tinymce/', include('tinymce.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# flatpages
if flatpage_views:
    urlpatterns += [
        path(_("terms/"), flatpage_views.flatpage, {"url": "/terms/"}, name="terms"),
        path(_("cookies/"), flatpage_views.flatpage, {"url": "/cookies/"}, name="cookies"),
        path(_("privacy/"), flatpage_views.flatpage, {"url": "/privacy/"}, name="privacy"),
    ]

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path("sitemap.xml/", sitemap, kwargs={"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt/", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = _("PENGCREST ADMIN DASHBOARD")
admin.site.site_title = _("PENGCREST ADMIN DASHBOARD")
admin.site.index_title = _("PENGCREST ADMIN DASHBOARD")
