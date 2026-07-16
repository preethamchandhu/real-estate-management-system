from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import role_required
from .models import Property
from .forms import PropertyForm, PropertyDocumentForm, PropertySearchForm
from . import mongo


def property_list(request):
    properties = Property.objects.filter(status='available')
    form = PropertySearchForm(request.GET or None)

    if form.is_valid():
        city = form.cleaned_data.get('city')
        listing_type = form.cleaned_data.get('listing_type')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        bedrooms = form.cleaned_data.get('bedrooms')

        if city:
            properties = properties.filter(city__icontains=city)
        if listing_type:
            properties = properties.filter(listing_type=listing_type)
        if min_price is not None:
            properties = properties.filter(price__gte=min_price)
        if max_price is not None:
            properties = properties.filter(price__lte=max_price)
        if bedrooms is not None:
            properties = properties.filter(bedrooms__gte=bedrooms)

    return render(request, 'properties/property_list.html', {
        'properties': properties,
        'form': form,
    })


def property_detail(request, pk):
    prop = get_object_or_404(Property, pk=pk)

    documents = []
    activity = []
    try:
        documents = mongo.get_documents(prop.id)
        if request.user.is_authenticated:
            mongo.log_activity(prop.id, 'viewed', request.user.username)
        activity = mongo.get_activity_for_property(prop.id)
    except Exception:
        # MongoDB not reachable - page still works, just without doc/activity data
        pass

    return render(request, 'properties/property_detail.html', {
        'property': prop,
        'documents': documents,
        'activity': activity,
    })


@role_required('agent')
def agent_property_list(request):
    properties = Property.objects.filter(agent=request.user)
    return render(request, 'properties/agent_property_list.html', {'properties': properties})


@role_required('agent')
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.agent = request.user
            prop.save()
            messages.success(request, "Property listed successfully.")
            return redirect('properties:detail', pk=prop.pk)
    else:
        form = PropertyForm()
    return render(request, 'properties/property_form.html', {'form': form, 'mode': 'Add'})


@role_required('agent')
def property_update(request, pk):
    prop = get_object_or_404(Property, pk=pk, agent=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated.")
            return redirect('properties:detail', pk=prop.pk)
    else:
        form = PropertyForm(instance=prop)
    return render(request, 'properties/property_form.html', {'form': form, 'mode': 'Edit'})


@role_required('agent')
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk, agent=request.user)
    if request.method == 'POST':
        prop.delete()
        messages.success(request, "Property deleted.")
        return redirect('properties:agent_list')
    return render(request, 'properties/property_confirm_delete.html', {'property': prop})


@role_required('agent')
def property_add_document(request, pk):
    prop = get_object_or_404(Property, pk=pk, agent=request.user)
    if request.method == 'POST':
        form = PropertyDocumentForm(request.POST)
        if form.is_valid():
            try:
                mongo.add_document(prop.id, form.cleaned_data['title'], form.cleaned_data['description'])
                messages.success(request, "Document added.")
            except Exception:
                messages.error(request, "Could not reach MongoDB. Is it running?")
            return redirect('properties:detail', pk=prop.pk)
    else:
        form = PropertyDocumentForm()
    return render(request, 'properties/property_document_form.html', {'form': form, 'property': prop})
