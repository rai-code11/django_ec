from django.views.generic import FormView
from .models import Checkout, Payment, LineItem
from checkout.models import Cart
from django.contrib import messages
from django.db import transaction
from .forms import OrderForm
from django.urls import reverse_lazy
from checkout.utils import _ensure_cart_session
from .send_mail import send_email_settings
from promo_code.models import PromoCode


# DBに請求情報とクレジットカード情報を保存するView
class Order(FormView):
    template_name = "checkout/checkout.html"
    form_class = OrderForm
    success_url = reverse_lazy("product:product_list")

    # トランザクション処理にする
    @transaction.atomic
    def form_valid(self, form):

        # form_validは引数にrequestを取らないのselfから取得する
        session_key = _ensure_cart_session(self.request)
        cart_obj = Cart.objects.get(session_id=session_key)

        # 合計金額と合計個数とカートのアイテムを取り出すためにCartのインスタンスに対してメソッドを呼ぶ
        total_amount = cart_obj.calculate_total_price()
        total_quantity = cart_obj.calculate_total_quantity()
        cart_items = cart_obj.get_items()

        # セッションからpromo_idを取り出す
        promo = None
        promo_id = self.request.session.get("promo_id")

        if promo_id is not None:
            try:
                promo = PromoCode.objects.get(pk=promo_id)
                # 割引を適用した合計金額に更新
                total_amount = promo.get_discount_amount(total_amount)
            except PromoCode.DoesNotExist:
                # プロモが消えていた場合は何もしないで通常金額で進める
                promo = None

        # formsで定義したバリデーションを突破した情報をdataに格納する
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
            total_amount=total_amount,
            total_quantity=total_quantity,
        )

        # 決済情報をPaymentモデルに保存
        payment = Payment.objects.create(
            checkout=checkout,
            card_holder=data["card_holder"],
            card_number=data["card_number"],  # 本来はDBに保存しない
            expiration_date=data["expiration_date"],
            cvv=data["cvv"],  # 本来はDBに保存しない
        )

        # LineItemに決済情報・クレカ情報・カートアイテム情報を保存する
        # カートインスタンスを取得する
        # LineItemへ保存をするためにカートアイテムインスタンスを取得する
        for item in cart_items:
            LineItem.objects.create(
                checkout=checkout,
                name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
                subtotal_amount=item.product.price * item.quantity,
            )

        # クーポン側と紐づける
        if promo is not None:
            promo.mark_used(checkout)
            del self.request.session["promo_id"]

        # メールを送信するメソッドを呼び出す
        send_email_settings(checkout, cart_items, promo)

        # カートを削除するメソッドを呼び出す
        cart_obj.clear()

        messages.success(self.request, "購入ありがとうございます")

        return super().form_valid(form)
