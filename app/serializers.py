from django.db import IntegrityError
from rest_framework import serializers  # DRF serializerlarini yaratish uchun modul
from app.models import *  # Serializer uchun kerak bo'lgan modullar


class UserSerializer(serializers.ModelSerializer):  # User modeli uchun Serializer
    # password = serializers.CharField(write_only=True, required=True)  # Password maydoni
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

class DepartmentSerializer(serializers.ModelSerializer):# Department uchun Serializers:
    class Meta:
        model = Departments # Serializer uchun model
        fields = ['id', 'title', 'is_active', 'descriptions'] #Serializatsiya qilinadigan maydonlar

class CourseSerializer(serializers.ModelSerializer): # Course uchun Serialzier
    class Meta:
        model = Course  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'title', 'descriptions']# Seriyalizatsiya qilinadigan maydonlar

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'departments', 'course', 'descriptions']

    def create(self, validated_data):  # yangi teacher yaratish uchun create funksiya
        user_data = validated_data.pop('user')  # user ma'lumotlarini ajratib olish
        departments = validated_data.pop('departments', [])
        courses = validated_data.pop('course', [])
        user = User.objects.create_user(**user_data)  # user ma'lumotlari asosida user yaratish
        teacher = Teacher.objects.create(user=user, **validated_data)  # teacherni create qilish
        teacher.departments.set(departments)  # .set() bilan many-to-many fieldga qiymat berish
        teacher.course.set(courses)
        return teacher  # yaratilgan teacherni qayatrish

    def update(self, instance, validated_data):  # teacher ma'lumotlarini tahrirlash
        user_data = validated_data.pop('user', {})  # user ma'lumotlarini olish bo'lmasa bosh dict
        # User serializerini yaratish:
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():  # Agar User ma'lumotlari to'g'ri bo'lsa
            user_serializer.save()  # saqlash
        # Bo'limlarni yangilash:
        instance.departments.set(validated_data.get('departments', instance.departments.all()))
        # Courslarni yangilash
        instance.course.set(validated_data.get('course', instance.departments.all()))
        instance.descriptions = validated_data.get('descriptions', instance.descriptions)  # tavsifni yangilash
        instance.save()  # o'zgarishlarni saqlash
        return instance  # o'zgargan Teacher ma'lumotlarini qaytarish

# Day modeli uchun serializer
class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'title', 'descriptions'] # Seriyalizatsiya qilinadigan maydonlar

# Rooms modeli uchun serializer
class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'title', 'descriptions'] # Seriyalizatsiya qilinadigan maydonlar

# TableType modeli uchun serializer
class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'title', 'descriptions'] # Seriyalizatsiya qilinadigan maydonlar

# Table modeli uchun serializer
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'start_time', 'end_time', 'room', 'type', 'descriptions']

# GroupStudent modeli uchun serializer
class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent  # Qaysi model bilan ishlashini ko‘rsatadi
        # Seriyalizatsiya qilinadigan maydonlar
        fields = ['id', 'title', 'course', 'teacher', 'table', 'start_date', 'end_date', 'descriptions']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['id', 'user', 'group', 'is_line', 'descriptions']

    def create(self, validated_data):  # yangi student yaratish
        user_data = validated_data.pop('user')  # user ma'lumotlarini ajratib olish
        group_data = validated_data.pop('group')  # groupni alohida ajratib olamiz
        user = User.objects.create_user(**user_data)  # user ma'lumotlari asosida yangi user yaratish
        student = Student.objects.create(user=user, **validated_data)  # student yaratish
        student.group.set(group_data)  # M2M uchun .set() ishlatamiz
        return student

    def update(self, instance, validated_data):  # student ma'lumotlarini tahrirlash
        user_data = validated_data.pop('user', {})  # user malumotlarini olish, ma'lumot bo'lmasa bo'sh dict
        # user uchun serializerni yaratish:
        user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
        if user_serializer.is_valid():  # Agar user ma'lumotlari to'g'ri bo'lsa
            user_serializer.save()  # saqlash

        if 'group' in validated_data:
            instance.group.set(validated_data['group'])  # M2M uchun .set()

        instance.group.set(validated_data.get('group', instance.group.all()))  # guruhni yangilash
        instance.is_line = validated_data.get('is_line', instance.is_line)  # holatni yangilash
        instance.descriptions = validated_data.get('descriptions', instance.descriptions)  # tavsif
        instance.save()  # saqlash
        return instance  # o'zgargan ma'lumotni qaytarish

# Parents modeli uchun serializer
class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents  # Qaysi model bilan ishlashini ko‘rsatadi
        # Seriyalizatsiya qilinadigan maydonlar
        fields = ['id', 'student', 'full_name', 'phone_number', 'address', 'descriptions']

# Attendance modeli uchun serializer
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'student', 'group', 'date', 'is_present', 'is_excused']  # Foydalaniladigan maydonlar
    def validate(self, data): # So‘rov ma'lumotlarini tekshirish
        student = data.get('student')  # So‘rovdan studentni olish
        group = data.get('group')  # So‘rovdan guruhni olish
        is_present = data.get('is_present')  # Talaba kelgan yoki kelmaganligi
        is_excused = data.get('is_excused')  # Kelmaganlik sababli bo‘lsa True

        # Student guruhga tegishli ekanligini tekshirish
        if not student.group.filter(id=group.id).exists():
            raise serializers.ValidationError("Student bu guruhda emas.")

        if is_present and is_excused:
            raise serializers.ValidationError("Darsga kelgan talabani 'is_exused'ga kiritib bo'lmaydi")

        return data


    def create(self, validated_data):
        # Yangi Attendance ob'ektini yaratish
        return super().create(validated_data)  # Obyektni saqlash va qaytarish

# Payment modeli uchun serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'student', 'amount', 'date', 'is_paid'] # Seriyalizatsiya qilinadigan maydonlar

# Assignment modeli uchun serializer
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'group', 'teacher', 'title', 'descriptions', 'due_date'] # Seriyalizatsiya qilinadigan maydonlar
        extra_kwargs = {
            'teacher': {'read_only': True}  # teacher maydoni faqat o‘qish uchun
        }

# OTPCode modeli uchun serializer
class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTPCode  # Qaysi model bilan ishlashini ko‘rsatadi
        fields = ['id', 'user', 'code', 'created', 'expires_at'] # Seriyalizatsiya qilinadigan maydonlar