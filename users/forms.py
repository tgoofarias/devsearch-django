from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Full Name'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({
            'class': 'input input--text',
            'id': 'formInput#text',
            'type': 'text',
            'placeholder': 'e.g. Dennis Ivanov',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'input input--email',
            'id': 'formInput#email',
            'type': 'email',
            'placeholder': 'e.g. user@domain.com',
        })
        self.fields['username'].widget.attrs.update({
            'class': 'input input--text',
            'id': 'formInput#text',
            'type': 'text',
            'placeholder': 'e.g. dennis123',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input input--password',
            'id': 'formInput#password',
            'type': 'password',
            'placeholder': '••••••••',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input input--password',
            'id': 'formInput#confirm-password',
            'type': 'password',
            'placeholder': '••••••••',
        })

