from django.urls import path
from .views import PostView

#URLConf
urlpatterns = [
    path('post', PostView.as_view())
]