from django.test import TestCase
from django.utils.translation import gettext_lazy as _
from ..models.season_models import Season

class SeasonModelTest(TestCase):
    def setUp(self):
        self.season = Season.objects.create(
            name="Temporada 2023-2024",
            start_date="2023-08-01",
            end_date="2024-06-30",
            is_active=True
        )

    def test_season_creation(self):
        self.assertEqual(self.season.name, "Temporada 2023-2024")
        self.assertTrue(self.season.is_active)
