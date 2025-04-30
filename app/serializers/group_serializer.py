from rest_framework import serializers  # DRF serializerlarini yaratish uchun modul
from app.models import *  # Serializer uchun kerak bo'lgan modullar

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
