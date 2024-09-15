from django.contrib import admin

# Register your models here.

from django.contrib import admin

from main.forms import GroupAdminForm
from .models import SortedMembers, Group, WaterWell,APKRelease


@admin.register(SortedMembers)
class SortedMembersAdmin(admin.ModelAdmin):
    list_display = ('member',"id", 'sort', 'time')
    search_fields = ('member__username',)  # Assuming User model has a username field
    list_filter = ('sort', 'time')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    list_display = ("id",'name', 'is_reverse')
    search_fields = ('name',)
    filter_horizontal = ('members',)  # For ManyToManyField with SortedMembers

@admin.register(WaterWell)
class WaterWellAdmin(admin.ModelAdmin):
    list_display = ("id",'address', 'is_on', 'admin')
    search_fields = ('address', 'admin__username')  # Assuming User model has a username field
    filter_horizontal = ('groups',)  # For ManyToManyField with Group
    


@admin.register(APKRelease)
class APKReleaseAdmin(admin.ModelAdmin):
    list_display = ('version', 'upload_date', 'is_active')
    list_filter = ('is_active', 'upload_date')
    search_fields = ('version', 'description')
