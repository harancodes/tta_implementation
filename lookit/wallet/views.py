from django.shortcuts import render
from .models import Wallet, WalletTransactions
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Case, DecimalField, When, F, Value
from django.db.models.functions import Coalesce


# Create your views here.
@login_required
def wallet(request):
    # ---get wallet details, if no wallet for user create one--------
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = WalletTransactions.objects.filter(wallet=wallet).order_by(
        '-created_at'
    )
    transaction_summary = transactions.aggregate(
        total_credit=Coalesce(
            Sum(
                Case(
                    When(transaction_type='credit', then=F('amount')),
                    default=Value(0),
                    output_field=DecimalField(),
                )
            ),
            Value(0),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        ),
        total_debit=Coalesce(
            Sum(
                Case(
                    When(transaction_type='debit', then=F('amount')),
                    default=Value(0),
                    output_field=DecimalField(),
                )
            ),
            Value(0),
            output_field=DecimalField(max_digits=10, decimal_places=2),
        ),
    )
    print(transaction_summary['total_credit'])
    return render(
        request,
        "wallet/wallet.html",
        {
            "wallet": wallet,
            'transactions': transactions,
            'summary': transaction_summary,
        },
    )


def wallet_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance -= amount
        wallet.save()
