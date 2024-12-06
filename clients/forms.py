
from django import forms
from django.forms import DateTimeInput, ModelForm, Form
from django.forms.widgets import DateTimeInput
from django.contrib import admin
from bootstrap_datepicker_plus.widgets import DatePickerInput
from phonenumber_field.formfields import PhoneNumberField

from clients.models import ServiceTitle, Appointment, Client, Agreement, Questionnaire
from clients.choices import services2


class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'],  # Set your desired format here
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    class Meta:
        model = Appointment
        fields = (
            "client", "google_event_id","appointment_date",
            "services", "beautician", "location", "notes"
        )
        widgets = {
            "appointment_date": DateTimeInput(attrs={
                "class": "form-control",
                "type": "datetime-local",
                "step": 900
            },
            format='%Y-%m-%d %H:%M')
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['appointment_date'].input_formats = ['%Y-%m-%d %H:%M']


class ServiceTitleForm(forms.ModelForm):
    service_titles = forms.ModelMultipleChoiceField(
        queryset=ServiceTitle.objects.all()
    )
    class Meta:
        model = ServiceTitle
        fields = ("service_titles",)
        widgets = {
            "title": forms.MultipleChoiceField(
                choices=services2,
                widget=forms.CheckboxSelectMultiple()
            )
        }


class AgreementForm(ModelForm):
    class Meta:
        model = Agreement
        fields = ("client", "beautician", "is_agreed", "service",)

    is_agreed = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input",
            "placeholder": "Estoy de acuerdo"
        }),
        label="Estoy de acuerdo",
        required=True,
        error_messages={"required": "Debe aceptar el consentimiento para continuar."}
    )





class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ("name", "lastname", "email", "phone", "sex", "age",
                  "date_of_birth", "civil_status", "occupation", "treatment_history",)

        name = forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre',
                'aria-label': 'Nombre'
            }),
            label="Nombre"
        )
        lastname = forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellidos',
                'aria-label': 'Apellidos'
            }),
            label="Apellidos"
        )
        email = forms.EmailField(
            required=False,
            widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Correo electrónico',
                'aria-label': 'Correo electrónico'
            }),
            label="Correo electrónico"
        )
        phone = PhoneNumberField(
            region="MX",
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+52 123 456 7890',
                'aria-label': 'Teléfono'
            }),
            label="Teléfono"
        )
        sex = forms.ChoiceField(
            choices=Client.SEX_CHOICES,
            widget=forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Sexo'
            }),
            label="Sexo"
        )
        age = forms.IntegerField(
            widget=forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 120,
                'aria-label': 'Edad',
                'placeholder': 'Edad'
            }),
            label="Edad"
        )
        date_of_birth = forms.DateField(
            widget=DatePickerInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fecha de Nacimiento - ej. dd/mm/aaaa',
                'aria-label': 'Fecha de Nacimiento'
            }),
            label="Fecha de Nacimiento - ej. dd/mm/aaaa"
        )
        civil_status = forms.ChoiceField(
            choices=Client.CIVIL_STATUS,
            widget=forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Estado Civil'
            }),
            label="Estado Civil"
        )
        occupation = forms.CharField(
            max_length=100,
            required=False,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ocupación',
                'aria-label': 'Ocupación'
            }),
            label="Ocupación"
        )
        treatment_history = forms.ModelMultipleChoiceField(
            queryset=ServiceTitle.objects.all(),
            required=False,
            widget=forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check',
                'aria-label': 'Historial de servicios | tratamientos'
            }),
            label="Historial de servicios | tratamientos"
        )


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = [
            "client",
            "previous_treatment",
            "had_botox",
            "boto_type",
            "historic_treatments",
            "birth_control_pills",
            "is_pregnant",
            "body_prothesis",
            "is_allergic",
            "allergies",
            "is_anemic",
            "under_medical_control",
            "medical_treatment",
            "current_illnesses",
            "chronic_illnesses",
            "coagulation_problems",
            "social_plans",
            "is_drinker",
            "is_smoker",
        ]

        # Optionally, customize field labels or widgets if needed
        labels = {
            "client": "Cliente",
            "previous_treatment": "Tratamientos previos",
            "had_botox": "Ha usado botox antes?",
            "boto_type": "Tipo de botox",
            "historic_treatments": "Tratamientos previos",
            "birth_control_pills": "Usa píldoras anticonceptivas?",
            "is_pregnant": "Está embarazada?",
            "body_prothesis": "Tiene prótesis?",
            "is_allergic": "Es alérgico(a) a algo?",
            "allergies": "Alergias",
            "is_anemic": "Es anémico(a)?",
            "under_medical_control": "Está bajo control médico?",
            "medical_treatment": "Tratamiento médico",
            "current_illnesses": "Padecimientos actuales",
            "chronic_illnesses": "Enfermedades crónicas",
            "coagulation_problems": "Problemas de coagulación?",
            "social_plans": "Planes sociales",
            "is_drinker": "Ingiere alcohol?",
            "is_smoker": "Es fumador(a)?",
        }

        widgets = {
            "boto_type": forms.TextInput(attrs={"placeholder": "Especifique el tipo de botox"}),
            "allergies": forms.TextInput(attrs={"placeholder": "Especifique alergias si las tiene"}),
            "medical_treatment": forms.TextInput(attrs={"placeholder": "Especifique el tratamiento médico"}),
            "current_illnesses": forms.Textarea(attrs={"placeholder": "Especifique padecimientos actuales"}),
            "chronic_illnesses": forms.TextInput(attrs={"placeholder": "Especifique enfermedades crónicas"}),
            "social_plans": forms.TextInput(attrs={"placeholder": "Planes sociales"}),
        }


class ConsentForm(forms.Form):
    accept_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input"
        }),
        label="Acepto los términos y condiciones"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["accept_terms"].label = f"Acepte los términos y condiciones para {user.username}."
        else:
            self.fields["accept_terms"].label = f"Acepte los términos y condiciones."
        self.fields["accept_terms"].help_text = "Por favor, lea y acepte los términos y condiciones antes de continuar."

