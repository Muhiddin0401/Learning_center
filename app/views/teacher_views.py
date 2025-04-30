from .user_views import *


class TeacherViewSet(ModelViewSet):  # Teacher uchun CRUD operatsiyasi sinfi
    queryset = Teacher.objects.all()  # barcha teacherlarni olish
    serializer_class = TeacherSerializer  # Teacher uchun teacherserializerni ishlatish
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Faqat Admin yoki Staff uchun ruxsat


    @swagger_auto_schema(operation_description="Teacherlar ro'ysatini olish")  # Get so'rovi uxhun swagger izohi
    def list(self, request, *args, **kwargs):  # Teacherlar ro'yxatini olish
        return super().list(request, *args, **kwargs)  # ModelViewSetni standart list metodi

    @swagger_auto_schema(operation_description="Yangi Teacher qo'shish")  # POST so'rovi
    def create(self, request, *args, **kwargs):  # POST funksiyasi
        return super().create(request, *args, **kwargs)  # ModelViewSetni standart create metodi

    @swagger_auto_schema(operation_description="Teacherni yangilash")  # PUT/PATCH so'rovi
    def update(self, request, *args, **kwargs):  # Teacherni yangilash (PUT/PATCH)
        return super().update(request, *args, **kwargs)  # ModelViewSet ning standart update metodini chaqirish

    @swagger_auto_schema(operation_description="Teacherni o'chirish")  # DELETE so'rovi
    def destroy(self, request, *args, **kwargs):  # Foydalanuvchini o'chirish (DELETE)
        return super().destroy(request, *args, **kwargs)  # ModelViewSet ning standart destroy metodini chaqirish

    # Teacher faqat o'ziga tegishli guruhlarni ko'rish uchun maxsus action
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsTeacher, IsAdminOrStaff])
    @swagger_auto_schema(operation_description="O'qituvchi guruhlarini ko'rish")
    def groups(self, request, pk=None):  # Guruhlarni qaytarish
        teacher = self.get_object()  # Joriy teacher obyektini olish
        groups = teacher.get_teacher.all()  # Faqat teacher ga tegishli guruhlar
        serializer = GroupStudentSerializer(groups, many=True)  # Guruhlarni serializatsiya qilish
        return Response(serializer.data)  # JSON formatda qaytarish

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated, IsTeacher, IsAdminOrStaff])
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
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsTeacher, IsAdminOrStaff])
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
        teacher = self.get_object()  # So‘rovdan guruh ID sini olish
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
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsTeacher, IsTeacherOfGroup])
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
