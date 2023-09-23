from django.urls import reverse
from django.core import signing
from django.contrib.auth.models import User
from rest_framework import status, exceptions
from rest_framework.response import Response
from PIL import Image
import os
import uuid
from typing import List

from core.settings import MEDIA_ROOT
from api.models import URLExpirationModel, UserTierModel, ImageModel


class TierResponseClass:
    """
    A class with methods to manage imgaes and urls due to specific account tier.
    """

    @classmethod
    def create_resized_thumbnail(
        cls, request, serializer, tier: UserTierModel
    ) -> Response:
        """
        Creates a thumbnail resized due to `sizes_list` parameter.
        Filename is craeted with uuid() generator and with suffix due to size of the image.
        Uses 'create_url' method to create url for the thumbnail.

        :param Request request: uses for `create_url` method
        :param ModelSerializer serializer: serializer with validated data
        :param UserTierModel tier: UserTierModel object with data about list of thumbnails sizes and `get_origin_img` boolean.
        """

        url_dict = dict()
        serialized_img = serializer.validated_data["img"]
        expiration_time = serializer.validated_data.get(
            "url_expiration_time", ImageModel.url_expiration_time.field.default
        )
        sizes_list = tier.get_sizes_list()

        for size in sizes_list:
            image = Image.open(serialized_img)
            image.thumbnail([int(size), int(size)])

            filename_suffix = f"_{size}px"
            filename = "".join([str(uuid.uuid4()), filename_suffix, ".jpg"])
            new_path = os.path.join(MEDIA_ROOT, "images", filename)

            image.save(new_path, "JPEG")

            url_dict[size] = cls.create_url(request, filename, expiration_time)

        if tier.get_origin_img:
            url_dict["origin_img"] = cls.create_url(
                request, serialized_img, expiration_time
            )

        return Response({"urls": url_dict}, status=status.HTTP_201_CREATED)

    @classmethod
    def create_url(self, request, filename: str, expiration_time: int) -> str:
        new_url_obj = URLExpirationModel.objects.create(
            user=request.user, img_filename=filename, expiration=expiration_time
        )
        url = request.build_absolute_uri(
            reverse(
                "url",
                kwargs={"url_pk": signing.dumps(new_url_obj.pk)},
            )
        )
        return url

    @staticmethod
    def get_tier(user: User) -> UserTierModel:
        try:
            return UserTierModel.objects.get(user=user).get_tier_obj()
        except UserTierModel.DoesNotExist:
            raise exceptions.PermissionDenied(
                "You do not have permission or group permission to perform this action."
            )
