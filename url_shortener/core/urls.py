from django.urls import include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserViewSet, UrlViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)  # POST(register)
# router.register(r'users/<int:pk>', UserViewSet)
# router.register(r'users/deactivate', UserViewSet)  # DELETE

router.register(r'urls', UrlViewSet)  # POST(origin_url)
# router.register(r'urls/{uuid}', UrlViewSet)         # GET(shorten_url detail), DELETE(shorten_url delete)

urlpatterns = router.urls
