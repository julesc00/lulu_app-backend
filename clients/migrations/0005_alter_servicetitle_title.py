# Generated by Django 4.2.16 on 2024-11-12 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_servicetitle_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicetitle',
            name='title',
            field=models.CharField(default='', max_length=256, unique=True, verbose_name='Titulo del servicio'),
        ),
    ]
