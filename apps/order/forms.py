from django import forms


class OrderForm(forms.Form):
    # 決済情報
    last_name = forms.CharField(max_length=50)
    first_name = forms.CharField(max_length=50)
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    zip_code = forms.CharField(max_length=50)
    prefecture = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    street_address = forms.CharField(max_length=50)
    building_name = forms.CharField(max_length=50)

    # クレジットカード情報
    card_holder = forms.CharField(max_length=100)
    card_number = forms.CharField(max_length=50, min_length=16)
    expiration_date = forms.CharField(max_length=20)
    cvv = forms.CharField(max_length=4, min_length=3)


# あとでもっと厳しい制約をつける
