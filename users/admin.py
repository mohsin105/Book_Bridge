from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Notification

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name','last_name', 'is_active')
    list_filter=('is_staff', 'is_active')

    fieldsets = (
        (None, {'fields':('email', 'password')}),
        ('Personal Info',{'fields':('first_name','last_name', 'bio','address', 'phone_number','profile_image')}),
        ('Permissions', {'fields':('is_staff', 'is_active','is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates',{'fields':('last_login', 'date_joined')})
    )
    # added from chatgpt, to enable user creation from admin panel. when userserializer not used yet
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering= ('email',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(Notification)
