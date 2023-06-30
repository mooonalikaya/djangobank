from django.contrib import admin
from .models import UserProfile, Transaction
from django.utils.safestring import mark_safe

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'get_first_name',
        'get_last_name',
        'get_email',
        'balance',
        'iin',   
        'phone',
        'created_at',
        'get_image',
    ]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'phone', 
        'iin',
    ]
    list_filter = ['created_at']

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'
    
    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150px" />')
        return 'Not image'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 
                    'summa', 'created_at']
    search_fields = [
        'sender__user__first_name',
        'sender__user__last_name',
        'summa',
    ]
    list_filter = ['sender', 'recipient', 'created_at']