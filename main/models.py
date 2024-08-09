from django.db import models
from account.models import User
# Create your models here.


class SortedMembers(models.Model):
    member = models.ForeignKey(User,on_delete=models.PROTECT)
    sort = models.IntegerField(default=0)
    time = models.IntegerField(verbose_name="تایم به دقیقه")
    
    def __str__(self) -> str:
        return f"{self.member.username} --- {self.sort}"


class Group(models.Model):
    name = models.TextField(verbose_name="نام گروه")
    members = models.ManyToManyField(SortedMembers,verbose_name="اعضا",)
    is_reverse = models.BooleanField(default=False)
    is_reversed = models.BooleanField(default=False)
    sort = models.IntegerField(default=1)
    

class WaterWell(models.Model):
    address = models.TextField(verbose_name="آدرس",)
    groups = models.ManyToManyField(Group,verbose_name="گروه",)
    is_on = models.BooleanField(default=True,verbose_name="روشن")
    admin = models.ForeignKey(User,verbose_name="ادمین",on_delete=models.PROTECT)
    start_member = models.DateTimeField(verbose_name="تایم به دقیقه")
    off_time = models.DateTimeField(verbose_name="تایم به دقیقه")
    current_member = models.ForeignKey(SortedMembers,verbose_name="نوبت نفر",on_delete=models.PROTECT,related_name="+")
    
    def next_members(self):
        sorted_members = SortedMembers.objects.filter(
            group__in=self.groups.all()
        ).distinct()
        current_member = self.current_member
        current_member_sort = sorted_members.filter(member=current_member).first().sort
        
        members_less_than_current = sorted_members.filter(sort__lt=current_member_sort)
        return members_less_than_current
    
    
    def get_repeated_sorted_members(self):
        # Collect all SortedMembers from all groups related to this WaterWell
        sorted_members = SortedMembers.objects.filter(
            group__in=self.groups.all()
        ).distinct()

        # Find the current member
        current_member = self.current_member
        
        # Get the sort value of the current_member
        current_member_sort = sorted_members.filter(member=current_member).first().sort

        # Separate members into those with a sort value less than and greater than or equal to current_member
        members_less_than_current = sorted_members.filter(sort__lt=current_member_sort)
        members_greater_or_equal = sorted_members.filter(sort__gte=current_member_sort)
        
        # Prepare the list with the current_member at the start for the first iteration
        first_iteration_list = [member for member in members_greater_or_equal] + [member for member in members_less_than_current]
        
        # Subsequent iterations
        subsequent_iterations_list = [member for member in sorted_members]

        # Repeat the lists 10 times
        repeated_list = []
        for i in range(10):
            if i == 0:
                repeated_list.extend(first_iteration_list)
            else:
                repeated_list.extend(subsequent_iterations_list)

        return repeated_list