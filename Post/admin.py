from django.contrib import admin
from.models import Post,Draft,Comment

# Register your models here.
admin.site.register(Draft)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id','posted_by_username','post_title','likes', 'hates', 'upvoted_by','downvoted_by']

    def posted_by_username(self, request):
        return request.posted_by.username

    def upvoted_by(self, request):
        return "\n".join([p.username for p in request.upvote.all()])

    def downvoted_by(self, request):
        return "\n".join([p.username for p in request.downvote.all()])

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['id','comment_under_post','comment_by', 'comment_content', 'upvoted_by','downvoted_by']

    def comment_under_post(self, request):
        return request.comment_under.post_title

    def posted_by_username(self, request):
        return request.posted_by.username

    def upvoted_by(self, request):
        return "\n".join([p.username for p in request.upvote.all()])

    def downvoted_by(self, request):
        return "\n".join([p.username for p in request.downvote.all()])