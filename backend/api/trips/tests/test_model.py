from datetime import datetime, timezone

from django.test import TestCase
from api.trips.models import Trip


class TripTestCase(TestCase):
    def setUp(self):
        Trip.objects.create(
            name="This is my testing trip",
            start_date=datetime(2027, 6, 10, 10, 0, tzinfo=timezone.utc),
            end_date=datetime(2027, 6, 15, 18, 0, tzinfo=timezone.utc))

    def test_invalid_trip(self):
        with self.assertRaises(Trip.DoesNotExist):
            Trip.objects.get(name="Invalid Trip")

    def test_get_trip(self):
        """Trips can be retrieved"""
        trip = Trip.objects.get(name="This is my testing trip")
        self.assertEqual(trip.name, 'This is my testing trip')

    def test_update_trip(self):
        """Trips can be updated"""
        trip = Trip.objects.get(name="This is my testing trip")
        trip.name = "Modified testing trip"
        trip.save(update_fields=["name"])
        self.assertEqual(trip.name, 'Modified testing trip')

    def test_create_trip(self):
        """Trips can be created"""
        trip = Trip.objects.create(
            name="My new Trip",
            start_date=datetime(2027, 8, 10, 10, 0, tzinfo=timezone.utc),
            end_date=datetime(2027, 8, 15, 18, 0, tzinfo=timezone.utc)
        )
        self.assertEqual(trip.name, 'My new Trip')

    def test_delete_trip(self):
        """Trips can be deleted"""
        trip = Trip.objects.get(name="This is my testing trip")
        trip.delete()
        trips = Trip.objects.all()
        self.assertEqual(len(trips), 0)