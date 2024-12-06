from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path ("api/v1.0/", include("api.urls")),
    path("", RedirectView.as_view(url="clients/", permanent=True)),
    path("clients/", include("clients.urls")),
    path("accounts/", include("allauth.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    import debug_toolbar  # it is there, but lints it, don't know why

    urlpatterns = [
                      path("__debug__/", include(debug_toolbar.urls)),
                  ] + urlpatterns
