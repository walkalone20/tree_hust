from turtle import pos
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions,generics, status, mixins
# ^ status: allows us to get access to http status 
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


from User.models import User
from .models import Post, Draft, Comment


from .serializer import CreatePostSerializer, SkimPostSerializer, OpenPostSerializer
from .serializer import SkimCollectionSerializer, SkimBrowserSerializer, CreateDraftSerializer
from .serializer import SkimDraftSerializer, OpenDraftSerializer, UpdateDraftSerializer
from .serializer import UpdatePostSerializer, UpvotePostSerializer, DownvotePostSerializer
from .serializer import UpvoteCommentSerializer, DownvoteCommentSerializer, CreateCommentSerializer
from .serializer import SkimCommentSerializer

from .permissions import IsOwnerOrReadOnlyPermission

##################################### Post View ################################################
class CreatePostView(generics.CreateAPIView):
    """
    创建一个帖子
    @url: /post/create/
    @method: post
    @param: post_title, post_content, tag
    @return: 创建成功的帖子的部分信息
    """
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [IsOwnerOrReadOnlyPermission]

    def perform_create(self, serializer):
        post_title = serializer.validated_data.get('post_title')
        post_content = serializer.validated_data.get('post_content')
        tag = serializer.validated_data.get('tag')
        return serializer.save(post_title=post_title, post_content=post_content, tag=tag)


class SkimPostView(generics.ListAPIView):
    """
        根据tag和search对帖子进行筛选和对帖子内容搜索, 并根据ordering排序, 均为可选参数
        @url: /post/
        @method: get
        @param: tag, ordering, search
        @return: 满足tag的所有帖子信息的概览
    """
    queryset = Post.objects.all()
    serializer_class = SkimPostSerializer
    model = Post
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['tag']
    ordering_fields = ['last_modified', 'likes', 'watches', 'stars', 'comments']
    ording = ['last_modified']
    search_fields = ['post_title', 'post_content']
    
    # TODO: add pagination


class MyPostView(generics.ListAPIView):
    """
    浏览自己发的的帖子
    @url: /post/my/
    @method: get
    @param: null
    @return: 用户的帖子的概要信息
    """
    queryset = Post.objects.all()
    serializer_class = SkimPostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        return qs.filter(posted_by=request.user)


class OpenPostView(generics.RetrieveAPIView):
    """
    点进一个帖子
    @url: /post/<int:pk>/
    @method: get
    @param: null
    @return: 帖子的所有信息和评论的信息
    """
    serializer_class = OpenPostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'
    # TODO: 显示相关评论
    # TODO: 增加浏览记录
    
    
class UpdatePostView(generics.UpdateAPIView):
    """
    根据tag对帖子进行编辑
    @url: /post/<int:pk>/update/
    @method: put
    @param: post_title, post_content (, last_modified)
    @return: update后的帖子的部分信息
    """
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class DeletePostView(generics.DestroyAPIView):
    """
    删除一个帖子
    @url: /post/<int:pk>/delete/
    @method: delete
    @param: null
    @return: 是否删除成功 
    """
    queryset = Post.objects.all()
    serializer_class = SkimPostSerializer   # ? 没搞懂什么鬼
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        return qs.filter(posted_by=request.user)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class UpvotePostView(generics.UpdateAPIView):
    """
    upvote一个帖子
    @url: /post/<int:pk>/upvote/
    @method: put
    @param: likes
    @return: 
    """
    queryset = Post.objects.all()
    serializer_class = UpvotePostSerializer
    lookup_field = 'pk'
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class DownvotePostView(generics.UpdateAPIView):
    """
    downvote一个帖子
    @url: /post/<int:pk>/downvote/
    @method: put
    @param: hates
    @return: 
    """
    queryset = Post.objects.all()
    serializer_class = DownvotePostSerializer
    lookup_field = 'pk'
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class BrowserListView(APIView):
    serializer_class = SkimBrowserSerializer

    @login_required
    def get(self,request):
        return Response(request.user.user_browser.all(), status=status.HTTP_200_OK)


