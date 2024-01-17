from django import forms
from userorder.models import shipping_address


class Shipping_adress_Form(forms.ModelForm):
    class Meta:
        model = shipping_address
        fields = [
            "first_name",
            "second_name",
            "address",
            "postal_code",
            "state",
            "phone",
            "country",
            "district",
        ]
