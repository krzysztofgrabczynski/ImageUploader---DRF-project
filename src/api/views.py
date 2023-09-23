from rest_framework import generics, exceptions

from api.models import ImageModel, URLExpirationModel, TierModel
from api.serializers import (
    BasicImageSerializer,
    ExtendImageSerializer,
    AccountTierSerializer,
)
from api.tiers import TierResponseClass
from api.mixins import CreateAccountTierMixin, URLExpirationMixin


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


class URLAPIVView(URLExpirationMixin, generics.RetrieveAPIView):
    """
    A View class for GET method to retrieve url (image/thumbnail) if url is still available.
    It uses `URLExpirationMixin` mixin for url expiration functionality.
    """

    queryset = URLExpirationModel()
    lookup_field = "image_pk"


class CreateAccountTierAPIView(CreateAccountTierMixin, generics.CreateAPIView):
    """
    A view for creating a new account tier.
    `CreateAccountTierMixin` check if the user get permission to create a new account tier model.
    """

    queryset = TierModel.objects.all()
    serializer_class = AccountTierSerializer
