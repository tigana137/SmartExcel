from django.contrib import admin

from x.models import AdminEcoledata

# Register your models here.



class AdminEcoledataAdminConfig(admin.ModelAdmin):
    model = AdminEcoledata
    list_display = ('sid', 'ministre_school_name', 'principal', 'dre', 'del1')
    search_fields = ('ministre_school_name', 'principal')
    list_filter = ('dre', )

admin.site.register(AdminEcoledata, AdminEcoledataAdminConfig) 
