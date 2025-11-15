# セッションIDを使ってカートを管理する関数
def _ensure_cart_session(request):
    if request.session.session_key is None:
        request.session.save()
    return request.session.session_key
