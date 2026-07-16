from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import role_required
from properties.models import Property
from properties import mongo
from .models import Transaction
from .forms import TransactionRequestForm


@role_required('client')
def request_transaction(request, property_id):
    prop = get_object_or_404(Property, pk=property_id)

    if request.method == 'POST':
        form = TransactionRequestForm(request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.property = prop
            txn.client = request.user
            txn.save()

            prop.status = 'pending'
            prop.save(update_fields=['status'])

            try:
                mongo.log_activity(prop.id, 'transaction_requested', request.user.username,
                                    {'transaction_type': txn.transaction_type, 'amount': str(txn.amount)})
            except Exception:
                pass

            messages.success(request, "Your request has been sent to the agent.")
            return redirect('transactions:my_transactions')
    else:
        initial = {'amount': prop.price}
        form = TransactionRequestForm(initial=initial)

    return render(request, 'transactions/transaction_form.html', {'form': form, 'property': prop})


@role_required('client')
def my_transactions(request):
    txns = Transaction.objects.filter(client=request.user).select_related('property')
    return render(request, 'transactions/my_transactions.html', {'transactions': txns})


@role_required('agent')
def agent_transactions(request):
    txns = Transaction.objects.filter(property__agent=request.user).select_related('property', 'client')
    return render(request, 'transactions/agent_transactions.html', {'transactions': txns})


@role_required('agent')
def update_transaction_status(request, pk, new_status):
    txn = get_object_or_404(Transaction, pk=pk, property__agent=request.user)
    if new_status not in dict(Transaction.STATUS_CHOICES):
        messages.error(request, "Invalid status.")
        return redirect('transactions:agent_transactions')

    txn.status = new_status
    txn.save(update_fields=['status'])

    if new_status == 'approved':
        txn.property.status = 'sold' if txn.transaction_type == 'buy' else 'rented'
        txn.property.save(update_fields=['status'])
    elif new_status == 'rejected':
        txn.property.status = 'available'
        txn.property.save(update_fields=['status'])

    try:
        mongo.log_activity(txn.property.id, f'transaction_{new_status}', request.user.username)
    except Exception:
        pass

    messages.success(request, f"Transaction marked as {new_status}.")
    return redirect('transactions:agent_transactions')
