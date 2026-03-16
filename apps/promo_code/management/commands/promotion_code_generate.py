from django.core.management.base import BaseCommand
import secrets
import string


class Command(BaseCommand):
    help = "ランダムな7桁の英数字のプロモーションコードを生成するコマンド"

    def add_arguments(self, parser):
        # オプションや引数を追加
        parser.add_argument("--name", type=str, help="名前を指定します")

    def handle(self, *args, **options):
        # 英数字からランダムに7桁選んだ文字列を作成する処理を10回繰り返してリストに入れる
        code_length = 7
        code_num = 10
        characters = string.ascii_letters + string.digits
        # 不確定性を高めるためにrandomではなくsecretsを使う
        generate_code_list = [
            "".join(secrets.choice(characters) for _ in range(code_length))
            for _ in range(code_num)
        ]
        print(generate_code_list)
