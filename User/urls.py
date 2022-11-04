from django.urls import path,include
from . import views
from knox import views as knox_views
from rest_framework.authtoken.views import obtain_auth_token

#URLConf
urlpatterns = [
    path('register/', views.RegisterAPI.as_view(),name="registermynigga"), # TODO: nigga!
    path('login/', obtain_auth_token,name="login"),   # TODO: nigga!
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('change_password/<int:pk>/', views.ChangePasswordAPI.as_view(), name='change password'),
    path('update_profile/<int:pk>/', views.UpdateProfileAPI.as_view(), name='update profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password reset')),
]