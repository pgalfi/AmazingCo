from django.urls import path, include
from rest_framework.routers import DefaultRouter

from branches.api_views import BranchViewSet

router = DefaultRouter()
router.register("branches", BranchViewSet)

urlpatterns = [
    path('v<str:version>/', include(router.urls)),
]