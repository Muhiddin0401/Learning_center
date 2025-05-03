from .teacher_model import *

class Student(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='student_profile')
    group=models.ManyToManyField('GroupStudent',related_name='get_group')
    is_line=models.BooleanField(default=False) # student onlayn yoki oflayn o'qishi
    graduation_date = models.DateField(null=True, blank=True)
    descriptions=models.CharField(max_length=500,blank=True,null=True)
    def __str__(self):
        return self.user.phone_number

class Parents(BaseModel):
    student=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='get_student')
    full_name=models.CharField(max_length=50,null=True,blank=True)
    phone_number=models.CharField(max_length=15,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    descriptions=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.full_name

class Attendance(BaseModel): # Davomat uchun modell
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    group = models.ForeignKey('GroupStudent', on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField(auto_now_add=True) # Davomat iqlingan kuni
    is_present = models.BooleanField(default=False)  # Talaba kelgan yoki kelmaganligi
    is_excused = models.BooleanField(default=False)  # Kelmaganlik sababli bo‘lsa True, aks holda False
    def __str__(self):
        return f"{self.student}-{self.date}" # String ko‘rinishi

class Payment(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2) # to'lov summasi
    date = models.DateField() # to'lov sanasi
    is_paid = models.BooleanField(default=False) #to'lov holati

    def __str__(self):
        return f"{self.student} - {self.amount} - {self.is_paid}"

class Assignment(BaseModel):
    group = models.ForeignKey('GroupStudent', on_delete=models.CASCADE, related_name='assignment')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignment')
    title = models.CharField(max_length=100) # Vazifa nomi
    descriptions = models.TextField() # Vazifa matni
    due_date = models.DateField() # Topshirish muddati

    def __str__(self):
        return self.title
