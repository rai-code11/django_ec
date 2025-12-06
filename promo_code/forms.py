from django import forms
from .models import PromoCode


class PromoForm(forms.Form):
    # プロモバリデーション
    promo_code = forms.CharField(max_length=7)

    # ユーザーが入力する時のバリデーションを記述する(フィールド単位のバリデーションは clean_フィールド名 で書く)
    def clean_promo_code(self):
        data = self.cleaned_data

        promo_code = data["promo_code"]

        # ユーザーが入力したプロモコードがDBにあるかを確認してなければエラーを出す。
        try:
            promo = PromoCode.objects.get(promo_code=promo_code)
        except PromoCode.DoesNotExist:
            raise forms.ValidationError("このプロモコードは存在しません。")

        # もしis_usedがTrue(使用済み)であればエラーを出す
        if promo.is_used:
            raise forms.ValidationError("このプロモコードは既に使用されています。")

        # viewsでインスタンスを使うために定義しておく
        self.promo = promo

        return promo_code
