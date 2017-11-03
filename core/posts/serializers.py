from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError
from .models import Post, Tag, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag


'''
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
'''


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    # comments= CommentSerializer(many=True,read_only=True)
    class Meta:
        model = Post

    def create(self, validated_data):  # registration or user creation
        post = Post.objects.create(
            title=validated_data['title'],
            text=validated_data['text'],
        )

        post.save()
        return post


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

    def create(self, validated_data):
        tag = Tag.objects.create(
            name=validated_data['name'],
        )

        tag.save()
        return tag


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)

    class Meta:
        model = Post

    def save(self, **kwargs):
        return super(PostCreateSerializer, self).save(**kwargs)


'''
     
class CommentCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField(required=True, write_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
   '''
