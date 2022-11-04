from django.urls import path
from .views import CreatePostView, SkimPostView, OpenPostView, DeletePostView
from .views import FilterPostView, SearchPostView, CollectionView

#URLConf
urlpatterns = [
    path('create_post/', CreatePostView.as_view()),
    path('delete_post/', DeletePostView.as_view()),
    path('skim_post/', SkimPostView.as_view()),
    path('open_post/', OpenPostView.as_view()),
    path('filter_post/', FilterPostView.as_view()),
    path('search_post/', SearchPostView.as_view()),
    path('collect_post/', CollectionView.as_view(), name='Collection'),
]