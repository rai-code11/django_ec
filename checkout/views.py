from .models import Cart, CartItem, Icon
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db.models import F

# Create your views here.


# セッションIDを使ってカートを管理する関数
def _ensure_cart_session(request):
    if request.session.session_key is None:
        request.session.save()
    return request.session.session_key


# カートの中身を追加、更新するView
class AddToCartView(View):

    # セッションIDをrequest.session.session_keyで取得して、もしCartになければ追加する。
    def post(self, request, product_id):
        # Formから送信された数量を取得する
        # 数値が送信されたらそれを使い、送信されなければ1を使う
        try:
            quantity = int(request.POST.get("quantity", 1))
            if quantity <= 0:
                messages.error(request, "数量は１以上を指定してください。")
                return redirect("product:detail", product_id=product_id)
        except (ValueError, TypeError):
            messages.error(request, "数量が不正です。")
            return redirect("product:detail", product_id=product_id)

        # セッションIDを取得する
        session_key = _ensure_cart_session(request)
        # セッションIDからカートを特定。なければ作成する。
        cart_obj, _ = Cart.objects.get_or_create(session_id=session_key)

        # CartItemに商品を追加する。すでにあれば数量を更新する
        cart_item, item_created = CartItem.objects.get_or_create(
            cart_id=cart_obj, product_id=product_id, defaults={"quantity": quantity}
        )

        if not item_created:
            CartItem.objects.filter(pk=cart_item.pk).update(
                quantity=F("quantity") + quantity
            )

        messages.success(request, "カートに商品を追加しました。")
        return redirect(request.META.get("HTTP_REFERER"))


# カートの中身を削除するView
class RemoveFromCartView(View):
    def post(self, request, cart_item_id):

        session_key = _ensure_cart_session(request)
        # このカートのセッションを特定する
        cart = get_object_or_404(Cart, session_id=session_key)
        # このセッションのカートに紐づくCartItemを削除する
        item = get_object_or_404(CartItem, id=cart_item_id, cart=cart)

        item.delete()

        messages.success(request, "カートから商品を削除しました。")
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

    # カートの中身や合計金額,個数を取得してテンプレートに渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # セッションIDを取得する
        session_key = _ensure_cart_session(self.request)
        cart_obj, _ = Cart.objects.get_or_create(session_id=session_key)

        # 商品を結合して取得（N+1回避）
        cart_items = (
            CartItem.objects.filter(cart=cart_obj).select_related("product").all()
        )

        # CartItemの合計個数と合計金額を計算する
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.quantity * item.product.price for item in cart_items)

        # テンプレートで使う変数をセットする
        context["cart_items"] = cart_items
        context["total_quantity"] = total_quantity
        context["total_price"] = total_price

        return context
