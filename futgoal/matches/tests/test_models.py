from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from futgoal.season.models import Season
from futgoal.team.models import Team
from futgoal.matches.models import Match


class MatchModelTest(TestCase):
    """Tests para el modelo Match"""

    def setUp(self):
        """Configuración inicial para los tests"""
        # Crear una temporada activa
        self.season = Season.objects.create(
            name="Temporada 2024",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=365),
            is_active=True
        )

        # Crear un equipo
        self.team = Team.objects.create(
            name="Club Deportivo Test"
        )

    def test_match_creation(self):
        """Test de creación básica de un partido"""
        match = Match.objects.create(
            away_team="Equipo Rival",
            match_date=timezone.now() + timedelta(days=7),
            match_type="friendly",
            status="scheduled"
        )

        self.assertEqual(match.season, self.season)
        self.assertEqual(match.away_team, "Equipo Rival")
        self.assertEqual(match.status, "scheduled")
        self.assertTrue(match.is_home)

    def test_match_str_representation(self):
        """Test de representación string del partido"""
        match = Match.objects.create(
            away_team="Equipo Rival",
            match_date=timezone.now() + timedelta(days=7),
        )

        self.assertIn("vs Equipo Rival", str(match))

    def test_automatic_season_assignment(self):
        """Test de asignación automática de temporada"""
        match = Match(
            away_team="Equipo Rival",
            match_date=timezone.now() + timedelta(days=7),
        )
        match.save()

        self.assertEqual(match.season, self.season)
