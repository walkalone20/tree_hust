from django.urls import path
from . import views
from .views import UserView

#URLConf
urlpatterns = [
    path('add/', views.addUser,name="addUser"),
    path('user/', UserView.as_view()),
    path('register/', views.RegisterAPI.as_view(),name="registermynigga"),
]