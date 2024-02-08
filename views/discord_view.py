from typing import Union
import discord

TIMEOUT_TYPE = Union[int, None]


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


# Twitchのチャンネルを追加する
# class TwitchAddView(discord.ui.View):

#     def __init__(self, timeout: TIMEOUT_TYPE = 180):
#         super().__init__(timeout=timeout)

#     @discord.ui.TextInput(label="TwitchのチャンネルID",
#                           placeholder="IDを入れてください",
#                           row=0)
#     async def add_twitch_channel(self, interaction: discord.Interaction,
#                                  textinput: discord.ui.TextInput):
#         await interaction.response.defer()
#         self.value = textinput.value
#         self.stop()
