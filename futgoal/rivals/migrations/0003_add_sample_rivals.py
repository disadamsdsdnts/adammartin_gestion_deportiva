# Generated manually for testing
from django.db import migrations

def create_sample_rivals(apps, schema_editor):
    Rival = apps.get_model('rivals', 'Rival')

    sample_rivals = [
        {
            'name': 'CD Real Betis B',
            'coach_name': 'Paco López',
            'field_name': 'Ciudad Deportiva Luis del Sol',
            'city': 'Sevilla',
            'coach_phone': '954123456',
            'coach_email': 'paco.lopez@realbetis.es',
            'notes': 'Filial del Real Betis. Equipo muy técnico.'
        },
        {
            'name': 'Sevilla FC C',
            'coach_name': 'Miguel Ángel',
            'field_name': 'José Ramón Cisneros Palacios',
            'city': 'Sevilla',
            'coach_phone': '954654321',
            'coach_email': 'miguel.angel@sevillafc.es',
            'notes': 'Filial del Sevilla FC. Juego físico y directo.'
        },
        {
            'name': 'CD Alcalá',
            'coach_name': 'Antonio Ruiz',
            'field_name': 'Campo Municipal de Deportes',
            'city': 'Alcalá de Guadaíra',
            'coach_phone': '955123789',
            'coach_email': 'antonio.ruiz@cdalcala.com',
            'notes': 'Equipo histórico de la provincia. Muy competitivo en casa.'
        }
    ]

    for rival_data in sample_rivals:
        Rival.objects.create(**rival_data)

def remove_sample_rivals(apps, schema_editor):
    Rival = apps.get_model('rivals', 'Rival')
    Rival.objects.filter(
        name__in=['CD Real Betis B', 'Sevilla FC C', 'CD Alcalá']
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('rivals', '0002_rival_seasons'),
    ]

    operations = [
        migrations.RunPython(
            create_sample_rivals,
            remove_sample_rivals
        ),
    ]
