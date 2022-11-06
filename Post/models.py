from email.policy import default
from django.db import models
from django.forms import BooleanField
from Tools import generate_name_animal
from Tools import generate_name_food
from Tools import generate_random_name
import random
from User.models import User


class Post(models.Model):
    TAG_CHOICES = [
        ('s', 'life is meaningless'),
        ('h', 'I am a procrastinator'),
        ('i', 'want to die'),
        ('t', 'venomous!'),
        ('a', 'I am a piece of shit'),
        ('b', 'I am the black sheep'),
    ]

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='user_post', verbose_name="posted by some user")  # & 发帖人
    tmp_name = models.CharField(null=False, default=generate_random_name, max_length=20)
    last_modified = models.DateTimeField(auto_now_add=True)   # * 发帖时间 (generated automatically)
    post_title = models.TextField(null=False)   # 帖子标题
    post_content = models.TextField(null=False)  # 帖子内容
    likes = models.IntegerField(null=False, default=0)  # * 赞数 (generated automatically)
    hates = models.IntegerField(null=False, default=0)  # * 踩数 (generated automatically)
    watches = models.IntegerField(null=False, default=0)    # * 观看数 (generated automatically)
    stars = models.IntegerField(null=False, default=0)  # * 收藏数 (generated automatically)
    comments = models.IntegerField(null=False, default=0)   # * 评论数 (generated automatically)
    tag = models.CharField(default='s', max_length=30, choices=TAG_CHOICES)    # 帖子的标签

    upvote = models.ManyToManyField(User, verbose_name="upvote by some user", 
        related_name='upvote_post', blank=True)   # & upvote帖子
    downvote = models.ManyToManyField(User, verbose_name="downvote by some user", 
        related_name='downvote_post', blank=True)   # & downvote帖子
    collection = models.ManyToManyField(User, verbose_name="collected by some user", 
        related_name='user_collection', blank=True)  # & 收藏帖子
    browser = models.ManyToManyField(User, verbose_name="browsered by some user", # through='browser_history',
        related_name='user_browser', blank=True)   # & 浏览记录


# class browser_history(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     browser_time = models.DateTimeField(auto_now_add=True)


class Draft(models.Model):
    TAG_CHOICES = [
        ('s', 'life is meaningless'),
        ('h', 'I am a procrastinator'),
        ('i', 'want to die'),
        ('t', 'venomous!'),
        ('a', 'I am a piece of shit'),
        ('b', 'I am the black sheep'),
    ]
    drafted_by = models.ForeignKey(User, on_delete=models.CASCADE,
        related_name='user_draft', verbose_name="draft drafted by some user")  # & 编辑草稿的人
    draft_title = models.TextField(null=False)  # 草稿标题
    draft_content = models.TextField(null=True, blank=True)  # 草稿内容
    tag = models.CharField(default='s', max_length=30, choices=TAG_CHOICES) # 草稿标签


class Comment(models.Model):
    tmp_name = models.CharField(null=False, default=generate_random_name, max_length=20)
    comment_under = models.ForeignKey(Post, on_delete=models.CASCADE, 
        related_name='post_comment', verbose_name="comment under some post") # & 在某个帖子下的所有评论
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, 
        related_name='user_comment', verbose_name="comment by some user")  # & 回复给某个人
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, default=None, null=True, blank=True,
        related_name='comment_comment', verbose_name='commeng on other comment')  # & 二级引用回复
    comment_content = models.TextField(null=False, default='')  # 内容
    comment_time = models.DateTimeField(auto_now_add=True) # * 发帖时间 (generated automatically)

    likes = models.IntegerField(null=False, default=0)  # * 赞数 (generated automatically)
    hates = models.IntegerField(null=False, default=0)  # * 踩数 (generated automatically)
    upvote = models.ManyToManyField(User, verbose_name="upvote by some user", 
        related_name='upvote_comment', blank=True)   # & upvote评论
    downvote = models.ManyToManyField(User, verbose_name="downvote by some user", 
        related_name='downvote_comment', blank=True)   # & downvote评论
    
