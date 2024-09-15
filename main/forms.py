from django import forms
from django.core.exceptions import ValidationError

from main.models import Group

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def clean_members(self):
        members = self.cleaned_data.get('members')
        for member in members:
            if Group.objects.filter(members=member).exclude(pk=self.instance.pk).exists():
                raise ValidationError(f"Member {member.member.username} is already part of another group.")
        return members