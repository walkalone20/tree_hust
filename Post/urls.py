from django.urls import path
from .views import CreatePostView, SkimPostView, OpenPostView,CollectionView

#URLConf
urlpatterns = [
    path('create_post', CreatePostView.as_view()),
    path('skim_post', SkimPostView.as_view()),
    path('open_post', OpenPostView.as_view()),
    path('collect_post/', CollectionView.as_view(), name='Collection'),
]