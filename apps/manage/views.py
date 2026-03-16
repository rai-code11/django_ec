from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from apps.product.models import Product
from apps.order.models import Checkout, Payment, LineItem
from .forms import ProductCreateForm
from django.urls import reverse_lazy


# 商品の一覧ページを表示するView
class List(ListView):
    model = Product
    context_object_name = "list"
    template_name = "control/list.html"


# 商品新規追加するView
class Create(CreateView):
    model = Product
    template_name = "control/form.html"
    form_class = ProductCreateForm
    success_url = "/manage/products/list/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_type"] = "create"
        return context


# 商品の編集をするView
class Update(UpdateView):
    model = Product
    # fields = "__all__"  # form_classを使う場合は使えない
    template_name = "control/form.html"
    form_class = ProductCreateForm

    success_url = "/manage/products/list/"

    # formのタイトル表示を切り替えるようのメソッド
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["view_type"] = "update"
        return context


# 商品の削除をするView
class Delete(DeleteView):
    model = Product
    template_name = "control/delete.html"

    success_url = reverse_lazy("manage:list")


# 購入者リストを一覧表示するView(ID,購入者,合計金額,注文日時)
class CustomerList(ListView):
    model = Checkout
    context_object_name = "customer"
    template_name = "control/customer_list.html"


# 購入者の詳細情報を表示するView
# Checkout=注文情報(氏名・住所・合計など), Payment=クレカ決済情報, LineItem=注文明細
class CustomerDetails(DetailView):
    model = Checkout
    pk_url_kwarg = "customer_id"
    template_name = "control/customer_details.html"
    # テンプレートでは「注文1件」として order で参照
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_order = self.get_object()  # 表示中の Checkout（注文）インスタンス
        # この注文に紐づく明細行
        context["order_line_items"] = LineItem.objects.filter(checkout=current_order)
        # この注文に紐づくクレジットカード決済情報
        context["card_payment"] = Payment.objects.get(checkout=current_order)
        return context
