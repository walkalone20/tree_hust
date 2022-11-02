from email.policy import default
from django.db import models
from django.forms import BooleanField
from Tools import generate_name_animal
from Tools import generate_name_food
import random


# Create your models here.

def generate_random_name():
    sample = random.randint(0, 1)
    if sample == 1:
        return generate_name_animal()
    else:
        return generate_name_food()

class Post(models.Model):
    posted_by = models.ForeignKey("User.User", on_delete=models.CASCADE)  # 发帖人
    tmp_name = models.CharField(null=False, default=generate_random_name, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)   # * 发帖时间 (generated automatically)
    post_title = models.TextField(null=False)   # 帖子标题
    post_content = models.TextField(null=False)  # 帖子内容
    likes = models.IntegerField(null=False, default=0)  # * 赞踩数 (generated automatically)
    watches = models.IntegerField(null=False, default=0)    # * 观看数 (generated automatically)
    comments = models.IntegerField(null=False, default=0)   # * 评论数 (generated automatically)
    tag = models.CharField(default='default', max_length=30)    # 帖子的标签
    favourite = models.ManyToManyField("User.User", related_name='post_favourite', blank=True)  #收藏帖子

    # PostID = models.IntergerField(primary_key=True)
    # reply_to = models.IntegerField()  # 给谁回复，comment的属性
    # father_post_id = models.IntegerField() # 父帖编号，comment的属性
    # sub_comment = [] # 子帖编号
"""
    def __init__(self, posted_by, post_title, post_content, tag):
        self.user_id = posted_by
        self.post_title = post_title
        self.post_content = post_content
        self.likes = 0
        self.tag = tag
"""

class Draft(models.Model):
    drafted_by = models.ForeignKey("User.User", on_delete=models.CASCADE)  # 编辑草稿的人
    draft_title = models.TextField(null=False)  # 草稿标题
    draft_content = models.TextField()  # 草稿内容
    tag = models.CharField(default='default', max_length=30) # 草稿标签


class Comment(models.Model):
    comment_under = models.ForeignKey("Post", on_delete=models.CASCADE) # 在某个帖子下的所有评论
    created_at = models.DateTimeField(auto_now_add=True) # * 发帖时间 (generated automatically)
    likes = models.IntegerField(null=False, default=0)  # * 赞踩数 (generated automatically)
    return_to = models.IntegerField(null=False, default=-1) 
    comment_by = models.ForeignKey("User.User", on_delete=models.CASCADE)
    tmp_name = models.CharField(null=False, default=generate_random_name, max_length=20)
    # * -1表示回复帖子, 正整数表示回复另一个回复 (generated automatically)



