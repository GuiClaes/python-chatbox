from django import forms

class MessageCreationForm(forms.Form):
    content = forms.CharField(label='Enter your message', max_length=200)

    def is_valid(self) -> bool:
        return super().is_valid() and self.get_content() != ""
    
    def get_content(self):
        return self.data.get('content') #Hardcoding attribute name is not very Cool...