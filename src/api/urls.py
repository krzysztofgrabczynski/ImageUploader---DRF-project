from django.urls import path

from api.views import ImageAPIView


urlpatterns = [
    path("upload/", ImageAPIView.as_view(), name="upload_image"),
]
