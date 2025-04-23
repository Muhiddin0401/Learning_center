from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from app.views import OTPSendView, OTPVerifyView

urlpatterns = [
    path('otp/send/', csrf_exempt(OTPSendView.as_view()), name='otp_send'),
    path('otp/verify/', csrf_exempt(OTPVerifyView.as_view()), name='otp_verify'),
]