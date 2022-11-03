from turtle import pos
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from rest_framework import generics, status
# ^ status: allows us to get access to http status 
from rest_framework.views import APIView
# ^ allow us to override some default method
from rest_framework.response import Response
# ^ Response in a json format
from django.shortcuts import get_object_or_404

from User.models import User
from .models import Post
# ^ import all the models
from .serializer import CreatePostSerializer, SkimPostSerializer, DeletePostSerializer, OpenPostSerializer
# ^ import all the serializers

# Create your views here.


class CreatePostView(APIView):
    serializer_class = CreatePostSerializer

    @login_required
    def post(self, request, format=None):
        """
            @type: API 接口, 创建一个帖子
            @url: /post/detailed_post
            @method: post
            @param: 
                - post_title: 帖子的标题
                - post_content: 帖子的内容
                - tag: 帖子的标签 (根据当前用户所处的tag下默认指定或用户选择)
            @return:
                - post.data: json格式的创建成功的帖子的所有信息
                - status: HTTP状态码, 成功为201 CREATED; 失败为400 BAD_REQUEST
            @exception:
                - ValidationError: 标题 或 内容 不合法时抛出
        """
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer= self.serializer_class(data=request.data)
        if serializer.is_valid():
            posted_by = User.objects.filter(id=self.request.user.id)
            post_title = serializer.data.get('post_title')
            post_content = serializer.data.get('post_content')
            tag = serializer.data.get('tag')

            post = Post(post_content=post_content, tag=tag, post_title=post_title, posted_by=posted_by)
            post.save()

            return Response(post.data, status=status.HTTP_201_CREATED)

        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
    

class DeletePostView(APIView):
    serializer_class = DeletePostSerializer

    @login_required
    def post(self, request, format=None):
        """
            @type: API 接口, 删除一个帖子
            @url: /post/detailed_post
            @method: delete
            @param: 
                - id: 帖子的id标识
            @return:
                - status: HTTP状态码, 删除成功为200 OK, 删除失败为400 BAD_REQUEST   
        """
        serializer = self.serializer_class(data=request.data)

        id = serializer.data.get('id')
        post= Post.objects.filter(id=id)
        
        posted_by = post.get('posted_by')
        if self.request.user.id != posted_by.id:
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        # ^ 判断是否有删除的权限

        post.delete()
        # ^ 因为设置了on_delete=CASCADE, 也同时删除了附着在帖子下面的评论

        return Response(request.data, status=status.HTTP_200_OK)


class SkimPostView(generics.ListAPIView):
    """
        @type: API 接口, 总览所有帖子
        @url: /post/skim_post
        @method: get
        @param: null
        @return:
            - post.data: json格式的所有帖子的概要信息 (帖子id, 用户, 临时名, 标题, 创建时间, 标签, 评论数, 观看数, 点赞数)
            - status: HTTP状态码, 成功为200 OK; 失败为400 BAD_REQUEST
    """
    queryset = Post.objects.all()
    # ^ tell queryset what we want to return 
    serializer_class = SkimPostSerializer
    # ^ how to convert this into some format (using PostSerializer)


class OpenPostView(APIView):
    serializer_class = OpenPostSerializer
    def get(self, request, format=None):
        """
            @type: API 接口, 点进一个帖子
            @url: /post/detailed_post
            @method: get
            @param: 
                - id: 帖子的id标识 (post的id)
            @return:
                - post.data: json格式的创建成功的帖子的所有信息和评论的信息
                - status: HTTP状态码, 获取成功为200 OK; 失败为400 BAD_REQUEST            
        """
        serializer = self.serializer_class(data=request.data)

        id = serializer.data.get('id')
        post = Post.objects.filter(id=id)

        return Response(post.data, status=status.HTTP_200_OK)

        





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
    def delete(self, request):
        post = get_object_or_404(Post, slug=request.data.get('slug'))
        if request.user in post.favourite.all():
            post.favourite.remove(request.user)
            return Response({'detail': 'User removed from post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)