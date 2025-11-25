from django import forms
from product.models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["code", "name", "price", "context", "image"]

        widgets = {
            "code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "ABC-XXXXX"}
            ),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "context": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image": forms.TextInput(attrs={"class": "form-control"}),
        }
