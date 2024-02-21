### 提案
## Repl.itでbotを動かすならそれでも良い
## せっかくローカルで動かせる環境があるなら、ngrokもしくはlocaltunnelという
## 選択肢がある。どちらもローカルを外部に公開するもの
## どうせうちはポート解放ができない（ルーター変えればギリできるが）ので、
## こういうのを使ってWebhookを受け取って動かすのが良いのではないかと思う
## その代わり、セキュリティ対策はしっかりやる必要がある（テスト含めて）

import os
from flask import Flask, request, abort
from discord import Webhook
from discord.ext import commands
import aiohttp  # 他にいいライブラリがあるならそっち使う

import sys, asyncio

# バージョンが低いとflaskでasyncioが動かないらしいので対策
if sys.platform == "win32" and (3, 8, 0) <= sys.version_info < (3, 9, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Python3 flask connect discord.py</h1>"


@app.route("/api/python")
def hello_world():
    return "<h2>Hello all!</h2>"


@app.route("/api/message")
def hello_message():
    return "hello message!"


@app.route("/api/online", methods=['POST'])
def streaming_start_detection():
    # Detects the start of a live Twitch broadcast (on webhook)
    if request.method == 'POST':
        data = request.get_json()
        print(request.json)

        # subのchallengeだったら値をそのまま返す
        if data.get("challange"):
            return data.get("challange"), 200

        return "", 200
    else:
        abort(400)


@app.route("/api/test", methods=['GET'])
async def test_function():
    # アクセスするとWebhookのURLを使ってメッセージをポストする
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(os.environ['TEST_WEBHOOK_URL'],
                                   session=session)
        await webhook.send("Hello World")
    return 'test function', 200


app.run(debug=True, port=3000, host='0.0.0.0')  # 0.0.0.0で外部に公開らしい
if __name__ == 'index':
    # 最初に1回だけ走るなにか
    print("Flask is running!")
