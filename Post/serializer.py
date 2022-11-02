from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user_id', 'created_at','post_title', 'post_content', 'likes', 'tag')


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('posted_by', 'post_title', 'post_content', 'tag')


class SkimPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user_id', 'created_at', 'post_title', 'post_content', 'tag')

class OpenPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'user_id', 'created_at', 'post_title', 'post_content', 'likes', 'tag')