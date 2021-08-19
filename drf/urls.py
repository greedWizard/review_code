from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import TransferViewSet


router = DefaultRouter()
router.register('transfer', TransferViewSet, basename='auth') # basename='transfers'

# urlpatterns = router.urls
urlpatterns = [
    url(r'api/', include(router.urls)), # url() уже морально устарел, надо использовать path
]