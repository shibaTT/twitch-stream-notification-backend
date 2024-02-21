import os
import sqlite3


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


def add_twitch_subscribe(twitch_id, channel_id):
    # Twitchの配信者の配信開始のサブスクをしてDBに登録する

    # TODOS:
    # DBにIDが登録されているかチェックする
    #  - DBに登録されていなければ、IDが存在するかチェックする
    #    - IDが存在すれば、TwitchAPIにWebhookのサブスクライブをし、DBに登録する
    #  - DBに登録されていれば、サブスクライバーテーブルにチャンネルIDを追加する
    #    - チャンネルIDではなく、当該チャンネルにWebhookを送信するための
    #      URLを取得して保存する方針に変えます
    # Webhookで送信するためにはまずチャンネルに対してcreate_webhookをする必要がある
    # その際に、アバター写真やユーザー名を設定する必要があるが、
    # そのためにはClient.application_info()を設定し、
    # nameやiconなどを取得して設定するのが丸いと思う
    # ただし、後からBOT名などを変えても反映はされないので注意

    with DatabaseConnector() as db:
        subscribe_result = db.execute(
            "SELECT * FROM streamers WHERE streamer_id = ?",
            (twitch_id)).fetchall()

        if len(subscribe_result) > 0:
            # すでに登録されている
            return False
        else:
            # 登録されていない
            return True