class CollectionView(APIView):
    bad_request_message = 'An error has occurred'
    # TODO: 需要加两个get方法
    
    @login_required
    def post(self, request):
        post = get_object_or_404(Post, slug=request.data.get('slug'))
        if request.user not in post.favourite.all():
            post.favourite.add(request.user)
            return Response({'detail': 'User added to post'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

    @login_required
    def delete(self, request):  # FIXME: delete 方法有问题
        post = get_object_or_404(Post, slug=request.data.get('slug'))
        if request.user in post.favourite.all():
            post.favourite.remove(request.user)
            return Response({'detail': 'User removed from post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


class CollectionListView(APIView):
    serializer_class = SkimCollectionSerializer

    def get(self,request):
        return Response(request.user.user_favorite.all(), status=status.HTTP_200_OK)




##################################### Comment View #####################################
class CreateCommentView(generics.CreateAPIView):
    """
    发布一个评论
    @url: /post/<int:pk>/comment/<int:on>
    @method: post
    @param: reply_to
    @return: 
    """
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from rest_framework import serializers
        comment = Comment()
        comment.comment_content = serializer.validated_data['comment_content']

        comment_under = Post.objects.filter(id=self.kwargs.get('pk')).first()
        comment.comment_under = comment_under

        reply_to = Comment.objects.filter(id=self.kwargs.get('on')).first()
        comment.reply_to = reply_to

        if self.request.user.is_authenticated:
            comment.comment_by = self.request.user
            comment.save()
            return comment
        else:
            raise serializers.ValidationError({"detailed": "please login first!"})


class DeleteCommentView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = SkimCommentSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'on'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        request = self.request
        return qs.filter(comment_by=request.user)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class UpvoteCommentView(generics.UpdateAPIView):
    """
    upvote一个评论
    @url: /post/<int:pk>/comment/<int:on>/upvote/
    @method: put
    @param: likes
    @return: 
    """
    queryset = Comment.objects.all()
    serializer_class = UpvoteCommentSerializer
    lookup_field = 'on'
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class DownvoteCommentView(generics.UpdateAPIView):
    """
    downvote一个评论
    @url: /post/<int:pk>/comment/<int:on>/downvote/
    @method: put
    @param: hates
    @return: 
    """
    queryset = Comment.objects.all()
    serializer_class = DownvoteCommentSerializer
    lookup_field = 'on'
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]




##################################### Draft View ############################################
class CreateDraftView(APIView):
    serializer_class = CreateDraftSerializer
    
    @login_required
    def post(self, request, format=None):
        serializer= self.serializer_class(data=request.data)
        if serializer.is_valid():
            drafted_by = User.objects.filter(id=self.request.user.id)
            draft_title = serializer.data.get('draft_title')
            draft_content = serializer.data.get('draft_content')
            tag = serializer.data.get('tag')

            draft = Draft(draft_content=draft_content, tag=tag, draft_title=draft_title, drafted_by=drafted_by)
            draft.save()

            return Response(draft.data, status=status.HTTP_201_CREATED)

        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    

# class oldDeleteDraftView(APIView):
#     serializer_class = SkimDraftSerializer

#     @login_required
#     def post(self, request, format=None):
#         serializer = self.serializer_class(data=request.data)

#         id = serializer.data.get('id')
#         draft= Draft.objects.filter(id=id)
        
#         drafted_by = draft.get('drafted_by')
#         if self.request.user.id != drafted_by.id:
#             return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
#         # ^ 判断是否有删除的权限

#         draft.delete()
#         # ^ 因为设置了on_delete=CASCADE, 也同时删除了附着在帖子下面的评论

#         return Response(request.data, status=status.HTTP_200_OK)


class SkimDraftView(generics.ListAPIView):
    """
        总览草稿
        @url: /draft/
        @method: get
        @param: 
        @return: 所有草稿信息的概览
    """
    model = Draft
    queryset = Draft.objects.all()
    serializer_class = SkimDraftSerializer
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        return qs.filter(drafted_by=request.user)


class OpenDraftView(generics.RetrieveAPIView):
    """
    点进一个帖子
    @url: /draft/<int:pk>/
    @method: get
    @param: null
    @return: 帖子的所有信息和评论的信息
    """
    serializer_class = OpenDraftSerializer
    queryset = Draft.objects.all()
    lookup_field = 'pk'
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        return qs.filter(drafted_by=request.user)


class UpdateDraftView(generics.UpdateAPIView):
    """
    对草稿进行编辑
    @url: /draft/<int:pk>/update/
    @method: put
    @param: draft_title, draft_content
    @return: update后的draft的部分信息
    """
    queryset = Draft.objects.all()
    serializer_class = UpdateDraftSerializer
    lookup_field = 'pk'
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        return qs.filter(drafted_by=request.user)


class DeleteDraftView(generics.DestroyAPIView):
    """
    删除一个草稿
    @url: /draft/<int:pk>/delete/
    @method: delete
    @param: null
    @return: 是否删除成功 
    """
    queryset = Draft.objects.all()
    serializer_class = SkimDraftSerializer   # ? 没搞懂什么鬼
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        return qs.filter(drafted_by=request.user)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class UploadDraftView(generics.DestroyAPIView):
    """
    上传一个草稿
    @url: /draft/<int:pk>/upload/
    @method: delete
    @param: null
    @return: 是否删除成功 
    """

    queryset = Draft.objects.all()
    serializer_class = OpenDraftSerializer   # ? 没搞懂什么鬼
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        return qs.filter(drafted_by=request.user)

    def perform_destroy(self, instance):
        from rest_framework import serializers
        from Tools import check
        from django.utils import timezone
        request = self.request
        post = Post()
        post.posted_by = request.user

        if instance.draft_title is None or not check(instance.draft_title):
            raise serializers.ValidationError({"message": "标题不合法"})
        post.post_title = instance.draft_title

        if instance.draft_content is None or not check(instance.draft_content):
            raise serializers.ValidationError({"message": "内容不合法"})
        post.post_content = instance.draft_content

        if instance.tag is None:
            raise serializers.ValidationError({"message": "标签不合法"})
        post.tag = instance.tag

        post.created_at = timezone.now()
        post.save()

        return super().perform_destroy(instance)   




# class oldCreatePostView(APIView):
#     serializer_class = CreatePostSerializer

#     @login_required 
#     def post(self, request, format=None):
#         serializer= self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             posted_by = User.objects.filter(id=self.request.user.id)
#             post_title = serializer.data.get('post_title')
#             post_content = serializer.data.get('post_content')
#             tag = serializer.data.get('tag')

#             post = Post(post_content=post_content, tag=tag, post_title=post_title, posted_by=posted_by.get('id'))
#             post.save()

#             return Response(post.data, status=status.HTTP_201_CREATED)

#         return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


# class oldDeletePostView(APIView):
#     serializer_class = DeletePostSerializer

#     def delete(self, request, pk=None, format=None):

#         serializer = self.serializer_class(data=request.data)

#         post= Post.objects.filter(id=pk)
        
#         posted_by = post.get('posted_by')
#         if not request.user.is_authenticated or self.request.user != posted_by:
#             return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
#         # ^ 判断是否有删除的权限

#         post.delete()
#         # ^ 因为设置了on_delete=CASCADE, 也同时删除了附着在帖子下面的评论

#         return Response(request.data, status=status.HTTP_200_OK)

       
# class oldOpenPostView(APIView):    
#     serializer_class = OpenPostSerializer

#     def get(self, request, pk = None, format=None):
#         """
          
#         """
#         if pk == None:
#             return Response({"detailed": "url error!"}, status=status.HTTP_400_BAD_REQUEST)

#         post = Post.objects.filter(id=pk)
#         serializer = self.serializer_class(data=post)

#         serializer.is_valid(raise_exception=True)

#         # if request.user.is_authenticated:
#         #     if request.user not in post.browser.all():
#         #         post.browser.add(request.user)
#         #         post.update()

#         # post.update()
#         
#         # if(request.user.is_authenticated):
#         #     if request.user not in post.browser.all():
#         #         post.browser.add(request.user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
