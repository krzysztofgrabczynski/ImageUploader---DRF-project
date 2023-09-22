from django.core.management.base import BaseCommand

from api.models import TierModel


class Command(BaseCommand):
    """
    A command class which creates a built-in account tiers.
    """

    help = "Command for creating a built-in account tiers."

    def handle(self, *args, **options):
        if not TierModel.objects.filter(name="Basic").exists():
            TierModel.objects.create(
                name="Basic",
                thumbnail_sizes="200",
                get_origin_img=False,
                renew_url_perm=False,
            )
        if not TierModel.objects.filter(name="Premium").exists():
            TierModel.objects.create(
                name="Premium",
                thumbnail_sizes="200,400",
                get_origin_img=True,
                renew_url_perm=False,
            )
        if not TierModel.objects.filter(name="Enterprise").exists():
            TierModel.objects.create(
                name="Enterprise",
                thumbnail_sizes="200,400",
                get_origin_img=True,
                renew_url_perm=True,
            )
