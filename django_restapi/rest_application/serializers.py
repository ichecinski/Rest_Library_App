from rest_framework import serializers
from .models import Author, Book, Borrow
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_id']
class BorrowSerializer(serializers.ModelSerializer):
    book = serializers.ReadOnlyField(source='book_id.title')
    author_first_name = serializers.ReadOnlyField(source='book_id.author_id.first_name')
    author_first_name = serializers.ReadOnlyField(source='book_id.author_id.first_name')
    author_last_name = serializers.ReadOnlyField(source='book_id.author_id.last_name')
    user_first_name = serializers.ReadOnlyField(source='user_id.first_name')
    user_last_name = serializers.ReadOnlyField(source='user_id.last_name')
    user_email = serializers.ReadOnlyField(source='user_id.email')
    user_id = serializers.ReadOnlyField(source='user_id.id')
    return_date = serializers.ReadOnlyField()
    class Meta:
        model = Borrow
        fields = ['id', 'user_id', 'user_first_name', 'user_last_name', 'user_email', 'book_id', 'book', 'author_first_name', 'author_last_name', 'borrow_date', 'return_date']

class BorrowReturnBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("This e-mail already exists")
        return lower_email
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', )