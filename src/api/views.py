from rest_framework import generics

from api.models import ImageModel
from api.serializers import ImageSerializer


class ImageAPIView(generics.CreateAPIView):
    """
    A APIView for POST method to upload a new image.
    """

    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer


class ListImageAPIView(generics.ListAPIView):
    """
    A APIView for GET method to list images of the specific logged in user.
    """

    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
