from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model  = Comment
        fields = ['id', 'content', 'author_name', 'created_at']


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    comments    = CommentSerializer(many=True, read_only=True)

    class Meta:
        model  = Post
        fields = ['id', 'title', 'content', 'author_name', 'comments', 'created_at', 'updated_at']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = ['id', 'title', 'content']