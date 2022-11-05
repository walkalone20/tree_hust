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
from .serializer import DeleteDraftSerializer, SkimDraftSerializer, OpenDraftSerializer, UpdateDraftSerializer
from .serializer import SearchPostSerialzer

from .permissions import IsOwnerOrReadOnlyPermission


class CreatePostView(generics.CreateAPIView):
    """
    创建一个帖子
    @url: /post/create_post
    @method: post
    @param: post_title, post_content, tag
    @return:
        - post.data: json格式的创建成功的帖子的所有信息
        - status: HTTP状态码, 成功为201 CREATED; 失败为400 BAD_REQUEST
    @exception:
        - ValidationError: 标题 或 内容 不合法时抛出
    """
    queryset = Post.objects.all()
    serializer_class = CreatePostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post_title = serializer.validated_data.get('post_title')
        post_content = serializer.validated_data.get('post_content')
        tag = serializer.validated_data.get('tag')
        serializer.save(post_title=post_title, post_content=post_content, tag=tag)

    # authentication_classes = [permissions.IsAuthenticated]
    # permission_classes = [IsOwnerOrReadOnlyPermission]


class SkimPostView(generics.ListAPIView):
    """
    总览所有帖子
    @url: /post/skim_post
    @method: get
    @param: null
    @return:
        - json格式的所有帖子的概要信息 (帖子id, 用户, 临时名, 标题, 创建时间, 标签, 评论数, 观看数, 点赞数)
    """
    queryset = Post.objects.all()
    serializer_class = SkimPostSerializer


class OpenPostView(generics.RetrieveAPIView):
    """
    点进一个帖子
    @url: /post/<int:pk>/
    @method: get
    @param: null
    @return:
      - post.data: json格式的创建成功的帖子的所有信息和评论的信息
      - status: HTTP状态码, 获取成功为200 OK; 失败为400 BAD_REQUEST  
    """
    serializer_class = OpenPostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'
    # TODO: 显示相关评论
    # TODO: 增加浏览记录
    
    
class UpdatePostView(generics.UpdateAPIView):
    """
        根据tag对帖子进行编辑
        @url: /post/<int:pk>/update
        @method: put
        @param: post_title, post_content, last_modified
        @return:
            - json格式的满足tag的所有帖子信息的概览
    """
    queryset = Post.objects.all()
    serializer_class = SkimPostSerializer
    lookup_field = 'pk'
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class DeletePostView(generics.DestroyAPIView):
    """
    删除一个帖子
    @url: /post/delete_post
    @method: delete
    @param: id(帖子的id)
    @return:
        - status: HTTP状态码, 删除成功为200 OK, 删除失败为400 BAD_REQUEST   
    """
    # serializer_class = DeletePostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'
    def get_queryset(self):
        queryset = Post.objects.filter(posted_by=self.request.user)
        return queryset

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class FilterPostView(generics.ListAPIView):
    """
        @type: API 接口, 根据tag对帖子进行筛选
        @url: /post/filter_post
        @method: get
        @param: tag
        @return:
            - json格式的满足tag的所有帖子信息的概览
    """
    queryset = Post.objects.all()
    serializer_class = SkimPostSerializer
    model = Post
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag']
    # ? paginate_by = 100


class TagFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.get('tag') is not None:
            queryset = queryset.filter(tag=request.get('tag'))
        return queryset


class SearchPostView(generics.ListAPIView):
    """
        @type: API 接口, 根据tag和search对帖子进行筛选和对帖子内容搜索
        @url: /post/search_post
        @method: get
        @param: 
            - tag: 帖子的标签
            - search: 对帖子标题和内容搜索的关键词
        @return:
            - json格式的满足tag和search(查询标题和内容)所有帖子信息的概览
    """
    queryset = Post.objects.all()
    serializer_class = SearchPostSerialzer
    model = Post
    filter_backends = [TagFilterBackend]
    search_fields = ['post_title', 'post_content']


class CollectionListView(APIView):
    serializer_class = SkimCollectionSerializer

    @login_required
    def get(self,request):
        return Response(request.user.user_favorite.all(), status=status.HTTP_200_OK)


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
    

class DeleteDraftView(APIView):
    serializer_class = DeleteDraftSerializer

    @login_required
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        id = serializer.data.get('id')
        draft= Draft.objects.filter(id=id)
        
        drafted_by = draft.get('drafted_by')
        if self.request.user.id != drafted_by.id:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        # ^ 判断是否有删除的权限

        draft.delete()
        # ^ 因为设置了on_delete=CASCADE, 也同时删除了附着在帖子下面的评论

        return Response(request.data, status=status.HTTP_200_OK)


class DraftListView(APIView):
    serializer_class = SkimDraftSerializer

    @login_required
    def get(self,request):
        return Response(request.user.user_draft.all(), status=status.HTTP_200_OK)


class OpenDraftView(APIView):
    serializer_class = OpenDraftSerializer

    @login_required
    def get(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        id = serializer.data.get('id')
        draft = Draft.objects.filter(id=id)

        return Response(draft.data, status=status.HTTP_200_OK)


class UpdateDraftView(generics.UpdateAPIView):

    queryset = Draft.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateDraftSerializer



# class oldCreatePostView(APIView):
#     serializer_class = CreatePostSerializer

#     @login_required # FIXME
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
    
