from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """
    A command class which creates a new permission groups.
    """

    help = "Command for creating a new permission groups."

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Basic")
        group, created = Group.objects.get_or_create(name="Premium")
        group, created = Group.objects.get_or_create(name="Enterprise")
