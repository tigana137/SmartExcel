from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from x.models import Dre



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields as needed for your UserProfile model
    dre = models.ForeignKey(
        Dre, on_delete=models.SET_NULL, blank=True, null=True)
    is_admin = models.BooleanField(default=False)  # New boolean field

    
    def __str__(self):
        return self.user.username
    


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)
    is_admin = forms.BooleanField(initial=False, required=False)  # Add is_admin field

    class Meta:
        model = UserProfile
        fields = ['dre', 'is_admin']  # Update to include is_admin instead of is_active
 
    def save(self, commit=True):
        user = None
        if not self.instance.pk:
            # Creating a new User
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email')
            )
            self.instance.user = user
            self.instance.is_admin = self.cleaned_data.get('is_admin')
        return super().save(commit=commit)