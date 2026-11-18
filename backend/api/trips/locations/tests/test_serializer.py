
from decimal import Decimal
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from api.trips.locations.serializers import LocationSerializer
from api.trips.locations.models import Location
from api.trips.models import Trip


class LocationSerializerTestCase(TestCase):

    def setUp(self):
        self.trip = Trip.objects.create(
            name="Paris Trip",
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=5)
        )

        self.valid_data = {
            "name": "Eiffel Tower",
            "description": "Iconic landmark in Paris.",
            "latitude": "48.858370",
            "longitude": "2.294481"
        }

    def test_serialize_location(self):
        """Test serializing a Location instance"""
        location = Location.objects.create(**self.valid_data, trip=self.trip)

        serializer = LocationSerializer(location)

        self.assertEqual(serializer.data["name"], "Eiffel Tower")
        self.assertEqual(serializer.data["description"], "Iconic landmark in Paris.")
        self.assertEqual(serializer.data["latitude"], "48.858370")
        self.assertEqual(serializer.data["longitude"], "2.294481")
        self.assertIn("id", serializer.data)

    def test_deserialize_valid_data(self):
        """Test deserializing valid data"""
        serializer = LocationSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["name"], "Eiffel Tower")
        self.assertEqual(serializer.validated_data["latitude"], Decimal("48.858370"))
        self.assertEqual(serializer.validated_data["longitude"], Decimal("2.294481"))

    def test_missing_required_field(self):
        """Test deserializing data with a missing required field"""
        data = self.valid_data.copy()
        del data["name"]

        serializer = LocationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_latitude(self):
        """Test deserializing data with an invalid latitude"""
        data = self.valid_data.copy()
        data["latitude"] = "invalid"

        serializer = LocationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("latitude", serializer.errors)

    def test_invalid_longitude(self):
        """Test deserializing data with an invalid longitude"""
        data = self.valid_data.copy()
        data["longitude"] = "invalid"

        serializer = LocationSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("longitude", serializer.errors)
