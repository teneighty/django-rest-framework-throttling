from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import authentication as auth
from rest_framework import permissions as perm
from rest_framework.authtoken.models import Token
from rest_framework.response import Response 
from rest_framework.views import APIView

from rest_framework_throttling.throttling import PerUserThrottle

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class GetNumbers(APIView):
    throttle_classes = (PerUserThrottle, )
    authentication_classes = (auth.TokenAuthentication, )
    permission_classes = (perm.IsAuthenticated, )

    def get(self, request):
        return Response(data=range(0, 10))


class GetChars(APIView):
    throttle_classes = (PerUserThrottle, )
    authentication_classes = (auth.TokenAuthentication, )
    permission_classes = (perm.IsAuthenticated, )

    def get(self, request):
        return Response(data=[chr(c) for c in range(ord('a'), ord('z'))])

