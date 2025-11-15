from .models import Cart, CartItem, Icon
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from .utils import _ensure_cart_session
from django.db.models import F

# Create your views here.


# カートの中身を追加、更新するView
class AddToCartView(View):

    # セッションIDをrequest.session.session_keyで取得して、もしCartになければ追加する。
    def post(self, request, product_id):
        # Formから送信された数量を取得する
        # 数値が送信されたらそれを使い、送信されなければ1を使う
        quantity = int(request.POST.get("quantity", 1))

        # セッションIDを取得する
        session_key = _ensure_cart_session(request)
        # セッションIDからカートを特定。なければそのセッションIDを使ってCartレコードを作成する。
        cart_obj, _ = Cart.objects.get_or_create(session_id=session_key)

        # Cこのカートにこの商品がもう入ってるか確認して、なければ新しくCartItemを作る。あれば既存のCartItemをそのまま返す。
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart_obj, product_id=product_id, defaults={"quantity": quantity}
        )

        if not item_created:
            CartItem.objects.filter(pk=cart_item.pk).update(
                quantity=F("quantity") + quantity
            )

        return redirect(request.META.get("HTTP_REFERER"))


# カートの中身を削除するView
class RemoveFromCartView(View):
    def post(self, request, product_id):

        session_key = _ensure_cart_session(request)
        # このカートのセッションを特定する
        cart = get_object_or_404(Cart, session_id=session_key)
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


# カートの中身を表示するView
class CartDetailView(LogoContextMixin, TemplateView):
    template_name = "checkout/checkout.html"

    # カートの中身や合計金額を取得してテンプレートに渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # セッションIDを取得する
        session_key = _ensure_cart_session(self.request)
        cart_obj, _ = Cart.objects.get_or_create(session_id=session_key)

        # 商品を結合して取得（N+1回避）
        cart_items = (
            CartItem.objects.filter(cart=cart_obj).select_related("product").all()
        )

        # カート内の合計数量を計算するメソッドを呼び出す
        cart_total_quantity = cart_obj.calculate_cart_total_quantity()

        # 各アイテムの小計を計算するメソッド
        for item in cart_items:
            item.subtotal = item.quantity * item.product.price

        # CartItemの合計個数と合計金額を計算する
        total_price = sum(item.quantity * item.product.price for item in cart_items)

        # テンプレートで使う変数をセットする
        context["cart_items"] = cart_items
        context["total_price"] = total_price
        context["cart_total_quantity"] = cart_total_quantity

        return context
