from rest_framework import serializers

from links.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('id', 'origin_url', 'short_url', 'owner', 'created', 'count',)
        read_only_fields = ('short_url', 'created', 'count', 'owner')
        # null=true
