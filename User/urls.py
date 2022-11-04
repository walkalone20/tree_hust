from django.urls import path,include
from . import views
from knox import views as knox_views

#URLConf
urlpatterns = [
    path('register/', views.RegisterAPI.as_view(),name="registermynigga"), # TODO: nigga!
    path('login/', views.LoginAPI.as_view(),name="loginmynigga"),   # TODO: nigga!
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('change_password/<int:pk>/', views.ChangePasswordAPI.as_view(), name='change password'),
    path('update_profile/<int:pk>/', views.UpdateProfileAPI.as_view(), name='update profile'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password reset')),
]