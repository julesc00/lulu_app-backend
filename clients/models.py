
from datetime import datetime, timedelta, time

import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from PIL import Image


from clients.choices import services2


SEX_CHOICES = (
    ("male", "Masculino"),
    ("female", "Femenino")
)

BEAUTICIAN_OPTIONS = (
    ("lulu", "Lulú"),
)
APPLICATION_LOCATION = (
    ("principal", "Principal: López Mateos #155, Tepatitlán"),
    ("client_address", "A domicilio del cliente")
)
YES_NO_CHOICES = (
    ("yes", "Sí"),
    ("no", "No"),
)

def get_secret():
    """Get google secrets from AWS Secrets Manager."""
    secret_name = "prod/lulu_app/google_creds"
    region = "us-east-1"
    session = boto3.session.Session()
    client = session.client(
        service_name="secrets_manager",
        region_name=region
    )
    try:
        res = client.get_secret_value(
            SecretId=secret_name
        )
        secret = res.get("SecretString")
    except ClientError as err:
        print(f"[ERROR] {err}")
        secret = None

    return secret


def get_calendar_service():
    secret = get_secret()
    credentials = service_account.Credentials.from_service_account_info(
        secret
    )

    service = build("calendar", "v3", credentials=credentials)
    current_date = timezone.now().date()
    start_date = timezone.make_aware(
        timezone.datetime.combine(current_date, timezone.datetime.min.time().replace(hour=9)))
    end_date = timezone.make_aware(
        timezone.datetime.combine(current_date, timezone.datetime.min.time().replace(hour=20)))

    # Retrieve current time zone settings
    settings_response = service.events().list(calendarId='primary').execute()
    time_zone_id = next((setting['id'] for setting in settings_response.get('items', []) if
                         setting['kind'] == 'calendar#setting' and setting['name'] == 'timeZone'), None)

    if time_zone_id:
        # Update time zone settings to show all hours
        hours = [f"{i:02d}:00" for i in range(24)]
        updated_setting = {'id': time_zone_id, 'value': {'timeZone': 'America/New_York', 'hours': hours}}
        service.settings().update(calendarId='primary', settingId=time_zone_id, body=updated_setting).execute()
    else:
        print("[WARNING] Fallo a obtener o actualizar la zona horaria")

    return service


def validate_business_hours(value):
    if not (time(9, 0) <= value.time() <= time(19, 0)):
        raise ValidationError("La cita tiene que ser entre 9:00 AM and 7:00 PM.")


def validate_birth_date(value) -> None:

    today = timezone.now()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

    if value.year > today.year:
        raise ValidationError("La fecha de nacimiento no puede ser en el futuro.")
    if age > 120:
        raise ValidationError("La edad no puede ser mayor a 120 años.")

def validate_appointment_date(value) -> None:
    today = timezone.now()
    if value < today:
        raise ValidationError("La fecha de su cita no puede ser en el pasado, elija una nueva fecha.")


def validate_image_size(image) -> None:
    max_size_kb = 2048
    if image.size > max_size_kb:
        raise ValidationError(f"[INFO] La imagen es demasiado grande (> {max_size_kb} KB).")


def validate_image_dimensions(image):
    img = Image.open(image)
    if img.height < 200 or img.width < 200:
        raise ValidationError("[INFO] The image is too small. Minimum size is 200x200 pixels.")


def agreement_upload_path(instance, filename):
    client_name = instance.client.name.replace(" ", "_")
    client_lastname = instance.client.lastname.replace(" ", "_")
    return f"consentimientos/{instance.date_created:%Y-%m-%d}/{client_name}-{client_lastname}/{filename}"


class ServiceTitle(models.Model):
    title = models.CharField(
        max_length=256,
        choices=services2,
        unique=True,
        default="",
        verbose_name="Titulo del servicio"
    )

    class Meta:
        verbose_name = _("Servicio | Tratamiento")
        verbose_name_plural = _("Servicios | Tratamientos")

    def __str__(self):
        return self.title


