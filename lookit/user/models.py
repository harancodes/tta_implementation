from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .utils import generate_referral_code
from datetime import timedelta
from django.utils import timezone
from coupon.models import Coupon
from product.models import Product
from django.conf import settings


# Creating custom user manager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove username field
    email = models.EmailField(unique=True)

    # will not use these fields, just making them harmless
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    full_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)

    profile_img_url = models.URLField(null=True, blank=True)
    profile_img_public_id = models.CharField(max_length=255, null=True, blank=True)

    #--referral code will be generated automatically when user signup------
    referral_code = models.CharField(max_length=50, unique=True, blank=True)
    #--referred by which user
    referred_by = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='referrals',
    )

    is_superadmin = models.BooleanField(default=False)  # only a single super admin

    status = models.CharField(max_length=10, default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    # for keeping the saved coupons by user
    saved_coupons = models.ManyToManyField(Coupon, related_name='saved_users')

    # Use email as the unique identifier for login instead of username.
    USERNAME_FIELD = 'email'

    # When creating superuser, don't ask for anything extra besides email + password
    REQUIRED_FIELDS = []

    # set custom user manager, becuase we are using email for authentication
    objects = UserManager()

    class Meta:
        ordering = ['-is_active', '-created_at']

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_referral_code()
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class OTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=settings.OTP_EXPIRY_TIME)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField()
    phone = models.CharField(max_length=30)
    second_phone = models.CharField(max_length=30, blank=True, null=True)
    address_line = models.TextField()
    city = models.CharField()
    state = models.CharField()
    pincode = models.CharField(max_length=15)
    type = models.CharField(max_length=15)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # if it's the only one set it as default
        if not Address.objects.filter(user=self.user, is_active=True).exists():
            self.is_default = True

        super().save(*args, **kwargs)

        # if it's default set is_default false for everything else
        if self.is_default:
            Address.objects.filter(user=self.user).exclude(id=self.id).update(
                is_default=False
            )

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','product')