from rest_framework.response import Response
from rest_framework import permissions,status,generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.contrib.auth import login
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
            data['token']=AuthToken.objects.create(auser)[1]
        else:
            data=serializer.errors
        return Response(data)
	
class ChangePasswordAPI(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

class UpdateProfileAPI(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateUserSerializer