import discord
from discord.ext import commands


# ヘルプコマンドの生成
class OriginalHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__(show_hidden=False,
                         command_attrs={"brief": "コマンドのヘルプを表示"})

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="コマンド一覧", brief="コマンドの使い方", color=0x00ff00)

        for cog in mapping:
            if cog is None:
                continue

            print(cog)

            for command in await self.filter_commands(mapping[cog]):
                embed.add_field(name=command.name,
                                value=command.brief,
                                inline=False)

        await self.get_destination().send(embed=embed)
