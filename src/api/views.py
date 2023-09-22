from rest_framework import generics, exceptions
from django.core import signing

from api.models import ImageModel, URLExpirationModel
from api.serializers import BasicImageSerializer, ExtendImageSerializer
from api.tiers import TierResponseClass


class ImageAPIView(generics.CreateAPIView):
    """
    A APIView for POST method to upload a new image.
    It creates images with a specific sizes and urls.
    It uses  `TierResponseClass` class for image and url management.
    """

    queryset = ImageModel.objects.all()
    serializer_class = BasicImageSerializer

    def get_serializer_class(self):
        """
        Set serializer class due to user permission to change url expiration time.
        """

        super().get_serializer_class()

        tier = TierResponseClass.get_tier(self.request.user)
        if tier.change_expiration_time_perm:
            return ExtendImageSerializer
        return BasicImageSerializer

    def create(self, request, *args, **kwargs):
        """
        This method uploads a new image and uses `TierResponseClass` methods for further image/url specific operations.
        Creates resized thumbnailes and urls.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        tier = TierResponseClass.get_tier(request.user)
        TierResponseClass.create_resized_thumbnail(
            serializer.validated_data["img"], tier.get_sizes_list()
        )
        response = TierResponseClass.create_image_url(request, tier.get_sizes_list())

        try:
            return response
        except UnboundLocalError:
            raise exceptions.PermissionDenied(
                "You do not have permission or group permission to perform this action."
            )


class ListImageAPIView(generics.ListAPIView):
    """
    A APIView for GET method to list images of the specific logged in user.
    """

    queryset = ImageModel.objects.all()
    serializer_class = BasicImageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class URLView(generics.RetrieveAPIView):
    """
    A View class for GET method to retrieve url (image/thumbnail) if url is still available.
    In case of timeout, `signing.loads` method will raise `BadSignature` exception and url will be deactivate.
    """

    queryset = URLExpirationModel()
    lookup_field = "image_pk"

    def get(self, request, *args, **kwargs):
        url_model = URLExpirationModel.objects.get(pk=signing.loads(kwargs["url_pk"]))
        try:
            signing.loads(kwargs["url_pk"], max_age=url_model.expiration)
        except signing.BadSignature:
            url_model.delete()
            raise exceptions.PermissionDenied(
                "Link that you trying to access expired or does not exist."
            )

        super().get(request, *args, **kwargs)
