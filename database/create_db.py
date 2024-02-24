import sqlite3

# データベースを作成する
dbname = "database/database.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# usersテーブルの作成
# user_id（DiscordのID）、guild_id（サーバーのID）、各日時
cur.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id VARCHAR(32) PRIMARY KEY, guild_id VARCHAR(32), created_at datetime, updated_at datetime, deleted_at datetime)"
)

# guildsテーブルの作成
# guild_id（サーバーのID）、channel_id（チャンネルID）、各日時
cur.execute(
    "CREATE TABLE IF NOT EXISTS guilds (guild_id VARCHAR(32) PRIMARY KEY, channel_id VARCHAR(32), created_at datetime, updated_at datetime, deleted_at datetime)"
)

# streamersテーブルの作成
# streamer_id（通知する配信者のbroadcasterID）、
# streamer_login_id（配信者のloginID（URLに表示されてるやつ））、
# streamer_name（配信者の表示名）
# channel_id（通知が送信されるチャンネルID）、
# is_active（通知がアクティブかどうか）
# 各日時
cur.execute(
    "CREATE TABLE IF NOT EXISTS streamers (streamer_id VARCHAR(32) PRIMARY KEY, streamer_login_id VARCHAR(32), streamer_name VARCHAR(128), channel_id VARCHAR(32), is_active BOOLEAN, created_at datetime, updated_at datetime, deleted_at datetime)"
)

# channelsテーブルの作成
# channel_id（チャンネルID）、channel_name（チャンネル名）、
# guild_id（サーバーのID）、webhook_url（WebhookURL）
# 各日時
cur.execute(
    "CREATE TABLE IF NOT EXISTS channels (channel_id VARCHAR(32) PRIMARY KEY, channel_name VARCHAR(128), guild_id VARCHAR(32), webhook_url VARCHAR(256), created_at datetime, updated_at datetime, deleted_at datetime)"
)

conn.commit()
cur.close()
conn.close()
