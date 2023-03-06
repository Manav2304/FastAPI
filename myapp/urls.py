from django.urls import path
from .views import payment_status

urlpatterns = [
    # Other URL patterns for your app
    path('', payment_status, name='payment_status'),
]
