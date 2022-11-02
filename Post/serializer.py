from rest_framework import serializers
from .models import Post
from Tools import check


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('posted_by', 'post_title', 'post_content', 'tag')

    def save(self, *args, **kwargs):
        if not check(self.post_title):
            raise serializers.ValidationError({'content_title': '标题不合法'})        
        if not check(self.post_content):
            raise serializers.ValidationError({'post_content': '内容不合法'})
        # ^ 检查内容是否合法

        super.save(*args, **kwargs)


class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id')


class SkimPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'created_at', 'post_title', 'tag', 'likes', 'watches', 'comments')


class OpenPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id')