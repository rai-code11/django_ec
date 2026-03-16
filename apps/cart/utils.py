# セッションIDを使ってカートを管理する関数
def _ensure_cart_session(request):
    """
    カート用に、必ず有効なセッションIDを返すヘルパー関数
    まだセッションが作られていなければここで作成する
    """
    if request.session.session_key is None:
        request.session.create()
    return request.session.session_key
