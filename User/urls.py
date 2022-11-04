from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

#URLConf
urlpatterns = [
    path('register/', views.RegisterAPI.as_view(),name="registermynigga"), # TODO: nigga!
    path('login/', obtain_auth_token,name="login"),   # TODO: nigga!
    path('logout/', views.LogoutAPI.as_view(), name='logout'),
    path('change_password/<int:pk>/', views.ChangePasswordAPI.as_view(), name='change password'),
    path('update_profile/<int:pk>/', views.UpdateProfileAPI.as_view(), name='update profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password reset')),
]