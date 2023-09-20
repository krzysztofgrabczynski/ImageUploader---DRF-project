from rest_framework import serializers

from api.models import ImageModel


class ImageSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ImageModel
        fields = "__all__"
