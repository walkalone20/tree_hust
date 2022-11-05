from django.urls import path
from .views import CreatePostView, SkimPostView, OpenPostView, DeletePostView, CollectionView
from .views import CollectionListView, CreateDraftView, DeleteDraftView, UpdateDraftView
from .views import BrowserListView, OpenDraftView, DraftListView, FilterPostView, SearchPostView
from .views import UpdatePostView, MyPostView

#URLConf
urlpatterns = [
    path('post/', SkimPostView.as_view(), name='skim-post'),
    path('post/my', MyPostView.as_view(), name='my-post'),
    path('post/create/', CreatePostView.as_view(), name='create-post'),

    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete-post'),
    path('post/<int:pk>/', OpenPostView.as_view(), name='open-post'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='update-post'),

    path('post/filter/', FilterPostView.as_view(), name='filter-post'),
    path('post/search/', SearchPostView.as_view(), name='search-post'),


    path('collect_post/', CollectionView.as_view()),
    path('skim_collect_post/', CollectionListView.as_view()),

    path('skim_browser_post/', BrowserListView.as_view()),

    path('skim_draft/', DraftListView.as_view()),
    path('open_draft/', OpenDraftView.as_view()),
    path('create_draft', CreateDraftView.as_view()),
    path('delete_draft', DeleteDraftView.as_view()),
    path('update_draft', UpdateDraftView.as_view()),

]