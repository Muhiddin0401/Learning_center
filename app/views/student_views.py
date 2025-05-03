from datetime import timedelta, datetime, time  # Vaqt intervallari bilan ishlash uchun modul
from django.db.models import Q

from .user_views import *
from app.permissions import (IsAdminOrStaff, IsStudent)  # Maxsus ruxsat sinflarifrom rest_framework.permissions import IsAuthenticated  # Autentifikatsiyadan o‘tgan foydalanuvchilar uchun ruxsat


class StudentViewSet(ModelViewSet):  # Student uchun CRUD operatsiyasi sinfi
    queryset = Student.objects.all()  # barcha Studentlarni olish
    serializer_class = StudentSerializer  # Student uchun Studentserializerni ishlatish
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Faqat Admin yoki Staff uchun ruxsat

    @swagger_auto_schema(operation_description="Studentlar ro'ysatini olish")  # Get so'rovi uxhun swagger izohi
    def list(self, request, *args, **kwargs):  # Studentlar ro'yxatini olish
        return super().list(request, *args, **kwargs)  # ModelViewSetni standart list metodi

    @swagger_auto_schema(operation_description="Yangi Student qo'shish")  # POST so'rovi
    def create(self, request, *args, **kwargs):  # POST funksiyasi
        return super().create(request, *args, **kwargs)  # ModelViewSetni standart create metodi

    @swagger_auto_schema(operation_description="Studentni yangilash")  # PUT/PATCH so'rovi
    def update(self, request, *args, **kwargs):  # Studentni yangilash (PUT/PATCH)
        return super().update(request, *args, **kwargs)  # ModelViewSet ning standart update metodini chaqirish

    @swagger_auto_schema(operation_description="Studentni o'chirish")  # DELETE so'rovi
    def destroy(self, request, *args, **kwargs):  # Studentni o'chirish (DELETE)
        return super().destroy(request, *args, **kwargs)  # ModelViewSet ning standart destroy metodini chaqirish

    @swagger_auto_schema(
        operation_description="Ikkita sana oralig'ida yangi qo'shilgan, bitirgan va o'qiyotgan talabalarni ko'rish (Admin/Staff uchun)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, format="date",
                                             description="Boshlang'ish sana(YYYY-MM-DD):"),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, format="date",
                                           description="Tugash sana(YYYY-MM-DD):")
            },
            required=['start_date', 'end_date']
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'newly_added': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'created_ed': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                'graduation_date': openapi.Schema(type=openapi.TYPE_STRING, format='date',
                                                                  nullable=True)
                            }
                        )
                    ),
                    'graduated': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'created_ed': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                'graduation_date': openapi.Schema(type=openapi.TYPE_STRING, format='date',
                                                                  nullable=True)
                            }
                        )
                    ),
                    'current_students': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'created_ed': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                'graduation_date': openapi.Schema(type=openapi.TYPE_STRING, format='date',
                                                                  nullable=True)
                            }
                        )
                    ),
                }
            )
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAdminOrStaff])
    def statisics(self, request):
        # Sanalarni olish
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return Response(
                {"error": "Sana formati noto‘g‘ri. YYYY-MM-DD formatida bo‘lishi kerak."},
                status=400
            )

        if start_date > end_date:
            return Response(
                {"error": "Boshlang‘ich sana tugash sanasidan katta bo‘lmasligi kerak."},
                status=400
            )
        # Datetime shaklga o‘tkazish
        start_datetime = datetime.combine(start_date, time.min)
        end_datetime = datetime.combine(end_date, time.max)
        # 1. Yangi qo‘shilgan talabalar (shu oraliqda ro‘yxatdan o‘tganlar)
        newly_added = Student.objects.filter(
            created_ed__gte=start_datetime,
            created_ed__lte=end_datetime
        )
        # 2. Bitirib ketgan talabalar (graduation_date shu oraliqda bo‘lganlar)
        graduated = Student.objects.filter(
            graduation_date__gte=start_date,
            graduation_date__lte=end_date
        )
        # 3. O‘sha vaqtda o‘qiyotgan talabalar:
        current_students = Student.objects.filter(
            Q(created_ed__lte=end_datetime) &
            (Q(graduation_date=None) | Q(graduation_date__gt=end_date))
        )
        # Serializatsiya
        newly_added_serializer = StudentStatisticsSerializer(newly_added, many=True)
        graduated_serializer = StudentStatisticsSerializer(graduated, many=True)
        current_serializer = StudentStatisticsSerializer(current_students, many=True)

        return Response({
            "newly_added": newly_added_serializer.data,
            "graduated": graduated_serializer.data,
            "current_students": current_serializer.data
        }, status=200)

    # Student davomatini ko'rish uchun
    @action(detail=True, methods=['get'], permission_classes=[IsStudent])
    @swagger_auto_schema(operation_description="Talaba Davomatini ko'rish")  # swaggerga qo'shish
    def attendance(self, request, pk=None):  # talabaga davomatini qaytarish uchun fuksiya
        student = self.get_object()  # Ayni student Ma'lumotini olish
        attendance = student.attendance.all()  # Studentga tegishli davomatlar
        serializer = AttendanceSerializer(attendance, many=True)  # to'lovlarni Json formatga o'tkazish
        return Response(serializer.data)  # JSON formatda javob qaytarish


    # Student to'lovini saqlash
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrStaff])
    @swagger_auto_schema(
        operation_description="Student to'lovlarini saqlash",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'student': openapi.Schema(type=openapi.TYPE_INTEGER, description='Student ID'),
                'amount': openapi.Schema(type=openapi.TYPE_STRING, description='To`lov summasi'),
                'date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='To`lov sanasi(YYYY-MM-DD)'),
                'is_paid': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='To`lov holati')
            },
            required = ['student', 'amount', 'data', 'is_paid']
        ),
        responses = {201: PaymentSerializer()}
    )
    def save_payments(self, request, pk=None):
        student = self.get_object()  # pk dan studentni olish
        data = request.data.copy()  # Ma'lumotlarni nusxa olish
        data['student'] = student.id  # Student ID'sini qo'shish
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


    # Student To'lovlarini ko'rish uchun
    @action(detail=True, methods=['get'], permission_classes=[IsStudent])
    @swagger_auto_schema(operation_description="Talaba To'lovlarini ko'rish")  # swaggerga qo'shish
    def payments(self, request, pk=None):  # talabaga to'lovlarini qaytarish uchun fuksiya
        student = self.get_object()  # Ayni student Ma'lumotini olish
        payments = student.payments.all()  # Studentga tegishli to'lovlarni
        serializer = PaymentSerializer(payments, many=True)  # to'lovlarni Json formatga o'tkazish
        return Response(serializer.data)  # JSON formatda javob qaytarish

    # Student Uyga vazifasini ko'rish uchun
    @swagger_auto_schema(operation_description="Talaba Uyga vazifasini ko'rish")  # swaggerga qo'shish
    @action(detail=True, methods=['get'], permission_classes=[IsStudent])
    def assignment(self, request, pk=None):  # talabaga vazifalarini qaytarish uchun fuksiya
        student = self.get_object()  # Ayni student Ma'lumotini olish
        assignment = Assignment.objects.filter(group__in=student.group.all())  # Studentga tegishli vazifalarni
        serializer = AssignmentSerializer(assignment, many=True)  # vazifalarni Json formatga o'tkazish
        return Response(serializer.data)  # JSON formatda javob qaytarish

    # Salom funksiyasi
    @swagger_auto_schema(operation_description="Salom berish")
    @action(detail=True, methods=['get'], permission_classes=[IsStudent])
    def hello(self, pk=None):
        serializer = {"Hi": "Assalomu aleykum"}
        return Response(serializer)
