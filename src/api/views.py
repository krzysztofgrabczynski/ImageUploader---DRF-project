from rest_framework import generics, exceptions

from api.models import ImageModel, TierModel
from api.serializers import (
    BasicImageSerializer,
    ExtendImageSerializer,
    AccountTierSerializer,
    RenewURLSerializer,
)
from api.tiers import TierResponseClass
from api.mixins import CreateAccountTierMixin, URLExpirationMixin, RenewURLMixin


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
        Creates resized thumbnailes and urls to access them.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        tier = TierResponseClass.get_tier(request.user)
        response = TierResponseClass.create_resized_thumbnail(request, serializer, tier)

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


class CreateAccountTierAPIView(CreateAccountTierMixin, generics.CreateAPIView):
    """
    A view for creating a new account tier.
    `CreateAccountTierMixin` check if the user get permission to create a new account tier model.
    """

    queryset = TierModel.objects.all()
    serializer_class = AccountTierSerializer


class URLAPIVView(URLExpirationMixin, generics.GenericAPIView):
    """
    A view class for GET method to retrieve url (image/thumbnail) if url is still available.
    It uses `URLExpirationMixin` mixin for url expiration functionality.
    """

    queryset = ImageModel.objects.all()
    serializer_class = BasicImageSerializer


class RenewURLAPIView(RenewURLMixin, generics.GenericAPIView):
    """
    A view class for POST method to create a new active url for image/thumbnail.
    """

    serializer_class = RenewURLSerializer
