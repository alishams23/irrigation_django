from django.db.models import Count
from django.core.management.base import BaseCommand

from main.models import Group, SortedMembers

class Command(BaseCommand):
    help = 'Load subtitles from server django'

    def handle(self, *args, **kwargs):

        # Find all SortedMembers that belong to two or more groups
        sorted_members_in_multiple_groups = SortedMembers.objects.annotate(group_count=Count('group')).filter(group_count__gt=1)

        # Print results
        for member in sorted_members_in_multiple_groups:
            self.stdout.write(f"Member {member.id} is in {member.group_count} groups.")
            for item in Group.objects.filter(member = member):
                self.stdout.write(f"{item.id} -- {item.name}")


        # self.stdout.write(f"{data}")
