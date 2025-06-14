# Generated by Django 5.2 on 2025-06-08 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0004_matchplayerstats'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchplayerstats',
            name='attended',
            field=models.BooleanField(default=True, help_text='Indica si el jugador asistió al partido', verbose_name='Asistió al partido'),
        ),
    ]
