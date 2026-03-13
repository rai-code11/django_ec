from .models import Cart, CartItem, Icon
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from .utils import _ensure_cart_session
from django.db.models import F
from apps.promo_code.models import PromoCode


# カートの中身を追加、更新するView
class AddToCartView(View):

    # Formから送信された情報を受け取るためにpostメソッドを定義
    def post(self, request, product_id):
        # 送信された数量を取得し、数値が送信されたらそれを使い、送信されなければ1を使う
        quantity = int(request.POST.get("quantity", 1))

        # セッションIDを取得する
        session_key = _ensure_cart_session(request)
        # セッションIDからカートを特定。なければそのセッションIDを使ってCartレコードを作成する。
        cart_obj, _ = Cart.objects.get_or_create(session_id=session_key)

        # 指定したカートに商品が既に入っていればレコードを取得し、なければ新しくCartItemを作る。
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart_obj, product_id=product_id, defaults={"quantity": quantity}
        )

        # 新しく生成されなかった場合、
        if not item_created:
            CartItem.objects.filter(id=cart_item.id).update(
                quantity=F("quantity") + quantity
            )
        # 元いたページにリダイレクトする
        return redirect(request.META.get("HTTP_REFERER"))


# カートの中身を削除するView
class RemoveFromCartView(View):
    def post(self, request, product_id):

        session_key = _ensure_cart_session(request)
        # このカートのセッションを特定する
        cart = Cart.objects.get(session_id=session_key)
        # このセッションのカートに紐づくCartItemを削除する
        item = get_object_or_404(CartItem, product_id=product_id, cart=cart)

        item.delete()

        return redirect(request.META.get("HTTP_REFERER"))


# アイコンを表示するclass
class LogoContextMixin:
    def get_icon(self):
        return Icon.objects.only("image").first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["icon"] = self.get_icon()
        return context


# カートページ用のコンテキストを提供するMixin（cart/cart.html 用）
class CartContextMixin:
    def get_cart_obj(self):
        session_key = _ensure_cart_session(self.request)
        cart_obj, _ = Cart.objects.get_or_create(session_id=session_key)
        return cart_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj = self.get_cart_obj()
        context["cart"] = cart_obj
        context["cart_items_with_subtotals"] = (
            cart_obj.get_items_with_subtotals()
        )
        total_price = cart_obj.calculate_total_price()
        context["total_price"] = total_price
        context["cart_total_quantity"] = cart_obj.calculate_total_quantity()

        # セッションにプロモ適用済みなら割引後合計を context に追加（表示は cart の責務）
        promo_id = self.request.session.get("promo_id")
        if promo_id:
            promo = get_object_or_404(PromoCode, id=promo_id)
            context["promo"] = promo
            context["discounted_total"] = promo.get_discount_amount(
                total_price
            )
        return context


# カートの中身を表示するView
class CartDetailView(LogoContextMixin, CartContextMixin, TemplateView):
    template_name = "cart/cart.html"
