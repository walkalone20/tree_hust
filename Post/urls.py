from django.urls import path
from .views import CreatePostView, SkimPostView, OpenPostView, DeletePostView, CollectionView
from .views import CollectionListView, CreateDraftView, DeleteDraftView, UpdateDraftView
from .views import BrowserListView, OpenDraftView, UploadDraftView, SkimDraftView
from .views import UpdatePostView, MyPostView, CommentPostView, UpvotePostView, DownvotePostView
from .views import DeleteCommentView, VoteCommentView
#URLConf
urlpatterns = [
    path('post/', SkimPostView.as_view(), name='skim-post'),
    path('post/my', MyPostView.as_view(), name='my-post'),
    path('post/create/', CreatePostView.as_view(), name='create-post'),

    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete-post'),
    path('post/<int:pk>/', OpenPostView.as_view(), name='open-post'),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='update-post'),
    path('post/<int:pk>/upvote/', UpvotePostView.as_view(), name='Upvote-post'),
    path('post/<int:pk>/downvote/', DownvotePostView.as_view(), name='Downvote-post'),

    path('post/<int:pk>/comment/', CommentPostView.as_view(), name='comment-post'),
    path('post/<int:pk>/comment/<int:on>/delete', DeleteCommentView.as_view(), name='delete-comment'),
    path('post/<int:pk>/comment/<int:on>/vote', VoteCommentView.as_view(), name='vote-comment'),


    path('collect_post/', CollectionView.as_view()),
    path('skim_collect_post/', CollectionListView.as_view()),

    path('skim_browser_post/', BrowserListView.as_view()),

    path('draft/', SkimDraftView.as_view(), name='skim-draft'),
    path('draft/<int:pk>/', OpenDraftView.as_view(), name='open-draft'),
    path('draft/create/', CreateDraftView.as_view(), name='create-draft'),
    path('draft/<int:pk>/delete/', DeleteDraftView.as_view(), name='delete-draft'),
    path('draft/<int:pk>/update/', UpdateDraftView.as_view(), name='update-draft'),
    path('draft/<int:pk>/upload/', UploadDraftView.as_view(), name='upload-draft'),

]