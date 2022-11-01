from django.urls import path
from . import views

#URLConf
urlpatterns = [
    path("register/", views.register_request, name="register")
]