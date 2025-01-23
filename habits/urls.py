from django.urls import path

from . import views
from .apps import HabitsConfig

app_name = HabitsConfig.name


urlpatterns = [
    path("habits/", views.HabitsListAPIView.as_view(), name="habits_list"),
    path("habits/<int:pk>", views.HabitsRetrieveAPIView.as_view(), name="habits_retrieve"),
    path("habits/create", views.HabitsCreateAPIView.as_view(), name="habits_create"),
    path(
        "habits/<int:pk>/update", views.HabitsUpdateAPIView.as_view(), name="habits_update"
    ),
    path(
        "habits/<int:pk>/delete",
        views.HabitsDestroyAPIView.as_view(),
        name="habits_delete",
    ),
    path(
        "habits/public/",
        views.HabitsPublicListAPIView.as_view(),
        name="habits_public_list",
    ),
]
