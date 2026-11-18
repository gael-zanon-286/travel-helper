
from datetime import timedelta
from io import BytesIO

from PIL import Image as PILImage

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from api.trips.models import Trip
from api.trips.locations.models import Location
from api.trips.locations.images.models import Image
from api.trips.locations.images.serializers import ImageSerializer


class ImageSerializerTestCase(TestCase):

    def setUp(self):
        now = timezone.now()

        self.trip = Trip.objects.create(
            name="Paris Trip",
            start_date=now,
            end_date=now + timedelta(days=5)
        )

        self.location = Location.objects.create(
            name="Eiffel Tower",
            latitude=48.858370,
            longitude=2.294481,
            trip=self.trip
        )

    def create_test_image(self):
        buffer = BytesIO()
        PILImage.new("RGB", (100, 100)).save(buffer, format="PNG")
        buffer.seek(0)

        return SimpleUploadedFile(
            "eiffel_tower.png",
            buffer.read(),
            content_type="image/png"
        )

    def test_serialize_image(self):
        image = Image.objects.create(
            name="Eiffel Tower",
            image=self.create_test_image(),
            location=self.location
        )

        serializer = ImageSerializer(image)

        self.assertEqual(serializer.data["name"], "Eiffel Tower")
        self.assertIn("id", serializer.data)
        self.assertIn("image", serializer.data)

    def test_deserialize_valid_data(self):
        data = {
            "name": "Eiffel Tower",
            "image": self.create_test_image(),
            "location": self.location.pk
        }

        serializer = ImageSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["name"], "Eiffel Tower")
        self.assertIn("image", serializer.validated_data)

    def test_missing_required_field(self):
        data = {
            "image": self.create_test_image()
        }

        serializer = ImageSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_invalid_image(self):
        data = {
            "name": "Eiffel Tower",
            "image": SimpleUploadedFile(
                "invalid.png",
                b"this is not a valid image",
                content_type="image/png"
            )
        }

        serializer = ImageSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("image", serializer.errors)
