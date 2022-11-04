from django.urls import path
from .views import CreatePostView, SkimPostView, OpenPostView, DeletePostView, CollectionView
from .views import CollectionListView, CreateDraftView, DeleteDraftView, UpdateDraftView
from .views import BrowserListView, OpenDraftView, DraftListView, FilterPostView, SearchPostView
from .views import UpdatePostView

#URLConf
urlpatterns = [
    path('skim_post/', SkimPostView.as_view()),
    path('create_post/', CreatePostView.as_view()),
    path('<int:pk>/delete_post/', DeletePostView.as_view()),
    path('<int:pk>/open_post/', OpenPostView.as_view()),
    path('<int:pk>/update_post/', UpdatePostView.as_view()),
    path('filter_post', FilterPostView.as_view()),
    path('search_post', SearchPostView.as_view()),

    path('collect_post/', CollectionView.as_view()),
    path('skim_collect_post/', CollectionListView.as_view()),

    path('skim_browser_post/', BrowserListView.as_view()),

    path('skim_draft/', DraftListView.as_view()),
    path('open_draft/', OpenDraftView.as_view()),
    path('create_draft', CreateDraftView.as_view()),
    path('delete_draft', DeleteDraftView.as_view()),
    path('update_draft', UpdateDraftView.as_view()),

]