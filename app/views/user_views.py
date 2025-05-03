from rest_framework.viewsets import ModelViewSet  # CRUD uchun DRF ning ModelViewSet moduli
from rest_framework.decorators import action, permission_classes  # Maxsus endpointlar (actions) yaratish uchun dekorator
from rest_framework.response import Response  # API javoblarini qaytarish uchun Response klassi
from rest_framework.permissions import IsAuthenticated
from app.models import *  # CRUD qilinadigan modellar
from app.serializers import *  # Serializers
from drf_yasg.utils import swagger_auto_schema  # swagger dokumentatsiyasi uchun dekorator
from drf_yasg import openapi  # swagger uchun openapi moduli
# Autintifiaktisiya va ruxsatlar uchun kerakli kuitibxonalar
from app.permissions import (IsAdminOrStaff, IsTeacher, IsStudent, IsTeacherOfGroup)  # Maxsus ruxsat sinflarifrom rest_framework.permissions import IsAuthenticated  # Autentifikatsiyadan o‘tgan foydalanuvchilar uchun ruxsat

class UserViewSet(ModelViewSet):  # User uchun CRUD operatsiyasi sinfi
    queryset = User.objects.all()  # barcha foydalanuvhilarni olish
    serializer_class = UserSerializer  # User uchun Userserializerni ishlatish
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    @swagger_auto_schema(operation_description="Foydalanuvchilar ro'ysatini olish")  # Get so'rovi uxhun swagger izohi
    def list(self, request, *args, **kwargs):  # Fotdalanuvchilar ro'yxatini olish
        return super().list(request, *args, **kwargs)  # ModelViewSetni standart list metodi

    @swagger_auto_schema(operation_description="Yangi Foydalanuvchi qo'shish")  # POST so'rovi
    def create(self, request, *args, **kwargs):  # POST funksiyasi
        return super().create(request, *args, **kwargs)  # ModelViewSetni standart create metodi

    @swagger_auto_schema(operation_description="Foydalanuvchini yangilash")  # PUT/PATCH so'rovi
    def update(self, request, *args, **kwargs):  # Foydalanuvchini yangilash (PUT/PATCH)
        return super().update(request, *args, **kwargs)  # ModelViewSet ning standart update metodini chaqirish

    @swagger_auto_schema(operation_description="Foydalanuvchini o'chirish")  # DELETE so'rovi
    def destroy(self, request, *args, **kwargs):  # Foydalanuvchini o'chirish (DELETE)
        return super().destroy(request, *args, **kwargs)  # ModelViewSet ning standart destroy metodini chaqirish

