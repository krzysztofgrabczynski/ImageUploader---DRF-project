from rest_framework import exceptions
from django.core import signing
from django.urls import reverse
from rest_framework.response import Response

from api.permissions import CanCreateAccountTierPermission, CanRenewURLPermission
from api.models import URLExpirationModel
from api.tiers import TierResponseClass


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
            tier = TierResponseClass.get_tier(self.request.user)
            if tier.renew_url_perm:
                url = self.renew_url(request, url_model.pk, kwargs["image_pk"])
                return Response({"url": f"If you want to renew url click: {url}"})
            else:
                raise exceptions.PermissionDenied(
                    "Link that you trying to access expired or does not exist."
                )

        super().get(request, *args, **kwargs)

    def renew_url(self, request, url_to_renew_pk: int, image_pk: int):
        return request.build_absolute_uri(
            reverse(
                "renew_url",
                kwargs={
                    "url_to_renew_pk": signing.dumps(url_to_renew_pk),
                    "image_pk": image_pk,
                },
            )
        )


class RenewURLMixin:
    """
    A mixin class for creating a renew URL for a specific image.
    `CanRenewURLPermission` permission check if the user is allowed to renew a URL.
    """

    permission_classes = [CanRenewURLPermission]

    def post(self, request, *args, **kwargs):
        self.delete_expired_url(**kwargs)

        image_pk = kwargs["image_pk"]

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data["renew_url"]:
            url = TierResponseClass.create_url(request, image_pk)
            return Response(url)

        return Response("Check 'Renew url' for renew image url")

    def delete_expired_url(self, **kwargs):
        url_model_pk = signing.loads(kwargs["url_to_renew_pk"])
        URLExpirationModel.objects.get(pk=url_model_pk).delete()
