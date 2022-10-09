from django.db import models

# Create your models here.

STATUS_CHOICE = [
    (0, NORMAL), 
    (1, NEGATIVE), 
    (2, NEGATIVE_FOLD)
    (3, USER_FOLD)
    (4, USER_DELETE)
    (5, ADMIN_FOLD)
    (6, ADMIN_DELETE)
]

Index = 0

class Post:
    PostID = models.IntergerField(primary_key = True)
    ID = models.IntegerField()  # 发帖人编号
    ReplyTo = models.IntegerField()
    Time = models.DateTimeField()
    Text = models.TextField()  # markdown 文本内容
    Like = models.IntegerField()  # 赞踩数
    Status = models.IntegerField(choice = STATUS_CHOICE)  # 评论显示状态
    Tag = models.CharField()
    Father_Post_ID = models.IntegerField() # 父帖编号
    Sub_Comment = [] # 子帖编号

    def __init__(self, ID, ReplyTo, Father_Post_ID, Time, Text, Tag):
        self.PostID = (Index += 1)
        self.ID = ID
        self.ReplyTo = ReplyTo
        self.Time = Time
        self.Text = Text
        self.Like = 0
        self.Tag = Tag
        self.Father_Comment = Father_Comment_ID
        self.Status = NORMAL
    
    def Reply_To(Father_Post_ID):
        DB_Query(Father_Post_ID).Sub_Comment.append(self.PostID)
        self.Father_Post_ID = Father_Post_ID

    def Vote(self, Like):
        self.Like += Like
        self.Update_Status()

    def Update_Status(self):
        if Status <= 2:
            if Like <= -50:
                Status = NEGATIVE_FOLD
            elif Like <= -10:
                Status = NEGATIVE
            else:
                Status = NORMAL
