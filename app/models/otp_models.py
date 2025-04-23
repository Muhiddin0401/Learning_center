from django.db import models
from django.utils import timezone
from datetime import timedelta
from .user_model import User

class OTPCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    code = models.CharField(max_length=6)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        if self.expires_at is None:
            return False
        return timezone.now() <= self.expires_at

    def __str__(self):
        return f"OTP {self.code} for {self.user.phone_number}"