class Client(models.Model):
    SEX_CHOICES = (
        ("male", "Masculino"),
        ("female", "Femenino")
    )
    CIVIL_STATUS = (
        ("single", "Soltero(a)"),
        ("in_relationship", "En relación"),
    )

    name = models.CharField(max_length=100, verbose_name="Nombre")
    lastname = models.CharField(max_length=100, verbose_name="Apellidos")
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(region="MX", verbose_name="Teléfono", max_length=15)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, verbose_name="Sexo", default="Femenino")
    age = models.PositiveIntegerField(validators=[
        MinValueValidator(0), MaxValueValidator(120)], verbose_name="Edad")
    date_of_birth = models.DateField(
        validators=[validate_birth_date],
        verbose_name="Fecha de Nacimiento - ej. dd/mm/aaaa")
    civil_status = models.CharField(
        max_length=15,
        choices=CIVIL_STATUS,
        default="soltero(a)",
        verbose_name="Estado Civil")
    occupation = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ocupación")
    treatment_history = models.ManyToManyField(
        ServiceTitle,
        blank=True,
        related_name="client_treatment_history",
        verbose_name="Historial de servicios | tratamientos")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def clean(self):
        self.name = self.name.title()
        self.lastname = self.lastname.title()

    def __str__(self):
        return f"{self.name} {self.lastname}"


