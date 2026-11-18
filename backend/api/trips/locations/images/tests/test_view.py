
from datetime import timedelta
from decimal import Decimal
from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image as PILImage

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from api.trips.models import Trip
from api.trips.locations.models import Location
from api.trips.locations.images.models import Image


class ImageViewTestCase(APITestCase):

    def setUp(self):
        self.temp_media = TemporaryDirectory()
        self.addCleanup(self.temp_media.cleanup)

        self.media_override = override_settings(
            MEDIA_ROOT=self.temp_media.name
        )
        self.media_override.enable()
        self.addCleanup(self.media_override.disable)

        now = timezone.now()

        self.trip = Trip.objects.create(
            name="Paris Trip",
            start_date=now,
            end_date=now + timedelta(days=5)
        )

        self.location = Location.objects.create(
            name="Eiffel Tower",
            latitude=Decimal("48.858370"),
            longitude=Decimal("2.294481"),
            trip=self.trip
        )

        self.other_location = Location.objects.create(
            name="Louvre Museum",
            latitude=Decimal("48.860600"),
            longitude=Decimal("2.337600"),
            trip=self.trip
        )

        self.image = Image.objects.create(
            name="Eiffel Tower",
            image=self.create_test_image(),
            location=self.location
        )

        self.collection_url = reverse(
            "image",
            kwargs={
                "trip_id": self.trip.pk,
                "location_id": self.location.pk
            }
        )

        self.detail_url = reverse(
            "image-detail",
            kwargs={
                "trip_id": self.trip.pk,
                "location_id": self.location.pk,
                "image_id": self.image.pk
            }
        )

    def create_test_image(self):
        buffer = BytesIO()
        PILImage.new("RGB", (100, 100)).save(buffer, format="PNG")
        buffer.seek(0)

        return SimpleUploadedFile(
            "test_image.png",
            buffer.read(),
            content_type="image/png"
        )

    # Collection GET

    def test_get_images(self):
        response = self.client.get(self.collection_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Eiffel Tower")

    def test_get_images_for_nonexistent_location(self):
        url = reverse("image", kwargs={"trip_id": self.trip.pk, "location_id": 9999})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Collection POST

    def test_create_image(self):
        data = {
            "name": "Eiffel Tower View",
            "image": self.create_test_image()
        }

        response = self.client.post(
            self.collection_url,
            data,
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 2)

        created_image = Image.objects.get(name="Eiffel Tower View")
        self.assertEqual(created_image.location, self.location)
        self.assertTrue(created_image.image)

    def test_create_image_with_invalid_file(self):
        data = {
            "name": "Invalid Image",
            "image": SimpleUploadedFile(
                "invalid.png",
                b"not a valid image",
                content_type="image/png"
            )
        }

        response = self.client.post(
            self.collection_url,
            data,
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Image.objects.count(), 1)

    def test_create_image_for_nonexistent_location(self):
        url = reverse("image", kwargs={"trip_id": self.trip.pk, "location_id": 9999})

        data = {
            "name": "Eiffel Tower",
            "image": self.create_test_image()
        }

        response = self.client.post(
            url,
            data,
            format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Image.objects.count(), 1)

    # Detail DELETE

    def test_delete_image(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Image.objects.filter(pk=self.image.pk).exists()
        )

    def test_delete_nonexistent_image(self):
        url = reverse(
            "image-detail",
            kwargs={
                "trip_id": self.trip.pk,
                "location_id": self.location.pk,
                "image_id": 9999
            }
        )

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
