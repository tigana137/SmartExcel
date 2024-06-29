"""
URL configuration for SmartExcel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include ,path


from schema_graph.views import Schema

from django.contrib.auth.models import User # for the OTP token
from django_otp.admin import OTPAdminSite # for the OTP token
from django_otp.plugins.otp_totp.models import TOTPDevice # for the OTP token
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

from users.models import UserProfile, UserProfileForm # for the OTP token

class OTPAdmin(OTPAdminSite):
   pass


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     form = UserProfileForm
#     list_display = ('user', 'dre', 'is_admin',)  # Update is_active to is_admin
#     search_fields = ('user__username', 'dre__name')
#     list_filter = ('dre', 'is_admin')

#     def get_readonly_fields(self, request, obj=None):
        
#         if obj:
#             return ['user']
#         return []
    


admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)
# admin_site.register(UserProfile,UserProfileAdmin)



urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/x/', include('x.urls')),
    path('api/users/', include('users.urls')),
    path('api/excel/', include('excel.urls')),
    path('api/excelpremiere/', include('excelpremiere.urls')),
    path('api/retrieve/', include('retrieve.urls')),
    path('api/formulaire/', include('formulaire.urls')),
    path('api/Tunis/', include('Tunis.urls')),



    path("schema/", Schema.as_view()),
]

