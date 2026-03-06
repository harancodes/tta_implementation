from wallet.models import Wallet, WalletTransactions
from decimal import Decimal

def refund_to_wallet(user, refund_amount, order_item):
    if user and refund_amount:
        wallet = Wallet.objects.get(user=user)

        WalletTransactions.objects.create(
            wallet=wallet,
            amount=refund_amount,
            order_item=order_item,
            transaction_type=WalletTransactions.TransactionType.CREDIT,
            txn_source=WalletTransactions.TransactionSource.REFUND,
            label="Refund – Order Cancelled/Returned"
        )
        
        wallet.balance += Decimal(refund_amount)
        wallet.save()
