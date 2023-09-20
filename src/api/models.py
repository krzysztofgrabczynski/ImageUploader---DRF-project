from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ImageModel(models.Model):
    """
    A model that represents a single image with a specific user that uploaded that image.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    img = models.ImageField(upload_to="images/", null=False, blank=False)
