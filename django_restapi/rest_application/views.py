from django.shortcuts import render
from django.db.models import query
from rest_framework import generics
from .models import Author, Book, Borrow
from .serializers import AuthorSerializer, BookSerializer, BorrowSerializer,BorrowReturnBookSerializer, UserSerializer, TokenSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class AuthorList(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowList(generics.ListCreateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class BorrowRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def delete(self, request, *args, **kwargs):
        borrow = Borrow.objects.filter(pk=kwargs['pk'], user_id=self.request.user)
        if borrow.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('You are not the owner')
class BorrowRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        borrow = Borrow.objects.filter(pk=kwargs['pk'], user_id=self.request.user)
        if borrow.exists():
            return self.update(self, *args, **kwargs)
        else:
            raise ValidationError('You are not the owner')
class BorrowReturnBookUpdate(generics.UpdateAPIView):
    queryset = Borrow.objects.all()
    serializer_class = BorrowReturnBookSerializer
    permission_class = [IsAuthenticated]
    def put(self, request, *args, **kwargs):
        borrow = Borrow.objects.filter(pk=kwargs['pk'], user_id=self.request.user)
        if borrow.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError('You are not the owner')
    def perform_update(self, serializer):
        serializer.instance.return_date = timezone.now()
        serializer.save()
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )

class UserTokenList(generics.ListAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Token.objects.filter(user=self.request.user)
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=self.request.user)
        if user.exists():
            token = Token.objects.filter(user=self.request.user)
            if token.exists():
                return self.list(request, *args, **kwargs)
            else:
                token = Token.objects.create(user=self.request.user)
                return self.list(request, *args, **kwargs)
        else:
            raise ValidationError('You are not sign up')
