from django.views import View
from .models import Checkout, Payment
from django.contrib import messages
from django.shortcuts import redirect


# DBに請求情報とクレジットカード情報を保存するView
class Order(View):
    def post(self, request):
        print(request.POST)
        # フォームから請求情報を取得してDBに保存
        # 請求情報をCheckoutモデルに格納し、決済情報のインスタンスを作成して保存する
        checkout = Checkout(
            last_name=request.POST["last_name"],
            first_name=request.POST["first_name"],
            user_name=request.POST["user_name"],
            email=request.POST["email"],
            zip_code=request.POST["zip_code"],
            prefecture=request.POST["prefecture"],
            city=request.POST["city"],
            street_address=request.POST["street_address"],
            building_name=request.POST["building_name"],
        )
        checkout.save()

        # フォームからクレジットカード情報を取得してDBに保存
        payment = Payment(
            checkout=checkout,
            card_holder=request.POST["card_holder"],
            card_number=request.POST["card_number"],
            expiration_date=request.POST["expiration_date"],
            cvv=request.POST["cvv"],
        )
        payment.save()

        # サクセスメッセージを表示する
        messages.success(request, "購入ありがとうございます")

        return redirect("product:product_list")
