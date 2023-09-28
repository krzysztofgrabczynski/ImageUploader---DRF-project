from django.urls import path

from api.views import (
    ImageAPIView,
    ListImageAPIView,
    URLAPIVView,
    CreateAccountTierAPIView,
    RenewURLAPIView,
)


urlpatterns = [
    path("upload/", ImageAPIView.as_view(), name="upload_image"),
    path("list_images/", ListImageAPIView.as_view(), name="list_images"),
    path("image_url/<str:url_pk>/", URLAPIVView.as_view(), name="image_url"),
    path("create_tier/", CreateAccountTierAPIView.as_view(), name="create_tier"),
    path(
        "renew_url/<str:url_to_renew_pk>/",
        RenewURLAPIView.as_view(),
        name="renew_url",
    ),
]
