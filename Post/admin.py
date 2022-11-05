from django.contrib import admin
from.models import Post,Draft,Comment

# Register your models here.
admin.site.register(Draft)
admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['id','posted_by_username','post_title','likes','voted_by']

    def posted_by_username(self, request):
        return request.posted_by.username

    def voted_by(self, request):
        return "\n".join([p.username for p in request.vote.all()])