
# Django EC Site

Djangoで作ったECサイトです。  
商品を見て、カートに入れて、購入（チェックアウト）までできるようにしています。

本アプリは **Docker（docker compose）** を使って開発・起動できます。

---

## 機能

### 購入者側
- 商品一覧を見る
- 商品詳細を見る
- カートに商品を追加する（数量も増やせる）
- カートから商品を削除する
- 注文フォームを入力して購入する
- プロモーションコードを入れて割引できる（使えるのは1回だけ）

### 管理者側（Basic認証つき）
- 商品の管理（一覧 / 作成 / 編集 / 削除）
- 購入明細（注文履歴）の一覧 / 詳細を見る  
  ※商品を消しても、購入時点の情報は残るようにしています

---

## 使った技術
- Backend: Django
- DB: PostgreSQL
- UI: Bootstrap
- image:cloudinary
- Container: Docker / Docker Compose
- Deploy: Heroku

---

## 動かし方（ローカル / Docker）

### 1) クローンして移動
```bash
git clone <your-repo-url>
cd django_ec
````

### 2) 環境変数を用意

プロジェクト直下に `.env` を作成し、以下を記載します。

* `SECRET_KEY` は自身で生成してください
  参考: [https://noauto-nolife.com/post/django-secret-key-regenerate/](https://noauto-nolife.com/post/django-secret-key-regenerate/)

```env
DATABASE_URL="postgres://postgres:postgres@db:5432/django_develop"
SECRET_KEY="ここに生成したSECRET_KEYを入れる"
```

※ `DEBUG` など他の環境変数が必要な場合は、プロジェクトの設定に合わせて追記してください。

### 3) Dockerを立ち上げる

```bash
docker compose up --build
```

### 4) DBの準備

別ターミナルで以下を実行します。

```bash
docker compose exec web python manage.py migrate
```

### 5) 商品データを入れる（seed）

```bash
docker compose exec web python manage.py loaddata test-data.json
```

### 6) ブラウザで開く

* [http://localhost:3000/products/](http://localhost:3000/products/)

---

## 停止方法

```bash
docker compose down
```

DBも含めて完全に消したい場合

```bash
docker compose down -v
```

---

## 管理者ページ（商品管理 / 購入明細）

Djangoの標準の `/admin` とは別に、管理者用ページを作っています。

・管理者用、商品情報詳細ページ

/manage/products/list/

・管理者用、購入者と商品

/manage/products/customer/

このページは **Basic認証** で守っています。

---

## カートの仕様

* カートは「ブラウザごと」に別になります
  例：ChromeとFirefoxで開くと、別々のカートになります
* 一覧ページで「Add to cart」を押すと数量+1
* 詳細ページでは入力した数量を追加できます
* カート内の商品の削除ができます

---

## 購入（チェックアウト）の仕様

* 購入フォームの内容はDBに保存します
* サンプルなので **クレジットカード情報もDBに保存**します
  ※本当の実務ではStripeなどを使い、カード番号はDBに保存しません
* 購入完了後は「購入ありがとうございます」のメッセージが出て、商品一覧に戻ります
* 購入完了時に、購入明細をメール送信します（Herokuの仕組みを利用）

---

## プロモーションコード（割引）の仕様

* 7桁の英数字（例：`A1B2C3D`）
* 割引額は 100〜1000円
* 1回だけ使用可能
* 1回の購入につき、使えるコードは1つだけ

### コード生成コマンド

```bash
docker compose exec web python manage.py promotion_code_generate
```

* 1回で10個作成します
