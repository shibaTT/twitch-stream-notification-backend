import os
from flask import Flask, request, abort
from notify import TwitchNotify
from discord import Webhook
from discord.ext import commands
import aiohttp  # 他にいいライブラリがあるならそっち使う

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
        print(request.json)
        return 'thank you post', 200
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


app.run(debug=True, port=3000, host='0.0.0.0')
if __name__ == 'index':
    # 最初に1回だけ走るなにか
    print("Flask is running!")
