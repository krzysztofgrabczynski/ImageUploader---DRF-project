from rest_framework import generics

from api.models import ImageModel
from api.serializers import ImageSerializer

class ImageAPIView(generics.CreateAPIView):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer




