
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from api.trips.models import Trip


class TripViewTestCase(APITestCase):

    def setUp(self):
        self.trip = Trip.objects.create(
            name="Madrid Trip",
            start_date="2027-06-10T10:00:00Z",
            end_date="2027-06-15T18:00:00Z"
        )

        self.valid_data = {
            "name": "Barcelona Trip",
            "start_date": "2027-07-10T10:00:00Z",
            "end_date": "2027-07-15T18:00:00Z"
        }

    def test_get_trips(self):
        response = self.client.get(reverse("trips"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Madrid Trip")

    def test_create_trip(self):
        response = self.client.post(
            reverse("trips"),
            self.valid_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Trip.objects.count(), 2)
        self.assertEqual(response.data["name"], "Barcelona Trip")

    def test_create_trip_invalid_data(self):
        data = self.valid_data.copy()
        del data["name"]

        response = self.client.post(
            reverse("trips"),
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Trip.objects.count(), 1)

    def test_get_trip_detail(self):
        response = self.client.get(
            reverse("trip-detail", kwargs={"trip_id": self.trip.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Madrid Trip")

    def test_get_nonexistent_trip(self):
        response = self.client.get(
            reverse("trip-detail", kwargs={"trip_id": 999})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_trip(self):
        response = self.client.put(
            reverse("trip-detail", kwargs={"trip_id": self.trip.pk}),
            self.valid_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.trip.refresh_from_db()
        self.assertEqual(self.trip.name, "Barcelona Trip")

    def test_delete_trip(self):
        response = self.client.delete(
            reverse("trip-detail", kwargs={"trip_id": self.trip.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Trip.objects.count(), 0)

    def test_delete_nonexistent_trip(self):
        response = self.client.delete(
            reverse("trip-detail", kwargs={"trip_id": 999})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)