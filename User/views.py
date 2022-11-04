from rest_framework.response import Response
from rest_framework import permissions,status,generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import logout
from User.serializer import RegistrationSerializer,UpdateUserSerializer,ChangePasswordSerializer
from Post.models import Post
from .models import User


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer=self.get_serializer(data=request.data)
        data={}
        if serializer.is_valid():
            auser=serializer.save()
            data['response']="succesfully registered a new user, u know i'm saying??"
            data['email']=auser.email
            data['username']=auser.username
            data['token']=Token.objects.get(user=auser).key
        else:
            data=serializer.errors
        return Response(data)

class LogoutAPI(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes=[IsAuthenticated,]
    def get(request):
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully')

class ChangePasswordAPI(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class UpdateProfileAPI(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer