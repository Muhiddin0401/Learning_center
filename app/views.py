from rest_framework.viewsets import ModelViewSet  # CRUD uchun DRF ning ModelViewSet moduli
from rest_framework.decorators import action, \
    permission_classes  # Maxsus endpointlar (actions) yaratish uchun dekorator
from rest_framework.response import Response  # API javoblarini qaytarish uchun Response klassi
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi

from app.models import *  # CRUD qilinadigan modellar
from .serializers import *  # Serializers

from drf_yasg.utils import swagger_auto_schema  # swagger dokumentatsiyasi uchun dekorator
from drf_yasg import openapi  # swagger uchun openapi moduli

# Autintifiaktisiya va ruxsatlar uchun kerakli kuitibxonalar
from .permissions import IsAdminOrStaff, IsTeacher, IsStudent, IsTeacherOfGroup # Maxsus ruxsat sinflarifrom rest_framework.permissions import IsAuthenticated  # Autentifikatsiyadan o‘tgan foydalanuvchilar uchun ruxsat
from django.utils import timezone  # Vaqt bilan ishlash uchun Django moduli
from datetime import timedelta  # Vaqt intervallari bilan ishlash uchun modul
import random  # Tasodifiy OTP kodi generatsiyasi uchun


class UserViewSet(ModelViewSet):  # User uchun CRUD operatsiyasi sinfi
    queryset = User.objects.all()  # barcha foydalanuvhilarni olish
    serializer_class = UserSerializer  # User uchun Userserializerni ishlatish
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    @swagger_auto_schema(operation_description="Foydalanuvchilar ro'ysatini olish")  # Get so'rovi uxhun swagger izohi
    def list(self, request, *args, **kwargs):  # Fotdalanuvchilar ro'yxatini olish
        return super().list(request, *args, **kwargs)  # ModelViewSetni standart list metodi

    @swagger_auto_schema(operation_description="Yangi Foydalanuvchi qo'shish")  # POST so'rovi
    def create(self, request, *args, **kwargs):  # POST funksiyasi
        return super().create(request, *args, **kwargs) # ModelViewSetni standart create metodi

    @swagger_auto_schema(operation_description="Foydalanuvchini yangilash")  # PUT/PATCH so'rovi
    def update(self, request, *args, **kwargs):  # Foydalanuvchini yangilash (PUT/PATCH)
        return super().update(request, *args, **kwargs)  # ModelViewSet ning standart update metodini chaqirish

    @swagger_auto_schema(operation_description="Foydalanuvchini o'chirish")  # DELETE so'rovi
    def destroy(self, request, *args, **kwargs):  # Foydalanuvchini o'chirish (DELETE)
        return super().destroy(request, *args, **kwargs)  # ModelViewSet ning standart destroy metodini chaqirish

