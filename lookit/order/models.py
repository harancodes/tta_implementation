from django.db import models
from user.models import User, Address
from product.models import Variant, Product
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from coupon.models import Coupon
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):

    class PaymentMethod(models.TextChoices):
        COD = 'COD', 'Cash on Delivery'
        ONLINE_PAYMENT = (
            'ONLINE_PAYMENT',
            'Online Payment',
        )
        WALLET = 'WALLET', 'Wallet'

    uuid = models.CharField(max_length=20, blank=True, null=True)  # add unique is true
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(
        max_length=30, choices=PaymentMethod.choices, blank=True
    )

    total_items = models.PositiveIntegerField(
        default=0
    )  # number of products in order (not quantity)
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # sum of base price of all items
    discount_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )  # sum of all discount amount applied in all products
    tax_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )  # sum of tax amount of all products
    delivery_total = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # total delivery amount

    coupon_applied = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True
    )
    coupon_discount_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    grand_total = models.DecimalField(max_digits=10, decimal_places=2)  # grand total

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.uuid:
            # Example: ORDM-2025-000123
            year = timezone.now().year
            prefix = "ORDM"
            # Pad database ID estimate — better to use random unique portion before first save
            unique_num = str(uuid.uuid4().int)[:6]  # shorter unique piece
            self.uuid = f"{prefix}-{year}-{unique_num}"
        super().save(*args, **kwargs)


class OrderItems(models.Model):

    class OrderStatus(models.TextChoices):
        INITIATED = 'INITIATED', 'Order Initiated'
        PLACED = 'PLACED', 'Order Placed'
        SHIPPED = 'SHIPPED', 'Shipped'
        OUT_FOR_DELIVERY = 'OUT_FOR_DELIVERY', 'Out For Delivery'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'
        RETURNED = 'RETURNED', 'Returned'
        REFUNDED = 'REFUNDED', 'Refunded'

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        FAILED = 'FAILED', 'Failed'
        COD = 'COD', 'Cash on Delivery'
        REFUNDED = 'REFUNDED', 'Refunded'

    uuid = models.CharField(max_length=20, unique=True, blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(
        Variant, on_delete=models.CASCADE, related_name='orders'
    )
    payment_status = models.CharField(
        max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )

    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # base price with tax
    sub_total = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # quantity x unit_price
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    coupon_discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )  # final line total

    tax_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    order_status = models.CharField(
        max_length=30, choices=OrderStatus.choices, default=OrderStatus.INITIATED
    )
    cancel_reason = models.TextField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)

    placed_at = models.DateTimeField(blank=True, null=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    out_for_delivery_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def product(self):
        return self.variant.product

    def save(self, *args, **kwargs):
        if not self.uuid:
            # Example: ORD-2025-000123
            year = timezone.now().year
            prefix = "ORD"
            # Pad database ID estimate — better to use random unique portion before first save
            unique_num = str(uuid.uuid4().int)[:6]  # shorter unique piece
            self.uuid = f"{prefix}-{year}-{unique_num}"
        super().save(*args, **kwargs)


class ReturnRequest(models.Model):

    class ReturnStatus(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        PICKUP_SCHEDULED = 'PICKUP_SCHEDULED', 'Pickup Scheduled'
        PICKED_UP = 'PICKED_UP', 'Picked Up'
        REFUNDED = 'REFUNDED', 'Refund Completed'

    uuid = models.CharField(max_length=20, blank=True, null=True)
    order_item = models.OneToOneField(
        OrderItems, on_delete=models.CASCADE, related_name="return_request"
    )

    pickup_address = models.ForeignKey(Address, on_delete=models.PROTECT)
    pickup_date = models.DateField(blank=True, null=True)

    reason = models.CharField(max_length=255)
    comments = models.TextField()

    product_image1 = models.URLField(null=True, blank=True)
    product_image2 = models.URLField(null=True, blank=True)
    product_image3 = models.URLField(null=True, blank=True)

    status = models.CharField(
        max_length=30, choices=ReturnStatus.choices, default=ReturnStatus.REQUESTED
    )
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # what user paid on purchase
    refunded_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    stock_updated = models.BooleanField(default=False)

    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    pickedup_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    pickup_scheduled_on = models.DateTimeField(
        null=True, blank=True
    )  # The date the pickup was scheduled
    pickup_scheduled_for = models.DateTimeField(
        null=True, blank=True
    )  # The date the pickup is planned to happen

    request_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def order(self):
        return self.order_item.order

    @property
    def product(self):
        return self.order_item.variant.product

    @property
    def variant(self):
        return self.order_item.variant

    def save(self, *args, **kwargs):
        if not self.uuid:
            year = timezone.now().year
            prefix = "RTN"
            unique_num = str(uuid.uuid4().int)[:6]  # shorter unique piece
            self.uuid = f"{prefix}-{year}-{unique_num}"
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['product', 'user']
