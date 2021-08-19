from django.conf.urls import url
from django.urls import include
from django.urls.conf import path
from rest_framework.routers import DefaultRouter

from .views import TransactionViewSet


router = DefaultRouter()
router.register('transactions', TransactionViewSet, basename='transactions')

urlpatterns = router.urls