from turtle import pos
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions,generics
# ^ status: allows us to get access to http status 
from rest_framework import permissions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils import timezone

from .models import Post, Draft, Comment


from .serializer import CreatePostSerializer, SkimPostSerializer, OpenPostSerializer
from .serializer import CreateDraftSerializer, SkimCollectionSerializer, SkimBrowserSerializer
from .serializer import SkimDraftSerializer, OpenDraftSerializer, UpdateDraftSerializer
from .serializer import UpdatePostSerializer, UpvotePostSerializer, DownvotePostSerializer
from .serializer import UpvoteCommentSerializer, DownvoteCommentSerializer, CreateCommentSerializer
from .serializer import SkimCommentSerializer, CollectPostSerializer


##################################### Post View ################################################
class CreatePostView(generics.CreateAPIView):
    """
    创建一个帖子, 需要处于登录状态
    @url: /post/create/
    @method: post
    @param: post_title, post_content, tag
    @return: 创建成功的帖子的对应信息
    """
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    authentication_classes = [TokenAuthentication]
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
    @param: [tag], [ordering], [search]
    @return: 所有帖子信息的概览
    """
    queryset = Post.objects.all()
    serializer_class = SkimPostSerializer
    model = Post
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['tag']
    ordering_fields = ['last_modified', 'likes', 'watches', 'stars']
    ording = ['last_modified']
    search_fields = ['post_title', 'post_content']
    
    # TODO: add pagination?


class MyPostView(generics.ListAPIView):
    """
    浏览自己发的的帖子, 需要处于登录状态
    @url: /post/my/
    @method: get
    @param: null
    @return: 用户自己创建的帖子的概要信息
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
    点进一个帖子浏览详细信息
    @url: /post/<int:pk>/
    @method: get
    @param: null
    @return: 帖子的所有信息和评论的信息
    """
    serializer_class = OpenPostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = Post.objects.filter(id=pk).first()

        if self.request.user.is_authenticated and self.request.user not in post.browser.all():
            post.browser.add(self.request.user)
            post.watches += 1
            post.save()

        # if self.request.user not in post.browser.all():
        #     post.browser.add(self.request.user, through_defaults={"browser_time": timezone.now()})
        #     post.watches += 1
        #     post.save()
        # else:
        #     post.browser.get(self.self.request.user)
        #     post.browser.add(self.request.user, through_defaults={"browser_time": timezone.now()})
        return super().retrieve(request, *args, **kwargs)
    
    
class UpdatePostView(generics.UpdateAPIView):
    """
    对帖子标题和内容进行编辑, 需要owner验证
    @url: /post/<int:pk>/update/
    @method: put
    @param: post_title, post_content
    @return: update后的帖子的部分信息
    """
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class DeletePostView(generics.DestroyAPIView):
    """
    删除一个帖子, 需要owner验证
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
    upvote一个帖子, 需要登录
    @url: /post/<int:pk>/upvote/
    @method: put
    @param: likes
    @return: upvote后的likes
    """
    queryset = Post.objects.all()
    serializer_class = UpvotePostSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class DownvotePostView(generics.UpdateAPIView):
    """
    downvote一个帖子, 需要登录
    @url: /post/<int:pk>/downvote/
    @method: put
    @param: hates
    @return: downvote后的hates
    """
    queryset = Post.objects.all()
    serializer_class = DownvotePostSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class SkimBrowserView(generics.ListAPIView):
    """
    概览自己浏览过的所有信息, 需要登录
    @url: /post/browser/
    @method: get
    @param: null
    @return: 当前用户浏览的所有帖子的一些信息(包括浏览的时间)
    """
    queryset = Post.objects.all()
    serializer_class = SkimBrowserSerializer
    model = Post
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        request = self.request
        qs = super().get_queryset(*args, **kwargs)
        browser = request.user.user_browser.all()
        qs = qs.filter(id__in=browser)
        return qs


# class BrowserListView(APIView):
#     serializer_class = SkimBrowserSerializer

#     @login_required
#     def get(self,request):
#         return Response(request.user.user_browser.all(), status=status.HTTP_200_OK)


class CollectPostView(generics.UpdateAPIView):
    """
    收藏一个帖子, 需要登录
    @url: /post/<int:pk>/collect
    @method: put
    @param: stars
    @return: 当前用户收藏的帖子
    """
    queryset = Post.objects.all()
    serializer_class = CollectPostSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class SkimCollectionView(generics.ListAPIView):
    """
    概览自己收藏的帖子, 需要登录
    @url: /post/collection
    @method: get
    @param: 
    @return: 当前用户收藏的所有帖子
    """
    queryset = Post.objects.all()
    serializer_class = SkimCollectionSerializer
    model = Post
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        request = self.request
        qs = super().get_queryset(*args, **kwargs)
        collections = request.user.user_collection.all()
        qs = qs.filter(id__in=collections)

        return qs


# class CollectionView(APIView):
#     bad_request_message = 'An error has occurred'
    
#     @login_required
#     def post(self, request):
#         post = get_object_or_404(Post, slug=request.data.get('slug'))
#         if request.user not in post.favourite.all():
#             post.favourite.add(request.user)
#             return Response({'detail': 'User added to post'}, status=status.HTTP_200_OK)
#         return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

#     @login_required
#     def delete(self, request):
#         post = get_object_or_404(Post, slug=request.data.get('slug'))
#         if request.user in post.favourite.all():
#             post.favourite.remove(request.user)
#             return Response({'detail': 'User removed from post'}, status=status.HTTP_204_NO_CONTENT)
#         return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


# class CollectionListView(APIView):
#     serializer_class = SkimCollectionSerializer

#     def get(self,request):
#         return Response(request.user.user_favorite.all(), status=status.HTTP_200_OK)




##################################### Comment View #####################################
class CreateCommentView(generics.CreateAPIView):
    """
    发布一个评论, 其中pk=0表示对帖子进行评论, pk!=0则表示对编号为pk的帖子进行评论(使用url进行评论更简便)
    @url: /post/<int:pk>/comment
    @method: post
    @param: comment_under
    @return: 发布的评论的部分内容
    """
    queryset = Comment.objects.all()
    serializer_class = CreateCommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        from rest_framework import serializers
        comment = Comment()

        comment_content = serializer.validated_data['comment_content']
        comment.comment_content = comment_content

        comment_under = serializer.validated_data['comment_under']
        comment.comment_under = comment_under

        pk = self.kwargs.get('pk')
        if pk != 0:
            reply_to = Comment.objects.filter(id=pk).first()
            comment.reply_to = reply_to
        else:
            comment.reply_to = None

        if self.request.user.is_authenticated:
            comment.comment_by = self.request.user
            comment.save()
            return comment
        else:
            raise serializers.ValidationError({"detailed": "please login first!"})


class DeleteCommentView(generics.DestroyAPIView):
    """
    删除一个评论, 需要登录, 对编号为pk的帖子进行删除(使用url更简便)
    @url: /post/<int:pk>/delete
    @method: delete
    @param: comment_under
    @return: 删除的评论的概要内容
    """
    queryset = Comment.objects.all()
    serializer_class = SkimCommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        return qs.filter(comment_by=request.user)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class UpvoteCommentView(generics.UpdateAPIView):
    """
    upvote一个评论
    @url: /post/comment/<int:pk>/upvote/
    @method: put
    @param: likes
    @return: upvote之后的likes
    """
    queryset = Comment.objects.all()
    serializer_class = UpvoteCommentSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class DownvoteCommentView(generics.UpdateAPIView):
    """
    downvote一个评论
    @url: /post/comment/<int:pk>/downvote/
    @method: put
    @param: hates
    @return: downvote之后的hates
    """
    queryset = Comment.objects.all()
    serializer_class = DownvoteCommentSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]




##################################### Draft View ############################################
class CreateDraftView(generics.CreateAPIView):
    """
    在草稿箱中创建一个草稿, title和content均为可选参数, tag必选
    @url: /draft/create
    @method: post
    @param: [draft_title], [draft_content], tag
    @return: 创建成功的草稿的部分信息
    """
    queryset = Draft.objects.all()
    serializer_class = CreateDraftSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        draft_title = serializer.validated_data.get('draft_title')
        draft_content = serializer.validated_data.get('draft_content')
        tag = serializer.validated_data.get('tag')
        serializer.save(draft_title=draft_title, draft_content=draft_content, tag=tag)
    

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

#         draft.delete()

#         return Response(request.data, status=status.HTTP_200_OK)


class SkimDraftView(generics.ListAPIView):
    """
        总览草稿箱中的草稿内容
        @url: /draft/
        @method: get
        @param: null
        @return: 所有草稿信息的概览
    """
    model = Draft
    queryset = Draft.objects.all()
    serializer_class = SkimDraftSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        return qs.filter(drafted_by=request.user)


class OpenDraftView(generics.RetrieveAPIView):
    """
    点进一个草稿
    @url: /draft/<int:pk>/
    @method: get
    @param: null
    @return: 草稿中的信息, (前端将其送到编辑框中, 即保留了草稿的编辑状态)
    """
    serializer_class = OpenDraftSerializer
    queryset = Draft.objects.all()
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        return qs.filter(drafted_by=request.user)


class UpdateDraftView(generics.UpdateAPIView):
    """
    对草稿的新的编辑结果进行上传
    @url: /draft/<int:pk>/update/
    @method: put
    @param: [draft_title], [draft_content]
    @return: update后的draft的部分信息
    """
    queryset = Draft.objects.all()
    serializer_class = UpdateDraftSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request
        return qs.filter(drafted_by=request.user)


class DeleteDraftView(generics.DestroyAPIView):
    """
    删除草稿箱中的某一个草稿
    @url: /draft/<int:pk>/delete/
    @method: delete
    @param: null
    @return: 删除的草稿的部分内容
    """
    queryset = Draft.objects.all()
    serializer_class = SkimDraftSerializer   # ? 没搞懂什么鬼
    authentication_classes = [TokenAuthentication]
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
    上传一个草稿(将原来的草稿删除, 然后将其中的内容上传到post数据库中, 如果内容审核没有通过则不删除)
    @url: /draft/<int:pk>/upload/
    @method: delete
    @param: nulww
    @return: 上传的草稿的内容
    """

    queryset = Draft.objects.all()
    serializer_class = OpenDraftSerializer   # ? 没搞懂什么鬼
    authentication_classes = [TokenAuthentication]
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

        if not instance.draft_title:
            raise serializers.ValidationError({"message": "标题为空"})
        post.post_title = check(instance.draft_title)

        if not instance.draft_content:
            raise serializers.ValidationError({"message": "内容为空"})
        post.post_content = check(instance.draft_content)

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

#         post.delete()

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
    
