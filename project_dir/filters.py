from django_filters import FilterSet
from .models import Post, UserResponse


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
        }

class ResponseFilter(FilterSet):
    class Meta:
        model = UserResponse
        fields = {
            'author': ['exact'],
            'text': ['icontains'],
        }
