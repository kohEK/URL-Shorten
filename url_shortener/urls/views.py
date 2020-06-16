from rest_framework import viewsets
from .models import Url
from .serializers import UrlSerializer


class UrlViewSet(viewsets.ModelViewSet):
    queryset = Url.objects.all()
    serializer_class = UrlSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
