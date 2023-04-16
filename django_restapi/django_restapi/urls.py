from django.contrib import admin
from django.urls import path, include
from rest_application import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authors', views.AuthorList.as_view()),
    path('api/books', views.BookList.as_view()),
    path('api/borrows', views.BorrowList.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api/borrows/<int:pk>', views.BorrowRetrieveDestroy.as_view()),
    path('api/borrows/<int:pk>/edit/', views.BorrowRetrieveUpdate.as_view()),
    path('api/borrows/<int:pk>/return/', views.BorrowReturnBookUpdate.as_view()),
    path('api/user/create', views.UserCreate.as_view()),
    path('api/user/login', views.UserTokenList.as_view())

]