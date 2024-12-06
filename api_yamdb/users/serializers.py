from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.validators import RegexValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z',
        message='Имя пользователя может содержать только буквы, цифры, точки, дефисы, подчеркивания и плюсики.')]
    )
    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Выберите другой username'
            )
        user_email = User.objects.filter(email=data['email']).first()
        user_username = User.objects.filter(username=data['username']).first()
        if user_email != user_username:
            msg = 'email' if user_email else 'username'
            raise serializers.ValidationError(
                'Пользователь с таким {} уже существует.'.format(msg)
            )
        return data


class UserAccessTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user,
            data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'})
        return data