from django.core.mail import send_mail
from textwrap import dedent
from django.conf import settings


def send_email_settings(checkout, cart_items, promocode=None):

    full_name = f"{checkout.last_name} {checkout.first_name}"

    lines = []
    for item in cart_items:
        lines.append(
            f"商品名：{item.product.name}\n商品コード：{item.product.code}\n数量：{checkout.total_quantity}\n小計：{item.product.price * item.quantity}"
        )

    products_text = "\n".join(lines)

    message = dedent(
        f"""ご注文ありがとうございます
─────────────────────

{full_name}様

ご注文いただきまして誠にありがとうございます。
ご注文内容は下記のとおりです。ご確認下さいますようお願い致します。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ご注文内容
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
注文番号：{checkout.id}
注文日時：{checkout.created_at}
お名前：{full_name}
お支払い方法：クレジットカード
お支払い金額：{checkout.total_amount}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
商品お届け先
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
お届け先住所へ宅配
お届け先：
〒{checkout.zip_code}
{checkout.full_address}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ご注文商品
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{products_text}
=======================================
クーポン割引：\\ {promocode.discount}
お支払い金額：\\ {checkout.total_amount}

"""
    )

    send_mail(
        subject="ご注文ありがとうございます",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[checkout.email],
    )
