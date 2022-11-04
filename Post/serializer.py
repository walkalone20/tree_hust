from rest_framework import serializers
from .models import Post, Draft, Comment
from Tools import check


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_title', 'post_content', 'tag')

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post()
        post.post_title = validated_data['post_title']
        post.post_content = validated_data['post_content']
        if not check(post.post_title):
            raise serializers.ValidationError({'post_title': '标题不合法'})        
        if not check(post.post_content):
            raise serializers.ValidationError({'post_content': '内容不合法'})
            
        post.posted_by = request.user
        post.save()
        return post

        # if request.user.is_authenticated:
        #     post.posted_by = request.user
        #     post.save()
        #     return post
        # else:
        #     raise serializers.ValidationError({"detailed": "please login first!"})


class OpenPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'post_title', 'post_content', 'created_at', 'likes',
            'watches', 'comments', 'tag')




class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id')


class SkimPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'created_at', 'post_title', 'tag', 'likes', 'watches', 'comments')


class FilterPostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'created_at', 'post_title', 'tag', 'likes', 'watches', 'comments')


class SearchPostSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'created_at', 'post_title', 'tag', 'likes', 'watches', 'comments')


class SkimCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'created_at', 'post_title', 'tag', 'likes', 'watches', 'comments')


class SkimBrowserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'created_at', 'post_title', 'tag', 'likes', 'watches', 'comments')


class CreateDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('drafted_by', 'draft_title', 'draft_content', 'tag')


class DeleteDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('id')


class SkimDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('id', 'drafted_by', 'draft_title', 'draft_content', 'tag')


class OpenDraftSerializer(serializers.ModelSerializer): # FIXME: ??
    class Meta:
        model = Draft
        fields = ('id')


class UpdateDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('draft_title', 'draft_content', 'tag')
        extra_kwargs = {
            'draft_title': {'required': True},
            'tag': {'required': True},
        }

    def update(self, instance, validated_data):
            draft = self.context['request'].draft

            if draft.pk != instance.pk:
                raise serializers.ValidationError({"authorize": "You dont have permission for this draft."})

            instance.draft_title = validated_data['draft_title']
            instance.draft_content = validated_data['draft_content']
            instance.tag = validated_data['tag']

            instance.save()

            return instance

