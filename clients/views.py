from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from clients.models import Agreement, Client
from clients.forms import AgreementForm, ClientForm, QuestionnaireForm, ConsentForm

C_INDEX = "clients/index.html"


class IndexPageView(TemplateView):
    template_name = C_INDEX


@login_required(login_url="account_login")
def client_form_view(request):
    form = ClientForm

    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            new_client = form.save(commit=False)
            new_client.username = request.user
            new_client.save()
            new_client.save_m2m()
            return redirect("clients:consent")
        form = ClientForm()
    context = {
        "form": form
    }
    return render(request, template_name=C_INDEX, context=context)


class AboutPageView(TemplateView):
    template_name = "clients/about.html"


class AgreementView(DetailView, FormView, ListView):
    model = Agreement
    template_name = "clients/consent.html"
    form_class = AgreementForm
    context_object_name = "consent"
    success_url = reverse_lazy("success_page")

    def get_object(self, queryset=None):
        agreement_id = int(self.kwargs.get("id"))
        return get_object_or_404(Agreement, pk=agreement_id)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.get_object()
        return kwargs


class QuestionnaireFormView(FormView):
    template_name = "clients/index.html"
    form_class = ClientForm
    success_url = reverse_lazy("form-success")

    def form_valid(self, form):
        # Create email

        return super().form_valid(form)


def consent_view(request):
    form = ConsentForm(user=request.user, initial={
        "accept_terms": "Accept me punk!"
    })
    context = {"form": form}
    return render(request, template_name="clients/consent.html", context=context)
