from django import forms
from accounts.models import User, UserProfile
from accounts.validators import allow_only_images_validator
from .models import PersonalLoan, TargetSaving

class CustomerForm(forms.ModelForm):
    country = forms.SelectMultiple(),
    # we are using validator to validate the file upload
    photo = forms.FileField(widget=forms.FileInput(
        attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])

    class Meta:
        model = UserProfile
        fields = ['country', 'photo', 'phone_number']
    
     # To make the form show the given style of our template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# FORMS FOR ALL NOBLESERVE PRODUCTS
# Personal Loans
class PersonalLoanForm(forms.ModelForm):

    class Meta:
        model = PersonalLoan
        fields = ['sex', 'dob', 'address', 'occupation',
                  'purpose_of_loan', 'amount', 'duration']
         # To make the form show the given style of our template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
       


class PerformApprovalLoanForm(forms.ModelForm):

    class Meta:
        model = PersonalLoan
        fields = [ 'status']
         # To make the form show the given style of our template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


# Target Savings-- for DOB make sure you install the DateOfBirthWidget()module
class TargetSavingsForm(forms.ModelForm):
    class Meta:
        model = TargetSaving
        fields = ['amount', 'start_save', 'save_by']
         # To make the form show the given style of our template
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    