class TeacherViewSet(ModelViewSet):  # Teacher uchun CRUD operatsiyasi sinfi
    queryset = Teacher.objects.all()  # barcha teacherlarni olish
    serializer_class = TeacherSerializer  # Teacher uchun teacherserializerni ishlatish

    @swagger_auto_schema(operation_description="Teacherlar ro'ysatini olish")  # Get so'rovi uxhun swagger izohi
    def list(self, request, *args, **kwargs):  # Teacherlar ro'yxatini olish
        return super().list(request, *args, **kwargs)  # ModelViewSetni standart list metodi

    @swagger_auto_schema(operation_description="Yangi Teacher qo'shish")  # POST so'rovi
    def create(self, request, *args, **kwargs):  # POST funksiyasi
        return super().create(request, *args, **kwargs) # ModelViewSetni standart create metodi

    @swagger_auto_schema(operation_description="Teacherni yangilash")  # PUT/PATCH so'rovi
    def update(self, request, *args, **kwargs):  # Teacherni yangilash (PUT/PATCH)
        return super().update(request, *args, **kwargs)  # ModelViewSet ning standart update metodini chaqirish

    @swagger_auto_schema(operation_description="Teacherni o'chirish")  # DELETE so'rovi
    def destroy(self, request, *args, **kwargs):  # Foydalanuvchini o'chirish (DELETE)
        return super().destroy(request, *args, **kwargs)  # ModelViewSet ning standart destroy metodini chaqirish

    # Teacher faqat o'ziga tegishli guruhlarni ko'rish uchun maxsus action
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsTeacher])
    @swagger_auto_schema(operation_description="O'qituvchi guruhlarini ko'rish")
    def groups(self,request, pk=None): #Guruhlarni qaytarish
        teacher = self.get_object() # Joriy teacher obyektini olish
        groups = teacher.get_teacher.all() # Faqat teacher ga tegishli guruhlar
        serializer = GroupStudentSerializer(groups, many=True) # Guruhlarni serializatsiya qilish
        return Response(serializer.data) # JSON formatda qaytarish

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsTeacher])
    # swagger izohi
    @swagger_auto_schema(operation_description="O'qituvchini bir guruhidagi studentlar ro'yxati")
    def students(self, request, pk=None):  # guruhdagi studentlar ro'yxatini olish
        teacher = self.get_object()  # joriy teacher ni olish
        if not pk:
            return Response({"error": "Guruh ID kiritilishi kerak"},
                            status=400)  # xato xabarini berish
        # Guruhni teacher va group_id bo‘yicha filtrlang
        group = GroupStudent.objects.filter(id=pk, teacher=teacher).first()
        if not group:
            return Response({"error": "Guruh topilmadi yoki bu guruh sizga tegishli emas"},
                            status=404)
        # Faqat o‘sha guruhdagi studentlarni olish
        students = Student.objects.filter(group=group)
        serializer = StudentSerializer(students, many=True)  # Studentlarni serializatsiya qilish
        return Response(serializer.data)  # JSON formatida javob qaytarish

    # Yo'qlama uchun maxsus action:

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsTeacher])
    @swagger_auto_schema(
        operation_description="Yo'qlama qilish",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'group': openapi.Schema(type=openapi.TYPE_INTEGER, description='Group ID'),
                'attendance_list': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'present': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_INTEGER),
                            description='Kelgan student ID lar'
                        ),
                        'excused': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_INTEGER),
                            description='Sababli kelmagan student ID lar'
                        )
                    },
                    description='Yo\'qlama ro\'yxati'
                ),
            },
            required=['group', 'attendance_list']
        )
    )
    def mark_attendance(self, request, pk=None):
        # Joriy teacher ni olish (pk orqali, ya'ni /teachers/1/mark_attendance/)
        teacher = self.get_object()        # So‘rovdan guruh ID sini olish
        group_id = request.data.get('group')
        # So‘rovdan yo‘qlama ma'lumotlarini olish ({"present": [1, 2, 3, 4], "excused": [5, 6]})
        attendance_list = request.data.get('attendance_list', {})

        # Guruh ID si kiritilganligini tekshirish
        if not group_id:
            return Response({"error": "Guruh ID kiritilishi kerak"}, status=400)

        # Guruhni teacher va group_id bo‘yicha filtrlash
        group = GroupStudent.objects.filter(id=group_id, teacher=teacher).first()
        if not group:
            return Response({"error": "Guruh topilmadi yoki bu guruh sizga tegishli emas"},
                            status=404)

        # attendance_list ichidan present va excused ro‘yxatlarini olish
        present_students = attendance_list.get('present', [])  # Kelgan talabalar ro‘yxati
        excused_absent_students = attendance_list.get('excused', [])  # Sababli kelmagan talabalar ro‘yxati

        # Guruhdagi barcha talabalarni olish (ID lar ro‘yxati sifatida)
        all_students = list(Student.objects.filter(group=group).values_list('id', flat=True))

        # Sababsiz kelmagan talabalar: guruhdagi barcha talabalar minus present va excused
        absent_students = [student_id for student_id in all_students if
                           student_id not in present_students and student_id not in excused_absent_students]

        # Har bir talaba uchun Attendance ob'ektini yaratish
        for student_id in all_students:
            # Talaba ma'lumotlarini tayyorlash
            attendance_data = {
                'student': student_id,  # Talaba ID si
                'group': group.id,  # Guruh ID si
                'is_present': student_id in present_students,  # Talaba kelgan bo‘lsa True
                'is_excused': student_id in excused_absent_students  # Talaba sababli kelmagan bo‘lsa True
            }
            # Serializer orqali ma'lumotlarni tekshirish va saqlash
            serializer = AttendanceSerializer(data=attendance_data, context={'request': request})
            if serializer.is_valid():
                serializer.save()  # Attendance ob'ektini saqlash
            else:
                # Agar ma'lumotlar noto‘g‘ri bo‘lsa, xatolarni qaytarish
                return Response(serializer.errors, status=400)

        # Yakuniy javobni qaytarish
        return Response({
            "present_students": present_students,  # Kelgan talabalar ro‘yxati [1, 2, 3, 4]
            "absent_students": absent_students,  # Sababsiz kelmagan talabalar ro‘yxati [7, 8]
            "excused_absent_students": excused_absent_students  # Sababli kelmagan talabalar ro‘yxati [5, 6]
        }, status=201)

    # Vazifa uchun maxsus action
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated,IsTeacher,IsTeacherOfGroup])
    @swagger_auto_schema(operation_description="Vazifa berish",  # Swaggerda endpointning izohi
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'group': openapi.Schema(type=openapi.TYPE_INTEGER, description='Guruh ID'),
                                 'title': openapi.Schema(type=openapi.TYPE_STRING, description='Vazifa nomi'),
                                 'descriptions': openapi.Schema(type=openapi.TYPE_STRING, description='Vazifa matni'),
                                 'due_date': openapi.Schema(type=openapi.TYPE_STRING, format='date',
                                                            description='Topshirish sanasi (YYYY-MM-DD)')
                             },
                             required=['group', 'title', 'descriptions', 'due_date'],
                         ),
                         responses={201: AssignmentSerializer()}
                         )
    def create_assignment(self, request):  # Yangi vazifa yaratish
        serializer = AssignmentSerializer(data=request.data)  # So‘rov ma'lumotlarini seriyalizatsiya qilish
        if serializer.is_valid():  # Agar ma'lumotlar to‘g‘ri bo‘lsa
            # Vazifani teacher bilan bog‘lab saqlash
            serializer.save(teacher=request.user.teacher_profile)
            return Response(serializer.data, status=201)  # Muvaffaqiyatli javob qaytarish
        return Response(serializer.errors, status=400)  # Xato xabarini qaytarish

