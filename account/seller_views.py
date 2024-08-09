from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response

from account.permissions import HasSellerPermission
from .serializers import UsernameShopCheckSerializer ,QueueVerifyShopSerializer,TermsSerializer,ZarinPalSerializer
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


        



class CodeCheckAdmin(views.APIView):
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
            
            return Response({'token':str(token[0]),'username_shop':user.shop.username if user.shop else None,'username':user.username,'status':user.status},status=status.HTTP_200_OK)
        else:   
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

      
      

class ChangeUsernameShopView(views.APIView):
    permission_classes = [HasSellerPermission, ]

    def put(self, request, *args, **kwargs):
        shop = self.request.user.shop
        new_username = self.request.data.get('username')
        if new_username:
            serializer = UsernameShopCheckSerializer(data={'username': new_username})

            if serializer.is_valid():
                shop.username = new_username
                shop.save()
                return Response({'message': 'Username updated successfully'})
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'New username not provided'}, status=status.HTTP_400_BAD_REQUEST)
        



class VerifyShopCreateAdminApi(generics.ListCreateAPIView):
    queryset = QueueVerifyShop.objects.all()
    serializer_class = QueueVerifyShopSerializer
    
    def perform_create(self, serializer):
        data= serializer.save(author=self.request.user,)



class VerifyShopListAdminApi(generics.ListCreateAPIView):
    queryset = QueueVerifyShop.objects.all()
    serializer_class = QueueVerifyShopSerializer
    
    def get_queryset(self):
        return QueueVerifyShop.objects.filter(author = self.request.user)




class VerifyShopRetrieveUpdateApi(generics.RetrieveUpdateAPIView):
    serializer_class = QueueVerifyShopSerializer

    def get_queryset(self):
        return QueueVerifyShop.objects.filter(author=self.request.user)


class TermsListApi(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = TermsSerializer
    queryset = Terms.objects.all()
    permission_classes = (AllowAny, )




class ZarinPalMerchantUpdateApi(generics.UpdateAPIView):
    serializer_class = ZarinPalSerializer

    def get_queryset(self):
        return  ZarinPal.objects.filter(id=self.request.user.shop.zarin_pal.id)


class ZarinPalMerchantListApi(generics.ListAPIView):
    serializer_class = ZarinPalSerializer

    def get_queryset(self):
        return  ZarinPal.objects.filter(id=self.request.user.shop.zarin_pal.id)



