# # from django.db import models
# # from django.contrib.auth.models import AbstractUser
# # # Create your models here.
# # class CustomUser(AbstractUser):
# #     def __str__(self):
# #         return self.username


# from django.db import models
# from django.contrib.auth.models import User
# from django.core.validators import MinValueValidator
# from decimal import Decimal

# class Profile(models.Model):
#     """User profile extension for additional user information"""
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
#     student_id = models.CharField(max_length=20, unique=True)
#     phone_number = models.CharField(max_length=15, blank=True)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, 
#                                 validators=[MinValueValidator(Decimal('0.00'))])
    
#     def __str__(self):
#         return f"{self.user.username} - {self.student_id}"

# class MealCategory(models.Model):
#     """Categories for meals (breakfast, lunch, dinner, etc.)"""
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)

#     class Meta:
#         verbose_name_plural = "Meal Categories"
    
#     def __str__(self):
#         return self.name

# class MenuItem(models.Model):
#     """Individual food items available in the mess"""
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     category = models.ForeignKey(MealCategory, on_delete=models.CASCADE, related_name='items')
#     price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
#     is_vegetarian = models.BooleanField(default=False)
#     is_available = models.BooleanField(default=True)
#     image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    
#     def __str__(self):
#         return self.name

# class MenuSchedule(models.Model):
#     """Daily or weekly menu schedule for the mess"""
#     date = models.DateField()
#     breakfast_items = models.ManyToManyField(MenuItem, related_name='breakfast_schedules', blank=True)
#     lunch_items = models.ManyToManyField(MenuItem, related_name='lunch_schedules', blank=True)
#     dinner_items = models.ManyToManyField(MenuItem, related_name='dinner_schedules', blank=True)
    
#     def __str__(self):
#         return f"Menu for {self.date}"

# class Transaction(models.Model):
#     """Financial transactions for wallet recharges and meal purchases"""
#     TRANSACTION_TYPES = (
#         ('TOPUP', 'Wallet Top-up'),
#         ('PURCHASE', 'Meal Purchase'),
#         ('REFUND', 'Refund'),
#     )
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
#     description = models.TextField(blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     reference_id = models.CharField(max_length=100, blank=True)
#     status = models.CharField(max_length=20, default='COMPLETED')
    
#     def __str__(self):
#         return f"{self.transaction_type} - {self.user.username} - {self.amount}"

# class MealOrder(models.Model):
#     """Order for meals placed by users"""
#     ORDER_STATUS = (
#         ('PENDING', 'Pending'),
#         ('CONFIRMED', 'Confirmed'),
#         ('READY', 'Ready for Pickup'),
#         ('DELIVERED', 'Delivered'),
#         ('CANCELLED', 'Cancelled'),
#     )
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
#     order_date = models.DateTimeField(auto_now_add=True)
#     meal_date = models.DateField()  # Date when the meal will be served
#     meal_type = models.CharField(max_length=20)  # Breakfast, Lunch, Dinner
#     status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
#     notes = models.TextField(blank=True)
#     transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    
#     def __str__(self):
#         return f"{self.user.username} - {self.meal_type} - {self.meal_date}"

# class OrderItem(models.Model):
#     """Individual items within a meal order"""
#     order = models.ForeignKey(MealOrder, on_delete=models.CASCADE, related_name='items')
#     menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
#     quantity = models.PositiveIntegerField(default=1)
#     unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
#     @property
#     def total_price(self):
#         return self.quantity * self.unit_price
    
#     def __str__(self):
#         return f"{self.quantity} x {self.menu_item.name}"

# class Feedback(models.Model):
#     """User feedback about meals and service"""
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')
#     order = models.ForeignKey(MealOrder, on_delete=models.SET_NULL, null=True, blank=True)
#     rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
#     comment = models.TextField(blank=True)
#     submitted_date = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.user.username} - Rating: {self.rating}"

# class Announcement(models.Model):
#     """System announcements for all users"""
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     publish_date = models.DateTimeField(auto_now_add=True)
#     expiry_date = models.DateTimeField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
    
#     def __str__(self):
#         return self.title


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    
    # Optional fields - you can add or remove these as needed
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    
    # Account verification fields
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    # For password reset
    reset_password_token = models.CharField(max_length=100, blank=True)
    reset_password_expires = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

# Automatically create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Optional: For tracking login attempts (useful for security)
class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    user_agent = models.TextField(blank=True)
    
    def __str__(self):
        status = "Successful" if self.successful else "Failed"
        return f"{status} login attempt for {self.user} from {self.ip_address}"