
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from api.trips.models import Trip
from api.trips.locations.models import Location
from api.trips.locations.images.models import Image


class ImageModelTestCase(TestCase):

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

        self.image = Image.objects.create(
            name="Eiffel Tower",
            location=self.location
        )

    def test_create_image(self):
        """Persistence testing"""
        self.assertIsNotNone(self.image.pk)

        image_from_db = Image.objects.get(pk=self.image.pk)

        self.assertEqual(image_from_db.name, "Eiffel Tower")
        self.assertEqual(image_from_db.location, self.location)

    def test_image_location_relationship(self):
        """Test the relationship between image and location"""
        self.assertEqual(self.image.location, self.location)
        self.assertIn(self.image, self.location.images.all())

    def test_deleting_location_deletes_images(self):
        """Cascading relationships test (Images are removed when a location is deleted)"""
        image_id = self.image.pk

        self.location.delete()

        self.assertFalse(Image.objects.filter(pk=image_id).exists())
