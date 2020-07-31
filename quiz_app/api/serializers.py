import json

from django.contrib.auth import authenticate
from django.core.validators import EmailValidator
from rest_framework import exceptions, serializers

from .models import Answer, Attempt, Profile, Question, Quiz, User


def _handle_missing_fields(serializer, data):
    errors = [
        field.field_name for field in serializer._writable_fields
        if not data.get(field.field_name)
    ]
    if errors:
        raise serializers.ValidationError(
            detail=errors,
            code='missing_field',
        )


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        _handle_missing_fields(self, data)
        errors = [
            field for field in ('email', 'username')
            if User.objects.filter(**{
                field: data.get(field)
            }).exists()
        ]
        if errors:
            raise serializers.ValidationError(
                detail=errors,
                code='already_exists',
            )
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        read_only_fields = ['token']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'validators': [EmailValidator]
            }
        }

    def to_internal_value(self, data):
        return data

    def validate(self, data):
        _handle_missing_fields(self, data)

        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email, password=password)

        if user is None:
            raise exceptions.AuthenticationFailed(
                detail={'message': 'Bad credentials'})

        return {'email': user.email, 'token': user.token}
