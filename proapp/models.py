from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.apps import apps

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    id_proof = models.FileField(upload_to='id_proofs/')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Flat(models.Model):
    flat_id = models.CharField(max_length=10, unique=True)
    flat_number = models.CharField(max_length=4)
    hall = models.IntegerField()
    bedroom = models.IntegerField()
    bathroom = models.IntegerField()
    kitchen = models.IntegerField()
    type_of_flat = models.CharField(max_length=50, null=True)  # New field
    description = models.TextField(null=True)
    rent_amount=models.IntegerField(null=True)
    buy_amount=models.IntegerField(null=True)
    payment_status_flat = models.IntegerField(default=1)  # New field to track payment status

    def __str__(self):
        return self.flat_number

    def update_payment_status(self):
        # Check if any associated Payment has non-pending status for rent or buy
        has_pending_payment = self.payments.filter(buy_status='pending', rent_status='pending').exists()
        self.payment_status_flat = 1 if has_pending_payment else 0
        self.save()

    # We don't need flat_image here anymore


def flat_image_upload_path(instance, filename):
        # Define the path as "flat_images/<flat_id>/<filename>"
    return f"flat_images/{instance.flat.flat_id}/{filename}"


    def __str__(self):
        return self.flat_number

class FlatImage(models.Model):
    flat = models.ForeignKey(Flat, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=flat_image_upload_path)
    def __str__(self):
        return f"Image for {self.flat.flat_number}"
    

    # models.py

User = get_user_model()
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    flat = models.ForeignKey('proapp.Flat', on_delete=models.CASCADE, related_name='payments')
    rent_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    buy_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment by {self.user.username} for Flat {self.flat.flat_id} - Amount: {self.amount} - Date: {self.date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update payment_status_flat in the related Flat instance
        self.flat.update_payment_status()





class ProgramRegistration(models.Model):
    program_reg_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"Registration with a fee of {self.program_reg_fee}"

class Program(models.Model):
    program_registration = models.OneToOneField(ProgramRegistration, on_delete=models.CASCADE, related_name="program", null=True)
    program_name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    date = models.DateField(null=True)
    location = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="programs", null=True)
    approval_status = models.BooleanField(default=False)
    payment_status = models.BooleanField(default=False)
    registration_date = models.DateTimeField(null=True)
    program_image = models.ImageField(upload_to='program_images/', null=True, blank=True)  # Add this field

    @property
    def program_reg_fee(self):
        return self.program_registration.program_reg_fee if self.program_registration else None

    def __str__(self):
        return self.program_name