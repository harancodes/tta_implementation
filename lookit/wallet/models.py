from django.db import models
from user.models import User
from django.utils import timezone
from django.utils.timezone import localtime
from order.models import OrderItems, Order

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class WalletTransactions(models.Model):
    
    class TransactionType(models.TextChoices):
        CREDIT = 'credit'
        DEBIT = 'debit'
        
    class TransactionSource(models.TextChoices):
        REWARD = 'reward'
        ONLINE = 'online'
        SHOPPING = 'shopping'
        REFUND = 'refund'
        
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True) #only for payment using wallet transaction on order
    order_item = models.ForeignKey(OrderItems, on_delete=models.CASCADE, null=True, blank=True) #only for transaction related to order refund
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=30, choices=TransactionType.choices) #credit or debit
    label = models.CharField(max_length=100) 
    txn_source = models.CharField(max_length=100, choices=TransactionSource.choices)  #from where the money came or where it gone
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #format created date into a custom format
    def formatted_created_at(self):
        now = localtime(timezone.now()).date()
        date = localtime(self.created_at).date()
        time_str = localtime(self.created_at).strftime("%I:%M %p").lstrip('0')

        if date == now:
            return f"Today, {time_str}"
        elif (now - date).days == 1:
            return f"Yesterday, {time_str}"
        else:
            return localtime(self.created_at).strftime("%b %d, %I:%M %p")
