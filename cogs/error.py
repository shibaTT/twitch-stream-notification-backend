import discord
from discord import app_commands
from discord.ext import commands


# エラーハンドリング
class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.tree.error(coro=self.__dispatch_to_app_command_handler)

    # app_commandのエラーをハンドリングする
    async def __dispatch_to_app_command_handler(
            self, interaction: discord.Interaction,
            error: discord.app_commands.AppCommandError):
        self.bot.dispatch("app_command_error", interaction, error)

    @commands.Cog.listener("on_command_error")
    async def get_command_error(self, ctx, error):
        try:
            raise error
        except commands.PrivateMessageOnly:
            await ctx.send('エラーが発生しました(DM(ダイレクトメッセージ)でのみ実行できます)', hidden=True)
        except commands.NoPrivateMessage:
            await ctx.send('エラーが発生しました(ギルドでのみ実行できます(DMやグループチャットでは実行できません))',
                           hidden=True)
        except commands.NotOwner:
            await ctx.send('エラーが発生しました(Botのオーナーのみ実行できます))', hidden=True)
        except Exception as e:
            await ctx.send(f'エラーが発生しました({e})', hidden=True)

    @commands.Cog.listener("on_app_command_error")
    async def get_app_command_error(
            self, interaction: discord.Interaction,
            error: discord.app_commands.AppCommandError):

        # コマンドに反応していなければ、レスポンスを作成する
        # ただしdeferまで行なっているのであればコマンドに反応しているのと同義
        if not interaction.response.is_done():
            await interaction.response.defer(ephemeral=True)
        try:
            raise error
        except app_commands.CheckFailure:
            await interaction.edit_original_response(
                content='このコマンドを実行する権限がありません')
        except app_commands.CommandNotFound:
            await interaction.edit_original_response(content="コマンドが見つかりません")
        except Exception as e:
            await interaction.edit_original_response(
                content=f'想定外のエラーが発生しました({e})'),


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
    print("error.pyが読み込まれました")
