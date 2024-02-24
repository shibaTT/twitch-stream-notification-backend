import os
import aiohttp  # 他にいいライブラリがあるならそっち使う
from dotenv import load_dotenv
from database.manage_db import read_streamers, read_channels_webhook
from discord import Webhook

load_dotenv()

async def send_stream_online(streamer_id: str | int):
    """
    配信者が配信を開始したときに通知を送る

    Args:
        streamer_id (str | int): 配信者ID
    """
    streamers = await read_streamers(streamer_id)

    if not streamers:
        return "配信者が見つかりませんでした"

    for streamer in streamers:
        if not streamer[4]:
            # 通知が非アクティブなのでスキップ
            continue

        channels = await read_channels_webhook(streamer[3])

        if not channels or not channels[0][3]:
            # チャンネルが存在しない、またはWebhookのURLが存在しないのでスキップ
            print("チャンネルが存在しない、またはWebhookのURLが存在しないためスキップします")
            continue

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(channels[0][3],
                                    session=session)
            await webhook.send(f"{streamer[2]}の配信が開始されました\nhttps://twitch.tv/{streamer[1]}")
