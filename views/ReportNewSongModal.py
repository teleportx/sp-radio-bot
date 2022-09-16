import datetime

import nextcord
from nextcord import Embed
from nextcord.types.channel import Channel

from views.ReportNewSongAdminButtons import ReportNewSongAdminButtonsView


class ReportNewSongModal(nextcord.ui.Modal):
    def __init__(self, report_channel: Channel, get_user_function: callable):
        self.report_channel = report_channel
        self.get_user_function = get_user_function

        super().__init__('Заявка на добавление новой песни')

        self.author = nextcord.ui.TextInput(
            label='Автор песни',
            style=nextcord.TextInputStyle.short,
            placeholder='Матушка',
            required=True,
            max_length=100,
        )

        self.full_title = nextcord.ui.TextInput(
            label='Полное название песни',
            style=nextcord.TextInputStyle.short,
            placeholder='Название - Альбом',
            required=True,
            max_length=400,
        )

        self.url = nextcord.ui.TextInput(
            label='Ссылка на песню',
            style=nextcord.TextInputStyle.short,
            placeholder='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            required=True,
            max_length=400
        )

        self.lyrics = nextcord.ui.TextInput(
            label='Лириксы песни',
            style=nextcord.TextInputStyle.paragraph,
            required=False,
            max_length=3000
        )

        self.add_item(self.author)
        self.add_item(self.full_title)
        self.add_item(self.url)
        self.add_item(self.lyrics)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        author = self.author.value
        full_title = self.full_title.value
        url = self.url.value
        lyrics = self.lyrics.value

        embed = Embed(
            title='Заявка на песню',
            description='**LYRICS**\n\n' + lyrics,
            timestamp=datetime.datetime.now()
        )

        embed.add_field(name='Author', value=author)
        embed.add_field(name='Full title', value=full_title)
        embed.add_field(name='Song URL', value=url)

        view = ReportNewSongAdminButtonsView(self.get_user_function)
        await self.report_channel.send(str(interaction.user.id), embed=embed, view=view)

        await interaction.edit(content='Ваша заявка принята!', view=None)
