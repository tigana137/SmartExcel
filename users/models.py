from django.db import models
from x.models import Dre


from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, full_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, full_name, password, **other_fields)

    def create_user(self, email, username, full_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,full_name=full_name, **other_fields)
        user.set_password(password)
        user.save()
        return user



class UserProfile(AbstractBaseUser,PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    dre = models.ForeignKey(Dre, on_delete=models.PROTECT, blank=True, null=True)
    isAdmin = models.BooleanField(default=False) 
    

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name','email']

    def __str__(self):
        return self.username


# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)
    
# def save_user_profile(sender, instance, **kwargs):
#         instance.userprofile.save()

# post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)





# class UserProfileForm(forms.ModelForm):
#     username = forms.CharField(max_length=150)
#     password = forms.CharField(widget=forms.PasswordInput)
#     full_name = forms.CharField(max_length=30, required=False)
#     last_name = forms.CharField(max_length=150, required=False)
#     email = forms.EmailField(required=False)
#     is_admin = forms.BooleanField(initial=False, required=False)  # Add is_admin field

#     class Meta:
#         model = UserProfile
#         fields = ['dre', 'is_admin']  # Update to include is_admin instead of is_active
 
#     def save(self, commit=True):
#         user = None
#         if not self.instance.pk:
#             # Creating a new User
#             user = User.objects.create_user(
#                 username=self.cleaned_data['username'],
#                 password=self.cleaned_data['password'],
#                 full_name=self.cleaned_data.get('full_name'),
#                 last_name=self.cleaned_data.get('last_name'),
#                 email=self.cleaned_data.get('email')
#             )
#             self.instance.user = user
#             self.instance.is_admin = self.cleaned_data.get('is_admin')
#         return super().save(commit=commit)