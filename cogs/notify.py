import discord, os
from discord import app_commands
from discord.ext import commands
from views.discord_view import SampleView

from database.manage_db import add_twitch_subscribe


# Modal Test
class SampleModal(discord.ui.Modal, title="Test"):
    name = discord.ui.TextInput(label='Name')
    answer = discord.ui.TextInput(label='Answer',
                                  style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f'Thanks for your response, {self.name}!', ephemeral=True)


class TwitchNotify(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="cat",
        # hidden=False,  # 隠しコマンドかどうか
        # brief="猫を呼び出す",  # 短い説明文
        description="コマンドを使うことで猫を呼び出して、鳴き声を聞くことができます")  # フルの説明文
    async def cat(self, interaction: discord.Interaction):
        # interactionは3秒以内にレスポンスしないといけないとエラーになるのでこの処理を入れる
        await interaction.response.defer()

        await interaction.followup.send("猫でした")

    @app_commands.command(name="help", description="コマンドの一覧を表示します")
    async def help(self, interaction: discord.Interaction):
        """
        ヘルプを表示します
        いつか……………。
        """
        # embed = message.create_bot_help_embed(list(self.bot.commands))
        await interaction.response.defer()
        await interaction.followup.send("誠意製作中", ephemeral=True)

    @app_commands.command(name="reload", description="コマンドを再読み込みします")
    async def reload(self, interaction: discord.Interaction):
        # ephemeral=Trueでメッセージ送った人にだけメッセージ返す
        await interaction.response.defer(ephemeral=True)

        # 全てのコグの再読み込み
        for cog in self.bot.extensions:
            await self.bot.reload_extension(cog)

        # ギルドIDを変換
        guild = discord.Object(id=interaction.guild_id)

        # スラッシュコマンドの再同期
        self.bot.tree.copy_global_to(guild=guild)
        await self.bot.tree.sync(guild=guild)

        await interaction.edit_original_response(content="コマンドを再読み込みしました")

    @app_commands.command(name="interact_test", description="インタラクトテストです")
    @app_commands.describe(your_choice="あなたは何を選ぶ？", your_name="あとあなたの名前は？")
    @app_commands.choices(your_choice=[
        app_commands.Choice(name="猫", value="cat"),
        app_commands.Choice(name="犬", value="dog"),
    ])
    async def interact_test(self, interaction: discord.Interaction,
                            your_choice: app_commands.Choice[str],
                            your_name: str):
        await interaction.response.defer()
        await interaction.followup.send("あなたは" + your_choice.name + "を選んだ" +
                                        your_name + "です")

    @app_commands.command(name="button_test", description="ボタンテストです")
    async def button_test(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await interaction.followup.send("ボタンテストです",
                                        view=SampleView(timeout=20))

    @app_commands.command(name="modal_test", description="モーダルテストです")
    async def modal_test(self, interaction: discord.Interaction):
        # await interaction.response.defer() # ←これを入れると2回目のresponseはエラーになる
        await interaction.response.send_modal(SampleModal())

    @app_commands.command(name="add_twitch_channel",
                          description="通知するTwitchチャンネルを追加します")
    @app_commands.describe(twitch_id="TwitchのIDを入力してください",
                           server_channel="送信するDiscordのチャンネル名を選択してください")
    # @app_commands.checks.bot_has_permissions(manage_webhooks=True)
    async def _add_twitch_channel(self, interaction: discord.Interaction,
                                  twitch_id: str,
                                  server_channel: discord.TextChannel):
        # どうやらtextInputはインタラクションでは使えない様子？Modalのみサポートっぽい
        # なので、普通にコマンドでやるのがいいかも
        # command_view = TwitchAddView(timeout=None)
        # await interaction.response.send_message("", view=command_view)
        # await interaction.followup.send(command_view.value)

        await interaction.response.defer()
        botInfo = await self.bot.application_info()
        result_message = await add_twitch_subscribe(twitch_id,
                                                    interaction.guild_id,
                                                    server_channel,
                                                    interaction.user.id,
                                                    botInfo.icon)

        if result_message:
            await interaction.edit_original_response(content="エラーが発生しました。" +
                                                     result_message)
        else:
            await interaction.edit_original_response(content="登録に成功しました")

    @commands.command(name="notification",
                      description="Description of the notification command")
    async def notification(self, ctx, caster_id: str):
        # broadcaster_idに紐づけられているチャンネルIDのリストを取得する
        channel = discord.utils.get(self.bot.get_all_channels(),
                                    guild__id=os.getenv("GUILD_ID"),
                                    id="1203920926366769216")
        print("CHANNEL INFO is", channel)
        print(self.bot.get_guild(os.getenv("GUILD_ID")))


# bot.run("TOKEN")


# main.pyからExtensionとして呼び出された際に
# 1度だけ実行される
async def setup(bot):
    await bot.add_cog(TwitchNotify(bot))
    print("notify.pyが読み込まれました")
