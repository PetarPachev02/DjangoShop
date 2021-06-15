from django import forms
from .models import OrderLine

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class cartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
                                