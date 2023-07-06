from django import forms
from accounts.models import User, UserProfile
from accounts.validators import allow_only_images_validator


class CustomerForm(forms.ModelForm):
    country = forms.SelectMultiple(),
    #we are using validator to validate the file upload
    photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    
    class Meta:
        model = UserProfile
        fields = ['country', 'photo', 'phone_number']

