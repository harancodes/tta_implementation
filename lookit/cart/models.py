from django.db import models
from user.models import User
from product.models import Variant
from coupon.models import Coupon

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def product(self):
        return self.variant.product

    class Meta:
        unique_together = ('user', 'variant')  # Prevent same product being added twice

class CartAppliedCoupon(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="applied_coupon")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
