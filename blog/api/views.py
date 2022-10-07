from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from blog.models import Post
from.serializers import PostSerializer


@api_view(['GET'])
def getRoutes(request):
    posts = [
        'GET /api',
        'GET /api/posts',
        'GET /api/posts/:id'
    ]
    return Response(posts)


@api_view(['GET', 'POST'])
def get_posts(request, format=None):

    if request.method == 'GET':
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def getPost(request, pk, format=None):

    try:
        posts = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostSerializer(posts, many=False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(posts, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        posts.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




    

    