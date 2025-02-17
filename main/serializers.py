from rest_framework import serializers

from account.models import User
from main.utils import calculate_order_members
from .models import SortedMembers, WaterWell,Group




class UserLessInformationSerializers(serializers.ModelSerializer):
    def getFullName(self, obj):
        return f"{obj.first_name + ' ' + obj.last_name}"
    full_name = serializers.SerializerMethodField("getFullName")

    class Meta:
        model = User
        fields = ["username", "id", "full_name",]
        
        

class SortedMembersSerializer(serializers.ModelSerializer):
    member = UserLessInformationSerializers()
    class Meta:
        model = SortedMembers
        fields = "__all__"

        
class GroupSerializer(serializers.ModelSerializer):
    members = SortedMembersSerializer(many=True)
    class Meta:
        model = Group
        fields = "__all__"

class GroupSortUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'sort']
        

class MembersSortUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortedMembers
        fields = ['id', 'sort']
        
class MembersTimeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SortedMembers
        fields = ['id', 'time']
        
class CurrentMemberWaterWellUpdateSerializer(serializers.Serializer):
    start_member = serializers.IntegerField()
    current_member = serializers.CharField()

class WaterWellSerializer(serializers.ModelSerializer):
    def next_member_calculate (self , obj:WaterWell):
        # group : list[Group]= obj.groups.all().order_by("sort")
        # list_members = []
        # for item  in group:
        #     item_member = item.members.all().order_by("sort") if item.is_reversed == True else item.members.all().order_by("-sort")
        #     list_members.extend([item for item in item_member])
        # current_member = obj.current_member
        # print(list_members)
        data = calculate_order_members(obj,2)
        return SortedMembersSerializer(data[data.index(obj.current_member):][1]).data
    
    def self_user_get (self , obj:WaterWell):
        user : User = self.context.get("request").user
        if user != None:
            return {"full_name" : user.get_full_name(),"phone_number": user.phone_number}
        return None
    
    def is_admin_check(self,obj):
        return obj.admin == self.context.get('request', None).user
    next_member = serializers.SerializerMethodField("next_member_calculate")
    is_admin = serializers.SerializerMethodField("is_admin_check")
    self_user = serializers.SerializerMethodField("self_user_get")
    current_member = SortedMembersSerializer()
    previous_member = SortedMembersSerializer()
    class Meta:
        model = WaterWell
        fields = ['id',"address",  'is_on', 'is_admin','next_member',"current_member","previous_member","start_member","off_time","is_aqueduct","self_user"]