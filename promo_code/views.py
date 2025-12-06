from django.views.generic import FormView
from .forms import PromoForm
from .models import PromoCode
from checkout.models import Cart
from django.contrib import messages
from checkout.utils import _ensure_cart_session
from checkout.views import LogoContextMixin


# フォームメソッドやモデルメソッドを使いプロモ処理する
class PromoCodeDiscountView(LogoContextMixin, FormView):
    template_name = "checkout/checkout.html"
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

        # プロモコードを使用済みにするメソッドを呼ぶ
        promo.mark_used()

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

    # 下記のコードだとバリデーション前と後で同じように変数を定義しないといけなくなり冗長になってしまうため処理をまとめる
    # def form_valid(self, form):
    #     """
    #     ①ユーザーが入力したプロモコードが英数字7桁であるかをチェックする(promo_code/forms.py)
    #     ②そのコードがDBにあるか確認(promo_code/forms.py)
    #     ③あれば合計金額から割引をする(promo_code/models.py)
    #     ④割引が完了したらis_usedをTrueに変更して使用済みにする(promo_code/models.py)
    #     """
    #     # 今のユーザーのカートを取得
    #     session_key = _ensure_cart_session(self.request)
    #     cart_obj = Cart.objects.get(session_id=session_key)

    #     # 元の合計金額を計算する
    #     total_amount = cart_obj.calculate_total_price()

    #     # フォーム側で保持しておいた PromoCode インスタンスを取得する
    #     promo = form.promo

    #     # 割引適用後の合計を計算する
    #     discounted_total = promo.get_discount_amount(total_amount)

    #     # プロモコードを使用済みにするメソッドを呼ぶ
    #     promo.mark_used()

    #     # プロモコード適応メッセを表示する
    #     messages.success(self.request, "プロモコードが適応されました。")

    #     session_key = _ensure_cart_session(self.request)
    #     # セッションIDを使ってカートオボジェクトを取得する。なければ新規作成する

    #     cart_items = cart_obj.get_items()

    #     # テンプレでdiscounted_totalを使うためにget_context_dataに渡す
    #     # discountもつけるようにしておく

    #     context = self.get_context_data(
    #         form=form,
    #         promo=promo,
    #         cart_items=cart_items,
    #         total_price=total_amount,
    #         discounted_total=discounted_total,
    #     )
    #     return self.render_to_response(context)

    #     # return self.render_to_response(
    #     #     self.get_context_data(form=form, discounted_total=discounted_total)
    #     # )

    # # バリデーション失敗処理を書く
    # def form_invalid(self, form):
    #     messages.error(self.request, "プロモコードが無効です。")
    #     return self.render_to_response(self.get_context_data(form=form))
