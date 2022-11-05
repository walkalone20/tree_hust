from django.urls import path,include
from . import views

#URLConf
urlpatterns = [
    path('register/', views.RegisterAPI.as_view(),name="registermynigga"), # TODO: nigga!
    path('login/', views.CustomAuthTokenAPI.as_view(),name="login"),
    path('verify_email',views.VerifyEmail.as_view(),name='verify email'),
    path('logout/', views.LogoutAPI.as_view(), name='logout'),
    path('change_password/<int:pk>/', views.ChangePasswordAPI.as_view(), name='change password'),
    path('update_profile/<int:pk>/', views.UpdateProfileAPI.as_view(), name='update profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password reset')),
]