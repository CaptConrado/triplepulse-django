from django import forms
from django.contrib.auth.models import User
from ecommerce.models import UserProfile

class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "Full name"

    def save(self, commit=True):

        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password',)

        widgets = {
            'password': forms.PasswordInput(),
            }

class ShippingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'stripe_id')

class BillingForm(forms.Form):
    name = forms.CharField(label="Full name")
    card = forms.CharField(label='Card number')
    cvc = forms.CharField(max_length=4, label='CVC code')
    exp_month = forms.CharField(max_length=2, label='Expiration Month', widget=forms.TextInput(attrs={'placeholder': 'MM'}))
    exp_year = forms.CharField(max_length=4, label='Expiration Year', widget=forms.TextInput(attrs={'placeholder': 'YYYY'}))
    zip = forms.CharField(label='ZIP Code')
