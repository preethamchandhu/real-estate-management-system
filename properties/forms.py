from django import forms
from .models import Property


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'listing_type', 'status', 'price',
            'address', 'city', 'bedrooms', 'bathrooms', 'area_sqft', 'image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class PropertyDocumentForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)


class PropertySearchForm(forms.Form):
    city = forms.CharField(required=False)
    listing_type = forms.ChoiceField(choices=(('', 'Any'),) + Property.LISTING_TYPE, required=False)
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    bedrooms = forms.IntegerField(required=False)
