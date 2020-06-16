from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, settings, mixins

from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from user.serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['DELETE'])
    def deactivate(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        user.delete()
        data = {
            "message": "Successfully Delete User.",
            "user": serializer.data
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    # response = Response({"detail": "Successfully Deactivate."}, status=status.HTTP_204_NO_CONTENT)
    # return super().destroy(self, request, *args, **kwargs)

    @action(detail=False)
    def logout(self, request):
        # permission_classes = (AllowAny,)
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)
        return response
