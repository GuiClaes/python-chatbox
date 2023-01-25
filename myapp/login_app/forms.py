from django import forms
from django.core.exceptions import ValidationError

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'id':'floatingInput', 'class':'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'floatingPassword', 'class':'form-control'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'floatingPassword', 'class':'form-control'}))
    email = forms.CharField(required=True, max_length=200, widget=forms.TextInput(attrs={'id':'floatingInput', 'class':'form-control'}))
    
    def is_valid(self) -> bool:
        return super().is_valid() and self.get_password() == self.get_confirm_password()

    #Hardcoding attribute name is not very Cool...
    def get_username(self):
        return self.data.get('username')

    def get_password(self):
        return self.data.get('password')

    def get_confirm_password(self):
        return self.data.get('confirm_password')

    def get_email(self):
        return self.data.get('email')

    def get_username_if_unique(self, exists):
        if exists:
            raise ValidationError("Username already exists")
        return self.data.get('username')


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'id':'floatingInput', 'class':'form-control'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'floatingPassword', 'class':'form-control'}))
    #Hardcoding attribute name is not very Cool...
    def get_username(self):
        return self.data.get('username')

    def get_password(self):
        return self.data.get('password')