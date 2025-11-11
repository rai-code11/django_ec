from django.conf import settings
from products.models import Product


cart_session_id = "cart"


class Cart:
    def __init__(self, reauest):
        self.session = request.session
