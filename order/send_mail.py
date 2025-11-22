from django.core.mail import send_mail
from textwrap import dedent


def send_email_settings(checkout, cart_items):

    full_name = f"{checkout.last_name} {checkout.first_name}"

    lines = []
    for item in cart_items:
        lines.append(
            f"商品名：{item.product.name}\n商品コード：{item.code}\n数量：{total_quanttity}\n小計：{item.product.price * item.quantity}"
        )

    products_text = "\n".join(lines)

    message = (
        dedent(
            f"""ご注文ありがとうございます
─────────────────────

{full_name}様

予約商品をご注文いただきまして誠にありがとうございます。
ご注文内容は下記のとおりです。ご確認下さいますようお願い致します。

なお、ご予約注文につきまして、商品入荷前におきましても、
カラーサイズ変更はお受けしておりません。
予めご了承下さいます様お願いいたします。

ご予約商品が入荷しましたら、
メールにてご連絡致しますので、今しばらくお待ちください。

商品入荷お知らせの際に、お支払い方法、受取先情報、配送希望日時をご変更いただけます。

※※入荷時のご注意※※
ご注文時にクレジットカード決済された場合でも、与信枠の関係で入荷時に決済方法が代引きに変更されている場合がございます。
入荷通知メール受信の際には必ずご確認ください。
上記の場合、他クレジットカードでの再登録、または他決済方法をお選びください。

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
商品合計金額：\\ {checkout.total_amount}
クーポン割引：\\ 0
お支払い金額：\\ {checkout.total_amount}

"""
        ),
    )

    send_mail(
        subject="ご注文ありがとうございます",
        message=message,
        from_email="settings.DEFAULT_FROM_EMAIL",
        recipient_list=[checkout.email],
    )
