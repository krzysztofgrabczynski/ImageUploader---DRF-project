from rest_framework import serializers

from api.models import ImageModel


class ImageSerializer(serializers.ModelSerializer):
    """
    A serializer class that serializes data for ImageModel model.
    A user field is hidden and default value is set to logged in user.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ImageModel
        fields = "__all__"
