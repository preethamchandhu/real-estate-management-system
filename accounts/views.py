from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import RegisterForm, ProfileUpdateForm
from properties.models import Property
from transactions.models import Transaction


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account was created.")
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


@login_required
def dashboard_view(request):
    user = request.user
    context = {'user': user}

    if user.is_admin_role():
        context['total_users'] = user.__class__.objects.count()
        context['total_properties'] = Property.objects.count()
        context['total_transactions'] = Transaction.objects.count()
        context['recent_transactions'] = Transaction.objects.select_related('property', 'client').order_by('-created_at')[:10]
        template = 'accounts/dashboard_admin.html'
    elif user.is_agent():
        my_properties = Property.objects.filter(agent=user)
        context['my_properties'] = my_properties
        context['property_count'] = my_properties.count()
        context['pending_transactions'] = Transaction.objects.filter(property__agent=user, status='pending')
        template = 'accounts/dashboard_agent.html'
    else:
        context['my_transactions'] = Transaction.objects.filter(client=user).select_related('property').order_by('-created_at')
        template = 'accounts/dashboard_client.html'

    return render(request, template, context)


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})
