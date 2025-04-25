from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('phone_number', 'address', 'is_verified')

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone_number', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'userprofile__phone_number')

    def get_phone_number(self, obj):
        return obj.userprofile.phone_number if hasattr(obj, 'userprofile') else '-'
    get_phone_number.short_description = 'Phone Number'

    def is_verified(self, obj):
        return obj.userprofile.is_verified if hasattr(obj, 'userprofile') else False
    is_verified.boolean = True
    is_verified.short_description = 'Verified'

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin) 