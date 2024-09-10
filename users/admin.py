from django.contrib import admin
from users.models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models

from x.models import AdminEcoledata


class UserAdminConfig(UserAdmin):
    model = UserProfile
    search_fields = ('username', 'full_name',)
    list_filter = ('isAdmin', 'dre')
    ordering = ('-start_date',)
    list_display = ('username', 'full_name', 'is_staff')


    fieldsets = (
        (None, {'fields': ('username', 'full_name', 'email', 'start_date')}),
        ('Permissions', {'fields': ('is_staff','isAdmin')}),
        ('DRE Info', {'fields': ('dre',)}),
    )

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ( 'username', 'full_name','email', 'isAdmin', 'dre' ,'password1', 'password2',  'is_staff')}
         ),
    )



admin.site.register(UserProfile, UserAdminConfig)




class AdminEcoledataAdminConfig(admin.ModelAdmin):
    model = AdminEcoledata
    list_display = ('sid', 'ministre_school_name', 'principal', 'dre', 'del1')
    search_fields = ('ministre_school_name', 'principal')
    ordering = ('sid',)

    list_filter = ('dre',)

admin.site.register(AdminEcoledata, AdminEcoledataAdminConfig) 
 