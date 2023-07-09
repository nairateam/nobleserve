from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CustomerUserAdminProfile(admin.ModelAdmin):
    #to avoid the error of the image field i.e The 'photo' attribute has no file associated with it. we passed it into a try/catch 
    def thumbnail(self, object):
        try:
            return format_html('<img src="{}" width="40" style="border-radius: 50px;" />'.format(object.photo.url))
        except:
            pass #just ingnore
    
    thumbnail.short_description = 'Customer Photo'
    list_display = ('id', 'thumbnail','user','phone_number', 'country','created_at')
    list_display_links = ('id','user',)
    readonly_fields = ('created_at', 'modified_at')
    ordering = ('-created_at',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, CustomerUserAdminProfile)
