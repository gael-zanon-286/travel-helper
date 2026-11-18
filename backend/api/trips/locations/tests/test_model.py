from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from api.trips.models import Trip
from api.trips.locations.models import Location


class LocationModelTestCase(TestCase):

    def setUp(self):
        self.trip = Trip.objects.create(
            name="Paris Trip",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=5)
        )

        self.location = Location.objects.create(
            name="Eiffel Tower",
            description="Iconic landmark in Paris.",
            latitude=48.858370,
            longitude=2.294481,
            trip=self.trip
        )

    def test_create_location(self):
        """Persistence testing"""
        self.assertIsNotNone(self.location.pk)
        self.assertEqual(self.location.name, "Eiffel Tower")
        self.assertEqual(self.location.description, "Iconic landmark in Paris.")
        self.assertEqual(float(self.location.latitude), 48.858370)
        self.assertEqual(float(self.location.longitude), 2.294481)

    def test_location_trip_relationship(self):
        """Test the relationship between Location and Trip"""
        self.assertEqual(self.location.trip, self.trip)
        self.assertIn(self.location, self.trip.locations.all())

    def test_deleting_trip_deletes_locations(self):
        """Cascading relationships test (Locations are removed when a trip is deleted)"""
        location_id = self.location.id

        self.trip.delete()

        self.assertFalse(Location.objects.filter(id=location_id).exists())