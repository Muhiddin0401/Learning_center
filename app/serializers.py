from rest_framework import serializers
from app.models import *

# OTP kodini yuborish
class OTPSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)

# kiritilgan OTP kodini tekshirish
class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)
    code = serializers.CharField(max_length=6)