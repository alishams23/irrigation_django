from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from django_filters import rest_framework as filterSpecial  

from account.permissions import HasSellerPermission
from .serializers import UserSettingRetrieveSerializers, UsernameShopCheckSerializer ,NotificationSerializers,UserSettingSerializers
from .models import *
from rest_framework.permissions import AllowAny
from rest_framework import generics
from smsir.token import get_token
from smsir.sms import VerificationCode
import random
from rest_framework.authtoken.models import Token
from decouple import config
from rest_framework import filters
import random
import string
from datetime import timedelta
import os
from django.conf import settings
from django.http import HttpResponse
import http.client
import json

def generate_random_username():
    # Generate a random username of length 8
    random_username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return random_username

def is_username_taken(username):
    # Check if the username already exists in the database
    return User.objects.filter(username=username).exists()

def create_unique_username():
    while True:
        random_username = generate_random_username()
        if not is_username_taken(random_username):
            return random_username
        
# Create your views here.



def user_profile(request, username):

    try:
        image = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("Image not found", status=404)
   
    image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
    with open(image_path, "rb") as image_file:
        response = HttpResponse(image_file.read(), content_type="image/jpeg")
        return response


class LoginSms(views.APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        number = self.request.POST['number']
        try:
            user = User.objects.get(phone_number = number)
        except User.DoesNotExist:
            return Response({'status': 'error','error':'کاربری با این مشخصات وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)
        
        
        user.verify_phone_code = random.randint(10000, 99999) 
        user.last_login_time = timezone.now()
        user.save()
        # token = get_token(UserApiKey=config("UserApiKeySms"), SecretKey=config("SecretKeySms"))
        # VerificationCode(Code=user.verify_phone_code , MobileNumber=number, Token=token)
        conn = http.client.HTTPSConnection("api.sms.ir")

        payload = {
            "mobile":number,
            "templateId": 100000,
            "parameters": [
                {"name": "Code", "value": f"{user.verify_phone_code}" },
            ]
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
        user.count_sms += 1
        user.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
     

class CodeCheck(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        code = self.request.POST['code']
        number = self.request.POST['number']
        #get user
        try:
            user = User.objects.get(phone_number = number)
        except User.DoesNotExist:
            return Response({'status': 'error','error':'کاربری با این مشخصات وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)
        if str(user.verify_phone_code ) == str(code) and user.last_login_time + timedelta(minutes=6) >= timezone.now():
            user.verify_phone = True
            user.save()
            token = Token.objects.get_or_create(user=user)
            # send token
            return Response({'token':str(token[0]),'username':user.username,'status':user.status},status=status.HTTP_200_OK)
        else:   
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        


class SignUpSms(views.APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        number = self.request.POST['number']
        user = QueueSignUp.objects.get_or_create(phone_number = number)
        user = QueueSignUp.objects.get(phone_number = number)
        user.first_name = self.request.POST['first_name']
        user.last_name = self.request.POST['last_name']
        user.email = self.request.POST['email']
        user.last_sign_up_time = timezone.now()
        user.save()

        user.verify_phone_code = random.randint(10000, 99999) 
        user.save()
        token = get_token(UserApiKey=config("UserApiKeySms"), SecretKey=config("SecretKeySms"))
        VerificationCode(Code=user.verify_phone_code , MobileNumber=number, Token=token)
        user.count_sms += 1
        user.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)
     
class CodeCheckSignUp(views.APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        code = self.request.POST['code']
        number = self.request.POST['number']
        #get user
        try:
            queue_instance = QueueSignUp.objects.get(phone_number = number)
        except QueueSignUp.DoesNotExist:
            return Response({'status': 'error','error':'کاربری با این مشخصات وجود ندارد'}, status=status.HTTP_404_NOT_FOUND)
        if str(queue_instance.verify_phone_code ) == str(code) and queue_instance.last_sign_up_time + timedelta(minutes=2) >= timezone.now():
            try:
                user = User.objects.get(phone_number = number)
            except User.DoesNotExist:
                user = User.objects.create(phone_number=queue_instance.phone_number,username =create_unique_username() ,password = ''.join(random.choices(string.ascii_letters + string.digits, k=12)))
                user.first_name = queue_instance.first_name
                user.last_name = queue_instance.last_name
                user.email = queue_instance.email
                user.verify_phone_code = queue_instance.verify_phone_code
                user.verify_phone = True
                user.save()
            token = Token.objects.get_or_create(user=user)
            # send token
            return Response({'token':str(token[0]),'username':user.username,'status':user.status},status=status.HTTP_200_OK)
        else:   
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

      


class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializers
    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)
   



class UserSettingsRetrieve(generics.RetrieveAPIView):
    lookup_field = 'username'
    serializer_class = UserSettingRetrieveSerializers
    def get_queryset(self):
        return  User.objects.filter(username = self.request.user.username)
    


class UserSettingsUpdate(generics.UpdateAPIView):
    lookup_field = 'username'
    serializer_class = UserSettingSerializers
    def get_queryset(self):
        return User.objects.filter(username = self.request.user.username)


