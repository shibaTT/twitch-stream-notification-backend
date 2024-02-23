import os
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import discord
from utils.fetcher import get_twitch_channel_id, subscribe_twitch_channel


class DatabaseConnector:
    DB_NAME = "database/database.db"

    def __init__(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, *args):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


async def add_twitch_subscribe(twitch_name: str, guild_id: str | int,
                               channel: discord.TextChannel,
                               user_id: str | int, avatar) -> str | None:
    """
    Twitchの配信者の配信開始のサブスクをしてDBに登録する

    ついでにDiscordのテキストチャンネルにWebhookの登録をし、それをDBにも登録する

    twitch_name: Twitchのユーザー名,
    guild_id: 通知するサーバーのID,
    channel: 通知するチャンネル情報
    user_id: コマンド送信ユーザーのID,
    avatar: コマンド送信ユーザーのアバターアイコン
    """

    # TODOS:
    # DBにIDが登録されているかチェックする　ok
    #  - DBに登録されていなければ、IDが存在するかチェックする ok
    #    - IDが存在すれば、TwitchAPIにWebhookのサブスクライブをし、DBに登録する ok
    #  - DBに登録されていれば、サブスクライバーテーブルにチャンネルIDを追加する ok
    #    - チャンネルIDではなく、当該チャンネルにWebhookを送信するための ok
    #      URLを取得して保存する方針に変えます
    # Webhookで送信するためにはまずチャンネルに対してcreate_webhookをする必要がある
    # その際に、アバター写真やユーザー名を設定する必要があるが、
    # そのためにはClient.application_info()を設定し、
    # nameやiconなどを取得して設定するのが丸いと思う
    # ただし、後からBOT名などを変えても反映はされないので注意

    with DatabaseConnector() as db:
        # ユーザーにチャンネルを紐づける
        users_result = db.execute(
            "SELECT * FROM users WHERE user_id = ? AND guild_id = ?",
            (user_id, guild_id)).fetchall()
        print("users", users_result)
        if len(users_result) > 0:
            # 既に紐づいているのでパス
            pass
        else:
            # まだ紐づいていないのでDBに登録する
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                       (user_id, guild_id, now, now, ""))

        # ギルドにチャンネルを紐づける
        guilds_result = db.execute(
            "SELECT * FROM guilds WHERE guild_id = ? AND channel_id = ?",
            (guild_id, channel.id)).fetchall()
        print("guilds", guilds_result)
        if len(guilds_result) > 0:
            # 既に紐づいているのでパス
            pass
        else:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.execute("INSERT INTO guilds VALUES (?, ?, ?, ?, ?)",
                       (guild_id, channel.id, now, now, ""))

        # 通知する配信者とチャンネルをDBに登録する
        subscribe_result = db.execute(
            "SELECT * FROM streamers WHERE streamer_id = ?",
            (twitch_name, )).fetchall()
        print("stream", subscribe_result)
        if len(subscribe_result) > 0:
            # すでにDBに登録されている ＝ すでにサブスクライブ済み
            # なので、既に通知まで登録済みでなければDBに登録だけする
            if channel.id not in (x[1] for x in subscribe_result):
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                db.execute(
                    "INSERT INTO streamers VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (subscribe_result[0][0], twitch_name, channel.id, True,
                     now, now, ""))

        else:
            # 登録されていない場合はTwitchにサブスクライブする
            twitch_id = get_twitch_channel_id(twitch_name)

            # 取得できなかったらエラー
            if twitch_id["status"] != 200:
                return twitch_id["reason"]

            result = subscribe_twitch_channel(twitch_id["id"])

            # 取得できなかったらエラー
            if result["status"] != 200:
                return result["reason"]

            # 配信者ID・配信者名・通知先チャンネルIDを登録する
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.execute(
                "INSERT INTO streamers VALUES (?, ?, ?, ?, ?, ?, ?)",
                (twitch_id["id"], twitch_name, channel.id, True, now, now, ""))

        # チャンネルテーブルに該当のチャンネルIDあるかどうか
        channels_result = db.execute(
            "SELECT * FROM channels WHERE channel_id = ?",
            (str(channel.id),)).fetchall()
        print("channels", channels_result)

        if len(channels_result) > 0:
            # 既にチャンネル登録済みであれば無視
            pass
        else:
            # まだチャンネルがなければ作成する
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                webhook_result = await channel.create_webhook(
                    name="Twitch配信開始通知", avatar=avatar)
            except discord.Forbidden:
                return "BotにWebhookを作成する権限がありません"
            except discord.HTTPException:
                return "Webhookの作成に失敗しました"

            db.execute("INSERT INTO channels VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (channel.id, channel.name, guild_id, webhook_result.url,
                        now, now, ""))
