from django import forms

class MessageCreationForm(forms.Form):
    content = forms.CharField(required=True, max_length=200, widget=forms.TextInput(attrs={'class':'write_msg', 'placeholder':"Send a message", 'autoComplete':'off'}))
    
    #Hardcoding attribute name is not very Cool...
    def get_content(self):
        return self.data.get('content')


class UserFinderForm(forms.Form):
    user = forms.CharField(required=False, max_length=200, widget=forms.TextInput(attrs={'class':'search-bar', 'placeholder':"Search", 'autoComplete':'off'}))
    
    #Hardcoding attribute name is not very Cool...
    def get_user(self):
        return self.data.get('user')