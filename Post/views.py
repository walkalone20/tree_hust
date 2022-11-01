from rest_framework import generics
from .models import Post
from .serializer import PostSerializer

# Create your views here.

class PostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    # ^ tell queryset what we want to return 
    serializer_class = PostSerializer
    # ^ how to convert this into some format (using PostSerializer)

