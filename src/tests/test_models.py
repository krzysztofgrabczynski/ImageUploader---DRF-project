from django.test import TestCase
from tests.mixins import *


class TestTierModel(CreateUserForTestMixin, CreateTierForTestMixin, TestCase):
    """
    Test module for testing TierModel.
    """

    def test_str_method(self) -> None:
        """
        Testing __str__() methods.
        When calling TierModel object, should return a `name` of the model object"
        """

        expected_str = self.tier.name
        self.assertEqual(str(self.tier), expected_str)

    def test_len_method(self) -> None:
        """
        Testing __len__() methods.
        When calling `len` on TierModel object, should return a number of the sizes (length of the list with sizes for thumbnails)."
        """

        self.assertEqual(len(self.tier), 2)

    def test_get_tier_users_method(self) -> None:
        """
        Testing get_tier_users() methods.
        When calling `get_tier_users()` on TierModel object, should return a list of the users that have this specific tier account."
        """

        user2 = CreateUserForTestMixin.create_user("test_user_2")
        UserTierForTestMixin.add_tier_to_user(self.test_user, self.tier)
        UserTierForTestMixin.add_tier_to_user(user2, self.tier)

        self.assertEqual(str(self.tier.get_tier_users()[0]), str(self.test_user))
        self.assertEqual(str(self.tier.get_tier_users()[1]), str(user2))

    def test_get_sizes_list_method(self) -> None:
        """
        Testing get_sizes_list() methods.
        When calling `get_sizes_list()` on TierModel object, should return a list of sizes of the thumbnailes provided by user."
        """

        expected = ["200", "400"]
        self.assertEqual(self.tier.get_sizes_list(), expected)


class TestUserTierModelModel(CreateUserForTestMixin, CreateTierForTestMixin, TestCase):
    """
    Test module for testing TierModel.
    """

    def test_str_method(self) -> None:
        """
        Testing __str__() methods.
        When calling UserTierModel object, should return a `username` of the User model object"
        """

        user_tier = UserTierForTestMixin.add_tier_to_user(self.test_user, self.tier)
        self.assertEqual(str(user_tier), self.test_user.username)

    def test_get_tier_obj_method(self) -> None:
        """
        Testing get_tier_obj() methods.
        When calling 'get_tier_obj()' method, should return a TierModel object."
        """

        user_tier = UserTierForTestMixin.add_tier_to_user(self.test_user, self.tier)
        self.assertEqual(user_tier.get_tier_obj(), self.tier)
