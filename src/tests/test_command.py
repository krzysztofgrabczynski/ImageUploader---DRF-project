from django.test import TestCase
from django.core.management import call_command

from api.models import TierModel


class TestCommand(TestCase):
    """
    Test module for testing custom commands.
    """

    def test_user_group_management(self):
        """
        It tests the user_group_management command which is creating defaults account tiers.
        """

        self.assertEqual(TierModel.objects.count(), 0)

        call_command("user_group_management")

        self.assertEqual(TierModel.objects.count(), 3)
