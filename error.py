import discord
from discord.ext import commands


# エラーハンドリング
class OriginalHelpCommand(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            raise error
        except discord.ext.commands.PrivateMessageOnly:
            await ctx.send('エラーが発生しました(DM(ダイレクトメッセージ)でのみ実行できます)', hidden=True)
        except discord.ext.commands.NoPrivateMessage:
            await ctx.send('エラーが発生しました(ギルドでのみ実行できます(DMやグループチャットでは実行できません))',
                           hidden=True)
        except discord.ext.commands.NotOwner:
            await ctx.send('エラーが発生しました(Botのオーナーのみ実行できます))', hidden=True)
        except:
            await ctx.send(f'エラーが発生しました({error})', hidden=True)


async def setup(bot):
    await bot.add_cog(OriginalHelpCommand(bot))
    print("error.pyが読み込まれました")
