# Generated by Django 5.2 on 2025-05-15 22:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Fecha y hora de la creación del objeto.', verbose_name='Fecha de creación')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Fecha y hora de la última modificación del objeto.', verbose_name='Fecha de modificación')),
                ('first_name', models.CharField(help_text='Nombre del jugador', max_length=100, verbose_name='Nombre')),
                ('last_name', models.CharField(help_text='Apellidos del jugador', max_length=200, verbose_name='Apellidos')),
                ('sport_name', models.CharField(blank=True, help_text='Nombre que aparece en la camiseta', max_length=100, null=True, verbose_name='Nombre deportivo')),
                ('number', models.PositiveIntegerField(blank=True, help_text='Número de dorsal del jugador', null=True, verbose_name='Dorsal')),
                ('address', models.CharField(help_text='Dirección completa de residencia', max_length=255, verbose_name='Dirección')),
                ('city', models.CharField(help_text='Población de residencia', max_length=100, verbose_name='Población')),
                ('municipality', models.CharField(help_text='Municipio de residencia', max_length=100, verbose_name='Municipio')),
                ('postal_code', models.CharField(help_text='Código postal de residencia', max_length=5, validators=[django.core.validators.RegexValidator(message='El código postal debe tener 5 dígitos', regex='^\\d{5}$')], verbose_name='Código postal')),
                ('nationality', models.CharField(help_text='Nacionalidad del jugador', max_length=100, verbose_name='Nacionalidad')),
                ('identity_document', models.CharField(help_text='Número de documento de identidad', max_length=20, unique=True, verbose_name='Documento de identidad')),
                ('email', models.EmailField(blank=True, help_text='Correo electrónico de contacto', max_length=254, null=True, verbose_name='Correo electrónico')),
                ('phone', models.CharField(help_text='Teléfono de contacto', max_length=15, validators=[django.core.validators.RegexValidator(message='El número de teléfono debe estar en formato: +999999999.', regex='^\\+?1?\\d{9,15}$')], verbose_name='Teléfono')),
                ('photo', models.ImageField(blank=True, help_text='Fotografía del jugador', null=True, upload_to='players/photos/', verbose_name='Fotografía')),
            ],
            options={
                'verbose_name': 'Jugador',
                'verbose_name_plural': 'Jugadores',
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
