from django import forms
from .models import Comments, Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name','email','massage']
        
        
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body']