class StudentViewSet(ModelViewSet):  # Student uchun CRUD operatsiyasi sinfi
    queryset = Student.objects.all()  # barcha Studentlarni olish
    serializer_class = StudentSerializer  # Student uchun Studentserializerni ishlatish

    @swagger_auto_schema(operation_description="Studentlar ro'ysatini olish")  # Get so'rovi uxhun swagger izohi
    def list(self, request, *args, **kwargs):  # Studentlar ro'yxatini olish
        return super().list(request, *args, **kwargs)  # ModelViewSetni standart list metodi

    @swagger_auto_schema(operation_description="Yangi Student qo'shish")  # POST so'rovi
    def create(self, request, *args, **kwargs):  # POST funksiyasi
        return super().create(request, *args, **kwargs) # ModelViewSetni standart create metodi

    @swagger_auto_schema(operation_description="Studentni yangilash")  # PUT/PATCH so'rovi
    def update(self, request, *args, **kwargs):  # Studentni yangilash (PUT/PATCH)
        return super().update(request, *args, **kwargs)  # ModelViewSet ning standart update metodini chaqirish

    @swagger_auto_schema(operation_description="Studentni o'chirish")  # DELETE so'rovi
    def destroy(self, request, *args, **kwargs):  # Studentni o'chirish (DELETE)
        return super().destroy(request, *args, **kwargs)  # ModelViewSet ning standart destroy metodini chaqirish

    # Student davomatini ko'rish uchun
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsStudent])
    @swagger_auto_schema(operation_description="Talaba Davomatini ko'rish") # swaggerga qo'shish
    def attendance(self, request, pk=None): # talabaga davomatini qaytarish uchun fuksiya
        student = self.get_object() # Ayni student Ma'lumotini olish
        attendance = student.attendace.all() # Studentga tegishli davomatlar
        serializer = AttendanceSerializer(attendance, many=True) # to'lovlarni Json formatga o'tkazish
        return  Response(serializer.data) # JSON formatda javob qaytarish

    # Student To'lovlarini ko'rish uchun
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsStudent])
    @swagger_auto_schema(operation_description="Talaba To'lovlarini ko'rish") # swaggerga qo'shish
    def payments(self, request, pk=None): # talabaga to'lovlarini qaytarish uchun fuksiya
        student = self.get_object() # Ayni student Ma'lumotini olish
        payments = student.attendace.all() # Studentga tegishli to'lovlarni
        serializer = PaymentSerializer(payments, many=True) # to'lovlarni Json formatga o'tkazish
        return  Response(serializer.data) # JSON formatda javob qaytarish


    # Student Uyga vazifasini ko'rish uchun
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsStudent])
    @swagger_auto_schema(operation_description="Talaba Uyga vazifasini ko'rish") # swaggerga qo'shish
    def assignment(self, request, pk=None): # talabaga vazifalarini qaytarish uchun fuksiya
        student = self.get_object() # Ayni student Ma'lumotini olish
        assignment = Assignment.objects.filter(group__in=student.group.all()) # Studentga tegishli vazifalarni
        serializer = AssignmentSerializer(assignment, many=True) # vazifalarni Json formatga o'tkazish
        return  Response(serializer.data) # JSON formatda javob qaytarish

