from django import forms
from .models import Product
from account.models import Profile

class AddProductForm(forms.Form):
    product_image = forms.ImageField()
    name = forms.CharField(max_length=100)
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows' : 3}))
    price = forms.DecimalField(max_digits = 9, decimal_places=0)
    stock = forms.IntegerField(min_value=1, max_value=100)

class RestockForm(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=100)

class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=0, max_value=5)
    review = forms.CharField(required=False, max_length=500, widget=forms.Textarea(attrs={'rows':3}))