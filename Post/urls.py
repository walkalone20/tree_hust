from django.urls import path
from .views import CreatePostView, SkimPostView, OpenPostView, DeletePostView, CollectionView,CollectionListView,CreateDraftView,DeleteDraftView

#URLConf
urlpatterns = [
    path('create_post', CreatePostView.as_view()),
    path('delete_post', DeletePostView.as_view()),
    path('skim_post', SkimPostView.as_view()),
    path('open_post', OpenPostView.as_view()),
    path('collect_post/', CollectionView.as_view()),
    path('skim_collect_post/', CollectionListView.as_view()),
    path('create_draft', CreateDraftView.as_view()),
    path('delete_draft', DeleteDraftView.as_view()),
    path('update_draft', DeleteDraftView.as_view()),
]