from django import forms

class MessageCreationForm(forms.Form):
    author = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'author'}))
    content = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'content'}))

    def is_valid(self) -> bool:
        return super().is_valid() and self.get_content() != "" and self.get_author() != ""
    
    #Hardcoding attribute name is not very Cool...
    def get_content(self):
        return self.data.get('content') 

    def get_author(self):
        return self.data.get('author')