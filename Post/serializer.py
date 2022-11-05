from rest_framework import serializers
from .models import Post, Draft, Comment
from Tools import check
from rest_framework.reverse import reverse
from django.utils import timezone


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_title', 'post_content', 'tag')

    def validate_post_title(self, value):
        if not check(value):
            raise serializers.ValidationError({'message': '标题不合法'})

        return value

    def validate_post_content(self, value):
        if not check(value):
            raise serializers.ValidationError({'message': '内容不合法'})

        return value

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post()
        post.post_title = validated_data['post_title']
        post.post_content = validated_data['post_content']   
        post.tag = validated_data['tag']

        if request.user.is_authenticated:
            post.posted_by = request.user
            post.save()
            return post
        else:
            raise serializers.ValidationError({"detailed": "please login first!"})
    
    # def validate(self, attrs):
    #     request = self.context['request']
    #     if not request.user.is_authenticated:
    #         raise serializers.ValidationError({"message": "当前尚未登陆"})

    #     return super().validate(attrs)


class SkimPostSerializer(serializers.ModelSerializer):
    open_url = serializers.HyperlinkedIdentityField(view_name='open-post', lookup_field='pk', read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'open_url', 'posted_by', 'tmp_name', 'last_modified',
         'post_title', 'tag', 'likes', 'watches', 'comments')


class OpenPostSerializer(serializers.ModelSerializer):
    # comment = serializers.RelatedField(source='comment', many=True)
    update_url = serializers.SerializerMethodField(method_name='get_update_url', read_only=True)
    delete_url = serializers.SerializerMethodField(method_name='get_delete_url', read_only=True)
    comment_url = serializers.SerializerMethodField(method_name='get_comment_url', read_only=True)
    vote_url = serializers.SerializerMethodField(method_name='get_vote_url', read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'update_url', 'delete_url', 'comment_url', 'vote_url', 'posted_by', 'tmp_name', 'post_title', 
        'post_content', 'last_modified', 'likes', 'watches', 'comments', 'tag', 'post_comment')

    def get_update_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated and request.user == obj.posted_by:
            return reverse('update-post', kwargs={"pk": obj.pk}, request=request)
        return None

    def get_delete_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated and request.user == obj.posted_by:
            return reverse('delete-post', kwargs={"pk": obj.pk}, request=request)
        return None

    def get_comment_url(self, obj):  # TODO
        request = self.context['request']
        if request == None:
            return None
        if request.user.is_authenticated:
            return reverse('comment-post', kwargs={"pk": obj.pk}, request=request)
        return None
    
    def get_vote_url(self, obj):
        request = self.context['request']
        if request == None:
            return None
        if request.user.is_authenticated:
            return reverse('vote-post', kwargs={"pk": obj.pk}, request=request)
        
        return None



class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_title', 'post_content')

    def validate_post_title(self, value):
        if not check(value):
            raise serializers.ValidationError({'message': '标题不合法'})

        return value

    def validate_post_content(self, value):
        if not check(value):
            raise serializers.ValidationError({'message': '内容不合法'})

        return value

    def update(self, instance, validated_data):
        request = self.context['request']
        if not request.user.is_authenticated:
            raise serializers.ValidationError({"message": "当前尚未登陆"})
        if request.user != instance.posted_by:
            raise serializers.ValidationError({"message": "没有权限"})
        
        validated_data['last_modified'] = timezone.now()

        return super().update(instance, validated_data)


class UpvotePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('likes', )

    def update(self, instance, validated_data):
        request = self.context['request']
        # if not request.user.is_authenticated:
        #     raise serializers.ValidationError({"message": "当前尚未登陆"})
        # if abs(instance.likes - validated_data.get('likes')) != 1:
        #     raise serializers.ValidationError({"message": "不合法的likes"})
        
        upvote = instance.upvote.all()
        downvote = instance.downvote.all()
        # vote = validated_data.pop('validated_data')

        if request.user in upvote:
            instance.upvote.remove(request.user)
            instance.likes-=1
        elif request.user in downvote:
            instance.downvote.remove(request.user)
            instance.hates-=1
            instance.save()
        
        instance.upvote.add(request.user)
        instance.likes+=1
        instance.save()

        # return super().update(instance, validated_data)
        return instance

class DownvotePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('likes', )

    def update(self, instance, validated_data):
        request = self.context['request']
        # if not request.user.is_authenticated:
        #     raise serializers.ValidationError({"message": "当前尚未登陆"})
        # if abs(instance.likes - validated_data.get('likes')) != 1:
        #     raise serializers.ValidationError({"message": "不合法的likes"})
        
        upvote = instance.upvote.all()
        downvote = instance.downvote.all()
        # vote = validated_data.pop('validated_data')

        if request.user in downvote:
            instance.downvote.remove(request.user)
            instance.hates-=1
        elif request.user in upvote:
            instance.upvote.remove(request.user)
            instance.likes-=1
            instance.save()
        
        instance.downvote.add(request.user)
        instance.hates+=1
        instance.save()

        # return super().update(instance, validated_data)
        return instance


class SkimCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_under', 'last_modified', 'likes', 'comment_content', 'reply_to', 'comment_by', 'tmp_name')
    

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('reply_to', '', 'comment_content')

    def validate_comment_content(self, value):
        if not check(value):
            raise serializers.ValidationError({'message': '评论'})

        return value

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post()
        post.post_title = validated_data['post_title']
        post.post_content = validated_data['post_content']   
        post.tag = validated_data['tag']

        if request.user.is_authenticated:
            post.posted_by = request.user
            post.save()
            return post
        else:
            raise serializers.ValidationError({"detailed": "please login first!"})















class SkimCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'last_modified', 'post_title', 'tag', 'likes', 'watches', 'comments')





class SkimBrowserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'last_modified', 'post_title', 'tag', 'likes', 'watches', 'comments')


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


# class DeletePostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('id')


# class SearchPostSerialzer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ('id', 'posted_by', 'tmp_name', 'last_modified', 'post_title', 'tag', 'likes', 'watches', 'comments')
