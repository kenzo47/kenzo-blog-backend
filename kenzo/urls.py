from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from wagtail.admin import urls as wagtailadmin_urls
from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

urlpatterns = [
    path("admin/autocomplete/", include(autocomplete_admin_urls)),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [  # noqa: RUF005
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1/blog/", include("blog.urls", namespace="blog"), name="blog"),
]
