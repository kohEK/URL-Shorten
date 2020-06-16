from rest_framework import serializers

from urls.models import Url


class UrlSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Url
        fields = ('id', 'origin_url', 'shorten_url', 'created', 'owner')
