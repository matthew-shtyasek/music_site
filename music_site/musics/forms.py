from django import forms

from profiles.models import Playlist


class PlaylistCreateForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('name',
                  'icon',
                  'public')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['icon'].widget.attrs['class'] = 'form-control-file'
        #self.fields['public'].widget.attrs['class'] = 'form-check-input'
