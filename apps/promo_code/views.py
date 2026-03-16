from django.views.generic import FormView
from .forms import PromoForm
from django.contrib import messages
from apps.cart.views import LogoContextMixin, CartContextMixin


# フォームメソッドやモデルメソッドを使いプロモ処理する
# カート表示用コンテキストは CartContextMixin（cartアプリ）に委譲
class PromoCodeDiscountView(LogoContextMixin, CartContextMixin, FormView):
    template_name = "cart/cart.html"
    form_class = PromoForm

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

        # フォーム側で保持しておいた PromoCode インスタンスを取得する
        promo = form.promo

        # 同一決済で既に適用済みのプロモコードかチェック
        if self.request.session.get("promo_id") == promo.id:
            messages.error(self.request, "すでに適応済みのプロモコードです。")
            return self.render_to_response(self.get_context_data(form=form))

        # 決済処理でプロモコードを特定できるようにセッションにidを渡す
        self.request.session["promo_id"] = promo.id
        messages.success(self.request, "プロモコードが適応されました。")
        # 割引後表示は CartContextMixin が session の promo_id を見て context に載せる
        return self.render_to_response(self.get_context_data(form=form))

    # バリデーション失敗処理を書く
    def form_invalid(self, form):
        messages.error(self.request, "プロモコードが無効です。")
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
