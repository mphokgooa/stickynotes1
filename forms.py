from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title','content']

    def clean_title(self):
        title = self.cleaned_data.get('title','').strip()
        if not title:
            raise forms.ValidationError('Title cannot be empty')
        return title
