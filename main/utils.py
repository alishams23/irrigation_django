from .models import WaterWell,SortedMembers,Group

def calculate_order_members(water_well:WaterWell , round :int) -> list[SortedMembers]:
    group : list[Group]= water_well.groups.all().order_by("sort")
    list_members = []
    for time in range(round):
        
        
        for item  in group:
            is_reversed = item.is_reversed if time % 2 == 0 else not item.is_reversed 
            if item.is_reverse == True : 
                item_member = item.members.all().order_by("sort") if is_reversed == True else item.members.all().order_by("-sort")
            else :
                item_member = item.members.all().order_by("sort")
            list_members.extend([item for item in item_member])
        
    
    return list_members
    
    
    # return SortedMembersSerializer(list_members[list_members.index(current_member):][1]).data
    