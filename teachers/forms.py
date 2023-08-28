from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form_input_1",
        'placeholder': " ",
    })
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form_input_1",
        'type': "password",
        'placeholder': " ",
    })
    )