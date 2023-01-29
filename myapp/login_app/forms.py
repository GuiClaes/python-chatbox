from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'id':'floatingInput', 'class':'form-control', 'autoComplete':'off'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'floatingPassword', 'class':'form-control'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'floatingPassword', 'class':'form-control'}))
    email = forms.CharField(required=True, max_length=200, widget=forms.TextInput(attrs={'id':'floatingInput', 'class':'form-control', 'autoComplete':'off'}))
    
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

class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'id':'floatingInput', 'class':'form-control', 'autoComplete':'off'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'floatingPassword', 'class':'form-control'}))
    #Hardcoding attribute name is not very Cool...
    def get_username(self):
        return self.data.get('username')

    def get_password(self):
        return self.data.get('password')