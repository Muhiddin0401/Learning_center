from .user_serializer import *

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
