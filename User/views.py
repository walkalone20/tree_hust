from django.shortcuts import  render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Post import serializer
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
            else:
                data=serializer.errors
            return Response(data)
	

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    # ^ tell queryset what we want to return 
    serializer_class = UserSerializer
    # ^ how to convert this into some format (using PostSerializer)

@api_view(['GET'])
def getData(request):
	users=User.objects.all()
	serializer=UserSerializer(users,mant=True)
	return Response(serializer.data)

@api_view(['POST'])
def addUser(request):
	serializer=UserSerializer(data=request.data)
	if serializer.is_valid():
		serializer.save()
	return Response(serializer.data)
