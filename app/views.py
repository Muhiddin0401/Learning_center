from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt  # CSRF himoyasini o'chirish uchun

from .serializers import *
from .utils import generate_otp
from app.models import *

# OTP yaratish
# @csrf_exempt
class OTPSendView(APIView):
    def post(self, request):
        serializer = OTPSendSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({"error": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)

            OTPCode.objects.filter(user=user).delete()

            otp_code = generate_otp()
            otp = OTPCode.objects.create(user=user, code=otp_code)

            print(f"OTP code: {otp_code} for {phone_number}")

            return Response({"message": "OTP code sent"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
class OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            code = serializer.validated_data["code"]

            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({"error": "Foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)

            try:
                otp = OTPCode.objects.get(user=user, code=code)
            except OTPCode.DoesNotExist:
                return Response({"error": "Noto'g'ri OTP kod"}, status=status.HTTP_400_BAD_REQUEST)

            if not otp.is_valid():
                return Response({"error": "OTP kod muddati o'tgan"}, status=status.HTTP_400_BAD_REQUEST)

            otp.delete()

            return Response({"message": "OTP kod tasdiqlandi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
