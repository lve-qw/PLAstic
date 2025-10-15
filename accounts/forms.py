# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "phone", "address"]

    def save(self, commit=True):
        user = super().save(commit)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user.profile.phone = self.cleaned_data["phone"]
            user.profile.address = self.cleaned_data["address"]
            user.profile.save()
        return user
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["phone", "address"]
