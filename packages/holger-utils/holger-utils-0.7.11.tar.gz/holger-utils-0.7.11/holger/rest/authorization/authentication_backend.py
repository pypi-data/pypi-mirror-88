from rest_framework.authentication import BaseAuthentication
from django.contrib.auth.models import AnonymousUser
from jose import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class HolgerUserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()
        user = AnonymousUser()
        try:
            raw_token = str(request.headers['Authorization'])
            if not raw_token.startswith('Bearer'):
                raise AuthenticationFailed()
            net_token = raw_token.split(' ')
            if not len(net_token) == 2:
                raise AuthenticationFailed()
            token = net_token[1].strip()
            key = getattr(settings, 'Holger_JWT_KEY', settings.SECRET_KEY)
            token = jwt.decode(token, key)
            user_queryset = User.objects.filter(pk=token['pk'])
            if token['token_type'] == 'access' and user_queryset.exists():
                user = user_queryset.last()
                return user, None
            else:
                raise AuthenticationFailed()
        except Exception:
            raise AuthenticationFailed()


class HolgerTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = AnonymousUser()
        try:
            raw_token = str(request.headers['Authorization'])
            if not raw_token.startswith('Bearer'):
                raise AuthenticationFailed()
            net_token = raw_token.split(' ')
            if not len(net_token) == 2:
                raise AuthenticationFailed()
            token = net_token[1].strip()
            key = getattr(settings, 'Holger_JWT_KEY', settings.SECRET_KEY)
            token = jwt.decode(token, key)
            if token['token_type'] == 'access':
                setattr(request, 'user', token)
                user = token
                return user, None
            else:
                raise AuthenticationFailed()
        except Exception:
            raise AuthenticationFailed()
