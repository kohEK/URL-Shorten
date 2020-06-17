from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout, authenticate
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, settings, mixins
from rest_framework.authtoken.models import Token

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

    @action(detail=False, methods=['post'])
    def login(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        print(username, password)
        user = authenticate(request=request,
                            username=username, password=password)

        print('UserId:', user.id)

        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        # permission_classes = (AllowAny,)
        print(request.user)
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
            return Response({'message': "인증되지 않은 유저입니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)
            return Response({"detail": "Successfully logged out."},
                            status=status.HTTP_200_OK)
