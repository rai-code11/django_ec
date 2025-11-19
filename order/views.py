from django.views.generic import FormView
from .models import Checkout, Payment
from checkout.models import Cart
from django.contrib import messages
from django.db import transaction
from .forms import OrderForm
from django.urls import reverse_lazy


# DBに請求情報とクレジットカード情報を保存するView
class Order(FormView):
    template_name = "checkout/checkout.html"
    form_class = OrderForm
    success_url = reverse_lazy("product:product_list")

    # トランザクション処理にする
    @transaction.atomic
    def form_valid(self, form):
        print("--- DEBUG: form_validが実行されました ---")

        data = form.cleaned_data
        # フォームから請求情報を取得してDBに保存
        # 請求情報をCheckoutモデルに格納し、決済情報のインスタンスを作成して保存する

        checkout = Checkout.objects.create(
            last_name=data["last_name"],
            first_name=data["first_name"],
            user_name=data["user_name"],
            email=data["email"],
            zip_code=data["zip_code"],
            prefecture=data["prefecture"],
            city=data["city"],
            street_address=data["street_address"],
            building_name=data["building_name"],
        )

        # --- 2. 決済情報 (Payment) の保存 ---
        payment = Payment.objects.create(
            checkout=checkout,
            card_holder=data["card_holder"],
            card_number=data["card_number"],  # 本来はトークンを保存
            expiration_date=data["expiration_date"],
            cvv=data["cvv"],  # 本来はトークンを保存
        )

        # 現在のセッションIDを取得してそれに該当するカートを削除する
        current_session_key = self.request.session.session_key
        Cart.objects.clear_by_session(current_session_key)

        messages.success(self.request, "購入ありがとうございます")

        return super().form_valid(form)

    def form_invalid(self, form):
        print("--- DEBUG: form_invalidが実行されました ---")
        print(form.errors)  # どのフィールドがエラーかコンソールに出る
        return super().form_invalid(form)
