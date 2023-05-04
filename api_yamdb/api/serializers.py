from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import ValidationError
from reviews.models import Category, Genre, Title, User, Review, Comment

import re

USERNAME_NAME: int = 150
EMAIL: int = 254


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'id', 'password', 'last_login',
            'is_superuser', 'is_staff', 'is_active',
            'date_joined', 'user_permissions', 'groups')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'id', 'password', 'last_login',
            'is_superuser', 'is_staff', 'is_active',
            'date_joined', 'user_permissions', 'groups')
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Оценки ставятся в диапазоне от 0 до 10 включительно'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
                request.method == 'POST'
                and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Вы уже оставляли отзыв')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
                                     max_length=USERNAME_NAME)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=USERNAME_NAME)
    email = serializers.EmailField(required=True, max_length=EMAIL)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        pattern = re.compile(r'^[\w.@+-]+')

        if pattern.fullmatch(value) is None:
            match = re.split(pattern, value)
            symbol = ''.join(match)
            raise ValidationError(f'Некорректные символы в username: {symbol}')
        if value == 'me':
            raise ValidationError('Ник "me" нельзя регистрировать!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        exclude = ('review',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title


class UserEditSerializer(UsersSerializer):
    class Meta(UsersSerializer.Meta):
        read_only_fields = ('role',)
