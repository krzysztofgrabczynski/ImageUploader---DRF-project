from rest_framework import generics, exceptions

from api.models import ImageModel
from api.serializers import ImageSerializer
from api.tiers import BaseTierClass


class ImageAPIView(generics.CreateAPIView):
    """
    A APIView for POST method to upload a new image.
    """

    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        """
        This method uploads a new image and check what tier/permission group user is belongs to for further specific operations.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        for tier in BaseTierClass.__subclasses__():
            if request.user.groups.filter(name=tier.class_name()).exists():
                response = tier.get_response(serializer)

        try:
            return response
        except UnboundLocalError:
            raise exceptions.PermissionDenied(
                "You do not have permission or group permission"
            )


class ListImageAPIView(generics.ListAPIView):
    """
    A APIView for GET method to list images of the specific logged in user.
    """

    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
