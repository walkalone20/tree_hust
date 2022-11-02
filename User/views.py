from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.models import AuthToken
from django.contrib.auth import login
from User.serializer import RegistrationSerializer
from rest_framework import generics
import get_object_or_404()

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
	
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class CollectionView(APIView):
    bad_request_message = 'An error has occurred'

    def post(self, request):
        post = get_object_or_404(Post, slug=request.data.get('slug'))
        if request.user not in post.favourite.all():
            post.favourite.add(request.user)
            return Response({'detail': 'User added to post'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        post = get_object_or_404(Post, slug=request.data.get('slug'))
        if request.user in post.favourite.all():
            post.favourite.remove(request.user)
            return Response({'detail': 'User removed from post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)