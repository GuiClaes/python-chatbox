from django import forms

class MessageCreationForm(forms.Form):
    author = forms.CharField(required=True, max_length=200, widget=forms.TextInput(attrs={'class':'short'}))
    content = forms.CharField(required=True, max_length=200)
    
    #Hardcoding attribute name is not very Cool...
    def get_content(self):
        return self.data.get('content') 

    def get_author(self):
        return self.data.get('author')