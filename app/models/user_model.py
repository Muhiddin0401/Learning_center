from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser # Djangoni Default User modeli
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class BaseModel(models.Model):
    created_ed = models.DateField(auto_now_add=True)
    updated_ed = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):  # Maxsus menejer sinfi
    def create_user(self, phone_number, password=None, **extra_fields):  # Oddiy foydalanuvchi yaratish metodi
        if not phone_number:  # Telefon raqami bo‘lmasa xato
            raise ValueError('The Phone Number field must be set')
        extra_fields.setdefault('is_staff', False)  # is_staff ni defolt False qilamiz agar berilmagan bo'lsa
        user = self.model(phone_number=phone_number, **extra_fields)  # Yangi foydalanuvchi obyekti yaratish
        user.set_password(password)  # Parolni shifrlash va o‘rnatish
        user.save(using=self._db)  # Foydalanuvchini bazaga saqlash
        return user  # Yaratilgan foydalanuvchini qaytarish

    def create_superuser(self, phone_number, password=None, **extra_fields):  # Superuser yaratish metodi
        extra_fields.setdefault('is_admin', True)  # is_admin ni True qilish
        extra_fields.setdefault('is_staff', True)  # is_staff ni True qilish
        extra_fields.setdefault('is_superuser', True)  # is_superuser ni True qilish
        return self.create_user(phone_number, password, **extra_fields)  # Oddiy foydalanuvchi yaratish metodini chaqirish


class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqam '+998XXXXXXXXX' formatida bo'lishi kerak!"
    )
    username=models.CharField(max_length=25)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(validators=[phone_regex],max_length=13, unique=True)
    is_admin = models.BooleanField(default=False)  # Admin holati
    is_staff = models.BooleanField(default=False)  # Staff holati (admin panelga kirish va boshqa imtiyozlar)
    is_active = models.BooleanField(default=True)  # Foydalanuvchi faol yoki yo‘qligi
    is_student = models.BooleanField(default=False)  # Talaba holati
    is_teacher = models.BooleanField(default=False)  # O‘qituvchi holati
    is_superuser = models.BooleanField(default=False)  # Superuser holati (CreateSuperuser orqali yaratilgan)

    groups = models.ManyToManyField(  # Foydalanuvchi guruhlari
        'auth.Group',  # Django’ning auth.Group modeli
        related_name='custom_user_groups',  # Teskari aloqa nomi
        blank=True,  # Ixtiyoriy
        help_text="Ushbu foydalanuvchi tegishli bo'lgan guruhlar.",  # Yordam matni
        verbose_name='groups',  # Admin paneldagi nomi
    )
    user_permissions = models.ManyToManyField(  # Foydalanuvchi ruxsatlari
        'auth.Permission',  # Django’ning auth.Permission modeli
        related_name='custom_user_permissions',  # Teskari aloqa nomi
        blank=True,  # Ixtiyoriy
        help_text="Bu foydalanuvchi uchun maxsus ruxsatlar.",  # Yordam matni
        verbose_name='user permissions',  # Admin paneldagi nomi
    )

    objects = UserManager()  # Maxsus menejerni o‘rnatish

    USERNAME_FIELD = 'phone_number'  # Autentifikatsiya uchun asosiy maydon (telefon raqami)
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.phone_number