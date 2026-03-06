from django.contrib import messages
from .models import User
from wallet.models import Wallet, WalletTransactions
from decimal import Decimal
from django.db import transaction


def validate_referral_code(request, code):
    try:
        is_valid = User.objects.filter(referral_code=code).exists()
        if not is_valid:
            return None
        referred_user = User.objects.get(referral_code=code)
        return referred_user
    except Exception as e:
        print("Error: ", e)
        messages.error(request, "Something went wrong")


# new user gets 50rs to wallet and referrer will get 100rs to wallet
def give_referral_reward(new_user, referrer):
    referrer_reward = Decimal(100)
    new_user_reward = Decimal(50)

    with transaction.atomic():
        new_user_wallet = Wallet.objects.get(user=new_user)
        referrer_wallet = Wallet.objects.get(user=referrer)

        #create wallet transaction for new user
        WalletTransactions.objects.create(
            wallet=new_user_wallet,
            amount=new_user_reward,
            transaction_type=WalletTransactions.TransactionType.CREDIT,
            txn_source = WalletTransactions.TransactionSource.REWARD,
            label = "Referral signup reward"
        )
        
        new_user_wallet.balance += new_user_reward 
        new_user_wallet.save()
        
        #create wallet transaction for referrer
        WalletTransactions.objects.create(
            wallet=referrer_wallet,
            amount=referrer_reward,
            transaction_type=WalletTransactions.TransactionType.CREDIT,
            txn_source = WalletTransactions.TransactionSource.REWARD,
            label = "Referral Reward Earned"
        )
        
        referrer_wallet.balance += referrer_reward
        referrer_wallet.save()
