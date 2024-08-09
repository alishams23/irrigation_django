from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import SortedMembers, Group, WaterWell

@admin.register(SortedMembers)
class SortedMembersAdmin(admin.ModelAdmin):
    list_display = ('member', 'sort', 'time')
    search_fields = ('member__username',)  # Assuming User model has a username field
    list_filter = ('sort', 'time')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_reverse')
    search_fields = ('name',)
    filter_horizontal = ('members',)  # For ManyToManyField with SortedMembers

@admin.register(WaterWell)
class WaterWellAdmin(admin.ModelAdmin):
    list_display = ('address', 'is_on', 'admin')
    search_fields = ('address', 'admin__username')  # Assuming User model has a username field
    filter_horizontal = ('groups',)  # For ManyToManyField with Group