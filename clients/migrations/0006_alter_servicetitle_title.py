# Generated by Django 4.2.16 on 2024-11-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_alter_servicetitle_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetitle',
            name='title',
            field=models.CharField(choices=[('Sin consentimiento', (('aplicacion_pestañas', 'Aplicación de pestañas'), ('desintoxicacion_ionica', 'Desintoxicación iónica'), ('derpamen', 'Derpamen'), ('diseño_cejas', 'Diseño de cejas'), ('lifting_pestañas', 'Lifting de pestañas'), ('limpieza_oidos', 'Limpieza de oídos'), ('pedicure_spa', 'Pedicure SPA'), ('facial', 'Facial'), ('hollywood_pell', 'Hollywood pell'), ('depilacion_laser', 'Depilación laser'), ('masaje:drenaje', 'Masaje: Drenaje linfático brasileño'), ('masaje:reductivo', 'Masaje: Reductivo'), ('masaje:moldeador', 'Masaje: Moldeador'), ('masaje:anticelulitis', 'Masaje: Anti celulitis'), ('masaje:aparatologia', 'Masaje: Aparatología'))), ('Con consentimiento', (('acido_hialuronico:labios', 'Acido hialurónico - labios'), ('acido_hialuronico:nariz', 'Acido hialurónico - nariz'), ('acido_hialuronico:menton', 'Acido hialurónico - mentón'), ('toxina_botuliniea', 'Toxina Botulíniea - Botox'), ('fibroblast:eliminacion_verrugas', 'Fibroblast: Eliminación de verrugas'), ('fibroblast:eliminacion_tatuajes', 'Fibroblast: Eliminación de tatuajes')))], default='', max_length=256, unique=True, verbose_name='Titulo del servicio'),
        ),
    ]
