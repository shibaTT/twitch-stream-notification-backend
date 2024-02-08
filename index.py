from flask import Flask, request, abort

app = Flask(__name__)


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
def test_function():
    return "test"


app.run(debug=True, port=3000, host='0.0.0.0')
if __name__ == 'index':
    # 最初に1回だけ走るなにか
    print("Flask is running!")
