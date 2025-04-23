import random
import string

# OTP code generatsiya qilish funksiyasi
def generate_otp(length = 6):
    digits = string.digits
    return ''.join(random.choice(digits) for _ in range(length))