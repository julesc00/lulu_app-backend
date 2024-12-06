from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from clients.views import (
    AgreementView,
    IndexPageView,
    AboutPageView,
    QuestionnaireFormView,
    consent_view,
    client_form_view
)

app_name = "clients"

urlpatterns = [
    path("", IndexPageView.as_view(), name="index"),
    path("client-form/", client_form_view, name="client_form"),
    path("questionnaire/", QuestionnaireFormView.as_view(), name="questionnaire"),
    path("consent/", consent_view, name="consent"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("agreement/<int:pk>/", AgreementView.as_view(), name="agreement-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
