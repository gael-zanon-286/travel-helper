
from datetime import datetime, timezone

from django.test import TestCase
from api.trips.models import Trip
from api.trips.serializers import TripSerializer


class TripSerializerTestCase(TestCase):

    def setUp(self):
        self.valid_data = {
            "name": "This is my testing Trip",
            "start_date": "2027-06-10T10:00:00Z",
            "end_date": "2027-06-15T18:00:00Z"
        }

    def test_valid_data(self):
        serializer = TripSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid())

    def test_missing_required_field(self):
        """Test that the serializer raises a validation error when a required field is missing."""
        data = self.valid_data.copy()
        del data["name"]

        serializer = TripSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_name_exceeds_max_length(self):
        """Test that the serializer raises a validation error when the name exceeds the maximum length."""
        data = self.valid_data.copy()
        data["name"] = "A" * 101

        serializer = TripSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_date_format(self):
        """Test that the serializer raises a validation error when the date format is invalid."""
        data = self.valid_data.copy()
        data["start_date"] = "not-a-date"

        serializer = TripSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("start_date", serializer.errors)

    def test_serializer_output(self):
        """Test that the serializer outputs the correct data."""
        trip = Trip.objects.create(
            name="My new Trip",
            start_date=datetime(2027, 6, 10, 10, 0, tzinfo=timezone.utc),
            end_date=datetime(2027, 6, 15, 18, 0, tzinfo=timezone.utc)
        )

        serializer = TripSerializer(trip)

        self.assertEqual(serializer.data["name"], "My new Trip")
        self.assertEqual(serializer.data["id"], trip.id)
