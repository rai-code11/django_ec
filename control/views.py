from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from product.models import Product
from order.models import Checkout, Payment, LineItem
from django.urls import reverse_lazy

# Create your views here.


class List(ListView):
    model = Product
    context_object_name = "list"
    template_name = "control/list.html"


class Create(CreateView):
    model = Product
    fields = "__all__"
    template_name = "control/form.html"

    success_url = "/manage/products/list/"


class Update(UpdateView):
    model = Product
    fields = "__all__"
    template_name = "control/form.html"

    success_url = "/manage/products/list/"


class Delete(DeleteView):
    model = Product
    template_name = "control/delete.html"

    success_url = reverse_lazy("manage:list")


# 購入者リストを一覧表示するView(ID,購入者,合計金額,注文日時)
class CustomerList(ListView):
    model = Checkout
    context_object_name = "customer"
    template_name = "control/customer_list.html"


# 購入者の詳細情報を表示するView(注文番号,注文日時,氏名,ユーザー名,メール,郵便番号,住所,カード名義,クレジットカード情報,有効期限,購入商品(商品名,単価,個数,小計,プロモ割引,合計金額))
# DBから商品詳細を取得して表示するView
class CustomerDetails(DetailView):
    # self.objectがアクセスするモデル
    model = Checkout
    # URLから取得するpkの名前を指定
    pk_url_kwarg = "customer_id"
    # templatesを指定
    template_name = "control/customer_details.html"
    # templatesにてproduct_listのデータをproduct_listという変数で使えるように指定
    context_object_name = "customer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_checkout = self.get_object()
        # 1対多
        context["line_items"] = LineItem.objects.filter(checkout=current_checkout)
        # 1対1
        context["payment_info"] = Payment.objects.get(checkout=current_checkout)

        return context
