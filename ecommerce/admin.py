from django.contrib import admin
from ecommerce.models import Shipment, UserProfile
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.models import User

class UserProfileInline(admin.TabularInline):
    model = UserProfile

class ShipmentAdmin(admin.ModelAdmin):
    list_filter = ('shipped',)
    list_display = ('date', 'type', 'name', 'street1', 'street2', 'city', 'state', 'zip', 'shipped', 'tracking_code')
    list_editable = ('shipped', 'tracking_code')
    ordering = ('shipped', 'date',)


admin.site.register(Shipment, ShipmentAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False

class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)