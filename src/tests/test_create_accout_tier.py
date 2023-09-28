from django.test import TestCase
from rest_framework.test import APIClient

from tests.mixins import *


class TestCreateTier(TestCase):
    """
    Test module for testing create account tier functionality.
    It creates a user with stuff status and post data to create tier account using '/create_tier/`' url.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = CreateUserForTestMixin.create_user("test_user", is_staff=True)
        self.client.login(username="test_user", password="example_password1!")

    def test_create_account_tier(self) -> None:
        data = {
            "name": "test_name",
            "thumbnail_sizes": "200,300",
            "get_origin_img": True,
            "renew_url_perm": True,
            "change_expiration_time_perm": True,
        }

        response = self.client.post("/create_tier/", data)

        test_obj = TierModel.objects.first()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(TierModel.objects.count(), 1)
        self.assertEqual(test_obj.name, "test_name")
        self.assertEqual(test_obj.thumbnail_sizes, "200,300")
        self.assertEqual(test_obj.get_origin_img, True)
        self.assertEqual(test_obj.renew_url_perm, True)
        self.assertEqual(test_obj.change_expiration_time_perm, True)
