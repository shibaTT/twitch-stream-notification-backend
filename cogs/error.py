import discord
from discord import app_commands
from discord.ext import commands


# エラーハンドリング
class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

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
        except:
            await ctx.send(f'エラーが発生しました({error})', hidden=True)

    @commands.Cog.listener("on_app_command_error")
    async def get_app_command_error(self, interaction, error):
        try:
            raise error
        except app_commands.CheckFailure:
            await interaction.response.send_message('このコマンドを実行する権限がありません',
                                                    ephemeral=True)
        except app_commands.CommandNotFound:
            await interaction.response.send_message("コマンドが見つかりません",
                                                    ephemeral=True)
        except Exception as error:
            await interaction.response.send_message(f'想定外のエラーが発生しました({error})'
                                                    ),


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
    print("error.pyが読み込まれました")
