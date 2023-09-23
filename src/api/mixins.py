from rest_framework import exceptions
from django.core import signing

from api.permissions import CanCreateAccountTierPermission
from api.models import URLExpirationModel


class CreateAccountTierMixin:
    permission_classes = [CanCreateAccountTierPermission]


class URLExpirationMixin:
    """
    A class mixin for checking if the timeout of URL expired.
    `signing.loads` method will raise `BadSignature` exception after timeout and url will be deactivate. 
    """
   
    def get(self, request, *args, **kwargs):
        url_model = URLExpirationModel.objects.get(pk=signing.loads(kwargs["url_pk"]))
        try:
            signing.loads(kwargs["url_pk"], max_age=url_model.expiration)
        except signing.BadSignature:
            raise exceptions.PermissionDenied(
                "Link that you trying to access expired or does not exist."
            )

        super().get(request, *args, **kwargs)
