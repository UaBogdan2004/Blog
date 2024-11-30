from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # Імпортуємо вбудовану вьюху
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<str:tag>/', views.post_list_by_tag, name='post_list_by_tag'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('post/delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', LoginView.as_view(), name='login'),  # Використовуємо вбудовану LoginView
    path('logout/', LogoutView.as_view(), name='logout'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('tag/<str:tag>/', views.post_list_by_tag, name='post_list_by_tag'),  # Маршрут для фільтрації по тегу

]
