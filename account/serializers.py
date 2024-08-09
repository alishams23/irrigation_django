
from rest_framework import serializers
from .models import *
from django.core.exceptions import ValidationError
from django.conf import settings


class UsernameShopCheckSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,min_length =6 )
    def validate_username(self, validated_data):
        username = validated_data
        special_characters = "!@#$%^&*()-+?=,<>/"
        if any(c in special_characters for c in username):
            raise ValidationError("Username must don't have character")
        return username.lower()





class UsersRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", 'username', 'password', 'first_name', 'last_name',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_password(self, validated_data):
        if len(validated_data) < 8:
            raise ValidationError("password need to be more than 8 character")
        return validated_data

    def validate_username(self, validated_data):
        username = validated_data
        special_characters = "!@#$%^&*()-+?=,<>/"
        if any(c in special_characters for c in username):
            raise ValidationError("Username must don't have character")
        return username.lower()


class UserLessInformationSerializers(serializers.ModelSerializer):
    def getFullName(self, obj):
        return f"{obj.first_name + ' ' + obj.last_name}"
    full_name = serializers.SerializerMethodField("getFullName")

    class Meta:
        model = User
        fields = ["username", "id", "full_name",]


class UserSettingSerializers(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = [ "first_name",
                  "last_name",
                  "state",
                  "city",
                    "email",
                  "street",
                  "zipCode",
                  ]


class UserSettingRetrieveSerializers(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = [ "first_name",
                  "last_name",
                  "state",
                  "email",
                  "city",
                  "phone_number",
                  "street",
                  "zipCode",
                  ]
        

class NotificationSerializers(serializers.ModelSerializer):
    receiver = UserLessInformationSerializers()
    user = UserLessInformationSerializers()

    class Meta:
        model = Notification
        fields = "__all__"





class UserWithPhoneNumberSerializers(serializers.ModelSerializer):
    def getFullName(self, obj):
        return f"{obj.first_name + ' ' + obj.last_name}"
    full_name = serializers.SerializerMethodField("getFullName")

    class Meta:
        model = User
        fields = ["username", "id", "full_name","phone_number"]


class QueueVerifyShopSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField(read_only=True)
    class Meta:
        model = QueueVerifyShop
        fields = "__all__"

class QueueVerifyShopSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField(read_only=True)
    class Meta:
        model = QueueVerifyShop
        fields = "__all__"
   

class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'
   

class ZarinPalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZarinPal
        fields = '__all__'
