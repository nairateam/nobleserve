from django.contrib import admin
from .models import PersonalLoan, TargetSaving
from django.utils.html import format_html
# Register your models here.


class CustomPersonalloan(admin.ModelAdmin):
    list_display = ( 'transaction_id', 'created_by','sex', 'dob', 'amount','status','created_at' )
    ordering = ('-created_at',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class CustomTargetSavings(admin.ModelAdmin):
    list_display = ('fullname' ,'user', 'start_save', 'save_by','status','created_at' )
    ordering = ('-created_at',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(PersonalLoan, CustomPersonalloan)
admin.site.register(TargetSaving, CustomTargetSavings)
