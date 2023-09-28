from django.test import TestCase

from tests.mixins import *


class TestTierModel(CreateUserForTestMixin, CreateTierForTestMixin, TestCase):
    """
    Test module for testing TierModel.
    """

    def test_get_method(self) -> None:
        """
        Testing GET method.
        When calling TierModel object, should return a `name` of the model object"
        """

        expected_str = self.tier.name
        self.assertEqual(str(self.tier), expected_str)
