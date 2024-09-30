from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Post, UserResponse
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostForm(ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = ['title', 'text', 'category', 'author']

        def clean(self):
            clean_data = super().clean()
            title = clean_data.get('title')
            if title is not None and len(title) < 20:
                raise ValidationError({
                'title': 'Заголовок не может быть менее 20 символов.'
                })
            text = clean_data.get('text')
            if text is not None and len(text) < 20:
                raise ValidationError({
                'text': 'Текст не может быть менее 20 символов.'
                })
            return clean_data

class ResponsesForm(ModelForm):

    class Meta:
        model = UserResponse
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type comment text here ...'}),
        }


class EditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }