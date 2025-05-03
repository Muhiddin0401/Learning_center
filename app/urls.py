from django.urls import path, include  # URL yo‘naltirish uchun modullar
from rest_framework.routers import DefaultRouter  # DRF routeri (ViewSetlarni avtomatik URLga ulash uchun)
from app.views import (UserViewSet, TeacherViewSet, StudentViewSet, DepartmentsViewSet, CourseViewSet,
                    GroupStudentViewSet, DayViewSet, RoomsViewSet, TableTypeViewSet, TableViewSet,
                    ParentsViewSet, OTPViewSet)  # Barcha ViewSetlar import qilinadi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView  # JWT token olish va yangilash uchun viewlar
from drf_yasg.views import get_schema_view  # Swagger dokumentatsiyasi uchun schema view
from drf_yasg import openapi  # Swagger uchun openapi moduli
from rest_framework import permissions  # Ruxsatlar moduli

# Router yaratish (ViewSetlarni avtomatik URLga ulash uchun)
router = DefaultRouter()
router.register(r'users', UserViewSet)  # /users/ endpointi uchun UserViewSet
router.register(r'teachers', TeacherViewSet)  # /teachers/ endpointi uchun TeacherViewSet
router.register(r'students', StudentViewSet)  # /students/ endpointi uchun StudentViewSet
# router.register(r'departments', DepartmentsViewSet)  # /departments/ endpointi uchun DepartmentsViewSet
# router.register(r'courses', CourseViewSet)  # /courses/ endpointi uchun CourseViewSet
router.register(r'groups', GroupStudentViewSet)  # /groups/ endpointi uchun GroupStudentViewSet
# router.register(r'days', DayViewSet)  # /days/ endpointi uchun DayViewSet
# router.register(r'rooms', RoomsViewSet)  # /rooms/ endpointi uchun RoomsViewSet
# router.register(r'table-types', TableTypeViewSet)  # /table-types/ endpointi uchun TableTypeViewSet
# router.register(r'tables', TableViewSet)  # /tables/ endpointi uchun TableViewSet
# router.register(r'parents', ParentsViewSet)  # /parents/ endpointi uchun ParentsViewSet
router.register(r'otp', OTPViewSet)  # /otp/ endpointi uchun OTPViewSet

# Swagger sozlamalari (API dokumentatsiyasi uchun)
schema_view = get_schema_view(
    openapi.Info(
        title="Learning Center API",  # API nomi
        default_version='v1',  # Versiya
        description="Learning Center API dokumentatsiyasi",  # Tavsif
    ),
    public=True,  # Hammaga ochiq
    permission_classes=[permissions.AllowAny],  # Ruxsat (hamma uchun ochiq)
    authentication_classes=[],
)
schema_view.security_definitions = {
    'Bearer': {  # JWT token sozlamasi
        'type': 'apiKey',
        'name': 'Authorization',
        'in': 'header',
        'description': 'Enter your token: Bearer <token>'
    }
}
schema_view.security = [{'Bearer': []}]  # Swaggerda Bearer token ishlatish

# URL yo‘naltirishlari
urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),  # Swagger UI uchun endpoint
    path('docs/', include(router.urls)),  # Routerdagi barcha URLlarni qo‘shish
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT token olish uchun endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT token yangilash uchun endpoint
]