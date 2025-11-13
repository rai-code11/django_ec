from .models import CartItem


# セッションIDを使ってカートを管理する関数
def _ensure_cart_session(request):
    if request.session.session_key is None:
        request.session.save()
    return request.session.session_key


# カート内の合計数量を計算する関数
def calculate_cart_total_quantity(cart_obj):
    cart_items = CartItem.objects.filter(cart=cart_obj)
    total_quantity = sum(item.quantity for item in cart_items)

    return total_quantity
