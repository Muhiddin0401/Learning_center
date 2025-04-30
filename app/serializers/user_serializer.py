from django.db import IntegrityError # Phone_numberni tekshirish kerak
from rest_framework import serializers  # DRF serializerlarini yaratish uchun modul
from app.models import *  # Serializer uchun kerak bo'lgan modullar


class UserSerializer(serializers.ModelSerializer):  # User modeli uchun Serializer
    class Meta:  # Meta ma'lumotlar uchun Meta class
        model = User  # serializer qaysi model bilan ishlashi
        # Serializatsiya qilinadigan maydonlar:
        fields = ['id', 'password', 'username', 'phone_number', 'email', 'is_admin', 'is_staff', 'is_teacher', 'is_student']
        extra_kwargs = {
            'phone_number': {'required': False},  # Telefon majburiy emas
            'email': {'required': False}, # Email majburiy emas
            'password': {'write_only': True}}  # parol faqat yozish uchun o'qishda ko'rinmaydi

    def create(self, validated_data):  # Yangi foydalanuvchi yaratish uchun maxsus funksiya
        try:
            user = User.objects.create_user(**validated_data)  # CustomUserManage orqali foydalanuvchi yaratish
        except IntegrityError as e : # Agar UNIQUE cheklovi bo'lsa(phone_number)
            if "UNIQUE constraint failed" in str(e): # Xatto UNIQUE bilan bo'g'liq bo'lsa
                raise serializers.ValidationError({
                    "phone_number": "Bu telefon raqami allaqachon mavjud"
                })
            raise e # Boshqacha error bo'lsa xatoni o'zini qaytarish
        return user  # yaratilgan foydalanuvchini qaytarish

    def update(self, instance, validated_data):  # foydalanuvchini update qilish uchun maxsus funksiya
        instance.username = validated_data.get('username', instance.username)  # usernameni yangilash
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)  # telefon raqamni yangilash
        instance.email = validated_data.get('email', instance.email)  # emailni yangilash
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)  # adminlik ruxsatini yangilash
        instance.is_teacher = validated_data.get('is_teacher', instance.is_teacher)  # teacherlik ruxsatini yangilash
        instance.is_student = validated_data.get('is_student', instance.is_student)  # studentlikni yangilash
        instance.is_staff = validated_data.get('is_staff', instance.is_staff) # staffni yangilash
        if 'password' in validated_data:  # Agar parol berilgan bo'lsa
            instance.set_password(validated_data['password'])  # parolni shifrlab yangilash
        instance.save()  # o'zgarisharni saqlash
        return instance  # yangilangan foydalanuvchini qaytarish

# OTPCode modeli uchun serializer
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPCode  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'user', 'code', 'created', 'expires_at'] # Seriyalizatsiya qilinadigan maydonlar