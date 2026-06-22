from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r"", views.VideosViewSet, basename="video")

urlpatterns = [
    path("ids/", views.VideoIdsView.as_view()),
    path("statistics-group-by/", views.StatisticGroupByView.as_view()),
    path("statistics-subquery/", views.StatisticSubqueryView.as_view()),
    path("", include(router.urls)),
]
