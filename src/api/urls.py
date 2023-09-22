from django.urls import path

from api.views import ImageAPIView, ListImageAPIView, URLView


urlpatterns = [
    path("upload/", ImageAPIView.as_view(), name="upload_image"),
    path("list_images/", ListImageAPIView.as_view(), name="list_images"),
    path("<str:url_pk>/<int:image_pk>/", URLView.as_view(), name="url"),
]
