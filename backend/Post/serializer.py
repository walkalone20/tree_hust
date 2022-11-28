from rest_framework import serializers
from .models import Post, Draft, Comment
from Tools import check
from rest_framework.reverse import reverse
from django.utils import timezone
from Tools.random_name import generate_random_name
from Tools.random_avatar import generate_random_avatar


############################# Post Serializer##################################
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_title', 'post_content', 'tag')

    def validate_post_title(self, value):
        if not value:
            raise serializers.ValidationError({'message': '标题为空'})

        return check(value)

    def validate_post_content(self, value):
        if not value:
            raise serializers.ValidationError({'message': '内容为空'})

        return check(value)

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post()
        post.post_title = check(validated_data['post_title'])
        post.post_content = check(validated_data['post_content'])
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
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'open_url', 'posted_by', 'last_modified', 
         'post_title', 'tag', 'likes', 'stars', 'watches', 'comments')

    def get_comments(self, obj):
        comments = Comment.objects.filter(comment_under=obj)
        return comments.count()


class SkimCommentSerializer(serializers.ModelSerializer):
    comment_url = serializers.SerializerMethodField(method_name='get_comment_url', read_only=True)
    delete_url = serializers.SerializerMethodField(method_name='get_delete_url', read_only=True)
    upvote_url = serializers.SerializerMethodField(method_name='get_upvote_url', read_only=True)
    downvote_url = serializers.SerializerMethodField(method_name='get_downvote_url', read_only=True)
    tmp_name = serializers.SerializerMethodField(method_name='get_tmp_name', read_only=True)
    avatar = serializers.SerializerMethodField(method_name='get_avatar', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'tmp_name', 'avatar', 'comment_under', 'comment_time', 'reply_to', 'comment_url', 'delete_url',
        'upvote_url', 'downvote_url', 'likes', 'hates', 'comment_content',  'comment_by', 'tmp_name',
        'avatar')

    def get_avatar(self, obj):
        request = self.context['request']
        if request is None:
            return None
        return generate_random_avatar(obj.comment_under.id, obj.comment_by.id)
    
    def get_tmp_name(self, obj):
        request = self.context['request']
        if request is None:
            return None
        return generate_random_name(obj.comment_under.id, obj.comment_by.id)

    def get_comment_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated:
            return reverse('create-comment', kwargs={"pk": obj.pk}, request=request)
        return None
    
    def get_delete_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated and request.user == obj.comment_by:
            return reverse('delete-comment', kwargs={"pk": obj.pk}, request=request)
        return None

    def get_upvote_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated:
            return reverse('upvote-comment', kwargs={"pk": obj.pk}, request=request)
        return None

    def get_downvote_url(self, obj):
        request = self.context['request']
        if request is None:
            return None
        if request.user.is_authenticated:
            return reverse('downvote-comment', kwargs={"pk": obj.pk}, request=request)
        return None



