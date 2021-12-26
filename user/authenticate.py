import os
import jwt
from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None

        _, token = auth_data.decode('utf-8').split(' ')
        try:
            payload = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms='HS256')

            user = User.objects.get(id=payload['id'])

            return user, token

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('your token is invalid, please log in!')

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('your token is expired, please log in again!')
