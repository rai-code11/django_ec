from django.views.generic import FormView
from .forms import PromoForm
from apps.cart.models import Cart
from django.contrib import messages
from apps.cart.utils import _ensure_cart_session
from apps.cart.views import LogoContextMixin


# フォームメソッドやモデルメソッドを使いプロモ処理する
class PromoCodeDiscountView(LogoContextMixin, FormView):
    template_name = "cart/cart.html"
    form_class = PromoForm

    # カートを特定しその中身を取得するメソッド
    def get_cart_obj(self):
        session_key = _ensure_cart_session(self.request)
        return Cart.objects.get(session_id=session_key)

    # カート系のコンテキストを全部まとめるメソッド
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_obj = self.get_cart_obj()
        context["cart_items"] = cart_obj.get_items()
        context["cart_total_quantity"] = cart_obj.calculate_total_quantity()
        context["total_price"] = cart_obj.calculate_total_price()
        return context

    # Formバリデーションを通過した際に処理するメソッド
    def form_valid(self, form):
        """
        ①ユーザーが入力したプロモコードが英数字7桁であるかをチェックする(promo_code/forms.py)
        ②そのコードがDBにあるか確認(promo_code/forms.py)
        ③あれば合計金額から割引をする(promo_code/models.py)
        ④割引が完了したらis_usedをTrueに変更して使用済みにする(promo_code/models.py)
        """
        # 今のユーザーのカートを取得
        cart_obj = self.get_cart_obj()

        # 元の合計金額を計算する
        total_amount = cart_obj.calculate_total_price()

        # フォーム側で保持しておいた PromoCode インスタンスを取得する
        promo = form.promo

        # 割引適用後の合計を計算する
        discounted_total = promo.get_discount_amount(total_amount)

        # 決済処理でプロモコードを特定できるようにセッションにidを渡す
        self.request.session["promo_id"] = promo.id

        # プロモコード適応メッセを表示する
        messages.success(self.request, "プロモコードが適応されました。")

        # テンプレでdiscounted_totalを使うためにget_context_dataに渡す
        # discountもつけるようにしておく

        context = self.get_context_data(form=form)
        context["promo"] = promo
        context["discounted_total"] = discounted_total

        return self.render_to_response(context)

    # バリデーション失敗処理を書く
    def form_invalid(self, form):
        messages.error(self.request, "プロモコードが無効です。")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
