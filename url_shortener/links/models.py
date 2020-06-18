import random
import string
import time

from django.db import models
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.utils.baseconv import base64
from rest_framework.generics import get_object_or_404

words = string.ascii_letters + string.digits


class Link(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='link_set', null=True, )
    origin_url = models.URLField(max_length=200)
    short_url = models.URLField(max_length=25, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='created')
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.origin_url

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.short_url = self.long_to_short()
        super().save(force_insert, force_update, using, update_fields)

    def long_to_short(self):
        result = 0
        for s in self.origin_url:
            # origin url 각각의 부분을 s 로 받은 다음, 그 s를 하나의 유니코드 포인트 ( 정수 ) 로 반환한다.
            result += ord(s)
            # print(ord(s))
        for s in self.owner.username:
            # 회원 가입이 되어있으면서 토큰으로 인증이 되어있는 유저가 (Url.owner)의 이름을 받아서 result에 넣는다.
            result += ord(s)
        result += int(time.time())
        # 시간까지 더한다음

        # 더한 result를 base62로 인코딩 한 값을 돌려줘요.
        return self.base62(result)

    def base62(self, index):
        print('index>>>>>>', index)
        result = ""
        # index를 62로 나눈 나머지가 0보다 크거나, result가 "" 라면 반복
        while (index % 62) > 0 or result == "":
            # index, i는 index랑 62를 나눈 몫과 나머지 이다.
            # index는 몫 i는 나머지
            index, i = divmod(index, 62)
            # result에 word[i]번째 값을 더한다.
            result += words[i]
        return result

    # def click_counter(self):
    #     url = get_object_or_404(Link, pk=self.short_url)
    #     url.count += 1
    #     url.save()
    #     return HttpResponseRedirect(url.origin_url)
