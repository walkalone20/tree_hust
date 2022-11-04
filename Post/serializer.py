from rest_framework import serializers
from .models import Post,Draft
from Tools import check


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('posted_by', 'post_title', 'post_content', 'tag')

    def save(self, *args, **kwargs):
        if not check(self.post_title):
            raise serializers.ValidationError({'post_title': '标题不合法'})        
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

    def save(self, *args, **kwargs):
        if not check(self.draft_title):
            raise serializers.ValidationError({'draft_title': '标题不合法'})        
        if not check(self.draft_content):
            raise serializers.ValidationError({'draft_content': '内容不合法'})
        # ^ 检查内容是否合法

        super.save(*args, **kwargs)

class DeleteDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('id')

class SkimDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('id', 'drafted_by', 'draft_title', 'draft_content', 'tag')

class OpenDraftSerializer(serializers.ModelSerializer):
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