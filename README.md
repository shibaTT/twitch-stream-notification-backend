# Python Discord Bot

This is a starting point for making your own Discord bot using Python and the [discordpy](https://discordpy.readthedocs.io/) library.
Read [their getting-started guides](https://discordpy.readthedocs.io/en/stable/#getting-started) to get the most out of this template.

## Getting Started

To get set up, you'll need to follow [these bot account setup instructions](https://discordpy.readthedocs.io/en/stable/discord.html),
and then copy the token for your bot and added it as a secret with the key of `TOKEN` in the "Secrets (Environment variables)" panel.

`.env` に記述すべき事項

-   TOKEN: (MUST)Discord のシークレットトークン
-   GUILD_ID: デバッグしたいギルドの ID、なくてもいいがスラッシュコマンドの即時反映のために欲しい
-   TWITCH_CLIENT_ID: TwitchのクライアントID
-   TWITCH_CLIENT_SECRET: Twitchの秘密鍵
-   BASEURL: このアプリケーションが動作するベースとなるURL（origin）

## FAQ

If you get the following error message while trying to start the server: `429 Too Many Requests` (accompanied by a lot of HTML code),
try the advice given in this Stackoverflow question:
https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests
