from rest_framework import serializers
from research.models import Paper
from research.models import Comment
from django.contrib.auth.models import User


class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = ['abstract',
                  'title',
                  'author',
                  'paper_url',
                  'published_date',
                  'subject',
                  'updated',
                  'pdf_url'
                  ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
