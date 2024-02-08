import discord
from discord import app_commands
from discord.ext import commands


# Discord UI Kit
class SampleView(discord.ui.View):  # UIキットを利用するためにdiscord.ui.Viewを継承する

    def __init__(self, timeout=180):  # Viewにはtimeoutがあり、初期値は180(s)である
        super().__init__(timeout=timeout)

    @discord.ui.button(label="OK", style=discord.ButtonStyle.success)
    async def ok(self, interaction: discord.Interaction,
                 button: discord.ui.Button):
        # OKボタンの生成と、押された際の挙動の定義
        await interaction.response.edit_message(
            content=f"{interaction.user.mention} OK!", view=None)


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
    async def help(self, interaction):
        """
        ヘルプを表示します
        いつか……………。
        """
        # embed = message.create_bot_help_embed(list(self.bot.commands))
        await interaction.response.defer()
        await interaction.response.send_message("誠意製作中")

    @app_commands.command(name="reload", description="コマンドを再読み込みします")
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            # このコグを再読み込み
            await self.bot.reload_extension('notify')

            # ギルドIDを変換
            guild = discord.Object(id=interaction.guild_id)

            # スラッシュコマンドの再同期
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)

            await interaction.followup.send("コマンドを再読み込みしました")
        except discord.HTTPException as e:
            await interaction.followup.send("エラーが発生しました")
            raise e

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


# bot.run("TOKEN")


# main.pyからExtensionとして呼び出された際に
# 1度だけ実行される
async def setup(bot):
    await bot.add_cog(TwitchNotify(bot))
    print("notify.pyです。cogがadd、もしくはreloadされた気がします")
