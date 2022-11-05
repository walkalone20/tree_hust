from rest_framework import serializers
from .models import Post, Draft, Comment
from Tools import check
from rest_framework.reverse import reverse
from django.utils import timezone


############################# Post Serializer##################################
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


class SkimCommentSerializer(serializers.ModelSerializer):
    # comment_url = serializers.SerializerMethodField(method_name='get_comment_url', read_only=True)
    # delete_url = serializers.SerializerMethodField(method_name='get_delete_url', read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'comment_under', 'comment_time', 'reply_to', # 'comment_url', 'delete_url',
        'likes', 'hates', 'comment_content',  'comment_by', 'tmp_name')
    
    def get_comment_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated:
            return reverse('create-comment', kwargs={"pk": obj.pk, "on": request.kwargs.get('on')}, request=request)
        return None
    
    def get_delete_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated and request.user == obj.comment_by:
            return reverse('delete-comment', kwargs={"pk": obj.pk, "on": request.kwargs.get('on')}, request=request)
        return None 


class OpenPostSerializer(serializers.ModelSerializer):
    post_comment = SkimCommentSerializer(many=True, read_only=True)
    update_url = serializers.SerializerMethodField(method_name='get_update_url', read_only=True)
    delete_url = serializers.SerializerMethodField(method_name='get_delete_url', read_only=True)
    comment_url = serializers.SerializerMethodField(method_name='get_comment_url', read_only=True)
    upvote_url = serializers.SerializerMethodField(method_name='get_upvote_url', read_only=True)
    downvote_url = serializers.SerializerMethodField(method_name='get_downvote_url', read_only=True)
    has_upvoted = serializers.SerializerMethodField(method_name='get_has_upvoted', read_only=True)
    has_downvoted = serializers.SerializerMethodField(method_name='get_has_downvoted', read_only=True)  

    class Meta:
        model = Post
        fields = ('id', 'update_url', 'delete_url', 'comment_url', 'upvote_url', 'downvote_url', 'has_upvoted',
           'has_downvoted', 'posted_by', 'tmp_name','post_title', 'post_content', 'last_modified', 'likes', 'hates',
           'watches', 'comments', 'tag', 'post_comment')

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
            return reverse('create-comment', kwargs={"pk": obj.pk, "on": 0}, request=request)
        return None
    
    def get_upvote_url(self, obj):
        request = self.context['request']
        if request == None:
            return None
        if request.user.is_authenticated:
            return reverse('upvote-post', kwargs={"pk": obj.pk}, request=request)
        return None

    def get_downvote_url(self, obj):
        request = self.context['request']
        if request == None:
            return None
        if request.user.is_authenticated:
            return reverse('downvote-post', kwargs={"pk": obj.pk}, request=request)
        return None

    def get_has_upvoted(self, obj):
        request = self.context['request']
        if request == None:
            return None
        if not request.user.is_authenticated:
            return False
        
        upvote = obj.upvote.all()
        if request.user in upvote:
            return True
        return False
        
    def get_has_downvoted(self, obj):
        request = self.context['request']
        if request == None:
            return None
        if not request.user.is_authenticated:
            return False

        downvote = obj.downvote.all()
        if request.user in downvote:
            return True 
        return False


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
        if not request.user.is_authenticated:
            raise serializers.ValidationError({"message": "当前尚未登陆"})
        
        upvote = instance.upvote.all()
        downvote = instance.downvote.all()

        if request.user in upvote:
            instance.upvote.remove(request.user)
            instance.likes-=1
        elif request.user in downvote:
            instance.downvote.remove(request.user)
            instance.hates-=1
        
            instance.upvote.add(request.user)
            instance.likes+=1
        else:
            instance.upvote.add(request.user)
            instance.likes+=1
        instance.save()

        return instance

class DownvotePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('hates', )

    def update(self, instance, validated_data):
        request = self.context['request'] 
        if not request.user.is_authenticated:
            raise serializers.ValidationError({"message": "当前尚未登陆"})
        
        upvote = instance.upvote.all()
        downvote = instance.downvote.all()
        # vote = validated_data.pop('validated_data')

        if request.user in downvote:
            instance.downvote.remove(request.user)
            instance.hates-=1
        elif request.user in upvote:
            instance.upvote.remove(request.user)
            instance.likes-=1
        
            instance.downvote.add(request.user)
            instance.hates+=1
        else:
            instance.downvote.add(request.user)
            instance.hates+=1
        instance.save()

        return instance

class SkimCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'last_modified', 'post_title', 'tag', 'likes', 'watches', 'comments')


class SkimBrowserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'posted_by', 'tmp_name', 'last_modified', 'post_title', 'tag', 'likes', 'watches', 'comments')




############################## Comment Serializer ##################################
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_content', )

    def validate_comment_content(self, value):
        if not check(value):
            raise serializers.ValidationError({'message': '评论内容不合法'})

        return value


class UpvoteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('likes', )

    def update(self, instance, validated_data):
        request = self.context['request']
        if not request.user.is_authenticated:
            raise serializers.ValidationError({"message": "当前尚未登陆"})
        
        upvote = instance.upvote.all()
        downvote = instance.downvote.all()

        if request.user in upvote:
            instance.upvote.remove(request.user)
            instance.likes-=1
        elif request.user in downvote:
            instance.downvote.remove(request.user)
            instance.hates-=1
            instance.upvote.add(request.user)
            instance.likes+=1
        else:
            instance.upvote.add(request.user)
            instance.likes+=1
        
        instance.save()

        return instance

class DownvoteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('likes', )

    def update(self, instance, validated_data):
        request = self.context['request'] 
        if not request.user.is_authenticated:
            raise serializers.ValidationError({"message": "当前尚未登陆"})
        
        upvote = instance.upvote.all()
        downvote = instance.downvote.all()

        if request.user in downvote:
            instance.downvote.remove(request.user)
            instance.hates-=1
        elif request.user in upvote:
            instance.upvote.remove(request.user)
            instance.likes-=1
            instance.downvote.add(request.user)
            instance.hates+=1
        else:
            instance.downvote.add(request.user)
            instance.hates+=1

        instance.save()

        return instance

############################## Draft Serializer##########################
class CreateDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('drafted_by', 'draft_title', 'draft_content', 'tag')

    def create(self, validated_data):
        request = self.context.get('request')
        draft = Draft()
        draft.draft_title = validated_data['draft_title']
        draft.draft_content = validated_data['draft_content']   
        draft.tag = validated_data['tag']

        if request.user.is_authenticated:
            draft.drafted_by = request.user
            draft.save()
            return draft
        else:
            raise serializers.ValidationError({"detailed": "please login first!"})


class SkimDraftSerializer(serializers.ModelSerializer):
    open_url = serializers.HyperlinkedIdentityField(view_name='open-draft', lookup_field='pk', read_only=True)

    class Meta:
        model = Draft
        fields = ('id', 'open_url', 'drafted_by', 'draft_title', 'tag')


class OpenDraftSerializer(serializers.ModelSerializer):
    update_url = serializers.SerializerMethodField(method_name='get_update_url', read_only=True)
    delete_url = serializers.SerializerMethodField(method_name='get_delete_url', read_only=True)
    upload_url = serializers.SerializerMethodField(method_name='get_upload_url', read_only=True)

    class Meta:
        model = Draft
        fields = ('id', 'update_url', 'delete_url', 'upload_url', 'drafted_by', 
        'draft_title', 'draft_content', 'tag')
    
    def get_update_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated and request.user == obj.drafted_by:
            return reverse('update-draft', kwargs={"pk": obj.pk}, request=request)
        return None

    def get_delete_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated and request.user == obj.drafted_by:
            return reverse('delete-draft', kwargs={"pk": obj.pk}, request=request)
        return None   

    def get_upload_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated and request.user == obj.drafted_by:
            return reverse('upload-draft', kwargs={"pk": obj.pk}, request=request)
        return None


class UpdateDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Draft
        fields = ('draft_title', 'draft_content', 'tag')

        # extra_kwargs = {
        #     'draft_title': {'required': True},
        #     'tag': {'required': True},
        # }

    def update(self, instance, validated_data):
        request = self.context['request']
        if not request.user.is_authenticated:
            raise serializers.ValidationError({"message": "当前尚未登陆"})
        if request.user != instance.drafted_by:
            raise serializers.ValidationError({"message": "没有权限"})

        return super().update(instance, validated_data)

