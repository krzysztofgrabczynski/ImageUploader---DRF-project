from django.test import TestCase
from rest_framework.test import APIClient

from tests.mixins import *
from api.models import ImageModel


class TestImageFunctionality(CreateUserForTestMixin, CreateTierForTestMixin, TestCase):
    """
    Test module for testing Image functionality.
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.client.login(username="test_user", password="example_password1!")

    def test_get_method(self) -> None:
        """
        Testing GET method.
        After calling this method, api should return images uploaded by specific user.
        """

        img = ImageForTestMixin.get_image_file()
        ImageModel.objects.create(
            user=self.test_user,
            img=img,
        )

        response = self.client.get("/list_images/")

        self.assertEqual(response.status_code, 200)

    def test_post_method(self) -> None:
        """
        Testing POST method.
        After calling this method, api should create ImageModel object and, if provided, creates a resized thumbnails.
        """

        UserTierForTestMixin.add_tier_to_user(self.test_user, self.tier)

        img = ImageForTestMixin.get_image_file()

        data = {
            "img": img,
        }

        response = self.client.post("/upload/", data)
        self.assertEqual(response.status_code, 201)