class OpenPostSerializer(serializers.ModelSerializer):
    post_comment = SkimCommentSerializer(many=True, read_only=True)
    update_url = serializers.SerializerMethodField(method_name='get_update_url', read_only=True)
    delete_url = serializers.SerializerMethodField(method_name='get_delete_url', read_only=True)
    comment_url = serializers.SerializerMethodField(method_name='get_comment_url', read_only=True)
    upvote_url = serializers.SerializerMethodField(method_name='get_upvote_url', read_only=True)
    downvote_url = serializers.SerializerMethodField(method_name='get_downvote_url', read_only=True)
    collect_url = serializers.SerializerMethodField(method_name='get_collect_url', read_only=True)
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)
    
    has_upvoted = serializers.SerializerMethodField(method_name='get_has_upvoted', read_only=True)
    has_downvoted = serializers.SerializerMethodField(method_name='get_has_downvoted', read_only=True)
    has_collected = serializers.SerializerMethodField(method_name='get_has_collected', read_only=True)
    tmp_name = serializers.SerializerMethodField(method_name='get_tmp_name', read_only=True)
    avatar = serializers.SerializerMethodField(method_name='get_avatar', read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'tmp_name', 'avatar', 'update_url', 'delete_url', 'comment_url', 'upvote_url', 'downvote_url', 'collect_url', 
           'has_upvoted', 'has_downvoted', 'has_collected', 'posted_by', 'tmp_name','post_title', 'post_content', 
           'last_modified', 'likes', 'hates', 'watches', 'comments', 'stars', 'tag', 'post_comment')
        # ! comment_url 需要前端加上当前post的id作为参数 -> comment_under
    
    def get_comments(self, obj):
        comments = Comment.objects.filter(comment_under=obj)
        return comments.count()

    def get_avatar(self, obj):
        request = self.context['request']
        if request is None:
            return None
        return generate_random_avatar(obj.id, obj.posted_by.id)
    
    def get_tmp_name(self, obj):
        request = self.context['request']
        if request is None:
            return None
        return generate_random_name(obj.id, obj.posted_by.id)

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

    def get_comment_url(self, obj): 
        request = self.context['request']
        if request == None:
            return None
        if request.user.is_authenticated:
            return reverse('create-comment', kwargs={"pk": 0}, request=request)
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
    
    def get_collect_url(self, obj):
        request = self.context['request']
        if request == None:
            return None
        if request.user.is_authenticated:
            return reverse('collect-post', kwargs={"pk": obj.pk}, request=request)
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

    def get_has_collected(self, obj):
        request = self.context['request']
        if request == None:
            return None
        if not request.user.is_authenticated:
            return False

        collection = obj.collection.all()
        if request.user in collection:
            return True
        return False


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('post_title', 'post_content')

    def validate_post_title(self, value):
        if not value:
            raise serializers.ValidationError({'message': '标题为空'})

        return check(value)

    def validate_post_content(self, value):
        if not value:
            raise serializers.ValidationError({'message': '内容为空'})

        return check(value)

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


class CollectPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('stars', )

    def update(self, instance, validated_data):
        request = self.context['request'] 
        if not request.user.is_authenticated:
            raise serializers.ValidationError({"message": "当前尚未登陆"})
        
        collection = instance.collection.all()
        # vote = validated_data.pop('validated_data')

        if request.user in collection:
            instance.collection.remove(request.user)
            instance.stars-=1
        else:
            instance.collection.add(request.user)
            instance.stars+=1

        instance.save()

        return instance

class SkimCollectionSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)
    open_url = serializers.HyperlinkedIdentityField(view_name='open-post', lookup_field='pk', read_only=True)
    star_time = serializers.SerializerMethodField(method_name='get_star_time', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'open_url', 'posted_by', 'post_title', 'tag', 'likes','hates', 'watches', 'comments', 'star_time')

    def get_comments(self, obj):
        comments = Comment.objects.filter(comment_under=obj)
        return comments.count()
    
    def get_star_time(self,obj):
        request=self.context['request']
        user = obj.collection_time_set.filter(user=request.user).first()
        return user.star_time


class SkimBrowserSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)
    open_url = serializers.HyperlinkedIdentityField(view_name='open-post', lookup_field='pk', read_only=True)
    browser_time = serializers.SerializerMethodField(method_name='get_browser_time', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'open_url', 'posted_by', 'post_title', 'tag', 'likes', 'hates', 'stars', 'watches',
        'comments', 'browser_time')

    def get_comments(self, obj):
        comments = Comment.objects.filter(comment_under=obj)
        return comments.count()
    
    def get_browser_time(self,obj):
        request=self.context['request']
        user = obj.browser_history_set.filter(user=request.user).first()
        return user.browser_time




############################## Comment Serializer ##################################
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment_content', 'comment_under')

    def validate_comment_content(self, value):
        if not value:
            raise serializers.ValidationError({'message': '评论它没内容啊'})
        return check(value)


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
        fields = ('hates', )

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
        fields = ( 'draft_title', 'draft_content', 'tag')

    def create(self, validated_data):
        request = self.context.get('request')
        draft = Draft()
        draft.draft_title = check(validated_data['draft_title'])
        draft.draft_content = check(validated_data['draft_content'])   
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

