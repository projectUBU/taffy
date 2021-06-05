from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import routers, serializers, viewsets
from blog.models import Post, Comment
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CommentSerializer

class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        post_pk = Post.objects.get(pk=pk)
        message = "Not allowed"
        print(post_pk.pk)

        if request.user.is_authenticated:
            is_liked = Post.objects.like_toggle(request.user, post_pk)
            liked_count = post_pk.liked.all().count()
            print(is_liked, liked_count)
            return Response({'liked': is_liked, 'likes_count': liked_count})

            # return Response({'liked': is_liked, 'likes_count': liked_count}) and redirect(f'/public/post/{post_pk.pk}/')
        return Response({"message": message}, status=400)


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]