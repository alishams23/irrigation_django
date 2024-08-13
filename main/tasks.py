from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from celery.utils.log import get_task_logger

from account.models import User
from extensions import jalali
from main.serializers import SortedMembersSerializer

from main.utils import calculate_order_members
from .models import Group, SortedMembers, WaterWell
import http.client
import json
from celery import shared_task
from decouple import config

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='sms_queue')
def sendSms(self,phone_number:int,template_id:int,parameters:list):
    conn = http.client.HTTPSConnection("api.sms.ir")

    payload = {
        "mobile":phone_number,
        "templateId": template_id,
        "parameters": 
            parameters   
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'text/plain',
        'x-api-key': config("Token")
    }
    payload_json = json.dumps(payload)
    conn.request("POST", "/v1/send/verify", payload_json, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
    
    
@shared_task(queue='default')
def check_time_field():
    list_water_wall = WaterWell.objects.all()
    for water_well in list_water_wall:
        if water_well.is_on == True:
        
            data :list[SortedMembers] = calculate_order_members(water_well,5)
            data = data[data.index(water_well.current_member):] 
            serializer = SortedMembersSerializer(data,many=True,)
            # Access the serialized data
            serialized_data = serializer.data

        
            current_time = timezone.now()
            left_time = water_well.current_member.time - ((current_time - water_well.start_member).total_seconds() / 60)
            
            print(left_time)
            if left_time <= 0  :
                
                #change reverse
                if Group.objects.get(members= data[0]) != Group.objects.get(members= data[1]):
                    current_group =  Group.objects.get(members= data[1])
                    current_group.is_reversed =  not current_group.is_reversed if current_group.is_reverse == True else current_group.is_reversed
                    current_group.save()
                    
                water_well.current_member  = data[1]
                water_well.start_member = timezone.now().replace(second=0, microsecond=0)
                water_well.save()
                
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
                item_day = time_to_tuple[2]
                item_month = time_to_tuple[1]
                item_year = time_to_tuple[0]
                item_hour =  time.hour
                item_minute =time.minute
                user :User = User.objects.get(username =item["member"]["username"])
                if round((time - current_time ).total_seconds() / 60)  == user.sms_schedules : 
                    sendSms.delay(phone_number=user.phone_number,template_id="617027",parameters=[{"name": "FIRST_NAME", "value":item["member"]["full_name"],},{"name": "TIME", "value":f"{item_hour}:{item_minute}",},{"name": "DATE", "value":f"{item_year}/{item_month}/{item_day}"}])
                    

        



