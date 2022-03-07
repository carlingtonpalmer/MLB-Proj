from django.urls import path, include
from . import views
# from reset_password import views as view_pass
# from django.contrib.auth import views as auth_views



urlpatterns = [
    # users
    path('login/', views.LoginUserApiView.as_view()),
    path('social-login/', views.SocialLogin.as_view()),
    path('user/<int:pk>/', views.UserUpdateView.as_view()),
    path('register/', views.Register.as_view()),
    path('logout/', views.LogoutUserView.as_view()),
    path('users/', views.UserViewset.as_view()),

    # email code confirmation
    path('send-confirm-code/', views.ConfirmEmailView.as_view()),
    path('confirm-code/', views.ConfirmEmailCodeView.as_view()),
    
]