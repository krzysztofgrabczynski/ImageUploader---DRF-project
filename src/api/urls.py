from django.urls import path

from api.views import (
    ImageAPIView,
    ListImageAPIView,
    URLAPIVView,
    CreateAccountTierAPIView,
)


urlpatterns = [
    path("upload/", ImageAPIView.as_view(), name="upload_image"),
    path("list_images/", ListImageAPIView.as_view(), name="list_images"),
    path("<str:url_pk>/<int:image_pk>/", URLAPIVView.as_view(), name="url"),
    path("create_tier", CreateAccountTierAPIView.as_view(), name="create_tier"),
]
