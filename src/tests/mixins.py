from django.contrib.auth.models import User
from django.core import signing
from django.urls import reverse

from api.models import TierModel, UserTierModel, URLExpirationModel


class CreateUserForTestMixin:
    """
    Mixin for testing. Updates `setUp()` method creating a new user.
    User params:
    `username: test_user`
    `password: example_password1!`
    Provide function to create a user with given params.
    """

    def setUp(self):
        self.test_user = User.objects.create_user(
            username="test_user", password="example_password1!"
        )
        super().setUp()

    @staticmethod
    def create_user(
        username: str, password: str = "example_password1!", **extra_fields
    ) -> User:
        return User.objects.create_user(
            username=username, password=password, **extra_fields
        )


class CreateTierForTestMixin:
    """
    Mixin for testing. Updates `setUp()` method creating a new account tier.
    Account tier params:
    `name: test_tier`
    `thumbnail_sizes: 200,400`
    `thumbnail_sizes: False`
    `get_origin_img: False`
    `renew_url_perm: False`
    Provide function to create a account tier with given params.
    """

    def setUp(self):
        data = {
            "name": "test_tier",
            "thumbnail_sizes": "200,400",
        }

        self.tier = TierModel.objects.create(**data)
        super().setUp()

    @staticmethod
    def create_tier(
        name: str,
        thumbnail_sizes: str,
        get_origin_img: bool = False,
        renew_url_perm: bool = False,
        change_expiration_time_perm: bool = False,
    ) -> TierModel:
        data = {
            "name": name,
            "thumbnail_sizes": thumbnail_sizes,
            "get_origin_img": get_origin_img,
            "renew_url_perm": renew_url_perm,
            "change_expiration_time_perm": change_expiration_time_perm,
        }

        return TierModel.objects.create(**data)


class UserTierForTestMixin:
    """
    Mixin for testing.
    Provide function to create a `UserTierModel` model object with given params.
    """

    @staticmethod
    def add_tier_to_user(user: User, tier: TierModel) -> UserTierModel:
        return UserTierModel.objects.create(user=user, tier=tier)


class URLForTestMixin:
    """ """

    @staticmethod
    def create_url(
        user: User = None,
        img_filename: str = "example",
        expiration: int = 10,
        renew_url_permission: bool = False,
    ) -> URLExpirationModel:
        return URLExpirationModel.objects.create(
            user=user,
            img_filename=img_filename,
            expiration=expiration,
            renew_url_permission=renew_url_permission,
        )

    @staticmethod
    def hash_url_pk(pk: int, reverse_url: str) -> str:
        return reverse(reverse_url, kwargs={"url_pk": signing.dumps(pk)})
