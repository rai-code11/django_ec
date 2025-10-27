from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import ProductList, ProductDetails

# Create your views here.


class ProductDetailsView(DetailView):
    # self.objectがアクセスするモデル
    model = ProductList
    # templatesを指定
    template_name = "product_details/product_details.html"
    # templatesにてproduct_listのデータをproduct_listという変数で使えるように指定
    context_object_name = "product_list"

    # データを取得する処理は、親クラス（DetailView）の内部ですでに終わっていて、その結果をここで受け取っている
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # self.objectはProductListオブジェクト
        # .productdetailsでOneToOneFieldで紐づくProductDetailsを辞書contextに追加
        context["product_details"] = self.object.productdetails

        # created_atの日付が新しい順に新しい順にデータを取得する
        # 表示されている商品だけを除く
        main_product_id = self.object.id
        # main商品以外の商品からcreated_at順に商品を上から並べる
        related_products = (
            ProductList.objects.exclude(id=main_product_id)
            .select_related("productdetails")
            .order_by("-productdetails__created_at")[:4]
        )
        # templatesで使えるように辞書contextを追加
        context["related_products"] = related_products

        return context
