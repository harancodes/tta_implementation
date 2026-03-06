from django.db import models
from product.models import Style, Product
import uuid

# Create your models here.
class Offer(models.Model):
    class Scopes(models.TextChoices):
        PRODUCT_BASED = 'PRODUCT_BASED'
        CATEGORY_BASED = 'CATEGORY_BASED'
    
    uuid = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100)
    scope = models.CharField(max_length=20, choices=Scopes.choices)
    
    style = models.ForeignKey(Style, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='offers')
    
    discount = models.IntegerField() #in percentage
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    is_active = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            prefix = "OFF"
            # Pad database ID estimate — better to use random unique portion before first save
            unique_num = str(uuid.uuid4().int)[:6]  # shorter unique piece
            self.uuid = f"{prefix}-{unique_num}"
        super().save(*args, **kwargs)
    