from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
    conf_pass = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'password',
            'conf_pass'
        ]

    def validate(self, data):
        password = data.get('password')
        conf_pass = data.get('conf_pass')

        if password != conf_pass:
            raise ValidationError('Parollar mos emas')

        return data

    def create(self, validated_data):
        validated_data.pop('conf_pass')
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'msg': 'User created',
            'user': data
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            raise ValidationError('Login yoki parol xato')

        attrs['user'] = user
        return attrs