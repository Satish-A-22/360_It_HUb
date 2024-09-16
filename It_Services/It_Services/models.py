# myapp/models.py
from django.db import models

class UserData(models.Model):
    id=models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    check_me_out = models.BooleanField(default=False)
    
class Service(models.Model):
    id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    payment_terms = models.TextField()
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_package = models.CharField(max_length=100)
    service_tax = models.DecimalField(max_digits=5, decimal_places=2)
    service_image = models.ImageField(upload_to='services/')

class Subscription(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    address = models.TextField()
    razorpay_order_id = models.CharField(max_length=255, null=False)
    razorpay_payment_id = models.CharField(max_length=255, null=False)
    razorpay_signature = models.CharField(max_length=255, null=False)
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)