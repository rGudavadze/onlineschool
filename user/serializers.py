from rest_framework import serializers
from .models import User, Profile, SellerProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'username', 'role', 'password', 'password_confirm')
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True}
        }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if not email or User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists!')

        if not password or password != password_confirm:
            raise serializers.ValidationError('Passwords are not matched!')

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
            instance.password_confirm = ""
        instance.save()

        return instance
