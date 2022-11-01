from django.db import models

# Create your models here.

class Post(models.Model):
    # PostID = models.IntergerField(primary_key=True)
    user_id = models.IntegerField(null=False)  # 发帖人编号
    reply_to = models.IntegerField()  # * 给谁回复，comment的属性
    time = models.DateTimeField(null=False)   # 发帖时间
    text = models.TextField(null=False)  # markdown 文本内容
    like = models.IntegerField(null=False, default=0)  # 赞踩数
    tag = models.TextField(default='default')    # 帖子的标签
    father_post_id = models.IntegerField() # * 父帖编号，comment的属性
    # sub_comment = [] # 子帖编号

    def __init__(self, user_id, reply_to, time, text, like, tag):
        self.user_id = user_id
        self.reply_to = reply_to
        self.time = time
        self.text = text
        self.like = like
        self.tag = tag
    
    # def reply_to(Father_Post_ID):
    
    # def vote(self, Like):


# class Draft:
#     DraftID = models.IntergerField(primary_key = True)
#     ID = models.IntegerField()  # 编辑草稿人的编号
#     ReplyTo = models.IntegerField()
#     Time = models.DateTimeField()
#     Text = models.TextField()  # markdown 文本内容
#     Like = models.IntegerField()  # 赞踩数
#     Status = models.IntegerField(choice = STATUS_CHOICE)  # 评论显示状态
#     Tag = models.CharField()
#     Father_Post_ID = models.IntegerField() # 父帖编号
#     Sub_Comment = [] # 子帖编号