class Address(models.Model):
    """
    This model will be autofilled from
    Google Places API Autocomplete Library coming
    from the frontend.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_query_name="addresses", verbose_name="Cliente")
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name="Domicilio")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    state = models.CharField(max_length=100, verbose_name="Estado")
    zip_code = models.CharField(max_length=10, verbose_name="Código Postal")
    # TODO: Set the proper city field from Google places or somenthing similar.

    class Meta:
        verbose_name = "Domicilio"
        verbose_name_plural = "Domicilios"

    def __str__(self):
        return f"{self.address}, {self.city}, CP: {self.zip_code}"


class Questionnaire(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="questionnaires",
        verbose_name="Cliente")
    previous_treatment = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Tratamientos previos")
    had_botox = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Ha usado botox antes?")
    boto_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo de botox")
    historic_treatments = models.TextField(blank=True, null=True, verbose_name="Historial de tratamientos")
    birth_control_pills = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Usa píldoras de contra el embarazo")
    is_pregnant = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Está embarazada")
    body_prothesis = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Tiene prótesis")
    is_allergic = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Es alérgico(a) a algo")
    allergies = models.CharField(max_length=256, blank=True, null=True, verbose_name="Alergias")
    is_anemic = models.CharField(max_length=5,choices=YES_NO_CHOICES, default="no", verbose_name="Es anémico(a)")
    under_medical_control = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Bajo control médico")
    medical_treatment = models.CharField(max_length=256, blank=True, null=True, verbose_name="Tratamiento médico")
    current_illnesses = models.TextField(blank=True, null=True, verbose_name="Padecimientos")
    chronic_illnesses = models.CharField(max_length=256, blank=True, null=True, verbose_name="Enfermedades crónicas")
    coagulation_problems = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Problemas de coagulación")
    social_plans = models.CharField(max_length=256, blank=True, null=True, verbose_name="Planes sociales")
    is_drinker = models.CharField(max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Ingiere alcohol")
    is_smoker = models.CharField(max_length=5, choices=YES_NO_CHOICES, default="no", verbose_name="Es fumador(a)")

    class Meta:
        verbose_name = "Cuestionario"
        verbose_name_plural = "Cuestionarios"

    def __str__(self):
        return f"Cuestionario de: {self.client.name} {self.client.lastname}"


class Agreement(models.Model):
    # agreement_id = models.UUIDField(default=uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_query_name="consentimientos", verbose_name="Cliente")
    beautician = models.CharField(max_length=100, choices=BEAUTICIAN_OPTIONS, default="Lulú", verbose_name="Esteticista")
    service = models.ManyToManyField(
        ServiceTitle,
        verbose_name="Servicio solicitado",
        related_name="solicited_service",
        blank=True
    )
    is_agreed = models.BooleanField(default=False, verbose_name="Aceptó el Consentimiento")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creado")
    agreement_file = models.FileField(
        upload_to=agreement_upload_path,
        blank=True,
        verbose_name="Archivo del Consentimiento")

    class Meta:
        verbose_name = "Consentimiento"
        verbose_name_plural = "Consentimientos"

    def __str__(self):
        return f"Acuerdo de: {self.client.name.title()} {self.client.lastname.title()}"


class Service(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="services", verbose_name="Cliente")
    agreement = models.ForeignKey(
        Agreement, on_delete=models.CASCADE, related_name="consentimientos",
        blank=True, null=True, verbose_name="Consentimiento")
    titles = models.ManyToManyField(
        ServiceTitle,
        related_name="service_titles",
        verbose_name="Servicios | Tratamientos")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha creado")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas | Observaciones")
    image = models.ImageField(
        upload_to="images/",
        validators=[FileExtensionValidator(
            ["jpg","JPG", "jpeg", "JPEG", "png", "PNG", "webp"]),
            validate_image_size,
            validate_image_dimensions
        ],
        blank=True,
        null=True, verbose_name="Imágenes"
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 1024 or img.width > 1024:
                output_size = (1024, 1024)
                img.thumbnail(output_size)
                img.save(self.image.path)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return f"{self.client.name} {self.client.lastname} | {', '.join([title.title for title in self.titles.all()])}"


class Appointment(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Cliente"
    )
    services = models.ManyToManyField(
        ServiceTitle,
        related_name="service_appointments",
        verbose_name="Servicios | Tratamientos")
    appointment_date = models.DateTimeField(
        validators=[validate_business_hours], default=timezone.now, verbose_name="Fecha de cita")
    google_event_id = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="ID de evento",
        help_text="Puede dejar este espacio en blanco")
    beautician = models.CharField(
        max_length=100,
        default="Lulú",
        choices=BEAUTICIAN_OPTIONS,
        verbose_name="Esteticista")
    location = models.CharField(
        max_length=100,
        default="Principal: López Mateos #155, Tepatitlán",
        choices=APPLICATION_LOCATION,
        verbose_name="Lugar de aplicación", help_text="Opciones: A domicilio, instalaciones Lulú")
    notes = models.TextField(blank=True, null=True, verbose_name="Notas")

    def save(self, *args, **kwargs):
        # Only create Google Calendar event if google_event_id is not already set
        if not self.google_event_id:
            self.create_google_event()
        super().save(*args, **kwargs)

    def formatted_appointment_date(self):
        return self.appointment_date.astimezone(timezone.get_current_timezone()).strftime("%A, %d de %B, %Y %I:%M %p")

    def create_google_event(self):
        service = get_calendar_service()
        event = {
            "summary": "Cita",
            "location": self.location,
            "description": f"Cita con {self.beautician}",
            "start": {
                "dateTime": self.appointment_date.isoformat(),
                "timeZone": "America/Mexico_City",
            },
            "end": {
                "dateTime": (self.appointment_date + timedelta(hours=1)).isoformat(),
                "timeZone": "America/Mexico_City",
            },
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()
        self.google_event_id = created_event["id"]

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"

    def __str__(self):
        return f"Cliente: {self.client.name} {self.client.lastname} | Fecha de cita: {self.formatted_appointment_date()}"


@receiver(post_save, sender=Appointment)
def handle_appointment_save(sender, instance, created, **kwargs):
    if created and not instance.google_event_id:
        instance.create_google_event()

@receiver(post_delete, sender=Appointment)
def handle_appointment_delete(sender, instance, **kwargs):
    if instance.google_event_id:
        service = get_calendar_service()
        try:
            service.events().delete(calendarId="primary", eventId=instance.google_event_id).execute()
        except HttpError:
            pass
