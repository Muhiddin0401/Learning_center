from .user_views import *


# departments uchun
class DepartmentsViewSet(ModelViewSet):
    queryset = Departments.objects.all()  # Barcha departmentsni olish
    serializer_class = DepartmentSerializer  # departments uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# Course uchun
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()  # Barcha Courseni olish
    serializer_class = CourseSerializer  # Course uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# GroupStudent uchun
class GroupStudentViewSet(ModelViewSet):
    queryset = GroupStudent.objects.all()  # Barcha GroupStudentni olish
    serializer_class = GroupStudentSerializer  # GroupStudent uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# Day uchun
class DayViewSet(ModelViewSet):
    queryset = Day.objects.all()  # Barcha Dayni olish
    serializer_class = DaySerializer  # Day uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# Rooms uchun
class RoomsViewSet(ModelViewSet):
    queryset = Rooms.objects.all()  # Barcha Roomsni olish
    serializer_class = RoomsSerializer  # Rooms uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# TableType uchun
class TableTypeViewSet(ModelViewSet):
    queryset = TableType.objects.all()  # Barcha TableTypeni olish
    serializer_class = TableTypeSerializer  # TableType uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# Table uchun
class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()  # Barcha Tableni olish
    serializer_class = TableSerializer  # Table uchun serializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]  # Bu ViewSet uchun ruxsati borlar


# Parents modeli uchun ViewSet
class ParentsViewSet(ModelViewSet):
    queryset = Parents.objects.all()  # Barcha ota-onalarni olish uchun queryset
    serializer_class = ParentsSerializer  # ParentsSerializer ishlatiladi
    permission_classes = [IsAuthenticated,
                          IsAdminOrStaff]  # Faqat autentifikatsiyadan o‘tgan Admin yoki Staff uchun ruxsat