""" Qo'shimcha modellar uchun ViewSet """
# departments uchun
class DepartmentsViewSet(ModelViewSet):
    queryset = Departments.objects.all() # Barcha departmentsni olish
    serializer_class = DepartmentSerializer # departments uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff] # Bu ViewSet uchun ruxsati borlar

# Course uchun
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all() # Barcha Courseni olish
    serializer_class = CourseSerializer # Course uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff] # Bu ViewSet uchun ruxsati borlar

# GroupStudent uchun
class GroupStudentViewSet(ModelViewSet):
    queryset = GroupStudent.objects.all() # Barcha GroupStudentni olish
    serializer_class = GroupStudentSerializer # GroupStudent uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff] # Bu ViewSet uchun ruxsati borlar

# Day uchun
class DayViewSet(ModelViewSet):
    queryset = Day.objects.all() # Barcha Dayni olish
    serializer_class = DaySerializer # Day uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff] # Bu ViewSet uchun ruxsati borlar

# Rooms uchun
class RoomsViewSet(ModelViewSet):
    queryset = Rooms.objects.all() # Barcha Roomsni olish
    serializer_class = RoomsSerializer # Rooms uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff] # Bu ViewSet uchun ruxsati borlar

# TableType uchun
class TableTypeViewSet(ModelViewSet):
    queryset = TableType.objects.all() # Barcha TableTypeni olish
    serializer_class = TableTypeSerializer # TableType uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff] # Bu ViewSet uchun ruxsati borlar

# Table uchun
class TableViewSet(ModelViewSet):
    queryset = Table.objects.all() # Barcha Tableni olish
    serializer_class = TableSerializer # Table uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff] # Bu ViewSet uchun ruxsati borlar

# Parents modeli uchun ViewSet
class ParentsViewSet(ModelViewSet):
    queryset = Parents.objects.all()  # Barcha ota-onalarni olish uchun queryset
    serializer_class = ParentsSerializer  # ParentsSerializer ishlatiladi
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Faqat autentifikatsiyadan o‘tgan Admin yoki Staff uchun ruxsat

# OTPCode modeli uchun ViewSet (OTP bilan parol o‘zgartirish)
class OTPViewSet(ModelViewSet):
    queryset = OTPCode.objects.all()  # Barcha OTP kodlarini olish uchun queryset
    serializer_class = OTPSerializer  # OTPSerializer ishlatiladi
    permission_classes = [IsAuthenticated]  # Faqat autentifikatsiyadan o‘tgan foydalanuvchilar uchun ruxsat

    # OTP so‘rash uchun maxsus endpoint
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    @swagger_auto_schema(operation_description="OTP so‘rash")  # Swaggerda endpointning izohi
    def request_otp(self, request):  # Yangi OTP kodi yaratish va foydalanuvchiga yuborish
        user = request.user  # Joriy foydalanuvchi obyektini olish
        code = str(random.randint(100000, 999999))  # 6 raqamli tasodifiy OTP kodi generatsiyasi
        otp = OTPCode.objects.create(user=user, code=code)  # OTPCode obyektini yaratish
        print(f"OTP kodi: {code}")  # Test uchun OTP kodini konsolga chiqarish (real loyihada SMS/email orqali yuboriladi)
        return Response({"message": "OTP yuborildi."}, status=200)  # Muvaffaqiyatli javob qaytarish

    # Parolni o‘zgartirish uchun maxsus endpoint
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    @swagger_auto_schema(operation_description="Parolni o‘zgartirish")  # Swaggerda endpointning izohi
    def reset_password(self, request):  # OTP kodi yordamida parolni o‘zgartirish
        code = request.data.get('code')  # So‘rovdan OTP kodini olish
        new_password = request.data.get('new_password')  # So‘rovdan yangi parolni olish
        try:  # OTP kodini tekshirish
            otp = OTPCode.objects.get(user=request.user, code=code)  # Foydalanuvchiga tegishli OTP kodini qidirish
            if not otp.is_valid():  # OTP kodining amal qilish muddati o‘tganligini tekshirish
                return Response({"error": "Noto‘g‘ri yoki muddati o‘tgan OTP."}, status=400)  # Xato xabarini qaytarish
        except OTPCode.DoesNotExist:  # Agar OTP kodi topilmasa
            return Response({"error": "Noto‘g‘ri OTP."}, status=400)  # Xato xabarini qaytarish
        request.user.set_password(new_password)  # Yangi parolni o‘rnatish
        request.user.save()  # Foydalanuvchi ma'lumotlarini saqlash
        otp.delete()  # Ishlatilgan OTP kodini o‘chirish
        return Response({"message": "Parol muvaffaqiyatli o‘zgartirildi."}, status=200)  # Muvaffaqiyatli javob qaytarish
