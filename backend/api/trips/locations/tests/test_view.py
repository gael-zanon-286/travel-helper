
from datetime import timedelta
from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from api.trips.models import Trip
from api.trips.locations.models import Location


class LocationViewTestCase(APITestCase):

    def setUp(self):
        now = timezone.now()

        self.trip = Trip.objects.create(
            name="Paris Trip",
            start_date=now,
            end_date=now + timedelta(days=5)
        )

        self.other_trip = Trip.objects.create(
            name="London Trip",
            start_date=now,
            end_date=now + timedelta(days=5)
        )

        self.location = Location.objects.create(
            name="Eiffel Tower",
            description="Iconic landmark in Paris.",
            latitude=Decimal("48.858370"),
            longitude=Decimal("2.294481"),
            trip=self.trip
        )

        self.valid_data = {
            "name": "Louvre Museum",
            "description": "World-famous art museum in Paris.",
            "latitude": "48.860600",
            "longitude": "2.337600"
        }

        self.collection_url = reverse(
            "location",
            kwargs={"trip_id": self.trip.pk}
        )

        self.detail_url = reverse(
            "location-detail",
            kwargs={
                "trip_id": self.trip.pk,
                "location_id": self.location.pk
            }
        )

    # Collection GET

    def test_get_locations(self):
        response = self.client.get(self.collection_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Eiffel Tower")

    def test_get_locations_for_nonexistent_trip(self):
        url = reverse("location", kwargs={"trip_id": 9999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Collection POST

    def test_create_location(self):
        response = self.client.post(
            self.collection_url,
            self.valid_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)
        self.assertEqual(response.data["name"], "Louvre Museum")
        self.assertEqual(
            Location.objects.get(name="Louvre Museum").trip,
            self.trip
        )

    def test_create_location_with_invalid_data(self):
        data = self.valid_data.copy()
        del data["name"]

        response = self.client.post(
            self.collection_url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Location.objects.count(), 1)

    def test_create_location_for_nonexistent_trip(self):
        url = reverse("location", kwargs={"trip_id": 9999})

        response = self.client.post(
            url,
            self.valid_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Location.objects.count(), 1)

    # Detail GET

    def test_get_location(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Eiffel Tower")

    def test_get_nonexistent_location(self):
        url = reverse(
            "location-detail",
            kwargs={
                "trip_id": self.trip.pk,
                "location_id": 9999
            }
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_location_from_another_trip(self):
        url = reverse(
            "location-detail",
            kwargs={
                "trip_id": self.other_trip.pk,
                "location_id": self.location.pk
            }
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Detail PUT

    def test_update_location(self):
        response = self.client.put(
            self.detail_url,
            self.valid_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Louvre Museum")
        self.assertEqual(
            self.location.latitude,
            Decimal("48.860600")
        )

    def test_update_location_with_invalid_data(self):
        data = self.valid_data.copy()
        data["latitude"] = "invalid"

        response = self.client.put(
            self.detail_url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.location.refresh_from_db()
        self.assertEqual(self.location.name, "Eiffel Tower")

    # Detail DELETE

    def test_delete_location(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Location.objects.filter(pk=self.location.pk).exists()
        )
