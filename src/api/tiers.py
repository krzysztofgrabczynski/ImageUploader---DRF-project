from django.urls import reverse
from django.core import signing
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from rest_framework import status, exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from PIL import Image
import os
import uuid
from typing import List

from core.settings import MEDIA_ROOT
from api.models import URLExpirationModel, UserTierModel


class TierResponseClass:
    """
    A class with methods to manage imgaes and urls due to specific account tier.
    """

    @staticmethod
    def create_resized_thumbnail(
        serialized_img: InMemoryUploadedFile, sizes_list: List
    ) -> None:
        """
        Creates a thumbnail resized due to `sizes_list` parameter.
        Filename is craeted with uuid() generator and with suffix due to size of the image.

        :param InMemoryUploadedFile serialized_img: image from serialized data
        :param List sizes_list: list of thumbnail sizes to resize images
        """

        for size in sizes_list:
            image = Image.open(serialized_img)
            image.thumbnail([int(size), int(size)])

            filename_suffix = f"_{size}px"
            filename = "".join([str(uuid.uuid4()), filename_suffix, ".jpg"])
            new_path = os.path.join(MEDIA_ROOT, "images", filename)

            image.save(new_path, "JPEG")

    @classmethod
    def create_image_url(cls, request: Request, sizes_list: List) -> Response:
        """
        Creates a url/s for a thumbnail/s using URLExpirationModel model.

        :param Request request: request
        :param List sizes_list: list of thumbnail sizes to resize images
        """

        url_dict = dict()

        for size in sizes_list:
            url = cls.create_url(request, 1)
            url_dict[size] = url

        return Response({"urls": url_dict}, status=status.HTTP_201_CREATED)

    @classmethod
    def create_url(self, request, image_pk: int) -> str:
        new_url_obj = URLExpirationModel.objects.create(user=request.user)
        url = request.build_absolute_uri(
            reverse(
                "url",
                kwargs={"url_pk": signing.dumps(new_url_obj.pk), "image_pk": image_pk},
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
