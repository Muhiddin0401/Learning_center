from rest_framework.viewsets import GenericViewSet  # OTP uchun GenericViewSet moduli
import random  # Tasodifiy OTP kodi generatsiyasi uchun

from .user_views import *

# OTP uchun maxsus class
class OTPViewSet(GenericViewSet):
    queryset = OTPCode.objects.all()
    serializer_class = OTPSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    @swagger_auto_schema(
        operation_description="Talaba uchun OTP so‘rash",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "old_password":openapi.Schema(type=openapi.TYPE_STRING, description="Eski parol")
            },
        )
    )
    def request_otp(self, request):
        user = request.user
        old_password = request.data.get('old_password')

        if not user.check_password(old_password):
            return Response({"error": "Password xato!!!"}, status=400)

        # Eski OTP kodlarini o‘chirish (ixtiyoriy)
        OTPCode.objects.filter(user=user).delete()

        # Yangi OTP kodi generatsiyasi
        code = str(random.randint(100000, 999999))
        otp = OTPCode.objects.create(user=user, code=code)

        # Test uchun konsolga chiqarish
        print(f"OTP kodi talaba uchun: {code}")
        return Response({"message": "OTP yuborildi."}, status=200)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    @swagger_auto_schema(
        operation_description="Talaba uchun parolni OTP yordamida o‘zgartirish",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'code': openapi.Schema(type=openapi.TYPE_STRING, description='OTP kodi'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='Yangi parol')
            },
            required=['code', 'new_password']
        )
    )
    def reset_password(self, request):
        user = request.user

        code = request.data.get('code')
        new_password = request.data.get('new_password')

        # So‘rov validatsiyasi
        if not code or not new_password:
            return Response({"error": "OTP kodi va yangi parol kiritilishi shart."}, status=400)

        try:
            otp = OTPCode.objects.get(user=user, code=code)
            if not otp.is_valid():
                return Response({"error": "Noto‘g‘ri yoki muddati o‘tgan OTP."}, status=400)
        except OTPCode.DoesNotExist:
            return Response({"error": "Noto‘g‘ri OTP."}, status=400)

        # Parolni o‘zgartirish
        user.set_password(new_password)
        user.save()

        # OTP kodini o‘chirish
        otp.delete()

        return Response({"message": "Parol muvaffaqiyatli o‘zgartirildi."}, status=200)