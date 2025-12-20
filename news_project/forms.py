from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','massage']
        
        
        
class CommentForm(forms.Form):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':4, 'placeholder':'Enter your comment here...'}))        