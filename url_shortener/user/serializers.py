from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password',)

    # 유저의 패스워드를 set_password로 hashing 해주자
    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        return user

        # # user = super(UserSerializer, self).create(validated_data)
        # # if 'password' in validated_data:
        # #     user.set_password(validated_data['password'])
        # #     user.save()
        # return user
