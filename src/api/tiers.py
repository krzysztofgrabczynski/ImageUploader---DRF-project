from django.urls import reverse
from django.core import signing
from django.contrib.auth.models import User
from rest_framework import status, exceptions
from rest_framework.response import Response
from PIL import Image
import os
from io import BytesIO
import uuid

from api.s3 import AWSServices
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
        Creates a resized thumbnail/s and save to s3 storage.
        It provieds as result url/s to view thumbnail/s. Url has expiration time due to expiration time in ImageModel (defaul or provided by user).
        It ueses `AWSServices` for operations such as upload new image to s3 or get url to that img.

        :param request: request object.
        :param serializer: serializer object with serialized data for ImageModel instance.
        :param UserTierModel tier: UserTierModel object with data about list of thumbnails sizes and `get_origin_img` boolean.
        """

        url_dict = dict()
        sizes_list = tier.get_sizes_list()
        expiration_time = serializer.validated_data.get(
            "url_expiration_time", ImageModel.url_expiration_time.field.default
        )

        original_img_root = f"""media/{serializer.validated_data["img"]}"""
        image_data = AWSServices.get_object_from_s3(original_img_root)

        for size in sizes_list:
            image = Image.open(BytesIO(image_data))
            image.thumbnail([int(size), int(size)])
            output_buffer = BytesIO()
            image.save(output_buffer, format="JPEG")

            filename_suffix = f"_{size}px"
            filename = "".join([str(uuid.uuid4()), filename_suffix, ".jpg"])
            new_obj_name = os.path.join("media/", filename)

            AWSServices.put_object_to_AWS(new_obj_name, output_buffer.getvalue())
            url = AWSServices.generate_url(new_obj_name)

            url_dict[size] = cls.create_url(request, url, expiration_time)

        if tier.get_origin_img:
            url = AWSServices.generate_url(original_img_root)
            url_dict["origin_img"] = cls.create_url(request, url, expiration_time)

        return Response({"urls": url_dict}, status=status.HTTP_201_CREATED)

    @classmethod
    def create_url(self, request, url: str, expiration_time: int) -> str:
        new_url_obj = URLExpirationModel.objects.create(
            user=request.user, img_filename=url, expiration=expiration_time
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
