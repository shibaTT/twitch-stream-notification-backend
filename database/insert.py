import sqlite3

###########################################
# テスト用のDB操作ファイル
#

# データベースを作成する
dbname = "database/database.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# streamersテーブルの作成
# streamer_id（通知する配信者のbroadcasterID）、
# streamer_login_id（配信者のloginID（URLに表示されてるやつ））、
# streamer_name（配信者の表示名）
# channel_id（通知が送信されるチャンネルID）、
# is_active（通知がアクティブかどうか）
# 各日時
cur.execute(
    "INSERT INTO streamers VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    ("777", "k4sen", "k4sen", "151214773801844737", True, "2024-01-01 10:00:00", "2024-01-01 10:00:00", ""))


cur.close()
# データベースを閉じる
conn.commit()
conn.close()
