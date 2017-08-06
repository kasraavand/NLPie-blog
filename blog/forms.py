from django import forms
from .models import Post, Comment, Tag
import re


class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, widget=forms.TextInput())

    class Meta:
        model = Post
        fields = ('title', 'text',)
        # widgets = {'tags': forms.TextInput()}

    def save(self, author, commit=True):
        post_instance = super(PostForm, self).save(commit=commit)
        # for refusing of null constraint
        post_instance.author = author
        tags = self.cleaned_data.get('tags', None)
        if tags is not None:
            all_tag_names = re.findall(r'([\w-]+):(\d+)', tags)
            # for refusing of null constraint
            post_instance.tag_densities = all_tag_names
            for t_name, density in all_tag_names:
                try:
                    t_obj = Tag.objects.get(name=t_name)
                except Tag.DoesNotExist as exc:
                    t_obj = Tag(name=t_name)
                    t_obj.save()
                post_instance.save()
                post_instance.tags.add(t_obj)
        post_instance.save()
        return post_instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'email', 'text',)
