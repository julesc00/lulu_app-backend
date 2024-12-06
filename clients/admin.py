from django import forms
from django.contrib import admin

from clients.forms import ServiceTitleForm, AppointmentForm
from clients.models import (
    Client, Address, Service, ServiceTitle, Appointment, Agreement, Questionnaire)


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'email', 'phone', 'sex', 'age',)

    def treatment_history(self, obj):
        return ", ".join([service.title for service in obj.treatment_history.all()])

    treatment_history.short_description = "Historial de servicios | tratamientos"


class AgreementAdmin(admin.ModelAdmin):
    list_display = ("client", "date_created", "is_agreed", "beautician",)


class AppointmentAdmin(admin.ModelAdmin):
    # form = AppointmentForm
    list_display = (
            "client","appointment_date",
            "formatted_services", "beautician", "location", "notes", "google_event_id",
        )
    fieldsets = (
        (None, {
            "fields": ("client", "services", "appointment_date", "google_event_id", "beautician", "location"),
            "description": "Aquí puedes vincular servicios a un cliente."
        }),
    )
    readonly_fields = ("google_event_id",)

    def formatted_services(self, obj):
        return ", ".join([str(service) for service in obj.services.all()])

    formatted_services.short_description = "Servicios"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("client", "formatted_titles", "agreement", "date_created", "date_updated", "notes",)
    fieldsets = (
        (None, {
            "fields": ("client", "agreement", "titles", "notes", "image"),
            "description": "Aquí puedes vincular servicios a un cliente."
        }),
    )

    def formatted_titles(self, obj):
        return ", ".join([str(service) for service in obj.titles.all()])

    formatted_titles.short_description = "Servicios"


class AddressAdmin(admin.ModelAdmin):
    list_display = ("client", "address", "city", "state",)


admin.site.register(Client, ClientAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(ServiceTitle)
admin.site.register(Agreement, AgreementAdmin)
# admin.site.register(Service)
admin.site.register(Questionnaire)
