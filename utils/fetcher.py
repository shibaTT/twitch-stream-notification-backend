import os
import urllib.request, urllib.parse, urllib.error
import json
from dotenv import load_dotenv

load_dotenv()


def get_twitch_channel_id(channel_name: str) -> dict:
    # TwitchのチャンネルIDを取得する
    url = 'https://api.twitch.tv/helix/users'
    params = {
        'login': channel_name,
    }

    req = urllib.request.Request('{}?{}'.format(
        url, urllib.parse.urlencode(params)))
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res)
            return {"status": 200, "id": data['data'][0]['id']}
    except urllib.error.HTTPError as error:
        # 4xxエラー、5xxエラー
        return {"status": error.code, "reason": error.reason}
    except urllib.error.URLError as error:
        # 何かしらのエラー
        return {"status": 999, "reason": error.reason}


def subscribe_twitch_channel(twitch_id: str) -> dict:
    base_url = os.getenv("BASEURL")
    twitch_secret = os.getenv("TWITCH_CLIENT_SECRET")

    if not base_url or not twitch_secret:
        return {"status": 999, "reason": "baseurlまたはtwitch_secretが設定されていません"}

    url = 'https://api.twitch.tv/helix/eventsub/subscriptions'
    body = {
        "type": "stream.online",
        "version": "1",
        "condition": {
            "broadcaster_user_id": twitch_id
        },
        "transport": {
            "method": "webhook",
            "callback": base_url + "/api/online",
            "secret": twitch_secret
        }
    }
    headers = {
        'Content-Type': 'application/json',
    }

    req = urllib.request.Request(url, json.dumps(body).encode(), headers)
    try:
        with urllib.request.urlopen(req) as res:
            data = json.loads(res)
            return {"status": 200, "data": data}
    except urllib.error.HTTPError as error:
        # 4xxエラー、5xxエラー
        return {"status": error.code, "reason": error.reason}
    except urllib.error.URLError as error:
        # 何かしらのエラー
        return {"status": 999, "reason": error.reason}
