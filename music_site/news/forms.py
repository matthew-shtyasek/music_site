from django import forms

from news.models import Comment, News


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Comment
        fields = ('text',)


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = News
        fields = ('title',
                  'slug',
                  'body',
                  'image',
                  'published')
