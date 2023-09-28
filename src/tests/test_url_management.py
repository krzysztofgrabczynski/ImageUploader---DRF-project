from django.test import TestCase
from rest_framework.test import APIClient
import time

from tests.mixins import *
from api.models import TierModel


class TestUrlExpiration(CreateUserForTestMixin, TestCase):
    """
    Test module for testing url expiration functionality.
    Creating url and check if it is unavailable after timeout (or return status code 200 if user has permission to renew url)
    """

    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.client.login(username="test_user", password="example_password1!")

    def test_url_exporation_without_renew_url_perm(self) -> None:
        url_obj = URLForTestMixin.create_url(user=self.test_user, expiration=2)
        url = URLForTestMixin.hash_url_pk(url_obj.pk, "image_url")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        time.sleep(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_url_exporation_with_renew_url_perm(self) -> None:
        tier = CreateTierForTestMixin.create_tier(
            name="test_name", thumbnail_sizes="200,300", renew_url_perm=True
        )
        UserTierForTestMixin.add_tier_to_user(self.test_user, tier)
        url_obj = URLForTestMixin.create_url(user=self.test_user, expiration=2)
        url = URLForTestMixin.hash_url_pk(url_obj.pk, "image_url")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        time.sleep(2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
