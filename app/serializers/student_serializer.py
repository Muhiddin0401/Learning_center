from .user_serializer import *

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

# Statistika uchun:
class StudentStatisticsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')  # user.username dan olish

    class Meta:
        model = Student
        fields = ['id', 'username', 'created_ed', 'graduation_date']

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
