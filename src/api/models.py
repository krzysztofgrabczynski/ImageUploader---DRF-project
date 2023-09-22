from django.db import models
from django.contrib.auth import get_user_model
from typing import List


User = get_user_model()


class ImageModel(models.Model):
    """
    A model that represents a single image with a specific user that uploaded that image.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    img = models.ImageField(upload_to="images/", null=False, blank=False)
    url_expiration_time = models.IntegerField(default=10)


class URLExpirationModel(models.Model):
    """
    A model class that represents url.
    It is used to create a url object that will expire in time `expiration`.
    `user` and `renew_url_permission` used for ability to fetch an expired url.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    expiration = models.IntegerField(default=10)
    renew_url_permission = models.BooleanField(default=False)


class TierModel(models.Model):
    """
    A model class that represents account tiers.
    """

    name = models.CharField(blank=False, null=True, unique=True, verbose_name="NAME")
    thumbnail_sizes = models.CharField(
        blank=False, null=True, verbose_name="THUMBNAIL SIZES [px]"
    )
    get_origin_img = models.BooleanField(
        default=False, blank=False, null=True, verbose_name="ORIGIN IMG URL"
    )
    renew_url_perm = models.BooleanField(
        default=False, blank=False, null=True, verbose_name="RENEW URL PERMISSION"
    )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.thumbnail_sizes.split(","))

    def get_tier_users(self) -> List:
        return list(self.usertiermodel_set.all())

    def get_sizes_list(self) -> List:
        """
        Create a list of sizes of the thumbnails.
        """
        return self.thumbnail_sizes.split(",")


class UserTierModel(models.Model):
    """
    A model class that creates a relationship between a user and account tier.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    tier = models.ForeignKey(
        TierModel, on_delete=models.CASCADE, blank=False, null=False
    )

    def __str__(self) -> str:
        return self.user.get_username()

    def __repr__(self) -> str:
        return self.__str__()

    def get_tier_obj(self) -> TierModel:
        return self.tier
