from django.shortcuts import render
from rest_framework import generics
from rest_framework import permissions
from .models import Post
from .serializers import PostListSerializer, PostCreateSerializer, PostDetailSerializer
from .permissions import IsAuthor, IsAuthorOrAdmin

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = PostListSerializer

    def perform_create(self, serializer):
        print(self.request.user, 'user')
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostCreateSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context.update({"python": 'heelo world'})
    #     return context


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return PostCreateSerializer
        return PostDetailSerializer
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return IsAuthorOrAdmin(),
        elif self.request.method in ('PUT', 'PATCH'):
            return IsAuthor(),
        return permissions.AllowAny(),
