from tkinter.ttk import Style
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    
    class Meta:
        model=User
        fields=['email','username','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def save(self):
        auser=User(email=self.validated_data['email'],username=self.validated_data['username'])
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'password':'Passwords must match.'})
        auser.set_password(password)
        auser.save()
        return auser


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')
        extra_kwargs = {
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        
        if user.email!=value:
            token=RefreshToken.for_user(user)

            current_site=get_current_site(self.context['request']).domain
            relativeLink=reverse('verify email')
            absurl='http://'+current_site+relativeLink+'?token='+str(token)
            email_body='Hi, '+user.username+'! Use the link below to verify your new email:\n'+absurl

            email=EmailMessage(subject='Verify your email',body=email_body,to=[value])
            email.send()

        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return Response({
            'notion':"We've successfully reset your email address, but it hasn't been verified yet. If you don't\
                verify it in time, you cannot login to Treehust next time.",
            'new email':instance.email,
            'new username':instance.username
        },status=status.HTTP_200_OK)