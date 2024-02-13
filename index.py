from flask import Flask, request, abort
from notify import TwitchNotify
import main
from discord.ext import commands

import sys, asyncio

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
        print(request.json)
        return 'thank you post', 200
    else:
        abort(400)


@app.route("/api/test", methods=['GET'])
async def test_function():
    await main.pass_notify("caster_id")
    return "ok"


app.run(debug=True, port=3000, host='0.0.0.0')

if __name__ == 'index':
    # 最初に1回だけ走るなにか
    print("Flask is running!")
