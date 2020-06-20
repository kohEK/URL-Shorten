from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from .models import Link
from .serializers import LinkSerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RedirectViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_field = 'short_url'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Link.click_counter(instance)
        return redirect(instance.origin_url)
