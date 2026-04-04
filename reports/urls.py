from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, test_postcode

router = DefaultRouter()
router.register(r'reports', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

