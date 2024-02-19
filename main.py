# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

# BOT招待URL
# https://discord.com/api/oauth2/authorize?client_id=1203920775376146482&permissions=2147502080&scope=bot

import asyncio
import os

import discord
from discord.ext import commands

import help

# 権限設定
intents = discord.Intents.default()
intents.message_content = True

# コグ一覧
COGS = ["notify", "error"]

# 名前下に表示されるアクティビティの設定
activity = discord.CustomActivity("play /help to help you.",
                                  emoji=discord.PartialEmoji(name="U+261D"))

# botの生成
client = commands.Bot(command_prefix="/",
                      help_command=help.OriginalHelpCommand(),
                      intents=intents,
                      activity=activity)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    # スラッシュコマンドの登録
    if os.getenv("GUILD_ID"):
        guild = discord.Object(id=os.getenv("GUILD_ID"))
        # スラッシュコマンドを登録する（ローカル検証用、即時反映）
        client.tree.copy_global_to(guild=guild)
        await client.tree.sync(guild=guild)
    else:
        # スラッシュコマンドを登録する（反映まで1時間ないくらいかかる）
        await client.tree.sync()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        print("きた！こんちわ！")
        await message.channel.send('Hello!')


# Cogの登録
async def add_cogs():
    for cog in COGS:
        await client.load_extension(cog)

    print("COG読み込み終わり！")


def main():
    token = os.getenv("TOKEN") or ""
    if token == "":
        print(
            "Discord token value is not set. check your .env file or read the manual."
        )
        exit()

    # Extension（Cog）の読み込み
    asyncio.run(add_cogs())

    # クライアントの起動
    print("走り出す………")
    # app.run(debug=True, port=3000, host="0.0.0.0")
    client.run(token)


# botの起動
if __name__ == "__main__":
    main()
