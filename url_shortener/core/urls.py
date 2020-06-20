from django.urls import include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import UserViewSet, LinkViewSet,RedirectViewSet

# UrlViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'users', UserViewSet)  # POST(register)
router.register(r'urls', LinkViewSet)
router.register(r'urls/redirect/*', RedirectViewSet)

urlpatterns = router.urls

