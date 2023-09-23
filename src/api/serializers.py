from rest_framework import serializers

from api.models import ImageModel, TierModel


class BasicImageSerializer(serializers.ModelSerializer):
    """
    A serializer class that serializes data for ImageModel model.
    A user field is hidden and default value is set to logged in user.
    Basic version is used for users without permission to change url expiration time.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ImageModel
        fields = ["user", "img"]


class ExtendImageSerializer(serializers.ModelSerializer):
    """
    A serializer class that serializes data for ImageModel model.
    A user field is hidden and default value is set to logged in user.
    Extended version is used for users with permission to change url expiration time.
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ImageModel
        fields = "__all__"


class AccountTierSerializer(serializers.ModelSerializer):
    """
    A serializer class for serializing data of the TierModel model.
    """
    
    class Meta:
        model = TierModel
        fields = "__all__"