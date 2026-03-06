from django.db import models
import uuid

class Style(models.Model):
    name = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['is_deleted', '-created_at']


class Product(models.Model):
    class Category(models.TextChoices):
        MEN = 'MEN', 'Men'
        WOMEN = 'WOMEN', 'Women'
        KIDS = 'KIDS', 'Kids'
        UNISEX = 'UNISEX', 'Unisex'
        
    class BaseColor(models.TextChoices):
        WHITE = "white", "White"
        BLACK = "black", "Black"
        BEIGE = "beige", "Beige"
        GREEN = "green", "Green"
        BLUE = "blue", "Blue"
        RED = "red", "Red"
        ORANGE = "orange", "Orange"
        GREY = "grey", "Grey"
        YELLOW = "yellow", "Yellow"
        BROWN = "brown", "Brown"
        PURPLE = "purple", "Purple"
        PINK = "pink", "Pink"

    uuid = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    image_url = models.URLField()
    image_public_id = models.CharField(max_length=255)

    material = models.CharField(max_length=50, null=True, blank=True)
    fit = models.CharField(max_length=50, null=True, blank=True)
    care_instructions = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    category = models.CharField(
        max_length=10, choices=Category.choices, default=Category.UNISEX
    )
    style = models.ForeignKey(Style, on_delete=models.PROTECT, blank=True, null=True)
    base_color = models.CharField(max_length=20, choices=BaseColor.choices, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_active','-created_at']
        
    def save(self, *args, **kwargs):
        if not self.uuid:
            prefix = "PRD"
            # Pad database ID estimate — better to use random unique portion before first save
            unique_num = str(uuid.uuid4().int)[:6]  # shorter unique piece
            self.uuid = f"{prefix}-{unique_num}"
        super().save(*args, **kwargs)
        
        
class Variant(models.Model): 
    class Size(models.TextChoices):
        XS = "XS", "XS"
        S = "S", "S"
        M = "M", "M"
        L = "L", "L"
        XL = "XL", "XL"
        XXL = "XXL", "XXL"
        XXXL = "XXXL", "XXXL"
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='variant')
    size = models.CharField(max_length=10, choices=Size.choices)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'size'], name="unique_product_size")
        ]
    
    #ensure size is always upper case
    def save(self, *args, **kwargs):
        if self.size:
            self.size = self.size.upper()
        super().save(*args, **kwargs)
        
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.URLField()
    image_public_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
        
