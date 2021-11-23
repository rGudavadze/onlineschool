from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from drf_spectacular.utils import extend_schema
from .models import Profile, SellerProfile, User
from .serializers import UserSerializer
import jwt
import datetime
import os


class RegisterView(APIView):
    @extend_schema(request=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginView(APIView):
    @extend_schema(request=UserSerializer)
    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']

        user = authenticate(username=username, password=password)

        if user:
            payload = {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, os.environ.get('JWT_SECRET_KEY'), algorithm='HS256')

            response = Response()

            response.set_cookie(key='jwt', value=token, httponly=True)

            response.data = {
                'jwt': token
            }

            return response

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, os.environ.get('JWT_SECRET_KEY'), algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated, JWT expired!')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)


class Logout(APIView):
    def post(self, request):
        response = Response()

        response.delete_cookie('jwt')

        response.data = {
            'message': 'success'
        }

        return response


class ListUser(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
