from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status ,generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from extensions import jalali
from extensions.utils import jalali_converter
from main.tasks import check_time_field
from main.utils import calculate_order_members
from .models import SortedMembers, WaterWell ,Group
from .serializers import SortedMembersSerializer, WaterWellSerializer ,GroupSerializer,GroupSortUpdateSerializer
from django.db.models import Q


class TurnOnWaterWell(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ):
        try:
            water_well = WaterWell.objects.get(admin=request.user)
        except WaterWell.DoesNotExist:
            return Response({'error': 'WaterWell not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
        water_well.start_member = water_well.start_member + (timezone.now() - water_well.off_time )
        water_well.is_on = True
        water_well.save()
        check_time_field()
        return Response( status=status.HTTP_200_OK)
    
    
class TurnOffWaterWell(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ):
        try:
            water_well = WaterWell.objects.get(admin=request.user)
        except WaterWell.DoesNotExist:
            return Response({'error': 'WaterWell not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)

        water_well.is_on = False
        water_well.off_time = timezone.now()
        water_well.save()
        return Response( status=status.HTTP_200_OK)

    
class WaterWellStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ):
        try:
            water_well = WaterWell.objects.filter(Q(admin=request.user) | Q(groups__members = SortedMembers.objects.get(member = request.user))).first()
        except WaterWell.DoesNotExist:
            return Response({'error': 'WaterWell not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WaterWellSerializer(water_well,context={
        'request': request
    })
        return Response(serializer.data, status=status.HTTP_200_OK)


    
class SortedMembersList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ):
        try:
            water_well = WaterWell.objects.filter(Q(admin=request.user)|  Q(groups__members = SortedMembers.objects.get(member = request.user))).first()
        except WaterWell.DoesNotExist:
            return Response({'error': 'WaterWell not found or not authorized'}, status=status.HTTP_404_NOT_FOUND)
        data :list[SortedMembers] = calculate_order_members(water_well,30)
        data = data[data.index( water_well.current_member):] 
        serializer = SortedMembersSerializer(data,many=True,context={
        'request': request
        })
        # Access the serialized data
        serialized_data = serializer.data
        if water_well.is_on == False:
            current_time = water_well.off_time
        else :
            current_time = timezone.now()

       
        left_time = water_well.current_member.time - ((current_time - water_well.start_member).total_seconds() / 60)
        # Add the key and value to each item in the serialized data list
        for index, item in enumerate(serialized_data):
            if index == 0 :
                time = timezone.localtime(water_well.start_member )    
            else : 
                if index > 1 :
                    left_time = left_time + serialized_data[index-1]["time"]
                time = timezone.localtime(current_time +  timedelta(minutes=left_time ) )
            
            time_to_str = "{},{},{}".format(time.year, time.month, time.day)
            # Convert Gregorian date to Jalali date
            time_to_tuple = list(jalali.Gregorian(time_to_str).persian_tuple())
            
            item["day"] = time_to_tuple[2]
            item["month"] = time_to_tuple[1]
            item["year"] = time_to_tuple[0]
            item["hour"] =  time.hour
            item["minute"] =time.minute
            item["is_on"] =water_well.is_on

            
            
        return Response(serialized_data , status=status.HTTP_200_OK)


class GroupListAPIView(generics.ListAPIView):
    serializer_class = GroupSerializer
    def get_queryset(self):
        
        return Group.objects.filter(waterwell__admin=self.request.user)
    
    
class GroupSortUpdateView(APIView):
    def put(self, request):
        # Expecting a list of dicts with 'id' and 'sort'
        group_data = request.data

        if not isinstance(group_data, list):
            return Response({"error": "Expected a list of dictionaries."}, status=status.HTTP_400_BAD_REQUEST)

        for item in group_data:
            serializer = GroupSortUpdateSerializer(data=item)
            if serializer.is_valid():
                try:
                    group = Group.objects.get(id=item['id'],waterwell__admin=self.request.user)
                    group.sort = item['sort']
                    group.save()
                except Group.DoesNotExist:
                    return Response({"error": f"Group with id {item['id']} does not exist."},
                                    status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "sort fields updated successfully"}, status=status.HTTP_200_OK)