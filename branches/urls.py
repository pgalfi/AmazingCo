from django.urls import path, include
from rest_framework.routers import DefaultRouter

from branches import views
from branches.api_views import OfficeViewSet

router = DefaultRouter()
router.register("offices", OfficeViewSet)

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('v<str:version>/', include(router.urls)),
]