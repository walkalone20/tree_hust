from turtle import pos
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
# ^ status: allows us to get access to http status 
from .models import Post
from .serializer import PostSerializer, CreatePostSerializer
from rest_framework.views import APIView
# ^ allow us to override some default method
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

# Create your views here.

# class CreatePostView(generics.CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class ListPostView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     # ^ tell queryset what we want to return 
#     serializer_class = PostSerializer
#     # ^ how to convert this into some format (using PostSerializer)



"""
    @type: API 接口, 创建一个帖子
    @url: /post/create_post
    @method: post
    @param: 
        - post_title: 帖子的标题
        - post_content: 帖子的内容
        - tag: 帖子的标签 (FIXME: 用户指定？)
    @return:
        - post.data: json格式的创建成功的帖子的所有信息
        - status: HTTP状态码, 成功为201 CREATED; 失败为400 BAD_REQUEST (FIXME:)
"""
@login_required # TODO:?
class CreatePostView(APIView):
    serializer_class = CreatePostSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.reuqest.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            
            # TODO: 根据当前session获取user_id
            post_content = serializer.data.get('post_content')
            tag = serializer.data.get('tag')    # FIXME: ?

            post = Post(post_content=post_content, tag=tag)
            post.save()

            return Response(post.data, status=status.HTTP_201_CREATED)

        return Response(request.data, status=status.HTTP_400_BAD_REQUEST)  # FIXME: bad request?

"""
    @type: API 接口, 总览所有帖子
    @url: /post/skim_post
    @method: get
    @param: null
    @return:
        - post.data: json格式的所有帖子的概要信息
            - 用户
            - 标题
            - 创建时间
            - 标签
            - 评论数 
            - 观看数
            - 点赞数
        - status: HTTP状态码, 成功为200 OK; 失败为400 BAD_REQUEST (FIXME:)
"""
class SkimPostView(APIView):
    pass


"""
    @type: API 接口, 打开并查看一个帖子
    @url: /post/open_post
    @method: get
    @param: id (post的id)
    @return:
        - post.data: json格式的一个特定帖子的具体信息
        - status: HTTP状态码, 成功为200 OK; 失败为400 BAD_REQUEST (FIXME:)
"""
class OpenPostView(APIView):
    pass

