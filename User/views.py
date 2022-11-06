from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions,status,generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings
from User.serializer import RegistrationSerializer,UpdateUserSerializer,ChangePasswordSerializer
from .models import User
import jwt


class RegisterAPI(generics.GenericAPIView):
    """
    注册一个用户
    @url: /register/
    @method: post
    @param: email, username, password, password2
    @return: (response, email, username)
    """
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        user_data={}
        if serializer.is_valid():
            auser=serializer.save()
            user_data['response']="succesfully registered a new user, u know i'm saying??"
            user_data['email']=auser.email
            user_data['username']=auser.username
        else:
            user_data=serializer.errors
        
        if user_data!=serializer.errors:
            user=User.objects.get(email=serializer.data['email'])
            token=RefreshToken.for_user(user)

            current_site=get_current_site(request).domain
            relativeLink=reverse('verify email')
            absurl='http://'+current_site+relativeLink+'?token='+str(token)
            email_body='您好, '+user.username+'! 请点击下面的链接来验证您的邮箱，没有验证是不能登陆的哦..\n'+absurl

            email=EmailMessage(subject='Verify your email',body=email_body,to=[user.email])
            email.send()
        return Response(user_data)

class VerifyEmail(generics.GenericAPIView):
    """
    验证一个邮箱
    @url: /verify_email/
    @method: post
    @param: token
    @return: (response)
    """
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
            user=User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'Successfully activated!'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation expired!'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token!'},status=status.HTTP_400_BAD_REQUEST)

class CustomAuthTokenAPI(ObtainAuthToken):
    """
    登陆用户
    @url: /login/
    @method: post
    @param: email, password
    @return: (token, user_id, username, email)
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.is_verified==True:
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username':user.username,
                'email': user.email
            })
        else:
            token=RefreshToken.for_user(user)

            current_site=get_current_site(request).domain
            relativeLink=reverse('verify email')
            absurl='http://'+current_site+relativeLink+'?token='+str(token)
            email_body='Hi, '+user.username+'! Use the link below to verify your email:\n'+absurl

            email=EmailMessage(subject='Verify your email',body=email_body,to=[user.email])
            email.send()

            return Response({
                'error': "You haven't verify your email yet! Now we'll sent you another email to activate your account."
            })


class LogoutAPI(generics.GenericAPIView):
    """
    登出用户
    @url: /logout/
    @method: get
    @param: token
    @return: (response)
    """
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated,]
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully')

class ChangePasswordAPI(generics.UpdateAPIView):
    """
    更改密码
    @url: /change_password/<int:pk>/
    @method: put
    @param: old_password, password, password2
    @return: 根本没得返回消息
    """
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class UpdateProfileAPI(generics.UpdateAPIView):
    """
    更改个人信息
    @url: /update_profile/<int:pk>/
    @method: put
    @param: username, email, aboutme(可选)
    @return: (username, email, aboutme(可选))
    """
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer