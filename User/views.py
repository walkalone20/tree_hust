from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.contrib.auth import login
from .models import User
from User.serializer import RegistrationSerializer, UserSerializer
from rest_framework import generics

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        if request.method=='POST':
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
	
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
