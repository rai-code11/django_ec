from .utils import _ensure_cart_session
from .models import Cart


def cart_context_processor(request):
    session_key = _ensure_cart_session(request)

    try:
        cart_obj = Cart.objects.get(session_id=session_key)
        total_quantity = cart_obj.calculate_cart_total_quantity()

        return {"cart_total_quantity": total_quantity}

    except Cart.DoesNotExist:
        return {"cart_total_quantity": 0}
